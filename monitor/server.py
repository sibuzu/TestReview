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
except ImportError:  # Also support running python monitor/server.py.
    from confirmation_store import edit_confirmations
    from comic_queue import subject_stats, next_entry
    from parallel_timing import measure

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
                  'notSuitable': counts['not_suitable'], 'awaitingConfirmation': counts['awaiting_confirmation'] + sum(r.get('state')=='pending' and r.get('kind')=='漫畫排版確認' for r in requests.get('requests', [])),
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
    acknowledged = {(r['id'], r.get('confirmationToken')) for r in requests.get('resolved', [])}
    confirmations = [dict(c, confirmationToken=confirmation_token(c)) for c in confirmations
                     if (c['id'], confirmation_token(c)) not in acknowledged]
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
        records['requests'] = [r for r in records.get('requests', []) if r['id'] != request_id]
        records.setdefault('resolved', []).append(result)
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
            if not 0 < length <= 8192:
                raise ValueError('Invalid body length')
            payload = json.loads(self.rfile.read(length))
            if (not isinstance(payload, dict) or set(payload) != {'id', 'confirmationToken'} or
                    not all(isinstance(v, str) and v for v in payload.values())):
                raise ValueError('Invalid confirmation')
            result = resolve_confirmation(payload['id'], payload['confirmationToken'], root=ROOT)
            return self.respond(json.dumps({'ok': True, 'id': result['id']}).encode(), 'application/json')
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
