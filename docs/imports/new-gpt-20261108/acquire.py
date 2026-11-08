import concurrent.futures,hashlib,json,pathlib,re,datetime,requests,io
from PIL import Image
R=pathlib.Path(__file__).resolve().parents[3]
IDS=['6af03166-a5b4-83ee-88dc-9d884a87b1c5','6af04774-019c-83ee-9f45-5df6edfd1739','6af05e92-295c-83e8-adfb-12e134c3492a']
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
for idx,sid in enumerate(IDS,62):
 d=json.loads((R/'.cache/intake-20261108'/f'{sid}-api.json').read_text());url='https://chatgpt.com/share/'+sid
 messages=[n['message'] for n in d['linear_conversation'] if n.get('message')]
 save(R/'docs/sources'/f'{sid}.json',dict(url=url,title=d['title'],messages=messages,create_time=d['create_time']))
 txt='\n\n'.join(m['author']['role']+'\n'+'\n'.join(p if isinstance(p,str) else '[attachment '+str(p.get('asset_pointer',''))+']' for p in m.get('content',{}).get('parts',[])) for m in messages if m['author']['role'] in ['user','assistant'])
 dr=R/'docs/imports/new-gpt-20261108'/f'gpt{idx:03}';dr.mkdir(parents=True,exist_ok=True);(dr/'transcript.txt').write_text(txt)
 pointers=[]
 for m in messages:
  if m['author']['role']!='user':continue
  for p in m.get('content',{}).get('parts',[]):
   if isinstance(p,dict) and p.get('content_type')=='image_asset_pointer':
    fid=re.search(r'file_[a-zA-Z0-9]+',p['asset_pointer']).group();pointers.append((fid,p,m))
 def fetch(it):
  j,(fid,p,m)=it;out=dict(fileId=fid,messageId=m['id'],firstQuestionTimestamp=m.get('create_time'),userText='\n'.join(t for t in m['content']['parts'] if isinstance(t,str)),expectedBytes=p.get('size_bytes'))
  try:
   meta=requests.get(f'https://chatgpt.com/backend-api/share/{sid}/file/{fid}',timeout=30);out['endpointStatus']=meta.status_code;meta.raise_for_status();v=meta.json();download=v.get('download_url') or v.get('url');assert download,'No download URL'
   data=requests.get(download,timeout=45);out['downloadStatus']=data.status_code;data.raise_for_status();raw=data.content
   image=Image.open(io.BytesIO(raw));image.load();ext={'JPEG':'jpg','PNG':'png','WEBP':'webp'}[image.format]
   path=R/'docs/source-pages'/f'chatgpt-{sid[:8]}-{j}.{ext}';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
   out.update(path=str(path.relative_to(R)),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),width=image.width,height=image.height,decoded=True,archiveSizeMatched=len(raw)==p.get('size_bytes'))
  except Exception as e:out['error']=str(e).split('?')[0][:200]
  return out
 result=list(concurrent.futures.ThreadPoolExecutor(6).map(fetch,enumerate(pointers,1)))
 record=dict(batch='gpt',order=idx,sourceId=f'src-more-{idx:03}',url=url,title=d['title'],state='acquired' if all(i.get('decoded') and i.get('archiveSizeMatched') for i in result) else 'partial',checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),imagesExpected=len(pointers),downloadedImages=[i for i in result if i.get('decoded')],errors=[i for i in result if not i.get('decoded')],archive=f'docs/sources/{sid}.json',textComplete=True,archiveMessages=len(messages),method='public_share_api_and_individual_original_attachment_downloads',sourceGeneratedArtUsed=False)
 save(R/'docs/acquisition'/f'new-gpt-20261108-{idx}.json',record);save(dr/'acquisition.json',record)
 print(json.dumps(dict(order=idx,imagesExpected=len(pointers),downloaded=len(record['downloadedImages']),errors=record['errors']),ensure_ascii=False),flush=True)
