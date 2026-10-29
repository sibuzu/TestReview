"""Acquire share evidence separately from question curation, using the live bridge.

plan writes JSONL commands for the already-authorized browser bridge; watch imports
finished bundles into isolated acquisition records; merge updates the curation queue.
Downloaded evidence never marks questions or sources as curated.
"""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time

from read_shares import decode_stream

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT/'.cache/share-prefetch'
RESULTS = ROOT/'docs/acquisition'
PROGRESS = ROOT/'docs/imports/more-gpt-progress.json'
STATUS = ROOT/'monitor/acquisition.json'


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(path)


def read(path):
    return json.loads(path.read_text())


READY = """(async()=>{const end=Date.now()+20000;while(Date.now()<end){if(location.href===URL_VALUE&&!window.__trLeaving&&document.title!=='New chat'&&(document.querySelector('.thread-scroll-container')?.innerText.length||0)>100&&[...document.images].some(i=>i.alt==='User attachment'&&(i.currentSrc||i.src))){await new Promise(r=>setTimeout(r,800));return {ready:true};}await new Promise(r=>setTimeout(r,200));}return {ready:false,title:document.title,url:location.href};})()"""
SWEEP = "(()=>{const job=window.__trPrefetch={status:'running',images:[]};(async()=>{const el=document.querySelector('.thread-scroll-container');if(!el)throw Error('Transcript not ready');const start=el.scrollTop,seen=new Set();const collect=()=>{for(const im of document.images){const src=im.currentSrc||im.src;if(im.alt==='User attachment'&&src&&!seen.has(src)){seen.add(src);job.images.push({src,width:im.naturalWidth,height:im.naturalHeight});}}};const deadline=Date.now()+33000;try{collect();for(let y=0;y<el.scrollHeight;y+=650){if(Date.now()>deadline)throw Error('Scroll sweep timed out; retry required');el.scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,100));collect();}}finally{el.scrollTo({top:start,behavior:'instant'});}job.status='complete';})().catch(e=>{job.status='failed';job.error=e.message;});return {started:true};})()"
WAIT = """(async()=>{const end=Date.now()+35000;while(Date.now()<end){const j=window.__trPrefetch;if(j&&j.status!=='running')return {status:j.status,images:j.images.length,error:j.error};await new Promise(r=>setTimeout(r,150));}return {status:'timeout'};})()"""
EXPORT = "(async()=>{\n const j=window.__trPrefetch;if(j?.status!=='complete')throw Error('Image sweep incomplete');if(location.href!==URL_VALUE)throw Error('Wrong share URL');\n const encode=blob=>new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result.split(',')[1]);r.onerror=reject;r.readAsDataURL(blob);});\n const shareId=new URL(location.href).pathname.split('/').pop();let authHeaders={};\n const archivePromise=(async()=>{try{const session=await(await fetch('/api/auth/session',{credentials:'include',signal:AbortSignal.timeout(5000)})).json();if(session.accessToken)authHeaders={Authorization:'Bearer '+session.accessToken};const r=await fetch('/backend-api/share/'+shareId,{credentials:'include',headers:authHeaders,signal:AbortSignal.timeout(12000)});if(!r.ok)throw Error('Share API HTTP '+r.status);const payload=await r.json();if(!Array.isArray(payload.linear_conversation))throw Error('No linear conversation');return {archive:{url:location.href,title:payload.title,messages:payload.linear_conversation.map(n=>n.message).filter(Boolean)}};}catch(e){return {error:e.message}}})();\n const visibleImages=Promise.all(j.images.map(async(im,index)=>{try{const r=await fetch(im.src,{credentials:'omit',signal:AbortSignal.timeout(15000)});if(!r.ok)throw Error('HTTP '+r.status);const b=await r.blob();return {index,width:im.width,height:im.height,mime:b.type,base64:await encode(b)};}catch(e){return {index,error:e.message}}}));\n const [result,images]=await Promise.all([archivePromise,visibleImages]);const archive=result.archive;\n if(archive){const pointers=new Map();for(const message of archive.messages){if(message.author?.role!=='user')continue;for(const p of message.content?.parts||[]){if(p?.content_type!=='image_asset_pointer')continue;const match=p.asset_pointer?.match(/^sediment:\\/\\/(file_[a-zA-Z0-9]+)(?:\\?.*)?$/);if(match)pointers.set(match[1],p);}}\n const missing=[...pointers].filter(([id])=>!j.images.some(im=>im.src.replaceAll('-','').includes(id.replace(/^file_/,''))));const offset=images.length;\n images.push(...await Promise.all(missing.map(async([id,p],i)=>{const index=offset+i;try{const r=await fetch('/backend-api/share/'+shareId+'/file/'+encodeURIComponent(id),{credentials:'include',headers:authHeaders,signal:AbortSignal.timeout(15000)});if(!r.ok)throw Error('Share file HTTP '+r.status);const meta=await r.json(),url=meta.download_url||meta.url;if(!url)throw Error('No download URL');const image=await fetch(url,{credentials:'omit',signal:AbortSignal.timeout(15000)});if(!image.ok)throw Error('Image HTTP '+image.status);const blob=await image.blob();return {index,fileId:id,width:p.width,height:p.height,mime:blob.type,base64:await encode(blob),origin:'archived_user_pointer'};}catch(e){return {index,fileId:id,error:e.message,origin:'archived_user_pointer'}}})));\n }\n const renderedText=j.text||document.querySelector('.thread-scroll-container').innerText;\n const fullText=archive?archive.messages.filter(m=>['user','assistant'].includes(m.author?.role)&&m.content?.parts?.length).map(m=>m.author.role+'\\n'+m.content.parts.map(p=>typeof p==='string'?p:'[原卷附圖]').join('\\n')).join('\\n\\n'):renderedText;\n const record={url:location.href,title:document.title,checkedAt:new Date().toISOString(),html:archive?'':document.documentElement.outerHTML,text:fullText,textMethod:archive?'share_api_full_transcript':'scroll_rendered',renderedWindowTextLength:renderedText.length,archive,archiveError:result.error,turns:j.turns||[],dates:j.dates?.length?j.dates:[...document.querySelectorAll('time')].map(t=>({text:t.innerText,dateTime:t.dateTime})),images};\n return {base64:await encode(new Blob([JSON.stringify(record)],{type:'application/json'})),mime:'application/json',width:images.length,height:images.filter(i=>i.base64).length};\n})()"


