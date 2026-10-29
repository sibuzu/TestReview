"""Single integration owner's publication after each authorized 20-comic batch."""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import re
from pathlib import Path
import subprocess
from .comic_pipeline import ROOT, load, save, locked


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def pending_batch():
    policy = load(ROOT/'docs/comics/commit-policy.json')
    state_path = ROOT/'.cache/comic-publish-state.json'
    state = load(state_path) if state_path.exists() else {}
    after = state.get('throughIntegratedAt', policy['baselineAt'])
    jobs = [j for j in load(ROOT/'docs/comics/pipeline.json')['jobs']
            if j['state']=='integrated' and j.get('decision')=='complete'
            and j.get('integratedAt', '') > after]
    jobs.sort(key=lambda j:j['integratedAt'])
    return policy, state_path, state, jobs


def publish():
    with (ROOT/'.cache/comic-publish.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        policy, state_path, state, jobs = pending_batch()
        assert policy['enabled'] and not policy.get('allowForcePush')
        if not state.get('pendingPush'):
            assert len(jobs)>=policy['batchSize'], 'Fewer than 20 verified, integrated comics.'
            checks=subprocess.run(['npm','test','--prefix','site'],cwd=ROOT,capture_output=True,text=True)
            (ROOT/'.cache/comic-publish-site-tests.log').write_text(checks.stdout+checks.stderr)
            checks.check_returncode()
            passed=re.search(r'\bpass (\d+)',checks.stdout)
            assert passed, 'Test runner did not report its pass count.'
            for job in jobs:
                spec=load(ROOT/'docs/comics'/f'{job["id"]}.json')
                assert spec.get('rootReview', {}).get('visualChecked'), job['id']
                assert (ROOT/'site/dist'/spec['nativeArt']).is_file(), job['id']
            branch=git('branch','--show-current')
            assert branch=='main', 'Publish the authorized main branch only.'
            batch_number=state.get('batchNumber',0)+1
            record={'preparedAt':datetime.now(timezone.utc).isoformat(),
                    'batchNumber':batch_number,'previousHEAD':git('rev-parse','HEAD'),
                    'verifiedComicCount':len(jobs),'questionIds':[j['id'] for j in jobs],
                    'throughIntegratedAt':jobs[-1]['integratedAt'],
                    'datasetRevision':load(ROOT/'site/dist/data.json')['revision'],
                    'checks':{'siteTests':int(passed[1]),
                              'entryViewportCheckReport':'docs/site-checks/entry-modes-2026-10-29.json',
                              'rawRasterExcludedFromGit':True},
                    'policy':'User authorized commit all and push each 20 verified comics.'}
            save(ROOT/'docs/comics'/f'publish-batch-2026-10-29-{batch_number:03d}.json',record)
            with locked():
                subprocess.run(['git','add','-A'],cwd=ROOT,check=True)
                subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
                assert not git('ls-files','docs/**/*.png','docs/**/*.jpg','docs/**/*.webp','docs/**/*.pdf','docs/**/*.html')
                subprocess.run(['git','commit','-m',f'Publish {len(jobs)} verified teaching comics and current site updates'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
                state['pendingPush']={**record,'commit':git('rev-parse','HEAD')}
                save(state_path,state)
        pending=state['pendingPush']
        assert git('rev-parse','HEAD')==pending['commit'], 'Finish the recorded push before another commit.'
        subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)
        remote=git('ls-remote','origin','refs/heads/main').split()[0]
        assert remote==pending['commit']
        state.update(throughIntegratedAt=pending['throughIntegratedAt'],
                     lastPushedCommit=remote,batchNumber=pending['batchNumber'],
                     pushedAt=datetime.now(timezone.utc).isoformat())
        state.pop('pendingPush')
        save(state_path,state)
        return {'commit':remote,'verifiedComicCount':pending['verifiedComicCount'],
                'throughIntegratedAt':state['throughIntegratedAt']}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish',action='store_true')
    args=parser.parse_args()
    if args.publish:
        print(json.dumps(publish(),ensure_ascii=False))
    else:
        policy,_,state,jobs=pending_batch()
        print(json.dumps({'readyToPublish':bool(state.get('pendingPush')) or len(jobs)>=policy['batchSize'],
                          'verifiedComicCount':len(jobs),'questionIds':[j['id'] for j in jobs]},ensure_ascii=False))
