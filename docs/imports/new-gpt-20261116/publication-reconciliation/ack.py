"""Source71-only, audited acknowledgement of an explicitly authorized normal push.

Default is read-only inspect. --ack --commit SHA is executed by Agent1 only after
normal push. No work events are created or edited; UTC is never a counting cursor.
"""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from monitor.comic_pipeline import locked, save

HERE = Path(__file__).resolve().parent
KEY = 'source71-normal-push-20261116'
BASE = json.loads((HERE.parent/'baseline.json').read_text())['head']
LEDGER = ROOT/'docs/comics/publication-ledger.json'
CACHE = ROOT/'.cache/comic-publish-state.json'
PIPELINE = ROOT/'docs/comics/pipeline.json'
NEW_IDS = {f'q-{n}' for n in range(1106, 1133)} - {'q-1122'}
OLD_IDS = {f'q-{n}' for n in range(1071, 1106)}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def committed(commit, path):
    return json.loads(git('show', commit+':'+path))


def eligible(pipeline):
    jobs = [j for j in pipeline['jobs'] if j['state']=='integrated' and j.get('decision')=='complete']
    events = [j.get('integrationEventId') for j in jobs]
    assert all(events) and len(events)==len(set(events)), 'Missing/duplicate integration identity'
    return jobs


def inspect(commit=None):
    ledger = json.loads(LEDGER.read_text())
    state = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    assert ledger['version']==2 and not state.get('pendingPush'), 'Finish any recorded push first'
    existing = [b for b in ledger['publishedBatches'] if b.get('manualAcknowledgementKey')==KEY]
    assert len(existing)<=1
    used = set(ledger['baselineExcludedEventIds']) | {
        e for b in ledger['publishedBatches'] if b not in existing for e in b['eventIds']}
    pipeline = committed(commit, 'docs/comics/pipeline.json') if commit else json.loads(PIPELINE.read_text())
    pending = sorted([j for j in eligible(pipeline) if j['integrationEventId'] not in used],
                     key=lambda j:j.get('integrationSequence',0))
    assert {j['id'] for j in pending}==OLD_IDS|NEW_IDS and len(pending)==61, 'Scope changed: refuse acknowledgement'
    old_jobs = {j['integrationEventId']:j for j in eligible(committed(BASE,'docs/comics/pipeline.json'))}
    previous = [j for j in pending if j['id'] in OLD_IDS]
    new = [j for j in pending if j['id'] in NEW_IDS]
    assert len(previous)==35 and len(new)==26
    for job in previous:
        old = old_jobs.get(job['integrationEventId'])
        assert old and all(old.get(k)==job.get(k) for k in
            ['id','jobId','integrationEventId','integrationSequence','integratedAt']), 'Old stable event changed'
        spec = committed(BASE, f'docs/comics/{job["id"]}.json')
        assert spec.get('rootReview',{}).get('visualChecked'), 'Old work was not formally verified'
        git('cat-file','-e',BASE+':site/dist/'+spec['nativeArt'])
    assert all(j['integrationEventId'] not in old_jobs for j in new), 'New event already existed in baseline'
    assert not any(j['id']=='q-1122' for j in pending)
    if commit:
        assert git('branch','--show-current')=='main'
        assert git('rev-parse','HEAD')==commit
        assert git('ls-remote','origin','refs/heads/main').split()[0]==commit, 'Remote main is not the pushed content commit'
        subprocess.run(['git','merge-base','--is-ancestor',BASE,commit],cwd=ROOT,check=True)
        live = {j['integrationEventId']:j for j in eligible(json.loads(PIPELINE.read_text()))}
        for job in pending:
            assert job['integrationEventId'] in live
            assert all(live[job['integrationEventId']].get(k)==job.get(k) for k in
                       ['id','jobId','state','decision','integrationSequence','integratedAt'])
        for job in new:
            qid=job['id'];spec=committed(commit,f'docs/comics/{qid}.json')
            assert spec.get('rootReview',{}).get('visualChecked')
            q=committed(commit,f'docs/complete-questions/{qid}.json')
            c=q['teachingComic'];images=[p.get('image') for p in c['panels']]+[c['fourth'].get('image')]
            assert len(images)==len(set(images))==4 and all(images)
            for image in images:git('cat-file','-e',commit+':site/dist/'+image)
    result=dict(key=KEY,baselineCommit=BASE,contentCommit=commit,
        oldAlreadyCommittedCount=35,newCompleteEventCount=26,totalAcknowledgedEvents=61,
        oldEventIds=[j['integrationEventId'] for j in previous],newEventIds=[j['integrationEventId'] for j in new],
        eventIds=[j['integrationEventId'] for j in pending],questionIds=[j['id'] for j in pending],
        throughIntegratedAt=pending[-1]['integratedAt'],awaitingWithoutCompleteEvent=['q-1122'],
        note='35 previously committed/verified events plus 26 source71 complete events; this is reconciliation, not 61 newly made comics or an automatic batch-of-20 publication.')
    return result,ledger,state,existing


