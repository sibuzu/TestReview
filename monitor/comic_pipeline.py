"""Atomic reservations and staging; workers continue without waiting for integration."""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
from .comic_queue import SETTLED, next_entry

ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    return json.loads(path.read_text())


def save(path, data):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    os.replace(temporary, path)


@contextmanager
def locked(root=ROOT):
    with (root/'monitor/comic-pipeline.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def update_display(root, pipeline):
    display = load(root/'monitor/parallel.json')
    for lane in display['lanes']:
        jobs = [j for j in pipeline['jobs'] if j['lane'] == lane['lane']]
        current = next((j for j in reversed(jobs) if j['state'] == 'claimed'), None)
        if current:
            lane.update(questionId=current['id'], title=current['title'], state='running', startedAt=current['startedAt'])
        else:
            lane['state'] = 'idle'
    ready = [j for j in pipeline['jobs'] if j['state'] == 'ready']
    active_ready, held = ready, []
    priority_path = root/'monitor/priority-source.json'
    if priority_path.exists():
        priority = load(priority_path)
        if priority.get('state') not in ('complete', 'cancelled'):
            allowed = set(priority.get('questionIds', []))
            active_ready = [j for j in ready if j['id'] in allowed]
            held = [j for j in ready if j['id'] not in allowed]
    display.update(updatedAt=now(), ready=ready,
                   waiting=[j for j in active_ready if not j.get('integrationStartedAt')],
                   integrating=[j for j in active_ready if j.get('integrationStartedAt')], held=held,
                   integrated=sum(j['state'] == 'integrated' for j in pipeline['jobs']),
                   blocked=[j for j in pipeline['jobs'] if j['state'] == 'blocked'])
    save(root/'monitor/parallel.json', display)


def claim(root, lane):
    with locked(root):
        pipeline = load(root/'docs/comics/pipeline.json')
        existing = next((j for j in pipeline['jobs'] if j['lane'] == lane and j['state'] == 'claimed'), None)
        if existing:
            return existing
        if pipeline.get('claimsPaused'):
            return None
        progress = load(root/'docs/comics/progress.json')
        reserved = {j['id'] for j in pipeline['jobs'] if j['state'] != 'integrated'}
        entries = progress['entries']
        priority_path = root/'monitor/priority-source.json'
        if priority_path.exists():
            priority = load(priority_path)
            if priority.get('state') not in ('complete', 'cancelled'):
                allowed = set(priority.get('questionIds', []))
                assignments = priority.get('laneAssignments', {})
                if assignments:
                    allowed &= set(assignments.get(str(lane), []))
                entries = [e for e in entries if e['id'] in allowed]
        candidate = next_entry([dict(e, state='reserved') if e['id'] in reserved else e for e in entries])
        if not candidate:
            return None
        job = dict(id=candidate['id'], title=candidate['title'], subject=candidate['subject'], lane=lane,
                   state='claimed', startedAt=now())
        pipeline['jobs'].append(job)
        save(root/'docs/comics/pipeline.json', pipeline)
        update_display(root, pipeline)
        return job


def stage(root, qid, decision, reason, evidence):
    assert decision in SETTLED | {'awaiting_confirmation'}
    assert evidence and all((root/p).is_file() and Path(p).is_relative_to('docs/comics') for p in evidence)
    with locked(root):
        pipeline = load(root/'docs/comics/pipeline.json')
        job = next(j for j in pipeline['jobs'] if j['id'] == qid)
        assert job['state'] == 'claimed', 'Only the assigned worker can finish a claimed job once.'
        job.update(state='blocked' if decision == 'awaiting_confirmation' else 'ready', readyAt=now(),
                   decision=decision, reason=reason, evidence=evidence)
        save(root/'docs/comics/pipeline.json', pipeline)
        update_display(root, pipeline)
        return job


def integrated(root, qid):
    """Root only, after artifact review and any attach/curate/integrated QA."""
    with locked(root):
        pipeline = load(root/'docs/comics/pipeline.json')
        job = next(j for j in pipeline['jobs'] if j['id'] == qid)
        assert job['state'] == 'ready'
        finished = now()
        progress = load(root/'docs/comics/progress.json')
        entry = next(e for e in progress['entries'] if e['id'] == qid)
        integration_started = job.get('integrationStartedAt', finished)
        entry.update(state=job['decision'], reason=job['reason'], reviewStartedAt=job['startedAt'],
                     workerLane=job['lane'], workerReadyAt=job['readyAt'], completedAt=finished,
                     checkedAt=finished, visualChecked=True,
                     integrationQueueSeconds=(datetime.fromisoformat(integration_started)-datetime.fromisoformat(job['readyAt'])).total_seconds(),
                     integrationSeconds=(datetime.fromisoformat(finished)-datetime.fromisoformat(integration_started)).total_seconds())
        if job['decision'] == 'complete':
            spec_path = root/'docs/comics'/f'{qid}.json'
            spec = load(spec_path)
            assert spec.get('nativeArt') and (root/'docs/comics'/f'{qid}-validation.json').exists()
            spec.update(visualChecked=True, checkedAt=finished, validationFile=f'docs/comics/{qid}-validation.json')
            save(spec_path, spec)
            entry.update(nativeArt=spec['nativeArt'], layoutVersion=spec['layoutVersion'],
                         questionUrl=f'https://monitor.sibuzu.com/site/index.html#question/{qid}')
        progress['updatedAt'] = finished
        save(root/'docs/comics/progress.json', progress)
        job.update(state='integrated', integratedAt=finished, integrationQueueSeconds=entry['integrationQueueSeconds'], integrationSeconds=entry['integrationSeconds'])
        save(root/'docs/comics/pipeline.json', pipeline)
        update_display(root, pipeline)
        counts = Counter(e['state'] for e in progress['entries'])
        settled = sum(counts[state] for state in SETTLED)
        save(root/'monitor/activity.json', {
            'title': f'三路製作、依序整合：已完成檢查{settled}／{len(progress["entries"])}題',
            'detail': f'剛整合{qid}。新製圖文{counts["complete"]}題、保留既有AI圖{counts["existing_ai"]}題、無需新漫畫{counts["not_suitable"]}題；工作線完成本題即暫存續領，主路持續整合。',
            'goalStatus': 'active', 'updatedAt': finished})
        return job


def begin(root, qid):
    with locked(root):
        pipeline = load(root/'docs/comics/pipeline.json')
        job = next(j for j in pipeline['jobs'] if j['id'] == qid)
        assert job['state'] == 'ready'
        job.setdefault('integrationStartedAt', now())
        save(root/'docs/comics/pipeline.json', pipeline)
        update_display(root, pipeline)
        return job


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['claim', 'stage', 'begin', 'integrated', 'status'])
    parser.add_argument('--lane', type=int, choices=[1, 2, 3])
    parser.add_argument('--id')
    parser.add_argument('--decision', choices=sorted(SETTLED | {'awaiting_confirmation'}))
    parser.add_argument('--reason')
    parser.add_argument('--evidence', nargs='+')
    args = parser.parse_args()
    if args.action == 'claim':
        assert args.lane
        result = claim(ROOT, args.lane)
    elif args.action == 'stage':
        assert args.id and args.decision and args.reason
        result = stage(ROOT, args.id, args.decision, args.reason, args.evidence)
    elif args.action == 'integrated':
        result = integrated(ROOT, args.id)
    elif args.action == 'begin':
        result = begin(ROOT, args.id)
    else:
        result = load(ROOT/'docs/comics/pipeline.json')
    print(json.dumps(result, ensure_ascii=False, indent=2))
