from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from .comic_pipeline import claim, stage, begin, integrated, load, save


class PipelineTests(unittest.TestCase):
    def test_priority_source_blocks_old_work_until_whole_group_is_released(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'monitor').mkdir()
            (root/'docs/comics').mkdir(parents=True)
            save(root/'docs/comics/progress.json', {'entries': [
                dict(id=f'q-{i}', title=str(i), subject='History', date='2026-10-21', state='queued')
                for i in range(1, 4)]})
            save(root/'docs/comics/pipeline.json', {'jobs': []})
            save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1, 2, 3)]})
            priority = root/'monitor/priority-source.json'
            save(priority, {'state': 'acquiring_originals', 'questionIds': []})
            self.assertIsNone(claim(root, 1))
            save(priority, {'state': 'curating_and_illustrating', 'questionIds': ['q-3'],
                            'laneAssignments': {'1': ['q-3'], '2': []}})
            self.assertEqual(claim(root, 1)['id'], 'q-3')
            self.assertIsNone(claim(root, 2))
            evidence = 'docs/comics/review.json'
            (root/evidence).write_text('{}')
            stage(root, 'q-3', 'complete', 'Worker ready, not integrated yet.', [evidence])
            self.assertIsNone(claim(root, 1))
            save(priority, {'state': 'complete', 'questionIds': ['q-3']})
            self.assertEqual(claim(root, 1)['id'], 'q-1')

    def test_parallel_claims_are_distinct_and_staging_does_not_wait_for_integration(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'monitor').mkdir()
            (root/'docs/comics').mkdir(parents=True)
            entries = [dict(id=f'q-{i}', title=str(i), subject='History', date='2026-10-21', state='queued') for i in range(1, 7)]
            save(root/'docs/comics/progress.json', {'entries': entries})
            save(root/'docs/comics/pipeline.json', {'jobs': []})
            save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1, 2, 3)]})
            with ThreadPoolExecutor(max_workers=3) as executor:
                jobs = list(executor.map(lambda lane: claim(root, lane), (1, 2, 3)))
            self.assertEqual(len({j['id'] for j in jobs}), 3)
            first = jobs[0]
            self.assertEqual(claim(root, first['lane'])['id'], first['id'])
            evidence = 'docs/comics/review.json'
            (root/evidence).write_text('{}')
            stage(root, first['id'], 'existing_ai', 'Individually reviewed.', [evidence])
            following = claim(root, first['lane'])
            self.assertNotIn(following['id'], {j['id'] for j in jobs})
            self.assertTrue(all(e['state'] == 'queued' for e in load(root/'docs/comics/progress.json')['entries']))
            self.assertEqual(len(load(root/'monitor/parallel.json')['ready']), 1)
            self.assertEqual(len(load(root/'monitor/parallel.json')['waiting']), 1)
            with self.assertRaises(AssertionError):
                stage(root, first['id'], 'existing_ai', 'Duplicate stage.', [evidence])
            # Staged work only becomes completed when the root integrates it.
            begin(root, first['id'])
            self.assertEqual(load(root/'monitor/parallel.json')['waiting'], [])
            self.assertEqual(len(load(root/'monitor/parallel.json')['integrating']), 1)
            integrated(root, first['id'])
            entry = next(e for e in load(root/'docs/comics/progress.json')['entries'] if e['id']==first['id'])
            self.assertEqual(entry['state'], 'existing_ai')
            self.assertLessEqual(entry['workerReadyAt'], entry['completedAt'])
            self.assertGreaterEqual(entry['integrationQueueSeconds'], 0)
            self.assertGreaterEqual(entry['integrationSeconds'], 0)
            self.assertEqual(load(root/'monitor/parallel.json')['ready'], [])
            self.assertIn('1／6', load(root/'monitor/activity.json')['title'])
