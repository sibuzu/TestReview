"""Sole integrator acceptance after actual independent original/art/formal review."""
from pathlib import Path
import argparse, json, subprocess, sys

R=Path(__file__).resolve().parents[3];D=Path(__file__).parent;sys.path.insert(0,str(R))
from monitor.comic_pipeline import integrated, locked, load, save, update_display, now
from monitor.comic_execution import assert_work_allowed
from monitor.comic_publish import pending_batch

p=argparse.ArgumentParser(description=__doc__);p.add_argument('id');p.add_argument('--note',required=True)
p.add_argument('--awaiting-confirmation',action='store_true');a=p.parse_args();qid=a.id
assert_work_allowed(R,qid)
scope=load(D/'execution-scope.json');plan=load(D/'plan.json')
pending=set(plan.get('pendingOriginalMaterialQuestionIds',[])+plan.get('pendingAnswerQuestionIds',[]))
assert a.awaiting_confirmation==(qid in pending), 'Pending material/answer cannot be accepted as complete.'
validation=load(R/f'docs/comics/{qid}-validation.json')
assert {(r['standalone'],r['viewport']) for r in validation['results']}=={(v,w) for v in [False,True] for w in [1440,1120,390]}
assert all(len(r['artImages'])==4 and len({im['src'] for im in r['artImages']})==4 and all(im['loaded'] for im in r['artImages']) and not r['overflow'] and not r['docOverflow'] and not r['wrapErrors'] and not r['protectedBreaks'] for r in validation['results'])
shots=[f'/tmp/weirugo-comic-checks/{qid}-{v}-{w}.png' for v in ['app','standalone'] for w in [1440,390]]
assert all(Path(p).is_file() for p in shots)
question=next(q for q in load(R/'site/dist/data.json')['questions'] if q['id']==qid)
if qid in plan.get('pendingOriginalMaterialQuestionIds',[]):
 assert question['contentStatus']=='待更新' and question.get('reviewQuestions') and '待核' in question['verification']
spec=load(R/f'docs/comics/{qid}.json')
spec['rootReview']={'reviewerAgent':'/root/comic_lane_1','visualChecked':True,'originalVisualChecked':True,'answerAndExplanationChecked':True,'fourActualIndependentImages':True,'desktopMobileActuallyViewed':True,'screenshots':shots,'originalMaterials':[str(R/'site/dist'/p) for p in question.get('images',[])]+[str(R/'site/dist'/f['src']) for f in question.get('questionFigures',[])],'note':a.note,'checkedAt':now(),'answerOrRequiredMaterialPending':a.awaiting_confirmation}
save(R/f'docs/comics/{qid}.json',spec)
latest=next(j for j in reversed(load(R/'docs/comics/pipeline.json')['jobs']) if j['id']==qid)
assert latest['jobId']==load(D/'prepared-jobs.json')[qid]['jobId']
assert latest['decision']==('awaiting_confirmation' if a.awaiting_confirmation else 'complete')
if a.awaiting_confirmation:
 # Preserve the formally checked artwork without creating any integration event.
 with locked(R):
  pipeline=load(R/'docs/comics/pipeline.json');job=next(j for j in pipeline['jobs'] if j.get('jobId')==latest['jobId'])
  assert 'integrationEventId' not in job
  job.update(state='blocked',formalArtValidatedAt=now(),formalValidation=f'docs/comics/{qid}-validation.json')
  progress=load(R/'docs/comics/progress.json');entry=next(e for e in progress['entries'] if e['id']==qid)
  entry.update(state='awaiting_confirmation',validatedImageCount=4,visualChecked=True,validationFile=f'docs/comics/{qid}-validation.json',reason='四圖與正式桌手機QA通過；原題必要材料/單選條件待核，不產生complete整合事件。')
  save(R/'docs/comics/progress.json',progress);save(R/'docs/comics/pipeline.json',pipeline);update_display(R,pipeline)
else:
 job=latest if latest['state']=='integrated' else integrated(R,qid)

