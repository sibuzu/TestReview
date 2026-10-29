"""Current user-assigned sources, separate from completed priority batches."""
import json


def current_sources(root, source_rows, questions, entries, confirmations, paths, source_catalog=None):
    plan_path = root/'docs/imports/new-source-plan-2026-10-29.json'
    selector = root/'monitor/active-source-plan.json'
    if selector.is_file():
        paths.append(selector)
        plan_path = root/json.loads(selector.read_text())['path']
    if not plan_path.exists():
        return None
    paths.append(plan_path)
    plan = json.loads(plan_path.read_text())
    published = {q['id'] for q in questions}
    by_id = {q['id']: q for q in questions}
    states = {e['id']: e['state'] for e in entries}
    rows, all_ids, all_original_ids = [], set(), set()
    terminal = {'complete', 'complete_with_skips', 'duplicate', 'excluded_no_question',
                'skipped_not_in_site', 'skipped_missing_images', 'skipped_unavailable',
                'skipped_invalid_question'}
    for item in plan.get('sources', []):
        batch = item.get('batch', 'gemini')
        candidates = (source_catalog or {}).get(batch, source_rows)
        source = next((s for s in candidates if s['order'] == item['suggestedOrder']), {})
        reports = []
        for relative in (item.get('acquisitionRecord'),
                         f'docs/acquisition/{batch}-{item["suggestedOrder"]:03d}.json'):
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
                       [r.get('imagesExpected') or r.get('userImagesExpected') or
                        len(r.get('originalImages', [])) for r in reports])
        source_id = source.get('sourceId') or item.get('sourceId') or f'src-gemini-more-{item["suggestedOrder"]:03d}'
        ids = (set(source.get('questionIds', [])) |
               {q['id'] for q in questions if q.get('sourceId') == source_id}) & published
        all_ids.update(ids)
        original_ids = {child['id'] for qid in ids
                        for child in (by_id[qid].get('groupQuestions') or [by_id[qid]])}
        all_original_ids.update(original_ids)
        state = source.get('state', 'awaiting_source_read')
        reason = source.get('reason', '')
        if state == 'awaiting_source_read' and any(r.get('state') in {
                'awaiting_chrome_approval', 'awaiting_browser_access'} for r in reports):
            reason = '對話文字已保存本機；取原卷的程式正等待 Chrome 允許連線，尚未開始判題。'
        # Acquisition writes its own reports; never change the curated records
        # merely to display downloaded originals in the monitor.
        if state == 'awaiting_source_read' and expected and len(images) >= expected:
            state = 'awaiting_transcription'
            reason = ('對話與原圖已保存本機，待逐題整理。'
                      '取回圖文不代表已完成錄題或插畫。')
        rows.append({'batch': batch, 'lane': item.get('lane'),
                     'order': item['suggestedOrder'], 'url': item['url'],
                     'title': next((r['title'] for r in reports if r.get('title')), source.get('title', item['key'])),
                     'state': state, 'reason': reason,
                     'settled': bool(source.get('sourceCurationComplete')) or source.get('state') in terminal,
                     'imagesAvailable': len(images), 'imagesExpected': expected or None,
                     'originalsExpected': item.get('expectedOriginalQuestions'),
                     'originalsPublished': len(original_ids),
                     'questionIds': sorted(ids),
                     'published': len(ids), 'generated': sum(states.get(qid) == 'complete' for qid in ids)})
    settled = sum(row['settled'] for row in rows)
    assigned_keys = {item['key'] for item in plan.get('sources', [])}
    assigned_urls = {item['url'] for item in plan.get('sources', [])}
    pending_ids = {r.get('questionId') or r.get('id') for r in confirmations
                   if (r.get('questionId') or r.get('id')) in all_ids
                   or r.get('sourceKey') in assigned_keys or r.get('sourceUrl') in assigned_urls}
    comics_settled=sum(states.get(qid) in {'complete','not_suitable','existing_ai'} for qid in all_ids)
    agents = []
    parallel_path = root/'monitor/parallel.json'
    if plan.get('showAgents') and parallel_path.is_file():
        paths.append(parallel_path)
        agents = json.loads(parallel_path.read_text()).get('lanes', [])
    return {'sources': rows, 'total': len(rows), 'settled': settled,
            'agents': agents,
            'originalsExpected': sum(item.get('expectedOriginalQuestions') or 0 for item in plan.get('sources', [])),
            'originalsPublished': len(all_original_ids),
            'originalsGenerated': sum(states.get(qid) == 'complete' for qid in all_original_ids),
            'complete':settled==len(rows) and not pending_ids and comics_settled==len(all_ids),
            'comicsSettled':comics_settled,
            'percent': round(100*settled/len(rows)) if rows else 0,
            'imagesAvailable': sum(row['imagesAvailable'] for row in rows),
            'imagesExpected': sum(row['imagesExpected'] or 0 for row in rows),
            'acquiredSources': sum(row['imagesExpected'] is not None and
                                   row['imagesAvailable'] >= row['imagesExpected'] for row in rows),
            'published': len(all_ids), 'generated': sum(states.get(qid) == 'complete' for qid in all_ids),
            'awaitingConfirmation': len(pending_ids)}
