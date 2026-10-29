"""Current user-assigned sources, separate from completed priority batches."""
import json


def current_sources(root, source_rows, questions, entries, confirmations, paths):
    plan_path = root/'docs/imports/new-source-plan-2026-10-29.json'
    if not plan_path.exists():
        return None
    paths.append(plan_path)
    plan = json.loads(plan_path.read_text())
    published = {q['id'] for q in questions}
    states = {e['id']: e['state'] for e in entries}
    rows, all_ids = [], set()
    terminal = {'complete', 'complete_with_skips', 'duplicate', 'excluded_no_question',
                'skipped_not_in_site', 'skipped_missing_images', 'skipped_unavailable',
                'skipped_invalid_question'}
    for item in plan.get('sources', []):
        source = next((s for s in source_rows if s['order'] == item['suggestedOrder']), {})
        reports = []
        for relative in (item.get('acquisitionRecord'),
                         f'docs/acquisition/gemini-{item["suggestedOrder"]:03d}.json'):
            if relative and (root/relative).is_file():
                path = root/relative
                paths.append(path)
                reports.append(json.loads(path.read_text()))
        images = {}
        for record in [source, *reports]:
            for image in record.get('downloadedImages', record.get('originalImages', [])):
                relative = image.get('path')
                if relative and (root/relative).is_file():
                    images[image.get('sha256') or relative] = relative
        expected = max([source.get('archiveImages') or 0] +
                       [r.get('imagesExpected') or len(r.get('originalImages', [])) for r in reports])
        source_id = source.get('sourceId') or f'src-gemini-more-{item["suggestedOrder"]:03d}'
        ids = (set(source.get('questionIds', [])) |
               {q['id'] for q in questions if q.get('sourceId') == source_id}) & published
        all_ids.update(ids)
        state = source.get('state', 'awaiting_source_read')
        reason = source.get('reason', '')
        # Acquisition writes its own reports; never change the curated records
        # merely to display downloaded originals in the monitor.
        if state == 'awaiting_source_read' and expected and len(images) >= expected:
            state = 'awaiting_transcription'
            reason = ('對話與原圖已保存本機，待逐題整理；本批只收入原卷有紅字訂正的題目。'
                      '取回圖文不代表已完成錄題或插畫。')
        rows.append({'order': item['suggestedOrder'], 'url': item['url'],
                     'title': next((r['title'] for r in reports if r.get('title')), source.get('title', item['key'])),
                     'state': state, 'reason': reason,
                     'settled': bool(source.get('sourceCurationComplete')) or source.get('state') in terminal,
                     'imagesAvailable': len(images), 'imagesExpected': expected or None,
                     'questionIds': sorted(ids),
                     'published': len(ids), 'generated': sum(states.get(qid) == 'complete' for qid in ids)})
    settled = sum(row['settled'] for row in rows)
    assigned_keys = {item['key'] for item in plan.get('sources', [])}
    assigned_urls = {item['url'] for item in plan.get('sources', [])}
    pending_ids = {r.get('questionId') or r.get('id') for r in confirmations
                   if (r.get('questionId') or r.get('id')) in all_ids
                   or r.get('sourceKey') in assigned_keys or r.get('sourceUrl') in assigned_urls}
    comics_settled=sum(states.get(qid) in {'complete','not_suitable','existing_ai'} for qid in all_ids)
    return {'sources': rows, 'total': len(rows), 'settled': settled,
            'complete':settled==len(rows) and not pending_ids and comics_settled==len(all_ids),
            'comicsSettled':comics_settled,
            'percent': round(100*settled/len(rows)) if rows else 0,
            'imagesAvailable': sum(row['imagesAvailable'] for row in rows),
            'imagesExpected': sum(row['imagesExpected'] or 0 for row in rows),
            'acquiredSources': sum(row['imagesExpected'] is not None and
                                   row['imagesAvailable'] >= row['imagesExpected'] for row in rows),
            'published': len(all_ids), 'generated': sum(states.get(qid) == 'complete' for qid in all_ids),
            'awaitingConfirmation': len(pending_ids)}