def plan(target, orders):
    sources = read(PROGRESS)['sources']
    CACHE.mkdir(parents=True, exist_ok=True)
    commands, queue = [], []
    for order in orders:
        source = sources[order-1]
        assert source['order'] == order
        url = source['url']
        assert re.fullmatch(r'https://chatgpt.com/share/[a-f0-9-]+', url)
        bundle = CACHE/f'gpt-{order:03}.json'
        # A plan never overwrites an existing acquisition; explicit new plan starts fresh.
        bundle.unlink(missing_ok=True)
        (RESULTS/f'gpt-{order:03}.json').unlink(missing_ok=True)
        queue.append({'order': order, 'url': url, 'title': source.get('title', ''),
                      'bundle': str(bundle.relative_to(ROOT)), 'state': 'queued'})
        def evaluate(expression):
            commands.append({'action': 'evaluate', 'targetId': target,
                             'expression': expression.replace('URL_VALUE', json.dumps(url))})
        evaluate('window.__trLeaving=true;location.href=URL_VALUE; "navigating"')
        # Navigation can destroy the first evaluation context; the second is a retry.
        evaluate(READY)
        evaluate(READY)
        evaluate(SWEEP)
        evaluate(WAIT)
        commands.append({'action': 'save', 'targetId': target,
                         'expression': EXPORT.replace('URL_VALUE', json.dumps(url)),
                         'path': str(bundle)})
    (CACHE/'commands.jsonl').write_text('\n'.join(json.dumps(c) for c in commands)+'\n')
    write(CACHE/'plan.json', {'createdAt': now(), 'sources': queue})
    write(STATUS, {'state': 'queued', 'title': '背景取回GPT對話與原圖',
                   'updatedAt': now(), 'sources': queue})
    print(json.dumps({'commands': len(commands), 'sources': orders,
                      'commandFile': str(CACHE/'commands.jsonl')}))


