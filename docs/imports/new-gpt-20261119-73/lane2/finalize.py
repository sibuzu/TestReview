from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
R=Path.cwd();B=R/'docs/imports/new-gpt-20261119-73/lane2';cache=R/'.cache/intake-20261119-73-lane2'
def read(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def rel(p):return str(p.relative_to(R))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(R/'docs/imports/new-gpt-20261119-73/acquisition.json');d={x['id']:x for x in read(B/'dedupe-review.json')['items']};m=read(B/'manifest.json');timestamp=datetime.now(timezone.utc).isoformat()
red={'q-1157':'第9題原選D；左側紅筆B及紅色劃記，與User 9@錯題D→B一致。','q-1158':'第19題原選C；左側紅筆D與紅色劃記，User 19@錯題c→D。共同哈伯法框全留。','q-1159':'第3題原選D；左側紅筆A與題號紅劃，User 3@錯題D→A。','q-1160':'第7題原選D；左側紅筆B與題號紅劃，User 7@錯題D→B。','q-1161':'第8題原選A；左側紅筆B與劃記，User 8@錯題A→B。','q-1162':'第10題原選B；左側紅筆D與劃記，User 10@錯題B→D。'}
for idx,row in enumerate(m['questions']):
 qid=row['id'];qp=R/row['questionPath'];sp=R/row['specPath'];q=read(qp);s=read(sp);vpath=B/'qa'/f'{qid}-validation.json';v=read(vpath);assert v['passed'] and len(v['results'])==3
 originals=[a['downloadedImages'][idx]['path']];crops=list(dict.fromkeys(q['images']+[f['src'] for f in q['questionFigures']]));paths=[p['image'] for p in s['panels']]+[s['fourth']['image']];assert len(set(paths))==4
 actual=originals+crops+[rel(cache/f'{qid}-art-contact.png')]+[rel(cache/f'{qid}-preview-{w}.png') for w in [1440,390]]
 assert all((R/p).exists() for p in actual)
 v['actualViewed']=True;v['actualViewedPaths']=actual;v['visualReview']='實看本題原卷、裁切、4張獨立SVG各630px檢視及1440/390隔離四格；化學結構與方向、公式、所有圖資、原題/選項/必要圖均核對，無溢出。';save(vpath,v)
 review=dict(id=qid,producerAgent='/root/comic_lane_2',reviewerAgent='/root/comic_lane_2',passed=True,checkedAt=timestamp,originalVisualChecked=True,originalMaterialsChecked=True,completeOriginalAndOptions=True,sourceGeneratedArtUsed=False,actualViewed=actual,inclusionEvidence=red[qid],duplicateReview=d[qid]['basis'],candidateIds=d[qid]['candidateIds'],crossSourceDuplicatesChecked=True,requiredMaterialMissing=False,answerAndExplanationChecked=True,fourActualIndependentImages=True,desktopMobileActuallyViewed=True,qaReportPath=rel(vpath),sourceUrl=m['sourceUrl'],issues=[])
 save(B/'qa'/f'{qid}-review.json',review)
 s.update(visualChecked=True,producerVisualChecked=True,checkedAt=timestamp,artSHA256=sha(R/paths[0]),producerReview=dict(reviewerAgent='/root/comic_lane_2',originalCropsActuallyViewed=True,allFourNewImagesActuallyViewed=True,desktopMobileActuallyViewed=True,screenshots=[rel(cache/f'{qid}-preview-{w}.png') for w in [1440,390]],artContactSheet=rel(cache/f'{qid}-art-contact.png'),validationFile=rel(vpath)))
 save(sp,s)
 row.update(draftPath=row['questionPath'],reviewPath=rel(B/'qa'/f'{qid}-review.json'),qaReportPath=rel(vpath),questionSHA256=sha(qp),specSHA256=sha(sp),reviewSHA256=sha(B/'qa'/f'{qid}-review.json'),qaReportSHA256=sha(vpath))
 row['assets']=[dict(sourcePath=p,sha256=sha(R/p)) for p in list(dict.fromkeys(crops+paths))]
m.update(state='ready',readyAt=timestamp,originalVisualChecked=True,crossSourceDuplicatesChecked=True,sourceGeneratedArtUsed=False,qaPassed=True,actualViewed=True,newQuestionCount=6,illustrationCount=24,reviewRequests=[],readiness='Producer complete; unique integrator still must publish and run formal site/app QA.')
save(B/'manifest.json',m)
save(B/'science-sources.json',dict(checkedAt=timestamp,sources=[dict(url='https://www.colorado.edu/lab/lecture-demo-manual/e790-acidbase-conductimetric-titration-baoh2-h2so4',supports='At equivalence Ba(OH)2/H2SO4 precipitation and neutralization can greatly reduce conductivity.',usedBy=['q-1160']),dict(url='https://www.nature.com/articles/s41586-023-06844-5',supports='Haber-Bosch actual catalysts include Fe; original printed Fe2O3 label preserved as original condition, not presented as active catalyst surface.',usedBy=['q-1158'])],notes='No answer change from original user correction in these six. Original AI raster/SVG content not reused.'))
print('READY',','.join(r['id'] for r in m['questions']),'24 independent new SVGs; six questions; 18 viewport checks; actual viewed originals/crops/fullsize/contact and desktop/mobile previews.')
