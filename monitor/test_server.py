import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from monitor import server


class MonitorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write('site/dist/data.json', {
            'revision': 'test', 'questions': [
                {'id': 'q-001', 'title': '已完成', 'verification': '原題已核對', 'contentStatus': '完整原題'},
                {'id': 'q-002', 'title': '有疑義', 'verification': '待核對', 'contentStatus': '完整原題',
                 'reviewQuestions': ['請確認選項用詞。']},
            ]})
        self.write('docs/imports/todo-progress.json', {'sources': [self.source(1, 'complete')]})
        self.write('docs/imports/more-gpt-progress.json', {'sources': [
            self.source(1, 'complete', questionIds=['q-001']),
            self.source(2, 'duplicate'),
            self.source(3, 'partial', archiveImages=3, downloadedImages=[{'path': 'one.jpg'}], questionIds=['q-002']),
            self.source(4, 'awaiting_transcription'),
        ]})
        self.write('docs/imports/more-gemini-progress.json', {'sources': [
            self.source(1, 'awaiting_source_read'), self.source(2, 'awaiting_source_read')]})
        self.write('monitor/activity.json', {'title': '目前工作', 'detail': '核對原圖', 'updatedAt': '2026-10-27T00:00:00Z'})
        self.write('monitor/confirmations.json', {'requests': [
            {'id': 'ask', 'state': 'pending', 'title': '待確認', 'kind': '存取', 'questions': ['看得到原圖嗎？']},
            {'id': 'done', 'state': 'resolved', 'title': '已確認'},
        ], 'resolved': []})

    @staticmethod
    def source(order, state, **extra):
        return {'order': order, 'state': state, 'url': 'https://example.com/'+str(order), 'title': '來源', **extra}

    def write(self, relative, value):
        p = self.root/relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value, ensure_ascii=False))

    def tearDown(self):
        self.tmp.cleanup()

    def test_new_source_denominator_excludes_original_todo(self):
        status = server.build_status(self.root)
        self.assertEqual(status['summary']['newSourcesTotal'], 6)
        self.assertEqual(status['summary']['newSourcesSettled'], 2)
        self.assertEqual(status['summary']['percent'], 33.3)
        self.assertEqual(status['batches'][1]['partial'], 1)
        self.assertEqual(status['batches'][1]['excluded'], 1)

    def test_complete_text_can_still_require_teacher_confirmation(self):
        status = server.build_status(self.root)
        self.assertEqual(status['summary']['questions'], 2)
        self.assertEqual(status['summary']['verifiedQuestions'], 1)
        self.assertEqual([c['id'] for c in status['confirmations']], ['q-002', 'ask'])
        self.assertEqual(status['confirmations'][0]['url'], '/site/index.html#question/q-002')
        self.assertEqual(status['imageRetries'][0]['imagesAvailable'], 1)

    def test_rereads_records_instead_of_cached_counts(self):
        first = server.build_status(self.root)
        self.write('docs/imports/more-gemini-progress.json', {'sources': [self.source(1, 'complete'), self.source(2, 'skipped_missing_images')]})
        second = server.build_status(self.root)
        self.assertEqual(second['summary']['newSourcesSettled'], first['summary']['newSourcesSettled']+2)

    def test_recent_comics_use_completion_time_and_only_five_finished_items(self):
        entries = [dict(id=f'q-{n:03}', subject='Chinese', title=str(n),
                        date='2026-10-01', state='complete',
                        completedAt=f'2026-10-{8-n:02}T00:00:00Z') for n in range(1, 8)]
        entries.append(dict(id='q-008', subject='Chinese', title='Not finished',
                            date='2026-10-01', state='reviewing',
                            completedAt='2026-10-28T00:00:00Z'))
        self.write('docs/comics/progress.json', {'entries': entries})
        recent = server.build_status(self.root)['comics']['recent']
        self.assertEqual([e['id'] for e in recent], [f'q-{n:03}' for n in range(1, 6)])

    def test_comic_status_reports_squared_completion_priority(self):
        entries = [dict(id=f'q-{n:03}', subject='Chinese', title=str(n),
                        date='2026-10-01', state='complete' if n < 10 else 'queued') for n in range(100)]
        entries += [dict(id=f'q-{100+n:03}', subject='Earth', title=str(n),
                         date='2026-10-01', state='complete' if n < 2 else 'queued') for n in range(10)]
        self.write('docs/comics/progress.json', {'entries': entries})
        comics = server.build_status(self.root)['comics']
        self.assertEqual(comics['next']['subject'], 'Earth')
        self.assertEqual(comics['subjects'][0]['completed'], 2)
        self.assertEqual(comics['subjects'][0]['priorityScore'], .4)

    def test_acquisition_does_not_mark_sources_or_questions_curated(self):
        first = server.build_status(self.root)
        self.write('monitor/acquisition.json', {
            'state': 'complete', 'title': '背景取資料', 'completed': 1, 'total': 1,
            'sources': [{'order': 4, 'state': 'acquired', 'imagesAvailable': 9}],
        })
        second = server.build_status(self.root)
        self.assertEqual(second['summary'], first['summary'])
        self.assertEqual(second['batches'][1]['sources'][3]['state'], 'awaiting_transcription')
        self.assertEqual(second['acquisition'][0]['completed'], 1)

    def test_static_paths_cannot_leave_public_site(self):
        base = self.root/'site/dist'
        (base/'index.html').write_text('public')
        (self.root/'secret').write_text('private')
        (base/'escape.txt').symlink_to(self.root/'secret')
        self.assertEqual(server.safe_file(base, 'index.html'), base/'index.html')
        for name in ('../../secret', '/etc/passwd', '.env', 'escape.txt', 'foo/../index.html', '..\\secret'):
            self.assertIsNone(server.safe_file(base, name))

    def test_confirmation_persists_snapshot_and_is_idempotent(self):
        pending = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
        result = server.resolve_confirmation('ask', pending['confirmationToken'], self.root)
        self.assertEqual(result['state'], 'resolved')
        self.assertIn('確認 OK', result['resolution'])
        self.assertNotIn('ask', [c['id'] for c in server.build_status(self.root)['confirmations']])
        server.resolve_confirmation('ask', pending['confirmationToken'], self.root)
        records = server.read_json(self.root/'monitor/confirmations.json')
        self.assertEqual(len(records['resolved']), 1)
        self.assertEqual(records['resolved'][0]['questions'], ['看得到原圖嗎？'])

    def test_old_card_cannot_approve_changed_content(self):
        token = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')['confirmationToken']
        records = server.read_json(self.root/'monitor/confirmations.json')
        records['requests'][0]['questions'] = ['更新後的問題']
        self.write('monitor/confirmations.json', records)
        with self.assertRaises(server.ConfirmationConflict):
            server.resolve_confirmation('ask', token, self.root)
        self.assertEqual(server.read_json(self.root/'monitor/confirmations.json')['resolved'], [])

    def test_simultaneous_confirmations_do_not_lose_records(self):
        cards = server.build_status(self.root)['confirmations']
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(server.resolve_confirmation, c['id'], c['confirmationToken'], self.root)
                       for c in cards]
            for future in futures:
                future.result()
        records = server.read_json(self.root/'monitor/confirmations.json')
        self.assertEqual({r['id'] for r in records['resolved']}, {'q-002', 'ask'})
        self.assertEqual(server.build_status(self.root)['confirmations'], [])

    def test_question_acknowledgement_does_not_fabricate_completed_content(self):
        pending = server.build_status(self.root)['confirmations'][0]
        server.resolve_confirmation('q-002', pending['confirmationToken'], self.root)
        self.assertEqual([c['id'] for c in server.build_status(self.root)['confirmations']], ['ask'])
        data = server.read_json(self.root/'site/dist/data.json')
        self.assertEqual(data['questions'][1]['verification'], '待核對')
        data['questions'][1]['reviewQuestions'] = ['另一項原題問題']
        self.write('site/dist/data.json', data)
        self.assertIn('q-002', [c['id'] for c in server.build_status(self.root)['confirmations']])

    def test_review_navigation_changes_do_not_reopen_confirmed_question(self):
        data = server.read_json(self.root/'site/dist/data.json')
        question = data['questions'][1]
        question.update(reviewLabel='優先核對 2／3', reviewPreviousId='q-001', reviewNextId='q-003')
        self.write('site/dist/data.json', data)
        card = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'q-002')
        question.update(reviewLabel='優先核對 1／1', reviewPreviousId='', reviewNextId='')
        self.write('site/dist/data.json', data)
        server.resolve_confirmation('q-002', card['confirmationToken'], self.root)
        question.update(reviewLabel='優先核對 1／2', reviewNextId='q-004')
        self.write('site/dist/data.json', data)
        self.assertNotIn('q-002', [c['id'] for c in server.build_status(self.root)['confirmations']])
        question['answer'] = '真正修改後的答案'
        self.write('site/dist/data.json', data)
        self.assertIn('q-002', [c['id'] for c in server.build_status(self.root)['confirmations']])

    def test_http_confirmation_requires_explicit_action_and_checks_origin(self):
        with patch.object(server, 'ROOT', self.root):
            http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
            thread = threading.Thread(target=http.serve_forever, daemon=True)
            thread.start()
            base = f'http://127.0.0.1:{http.server_port}'
            pending = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
            body = json.dumps({'id': 'ask', 'confirmationToken': pending['confirmationToken']}).encode()
            headers = {'Content-Type': 'application/json', 'X-TestReview-Action': 'confirm', 'Origin': base}
            try:
                for invalid, expected in [({'Content-Type': 'application/json'}, 403),
                                          ({**headers, 'Origin': 'https://unrelated.example'}, 403),
                                          ({**headers, 'Content-Type': 'text/plain'}, 415)]:
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        urllib.request.urlopen(urllib.request.Request(base+'/api/confirm', data=body, headers=invalid))
                    self.assertEqual(caught.exception.code, expected)
                for _ in range(2):
                    with urllib.request.urlopen(urllib.request.Request(base+'/api/confirm', data=body, headers=headers)) as response:
                        self.assertEqual(json.load(response), {'ok': True, 'id': 'ask'})
                self.assertEqual(len(server.read_json(self.root/'monitor/confirmations.json')['resolved']), 1)
            finally:
                http.shutdown()
                http.server_close()
                thread.join()

    def test_http_status_health_static_and_read_only(self):
        (self.root/'monitor/index.html').write_text('<h1>Monitor</h1>')
        (self.root/'site/dist/index.html').write_text('<h1>題庫</h1>')
        with patch.object(server, 'ROOT', self.root), patch.object(server, 'build_status', lambda: {'summary': {'questions': 2}}):
            http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
            thread = threading.Thread(target=http.serve_forever, daemon=True)
            thread.start()
            base = f'http://127.0.0.1:{http.server_port}'
            try:
                with urllib.request.urlopen(base+'/api/status') as response:
                    self.assertEqual(json.load(response)['summary']['questions'], 2)
                    self.assertEqual(response.headers['Cache-Control'], 'no-store')
                for path in ('/health', '/', '/site/index.html'):
                    with urllib.request.urlopen(base+path) as response:
                        self.assertEqual(response.status, 200)
                for path, method, expected in [('/docs/imports/more-gpt-progress.json', 'GET', 404),
                                               ('/site/%2e%2e/monitor/activity.json', 'GET', 404),
                                               ('/api/status', 'POST', 405)]:
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        urllib.request.urlopen(urllib.request.Request(base+path, method=method))
                    self.assertEqual(caught.exception.code, expected)
            finally:
                http.shutdown()
                http.server_close()
                thread.join()


if __name__ == '__main__':
    unittest.main()