def import_bundle(item):
    bundle = read(ROOT/item['bundle'])
    if bundle['url'] != item['url']:
        raise ValueError('Bundle does not match the requested source')
    source = read(PROGRESS)['sources'][item['order']-1]
    key = item['url'].rsplit('/', 1)[-1]
    archive_path = ROOT/'docs/sources'/f'{key}.json'
    archive = read(archive_path) if archive_path.exists() else None
    supplied_archive = bundle.get('archive')
    if supplied_archive and supplied_archive.get('messages'):
        if supplied_archive.get('url') != item['url']:
            raise ValueError('Full conversation archive URL does not match source')
        archive = supplied_archive
        write(archive_path, archive)
    try:
        decoded = None if supplied_archive else decode_stream(bundle.get('html', ''))
        if decoded and decoded.get('linear_conversation'):
            archive = {'url': item['url'], 'title': decoded.get('title'),
                       'messages': [n['message'] for n in decoded.get('linear_conversation', []) if n.get('message')]}
            write(archive_path, archive)
    except (ValueError, KeyError, TypeError, RecursionError):
        pass
    rendered = {'url': bundle['url'], 'title': bundle['title'],
                'text': bundle['text'], 'turns': bundle.get('turns', []), 'dates': bundle.get('dates', []),
                'checkedAt': bundle['checkedAt'], 'method': bundle.get('textMethod', 'legacy_rendered')}
    write(ROOT/'docs/sources'/f'{key}-rendered.json', rendered)
    attachments = [p for m in (archive or {}).get('messages', []) if m['author']['role'] == 'user'
                   for p in m['content'].get('parts', [])
                   if isinstance(p, dict) and p.get('content_type') == 'image_asset_pointer']
    expected = len(attachments)
    known = {im['sha256']: im for im in source.get('downloadedImages', [])}
    originals = ROOT/'docs/source-pages'
    numbered = [p for p in originals.glob(f'chatgpt-{key[:8]}-*') if re.search(r'-\d+\.(jpg|png|webp)$', p.name)]
    counter = max([int(re.search(r'-(\d+)\.', p.name).group(1)) for p in numbered] or [0])
    # Also recognize files fetched by another worker, without renumbering them.
    for p in numbered:
        raw = p.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        known.setdefault(digest, {'path': str(p.relative_to(ROOT)), 'sha256': digest, 'bytes': len(raw)})
    downloaded, errors = [], []
    for image in bundle['images']:
        if not image.get('base64'):
            errors.append({'index': image['index'], 'error': image.get('error', 'No image data')})
            continue
        raw = base64.b64decode(image['base64'], validate=True)
        digest = hashlib.sha256(raw).hexdigest()
        if digest not in known:
            ext = '.jpg' if raw.startswith(b'\xff\xd8') else '.png' if raw.startswith(b'\x89PNG') else '.webp' if raw.startswith(b'RIFF') else None
            if not ext:
                errors.append({'index': image['index'], 'error': 'Response is not an image'})
                continue
            counter += 1
            path = originals/f'chatgpt-{key[:8]}-{counter}{ext}'
            path.write_bytes(raw)
            known[digest] = {'path': str(path.relative_to(ROOT)), 'sha256': digest,
                             'bytes': len(raw), 'renderedWidth': image['width'], 'renderedHeight': image['height']}
        if digest not in {i['sha256'] for i in downloaded}:
            for dimension in ('Width', 'Height'):
                if not known[digest].get('rendered'+dimension) and image.get(dimension.lower()):
                    known[digest]['rendered'+dimension] = image[dimension.lower()]
            if image.get('fileId'):
                known[digest]['fileId'] = image['fileId']
            downloaded.append(known[digest])
    sizes = {i['bytes'] for i in downloaded}
    matched = sum(p.get('size_bytes') in sizes for p in attachments)
    coverage = matched == expected if expected else bool(downloaded)
    text_complete = bool((archive or {}).get('messages'))
    result = {'batch': 'gpt', 'order': item['order'], 'url': item['url'],
              'title': (archive or {}).get('title') or bundle['title'],
              'state': 'acquired' if not errors and coverage and text_complete and len(bundle['text']) > 100 else 'partial',
              'checkedAt': bundle['checkedAt'], 'imagesExpected': expected,
              'renderedImages': len(bundle['images']), 'matchedArchiveAttachments': matched, 'downloadedImages': downloaded,
              'archive': str(archive_path.relative_to(ROOT)) if archive_path.exists() else None,
              'renderedArchive': f'docs/sources/{key}-rendered.json',
              'textLength': len(bundle['text']), 'textComplete': text_complete,
              'archiveMessages': len((archive or {}).get('messages', [])), 'errors': errors,
              'method': 'authorized_share_api_and_original_files' if supplied_archive else 'authorized_chrome_scroll_all_attachments'}
    write(RESULTS/f'gpt-{item["order"]:03}.json', result)
    return result


