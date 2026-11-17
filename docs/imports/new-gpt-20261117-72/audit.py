"""Read-only source72 integrity audit. Intake baseline is intentionally local/ignored."""
from pathlib import Path
import argparse, datetime, hashlib, json, sys

R=Path(__file__).resolve().parents[3];D=Path(__file__).parent;sys.path.insert(0,str(R))
from monitor.comic_execution import assert_work_allowed
from monitor.comic_publish import pending_batch

def load(p):return json.loads(p.read_text())
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--final',action='store_true');a=p.parse_args()
before=load(R/'.cache/intake-20261117-72/baseline-data.json');after=load(R/'site/dist/data.json')
old={q['id']:q for q in before['questions']};new={q['id']:q for q in after['questions']}
assert old.keys()<=new.keys()
derived={'reviewLabel','reviewPreviousId','reviewNextId'};nav=[]
for qid,question in old.items():
 changed=[key for key in set(question)|set(new[qid]) if question.get(key)!=new[qid].get(key)]
 assert set(changed)<=derived, ('Existing question changed',qid,changed)
 if changed:
  assert question.get('reviewQuestions'), ('Review navigation changed on nonreview question',qid)
  nav.append({'id':qid,'derivedFields':changed})
scope=load(D/'execution-scope.json');ids=set(scope['newQuestionIds']);published=set(new)-set(old)
assert published<=ids
reserved={r['candidateId']:r for r in load(D/'qid-reservations.json')['items']}
for qid in published:
 q=new[qid];assert q['sourceId']=='src-more-072' and q['date']==reserved[qid]['date']=='2026-11-17'
 assert all(f'({c})' in q['question'] for c in 'ABCD')
 if qid in {'q-1153','q-1154'}:assert q['contentStatus']=='待更新' and q.get('reviewQuestions') and '待核' in q['verification']
 if qid=='q-1135':assert q['contentStatus']=='完整原題' and q.get('reviewQuestions') and '待核' in q['verification']
 assert not q.get('explanationFigures')
plan=load(D/'plan.json');execution=load(D/'execution-progress.json')
completed=set(execution['completedQuestionIds']);awaiting=set(execution.get('awaitingConfirmationQuestionIds',[]))
assert not completed&awaiting and completed|awaiting<=ids
pipeline=load(R/'docs/comics/pipeline.json')
base_pending=load(D/'publication-baseline.json');_,_,_,pending=pending_batch()
all_events={j['integrationEventId'] for j in pipeline['jobs'] if j.get('integrationEventId')}
assert set(base_pending['baselineEventIds'])<=all_events
for qid in completed:
 jobs=[j for j in pipeline['jobs'] if j['id']==qid];assert len(jobs)==1 and jobs[0]['decision']=='complete' and jobs[0]['state']=='integrated' and jobs[0].get('integrationEventId')
for qid in awaiting:
 jobs=[j for j in pipeline['jobs'] if j['id']==qid];assert len(jobs)==1 and jobs[0]['decision']=='awaiting_confirmation' and jobs[0]['state']=='blocked' and not jobs[0].get('integrationEventId')
for qid in completed|awaiting:
 q=new[qid];comic=q['teachingComic'];images=[p['image'] for p in comic['panels']]+[comic['fourth']['image']]
 assert len(images)==len(set(images))==4
 assert len({hashlib.sha256((R/'site/dist'/p).read_bytes()).hexdigest() for p in images})==4
 spec=load(R/f'docs/comics/{qid}.json');review=spec['rootReview']
 assert all(review.get(k) is True for k in ['visualChecked','originalVisualChecked','answerAndExplanationChecked','fourActualIndependentImages','desktopMobileActuallyViewed'])
 assert all(Path(p).is_file() for p in review['screenshots'])
 check=load(R/f'docs/comics/{qid}-validation.json')
 assert {(r['standalone'],r['viewport']) for r in check['results']}=={(v,w) for v in [False,True] for w in [1440,1120,390]}
 assert all(len(r['artImages'])==4 and all(i['loaded'] for i in r['artImages']) and not r['docOverflow'] and not r['overflow'] and not r['wrapErrors'] and not r['protectedBreaks'] for r in check['results'])
originals=load(D/'acquisition.json')['downloadedImages']
for image in originals:
 p=R/image['path'];assert p.stat().st_size==image['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==image['sha256']
references=[]
def assets(node):
 if isinstance(node,dict):
  for v in node.values():assets(v)
 elif isinstance(node,list):
  for v in node:assets(v)
 elif isinstance(node,str) and node.startswith('assets/'):
  assert (R/'site/dist'/node).is_file(),node
  references.append(node)
assets(after)
old_ids={c['id'] for q in before['questions'] for c in q.get('groupQuestions') or [q]}
assert all((R/'site/dist'/f'{qid}.html').is_file() for qid in old_ids)
if a.final:
 assert published==ids and completed|awaiting==ids and plan['productionStopped']
 assert load(R/'monitor/new-source-authorization.json')['state']=='closed'
 assert pipeline['claimsPaused'] and all(l['claimsPaused'] for l in load(R/'monitor/parallel.json')['lanes'])
 for qid in ids|{'q-969','q-912','q-1044','q-1157'}:
  try:assert_work_allowed(R,qid)
  except ValueError:continue
  raise AssertionError('Closed scope still allows '+qid)
out={'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'final':a.final,'preservedQuestionPages':len(old),'preservedOriginalQuestionsAndUrls':len(old_ids),'permittedDerivedReviewNavigationChanges':nav,'newQuestionPagesPublished':len(published),'completeEvents':len(completed),'awaitingWithoutIntegrationEvents':sorted(awaiting),'validatedActualImages':4*(len(completed)+len(awaiting)),'rawOriginalsPreserved':len(originals),'existingAndNewAssetReferencesPresent':len(references),'publicationPendingCount':len(pending),'productionStopped':plan.get('productionStopped',False)}
(D/'completion-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
