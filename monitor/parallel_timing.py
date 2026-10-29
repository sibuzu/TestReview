"""Measure the first twenty completed reviews after the parallel dispatch."""
from collections import Counter
from datetime import datetime

SETTLED = {'complete', 'existing_ai', 'not_suitable'}


def measure(batch, entries):
    if batch.get('state') == 'complete' and len(batch.get('samples', [])) == batch['target']:
        return dict(batch)  # Keep the completed comparison reproducible after later edits.
    result = dict(batch)
    start = datetime.fromisoformat(batch['startedAt'])
    excluded = set(batch['baselineSettledIds'])
    samples = []
    for entry in entries:
        finished = entry.get('completedAt')
        if entry['id'] in excluded or entry['state'] not in SETTLED or not finished:
            continue
        if datetime.fromisoformat(finished) < start:
            continue
        samples.append({k: entry.get(k) for k in ('id', 'state', 'reviewStartedAt', 'workerReadyAt', 'completedAt', 'workerLane', 'integrationQueueSeconds', 'integrationSeconds')})
    samples.sort(key=lambda e: (datetime.fromisoformat(e['completedAt']), e['id']))
    samples = samples[:batch['target']]
    result.update(samples=samples, completed=len(samples), mix=dict(Counter(e['state'] for e in samples)))
    timed = [e for e in samples if e.get('integrationSeconds') is not None and e.get('workerReadyAt')]
    if timed:
        result['pipelineTiming'] = {
            'sampleCount': len(timed),
            'averageWorkerSeconds': sum((datetime.fromisoformat(e['workerReadyAt'])-datetime.fromisoformat(e['reviewStartedAt'])).total_seconds() for e in timed)/len(timed),
            'averageQueueSeconds': sum(e['integrationQueueSeconds'] for e in timed)/len(timed),
            'averageIntegrationSeconds': sum(e['integrationSeconds'] for e in timed)/len(timed),
            'note': '只含啟用暫存計時後有完整時間戳的題目；排隊與整合分開。'
        }
    if len(samples) == batch['target']:
        elapsed = (datetime.fromisoformat(samples[-1]['completedAt']) - start).total_seconds()
        average = elapsed / batch['target']
        result.update(state='complete', completedAt=samples[-1]['completedAt'], elapsedSeconds=elapsed,
                      averageSecondsPerQuestion=average,
                      comparisons=[dict(b, changePercent=(average / b['averageSecondsPerWork'] - 1) * 100,
                                        speedup=b['averageSecondsPerWork'] / average)
                                   for b in batch['baselines']])
    return result
