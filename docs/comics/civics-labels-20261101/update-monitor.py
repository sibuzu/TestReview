"""Publish this batch's verified integration progress to the existing monitor."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from monitor.comic_pipeline import locked, save

with locked(ROOT):
    path = ROOT / 'docs/comics/civics-labels-20261101/progress.json'
    batch = json.loads(path.read_text())
    previous_items = json.dumps(batch['items'], sort_keys=True)
    pipeline = json.loads((ROOT / 'docs/comics/pipeline.json').read_text())
    for item in batch['items']:
        jobs = [j for j in pipeline['jobs'] if j['id'] == item['id']
                and j['startedAt'] >= batch['startedAt']]
        if jobs:
            job = jobs[-1]
            state = job['state']
            item['state'] = ('complete' if state == 'integrated'
                             else 'integrating' if job.get('integrationStartedAt')
                             else state)
            item['jobId'] = job['jobId']
    if previous_items == json.dumps(batch['items'], sort_keys=True):
        print('No work transition; keeping the last activity timestamp.')
        sys.exit(0)
    now = datetime.now(timezone.utc).isoformat()
    done = sum(q['state'] == 'complete' for q in batch['items'])
    batch.update(updatedAt=now, state='complete' if done == len(batch['items']) else 'active')
    if batch['state'] == 'complete':
        batch.setdefault('completedAt', now)
    save(path, batch)
    save(ROOT / 'monitor/activity.json', {
        'title': f'{batch["title"]}：{done}／{len(batch["items"])}完成',
        'detail': batch['description'],
        'updatedAt': now, 'goalStatus': batch['state'], 'comicRework': batch,
    })
print(f'{done}/{len(batch["items"])} complete')
