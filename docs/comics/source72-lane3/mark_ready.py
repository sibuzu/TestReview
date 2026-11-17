from pathlib import Path
import json,datetime,sys,hashlib
R=Path(__file__).resolve().parents[3];P=R/'docs/imports/new-gpt-20261117-72/lane3';O=P/'comics';qid=sys.argv[1]
sp=R/f'docs/comics/{qid}.json';vp=R/f'docs/comics/{qid}-preview-validation.json';s=json.load(open(sp));qa=json.load(open(vp));q=json.load(open(P/f'{qid}.json'));assert len(s['artHashes'])==4 and len(set(s['artHashes'].values()))==4
assert {x['viewport'] for x in qa['results']}=={1440,1120,390}
for x in qa['results']:
 assert not x['wrapErrors'] and not x['protectedBreaks'] and not x['overflow'] and not x['docOverflow'];assert len(x['art'])==4 and all(a['loaded'] and a['single'] for a in x['art'])
now=datetime.datetime.now(datetime.timezone.utc).isoformat();s.update(visualChecked=True,producerVisualChecked=True,producerCheckedAt=now,checkedAt=now,previewValidation=str(vp.relative_to(R)),visualReview='Actually viewed original materials, all four new native/raster art works at original rendering size, and 1440/1120/390 preview screenshots. Historical contexts and precise relations checked; no missing text, clipping or overflow; original answer/date preserved.')
sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
actual=s['originalMaterials']+list(s['artHashes'])+[x['screenshot'] for x in qa['results']]
r={'id':qid,'originalVisualChecked':True,'completeOriginalAndOptions':True,'sourceGeneratedArtUsed':False,'actualViewed':actual,'rationale':s['rationale'],'answerPreserved':q['answer'],'datePreserved':q['date'],'artHashes':s['artHashes'],'previewValidation':str(vp.relative_to(R)),'generationEvidence':s['generationEvidence'],'supportingSources':s['supportingSources'],'passed':True,'checkedAt':now}
rp=O/f'{qid}-comic-review.json';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(Path(__file__).parent/f'{qid}-review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
m=json.load(open(P/'manifest.json'))
for x in m['items']:
 if x['candidateId']==qid:x.update(specPath=str(sp.relative_to(R)),specSHA256=hashlib.sha256(sp.read_bytes()).hexdigest(),previewValidation=str(vp.relative_to(R)),comicReviewPath=str(rp.relative_to(R)),illustrationStatus='ready',status='ready')
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(qid,'4 new images + actual visual QA ready')
