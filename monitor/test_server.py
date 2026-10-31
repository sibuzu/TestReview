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

    def test_group_review_counts_remain_separate_from_published_bank_and_comics(self):
        self.write('site/dist/data.json',{'revision':'test','questions':[
            {'id':'q-001','title':'子題一'},{'id':'q-002','title':'子題二'}],
            'subjects':[{'id':'Chinese','name':'國文'},{'id':'Math','name':'數學'}]})
        self.write('docs/imports/group-review/queue.json',{'baselineQuestionIds':['q-001','q-002'],
            'candidates':[{'id':'candidate-1','state':'confirmed'},
                {'id':'candidate-2','state':'reviewing','owner':'worker2','questionIds':['q-002']}],
            'groups':[{'id':'group-1','questionIds':['q-001','q-002'],'subject':'Chinese','state':'confirmed'}]})
        d=server.build_status(self.root);g=d['groupReview']
        self.assertEqual(d['summary']['questions'],2)
        self.assertEqual((g['candidates'],g['reviewed'],g['confirmedGroups'],g['groupedQuestions']),(2,1,1,2))
        self.assertFalse(g['reviewComplete']);self.assertEqual(g['subjects'][1]['groups'],0)
        self.assertEqual(g['groups'][0]['questions'][1]['url'],'/site/index.html#question/q-002')

    def test_current_new_sources_use_plan_and_local_acquisition_reports(self):
        self.write('docs/imports/new-source-plan-2026-10-29.json', {'sources': [
            {'key': 'new1', 'suggestedOrder': 1, 'url': 'https://example.com/1'},
            {'key': 'new2', 'suggestedOrder': 2, 'url': 'https://example.com/2'}]})
        original = self.root/'docs/original.jpg'
        original.parent.mkdir(exist_ok=True)
        original.write_bytes(b'local-acquisition-fixture')
        self.write('docs/imports/more-gemini-progress.json', {'sources': [
            self.source(1, 'complete', sourceCurationComplete=True, questionIds=['q-001'],
                        archiveImages=1, downloadedImages=[{'path': 'docs/original.jpg'}]),
            self.source(2, 'partial', questionIds=['q-002'])]})
        self.write('docs/acquisition/gemini-002.json', {
            'title': '已取回文字，圖片未完成', 'imagesExpected': 2,
            'downloadedImages': [{'path': 'docs/missing-original.jpg'}]})
        status = server.build_status(self.root)['newSources']
        self.assertEqual((status['settled'], status['total'], status['percent']), (1, 2, 50))
        self.assertEqual((status['imagesAvailable'], status['acquiredSources']), (1, 1))
        self.assertEqual(status['published'], 2)
        self.assertEqual(status['awaitingConfirmation'], 1)
        self.assertEqual(status['sources'][1]['title'], '已取回文字，圖片未完成')

    def test_current_new_sources_absent_without_assignment_plan(self):
        self.assertIsNone(server.build_status(self.root)['newSources'])

    def test_active_gpt_assignment_does_not_read_same_order_gemini(self):
        self.write('monitor/active-source-plan.json', {'path': 'docs/imports/current-gpt.json'})
        self.write('docs/imports/current-gpt.json', {'sources': [
            {'key': 'gpt004', 'batch': 'gpt', 'suggestedOrder': 4,
             'sourceId': 'src-more-004', 'expectedOriginalQuestions': 2,
             'url': 'https://chatgpt.com/share/new',
             'acquisitionRecord': 'docs/acquisition/current.json'}]})
        self.write('site/dist/data.json', {'revision': 'group', 'questions': [
            {'id': 'q-001', 'title': '完整題組', 'sourceId': 'src-more-004',
             'verification': '原題已核對', 'contentStatus': '完整原題',
             'groupQuestions': [{'id': 'q-001'}, {'id': 'q-009'}]}]})
        self.write('docs/imports/more-gemini-progress.json', {'sources': [self.source(4, 'complete')]})
        self.write('docs/acquisition/current.json', {
            'userImagesExpected': 1, 'originalImages': [{'path': 'original.jpg'}]})
        (self.root/'original.jpg').write_bytes(b'original')
        result = server.build_status(self.root)
        source = result['newSources']['sources'][0]
        self.assertEqual(source['batch'], 'gpt')
        self.assertEqual(source['state'], 'awaiting_transcription')
        self.assertEqual(result['newSources']['settled'], 0)
        self.assertEqual(result['newSources']['imagesExpected'], 1)
        self.assertEqual(result['newSources']['published'], 1)
        self.assertEqual(result['newSources']['originalsPublished'], 2)
        self.assertEqual(result['newSources']['originalsExpected'], 2)
        batches = {batch['id']: batch for batch in result['batches']}
        self.assertEqual(batches['gemini']['sources'][0]['state'], 'complete')
        self.assertEqual(batches['gpt']['sources'][3]['imagesAvailable'], 1)

    def test_import_pause_is_explicit_without_pausing_comic_production(self):
        self.write('monitor/import-control.json', {'state': 'paused', 'lastAllowedSourceOrder': 63})
        self.write('docs/comics/progress.json', {'entries': [dict(
            id='q-001',subject='Chinese',title='既有題',date='2026-01-01',state='queued')]})
        self.write('monitor/parallel.json', {'lanes': [
            dict(lane=2,role='import',state='importing',title='整理來源'),
            dict(lane=3,role='production',state='running',questionId='q-001',title='製圖')]})
        status=server.build_status(self.root)
        self.assertEqual(status['importControl']['state'],'paused')
        self.assertEqual(status['comics']['parallel']['lanes'][0]['state'],'paused')
        self.assertEqual(status['comics']['parallel']['lanes'][1]['state'],'running')
        self.assertEqual(status['summary']['questions'],2)
        self.assertEqual(status['comics']['active'][0]['id'],'q-001')

    def test_blocked_comic_counts_unresolved_questions_once_and_stops_after_ok(self):
        self.write('docs/comics/progress.json', {'entries': [dict(
            id='q-001', subject='Chinese', title='待核對譯文', date='2026-01-01', state='queued')]})
        self.write('docs/comics/pipeline.json', {'jobs': [dict(
            id='q-001', state='blocked', decision='awaiting_confirmation')]})
        self.write('monitor/confirmations.json', {'requests': [dict(
            id='review-'+str(i), questionId='q-001', state='pending', title='譯文',
            kind='白話譯文指涉核對', questions=['請核對']) for i in range(2)], 'resolved': []})
        pipeline_before = (self.root/'docs/comics/pipeline.json').read_bytes()
        status = server.build_status(self.root)
        self.assertEqual(status['comics']['awaitingConfirmation'], 1)
        for card in status['confirmations']:
            if card['id'].startswith('review-'):
                server.resolve_confirmation(card['id'], card['confirmationToken'], root=self.root)
        self.assertEqual(server.build_status(self.root)['comics']['awaitingConfirmation'], 0)
        self.assertEqual((self.root/'docs/comics/pipeline.json').read_bytes(), pipeline_before)

    def test_comic_confirmation_deduplicates_progress_layout_and_pipeline(self):
        self.write('docs/comics/progress.json', {'entries': [dict(
            id='q-002', subject='Chinese', title='待確認', date='2026-01-01', state='awaiting_confirmation')]})
        self.write('docs/comics/pipeline.json', {'jobs': [dict(
            id='q-002', state='blocked', decision='awaiting_confirmation')]})
        self.write('monitor/confirmations.json', {'requests': [dict(
            id='layout', questionId='q-002', state='pending', title='排版', kind='漫畫排版確認',
            questions=['請核對'])], 'resolved': []})
        self.assertEqual(server.build_status(self.root)['comics']['awaitingConfirmation'], 1)

    def test_new_source_counts_published_bank_and_unpublished_source_confirmation(self):
        self.write('docs/imports/new-source-plan-2026-10-29.json', {'sources': [
            {'key': 'gemini001', 'suggestedOrder': 1, 'url': 'https://example.com/1'}]})
        data = server.read_json(self.root/'site/dist/data.json')
        data['questions'][0]['sourceId'] = 'src-gemini-more-001'
        self.write('site/dist/data.json', data)
        self.write('monitor/confirmations.json', {'requests': [
            {'id': 'missing-original', 'state': 'pending', 'title': '尚未收入的題目缺字',
             'sourceKey': 'gemini001', 'questions': ['請核對原圖']}], 'resolved': []})
        status = server.build_status(self.root)
        self.assertEqual(status['newSources']['published'], 1)
        self.assertEqual(status['newSources']['awaitingConfirmation'], 1)
        self.assertEqual(status['batches'][2]['sources'][0]['questions'][0]['id'], 'q-001')
        self.assertFalse(status['batches'][2]['sources'][0]['settled'])

    def test_source_list_displays_local_acquisition_without_claiming_curation(self):
        self.write('docs/imports/new-source-plan-2026-10-29.json', {'sources': [
            {'key': 'new1', 'suggestedOrder': 1, 'url': 'https://example.com/1'}]})
        original = self.root/'docs/original.jpg'
        original.parent.mkdir(exist_ok=True)
        original.write_bytes(b'original')
        self.write('docs/acquisition/gemini-001.json', {
            'title': '已取回的歷史原卷', 'imagesExpected': 1,
            'downloadedImages': [{'path': 'docs/original.jpg'}]})
        original_progress = (self.root/'docs/imports/more-gemini-progress.json').read_bytes()
        status = server.build_status(self.root)
        row = status['batches'][2]['sources'][0]
        self.assertEqual(row['title'], '已取回的歷史原卷')
        self.assertEqual(row['state'], 'awaiting_transcription')
        self.assertEqual(row['stateLabel'], '原圖已取得／待整理')
        self.assertEqual((row['imagesAvailable'], row['imagesExpected']), (1, 1))
        self.assertEqual(row['questions'], [])
        self.assertFalse(row['settled'])
        self.assertEqual(status['newSources']['settled'], 0)
        self.assertEqual(status['newSources']['published'], 0)
        self.assertEqual((self.root/'docs/imports/more-gemini-progress.json').read_bytes(), original_progress)

    def test_missing_acquired_file_does_not_advance_source_state(self):
        self.write('docs/imports/new-source-plan-2026-10-29.json', {'sources': [
            {'key': 'new1', 'suggestedOrder': 1, 'url': 'https://example.com/1'}]})
        self.write('docs/acquisition/gemini-001.json', {
            'title': '缺圖來源', 'imagesExpected': 1,
            'downloadedImages': [{'path': 'docs/not-downloaded.jpg'}]})
        status = server.build_status(self.root)
        row = status['batches'][2]['sources'][0]
        self.assertEqual(row['state'], 'awaiting_source_read')
        self.assertEqual((row['imagesAvailable'], row['imagesExpected']), (0, 1))
        self.assertEqual(status['newSources']['acquiredSources'], 0)

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

    def test_comment_stays_pending_and_is_preserved_until_addressed(self):
        card = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
        note = '請補原圖，答案先保留 B。'
        first = server.submit_confirmation_comment('ask', card['confirmationToken'], note, self.root)
        again = server.submit_confirmation_comment('ask', card['confirmationToken'], note, self.root)
        self.assertEqual(first, again)
        records = server.read_json(self.root/'monitor/confirmations.json')
        self.assertEqual(records['resolved'], [])
        self.assertEqual(len(records['feedback']), 1)
        current = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
        self.assertTrue(current['feedbackPending'])
        self.assertEqual(current['userComments'][0]['text'], note)
        self.assertEqual(current['confirmationToken'], card['confirmationToken'])
        result = server.resolve_confirmation('ask', current['confirmationToken'], self.root,
                                             resolution='已依意見補齊原圖，保留 B。')
        self.assertEqual(result['userComments'][0]['text'], note)
        self.assertEqual(result['userComments'][0]['state'], 'addressed')
        self.assertEqual(server.read_json(self.root/'monitor/confirmations.json')['feedback'][0]['state'], 'addressed')
        self.assertNotIn('ask', [c['id'] for c in server.build_status(self.root)['confirmations']])

    def test_comment_on_generated_question_does_not_duplicate_card(self):
        card = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'q-002')
        server.submit_confirmation_comment(card['id'], card['confirmationToken'], '補上 C 選項。', self.root)
        cards = server.build_status(self.root)['confirmations']
        self.assertEqual(sum(c['id'] == 'q-002' for c in cards), 1)
        self.assertEqual(next(c for c in cards if c['id'] == 'q-002')['userComments'][0]['text'], '補上 C 選項。')

    def test_late_comment_after_approval_reopens_for_followup(self):
        card = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
        server.resolve_confirmation('ask', card['confirmationToken'], self.root)
        server.submit_confirmation_comment('ask', card['confirmationToken'], '另一頁原圖還缺一張。', self.root)
        pending = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
        self.assertTrue(pending['feedbackPending'])
        self.assertEqual(pending['questions'], card['questions'])
        self.assertEqual(len(server.read_json(self.root/'monitor/confirmations.json')['resolved']), 1)

    def test_stale_or_invalid_comment_cannot_change_confirmation(self):
        card = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
        records = server.read_json(self.root/'monitor/confirmations.json')
        records['requests'][0]['questions'] = ['新版本的問題']
        self.write('monitor/confirmations.json', records)
        with self.assertRaises(server.ConfirmationConflict):
            server.submit_confirmation_comment('ask', card['confirmationToken'], '舊版本的意見', self.root)
        for comment in ('', ' ', 'x'*2001, None):
            with self.assertRaises(ValueError):
                server.submit_confirmation_comment('ask', card['confirmationToken'], comment, self.root)
        self.assertFalse(server.read_json(self.root/'monitor/confirmations.json').get('feedback'))

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

    def test_http_comment_is_not_approval_and_blank_comment_is_approval(self):
        with patch.object(server, 'ROOT', self.root):
            http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
            thread = threading.Thread(target=http.serve_forever, daemon=True)
            thread.start()
            base = f'http://127.0.0.1:{http.server_port}'
            card = next(c for c in server.build_status(self.root)['confirmations'] if c['id'] == 'ask')
            payload = {'id':'ask', 'confirmationToken':card['confirmationToken']}
            headers = {'Content-Type':'application/json', 'X-TestReview-Action':'confirm', 'Origin':base}
            def post(comment):
                body = json.dumps(dict(payload, comment=comment), ensure_ascii=False).encode()
                return urllib.request.urlopen(urllib.request.Request(base+'/api/confirm', data=body, headers=headers))
            try:
                for invalid in (None, 12, [], '字'*2001):
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        post(invalid)
                    self.assertEqual(caught.exception.code, 400)
                for _ in range(2):
                    with post('這是意見，請修改選項。') as response:
                        self.assertEqual(json.load(response), {'ok':True, 'id':'ask', 'state':'feedback_pending'})
                records = server.read_json(self.root/'monitor/confirmations.json')
                self.assertEqual(records['resolved'], [])
                self.assertEqual(len(records['feedback']), 1)
                with post(' \n ') as response:
                    self.assertEqual(json.load(response), {'ok':True, 'id':'ask'})
                records = server.read_json(self.root/'monitor/confirmations.json')
                self.assertEqual(len(records['resolved']), 1)
                self.assertEqual(records['feedback'][0]['state'], 'addressed')
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
