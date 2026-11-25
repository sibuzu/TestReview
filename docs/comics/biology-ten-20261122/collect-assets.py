"""Audit decoded publication assets against this batch's copied raw images."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=read(D/'manifest.json');assert m['state']=='complete' and len(m['completedQuestionIds'])==10
data=read(R/'site/dist/data.json');questions={q['id']:q for q in data['questions']};results=[]
for qid in m['questionIds']:
 matches=list(D.glob(f'bio_*/{qid}-handoff.json'));assert len(matches)==1
 hp=matches[0];h=read(hp);sp=R/h['specPath'];rp=R/h['reviewPath']
 assert sha(sp)==h['specSHA256'] and sha(rp)==h['reviewSHA256']
 spec=read(sp);q=questions[qid];comic=q['teachingComic'];raw=[p['image']for p in spec['panels']]+[spec['fourth']['image']];web=[p['image']for p in comic['panels']]+[comic['fourth']['image']]
 images=[]
 for a,b in zip(raw,web):
  source=R/a;dest=R/'site/dist'/b;assert source.is_file() and dest.is_file() and b.endswith('.webp')
  with Image.open(source)as im:im.load();raw_size=im.size
  with Image.open(dest)as im:im.load();web_size=im.size
  assert raw_size==web_size
  images.append(dict(original=a,published='site/dist/'+b,originalSHA256=sha(source),publishedSHA256=sha(dest),width=raw_size[0],height=raw_size[1],decoded=True,originalDimensionsPreserved=True))
 assert len({i['originalSHA256']for i in images})==len({i['publishedSHA256']for i in images})==4
 results.append(dict(id=qid,title=q['title'],url='https://monitor-test.sibuzu.com/site/index.html#question/'+qid,method='built-in image_gen; four separate accepted illustrations',handoff=str(hp.relative_to(R)),prompts=h['promptsPath'],generationEvidence=h['generationPath'],review=h['reviewPath'],images=images))
report=dict(checkedAt=datetime.now(timezone.utc).isoformat(),passed=True,questionCount=10,imageCount=40,method='built-in image_gen',rawPNGPolicy='Saved in the workspace; excluded from Git. Website uses shared full-dimension WebP quality88.',results=results)
(D/'final-assets.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS 40 decoded WebP files match raw image dimensions; prompt records retained')
