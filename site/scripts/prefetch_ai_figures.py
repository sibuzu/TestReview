"""Save generated explanation images separately from original question evidence."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import time
from prefetch_gpt import ROOT, READY, SWEEP, WAIT, write, read, now

CACHE=ROOT/'.cache/ai-figure-prefetch'
RESULTS=ROOT/'docs/acquisition'
STATUS=ROOT/'monitor/ai-acquisition.json'

def archived_generated_images(url):
    """Tool-produced images may be archived even when the share UI omits them."""
    archive=ROOT/'docs/sources'/f'{url.rsplit("/",1)[-1]}.json'
    if not archive.exists():return []
    found=[];seen=set()
    for message in read(archive).get('messages',[]):
        if message.get('author',{}).get('role') not in ('assistant','tool'):continue
        for part in message.get('content',{}).get('parts',[]):
            if not isinstance(part,dict) or part.get('content_type')!='image_asset_pointer':continue
            match=re.fullmatch(r'sediment://(file_[a-zA-Z0-9]+)(?:\?.*)?',part.get('asset_pointer',''))
            if not match or match[1] in seen:continue
            seen.add(match[1]);found.append({'fileId':match[1],'width':part.get('width',0),'height':part.get('height',0),'alt':message.get('metadata',{}).get('image_gen_title') or '來源AI生成圖'})
    return found

def plan(target,orders):
    CACHE.mkdir(parents=True,exist_ok=True)
    sources=read(ROOT/'docs/imports/more-gpt-progress.json')['sources'];queue=[];commands=[]
    # Some share pages omit generated tool images entirely. Readiness checks
    # the transcript; the sweep and archived-pointer fallback check images.
    ready=READY.replace("&&[...document.images].some(i=>i.alt==='User attachment'&&(i.currentSrc||i.src))","")
    sweep=SWEEP.replace("im.alt==='User attachment'","/^Generated image/i.test(im.alt)").replace("{src,width:im.naturalWidth,height:im.naturalHeight}","{src,alt:im.alt,width:im.naturalWidth,height:im.naturalHeight}").replace('__trPrefetch','__trAIFetch')
    wait=WAIT.replace('__trPrefetch','__trAIFetch')
    export="""(async()=>{const j=window.__trAIFetch;if(j?.status!=='complete'&&!(j?.status==='failed'&&window.__trAIAssets?.length))throw Error('Sweep incomplete');if(location.href!==URL_VALUE)throw Error('Wrong source URL');const encode=b=>new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result.split(',')[1]);r.onerror=reject;r.readAsDataURL(b);});const record={url:location.href,title:document.title,kind:'ai_explanation',domSweepStatus:j.status,acquisitionMethod:'captured DOM images plus all archived generated pointers',checkedAt:new Date().toISOString(),images:await Promise.all(j.images.map(async(im,index)=>{try{const r=await fetch(im.src,{credentials:'omit',signal:AbortSignal.timeout(15000)});if(!r.ok)throw Error('HTTP '+r.status);return {index,alt:im.alt,width:im.width,height:im.height,base64:await encode(await r.blob())};}catch(e){return {index,error:e.message};}}))};return {base64:await encode(new Blob([JSON.stringify(record)],{type:'application/json'})),mime:'application/json',width:record.images.length,height:record.images.filter(i=>i.base64).length};})()"""
    for order in orders:
        s=sources[order-1];url=s['url'];bundle=CACHE/f'gpt-ai-{order:03}.json';bundle.unlink(missing_ok=True)
        pointers=archived_generated_images(url)
        queue.append({'order':order,'url':url,'title':s['title'],'state':'queued','bundle':str(bundle.relative_to(ROOT)),'archiveGeneratedImages':len(pointers)})
        def evaluate(expression):commands.append({'action':'evaluate','targetId':target,'expression':expression.replace('URL_VALUE',json.dumps(url))})
        evaluate('window.__trLeaving=true;location.href=URL_VALUE; "opening AI explanation images"')
        evaluate(ready);evaluate(ready)
        # The authorized bridge may run in a PTY with a 4096-byte input line
        # limit. Keep pointer inventories out of the already-long save command.
        evaluate('window.__trAIAssets=[]; true')
        for offset in range(0,len(pointers),5):
            evaluate('window.__trAIAssets.push(...'+json.dumps(pointers[offset:offset+5])+'); true')
        evaluate(sweep);evaluate(wait)
        # Match the actual share client's read-only download route. Keep session
        # credentials and temporary signed URLs inside the authorized browser.
        fallback="""let authHeaders;for(const asset of ARCHIVED_ASSETS){const compact=asset.fileId.replace(/^file_/, '').replaceAll('-','');if(j.images.some(im=>im.src.replaceAll('-','').includes(compact)))continue;const index=record.images.length;try{const endpoint='/backend-api/share/'+encodeURIComponent(new URL(location.href).pathname.split('/').pop())+'/file/'+encodeURIComponent(asset.fileId);let r=await fetch(endpoint,{credentials:'include',signal:AbortSignal.timeout(15000)});if(r.status===401){if(authHeaders===undefined){const session=await(await fetch('/api/auth/session',{credentials:'include',signal:AbortSignal.timeout(15000)})).json();authHeaders=session.accessToken?{Authorization:'Bearer '+session.accessToken}:{};}r=await fetch(endpoint,{credentials:'include',headers:authHeaders,signal:AbortSignal.timeout(15000)});}if(!r.ok)throw Error('Share file HTTP '+r.status);const meta=await r.json();const download=meta.download_url||meta.url;if(!download)throw Error('Share file has no download URL');const image=await fetch(download,{credentials:'omit',signal:AbortSignal.timeout(15000)});if(!image.ok)throw Error('Image HTTP '+image.status);record.images.push({...asset,index,origin:'archived_generated_pointer',base64:await encode(await image.blob())});}catch(e){record.images.push({...asset,index,error:e.message,origin:'archived_generated_pointer'});}}""".replace('ARCHIVED_ASSETS','window.__trAIAssets')
        export_expression=export.replace('URL_VALUE',json.dumps(url)).replace(';return {base64:await encode(new Blob([JSON.stringify(record)]', ';'+fallback+'return {base64:await encode(new Blob([JSON.stringify(record)]')
        commands.append({'action':'save','targetId':target,'expression':export_expression,'path':str(bundle)})
    lines=[json.dumps(c) for c in commands]
    if any(len(line.encode('utf-8'))>=4000 for line in lines):
        raise ValueError('Browser command exceeds the bridge PTY line limit')
    (CACHE/'commands.jsonl').write_text('\n'.join(lines)+'\n')
    write(CACHE/'plan.json',{'sources':queue,'createdAt':now()});write(STATUS,{'title':'背景取回來源AI解說圖','state':'queued','sources':queue,'updatedAt':now(),'total':len(queue),'completed':0})
    print({'sources':orders,'commands':len(commands)})

def watch(timeout):
    queue=read(CACHE/'plan.json')['sources'];deadline=time.monotonic()+timeout
    dest=ROOT/'docs/source-ai-images';dest.mkdir(parents=True,exist_ok=True)
    while True:
        for item in queue:
            file=ROOT/item['bundle']
            if item['state']!='queued' or not file.exists():continue
            try:
                bundle=read(file);assert bundle['url']==item['url'] and bundle['kind']=='ai_explanation'
                images=[];errors=[];seen=set();key=item['url'].split('/')[-1][:8]
                for image in bundle['images']:
                    if not image.get('base64'):errors.append({'index':image['index'],'fileId':image.get('fileId'),'title':image.get('alt'),'error':image.get('error')});continue
                    raw=base64.b64decode(image['base64'],validate=True);digest=hashlib.sha256(raw).hexdigest()
                    if digest in seen:continue
                    seen.add(digest);ext='.png' if raw.startswith(b'\x89PNG') else '.jpg' if raw.startswith(b'\xff\xd8') else '.webp' if raw.startswith(b'RIFF') else None
                    if ext is None:raise ValueError('Not image data')
                    path=dest/f'chatgpt-{key}-ai-{image["index"]+1}{ext}';path.write_bytes(raw)
                    images.append({'path':str(path.relative_to(ROOT)),'index':image['index']+1,'sha256':digest,'bytes':len(raw),'width':image['width'],'height':image['height'],'alt':image['alt'],'visualChecked':False,'questionId':None})
                state='acquired' if images and not errors else 'partial'
                write(RESULTS/f'gpt-ai-{item["order"]:03}.json',{'batch':'gpt','order':item['order'],'url':item['url'],'kind':'ai_explanation','checkedAt':bundle['checkedAt'],'state':state,'archiveGeneratedImages':item.get('archiveGeneratedImages',0),'domSweepStatus':bundle.get('domSweepStatus'),'acquisitionMethod':bundle.get('acquisitionMethod'),'images':images,'errors':errors,'note':'尚待逐圖核對，不是原卷證據；未自動加入題目。'})
                item.update(state=state,imagesAvailable=len(images));print(json.dumps({'order':item['order'],'aiImages':len(images),'errors':errors}),flush=True)
            except (OSError,ValueError,KeyError):continue
        pending=[s for s in queue if s['state']=='queued'];expired=time.monotonic()>=deadline
        write(STATUS,{'title':'背景取回來源AI解說圖','state':'timeout' if expired and pending else 'running' if pending else 'complete','sources':queue,'updatedAt':now(),'total':len(queue),'completed':len(queue)-len(pending)})
        if not pending or expired:break
        time.sleep(3)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True);q=sub.add_parser('plan');q.add_argument('--target',required=True);q.add_argument('orders',nargs='+',type=int);w=sub.add_parser('watch');w.add_argument('--timeout',type=int,default=2400);a=p.parse_args();plan(a.target,a.orders) if a.action=='plan' else watch(a.timeout)
