"""Record technical acceptance after producer review and formal, actually viewed pages."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import locked,load,save,now,integrated,update_display
from monitor.comic_publish import pending_batch
from monitor.comic_execution import assert_work_allowed
plan=load(D/'plan.json');scope=load(D/'execution-scope.json');all_ids=scope['newQuestionIds'];ids=sys.argv[1:] or all_ids;viewed=load(D/'integration/formal-visual-review.json')
assert len(ids)==len(set(ids)) and set(ids)<=set(all_ids)
assert set(ids)<=set(viewed['questionIds']) and viewed['actualViewed'] is True
awaiting=set(plan.get('pendingReviewQuestionIds',[])+plan.get('pendingAnswerQuestionIds',[])+plan.get('pendingOriginalMaterialQuestionIds',[]))
assert awaiting<=set(all_ids)
for qid in ids:
 assert_work_allowed(ROOT,qid)
 spec=load(ROOT/f'docs/comics/{qid}.json');validation=load(ROOT/f'docs/comics/{qid}-validation.json')
 assert {(r['standalone'],r['viewport']) for r in validation['results']}=={(s,w) for s in [False,True] for w in [1440,1120,390]}
 assert all(len(r['artImages'])==4 and len({im['src'] for im in r['artImages']})==4 and all(im['loaded'] for im in r['artImages']) and not r['overflow'] and not r['docOverflow'] and not r['wrapErrors'] and not r['protectedBreaks'] for r in validation['results'])
 shots=[f'/tmp/weirugo-comic-checks/{qid}-{v}-{w}.png' for v in ['app','standalone'] for w in [1440,390]]
 assert all(Path(p).is_file() for p in shots)
 spec['rootReview']=dict(reviewerAgent='/root/comic_lane_1',visualChecked=True,technicalIntegrationChecked=True,fourActualIndependentImages=True,desktopMobileActuallyViewed=True,screenshots=shots,inheritedProducerOriginalAndAnswerReview=spec['producerReviewPath'],inheritedWithoutRepeatedOriginalReview=True,note='製作代理已完整核對原題、答案與四圖並自驗；整合者依最新分工做完整性、去重、引用與正式桌手機版面驗收，不冒稱重做題解。',checkedAt=now(),answerOrRequiredMaterialPending=qid in awaiting)
 save(ROOT/f'docs/comics/{qid}.json',spec)
 if qid in awaiting:
  with locked(ROOT):
   pipeline=load(ROOT/'docs/comics/pipeline.json');job=next(j for j in reversed(pipeline['jobs']) if j['id']==qid);assert job['decision']=='awaiting_confirmation' and 'integrationEventId' not in job
   job.update(state='blocked',formalArtValidatedAt=now(),formalValidation=f'docs/comics/{qid}-validation.json')
   progress=load(ROOT/'docs/comics/progress.json');entry=next(e for e in progress['entries'] if e['id']==qid);entry.update(state='awaiting_confirmation',validatedImageCount=4,visualChecked=True,validationFile=f'docs/comics/{qid}-validation.json',reason='原題及四張新圖可讀，正式桌手機QA通過；原AI錯圖／內容訂正仍待使用者確認，不計complete事件。')
   save(ROOT/'docs/comics/progress.json',progress);save(ROOT/'docs/comics/pipeline.json',pipeline)
 else:
  job=integrated(ROOT,qid);plan.setdefault('integrationEvents',[]).append(dict(id=qid,integrationEventId=job['integrationEventId'],integratedAt=job['integratedAt']))
 plan.setdefault('validatedFourImageQuestionIds',[]).append(qid)
 execution=load(D/'execution-progress.json');key='awaitingConfirmationQuestionIds' if qid in awaiting else 'completedQuestionIds';execution.setdefault(key,[]).append(qid);save(D/'execution-progress.json',execution)
_,_,_,publication_pending=pending_batch();execution=load(D/'execution-progress.json');complete=execution['completedQuestionIds'];pending=execution['awaitingConfirmationQuestionIds'];ts=now();checked=len(plan['validatedFourImageQuestionIds']);total=len(all_ids);finished=checked==total
with locked(ROOT):
 execution.update(state=('awaiting_confirmation' if pending else 'complete') if finished else 'active');execution.update({'stoppedAt':ts} if finished else {});save(D/'execution-progress.json',execution)
 plan.update(state=execution['state'],productionStopped=finished,stage=('four_images_published_with_pending_review' if pending else 'complete') if finished else 'source_four_image_integration',completedFourImageQuestionIds=complete,completedOriginalQuestionCount=len(complete),validatedIllustrationCount=4*checked,illustrationsOutstanding=4*(total-checked),pendingPublicationEvents=len(publication_pending),updatedAt=ts);save(D/'plan.json',plan)
 gp=load(ROOT/'docs/imports/more-gpt-progress.json');row=next(s for s in gp['sources'] if s.get('sourceId')==scope['sourceId']);row.update(state='complete' if finished and not pending else 'partial',sourceCurationComplete=finished and not pending,contentCurationComplete=finished and not pending,validatedFourImageQuestionIds=plan['validatedFourImageQuestionIds'],fourImageQuestionIds=complete,pendingFourImageQuestionIds=pending,newIllustrationCount=4*checked,requiredIllustrationCount=4*total,illustrationsOutstanding=4*(total-checked),teachingComicState=('complete_with_pending_review' if pending else 'complete') if finished else 'partial',reason=f'本次{total}指定原問；已驗收{checked}題、{4*checked}張新圖與正式桌手機版面，{len(complete)}題正式完成，{len(pending)}題訂正待確認，不計complete事件。');gp['updatedAt']=ts;save(ROOT/'docs/imports/more-gpt-progress.json',gp)
 if finished:
  pointer=load(ROOT/'monitor/new-source-authorization.json');pointer.update(state='closed',closedAt=ts);save(ROOT/'monitor/new-source-authorization.json',pointer)
  priority=load(ROOT/'monitor/priority-source.json');priority.update(state='paused' if pending else 'complete',updatedAt=ts);save(ROOT/'monitor/priority-source.json',priority)
  pipeline=load(ROOT/'docs/comics/pipeline.json');pipeline.update(claimsPaused=True,pauseReason='第73來源製作已收尾；待確認不計complete，舊來源與重製持續暫停。',pausedAt=ts);save(ROOT/'docs/comics/pipeline.json',pipeline)
  display=load(ROOT/'monitor/parallel.json');display['rootRole']='第73來源原題與48張四圖已驗版；待確認個別保留，所有舊佇列維持暫停。'
  for lane in display['lanes']:lane.update(claimsPaused=True,batchQuestionIds=[],activeTask=None,pauseReason=pipeline['pauseReason'])
  save(ROOT/'monitor/parallel.json',display);update_display(ROOT,pipeline)
 save(ROOT/'monitor/activity.json',dict(title=f'第73來源：{checked}／{total}原題四圖驗版，{len(complete)}題完成、{len(pending)}題待核',detail=f'12張原卷、80訊息已保存；{checked*4}張自製獨立圖及正式桌手機版面均通過。待確認不計complete事件，累計{len(publication_pending)}件未發布；舊佇列保持暫停。',stage=('source_pending_confirmation' if pending else 'source_completed') if finished else 'source_four_image_integration',goalStatus=('review' if pending else 'done') if finished else 'running',activePlan=str((D/'plan.json').relative_to(ROOT)),updatedAt=ts))
print(json.dumps(dict(completedQuestionIds=complete,awaitingConfirmationQuestionIds=pending,pendingPublicationEvents=len(publication_pending)),ensure_ascii=False))
