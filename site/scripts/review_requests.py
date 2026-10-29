"""Attach the questions a reader must verify, without completing unverified exercises."""
import hashlib
import json
from pathlib import Path


def apply_review_requests(records, root):
    requests = json.loads((root / 'docs/review-requests.json').read_text())
    pending = {
        q['id']: q for q in records
        if q.get('contentStatus') == '待更新'
        or q.get('verification') in ('待核對', '待補原題')
    }
    ordered = [qid for qid in requests if qid in pending]
    for q in records:
        for key in ('reviewQuestions', 'reviewExcerpt', 'reviewLabel', 'reviewPreviousId', 'reviewNextId'):
            q.pop(key, None)
    for index, qid in enumerate(ordered):
        q = pending[qid]
        request = requests[qid]
        q.update(
            reviewQuestions=request['questions'],
            reviewExcerpt=request.get('excerpt', ''),
            reviewLabel=f'優先核對 {index + 1}／{len(ordered)}',
            reviewPreviousId=ordered[index - 1] if index else '',
            reviewNextId=ordered[index + 1] if index + 1 < len(ordered) else '',
        )
    return len(ordered)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[2]
    path = root / 'site/dist/data.json'
    payload = json.loads(path.read_text())
    count = apply_review_requests(payload['questions'], root)
    digest = hashlib.sha256(json.dumps([payload['sources'], payload['questions']], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]
    payload['revision'] = '2026-10-27.' + digest
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(f'Updated review requests for {count} existing exercises.')
