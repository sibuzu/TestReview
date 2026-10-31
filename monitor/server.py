"""WeiRuGo progress monitor with explicit user confirmation actions."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import hashlib
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    from .confirmation_store import edit_confirmations
    from .comic_queue import subject_stats, next_entry
    from .parallel_timing import measure
    from .new_sources import current_sources
    from .group_queue import summary as group_summary
except ImportError:  # Also support running python monitor/server.py.
    from confirmation_store import edit_confirmations
    from comic_queue import subject_stats, next_entry
    from parallel_timing import measure
    from new_sources import current_sources
    from group_queue import summary as group_summary

ROOT = Path(__file__).resolve().parents[1]
TERMINAL = {
    'complete', 'complete_with_skips', 'duplicate', 'skipped_not_in_site',
    'skipped_missing_images', 'excluded_no_question', 'skipped_unavailable',
    'skipped_invalid_question',
}
STATE_NAMES = {
    'complete': '完成', 'complete_with_skips': '完成（含明確跳過）',
    'duplicate': '重複來源', 'partial': '部分完成／需回查',
    'awaiting_transcription': '原圖已取得／待整理',
    'awaiting_crop_review': '待檢視裁切', 'awaiting_source_read': '待讀取來源',
    'awaiting_image_retry': '待重試原圖', 'skipped_not_in_site': '跳過：無原題',
    'skipped_missing_images': '跳過：原圖無法取得',
    'excluded_no_question': '排除：非題目', 'skipped_unavailable': '跳過：連結失效',
    'skipped_invalid_question': '排除：原題有誤',
}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def iso_time(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def confirmation_token(request):
    fields = ('id', 'title', 'kind', 'questions', 'questionText', 'questionUrl',
              'url', 'sourceUrl', 'before', 'after', 'questionSnapshot')
    snapshot = {key: request.get(key) for key in fields}
    return hashlib.sha256(json.dumps(snapshot, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def safe_file(base, relative):
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or '\\' in relative:
        return None
    if any(part.startswith('.') for part in parts):
        return None
    path = base
    for part in parts:
        path /= part
        if path.is_symlink():
            return None
    return path if path.is_file() and path.resolve().is_relative_to(base.resolve()) else None


def build_status(root=ROOT):
    paths = [root/'site/dist/data.json', root/'docs/imports/todo-progress.json',
             root/'docs/imports/more-gpt-progress.json', root/'docs/imports/more-gemini-progress.json',
             root/'monitor/activity.json', root/'monitor/confirmations.json']
    data, todo, gpt, gemini, activity, requests = [read_json(p) for p in paths]
    import_control_path = root/'monitor/import-control.json'
    import_control = read_json(import_control_path) if import_control_path.exists() else {}
    if import_control:
        paths.append(import_control_path)
    acquisition = []
    for name in ('acquisition.json', 'gemini-acquisition.json', 'ai-acquisition.json'):
        p = root/'monitor'/name
        if p.exists():
            acquisition.append(read_json(p))
            paths.append(p)
    comic_path = root/'docs/comics/progress.json'
    comics = None
    if comic_path.exists():
        comic_data = read_json(comic_path)
        paths.append(comic_path)
        entries = comic_data.get('entries', [])
        counts = Counter(e['state'] for e in entries)
        settled_comics = sum(counts[k] for k in ('complete', 'existing_ai', 'not_suitable'))
        comics = {'total': len(entries), 'settled': settled_comics,
                  'generated': counts['complete'], 'existingAI': counts['existing_ai'],
                  'notSuitable': counts['not_suitable'], 'awaitingConfirmation': 0,
                  'remaining': len(entries)-settled_comics,
                  'percent': round(settled_comics/len(entries)*100, 1) if entries else 0,
                  'updatedAt': comic_data.get('updatedAt', comic_data.get('startedAt')),
                  'active': [e for e in entries if e['state'] in ('reviewing', 'generating', 'layout')],
                  'recent': sorted((e for e in entries if e['state']=='complete'),
                                   key=lambda e: (e.get('completedAt', ''), e['id']), reverse=True)[:5],
                  'subjects': [dict(row, name=next((s['name'] for s in data.get('subjects', []) if s['id']==row['subject']), row['subject'])) for row in subject_stats(entries)],
                  'next': next_entry(entries)}
        timing_path = root/'docs/comics/speed-comparison.json'
        if timing_path.exists():
            comics['speedComparison'] = read_json(timing_path)
            paths.append(timing_path)
        parallel_timing_path = root/'docs/comics/parallel-speed-comparison.json'
        if parallel_timing_path.exists():
            comics['parallelSpeedComparison'] = measure(read_json(parallel_timing_path), entries)
            paths.append(parallel_timing_path)
        parallel_path = root/'monitor/parallel.json'
        reserved = set()
        if parallel_path.exists():
            comics['parallel'] = read_json(parallel_path)
            paths.append(parallel_path)
            if import_control.get('state') == 'paused':
                for lane in comics['parallel'].get('lanes', []):
                    if lane.get('role') == 'import':
                        lane.update(state='paused', questionId=None,
                                    title='第63來源已收尾；新題整理依使用者指示暫停')
            running = [dict(id=l['questionId'], title=l['title']) for l in comics['parallel'].get('lanes', []) if l['state']=='running' and l.get('questionId')]
            running += [dict(id=j['id'], title=j['title']) for j in comics['parallel'].get('integrating', [])]
            comics['active'] = running
            reserved = {e['id'] for e in comics['parallel'].get('ready', []) + comics['parallel'].get('blocked', [])}
            reserved.update(e['id'] for e in running)
            comics['next'] = next_entry([dict(e, state='reserved') if e['id'] in reserved else e for e in entries])
        priority_path = root/'monitor/priority-source.json'
        if priority_path.exists():
            priority = read_json(priority_path)
            priority_ids = set(priority.get('questionIds', []))
            priority_entries = [e for e in entries if e['id'] in priority_ids]
            published_ids = {q['id'] for q in data['questions']} & priority_ids
            pending_ids = {r.get('questionId') for r in requests.get('requests', [])
                           if r.get('state') == 'pending' and r.get('questionId') in priority_ids}
            pending_ids.update(e['id'] for e in priority_entries if e['state']=='awaiting_confirmation')
            comics['prioritySource'] = dict(priority, total=len(priority_ids),
                published=len(published_ids), generated=sum(e['state']=='complete' for e in priority_entries),
                awaitingConfirmation=len(pending_ids))
            paths.append(priority_path)
            if priority.get('state') not in ('complete', 'cancelled'):
                comics['next'] = next_entry([dict(e, state='reserved') if e['id'] in reserved else e
                                             for e in entries if e['id'] in priority_ids])
    questions = data['questions']
    by_id = {q['id']: q for q in questions}
    for parent in questions:
        for child in parent.get('groupQuestions',[]):by_id.setdefault(child['id'],child)
    group_review = None
    group_path = root/'docs/imports/group-review/queue.json'
    if group_path.exists():
        queue = read_json(group_path)
        group_review = dict(group_summary(queue),updatedAt=queue.get('updatedAt'))
        group_review['subjects'] = [dict(subject=s['id'],name=s['name'],
            **group_review['subjects'].get(s['id'],{'groups':0,'questions':0}))
            for s in data.get('subjects',[])]
        group_review['groups'] = [dict(id=g['id'],state=g['state'],
            subject=g['subject'],questions=[{'id':qid,'title':by_id.get(qid,{}).get('title',qid),
                'url':'/site/index.html#question/'+qid} for qid in g['questionIds']])
            for g in queue.get('groups',[]) if g['state']!='superseded']
        group_review['active'] = [{'id':c['id'],'owner':c.get('owner'),
            'questionIds':c['questionIds']} for c in queue.get('candidates',[]) if c['state']=='reviewing']
        control_path=root/'monitor/group-control.json'
        control=read_json(control_path) if control_path.exists() else {}
        if control_path.exists():paths.append(control_path)
        group_review['integrationGate']=control
        groups=[g for g in queue.get('groups',[]) if g['state']!='superseded']
        eligible=sorted((g for g in groups if g['state']=='ready' and g.get('qaState')=='complete'),key=lambda g:g.get('qaCompletedAt',''))
        awaiting_layout=[g for g in groups if g['state']=='ready' and g.get('qaState')!='complete']
        lanes=[]
        for lane in (1,2,3):
            agent='/root/comic_lane_'+str(lane)
            job=next((g for g in groups if g.get('integrator' if lane==1 else 'owner')==agent
                and g['state']==('integrating' if lane==1 else 'merging')),None)
            review=next((c for c in queue['candidates'] if c.get('owner')==agent and c['state']=='reviewing'),None)
            qa=next((g for g in groups if g.get('qaOwner')==agent and g.get('qaState')=='running'),None)
            if not job and qa:job=qa
            upcoming=eligible[0] if lane==1 and eligible else next((g for g in awaiting_layout if g.get('owner')==agent),None) if lane!=1 else None
            ids=job['questionIds'] if job else review['questionIds'] if review else upcoming['questionIds'] if upcoming else []
            state=('qa_checking' if qa and job is qa else 'integrating' if lane==1 else 'merging') if job else 'reviewing' if review else (
                'preparing' if lane==1 and control.get('state')=='preparing_compatibility' else
                'ready' if lane==1 and eligible else
                'waiting_qa' if lane==1 and awaiting_layout else
                'qa_preparing' if lane!=1 and upcoming else
                'preparing' if lane!=1 and any(g['state']=='confirmed' for g in groups) else 'idle')
            lanes.append({'lane':lane,'state':state,'questionIds':ids,
                'next':bool(upcoming and not job and not review),
                'titles':[by_id.get(qid,{}).get('title',qid) for qid in ids],
                'detail':control.get('detail','') if lane==1 and state=='preparing' else
                    '等待合稿線完成'+str(len(awaiting_layout))+'組版面驗收；通過後直接加入。' if state=='waiting_qa' else
                    '本路已完成交稿與版面驗收。' if lane!=1 and state=='idle' else
                    '所有通過驗收的稿件均已加入。' if lane==1 and state=='idle' else '',
                'qaCompleted':sum(g.get('qaState')=='complete' and g.get('qaOwner')==agent for g in groups),
                'completed':sum(g['state']=='integrated' and g.get('integrator')==agent for g in groups) if lane==1
                    else sum(g['state'] in {'ready','integrating','integrated'} and g.get('owner')==agent for g in groups)})
        group_review['lanes']=lanes
        group_review['waiting']=[{'id':g['id'],'retainId':g['retainId'],
            'readyAt':g.get('qaCompletedAt'),'handedOffAt':g.get('readyAt')} for g in eligible]
        group_review['awaitingLayout']=len(awaiting_layout)
        group_review['readyForIntegration']=len(eligible)
        group_review['layoutChecked']=sum(g.get('qaState')=='complete' for g in groups)
        paths.append(group_path)
    batches = []
    for key, title, payload in [('todo', '原 TODO', todo), ('gpt', 'more_gpt', gpt), ('gemini', 'more_gemini', gemini)]:
        rows = []
        for source in payload['sources']:
            state = source['state']
            qids = source.get('questionIds', source.get('completeQuestionIds', []))
            rows.append({
                'order': source['order'], 'title': source.get('title') or '尚未讀取標題',
                'url': source['url'], 'state': state, 'stateLabel': STATE_NAMES.get(state, state),
                'settled': state in TERMINAL,
                'questions': [{'id': qid, 'title': by_id[qid]['title'], 'url': '/site/index.html#question/'+qid}
                              for qid in qids if qid in by_id],
                'imagesAvailable': len(source.get('downloadedImages', [])),
                'imagesExpected': source.get('archiveImages'),
                'reason': source.get('reason', ''),
                'skippedQuestions': source.get('skippedQuestions', []),
            })
        states = Counter(s['state'] for s in rows)
        settled = sum(s['settled'] for s in rows)
        complete = states['complete'] + states['complete_with_skips']
        batches.append({'id': key, 'title': title, 'total': len(rows), 'settled': settled,
                        'complete': complete, 'excluded': settled-complete,
                        'partial': states['partial'], 'pending': len(rows)-settled,
                        'percent': round(settled/len(rows)*100, 1) if rows else 100,
                        'sources': rows})
    total = sum(b['total'] for b in batches if b['id'] != 'todo')
    settled = sum(b['settled'] for b in batches if b['id'] != 'todo')
    confirmations = []
    source_urls = {s['id']: s['url'] for s in data.get('sources', [])}
    for q in questions:
        if q.get('verification') in ('待核對', '待補原題') or q.get('contentStatus') == '待更新':
            question_snapshot = {key: value for key, value in q.items()
                                 if key not in ('reviewLabel', 'reviewPreviousId', 'reviewNextId')}
            confirmations.append({'id': q['id'], 'title': q['title'], 'kind': '題目核對',
                                  'questions': q.get('reviewQuestions') or [q.get('verificationNote') or '請核對原題內容。'],
                                  'url': '/site/index.html#question/'+q['id'],
                                  'questionUrl': '/site/index.html#question/'+q['id'],
                                  'questionText': '\n\n'.join(part for part in [q.get('passage', ''), q.get('question', '')] if part),
                                  'questionSnapshot': hashlib.sha256(json.dumps(question_snapshot, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
                                  'sourceUrl': source_urls.get(q.get('sourceId'))})
    for request in requests.get('requests', []):
        if request.get('state') == 'pending':
            confirmations.append(request)
    pending_feedback = {}
    for item in requests.get('feedback', []):
        if item.get('state') == 'pending':
            pending_feedback.setdefault(item['id'], []).append(item)
    # A comment submitted from another still-open tab also remains actionable
    # after an earlier approval; retain the exact version that prompted it.
    for request_id, items in pending_feedback.items():
        if not any(c['id'] == request_id for c in confirmations):
            confirmations.append(items[-1]['requestSnapshot'])
    acknowledged = {(r['id'], r.get('confirmationToken')) for r in requests.get('resolved', [])}
    confirmations = [dict(c, confirmationToken=confirmation_token(c)) for c in confirmations
                     if c['id'] in pending_feedback or (c['id'], confirmation_token(c)) not in acknowledged]
    for card in confirmations:
        comments = [dict(text=f['text'], submittedAt=f['submittedAt'], state=f['state'],
                         basedOnPreviousVersion=f['confirmationToken'] != card['confirmationToken'])
                    for f in requests.get('feedback', []) if f['id'] == card['id']]
        if comments:
            card.update(userComments=comments, feedbackPending=card['id'] in pending_feedback)
    if comics:
        waiting_ids = {e['id'] for e in entries if e['state']=='awaiting_confirmation'}
        pipeline_path = root/'docs/comics/pipeline.json'
        if pipeline_path.exists():
            paths.append(pipeline_path)
            published_comic_ids = {e['id'] for e in entries}
            waiting_ids.update(j['id'] for j in read_json(pipeline_path).get('jobs', [])
                               if j.get('state')=='blocked' and j.get('decision')=='awaiting_confirmation'
                               and j.get('id') in published_comic_ids)
        review_ids = {c.get('questionId') or c['id'] for c in confirmations}
        waiting_ids.update(c.get('questionId') or c['id'] for c in confirmations
                           if c.get('kind')=='漫畫排版確認')
        # Count questions once, and stop asking after OK even while integration is pending.
        comics['awaitingConfirmation'] = len(waiting_ids & review_ids)
    new_sources = current_sources(root, gemini['sources'], questions,
                                  comic_data.get('entries', []) if comics else [], confirmations, paths,
                                  source_catalog={'gpt': gpt['sources'], 'gemini': gemini['sources']})
    if new_sources:
        acquired_rows = {(row['batch'], row['order']): row for row in new_sources['sources']}
        for batch in batches:
            for row in batch['sources']:
                acquired = acquired_rows.get((batch['id'], row['order']))
                if acquired is not None:
                    for key in ('title', 'state', 'reason', 'imagesAvailable', 'imagesExpected'):
                        row[key] = acquired[key]
                    row['questions'] = [{'id': qid, 'title': by_id[qid]['title'],
                                         'url': '/site/index.html#question/'+qid}
                                        for qid in acquired['questionIds']]
                    row['stateLabel'] = STATE_NAMES.get(row['state'], row['state'])
    missing = [dict(batch=b['title'], **s) for b in batches for s in b['sources']
               if not s['settled'] and (s['skippedQuestions'] or s['state'] == 'awaiting_image_retry'
                   or s['imagesExpected'] and s['imagesAvailable'] < s['imagesExpected'])]
    return {
        'project': 'WeiRuGo', 'title': '錯題整理進度', 'generatedAt': iso_time(datetime.now().timestamp()),
        'dataUpdatedAt': iso_time(max(p.stat().st_mtime for p in paths)),
        'revision': data['revision'], 'activity': activity, 'acquisition': acquisition, 'comics': comics,
        'summary': {'questions': len(questions),
                    'verifiedQuestions': sum(q.get('verification') not in ('待核對', '待補原題') and q.get('contentStatus') != '待更新' for q in questions),
                    'confirmations': len(confirmations), 'newSourcesTotal': total,
                    'newSourcesSettled': settled, 'newSourcesPending': total-settled,
                    'percent': round(settled/total*100, 1) if total else 100},
        'batches': batches, 'confirmations': confirmations, 'imageRetries': missing,
        'newSources': new_sources, 'importControl': import_control, 'groupReview': group_review,
        'resolvedConfirmations': requests.get('resolved', []),
    }


class ConfirmationConflict(ValueError):
    pass


def resolve_confirmation(request_id, token, root=ROOT, resolution='使用者在 monitor 點選「確認 OK」，確認目前內容沒有問題。'):
    with edit_confirmations(root) as records:
        current = next((r for r in build_status(root)['confirmations'] if r['id'] == request_id), None)
        if current is None:
            previous = next((r for r in records.get('resolved', [])
                             if r['id'] == request_id and r.get('confirmationToken') == token), None)
            if previous:
                return previous  # Double-clicks and retries do not duplicate records.
            raise KeyError(request_id)
        if current['confirmationToken'] != token:
            raise ConfirmationConflict('內容已更新，請重新查看後再確認。')
        result = dict(current, state='resolved', resolution=resolution,
                      resolvedAt=datetime.now(timezone.utc).isoformat())
        for item in records.get('feedback', []):
            if item['id'] == request_id and item.get('state') == 'pending':
                item.update(state='addressed', addressedAt=result['resolvedAt'], resolution=resolution)
        if result.get('userComments'):
            result['userComments'] = [dict(c, state='addressed') for c in result['userComments']]
        records['requests'] = [r for r in records.get('requests', []) if r['id'] != request_id]
        records.setdefault('resolved', []).append(result)
        return result


def submit_confirmation_comment(request_id, token, comment, root=ROOT):
    if not isinstance(comment, str) or not comment.strip() or len(comment) > 2000:
        raise ValueError('意見請填寫1至2000字。')
    comment = comment.strip()
    with edit_confirmations(root) as records:
        current = next((r for r in build_status(root)['confirmations'] if r['id'] == request_id), None)
        if current is None:
            current = next((r for r in reversed(records.get('resolved', []))
                            if r['id'] == request_id and r.get('confirmationToken') == token), None)
        if current is None:
            raise KeyError(request_id)
        if confirmation_token(current) != token:
            raise ConfirmationConflict('內容已更新，請重新查看後再送出意見。')
        previous = next((f for f in records.get('feedback', [])
                         if f['id'] == request_id and f['confirmationToken'] == token
                         and f['text'] == comment and f.get('state') == 'pending'), None)
        if previous:
            return previous
        result = dict(id=request_id, confirmationToken=token, text=comment, state='pending',
                      submittedAt=datetime.now(timezone.utc).isoformat(),
                      requestSnapshot={k:v for k,v in current.items()
                                       if k not in ('userComments','feedbackPending')})
        records.setdefault('feedback', []).append(result)
        return result


class Handler(BaseHTTPRequestHandler):
    def respond(self, body, content_type, status=200, head=False):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def do_GET(self, head=False):
        route = unquote(urlsplit(self.path).path)
        if route == '/health':
            return self.respond(b'{"ok":true,"project":"WeiRuGo"}', 'application/json', head=head)
        if route == '/api/status':
            try:
                body = json.dumps(build_status(), ensure_ascii=False).encode()
                return self.respond(body, 'application/json; charset=utf-8', head=head)
            except (OSError, ValueError, KeyError, TypeError):
                return self.respond(b'{"error":"Progress records are temporarily unavailable"}', 'application/json', 503, head)
        if route in ('/', '/index.html'):
            path = ROOT/'monitor/index.html'
        elif route == '/favicon.svg':
            path = ROOT/'monitor/favicon.svg'
        elif route.startswith('/site/'):
            path = safe_file(ROOT/'site/dist', route[len('/site/'):] or 'index.html')
            if path and path.suffix.lower() not in {'.html', '.css', '.js', '.json', '.svg', '.jpg', '.jpeg', '.png', '.webp', '.txt'}:
                path = None
        else:
            path = None
        if path is None:
            return self.respond(b'Not found', 'text/plain', 404, head)
        try:
            body = path.read_bytes()
        except OSError:
            return self.respond(b'Not found', 'text/plain', 404, head)
        content_type = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        if content_type.startswith('text/') or content_type in ('application/json', 'application/javascript'):
            content_type += '; charset=utf-8'
        return self.respond(body, content_type, head=head)

    def do_HEAD(self):
        self.do_GET(head=True)

    def do_POST(self):
        if urlsplit(self.path).path != '/api/confirm':
            return self.respond(b'Method not allowed', 'text/plain', 405)
        origin = self.headers.get('Origin')
        if origin and (urlsplit(origin).scheme not in ('http', 'https') or
                       urlsplit(origin).hostname not in ('localhost', '127.0.0.1', 'monitor.sibuzu.com')):
            return self.respond(b'Forbidden origin', 'text/plain', 403)
        if self.headers.get('X-TestReview-Action') != 'confirm':
            return self.respond(b'Explicit confirmation required', 'text/plain', 403)
        if self.headers.get('Content-Type', '').split(';')[0].strip() != 'application/json':
            return self.respond(b'JSON required', 'text/plain', 415)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 16384:
                raise ValueError('Invalid body length')
            payload = json.loads(self.rfile.read(length))
            if (not isinstance(payload, dict) or not {'id', 'confirmationToken'} <= set(payload)
                    or set(payload) - {'id', 'confirmationToken', 'comment'}
                    or not all(isinstance(payload[k], str) and payload[k] for k in ('id', 'confirmationToken'))
                    or not isinstance(payload.get('comment', ''), str)
                    or len(payload.get('comment', '')) > 2000):
                raise ValueError('Invalid confirmation')
            if payload.get('comment', '').strip():
                result = submit_confirmation_comment(payload['id'], payload['confirmationToken'], payload['comment'], root=ROOT)
                response = {'ok': True, 'id': result['id'], 'state': 'feedback_pending'}
            else:
                result = resolve_confirmation(payload['id'], payload['confirmationToken'], root=ROOT)
                response = {'ok': True, 'id': result['id']}
            return self.respond(json.dumps(response).encode(), 'application/json')
        except ConfirmationConflict as error:
            return self.respond(json.dumps({'error': str(error)}, ensure_ascii=False).encode(), 'application/json', 409)
        except KeyError:
            return self.respond(b'{"error":"Confirmation not found"}', 'application/json', 404)
        except (ValueError, TypeError):
            return self.respond(b'{"error":"Invalid confirmation request"}', 'application/json', 400)
        except OSError:
            return self.respond(b'{"error":"Could not save confirmation; please retry"}', 'application/json', 503)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
