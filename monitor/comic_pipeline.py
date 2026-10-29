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


def active_priority(root):
    for filename in ('rework-priority.json', 'priority-source.json'):
        path = root/'monitor'/filename
        if path.exists():
            priority = load(path)
            if priority.get('state') not in ('complete', 'cancelled'):
                return priority
    return None


def update_display(root, pipeline):
    display = load(root/'monitor/parallel.json')
    for lane in display['lanes']:
        jobs = [j for j in pipeline['jobs'] if j['lane'] == lane['lane']]
        current = next((j for j in reversed(jobs) if j['state'] == 'claimed'), None)
        if current:
            lane.update(questionId=current['id'], title=current['title'], state='running', startedAt=current['startedAt'])
        elif lane.get('role') == 'integration':
            integrating = [j for j in pipeline['jobs'] if j['state'] == 'ready' and j.get('integrationStartedAt')]
            lane.update(questionId=integrating[0]['id'] if integrating else None,
                        title='、'.join(j['id'] for j in integrating) if integrating else '等待下一批整合',
                        state='integrating' if integrating else 'preparing')
        else:
            lane['state'] = 'idle'
    ready = [j for j in pipeline['jobs'] if j['state'] == 'ready']
    active_ready, held = ready, []
    priority = active_priority(root)
    if priority:
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
        configuration = load(root/'monitor/parallel.json')
        lane_configuration = next((item for item in configuration.get('lanes', []) if item['lane'] == lane), {})
        if lane_configuration.get('role') == 'integration':
            return None
        if pipeline.get('claimsPaused'):
            return None
        progress = load(root/'docs/comics/progress.json')
        reserved = {j['id'] for j in pipeline['jobs'] if j['state'] != 'integrated'}
        entries = progress['entries']
        priority = active_priority(root)
        if priority:
            allowed = set(priority.get('questionIds', []))
            assignments = priority.get('laneAssignments', {})
            if assignments:
                allowed &= set(assignments.get(str(lane), []))
            # Preserve whole-bank totals/completions for completed²/total;
            # only availability is limited to the active priority scope.
            entries = [dict(e, state='reserved') if e['id'] not in allowed and e['state']=='queued' else e for e in entries]
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
        job = next((j for j in reversed(pipeline['jobs']) if j['id'] == qid and j['state'] == 'claimed'), None)
        assert job is not None, 'Only the assigned worker can finish a claimed job once.'
        policy_path = root/'docs/comics/policy.json'
        if policy_path.exists() and not load(policy_path).get('reuseSourceAI', True):
            assert decision != 'existing_ai', 'Current user policy requires new four-panel artwork, not source AI reuse.'
            entry = next(e for e in load(root/'docs/comics/progress.json')['entries'] if e['id'] == qid)
            if entry.get('freshFourPanelRequired'):
                assert decision in ('complete', 'awaiting_confirmation'), 'This reopened question requires fresh four-panel artwork.'
        job.update(state='blocked' if decision == 'awaiting_confirmation' else 'ready', readyAt=now(),
                   decision=decision, reason=reason, evidence=evidence)
        save(root/'docs/comics/pipeline.json', pipeline)
        update_display(root, pipeline)
        return job


def integrated(root, qid):
    """The single integration owner, after artifact review and formal QA."""
    with locked(root):
        pipeline = load(root/'docs/comics/pipeline.json')
        job = next((j for j in reversed(pipeline['jobs']) if j['id'] == qid and j['state'] == 'ready'), None)
        assert job is not None
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
        priority = active_priority(root)
        if priority and priority.get('kind') == 'rework':
            scope = set(priority['questionIds'])
            completed = sum(e['id'] in scope and e['state']=='complete' for e in progress['entries'])
            save(root/'monitor/activity.json', {
                'title': f'54題重作優先：{completed}／{len(scope)}已整合（全題庫{settled}／{len(progress["entries"])}）',
                'detail': f'剛整合{qid}；製作線只領重作清單，其他已製作項目暫存。全新四格依教學效果選用幾何／結構或情境圖，維持WebP與共用資產減量。',
                'goalStatus': 'active', 'updatedAt': finished})
            return job
        save(root/'monitor/activity.json', {
            'title': f'兩路製作、一路整合：已完成檢查{settled}／{len(progress["entries"])}題',
            'detail': f'剛整合{qid}。新製圖文{counts["complete"]}題、保留既有AI圖{counts["existing_ai"]}題、無需新漫畫{counts["not_suitable"]}題；兩路完成本題即暫存續領，專職整合線持續核對，主代理保留回應與機動。',
            'goalStatus': 'active', 'updatedAt': finished})
        return job


def begin(root, qid):
    with locked(root):
        pipeline = load(root/'docs/comics/pipeline.json')
        job = next((j for j in reversed(pipeline['jobs']) if j['id'] == qid and j['state'] == 'ready'), None)
        assert job is not None
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
