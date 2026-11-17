"""Accept one independently inspected biology comic and atomically enforce 10-stop."""
from pathlib import Path
import json,datetime,sys,argparse,subprocess
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent;sys.path.insert(0,str(R))
from monitor.comic_pipeline import integrated,locked,load,save,update_display,now
from monitor.comic_execution import assert_work_allowed
p=argparse.ArgumentParser(description=__doc__);p.add_argument('id');p.add_argument('--note',required=True);a=p.parse_args();qid=a.id
assert_work_allowed(R,qid);m=load(D/'manifest.json');assert qid in m['questionIds'] and qid not in m['completedQuestionIds']
v=load(R/f'docs/comics/{qid}-validation.json')
assert {(r['standalone'],r['viewport']) for r in v['results']}=={(view,w) for view in [True,False] for w in [1440,1120,390]}
assert all(len(r['artImages'])==4 and len({im['src'] for im in r['artImages']})==4 and all(im['loaded'] for im in r['artImages']) and not r['overflow'] and not r['docOverflow'] and not r['wrapErrors'] and not r['protectedBreaks'] for r in v['results'])
base=load(D/'questions-before.json');q=next(q for q in base['questions'] if q['id']==qid)
shots=[f'/tmp/weirugo-comic-checks/{qid}-{view}-{w}.png' for view in ['app','standalone'] for w in [1440,390]];assert all(Path(p).is_file() for p in shots)
s=load(R/f'docs/comics/{qid}.json');s['rootReview']={'reviewerAgent':'/root/comic_lane_1','visualChecked':True,'originalVisualChecked':True,'answerAndExplanationChecked':True,'fourActualIndependentImages':True,'desktopMobileActuallyViewed':True,'screenshots':shots,'originalMaterials':[str(R/'site/dist'/p) for p in q['images']]+[str(R/'site/dist'/f['src']) for f in q.get('questionFigures',[])],'note':a.note,'checkedAt':now()};save(R/f'docs/comics/{qid}.json',s)
prepared=load(D/'prepared-jobs.json')[qid];latest=next(j for j in reversed(load(R/'docs/comics/pipeline.json')['jobs']) if j['id']==qid);assert latest['jobId']==prepared['jobId'];job=latest if latest['state']=='integrated' else integrated(R,qid)
with locked(R):
 m=load(D/'manifest.json');assert qid not in m['completedQuestionIds'];m['completedQuestionIds'].append(qid);m.setdefault('integrationEvents',[]).append({'id':qid,'integrationEventId':job['integrationEventId'],'integratedAt':job['integratedAt']});n=len(m['completedQuestionIds']);assert n<=m['limit']==10;m.update(completedImages=4*n,remaining=10-n,updatedAt=now())
 plan=load(R/'docs/comics/biology-rework-20261112/plan.json');entry=next(e for e in plan['entries'] if qid in e.get('originalQuestionIds',[e['id']]));assert entry['subject']=='Biology';entry.update(state='complete',completedImages=4,completedOriginalIds=[qid],completedAt=now(),limitedBatch='biology-ten-20261117',visualChecked=True,validationFile=f'docs/comics/{qid}-validation.json');entry.pop('pauseReason',None)
 done=[e for e in plan['entries'] if e['state']=='complete'];plan.update(completedQuestionPages=len(done),completedOriginalQuestions=sum(len(e.get('originalQuestionIds',[e['id']])) for e in done),completedImages=sum(e.get('completedImages',0) for e in done),updatedAt=now());plan['executionControl']['remainingActiveOriginalQuestions']=10-n
 paused=[e for e in plan['entries'] if e['state']!='complete' and not set(e.get('originalQuestionIds',[e['id']])) & set(m['questionIds'])];paused_ids=sorted({qid for e in paused for qid in e.get('originalQuestionIds',[e['id']])});plan['executionControl'].update(pausedQuestionPageCount=len(paused),pausedOriginalQuestionCount=len(paused_ids),pausedOriginalQuestionIds=paused_ids)
 priority=load(R/'monitor/rework-priority.json');priority.update(completed=plan['completedOriginalQuestions'],completedQuestionPages=plan['completedQuestionPages'],batchCompletedOriginalQuestions=n,batchRequiredOriginalQuestions=10,updatedAt=now())
 if n==10:
  m.update(state='complete',completedAt=now(),stopGateClosed=True)
  plan.update(state='paused',goalActive=False,pauseReason='本批10題已驗收完成即停，其餘19生物與46非生物仍暫停。');plan['executionControl'].update(biologyQualityUpgrade='paused',textOnlyReplacement='paused',remainingActiveOriginalQuestions=0,limitedBatchCompletedAt=now())
  priority.update(state='paused',title='本批生物10題已完成；其他65原問暫停',questionIds=[],laneAssignments={'1':[],'2':[],'3':[]})
  pipeline=load(R/'docs/comics/pipeline.json');pipeline.update(claimsPaused=True,pauseReason=plan['pauseReason'],pausedAt=now());save(R/'docs/comics/pipeline.json',pipeline)
  display=load(R/'monitor/parallel.json')
  for lane in display['lanes']:
   lane.update(claimsPaused=True,batchQuestionIds=[],activeTask=None)
   if lane['lane']!=2:lane.update(pauseReason=plan['pauseReason'])
  display['rootRole']='本批10題正式驗收完成即停，沒有第11題；其餘重製及Agent2仍暫停。';save(R/'monitor/parallel.json',display)
 priority['executionControl']=plan['executionControl'];save(D/'manifest.json',m);save(R/'docs/comics/biology-rework-20261112/plan.json',plan);save(R/'monitor/rework-priority.json',priority)
 if n==10:update_display(R,load(R/'docs/comics/pipeline.json'))
 save(R/'monitor/activity.json',{'title':f'生物精美解說圖：正式驗收{n}／10'+('，已停止' if n==10 else ''),'detail':f'剛完成{qid}：原卷/答案/四張科學教材圖及正式桌手機實看。其餘19生物與46非生物維持暫停；本批未滿20且未另授權，不commit/push。','stage':'limited_biology_complete' if n==10 else 'limited_biology_integration','goalStatus':'complete' if n==10 else 'active','activePlan':'docs/comics/biology-ten-20261117/manifest.json','updatedAt':now()})
# Quality labels become fine only after the accepted plan and all review flags exist.
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=R,check=True)
if n==10:
 for test_id in m['questionIds']+['q-969','q-912']:
  try:assert_work_allowed(R,test_id)
  except ValueError:continue
  raise AssertionError('Stop gate was not closed for '+test_id)
print(json.dumps({'id':qid,'accepted':n,'limit':10,'stopGateClosed':n==10,'integrationEventId':job['integrationEventId']},ensure_ascii=False))
