"""Register a substantive question/AI correction with both review links.

Run after curate.py so the confirmation contains the published question.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from monitor.confirmation_store import edit_confirmations


def full_question_text(question):
    sections = []
    if question.get('passage'):
        sections.append('作答材料：\n'+question['passage'])
    for table in question.get('tables', []):
        lines = [table.get('caption', ''), '｜'.join(table.get('headers', []))]
        lines.extend('｜'.join(row) for row in table.get('rows', []))
        sections.append('\n'.join(line for line in lines if line))
    sections.append(question['question'])
    return '\n\n'.join(sections)


def register(question_id, reason, before, after, source_url=None, kind='題目訂正確認', root=ROOT):
    data = json.loads((root/'site/dist/data.json').read_text())
    question = next(q for q in data['questions'] if q['id'] == question_id)
    if not source_url:
        source_url = next(s['url'] for s in data['sources'] if s['id'] == question['sourceId'])
    url = urlsplit(source_url)
    if url.scheme != 'https' or url.hostname not in {'chatgpt.com', 'share.gemini.google', 'gemini.google.com'}:
        raise ValueError('A readable original AI conversation link is required')
    signature = hashlib.sha256(json.dumps([question_id, reason, before, after, source_url]).encode()).hexdigest()[:12]
    request_id = 'correction-'+question_id+'-'+signature
    question_url = '/site/index.html#question/'+question_id
    request = {
        'id': request_id, 'state': 'pending', 'kind': kind, 'title': question['title'],
        'questionId': question_id, 'questionText': full_question_text(question),
        'questionUrl': question_url, 'url': question_url, 'sourceUrl': source_url,
        'questions': [reason, '修改前／原AI內容：'+before, '目前處理：'+after],
        'before': before, 'after': after, 'createdAt': datetime.now(timezone.utc).isoformat(),
    }
    with edit_confirmations(root) as confirmations:
        if not any(item['id'] == request_id for item in confirmations.get('requests', [])+confirmations.get('resolved', [])):
            confirmations.setdefault('requests', []).append(request)
    return request_id


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question_id')
    parser.add_argument('--reason', required=True)
    parser.add_argument('--before', required=True)
    parser.add_argument('--after', required=True)
    parser.add_argument('--source-url')
    parser.add_argument('--kind', default='題目訂正確認')
    args = parser.parse_args()
    print(register(args.question_id, args.reason, args.before, args.after, args.source_url, args.kind))
