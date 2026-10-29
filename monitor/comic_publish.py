"""Publish each authorized batch using stable integration events, never a UTC cursor."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import re
import subprocess
from .comic_pipeline import ROOT, load, save, locked, ensure_job_identity

LEDGER = 'docs/comics/publication-ledger.json'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def _event(job):
    ensure_job_identity(job)
    job.setdefault('integrationEventId', 'integration-' + job['jobId'])
    return job['integrationEventId']


def _ensure_ledger(policy, state_path, state):
    """One audited migration. Historical UTC is used only to match old receipts."""
    path = ROOT/LEDGER
    if path.exists():
        ledger = load(path)
        assert ledger['version'] == 2
        batches = ledger['publishedBatches']
        # The tracked ledger also restores a missing/stale local cache. A pending
        # network retry keeps its own transaction until _finish_push completes.
        if batches and not state.get('pendingPush'):
            last = max(batches, key=lambda b: b['batchNumber'])
            assert state.get('batchNumber', 0) <= last['batchNumber'], 'Publication cache is ahead of its event ledger.'
            if (state.get('batchNumber') != last['batchNumber'] or
                    state.get('lastPushedCommit') != last['commit']):
                remote = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
                assert remote == last['commit'], 'Reconcile remote HEAD before restoring publication cache.'
                state.update(batchNumber=last['batchNumber'], lastPushedCommit=last['commit'], publicationLedgerVersion=2)
                save(state_path, state)
        return ledger
    assert not state.get('pendingPush'), 'Finish legacy pending push before event-ledger migration.'
    if state.get('lastPushedCommit'):
        remote = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
        assert remote == state['lastPushedCommit'], 'Reconcile remote HEAD before migration.'
    manifests = sorted((ROOT/'docs/comics').glob('publish-batch-*.json'),
                       key=lambda p: load(p)['batchNumber'])
    manifests = [p for p in manifests if load(p)['batchNumber'] <= state.get('batchNumber', 0)]
    assert len(manifests) == state.get('batchNumber', 0), 'Missing historical publication receipt.'
    with locked(ROOT):
        pipeline = load(ROOT/'docs/comics/pipeline.json')
        completed = [j for j in pipeline['jobs'] if j['state'] == 'integrated' and j.get('decision') == 'complete']
        assert all(j.get('integratedAt') for j in completed)
        for job in completed:
            _event(job)
        # Freeze the historical boundary once. Future events may have earlier UTC labels.
        excluded = [j['integrationEventId'] for j in completed if j['integratedAt'] <= policy['baselineAt']]
        eligible = [j for j in completed if j['integrationEventId'] not in set(excluded)]
        used = set()
        batches = []
        for index, manifest_path in enumerate(manifests):
            manifest = load(manifest_path)
            assert manifest['batchNumber'] == index+1
            assert manifest['verifiedComicCount'] == len(manifest['questionIds'])
            event_ids = []
            for qid in manifest['questionIds']:
                candidates = [j for j in eligible if j['id'] == qid
                              and j['integrationEventId'] not in used
                              and j['integratedAt'] <= manifest['throughIntegratedAt']]
                assert candidates, f'No historical work event for {manifest_path.name}: {qid}'
                job = min(candidates, key=lambda j: j['integratedAt'])
                event_id = job['integrationEventId']
                used.add(event_id)
                event_ids.append(event_id)
            commit = (load(manifests[index+1])['previousHEAD'] if index+1 < len(manifests)
                      else state['lastPushedCommit'])
            batches.append(dict(batchNumber=manifest['batchNumber'], commit=commit,
                                eventIds=event_ids, questionIds=manifest['questionIds'],
                                legacyReceipt=str(manifest_path.relative_to(ROOT)),
                                legacyReceiptSHA256=hashlib.sha256(manifest_path.read_bytes()).hexdigest()))
        assert len(used) == sum(b['verifiedComicCount'] for b in map(load, manifests))
        pending = [j for j in eligible if j['integrationEventId'] not in used]
        # Assign a stable ordering; UTC is no longer consulted after migration.
        ordered = sorted([j for j in pipeline['jobs'] if j['state'] == 'integrated'],
                         key=lambda j: j.get('integratedAt', ''))
        for sequence, job in enumerate(ordered, 1):
            job.setdefault('integrationSequence', sequence)
        pipeline['nextIntegrationSequence'] = max([j.get('integrationSequence', 0) for j in pipeline['jobs']] or [0])
        ledger = dict(version=2, baselineExcludedEventIds=excluded, publishedBatches=batches,
                      migratedAt=datetime.now(timezone.utc).isoformat(),
                      migration=dict(baselineAt=policy['baselineAt'], publishedEventCount=len(used),
                                     eligibleAtMigration=len(eligible), pendingEventCount=len(pending),
                                     pendingQuestionIds=[j['id'] for j in pending],
                                     remoteCommitVerified=state.get('lastPushedCommit'),
                                     historicalReceiptsPreserved=True,
                                     note='Legacy UTC boundary frozen once; new work uses event identity regardless of UTC.'))
        save(ROOT/'docs/comics/pipeline.json', pipeline)
        save(path, ledger)
    state['publicationLedgerVersion'] = 2
    save(state_path, state)
    return ledger


def _pending_batch():
    policy = load(ROOT/'docs/comics/commit-policy.json')
    state_path = ROOT/'.cache/comic-publish-state.json'
    state = load(state_path) if state_path.exists() else {}
    ledger = _ensure_ledger(policy, state_path, state)
    published = {event for batch in ledger['publishedBatches'] for event in batch['eventIds']}
    excluded = set(ledger['baselineExcludedEventIds'])
    jobs = [j for j in load(ROOT/'docs/comics/pipeline.json')['jobs']
            if j['state'] == 'integrated' and j.get('decision') == 'complete']
    assert all(j.get('integrationEventId') for j in jobs), 'Integrated job is missing its event identity.'
    event_ids = [j['integrationEventId'] for j in jobs]
    assert len(event_ids) == len(set(event_ids)), 'Distinct work attempts must have distinct events.'
    jobs = [j for j in jobs if j['integrationEventId'] not in published | excluded]
    jobs.sort(key=lambda j: j.get('integrationSequence', 0))
    return policy, state_path, state, jobs


def pending_batch():
    with (ROOT/'.cache/comic-publish.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return _pending_batch()


def _finish_push(state_path, state, pending, remote):
    """Idempotently record success, including a crash after ledger save."""
    ledger = load(ROOT/LEDGER)
    existing = next((b for b in ledger['publishedBatches'] if b['batchNumber'] == pending['batchNumber']), None)
    if existing:
        assert existing['commit'] == remote and existing['eventIds'] == pending['integrationEventIds']
    else:
        used = {event for batch in ledger['publishedBatches'] for event in batch['eventIds']}
        assert not used.intersection(pending['integrationEventIds']), 'Do not publish a work event twice.'
        ledger['publishedBatches'].append(dict(batchNumber=pending['batchNumber'], commit=remote,
                                               eventIds=pending['integrationEventIds'], questionIds=pending['questionIds']))
        save(ROOT/LEDGER, ledger)
    state.update(throughIntegratedAt=pending['throughIntegratedAt'],
                 lastPushedCommit=remote, batchNumber=pending['batchNumber'],
                 pushedAt=datetime.now(timezone.utc).isoformat(), publicationLedgerVersion=2)
    state.pop('pendingPush', None)
    save(state_path, state)


def publish():
    with (ROOT/'.cache/comic-publish.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        policy, state_path, state, jobs = _pending_batch()
        assert policy['enabled'] and not policy.get('allowForcePush')
        if not state.get('pendingPush'):
            assert len(jobs) >= policy['batchSize'], 'Fewer than 20 verified, integrated comics.'
            jobs = jobs[:policy['batchSize']]
            checks = subprocess.run(['npm', 'test', '--prefix', 'site'], cwd=ROOT, capture_output=True, text=True)
            (ROOT/'.cache/comic-publish-site-tests.log').write_text(checks.stdout+checks.stderr)
            checks.check_returncode()
            passed = re.search(r'\bpass (\d+)', checks.stdout)
            assert passed, 'Test runner did not report its pass count.'
            for job in jobs:
                spec = load(ROOT/'docs/comics'/f'{job["id"]}.json')
                assert spec.get('rootReview', {}).get('visualChecked'), job['id']
                assert (ROOT/'site/dist'/spec['nativeArt']).is_file(), job['id']
            assert git('branch', '--show-current') == 'main', 'Publish the authorized main branch only.'
            batch_number = state.get('batchNumber', 0)+1
            record = dict(preparedAt=datetime.now(timezone.utc).isoformat(), batchNumber=batch_number,
                          previousHEAD=git('rev-parse', 'HEAD'), verifiedComicCount=len(jobs),
                          questionIds=[j['id'] for j in jobs], integrationEventIds=[j['integrationEventId'] for j in jobs],
                          throughIntegratedAt=jobs[-1]['integratedAt'],
                          datasetRevision=load(ROOT/'site/dist/data.json')['revision'],
                          checks=dict(siteTests=int(passed[1]), entryViewportCheckReport='docs/site-checks/entry-modes-2026-10-29.json', rawRasterExcludedFromGit=True),
                          policy='User authorized commit all and push each 20 verified work events; UTC is only a label.')
            save(ROOT/'docs/comics'/f'publish-batch-2026-10-29-{batch_number:03d}.json', record)
            with locked(ROOT):
                subprocess.run(['git', 'add', '-A'], cwd=ROOT, check=True)
                subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
                assert not git('ls-files', 'docs/**/*.png', 'docs/**/*.jpg', 'docs/**/*.webp', 'docs/**/*.pdf', 'docs/**/*.html')
                subprocess.run(['git', 'commit', '-m', f'Publish {len(jobs)} verified teaching comics and current site updates'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
                state['pendingPush'] = {**record, 'commit': git('rev-parse', 'HEAD')}
                save(state_path, state)
        pending = state['pendingPush']
        assert git('rev-parse', 'HEAD') == pending['commit'], 'Finish the recorded push before another commit.'
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=ROOT, check=True)
        remote = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
        assert remote == pending['commit']
        _finish_push(state_path, state, pending, remote)
        return dict(commit=remote, verifiedComicCount=pending['verifiedComicCount'],
                    throughIntegratedAt=state['throughIntegratedAt'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    if args.publish:
        print(__import__('json').dumps(publish(), ensure_ascii=False))
    else:
        policy, _, state, jobs = pending_batch()
        print(__import__('json').dumps(dict(readyToPublish=bool(state.get('pendingPush')) or len(jobs) >= policy['batchSize'],
                                          verifiedComicCount=len(jobs), questionIds=[j['id'] for j in jobs]), ensure_ascii=False))
