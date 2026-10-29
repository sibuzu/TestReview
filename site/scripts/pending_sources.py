"""Expose the actual unfinished import queue without counting completed archives."""
import hashlib
import json
from pathlib import Path

TERMINAL = {
    'complete', 'complete_with_skips', 'duplicate', 'skipped_not_in_site',
    'skipped_missing_images', 'excluded_no_question', 'skipped_unavailable',
    'skipped_invalid_question',
}


def apply_pending_sources(sources, root):
    by_id = {source['id']: source for source in sources}
    by_url = {source['url'].rstrip('/'): source for source in sources}
    for filename, prefix, platform in [
        ('more-gpt-progress.json', 'src-more-', 'ChatGPT'),
        ('more-gemini-progress.json', 'src-gemini-more-', 'Gemini'),
    ]:
        path = root / 'docs/imports' / filename
        if not path.exists():
            continue
        for entry in json.loads(path.read_text())['sources']:
            sid = prefix + f"{entry['order']:03}"
            source = by_id.get(sid) or by_url.get(entry['url'].rstrip('/'))
            unfinished = entry['state'] not in TERMINAL
            if not unfinished:
                if source and source['id'] == sid:
                    source['status'] = 'read'
                continue
            if source is None:
                source = dict(
                    id=sid, url=entry['url'], status='pending',
                    title=entry.get('title') or f"{platform} 待整理來源 {entry['order']}",
                    platform=platform, date=entry.get('createdDate', ''),
                    addedAt='2026-10-27', note='', content='', transcript='', images=[],
                )
                sources.append(source)
                by_id[sid] = source
                by_url[source['url'].rstrip('/')] = source
            source['status'] = 'pending'
            count = len(entry.get('questionIds', []))
            source['note'] = entry.get('reason') or (
                f'已整理{count}題，尚有內容待核對或補圖。' if count
                else '已加入整理清單，尚未完成原題及圖片核對。'
            )
    return sum(source['status'] == 'pending' for source in sources)


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[2]
    path = root / 'site/dist/data.json'
    payload = json.loads(path.read_text())
    count = apply_pending_sources(payload['sources'], root)
    digest = hashlib.sha256(json.dumps(
        [payload['sources'], payload['questions']], ensure_ascii=False, sort_keys=True
    ).encode()).hexdigest()[:12]
    payload['revision'] = '2026-10-27.' + digest
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(f'{count} sources remain in the import queue.')
