import pathlib,json,base64,hashlib,io,datetime,re
from PIL import Image
R=pathlib.Path(__file__).resolve().parents[3]
IDS={62:'6af03166-a5b4-83ee-88dc-9d884a87b1c5',63:'6af04774-019c-83ee-9f45-5df6edfd1739',64:'6af05e92-295c-83e8-adfb-12e134c3492a'}
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
known={}
for order in [62,64]:
 b=json.loads((R/f'.cache/intake-20261108/signed-chrome-{order}.json').read_text())
 for i in b['images']:
  if not i.get('base64'):continue
  raw=base64.b64decode(i['base64'],validate=True);im=Image.open(io.BytesIO(raw));im.load();ext={'JPEG':'jpg','PNG':'png','WEBP':'webp'}[im.format]
  p=R/f'docs/source-pages/chatgpt-{IDS[order][:8]}-{i["index"]}.{ext}';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
  known[i['fileId']]=dict(fileId=i['fileId'],path=str(p.relative_to(R)),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),width=im.width,height=im.height,decoded=True)
for order,sid in IDS.items():
 archive=json.loads((R/f'docs/sources/{sid}.json').read_text());rows=[];errors=[]
 for mi,m in enumerate(archive['messages']):
  if m['author']['role']!='user':continue
  for p in m.get('content',{}).get('parts',[]):
   if not isinstance(p,dict) or p.get('content_type')!='image_asset_pointer':continue
   fid=re.search(r'file_[a-zA-Z0-9]+',p['asset_pointer']).group();v=known.get(fid)
   if not v:errors.append(dict(fileId=fid,error='Original not downloaded'));continue
   row=dict(v,messageId=m['id'],messageIndex=mi,firstQuestionTimestamp=m.get('create_time'),userText='\n'.join(x for x in m['content']['parts'] if isinstance(x,str)),archiveSizeMatched=v['bytes']==p.get('size_bytes'))
   rows.append(row)
 path=R/f'docs/acquisition/new-gpt-20261108-{order}.json';old=json.loads(path.read_text());attempt={k:old[k] for k in ['state','method','errors','checkedAt'] if k in old}
 record=dict(batch='gpt',order=order,sourceId=f'src-more-{order:03}',url='https://chatgpt.com/share/'+sid,title=archive['title'],state='acquired' if not errors and len(rows)==old['imagesExpected'] and all(i['archiveSizeMatched'] for i in rows) else 'partial',checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),imagesExpected=old['imagesExpected'],downloadedImages=rows,errors=errors,archive=f'docs/sources/{sid}.json',textComplete=True,archiveMessages=len(archive['messages']),method='user_authorized_signed_in_Windows_Chrome_CDP_and_archived_original_file_ids',sourceGeneratedArtUsed=False,previousAttempt=attempt,anonymousPlaywrightEvidence='docs/acquisition/new-gpt-20261108-playwright.json',notes='真正上傳原卷以archive fileId下載，實際解碼尺寸、位元組數與SHA256核對。63與64的19個附件fileId相同，重用已保存原檔；此點尚非逐題重複判定。無token或圖片簽章網址保存至紀錄。')
 save(path,record);save(R/f'docs/imports/new-gpt-20261108/gpt{order:03}/acquisition.json',record)
 print(order,record['state'],len(rows),'/',record['imagesExpected'],[r['width'] for r in rows],flush=True)
