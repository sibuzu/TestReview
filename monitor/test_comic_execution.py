import json
from pathlib import Path
import tempfile
import unittest
from .comic_execution import assert_work_allowed


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
