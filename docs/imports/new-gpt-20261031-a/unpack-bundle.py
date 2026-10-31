from pathlib import Path
import sys,json,base64,hashlib,datetime
from PIL import Image
R=Path('/home/jack/git/TestReview');tag=sys.argv[1];P=R/f'docs/imports/new-gpt-20261031-{tag}';cache=R/f'.cache/new-gpt-20261031-{tag}';folder=R/f'.cache/new-gpt-20261031-{tag}-originals';folder.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');t.replace(p)
bPath=R/f'.cache/new-gpt-20261031-{tag}-bundle.json';bundle=json.loads(bPath.read_text());assert bundle['url']==json.loads((P/'archive.json').read_text())['url'];archive=bundle.get('archive');assert archive and archive.get('messages'),bundle.get('archiveError')
public=json.loads((P/'archive.json').read_text());apiMessages=archive['messages'];publicMessages=public['messages'];sameIDs=[m['id'] for m in apiMessages]==[m['id'] for m in publicMessages]
keys=lambda m:(m.get('id'),m.get('author',{}).get('role'),m.get('create_time'),m.get('content'))
sameContents=[keys(m) for m in apiMessages]==[keys(m) for m in publicMessages]
apiPath=cache/'archive-authorized.json';dump(apiPath,archive)
lookup={}
for mi,m in enumerate(apiMessages):
 if m.get('author',{}).get('role')!='user':continue
 for p in m.get('content',{}).get('parts',[]):
  if isinstance(p,dict) and p.get('content_type')=='image_asset_pointer':
   fid=p['asset_pointer'].split('sediment://',1)[-1].split('?',1)[0];lookup[fid]={'messageIndex':mi,'messageId':m['id'],'prompt':'\n'.join(v for v in m['content']['parts'] if isinstance(v,str)),**p}
items=[];errors=[]
for n,img in enumerate(bundle['images'],1):
 if not img.get('base64'):errors.append({k:v for k,v in img.items() if k!='base64'});continue
 raw=base64.b64decode(img['base64'],validate=True);ext='.jpg' if raw.startswith(b'\xff\xd8') else '.png' if raw.startswith(b'\x89PNG') else '.webp' if raw.startswith(b'RIFF') else None;assert ext,'Not an image'
 path=folder/f'user-{n:03}{ext}';path.write_bytes(raw)
 with Image.open(path) as im:width,height=im.size;im.verify()
 f=lookup.get(img.get('fileId'),{});items.append(dict(index=n-1,path=str(path.relative_to(R)),fileId=img.get('fileId'),sha256=sha(raw),bytes=len(raw),width=width,height=height,archivePointerWidth=f.get('width'),archivePointerHeight=f.get('height'),archivePointerSizeBytes=f.get('size_bytes'),pointerDimensionsMatch=(width,height)==(f.get('width'),f.get('height')),pointerSizeMatches=len(raw)==f.get('size_bytes'),messageIndex=f.get('messageIndex'),messageId=f.get('messageId'),prompt=f.get('prompt'),origin=img.get('origin'),visualChecked=False))
expected=set(lookup);covered={i['fileId'] for i in items};assert covered<=expected;missing=sorted(expected-covered)
mapPath=P/'original-image-map.json';dump(mapPath,items)
acqPath=R/f'docs/acquisition/new-gpt-20261031-{tag}.json';a=json.loads(acqPath.read_text());a.update(checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),state='acquired_pending_visual_check' if not errors and not missing else 'partial_original_acquisition',browserConnection='connected',downloadedImages=items,downloadedImageCount=len(items),expectedImageCount=len(expected),uniqueImageSHA256Count=len({i['sha256'] for i in items}),matchedArchiveAttachments=len(expected&covered),allPointerDimensionsMatch=all(i['pointerDimensionsMatch'] for i in items),allPointerSizesMatch=all(i['pointerSizeMatches'] for i in items),bundlePath=str(bPath.relative_to(R)),bundleSHA256=sha(bPath.read_bytes()),authorizedArchivePath=str(apiPath.relative_to(R)),apiMessageCount=len(apiMessages),publicAndApiMessageIDsMatch=sameIDs,publicAndApiQuestionContentsMatch=sameContents,originalImageMapPath=str(mapPath.relative_to(R)),errors=errors,missingFileIds=missing,noTranscriptionStarted=True,visualChecked=False)
dump(acqPath,a)
print(json.dumps({'tag':tag,'saved':len(items),'expected':len(expected),'uniqueImageHashes':a['uniqueImageSHA256Count'],'allDimensionsMatch':a['allPointerDimensionsMatch'],'allSizesMatch':a['allPointerSizesMatch'],'samePublicAndApi':sameIDs and sameContents,'errors':errors,'missing':missing},ensure_ascii=False))