def acknowledge(commit):
    with (ROOT/'.cache/comic-publish.lock').open('a') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        with locked(ROOT):
            proof,ledger,state,existing=inspect(commit)
            pipeline_sha=hashlib.sha256(PIPELINE.read_bytes()).hexdigest()
            for name,path in [('before-ledger.json',LEDGER),('before-publish-state.json',CACHE)]:
                target=HERE/name
                if not target.exists():target.write_bytes(path.read_bytes())
            if existing:
                batch=existing[0]
                assert batch['commit']==commit and batch['eventIds']==proof['eventIds']
            else:
                batch=dict(batchNumber=max((b['batchNumber'] for b in ledger['publishedBatches']),default=0)+1,
                    commit=commit,eventIds=proof['eventIds'],questionIds=proof['questionIds'],
                    manualAcknowledgementKey=KEY,kind='explicit_source_completion_and_prior_publication_reconciliation',
                    previouslyPublishedEventIds=proof['oldEventIds'],newlyPublishedEventIds=proof['newEventIds'],
                    evidence='docs/imports/new-gpt-20261116/publication-reconciliation/acknowledgement.json')
                ledger['publishedBatches'].append(batch)
                save(LEDGER,ledger)
            state.update(batchNumber=batch['batchNumber'],lastPushedCommit=commit,
                publicationLedgerVersion=2,throughIntegratedAt=proof['throughIntegratedAt'],
                pushedAt=datetime.now(timezone.utc).isoformat(),manualAcknowledgementKey=KEY)
            save(CACHE,state)
            all_used=set(ledger['baselineExcludedEventIds'])|{e for b in ledger['publishedBatches'] for e in b['eventIds']}
            remaining=[j for j in eligible(json.loads(PIPELINE.read_text())) if j['integrationEventId'] not in all_used]
            assert not remaining and hashlib.sha256(PIPELINE.read_bytes()).hexdigest()==pipeline_sha
            proof.update(acknowledged=True,batchNumber=batch['batchNumber'],pendingCompleteEvents=0,
                         pipelineUnchanged=True,acknowledgedAt=datetime.now(timezone.utc).isoformat())
            save(HERE/'acknowledgement.json',proof)
            return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit',help='Full content SHA; required for --ack, after normal push')
    parser.add_argument('--ack',action='store_true')
    args=parser.parse_args()
    if args.ack:
        assert args.commit, '--ack requires the pushed content commit'
        result=acknowledge(args.commit)
    else:
        result=inspect(args.commit)[0]
        save(HERE/'inspection.json',result)
    print(json.dumps({k:result[k] for k in ['key','contentCommit','oldAlreadyCommittedCount','newCompleteEventCount','totalAcknowledgedEvents','awaitingWithoutCompleteEvent']},ensure_ascii=False))
