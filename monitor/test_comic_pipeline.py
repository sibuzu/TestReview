from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from .comic_pipeline import claim, stage, begin, integrated, load, save, update_display


class PipelineTests(unittest.TestCase):
    def idle_integration_fixture(self, directory):
        root = Path(directory)
        (root/'monitor').mkdir()
        (root/'docs/comics').mkdir(parents=True)
        save(root/'docs/comics/progress.json', {'entries': [
            dict(id=f'q-{i}', title=str(i), subject='Math', date='2026-10-21', state='queued')
            for i in (1, 2, 3)]})
        save(root/'docs/comics/pipeline.json', {'jobs': []})
        save(root/'monitor/parallel.json', {'lanes': [
            {'lane':1,'role':'integration'}, {'lane':2,'role':'import'}, {'lane':3,'role':'production'}]})
        return root

    def test_idle_integrator_can_help_without_duplicate_claims(self):
        with TemporaryDirectory() as directory:
            root=self.idle_integration_fixture(directory)
            with ThreadPoolExecutor(max_workers=2) as pool:
                jobs=list(pool.map(lambda lane:claim(root,lane),[1,3]))
            self.assertEqual(len({job['id'] for job in jobs}),2)
            self.assertIsNone(claim(root,2))

    def test_new_ready_work_waits_until_existing_helper_job_finishes(self):
        with TemporaryDirectory() as directory:
            root=self.idle_integration_fixture(directory)
            helper=claim(root,1)
            production=claim(root,3)
            (root/'docs/comics/evidence.json').write_text('{}')
            stage(root,production['id'],'not_suitable','Reviewed',['docs/comics/evidence.json'])
            self.assertEqual(claim(root,1)['jobId'],helper['jobId'])
            stage(root,helper['id'],'not_suitable','Reviewed',['docs/comics/evidence.json'])
            self.assertIsNone(claim(root,1))

    def test_handed_off_drafts_block_help_but_cancelled_sources_do_not(self):
        with TemporaryDirectory() as directory:
            root=self.idle_integration_fixture(directory)
            (root/'docs/imports/new-gemini/gemini063').mkdir(parents=True)
            (root/'docs/imports/new-gemini/gemini064').mkdir()
            save(root/'docs/imports/more-gemini-progress.json', {'sources':[{'order':63,'sourceCurationComplete':False}]})
            for order in (63,64):
                save(root/f'docs/imports/new-gemini/gemini{order:03}/manifest.json',{'readyCandidates':[f'gemini{order:03}-one']})
            self.assertIsNone(claim(root,1))
            save(root/'docs/imports/new-gemini/gemini063/integrated.json',{'mappings':[{'candidateId':'gemini063-one'}]})
            self.assertIsNotNone(claim(root,1))

    def test_import_qa_activity_survives_production_refresh(self):
        with TemporaryDirectory() as directory:
            root=self.idle_integration_fixture(directory)
            configuration=load(root/'monitor/parallel.json')
            configuration['lanes'][0]['activeTask']={'title':'Published question QA','state':'integrating'}
            save(root/'monitor/parallel.json',configuration)
            self.assertIsNone(claim(root,1))
            claim(root,3)
            owner=load(root/'monitor/parallel.json')['lanes'][0]
            self.assertEqual(owner['title'],'Published question QA')
            self.assertEqual(owner['state'],'integrating')

    def timing_fixture(self, root):
        (root/'monitor').mkdir()
        (root/'docs/comics').mkdir(parents=True)
        save(root/'docs/comics/progress.json', {'entries': [dict(id='q-1', title='Clock', subject='Math', date='2026-10-21', state='queued')]})
        save(root/'docs/comics/pipeline.json', {'jobs': []})
        save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1, 2, 3)]})
        claim(root, 1)
        (root/'docs/comics/evidence.json').write_text('{}')
        stage(root, 'q-1', 'not_suitable', 'Individual review', ['docs/comics/evidence.json'])

    def test_same_host_monotonic_interval_survives_utc_label_reversal(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)
            self.timing_fixture(root)
            with patch('monitor.comic_pipeline.now', return_value='2026-10-29T10:00:00+00:00'), patch('monitor.comic_pipeline.time.monotonic_ns', return_value=1000000000), patch('monitor.comic_pipeline.socket.gethostname', return_value='same-host'):
                begin(root, 'q-1')
            with patch('monitor.comic_pipeline.now', return_value='2026-10-29T09:00:00+00:00'), patch('monitor.comic_pipeline.time.monotonic_ns', return_value=4000000000), patch('monitor.comic_pipeline.socket.gethostname', return_value='same-host'):
                integrated(root, 'q-1')
            job=load(root/'docs/comics/pipeline.json')['jobs'][0]
            self.assertEqual(job['integrationSeconds'],3.0)
            self.assertTrue(job['integrationTimingValid'])
            self.assertEqual(job['integrationTimingMethod'],'monotonic')
            self.assertEqual(job['originalReportedIntegrationSeconds'],-3600.0)
            self.assertTrue(job['integrationUTCLabelsWentBackwards'])
            self.assertEqual(job['integratedAt'],'2026-10-29T09:00:00+00:00')
            self.assertIn('integrationEventId',job)

    def test_different_hosts_have_no_comparable_monotonic_interval(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)
            self.timing_fixture(root)
            with patch('monitor.comic_pipeline.socket.gethostname', return_value='host-a'):
                begin(root,'q-1')
            with patch('monitor.comic_pipeline.socket.gethostname', return_value='host-b'):
                integrated(root,'q-1')
            job=load(root/'docs/comics/pipeline.json')['jobs'][0]
            self.assertIsNone(job['integrationSeconds'])
            self.assertFalse(job['integrationTimingValid'])

    def test_integration_lane_finishes_existing_job_then_stops_claiming(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'monitor').mkdir()
            (root/'docs/comics').mkdir(parents=True)
            save(root/'docs/comics/progress.json', {'entries': [
                dict(id=f'q-{i}', title=str(i), subject='Math', date='2026-10-21', state='queued')
                for i in (1, 2, 3)]})
            save(root/'docs/comics/pipeline.json', {'jobs': []})
            save(root/'monitor/parallel.json', {'lanes': [{'lane': i} for i in (1, 2, 3)]})
            current = claim(root, 3)
            configuration = load(root/'monitor/parallel.json')
            configuration['lanes'][2]['role'] = 'integration'
            configuration['lanes'][1]['role'] = 'import'
            save(root/'monitor/parallel.json', configuration)
            self.assertIsNone(claim(root, 2))
            self.assertEqual(claim(root, 3)['id'], current['id'])
            evidence = 'docs/comics/review.json'
            (root/evidence).write_text('{}')
            stage(root, current['id'], 'not_suitable', 'Reviewed current job.', [evidence])
            self.assertIsNone(claim(root, 3))
            # The integration owner reports work from either production lane.
            other = claim(root, 1)
            stage(root, other['id'], 'not_suitable', 'Reviewed production job.', [evidence])
            begin(root, other['id'])
            integrator = load(root/'monitor/parallel.json')['lanes'][2]
            self.assertEqual(integrator['state'], 'integrating')
            self.assertEqual(integrator['questionId'], other['id'])

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
