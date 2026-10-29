import json
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from . import comic_publish
from .comic_pipeline import save, load


class PublishCountingTests(unittest.TestCase):
    def setup_root(self, directory, jobs=()):
        root = Path(directory)
        for path in ['docs/comics', '.cache', 'monitor', 'site/dist/assets']:
            (root/path).mkdir(parents=True, exist_ok=True)
        save(root/'docs/comics/commit-policy.json', dict(baselineAt='2026-10-29T00:00:00+00:00', batchSize=20, enabled=True, allowForcePush=False))
        save(root/'docs/comics/pipeline.json', dict(jobs=list(jobs)))
        save(root/'site/dist/data.json', dict(revision='test-revision'))
        return root

    def job(self, qid, event, utc='2026-10-29T01:00:00+00:00', sequence=1):
        return dict(id=qid, jobId=event, integrationEventId='integration-'+event,
                    integrationSequence=sequence, state='integrated', decision='complete', integratedAt=utc)

    def ledger(self, root, published=(), excluded=()):
        save(root/comic_publish.LEDGER, dict(version=2, baselineExcludedEventIds=list(excluded), publishedBatches=list(published)))
        if published:
            last=max(published,key=lambda b:b['batchNumber'])
            save(root/'.cache/comic-publish-state.json',dict(batchNumber=last['batchNumber'],lastPushedCommit=last['commit']))

    def test_new_event_earlier_than_last_utc_cursor_is_still_counted(self):
        with TemporaryDirectory() as directory:
            old = self.job('q-1', 'old', '2026-10-29T04:00:00+00:00')
            new = self.job('q-2', 'new', '2026-10-28T23:00:00+00:00', 2)
            root = self.setup_root(directory, [old, new])
            self.ledger(root, [dict(batchNumber=1, commit='pushed', eventIds=['integration-old'])])
            save(root/'.cache/comic-publish-state.json', dict(throughIntegratedAt=old['integratedAt'],batchNumber=1,lastPushedCommit='pushed'))
            with patch.object(comic_publish, 'ROOT', root):
                self.assertEqual([j['id'] for j in comic_publish.pending_batch()[3]], ['q-2'])

    def test_same_question_rework_is_distinct_but_metadata_edit_is_not(self):
        with TemporaryDirectory() as directory:
            old = self.job('q-1', 'first')
            old['metadataSpellingFix'] = 'no new work event'
            new = self.job('q-1', 'rework', sequence=2)
            root = self.setup_root(directory, [old, new])
            self.ledger(root, [dict(batchNumber=1, commit='pushed', eventIds=['integration-first'])])
            with patch.object(comic_publish, 'ROOT', root):
                self.assertEqual([j['integrationEventId'] for j in comic_publish.pending_batch()[3]], ['integration-rework'])
                self.assertEqual(len(comic_publish.pending_batch()[3]), 1)

    def test_ready_blocked_and_non_complete_do_not_count(self):
        with TemporaryDirectory() as directory:
            jobs = [self.job('q-1', 'one'), dict(id='q-2', state='ready', decision='complete'),
                    dict(id='q-3', state='blocked', decision='awaiting_confirmation'),
                    dict(id='q-4', state='integrated', decision='not_suitable')]
            root = self.setup_root(directory, jobs)
            self.ledger(root)
            with patch.object(comic_publish, 'ROOT', root):
                self.assertEqual([j['id'] for j in comic_publish.pending_batch()[3]], ['q-1'])

    def test_tracked_event_ledger_recovers_missing_cache_after_remote_verification(self):
        with TemporaryDirectory() as directory:
            root=self.setup_root(directory,[self.job('q-1','old'),self.job('q-2','new',sequence=2)])
            self.ledger(root,[dict(batchNumber=1,commit='pushed',eventIds=['integration-old'])])
            (root/'.cache/comic-publish-state.json').unlink()
            with patch.object(comic_publish,'ROOT',root),patch.object(comic_publish,'git',return_value='pushed\trefs/heads/main'):
                self.assertEqual([j['id'] for j in comic_publish.pending_batch()[3]],['q-2'])
            self.assertEqual(load(root/'.cache/comic-publish-state.json')['batchNumber'],1)

    def test_legacy_migration_reconciles_repeated_ids_receipts_and_baseline_once(self):
        with TemporaryDirectory() as directory:
            old = self.job('q-old', 'baseline', '2026-10-28T23:00:00+00:00')
            jobs = [old]+[self.job('q-1' if i < 2 else f'q-{i}', f'work-{i}', f'2026-10-29T01:{i:02}:00+00:00', i+1) for i in range(20)]
            jobs.append(self.job('q-pending', 'later', '2026-10-29T02:00:00+00:00', 21))
            root = self.setup_root(directory, jobs)
            manifest = dict(batchNumber=1, verifiedComicCount=20, questionIds=[j['id'] for j in jobs[1:21]], throughIntegratedAt='2026-10-29T01:19:00+00:00', previousHEAD='before')
            manifest_path=root/'docs/comics/publish-batch-test-001.json'
            save(manifest_path, manifest)
            original_bytes=manifest_path.read_bytes()
            save(root/'.cache/comic-publish-state.json', dict(batchNumber=1, lastPushedCommit='remote', throughIntegratedAt=manifest['throughIntegratedAt']))
            with patch.object(comic_publish, 'ROOT', root), patch.object(comic_publish, 'git', return_value='remote\trefs/heads/main'):
                self.assertEqual([j['id'] for j in comic_publish.pending_batch()[3]], ['q-pending'])
                ledger=load(root/comic_publish.LEDGER)
                self.assertEqual(ledger['migration']['publishedEventCount'], 20)
                self.assertEqual(len(set(ledger['publishedBatches'][0]['eventIds'])),20)
                self.assertEqual(ledger['baselineExcludedEventIds'], ['integration-baseline'])
                self.assertEqual(manifest_path.read_bytes(),original_bytes)
                # A newly integrated, earlier-dated event must not be reclassified as baseline.
                payload=load(root/'docs/comics/pipeline.json')
                payload['jobs'].append(self.job('q-new-backward', 'backward', '2026-10-28T21:00:00+00:00',22))
                save(root/'docs/comics/pipeline.json',payload)
                self.assertEqual(len(comic_publish.pending_batch()[3]),2)

    def test_migration_refuses_pending_push_or_remote_mismatch(self):
        with TemporaryDirectory() as directory:
            root=self.setup_root(directory)
            state_path=root/'.cache/comic-publish-state.json'
            save(state_path,dict(pendingPush={'commit':'unresolved'}))
            with patch.object(comic_publish,'ROOT',root):
                with self.assertRaisesRegex(AssertionError,'legacy pending'):
                    comic_publish.pending_batch()
            save(state_path,dict(lastPushedCommit='expected'))
            with patch.object(comic_publish,'ROOT',root),patch.object(comic_publish,'git',return_value='other\trefs/heads/main'):
                with self.assertRaisesRegex(AssertionError,'remote HEAD'):
                    comic_publish.pending_batch()
            self.assertFalse((root/comic_publish.LEDGER).exists())

    def test_failed_network_retry_commits_once_and_records_each_event_once(self):
        with TemporaryDirectory() as directory:
            jobs=[self.job(f'q-{i}',f'job-{i}',sequence=i) for i in range(25)]
            root=self.setup_root(directory,jobs)
            self.ledger(root)
            (root/'site/dist/assets/art.svg').write_text('<svg/>')
            for job in jobs:
                save(root/'docs/comics'/f'{job["id"]}.json',dict(rootReview={'visualChecked':True},nativeArt='assets/art.svg'))
            calls=[]; current_head=['old']; fail_push=[True]
            def fake_git(*args):
                if args==('branch','--show-current'):return 'main'
                if args==('rev-parse','HEAD'):return current_head[0]
                if args[0]=='ls-files':return ''
                if args[0]=='ls-remote':return current_head[0]+'\trefs/heads/main'
                raise AssertionError(args)
            def fake_run(args,**kwargs):
                calls.append(args)
                if args[0]=='npm':return subprocess.CompletedProcess(args,0,stdout='# pass 72\n',stderr='')
                if args[:2]==['git','commit']:current_head[0]='new-commit'
                if args[:2]==['git','push'] and fail_push[0]:
                    fail_push[0]=False
                    raise subprocess.CalledProcessError(1,args)
                return subprocess.CompletedProcess(args,0)
            with patch.object(comic_publish,'ROOT',root),patch.object(comic_publish,'git',side_effect=fake_git),patch.object(comic_publish.subprocess,'run',side_effect=fake_run):
                with self.assertRaises(subprocess.CalledProcessError):comic_publish.publish()
                pending=load(root/'.cache/comic-publish-state.json')
                self.assertEqual(len(pending['pendingPush']['integrationEventIds']),20)
                self.assertEqual(len(load(root/comic_publish.LEDGER)['publishedBatches']),0)
                result=comic_publish.publish()
                self.assertEqual(result['verifiedComicCount'],20)
                self.assertEqual(len(comic_publish.pending_batch()[3]),5)
            self.assertEqual(sum(c[:2]==['git','commit'] for c in calls),1)
            self.assertEqual(sum(c[:2]==['git','push'] for c in calls),2)
            ledger=load(root/comic_publish.LEDGER)
            self.assertEqual(len(ledger['publishedBatches']),1)
            self.assertEqual(len(set(ledger['publishedBatches'][0]['eventIds'])),20)
            state=load(root/'.cache/comic-publish-state.json')
            self.assertNotIn('pendingPush',state)
            self.assertEqual(state['lastPushedCommit'],'new-commit')
            # Crash after ledger save but before cache finalization is also idempotent.
            with patch.object(comic_publish,'ROOT',root):
                comic_publish._finish_push(root/'.cache/comic-publish-state.json',state,pending['pendingPush'],'new-commit')
            self.assertEqual(len(load(root/comic_publish.LEDGER)['publishedBatches']),1)
