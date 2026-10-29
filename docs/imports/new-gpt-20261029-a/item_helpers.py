from pathlib import Path
import json,hashlib,datetime,time
from PIL import Image
from zoneinfo import ZoneInfo
R=Path('/home/jack/git/TestReview');P=R/'docs/imports/new-gpt-20261029-a'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_item(q,spec,svg,page,crop,contentReview,artPath=None):
 qid=q['id'];qp=P/'questions'/f'{qid}.json';assert not qp.exists(),f'Do not overwrite frozen {qid}'
 start=time.monotonic_ns();stamp=now();maps=json.loads((P/'original-image-map.json').read_text());orig=maps[page-1]
 art=R/artPath if artPath else R/'docs/comics/art'/f'{qid}.svg'
 if not artPath:art.write_text(svg)
 assert art.exists()
 spec.update(id=qid,subject=q['subject'],art=str(art.relative_to(R)),layoutVersion='native-fluid-v6',generationMethod='new_builtin_imagegen' if artPath else 'precise_native_svg',generationCalls=1 if artPath else 0,sourceGeneratedArtUsed=False,sourceOriginalImage=orig['path'],sourceOriginalSHA256=orig['sha256'],sourceQuestionNumber=q.get('originalQuestionNumber'),startedAt=stamp,startedMonotonicNs=start,timingScope='本題專屬稿、原生SVG與隔離QA；不含先前來源取得與整批原卷預讀')
 dump(R/'docs/comics'/f'{qid}.json',spec)
 out=R/'.cache/new-gpt-20261029-a-publish'/f'{qid}-original.webp';im=Image.open(R/orig['uprightPath']);im.crop(crop).save(out,lossless=True,method=6)
 target=f'assets/originals/{qid}-original.webp';publicArt=f'assets/comics/{qid}-new-art'+('.webp' if artPath else '.svg')
 if artPath:
  publishArt=R/'.cache/new-gpt-20261029-a-publish'/f'{qid}-new-art.webp';Image.open(art).save(publishArt,'WEBP',quality=88,method=6)
 else:publishArt=art
 q.update(sourceId='src-more-049',volume='綜合',chapter='綜合',date='2026-10-29',dateLabel='首次出題日期',addedAt=datetime.datetime.now(ZoneInfo('Asia/Taipei')).date().isoformat(),images=[target],questionFigures=q.get('questionFigures',[]),explanationFigures=[],tables=q.get('tables',[]),passage=q.get('passage',''),sourceLabel=f"分享原卷｜第{q['originalQuestionNumber']}題",verification='原卷逐題核對',verificationNote='已逐字實看原卷、完整上文及全部選項；答案與原卷紅筆及獨立推理對照，未使用來源AI圖。',contentStatus='完整原題',status='todo',starred=False,notes='',teachingComic={**{k:spec[k] for k in ['title','panels','fourth','protectedWords']},'art':publicArt})
 dump(qp,q)
 assets=[dict(sourcePath=str(out.relative_to(R)),targetPath=target,sha256=sha(out),lossless=True,kind='original_crop',cropBox=list(crop),originalSHA256=orig['sha256']),dict(sourcePath=str(publishArt.relative_to(R)),targetPath=publicArt,sha256=sha(publishArt),lossless=not bool(artPath),kind='new_generated_illustration' if artPath else 'new_native_art')]
 ap=P/'asset-map.json';am=json.loads(ap.read_text());am.extend(assets);dump(ap,am)
 src=json.loads((P/'source.json').read_text());src['images'].append(target);dump(P/'source.json',src)
 contentReview.update(id=qid,sourceQuestionNumber=q['originalQuestionNumber'],originalPath=orig['path'],originalSHA256=orig['sha256'],actualViewed=orig['uprightPath'],fullStemAndFourChoicesChecked=True,sourceGeneratedArtUsed=False,checkedAt=stamp)
 dump(P/'reviews'/f'{qid}-content.json',contentReview)
 print(qid,'draft built',out.stat().st_size)
def svg(body):return '<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><rect width="540" height="180" fill="#f8fbf3"/><g font-family="Noto Sans CJK TC,sans-serif" text-anchor="middle" fill="#294d42">'+body+'</g></svg>'
def choice_records(rows,answer):return [dict(label=l,text=t,wordClass='應選' if l==answer else '不選',meaning='',explanation=e) for l,t,e in rows]
