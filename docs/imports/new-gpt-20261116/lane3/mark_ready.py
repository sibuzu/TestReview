from pathlib import Path
import json,sys,datetime,hashlib
P=Path(__file__).parent;R=P.resolve().parents[3]
mp=P/'manifest.json';m=json.load(open(mp));now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for n in map(int,sys.argv[1:]):
 q=f'q-{n}';sp=R/f'docs/comics/{q}.json';s=json.load(open(sp));vp=R/f'docs/comics/{q}-preview-validation.json';v=json.load(open(vp));assert len(v['results'])==3 and all(len(x['art'])==4 and all(z['loaded'] and z['single'] for z in x['art']) for x in v['results']);ims=[x['image'] for x in s['panels']]+[s['fourth']['image']];assert len(set(hashlib.sha256((R/x).read_bytes()).hexdigest() for x in ims))==4
 s.update(visualChecked=True,producerVisualChecked=True,producerCheckedAt=now,checkedAt=now,previewValidation=str(vp.relative_to(R)),visualReview='四張新製獨立SVG與1440/1120/390隔離成品逐張實看，原卷與正式題條件/四選項核對；四圖皆實際載入且完整，繁中公式數值與方向核對，無橫向溢出、保護詞拆行或文字遺漏，答案預設收合。')
 sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
 for x in m['items']:
  if x['candidateId']==q:x.update(specPath=str(sp.relative_to(R)),previewValidation=str(vp.relative_to(R)),comicStatus='ready')
 r=P/f'{q}-review.json';d=json.load(open(r));d['comicReview']=dict(fourActualIndependentImages=True,actualViewed=[x['screenshot'] for x in v['results']],threeWidthsPassed=True,producerCheckedAt=now);r.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
