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


if __name__ == '__main__':
    unittest.main()
