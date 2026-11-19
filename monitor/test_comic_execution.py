import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from .comic_execution import assert_work_allowed
from .comic_pipeline import claim, stage, begin, integrated


class ExplicitQuestionUpdateTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory)
        def write(relative, value):
            path = root/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value))
            return path
        batch_ids = [f'q-{n}' for n in range(1, 11)]
        write('docs/comics/limited/manifest.json', dict(state='complete', limit=10,
              questionIds=batch_ids, completedQuestionIds=batch_ids))
        write('docs/comics/biology-rework-20261112/plan.json', dict(executionControl=dict(
              mode='biology_limited', biologyQualityUpgrade='paused', activeOriginalQuestionIds=batch_ids,
              remainingActiveOriginalQuestions=0, limitedBatch='docs/comics/limited/manifest.json')))
        questions = [dict(id=q, sourceId='src-more-072', date='2026-11-17')
                     for q in ['q-1153', 'q-1154', 'q-1155']]
        data = write('site/dist/data.json', dict(questions=questions))
        image = root/'docs/source-pages/supplement.jpg'
        image.parent.mkdir(parents=True)
        image.write_bytes(b'original image evidence')
        url = 'https://chatgpt.com/share/6aff112c-c79c-83e8-affb-e6e4a4a40848'
        acquisition = write('docs/imports/update/acquisition.json', dict(state='acquired',
            sourceId='src-more-072', url=url, imagesExpected=1, downloadedImages=[dict(
                path='docs/source-pages/supplement.jpg', bytes=image.stat().st_size,
                sha256=hashlib.sha256(image.read_bytes()).hexdigest(), decoded=True,
                archiveSizeMatched=True, width=1080, height=1440)]))
        scope = write('docs/imports/update/scope.json', dict(kind='explicit_question_update',
            authorizedBy='user_update', sourceId='src-more-072', url=url,
            questionIds=['q-1153', 'q-1154'], noNewQuestions=True,
            baselineQuestions={q['id']: q for q in questions[:2]}, originalsVisualChecked=True,
            existingQuestionIdentityChecked=True, expectedOriginalImages=1,
            acquisitionPath='docs/imports/update/acquisition.json',
            acquisitionSHA256=hashlib.sha256(acquisition.read_bytes()).hexdigest()))
        progress = write('docs/imports/update/progress.json', dict(state='active',
            sourceId='src-more-072', completedQuestionIds=[]))
        pointer = write('monitor/question-update-authorization.json', dict(state='active',
            sourceId='src-more-072', url=url, scopePath='docs/imports/update/scope.json',
            scopeSHA256=hashlib.sha256(scope.read_bytes()).hexdigest(),
            progressPath='docs/imports/update/progress.json'))
        return root, scope, progress, pointer, acquisition, image, data

    def test_only_two_named_existing_questions_override_the_paused_queue(self):
        with tempfile.TemporaryDirectory() as d:
            root, *_ = self.fixture(d)
            for qid in ['q-1153', 'q-1154']:
                assert_work_allowed(root, qid)
            for qid in ['q-1155', 'q-1168', 'q-1']:
                with self.assertRaisesRegex(ValueError, '已停止'):
                    assert_work_allowed(root, qid)

    def test_completed_question_and_closed_update_cannot_be_reentered(self):
        with tempfile.TemporaryDirectory() as d:
            root, _, progress, pointer, *_ = self.fixture(d)
            state = json.loads(progress.read_text())
            state['completedQuestionIds'] = ['q-1153']
            progress.write_text(json.dumps(state))
            assert_work_allowed(root, 'q-1154')
            for action, args in [(assert_work_allowed, ()), (begin, ()),
                                 (integrated, ()), (stage, ('complete', 'ready before closure', []))]:
                with self.assertRaisesRegex(ValueError, '已完成'):
                    action(root, 'q-1153', *args)
            config = json.loads(pointer.read_text()); config['state'] = 'closed'
            pointer.write_text(json.dumps(config))
            with self.assertRaisesRegex(ValueError, '已停止'):
                assert_work_allowed(root, 'q-1154')

    def test_tampered_scope_acquisition_or_original_fails_closed(self):
        for target in ('scope', 'acquisition', 'image'):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as d:
                root, scope, _, _, acquisition, image, _ = self.fixture(d)
                path = {'scope': scope, 'acquisition': acquisition, 'image': image}[target]
                path.write_bytes(path.read_bytes()+b'changed')
                with self.assertRaises(ValueError):
                    assert_work_allowed(root, 'q-1153')

    def test_existing_source_and_date_cannot_change_and_new_id_is_rejected(self):
        for change in ('date', 'sourceId', 'id'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                root, _, _, _, _, _, data = self.fixture(d)
                bank = json.loads(data.read_text()); bank['questions'][0][change] = 'different'
                data.write_text(json.dumps(bank))
                with self.assertRaisesRegex(ValueError, '不得新增題號或改變'):
                    assert_work_allowed(root, 'q-1153')

    def test_path_escape_and_missing_original_review_do_not_unlock_update(self):
        for change in ('scopePath', 'originalsVisualChecked'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                root, scope, _, pointer, *_ = self.fixture(d)
                config = json.loads(pointer.read_text())
                if change == 'scopePath':
                    config['scopePath'] = '../scope.json'
                else:
                    manifest = json.loads(scope.read_text()); manifest['originalsVisualChecked'] = False
                    scope.write_text(json.dumps(manifest))
                    config['scopeSHA256'] = hashlib.sha256(scope.read_bytes()).hexdigest()
                pointer.write_text(json.dumps(config))
                with self.assertRaises(ValueError):
                    assert_work_allowed(root, 'q-1153')

    def test_monitor_confirmation_requires_unchanged_resolved_record_for_each_question(self):
        with tempfile.TemporaryDirectory() as d:
            root, scope, _, pointer, *_ = self.fixture(d)
            records = [dict(id='correction-'+qid, questionId=qid, state='resolved',
                            resolution='使用者確認OK', resolvedAt='2026-11-19T00:00:00Z')
                       for qid in ['q-1153', 'q-1154']]
            confirmations = root/'monitor/confirmations.json'
            confirmations.write_text(json.dumps(dict(resolved=records)))
            manifest = json.loads(scope.read_text()); manifest['authorizedBy'] = 'monitor_confirmation'
            manifest['confirmationEvidence'] = [dict(questionId=r['questionId'], requestId=r['id'],
                snapshotSHA256=hashlib.sha256(json.dumps(r, ensure_ascii=False, sort_keys=True).encode()).hexdigest())
                for r in records]
            scope.write_text(json.dumps(manifest)); config = json.loads(pointer.read_text())
            config['scopeSHA256'] = hashlib.sha256(scope.read_bytes()).hexdigest()
            pointer.write_text(json.dumps(config))
            assert_work_allowed(root, 'q-1153')
            records[0]['resolution'] = 'changed content after scope froze'
            confirmations.write_text(json.dumps(dict(resolved=records)))
            with self.assertRaisesRegex(ValueError, '已變更'):
                assert_work_allowed(root, 'q-1153')


class ExecutionControlTests(unittest.TestCase):
    def test_paused_ready_art_cannot_be_integrated_but_missing_group_children_can(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            path=root/'docs/comics/biology-rework-20261112/plan.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(dict(executionControl={'mode':'missing_only'}, entries=[
                dict(id='q-581',originalQuestionIds=['q-581','q-582','q-583'],reasons=['missing_illustration']),
                dict(id='q-307',originalQuestionIds=['q-307'],reasons=['biology_quality_upgrade'],state='ready'),
                dict(id='q-912',originalQuestionIds=['q-912'],reasons=['text_only_diagram_without_actual_illustration'])])))
            assert_work_allowed(root,'q-583')
            for qid in ['q-307','q-912']:
                with self.assertRaisesRegex(ValueError,'暫停重製'):assert_work_allowed(root,qid)

    def limited_fixture(self, root):
        ids=[f'q-{n}' for n in range(1,11)]
        manifest=root/'docs/comics/biology-ten/manifest.json'
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps(dict(state='active',limit=10,questionIds=ids,completedQuestionIds=[])))
        plan=root/'docs/comics/biology-rework-20261112/plan.json'
        plan.parent.mkdir(parents=True)
        plan.write_text(json.dumps(dict(executionControl=dict(mode='biology_limited',
            biologyQualityUpgrade='active',activeOriginalQuestionIds=ids,
            remainingActiveOriginalQuestions=10,limitedBatch='docs/comics/biology-ten/manifest.json'))))
        return manifest,plan,ids

    def test_limited_batch_allows_only_exact_unfinished_whitelist(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest,_,ids=self.limited_fixture(root)
            for qid in ids:assert_work_allowed(root,qid)
            for qid in ['q-11','q-912','q-1048']:
                with self.assertRaisesRegex(ValueError,'白名單'):assert_work_allowed(root,qid)
            batch=json.loads(manifest.read_text());batch['completedQuestionIds']=[ids[0]]
            manifest.write_text(json.dumps(batch))
            with self.assertRaisesRegex(ValueError,'白名單'):assert_work_allowed(root,ids[0])
            assert_work_allowed(root,ids[1])

    def test_limited_completion_closes_gate_even_if_active_flags_are_stale(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest,_,ids=self.limited_fixture(root)
            batch=json.loads(manifest.read_text());batch['completedQuestionIds']=ids
            manifest.write_text(json.dumps(batch))
            for qid in [ids[-1],'q-11']:
                with self.assertRaisesRegex(ValueError,'已停止'):assert_work_allowed(root,qid)
            # Ready or attached drafts cannot bypass the same stop gate.
            for action,args in [(stage,('complete','old ready draft',[])),(begin,()),(integrated,())]:
                with self.assertRaisesRegex(ValueError,'已停止'):action(root,ids[-1],*args)

    def test_limited_missing_or_mismatched_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest,plan,ids=self.limited_fixture(root)
            control=json.loads(plan.read_text());control['executionControl']['activeOriginalQuestionIds'].append('q-11')
            plan.write_text(json.dumps(control))
            with self.assertRaisesRegex(ValueError,'不一致'):assert_work_allowed(root,ids[0])
            manifest.unlink()
            with self.assertRaisesRegex(ValueError,'缺漏'):assert_work_allowed(root,ids[0])

    def test_limited_cannot_expand_limit_or_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest,_,ids=self.limited_fixture(root)
            batch=json.loads(manifest.read_text())
            for invalid in [dict(batch,limit=11),dict(batch,questionIds=ids+[ids[0]]),
                            dict(batch,completedQuestionIds=['q-11'])]:
                manifest.write_text(json.dumps(invalid))
                with self.assertRaisesRegex(ValueError,'不一致'):assert_work_allowed(root,ids[0])

    def test_limited_paused_or_finished_manifest_closes_gate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest,plan,ids=self.limited_fixture(root)
            batch=json.loads(manifest.read_text());batch['state']='complete'
            manifest.write_text(json.dumps(batch))
            with self.assertRaisesRegex(ValueError,'已停止'):assert_work_allowed(root,ids[0])
            batch['state']='active';manifest.write_text(json.dumps(batch))
            config=json.loads(plan.read_text());config['executionControl']['biologyQualityUpgrade']='paused'
            plan.write_text(json.dumps(config))
            with self.assertRaisesRegex(ValueError,'已停止'):assert_work_allowed(root,ids[0])

    def test_claim_rechecks_existing_job_after_batch_completion(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest,_,ids=self.limited_fixture(root)
            (root/'monitor').mkdir()
            pipeline=root/'docs/comics/pipeline.json'
            pipeline.write_text(json.dumps(dict(jobs=[dict(id=ids[0],lane=3,state='claimed')])))
            batch=json.loads(manifest.read_text());batch['completedQuestionIds']=ids
            manifest.write_text(json.dumps(batch))
            self.assertIsNone(claim(root,3))
            self.assertEqual(json.loads(pipeline.read_text())['jobs'][0]['state'],'claimed')

    def test_claim_cannot_use_priority_misconfiguration_to_take_eleventh(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.limited_fixture(root);(root/'monitor').mkdir()
            pipeline=root/'docs/comics/pipeline.json';pipeline.write_text(json.dumps(dict(jobs=[])))
            (root/'monitor/parallel.json').write_text(json.dumps(dict(lanes=[dict(lane=3,role='production')])))
            candidate=dict(id='q-11',title='第11題',subject='Biology',state='queued')
            (root/'docs/comics/progress.json').write_text(json.dumps(dict(entries=[candidate])))
            with patch('monitor.comic_pipeline.next_entry',return_value=candidate):
                self.assertIsNone(claim(root,3))
            self.assertEqual(json.loads(pipeline.read_text())['jobs'],[])