def watch(timeout):
    queue = read(CACHE/'plan.json')['sources']
    deadline = time.monotonic()+timeout
    while True:
        for item in queue:
            path = ROOT/item['bundle']
            if item['state'] != 'queued' or not path.exists():
                continue
            try:
                result = import_bundle(item)
                item.update(state=result['state'], title=result['title'],
                            imagesAvailable=len(result['downloadedImages']),
                            imagesExpected=result['imagesExpected'], textLength=result['textLength'])
                print(json.dumps({k: v for k, v in item.items() if k != 'bundle'}, ensure_ascii=False), flush=True)
            except (OSError, ValueError, KeyError) as error:
                # A SAVE may still be writing: retry before calling the result a failure.
                item['lastReadError'] = str(error)
        pending = [i for i in queue if i['state'] == 'queued']
        expired = time.monotonic() >= deadline
        write(STATUS, {'state': 'timeout' if expired and pending else 'running' if pending else 'complete',
                       'title': '背景取回GPT對話與原圖', 'updatedAt': now(),
                       'completed': len(queue)-len(pending), 'total': len(queue), 'sources': queue})
        if not pending or expired:
            break
        time.sleep(3)


def merge():
    progress = read(PROGRESS)
    changed = []
    for path in sorted(RESULTS.glob('gpt-*.json')):
        result = read(path)
        source = progress['sources'][result['order']-1]
        assert source['url'] == result['url']
        known = {i['sha256'] for i in source.get('downloadedImages', [])}
        for image in result['downloadedImages']:
            if image['sha256'] not in known:
                source['downloadedImages'].append(image)
                known.add(image['sha256'])
        source['archiveImages'] = result['imagesExpected'] or source['archiveImages']
        source['title'] = result['title']
        source['acquisitionEvidence'] = {k: v for k, v in result.items() if k != 'downloadedImages'}
        if source['state'] not in ('complete', 'complete_with_skips', 'duplicate', 'excluded_no_question'):
            source['state'] = 'partial' if source.get('questionIds') else 'awaiting_transcription'
        changed.append(source['order'])
    write(PROGRESS, progress)
    print(json.dumps({'mergedSources': changed, 'note': 'Acquisition is separate from curation; no source marked complete.'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('plan')
    create.add_argument('--target', required=True)
    create.add_argument('orders', nargs='+', type=int)
    worker = commands.add_parser('watch')
    worker.add_argument('--timeout', type=int, default=3600)
    commands.add_parser('merge')
    args = parser.parse_args()
    if args.command == 'plan':
        plan(args.target, args.orders)
    elif args.command == 'watch':
        watch(args.timeout)
    else:
        merge()