_,_,_,publication_pending=pending_batch()
with locked(R):
 execution=load(D/'execution-progress.json');key='awaitingConfirmationQuestionIds' if a.awaiting_confirmation else 'completedQuestionIds'
 assert qid not in execution.get(key,[]);execution.setdefault(key,[]).append(qid)
 plan=load(D/'plan.json');validated=plan.setdefault('validatedFourImageQuestionIds',[])
 assert qid not in validated;validated.append(qid)
 plan['completedFourImageQuestionIds']=execution['completedQuestionIds'][:]
 if not a.awaiting_confirmation:
  plan.setdefault('integrationEvents',[]).append({'id':qid,'integrationEventId':job['integrationEventId'],'integratedAt':job['integratedAt']})
 complete=len(execution['completedQuestionIds']);awaiting=len(execution['awaitingConfirmationQuestionIds']);checked=len(validated);total=len(scope['newQuestionIds'])
 plan.update(validatedIllustrationCount=4*checked,completedOriginalQuestionCount=complete,illustrationsOutstanding=4*(total-checked),pendingPublicationEvents=len(publication_pending),updatedAt=now())
 gp=load(R/'docs/imports/more-gpt-progress.json');source=next(s for s in gp['sources'] if s.get('sourceId')==scope['sourceId'])
 source.update(state='partial',contentCurationComplete=False,validatedFourImageQuestionIds=validated[:],fourImageQuestionIds=execution['completedQuestionIds'][:],newIllustrationCount=4*checked,requiredIllustrationCount=4*total,illustrationsOutstanding=4*(total-checked),pendingFourImageQuestionIds=execution['awaitingConfirmationQuestionIds'][:],teachingComicState='partial')
 if checked==total:
  assert complete+awaiting==total and set(validated)==set(scope['newQuestionIds'])
  execution.update(state='awaiting_confirmation' if awaiting else 'complete',stoppedAt=now())
  plan.update(state='awaiting_confirmation' if awaiting else 'complete',stage='four_images_published_with_pending_review' if awaiting else 'complete',productionStopped=True)
  source.update(teachingComicState='complete_with_pending_review' if awaiting else 'complete')
  if not awaiting:source.update(state='complete',contentCurationComplete=True)
  pointer=load(R/'monitor/new-source-authorization.json');pointer.update(state='closed',closedAt=now());save(R/'monitor/new-source-authorization.json',pointer)
  pipeline=load(R/'docs/comics/pipeline.json');pipeline.update(claimsPaused=True,pauseReason='第72來源新題四圖已驗版；待核題不計complete，其餘舊重製持續暫停。',pausedAt=now());save(R/'docs/comics/pipeline.json',pipeline)
  priority=load(R/'monitor/priority-source.json');priority.update(state='paused',updatedAt=now());save(R/'monitor/priority-source.json',priority)
  display=load(R/'monitor/parallel.json')
  for lane in display['lanes']:
   lane.update(claimsPaused=True,batchQuestionIds=[],activeTask=None)
   if lane['lane']!=2:lane['pauseReason']=pipeline['pauseReason']
  display['rootRole']='第72來源21新題四圖已驗版，待核題保留、不計complete事件；全部製作領題已停，其他舊重製持續暫停。'
  save(R/'monitor/parallel.json',display);update_display(R,pipeline)
 save(D/'execution-progress.json',execution);save(D/'plan.json',plan);gp['updatedAt']=now();save(R/'docs/imports/more-gpt-progress.json',gp)
 save(R/'monitor/activity.json',{'title':f'第72來源：{checked}／{total}新題四圖驗版，{complete}題正式完成、{awaiting}題待核','detail':f'剛驗收{qid}。原題/原圖與四張正式桌手機成品已實看；待確認不計complete事件，前批10事件持續累計，每20正常發布。舊19生物+46其他/Agent2保持暫停。','stage':'source_four_image_review' if checked<total else 'source_pending_confirmation','goalStatus':'running' if checked<total else 'review','activePlan':str((D/'plan.json').relative_to(R)),'updatedAt':now()})
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=R,check=True)
print(json.dumps({'id':qid,'validated':checked,'completedEvents':complete,'awaiting':awaiting,'stopped':checked==total},ensure_ascii=False))
