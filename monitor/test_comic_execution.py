import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from .comic_execution import assert_work_allowed
from .comic_pipeline import claim, stage, begin, integrated


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
