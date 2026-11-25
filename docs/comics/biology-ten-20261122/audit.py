"""Read-only limited biology audit; does not accept work or alter queue state."""
from pathlib import Path
import json,hashlib,subprocess,datetime,argparse,sys
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent;sys.path.insert(0,str(R))
from monitor.comic_execution import assert_work_allowed
def load(p):return json.loads((R/p).read_text())
parser=argparse.ArgumentParser();parser.add_argument('--final',action='store_true');args=parser.parse_args()
m=load(D/'manifest.json');scope=set(m['questionIds']);accepted=set(m['completedQuestionIds']);assert len(scope)==10 and len(accepted)==len(m['completedQuestionIds']) and accepted<=scope
before=load(D/'questions-before.json');after=load('site/dist/data.json');old={q['id']:q for q in before['questions']};new={q['id']:q for q in after['questions']};assert old.keys()==new.keys()
for qid,q in old.items():
 a=dict(q);b=dict(new[qid])
 if qid in scope:a.pop('teachingComic',None);b.pop('teachingComic',None)
 assert a==b,('Original content/date/answer changed',qid)
baseline=json.loads(subprocess.check_output(['git','show',m['baselineCommit']+':docs/comics/pipeline.json'],text=True,cwd=R))
baseline_events={j.get('integrationEventId') for j in baseline['jobs'] if j.get('integrationEventId')}
jobs=load('docs/comics/pipeline.json')['jobs'];fresh=[j for j in jobs if j.get('integrationEventId') and j['integrationEventId'] not in baseline_events]
assert len(fresh)==len(accepted) and {j['id'] for j in fresh}==accepted
quality=load('site/dist/biology-illustration-status.json');old_quality=load(D/'biology-illustration-status-before.json')
for qid in set(quality)-scope:assert quality[qid]==old_quality[qid],('Unselected biology label changed',qid)
for qid in accepted:
 q=new[qid];s=load(f'docs/comics/{qid}.json');review=s['rootReview'];assert all(review.get(k) is True for k in ['visualChecked','originalVisualChecked','answerAndExplanationChecked','fourActualIndependentImages','desktopMobileActuallyViewed']);assert all(Path(p).is_file() for p in review['screenshots'])
 c=q['teachingComic'];images=[p['image'] for p in c['panels']]+[c['fourth']['image']];assert len(images)==len(set(images))==4
 hashes=[]
 for path in images:
  p=R/'site/dist'/path;assert p.is_file();hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
 assert len(set(hashes))==4 and quality[qid]['state']=='fine'
 v=load(f'docs/comics/{qid}-validation.json');assert {(r['standalone'],r['viewport']) for r in v['results']}=={(view,w) for view in [False,True] for w in [1440,1120,390]}
 assert all(len(r['artImages'])==4 and all(im['loaded'] for im in r['artImages']) and not r['overflow'] and not r['docOverflow'] and not r['wrapErrors'] and not r['protectedBreaks'] for r in v['results'])
if args.final:
 assert len(accepted)==10 and m['state']=='complete' and m['stopGateClosed']
 assert load('docs/comics/pipeline.json')['claimsPaused']
 assert all(lane['claimsPaused'] for lane in load('monitor/parallel.json')['lanes'])
 plan=load('docs/comics/biology-rework-20261112/plan.json');control=plan['executionControl'];assert control['mode']=='biology_limited' and control['biologyQualityUpgrade']=='paused' and control['textOnlyReplacement']=='paused' and control['remainingActiveOriginalQuestions']==0
 paused=[e for e in plan['entries'] if e['state']=='paused'];paused_ids={qid for e in paused for qid in e.get('originalQuestionIds',[e['id']])};assert control['pausedQuestionPageCount']==len(paused)==48 and control['pausedOriginalQuestionCount']==len(paused_ids)==55 and set(control['pausedOriginalQuestionIds'])==paused_ids
 assert load('monitor/rework-priority.json')['executionControl']==control
 for qid in scope|{'q-311','q-912'}:
  try:assert_work_allowed(R,qid)
  except ValueError:continue
  raise AssertionError('Stopped scope still accepts '+qid)
out={'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'final':args.final,'scope':m['questionIds'],'accepted':len(accepted),'fourImagesAccepted':4*len(accepted),'newStableIntegrationEvents':len(fresh),'allQuestionPagesPreserved':len(new),'allOriginalContentsDatesAnswersPreserved':True,'unselectedBiologyQualityUnchanged':True,'stopGateClosed':len(accepted)==10}
(D/'completion-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
