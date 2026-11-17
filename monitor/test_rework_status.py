import json
from pathlib import Path
import tempfile
import unittest

from monitor.rework_status import PLAN, build_rework_status


def comic(count=4):
    return {'panels': [{'image': f'image-{i}.svg'} for i in range(3)],
            'fourth': {'image': 'image-3.svg'} if count == 4 else {}}


class ReworkStatusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def plan(self, entries):
        path = self.root / PLAN
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({'state': 'paused', 'entries': entries,
            'executionControl': {'biologyResumePhrase': '將生物的舊解說圖改為精美解說圖'}}))

    def test_no_plan_does_not_invent_a_backlog(self):
        self.assertIsNone(build_rework_status(self.root, {}, {}))

    def test_group_originals_and_subjects_are_counted_once(self):
        data = {'questions': [{'id': 'q-001', 'groupQuestions': [
            {'id': 'q-001', 'subject': 'Biology', 'teachingComic': comic()},
            {'id': 'q-002', 'subject': 'Biology', 'teachingComic': comic()}]},
            {'id': 'q-003', 'subject': 'Chinese', 'teachingComic': comic()}]}
        entries = [dict(id='q-001', originalQuestionIds=['q-001', 'q-002'], state='complete'),
                   dict(id='q-003', state='paused'), dict(id='q-002', state='complete')]
        self.plan(entries)
        status = build_rework_status(self.root, data, {})
        self.assertEqual((status['completed'], status['pending'], status['total']), (2, 1, 3))
        self.assertEqual((status['biologyPending'], status['otherPending']), (0, 1))
        self.assertEqual(status['items'][1]['url'], '/site/index.html#question/q-001')
        self.assertEqual(status['state'], 'paused')

    def test_unaccepted_drafts_and_old_three_image_comics_are_not_complete(self):
        self.plan([dict(id='q-001', state='validation'), dict(id='q-002', state='complete')])
        data = {'questions': [dict(id='q-001', subject='Biology', teachingComic=comic()),
                              dict(id='q-002', subject='Chinese', teachingComic=comic(3))]}
        status = build_rework_status(self.root, data, {})
        self.assertEqual((status['completed'], status['pending']), (0, 2))
        self.assertEqual(status['biologyResumeCommand'], '將生物的舊解說圖改為精美解說圖')

    def test_legacy_exemption_is_separate_and_links_to_its_group(self):
        self.plan([dict(id='q-001', state='paused')])
        data = {'questions': [dict(id='q-001', subject='Biology'),
            {'id': 'q-080', 'groupQuestions': [dict(id='q-081', subject='History', title='伊拉克戰亂')]}]}
        progress = {'entries': [dict(id='q-081', state='not_suitable', reason='舊免製原因'),
                                dict(id='q-001', state='not_suitable')]}
        before = json.dumps(progress)
        status = build_rework_status(self.root, data, progress)
        self.assertEqual((status['pending'], status['reassess']), (1, 1))
        self.assertEqual(status['reassessItems'][0]['url'], '/site/index.html#question/q-080')
        self.assertIn('q-081', status['reassessCommand'])
        self.assertEqual(json.dumps(progress), before)

    def test_limited_batch_does_not_resume_the_rest_of_the_backlog(self):
        self.plan([dict(id='q-001', state='queued'), dict(id='q-002', state='paused')])
        path = self.root / PLAN
        plan = json.loads(path.read_text())
        plan['executionControl']['limitedBatch'] = 'batch.json'
        path.write_text(json.dumps(plan))
        batch_path = self.root / 'batch.json'
        batch = dict(state='active', limit=10, questionIds=['q-001'], completedQuestionIds=[])
        batch_path.write_text(json.dumps(batch))
        data = {'questions': [dict(id='q-001', subject='Biology'), dict(id='q-002', subject='Biology')]}
        status = build_rework_status(self.root, data, {})
        self.assertEqual([q['state'] for q in status['items']], ['active', 'paused'])
        self.assertEqual(status['activeBatch']['remaining'], 1)
        batch['state'] = 'complete'
        batch_path.write_text(json.dumps(batch))
        self.assertTrue(all(q['state'] == 'paused' for q in build_rework_status(self.root, data, {})['items']))


if __name__ == '__main__':
    unittest.main()
