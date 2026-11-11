"""Explicit user scope controls also apply to ready or already attached drafts."""
import json


def assert_work_allowed(root, qid):
    path = root/'docs/comics/biology-rework-20261112/plan.json'
    if not path.exists():
        return
    plan = json.loads(path.read_text())
    control = plan.get('executionControl', {})
    if control.get('mode') != 'missing_only':
        return
    for entry in plan.get('entries', []):
        if qid in entry.get('originalQuestionIds', [entry['id']]):
            if 'missing_illustration' not in entry.get('reasons', []):
                raise ValueError(f'{qid}: 使用者已暫停重製；保留草稿，不續製作、驗收或整合。')
            return
