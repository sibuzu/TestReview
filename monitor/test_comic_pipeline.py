from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from .comic_pipeline import claim, stage, begin, integrated, load, save


class PipelineTests(unittest.TestCase):
    def test_rework_priority_holds_general_work_and_uses_whole_bank_subject_scores(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'monitor').mkdir()
            (root/'docs/comics').mkdir(parents=True)
            entries = [dict(id=f'q-{i}', title=str(i), subject='Math' if i<=4 else 'Biology',
                            date='2026-10-21', state='complete' if i in (1,2,5) else 'queued')
                       for i in range(1,7)]
            save(root/'docs/comics/progress.json', {'entries': entries})
            save(root/'docs/comics/pipeline.json', {'jobs': []})
            save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1,2,3)]})
            save(root/'monitor/rework-priority.json', {'kind':'rework','state':'active','questionIds':['q-3','q-6']})
            # Whole-bank scores: Biology 1/2 < Math 4/4.
            self.assertEqual(claim(root, 1)['id'], 'q-6')
            self.assertEqual(claim(root, 2)['id'], 'q-3')
            self.assertIsNone(claim(root, 3))
            save(root/'monitor/rework-priority.json', {'kind':'rework','state':'complete','questionIds':['q-3','q-6']})
            self.assertEqual(claim(root, 3)['id'], 'q-4')

    def test_fresh_art_policy_rejects_source_reuse_and_skip_without_losing_claim(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'monitor').mkdir()
            (root/'docs/comics').mkdir(parents=True)
            save(root/'docs/comics/progress.json', {'entries': [
                dict(id='q-1', title='Fresh art', subject='Biology', date='2026-10-21',
                     state='queued', freshFourPanelRequired=True)]})
            save(root/'docs/comics/pipeline.json', {'jobs': []})
            save(root/'docs/comics/policy.json', {'reuseSourceAI': False})
            save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1, 2, 3)]})
            claim(root, 1)
            evidence = 'docs/comics/review.json'
            (root/evidence).write_text('{}')
            for decision in ('existing_ai', 'not_suitable'):
                with self.assertRaises(AssertionError):
                    stage(root, 'q-1', decision, 'Old figure or unrelated-art skip.', [evidence])
                self.assertEqual(load(root/'docs/comics/pipeline.json')['jobs'][0]['state'], 'claimed')
            stage(root, 'q-1', 'complete', 'New four-panel content checked.', [evidence])
            self.assertEqual(load(root/'docs/comics/pipeline.json')['jobs'][0]['state'], 'ready')

    def test_reopened_question_can_finish_again_without_overwriting_prior_job(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'monitor').mkdir()
            (root/'docs/comics').mkdir(parents=True)
            save(root/'docs/comics/progress.json', {'entries': [
                dict(id='q-1', title='Reopened', subject='Math', date='2026-10-21', state='queued')]})
            prior = dict(id='q-1', lane=1, state='integrated', decision='existing_ai',
                         integratedAt='2026-10-28T00:00:00+00:00')
            save(root/'docs/comics/pipeline.json', {'jobs': [prior]})
            save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1, 2, 3)]})
            self.assertEqual(claim(root, 2)['id'], 'q-1')
            evidence = 'docs/comics/review.json'
            (root/evidence).write_text('{}')
            stage(root, 'q-1', 'not_suitable', 'Reviewed under updated requirements.', [evidence])
            begin(root, 'q-1')
            integrated(root, 'q-1')
            jobs = load(root/'docs/comics/pipeline.json')['jobs']
            self.assertEqual(jobs[0], prior)
            self.assertEqual(jobs[1]['state'], 'integrated')
            self.assertEqual(jobs[1]['lane'], 2)
            self.assertEqual(jobs[1]['decision'], 'not_suitable')
            self.assertEqual(load(root/'docs/comics/progress.json')['entries'][0]['state'], 'not_suitable')

    def test_paused_claims_finish_existing_work_without_reserving_new_questions(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'monitor').mkdir()
            (root/'docs/comics').mkdir(parents=True)
            save(root/'docs/comics/progress.json', {'entries': [
                dict(id=f'q-{i}', title=str(i), subject='History', date='2026-10-21', state='queued')
                for i in range(1, 4)]})
            save(root/'docs/comics/pipeline.json', {'jobs': []})
            save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1, 2, 3)]})
            active = claim(root, 1)
            pipeline = load(root/'docs/comics/pipeline.json')
            pipeline['claimsPaused'] = True
            save(root/'docs/comics/pipeline.json', pipeline)
            self.assertEqual(claim(root, 1)['id'], active['id'])
            self.assertIsNone(claim(root, 2))
            evidence = 'docs/comics/review.json'
            (root/evidence).write_text('{}')
            stage(root, active['id'], 'existing_ai', 'Finish already reserved work.', [evidence])
            self.assertIsNone(claim(root, 1))
            begin(root, active['id'])
            integrated(root, active['id'])
            self.assertEqual(len(load(root/'docs/comics/pipeline.json')['jobs']), 1)
            self.assertEqual([e['state'] for e in load(root/'docs/comics/progress.json')['entries']],
                             ['existing_ai', 'queued', 'queued'])

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
