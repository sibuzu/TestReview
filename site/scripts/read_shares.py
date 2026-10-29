"""Read public ChatGPT share streams into an auditable local archive.

Usage: python3 site/scripts/read_shares.py
The archive is evidence for curation, not an automatically verified answer key.
"""
import concurrent.futures
import datetime
import json
import pathlib
import re
import urllib.request

BASE = pathlib.Path(__file__).resolve().parents[1]
ROOT = BASE if (BASE / 'todo/todo.md').exists() else BASE.parent
OUT = ROOT / 'docs' / 'sources'


def decode_stream(html):
    for match in re.finditer(r'streamController.enqueue\(("(?:[^"\\]|\\.)*")\)', html):
        raw = json.loads(match.group(1))
        if not raw.startswith('['):
            continue
        values = json.loads(raw)
        memo = {}

        def read(index):
            if index < 0:
                return None
            if index in memo:
                return memo[index]
            value = values[index]
            if isinstance(value, dict):
                result = {}
                memo[index] = result
                for key, ref in value.items():
                    result[str(read(int(key[1:])))] = read(ref)
                return result
            if isinstance(value, list):
                result = []
                memo[index] = result
                result.extend(read(v) if isinstance(v, int) else v for v in value)
                return result
            return value

        data = read(0)
        route = data.get('loaderData', {}).get('routes/share.$shareId.($action)')
        if route:
            return route.get('serverResponse', {}).get('data') or route.get('data')
        # The route name can change; look for the conversation object.
        for item in memo.values():
            if isinstance(item, dict) and 'linear_conversation' in item:
                return item
    raise ValueError('No readable conversation stream')


def fetch(url):
    share_id = url.rsplit('/', 1)[-1]
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode()
        data = decode_stream(html)
        if not data:
            raise ValueError('Conversation is unavailable')
        messages = [n['message'] for n in data.get('linear_conversation', []) if n.get('message')]
        record = {'url': url, 'title': data.get('title'), 'messages': messages}
        (OUT / f'{share_id}.json').write_text(json.dumps(record, ensure_ascii=False, indent=2))
        return {'url': url, 'status': 'read', 'title': data.get('title'), 'messages': len(messages)}
    except Exception as error:
        return {'url': url, 'status': 'unreadable', 'reason': str(error)}


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    urls = re.findall(r'https://chatgpt.com/share/[^\s]+', (ROOT / 'todo/todo.md').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch, urls))
    (OUT / 'chatgpt-fetch.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(json.dumps(results, ensure_ascii=False, indent=2))
