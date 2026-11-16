"""Read-only intake validation; only writes this batch's audit report."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
data=read('site/dist/data.json');old=read('.cache/intake-20261116/integration-baseline-data.json')
ids={f'q-{i}' for i in range(1106,1133)};new={q['id']:q for q in data['questions'] if q['id'] in ids};assert set(new)==ids
assert len(data['questions'])==936 and sum(len(q.get('groupQuestions') or [q]) for q in data['questions'])==1012
oldmap={q['id']:q for q in old['questions']};current={q['id']:q for q in data['questions']};derived={'reviewLabel','reviewPreviousId','reviewNextId'};changes=[]
for qid,q in oldmap.items():
 a=dict(q);b=dict(current[qid]);changed={k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)}
 if changed:
  assert qid in {'q-951','q-1092','q-1095'} and changed<=derived,(qid,changed)
  changes.append({'id':qid,'derivedReviewNavigationFields':sorted(changed)})
 for key in derived:a.pop(key,None);b.pop(key,None)
 assert a==b,qid
orig=read('docs/acquisition/new-gpt-20261116-71.json');assert len(orig['downloadedImages'])==28
for im in orig['downloadedImages']:
 p=R/im['path'];assert sha(p)==im['sha256'];matches=list((R/'site/dist/assets/originals').glob(p.stem+'-*.jpg'));assert any(dest.read_bytes()==p.read_bytes() for dest in matches)
assets=[];jobs=read('docs/comics/pipeline.json')['jobs'];events=[];formats={}
for qid,q in new.items():
 assert q['sourceId']=='src-more-071' and q['date']=='2026-11-16' and q['contentStatus']==('待更新' if qid=='q-1107' else '完整原題')
 assert not q.get('explanationFigures') and q.get('studentAnswer')
 comic=q['teachingComic'];images=[p['image'] for p in comic['panels']]+[comic['fourth']['image']];assert len(images)==len(set(images))==4
 hashes=[]
 for path in images:
  p=R/'site/dist'/path;assert p.is_file();hashes.append(sha(p));assets.append(path);formats[p.suffix]=formats.get(p.suffix,0)+1
 assert len(set(hashes))==4
 s=read(f'docs/comics/{qid}.json');assert s['sourceGeneratedArtUsed'] is False and s['rootReview']['visualChecked']
 assert s['rootReview']['desktopMobileActuallyViewed'] and all(Path(p).is_file() for p in s['rootReview']['screenshots'])
 v=read(f'docs/comics/{qid}-validation.json');assert {(r['standalone'],r['viewport']) for r in v['results']}=={(x,w) for x in [True,False] for w in [1440,1120,390]}
 assert all(len(r['artImages'])==4 and all(im['loaded'] for im in r['artImages']) and not r['overflow'] and not r['docOverflow'] and not r['wrapErrors'] and not r['protectedBreaks'] for r in v['results'])
 preview=read(f'docs/comics/{qid}-preview-validation.json');assert {r['viewport'] for r in preview['results']}=={1440,1120,390}
 job=next(j for j in reversed(jobs) if j['id']==qid)
 if qid=='q-1122':assert job['state']=='blocked' and job['decision']=='awaiting_confirmation' and not job.get('integrationEventId')
 else:assert job['state']=='integrated' and job['decision']=='complete';events.append(job['integrationEventId'])
assert len(events)==len(set(events))==26 and len(assets)==len(set(assets))==108
for qid in ['q-1107','q-1122']:assert new[qid]['verification']=='待核對' and new[qid]['reviewQuestions']
for qid in ids-{'q-1107','q-1122'}:assert new[qid]['verification']=='原卷逐題核對'
c=read('monitor/confirmations.json');oldc=read('.cache/intake-20261116/integration-baseline-confirmations.json');preserved={r['id'] for key in ['requests','resolved'] for r in oldc[key]};assert preserved<={r['id'] for key in ['requests','resolved'] for r in c[key]}
reviews=read('docs/imports/new-gpt-20261116/registered-reviews.json');assert len(reviews)==7
for ref in reviews:
 row=next(r for key in ['requests','resolved'] for r in c[key] if r['id']==ref['confirmationId']);assert row['questionText'] and row['questionUrl'] and row['sourceUrl'] and row['before'] and row['after']
for q in data['questions']:
 for child in q.get('groupQuestions') or [q]:
  def walk(x):
   if isinstance(x,dict):
    for k,v in x.items():yield from walk(v)
   elif isinstance(x,list):
    for y in x:yield from walk(y)
   elif isinstance(x,str) and x.startswith('assets/'):yield x
  for path in walk(child):assert (R/'site/dist'/path).is_file(),path
out={'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'pages':936,'originalQuestions':1012,'newQuestions':27,'originalFilesByteExact':28,'fourImageFiles':108,'imageFormats':formats,'completeIntegrationEvents':26,'awaitingAnswerWithoutEvent':['q-1122'],'pendingOriginalQuestionReviews':['q-1107','q-1122'],'incompleteOriginalTranscription':['q-1107'],'oldQuestionPagesPreserved':909,'oldOriginalQuestionsPreserved':985,'derivedReviewNavigationChanges':changes,'priorConfirmationIdsPreserved':len(preserved),'newConfirmationCards':7,'formalComicLayouts':162,'producerPreviewLayouts':81,'allReferencedQuestionAssetsExist':True}
(D/'completion-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
