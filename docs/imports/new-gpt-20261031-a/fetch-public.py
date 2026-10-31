from pathlib import Path
import sys,json,re,urllib.request,datetime,concurrent.futures
from zoneinfo import ZoneInfo
R=Path('/home/jack/git/TestReview');sys.path.insert(0,str(R/'site/scripts'));from read_shares import decode_stream
sources=[('a','https://chatgpt.com/share/6ae5b2dc-89a8-83e8-9d82-7bb25a2a1174'),('b','https://chatgpt.com/share/6ae5b33f-e5a0-83ec-8e02-1b414683bea3')]
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)
def date(v):
 try:return datetime.datetime.fromtimestamp(float(v),ZoneInfo('Asia/Taipei')).isoformat()
 except (ValueError,TypeError,OSError):return None
def fetch(item):
 tag,url=item;P=R/f'docs/imports/new-gpt-20261031-{tag}';cache=R/f'.cache/new-gpt-20261031-{tag}';cache.mkdir(parents=True,exist_ok=True)
 checked=datetime.datetime.now(datetime.timezone.utc).isoformat();result=dict(url=url,checkedAt=checked,state='awaiting_browser_connection',bridgeFailure='ECONNREFUSED 127.0.0.1:9222; no Chrome process/listener observed',downloadedImages=[],downloadedImageCount=0,visualChecked=False,noTranscriptionStarted=True)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'text/html'});resp=urllib.request.urlopen(req,timeout=40);html=resp.read().decode();(cache/'share-page.html').write_text(html)
  data=decode_stream(html);assert data and data.get('linear_conversation'),'No readable conversation'
  messages=[n['message'] for n in data['linear_conversation'] if n.get('message')];archive=dict(url=url,title=data.get('title'),messages=messages,shareCreated=data.get('create_time'),shareUpdated=data.get('update_time'),checkedAt=checked,method='public_share_html_decode')
  write(P/'archive.json',archive);users=[];attachments=[];lines=[]
  for i,m in enumerate(messages):
   role=m.get('author',{}).get('role');parts=m.get('content',{}).get('parts',[]);texts=[x for x in parts if isinstance(x,str)];stamp=date(m.get('create_time'))
   lines.extend([f'MESSAGE {i} | {role} | {m.get("channel")} | {stamp or "date unavailable"}',*texts,''])
   if role=='user':
    users.append(dict(messageIndex=i,messageId=m.get('id'),prompt='\n'.join(texts),createTime=m.get('create_time'),taipeiTime=stamp))
    for part in parts:
     if isinstance(part,dict) and part.get('content_type')=='image_asset_pointer':
      pointer=part.get('asset_pointer','');match=re.match(r'^sediment://(file_[a-zA-Z0-9]+)',pointer)
      attachments.append(dict(messageIndex=i,messageId=m.get('id'),prompt='\n'.join(texts),fileId=match.group(1) if match else None,assetPointer=pointer,width=part.get('width'),height=part.get('height'),sizeBytes=part.get('size_bytes'),createTime=m.get('create_time'),taipeiTime=stamp))
  (P/'transcript.txt').write_text('\n'.join(s.rstrip() for s in lines).rstrip()+'\n');write(P/'user-turns.json',users);write(P/'user-attachment-index.json',attachments)
  unique=list(dict.fromkeys(a['fileId'] or a['assetPointer'] for a in attachments));dates=[u['taipeiTime'][:10] for u in users if u['taipeiTime']]
  result.update(title=data.get('title'),publicTextState='saved',publicHttpStatus=resp.status,archivePath=str((P/'archive.json').relative_to(R)),transcriptPath=str((P/'transcript.txt').relative_to(R)),archiveMessageCount=len(messages),userTurnCount=len(users),userAttachmentOccurrenceCount=len(attachments),expectedImageCount=len(unique),originalMessageDates=sorted(set(dates)),earliestOriginalMessageDate=min(dates) if dates else None,rawHtmlPath=str((cache/'share-page.html').relative_to(R)))
 except Exception as e:result.update(publicTextState='failed',publicError=f'{type(e).__name__}: {e}')
 write(R/f'docs/acquisition/new-gpt-20261031-{tag}.json',result)
 return {k:result.get(k) for k in ['url','title','publicTextState','publicError','archiveMessageCount','userTurnCount','userAttachmentOccurrenceCount','expectedImageCount','originalMessageDates']}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for r in pool.map(fetch,sources):print(json.dumps(r,ensure_ascii=False),flush=True)
