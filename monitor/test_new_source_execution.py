import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from .comic_execution import assert_work_allowed
from .comic_pipeline import active_priority, claim
from . import test_comic_execution


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


class NewSourceExecutionTests(unittest.TestCase):
    def test_paused_old_priority_cannot_hide_explicit_new_source(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write(root/'monitor/rework-priority.json', dict(state='paused', questionIds=['q-969']))
            source = dict(state='active', sourceId='src-more-072', questionIds=['q-1133'])
            write(root/'monitor/priority-source.json', source)
            self.assertEqual(active_priority(root), source)
            source['state'] = 'complete'
            write(root/'monitor/priority-source.json', source)
            self.assertIsNone(active_priority(root))

    def fixture(self, root):
        manifest, plan, old_ids = test_comic_execution.ExecutionControlTests().limited_fixture(root)
        old = json.loads(manifest.read_text())
        old.update(state='complete', completedQuestionIds=old_ids)
        write(manifest, old)
        directory = root/'docs/imports/new-source-test'
        image = root/'docs/source-pages/original.jpg'
        image.parent.mkdir(parents=True)
        image.write_bytes(b'original bytes checked by acquisition')
        url = 'https://chatgpt.com/share/6afc7636-b8dc-83ec-a9de-c3ac330e5d27'
        source = 'src-more-072'
        acquisition = root/'docs/acquisition/test.json'
        write(acquisition, dict(state='acquired', sourceId=source, url=url, imagesExpected=1,
                               downloadedImages=[dict(path=str(image.relative_to(root)), bytes=image.stat().st_size,
                                sha256=hashlib.sha256(image.read_bytes()).hexdigest(), decoded=True,
                                archiveSizeMatched=True, width=1080, height=1440)]))
        scope = directory/'execution-scope.json'
        write(scope, dict(kind='explicit_new_source', authorizedBy='user_add', sourceId=source, url=url,
                          newQuestionIds=['q-1133', 'q-1134'], baselineQuestionIds=old_ids,
                          baselineSourceIds=['src-more-071'], originalsVisualChecked=True,
                          crossSourceDuplicatesChecked=True, acquisitionPath=str(acquisition.relative_to(root)),
                          acquisitionSHA256=hashlib.sha256(acquisition.read_bytes()).hexdigest()))
        progress = directory/'execution-progress.json'
        write(progress, dict(state='active', sourceId=source, completedQuestionIds=[]))
        pointer = root/'monitor/new-source-authorization.json'
        write(pointer, dict(state='active', sourceId=source, url=url, scopePath=str(scope.relative_to(root)),
                            scopeSHA256=hashlib.sha256(scope.read_bytes()).hexdigest(),
                            progressPath=str(progress.relative_to(root))))
        return pointer, scope, progress, acquisition, image, plan, manifest

    def refreeze(self, pointer, scope):
        config = json.loads(pointer.read_text())
        config['scopeSHA256'] = hashlib.sha256(scope.read_bytes()).hexdigest()
        write(pointer, config)

    def test_new_source_does_not_resume_finished_biology_or_eleventh(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            *_, plan, manifest = self.fixture(root)
            snapshots = [p.read_bytes() for p in [plan, manifest]]
            for qid in ['q-1133', 'q-1134']:
                assert_work_allowed(root, qid)
            for qid in ['q-1', 'q-11', 'q-969', 'q-912', 'q-1135']:
                with self.assertRaises(ValueError):
                    assert_work_allowed(root, qid)
            self.assertEqual(snapshots, [p.read_bytes() for p in [plan, manifest]])

    def test_claim_takes_only_new_source_and_cannot_continue_after_source_stop(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _, _, progress, *_ = self.fixture(root)
            write(root/'docs/comics/pipeline.json', dict(jobs=[], claimsPaused=False))
            write(root/'monitor/parallel.json', dict(lanes=[dict(lane=3, role='production')]))
            write(root/'monitor/rework-priority.json', dict(state='paused', questionIds=['q-969']))
            write(root/'monitor/priority-source.json', dict(state='active', questionIds=['q-1133']))
            write(root/'docs/comics/progress.json', dict(entries=[
                dict(id='q-969', title='舊生物', subject='Biology', state='queued', date='2026-11-17'),
                dict(id='q-1133', title='新來源', subject='History', state='queued', date='2026-11-17')]))
            self.assertEqual(claim(root, 3)['id'], 'q-1133')
            write(progress, dict(state='complete', sourceId='src-more-072', completedQuestionIds=['q-1133']))
            self.assertIsNone(claim(root, 3))
            jobs = json.loads((root/'docs/comics/pipeline.json').read_text())['jobs']
            self.assertEqual([j['id'] for j in jobs], ['q-1133'])

    def test_initial_blocked_and_completed_progress_refuse_new_work(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            pointer, _, progress, *_ = self.fixture(root)
            config = json.loads(pointer.read_text())
            config['state'] = 'blocked'
            write(pointer, config)
            with self.assertRaises(ValueError):
                assert_work_allowed(root, 'q-1133')
            config['state'] = 'active'
            write(pointer, config)
            for update in [dict(state='complete'), dict(completedQuestionIds=['q-1133']),
                           dict(awaitingConfirmationQuestionIds=['q-1133']),
                           dict(completedQuestionIds=['q-1133', 'q-1134'])]:
                write(progress, dict(state='active', sourceId='src-more-072', completedQuestionIds=[]) | update)
                with self.assertRaises(ValueError):
                    assert_work_allowed(root, 'q-1133')

    def test_missing_or_modified_original_and_false_validation_refuse(self):
        for change in ['missing', 'changed', 'decode', 'archive_size', 'partial']:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                root = Path(d)
                pointer, scope, _, acquisition, image, *_ = self.fixture(root)
                data = json.loads(acquisition.read_text())
                if change == 'missing': image.unlink()
                elif change == 'changed': image.write_bytes(b'changed original')
                else:
                    if change == 'decode': data['downloadedImages'][0]['decoded'] = False
                    if change == 'archive_size': data['downloadedImages'][0]['archiveSizeMatched'] = False
                    if change == 'partial': data['imagesExpected'] = 2
                    write(acquisition, data)
                    frozen = json.loads(scope.read_text())
                    frozen['acquisitionSHA256'] = hashlib.sha256(acquisition.read_bytes()).hexdigest()
                    write(scope, frozen)
                    self.refreeze(pointer, scope)
                with self.assertRaises(ValueError):
                    assert_work_allowed(root, 'q-1133')

    def test_scope_edit_unchecked_source_and_old_ids_fail_closed(self):
        for change in ['hash', 'unchecked', 'old_id', 'old_source', 'wrong_source', 'path_escape']:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                root = Path(d)
                pointer, scope, *_ = self.fixture(root)
                data = json.loads(scope.read_text())
                if change == 'unchecked': data['crossSourceDuplicatesChecked'] = False
                if change == 'old_id': data['newQuestionIds'].append('q-1')
                if change == 'old_source': data['baselineSourceIds'].append(data['sourceId'])
                if change == 'wrong_source': data['sourceId'] = 'src-more-073'
                if change == 'hash': data['newQuestionIds'].append('q-1135')
                if change == 'path_escape': data['acquisitionPath'] = '/tmp/external.json'
                write(scope, data)
                if change != 'hash': self.refreeze(pointer, scope)
                with self.assertRaises(ValueError):
                    assert_work_allowed(root, 'q-1133')

    def test_old_rework_cannot_be_added_even_with_incorrect_baseline(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            pointer, scope, _, _, _, plan, _ = self.fixture(root)
            old = json.loads(plan.read_text())
            old['entries'] = [dict(id='q-969', originalQuestionIds=['q-969'])]
            write(plan, old)
            data = json.loads(scope.read_text())
            data['newQuestionIds'].append('q-969')
            write(scope, data)
            self.refreeze(pointer, scope)
            with self.assertRaisesRegex(ValueError, '舊重製'):
                assert_work_allowed(root, 'q-969')
