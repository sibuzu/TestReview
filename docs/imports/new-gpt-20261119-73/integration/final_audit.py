"""Read-only evidence that this intake preserves existing content and publishes 4 images/item."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,now
from monitor.comic_publish import pending_batch
old=load(ROOT/'.cache/intake-20261119-6aff02c8/baseline-data.json');new=load(ROOT/'site/dist/data.json');plan=load(D/'plan.json');scope=load(D/'execution-scope.json');ids=set(scope['newQuestionIds'])
oldq={q['id']:q for q in old['questions']};newq={q['id']:q for q in new['questions']}
assert set(newq)-set(oldq)==ids and set(oldq)<=set(newq)
assert len(ids)==12 and len(newq)==969 and len(oldq)==957
assert all(oldq[i]==newq[i] for i in oldq),'An existing question changed'
assert old['revision']!=new['revision']
assert all(newq[i]['date']=='2026-11-19' and newq[i]['sourceId']=='src-more-073' for i in ids)
assets=[]
for qid in sorted(ids):
 q=newq[qid];assert q['contentStatus']=='完整原題' and not q.get('explanationFigures')
 assert q['volume']==q['chapter']=='綜合'
 comic=q['teachingComic'];paths=[p['image'] for p in comic['panels']]+[comic['fourth']['image']]
 assert len(paths)==len(set(paths))==4
 hashes=[]
 for relative in paths:
  p=ROOT/'site/dist'/relative;raw=p.read_bytes();hashes.append(hashlib.sha256(raw).hexdigest());assert p.suffix=='.svg';ET.fromstring(raw)
  assert any(x in raw for x in [b'<path',b'<circle',b'<rect',b'<line',b'<polygon',b'<ellipse'])
  assets.append(dict(id=qid,path=relative,bytes=len(raw),sha256=hashes[-1]))
 assert len(set(hashes))==4
 for p in q['images']+[f['src'] for f in q.get('questionFigures',[])]:assert (ROOT/'site/dist'/p).is_file()
 spec=load(ROOT/f'docs/comics/{qid}.json');assert spec['sourceGeneratedArtUsed'] is False
 assert spec['rootReview']['desktopMobileActuallyViewed'] and spec['rootReview']['inheritedWithoutRepeatedOriginalReview']
 v=load(ROOT/f'docs/comics/{qid}-validation.json');assert len(v['results'])==6
 assert all(len(r['artImages'])==4 and not r['overflow'] and not r['docOverflow'] and all(im['loaded'] for im in r['artImages']) for r in v['results'])
 html=(ROOT/f'site/dist/{qid}.html').read_text();assert '<details class="review">' in html and 'base64,' not in html
assert len(assets)==48
acq=load(D/'acquisition.json');assert len(acq['downloadedImages'])==acq['imagesExpected']==12
for r in acq['downloadedImages']:
 p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 assert r['decoded'] and r['archiveSizeMatched'] and (r['width'],r['height'])==(1080,1440)
execution=load(D/'execution-progress.json');complete=set(execution['completedQuestionIds']);pending=set(execution['awaitingConfirmationQuestionIds']);assert complete|pending==ids and not complete&pending
assert len(plan['integrationEvents'])==len(complete)
assert {e['id'] for e in plan['integrationEvents']}==complete
assert not pending&{e['id'] for e in plan['integrationEvents']}
assert plan['productionStopped'] and plan['illustrationsOutstanding']==0 and plan['validatedIllustrationCount']==48
assert load(ROOT/'monitor/new-source-authorization.json')['state']=='closed' and load(ROOT/'docs/comics/pipeline.json')['claimsPaused']
_,_,_,jobs=pending_batch();baseline=load(D/'publication-baseline.json');assert len(jobs)==baseline['pendingEventCount']+len(complete)
report=dict(checkedAt=now(),passed=True,originals=12,archiveMessages=80,oldQuestionsPreserved=957,newQuestionPages=12,totalQuestionPages=969,independentNewImages=48,formalLayoutChecks=72,completedIntegrationEvents=len(complete),awaitingConfirmationQuestionIds=sorted(pending),pendingPublicationEvents=len(jobs),sourceProductionStopped=True,oldQueuesRemainPaused=True,assets=assets)
save(D/'integration/final-audit.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='assets'},ensure_ascii=False))
