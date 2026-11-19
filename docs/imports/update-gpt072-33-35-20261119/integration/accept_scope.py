"""Accept only a frozen update's named jobs, then close its independent gate."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,locked,now,integrated,update_display
from monitor.comic_execution import assert_work_allowed
from monitor.comic_publish import pending_batch
D=(ROOT/sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
scope=load(D/'execution-scope.json');ids=scope['questionIds'];review=load(D/'formal-review.json');assert review['actualViewedOrUnchangedApprovedArtifacts'] and set(review['questionIds'])==set(ids)
events=[]
for qid in ids:
 assert_work_allowed(ROOT,qid);v=load(ROOT/f'docs/comics/{qid}-validation.json');assert len(v['results'])==6 and all(not r['overflow'] and not r['docOverflow'] and not r['wrapErrors'] and all(im['loaded'] for im in r['artImages']) for r in v['results'])
 spec=load(ROOT/f'docs/comics/{qid}.json');spec.update(visualChecked=True,checkedAt=now());spec['rootReview'].update(visualChecked=True,answerOrRequiredMaterialPending=False,updateScope=str((D/'execution-scope.json').relative_to(ROOT)),updateReview=str((D/'formal-review.json').relative_to(ROOT)),note=review['note'],checkedAt=now());save(ROOT/f'docs/comics/{qid}.json',spec)
 job=integrated(ROOT,qid);events.append(dict(id=qid,integrationEventId=job['integrationEventId'],integratedAt=job['integratedAt']))
 progress=load(D/'execution-progress.json');assert qid not in progress['completedQuestionIds'];progress['completedQuestionIds'].append(qid);save(D/'execution-progress.json',progress)
_,_,_,pending_events=pending_batch();bank=load(ROOT/'site/dist/data.json');questions={q['id']:q for q in bank['questions']};confirmations=load(ROOT/'monitor/confirmations.json')
with locked(ROOT):
 gp=load(ROOT/'docs/imports/more-gpt-progress.json');row=next(r for r in gp['sources'] if r.get('sourceId')==scope['sourceId']);source_ids=set(row['questionIds']);current_pending={q['id'] for q in questions.values() if q['id'] in source_ids and (q.get('verification') in ['待核對','待補原題'] or q.get('contentStatus')=='待更新')};current_pending.update(r.get('questionId') or r['id'] for r in confirmations['requests'] if r.get('state')=='pending' and (r.get('questionId') or r['id']) in source_ids)
 for key in ['pendingOriginalMaterialQuestionIds','pendingAnswerQuestionIds','pendingFourImageQuestionIds']:
  if key in row:row[key]=[q for q in row[key] if q not in ids]
 row['fourImageQuestionIds']=list(dict.fromkeys(row.get('fourImageQuestionIds',[])+ids));row.update(state='partial' if current_pending else 'complete',sourceCurationComplete=not current_pending,contentCurationComplete=not current_pending,teachingComicState='complete_with_pending_review' if current_pending else 'complete',pendingContentQuestionIds=sorted(current_pending),reason=('指定補文／確認已同步，仍保留未解資料：'+ '、'.join(sorted(current_pending))) if current_pending else '所有指定原題、既有四圖及監看確認均已同步完成；保留原題ID、首次日期與必要條件限制。');gp['updatedAt']=now();save(ROOT/'docs/imports/more-gpt-progress.json',gp)
 plan_path=ROOT/row.get('plan',f'docs/imports/new-gpt-20261119-73/plan.json');plan=load(plan_path)
 for key in ['pendingOriginalMaterialQuestionIds','pendingAnswerQuestionIds','pendingReviewQuestionIds','fourImageValidatedPendingQuestionIds','pendingQuestionReviewIds']:
  if key in plan:plan[key]=[q for q in plan[key] if q not in ids]
 plan['completedFourImageQuestionIds']=list(dict.fromkeys(plan.get('completedFourImageQuestionIds',[])+ids));plan['integrationEvents']=plan.get('integrationEvents',[])+events;plan.update(state='awaiting_confirmation' if current_pending else 'complete',productionStopped=True,completedOriginalQuestionCount=len(plan['completedFourImageQuestionIds']),pendingContentQuestionIds=sorted(current_pending),pendingPublicationEvents=len(pending_events),lastMaterialOrConfirmationUpdate=str(D.relative_to(ROOT)),updatedAt=now());save(plan_path,plan)
 old_execution=plan_path.parent/'execution-progress.json'
 if old_execution.exists():
  ex=load(old_execution);ex['completedQuestionIds']=list(dict.fromkeys(ex.get('completedQuestionIds',[])+ids));ex['awaitingConfirmationQuestionIds']=[q for q in ex.get('awaitingConfirmationQuestionIds',[]) if q not in ids];ex.update(state='awaiting_confirmation' if current_pending else 'complete',updatedByExplicitScope=str((D/'execution-scope.json').relative_to(ROOT)));save(old_execution,ex)
 execution=load(D/'execution-progress.json');execution.update(state='complete',completedAt=now(),integrationEvents=events);save(D/'execution-progress.json',execution)
 pointer=load(ROOT/'monitor/question-update-authorization.json');assert pointer['scopePath']==str((D/'execution-scope.json').relative_to(ROOT));pointer.update(state='closed',closedAt=now());save(ROOT/'monitor/question-update-authorization.json',pointer)
 priority=load(ROOT/'monitor/priority-source.json');priority.update(state='complete',updatedAt=now());save(ROOT/'monitor/priority-source.json',priority)
 display=load(ROOT/'monitor/parallel.json');lane=next(l for l in display['lanes'] if l['lane']==1);lane.update(claimsPaused=True,activeTask=None,pauseReason='本次狹義更新完成；其他舊佇列維持暫停。');save(ROOT/'monitor/parallel.json',display);update_display(ROOT,load(ROOT/'docs/comics/pipeline.json'))
 save(ROOT/'monitor/activity.json',dict(title='指定題目更新已完成：'+ '、'.join(ids),detail='完整原題／原圖與既有四圖已核對；僅完成本次白名單，原題ID、來源與日期保留。其他未補資料不猜補。',stage='question_update_complete',goalStatus='running',activePlan=str((D/'execution-scope.json').relative_to(ROOT)),updatedAt=now()))
save(D/'acceptance.json',dict(passed=True,acceptedAt=now(),questionIds=ids,integrationEvents=events,scopeClosed=True,sourceRemainingQuestionIds=sorted(current_pending),pendingPublicationEvents=len(pending_events)))
print(json.dumps(dict(accepted=ids,scopeClosed=True,sourceRemaining=sorted(current_pending),pendingPublicationEvents=len(pending_events)),ensure_ascii=False))
