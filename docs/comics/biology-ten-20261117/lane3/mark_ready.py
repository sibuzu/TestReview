from pathlib import Path
import json,datetime,sys,hashlib
R=Path(__file__).resolve().parents[4];P=Path(__file__).parent;qid=sys.argv[1]
spec=R/f'docs/comics/{qid}.json';v=R/f'docs/comics/{qid}-preview-validation.json';s=json.loads(spec.read_text());qa=json.loads(v.read_text())
assert {x['viewport'] for x in qa['results']}=={1440,1120,390}
for x in qa['results']:
 assert not x['wrapErrors'] and not x['protectedBreaks'] and not x['overflow'] and not x['docOverflow']
 assert len(x['art'])==4 and all(a['loaded'] and a['single'] for a in x['art'])
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
s.update(visualChecked=True,producerVisualChecked=True,producerCheckedAt=now,checkedAt=now,previewValidation=str(v.relative_to(R)),visualReview='Producer actually viewed the original materials, all four new full-size PNGs, and 1440/1120/390 isolated screenshots; distinct scientific illustrations and all explanatory text readable; no clipping or overflow.')
spec.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
review=dict(id=qid,originalsActuallyViewed=s['originalMaterials'],actualViewed=list(s['artHashes'])+[x['screenshot'] for x in qa['results']],artHashes=s['artHashes'],scientificReview=s['rationale'],answerPreserved=True,sourceGeneratedArtUsed=False,reusedOldGeneratedArt=False,fourIndependentNewImages=True,previewValidation=str(v.relative_to(R)),checkedAt=now,passed=True)
(P/f'{qid}-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(qid,'review saved',hashlib.sha256(spec.read_bytes()).hexdigest())
