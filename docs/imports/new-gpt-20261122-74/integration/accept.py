"""Record source 74 acceptance after root has actually viewed formal QA."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];B=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,now,integrated,locked,update_display
from monitor.comic_publish import pending_batch
ids=[f'q-{n}' for n in range(1169,1179)];pending={'q-1176','q-1178'}
view=load(B/'integration/formal-visual-review.json')
assert view['actualViewed'] and view['questionIds']==ids
plan=load(B/'plan.json');plan['integrationEvents']=[]
for qid in ids:
 spec=load(ROOT/f'docs/comics/{qid}.json');v=load(ROOT/f'docs/comics/{qid}-validation.json')
 assert {(r['standalone'],r['viewport']) for r in v['results']}=={(s,w) for s in [False,True] for w in [1440,1120,390]}
 assert all(len(r['artImages'])==4 and len({i['src'] for i in r['artImages']})==4 and all(i['loaded'] for i in r['artImages']) and not r['overflow'] and not r['docOverflow'] and not r['wrapErrors'] and not r['protectedBreaks'] for r in v['results'])
 shots=[f'/tmp/weirugo-comic-checks/{qid}-{s}-{w}.png' for s in ['app','standalone'] for w in [1440,390]]
 assert all(p in view['screenshots'] and Path(p).is_file() for p in shots)
 spec.update(visualChecked=True,checkedAt=now(),validationFile=f'docs/comics/{qid}-validation.json',rootReview=dict(reviewerAgent='/root',visualChecked=True,technicalIntegrationChecked=True,fourActualIndependentImages=True,desktopMobileActuallyViewed=True,screenshots=shots,originalsAlsoViewed=True,substantiveExplanationReviewPending=qid in pending,checkedAt=now()))
 save(ROOT/f'docs/comics/{qid}.json',spec)
 if qid in pending:
  with locked(ROOT):
   pipe=load(ROOT/'docs/comics/pipeline.json');job=next(j for j in pipe['jobs'] if j['id']==qid);assert job['state']=='blocked' and 'integrationEventId' not in job
   job.update(formalArtValidatedAt=now(),formalValidation=f'docs/comics/{qid}-validation.json',reason='完整原題、四張新圖與正式app/單頁桌手機QA通過；原AI選項解說訂正待monitor確認，答案不變，待確認不計complete事件。');save(ROOT/'docs/comics/pipeline.json',pipe)
   progress=load(ROOT/'docs/comics/progress.json');entry=next(e for e in progress['entries'] if e['id']==qid);entry.update(state='awaiting_confirmation',validatedImageCount=4,visualChecked=True,validationFile=f'docs/comics/{qid}-validation.json',reason=job['reason']);save(ROOT/'docs/comics/progress.json',progress)
 else:
  job=integrated(ROOT,qid);plan['integrationEvents'].append(dict(id=qid,integrationEventId=job['integrationEventId'],integratedAt=job['integratedAt']))
 execution=load(B/'execution-progress.json');execution['awaitingConfirmationQuestionIds' if qid in pending else 'completedQuestionIds'].append(qid);save(B/'execution-progress.json',execution)
_,_,_,pub=pending_batch();ts=now();complete=[i for i in ids if i not in pending]
execution.update(state='awaiting_confirmation',stoppedAt=ts);save(B/'execution-progress.json',execution)
plan.update(state='awaiting_confirmation',productionStopped=True,stage='four_images_published_with_pending_review',newQuestionIds=ids,publishedQuestionIds=ids,validatedFourImageQuestionIds=ids,completedFourImageQuestionIds=complete,pendingReviewQuestionIds=sorted(pending),pendingAnswerQuestionIds=[],pendingOriginalMaterialQuestionIds=[],validatedIllustrationCount=40,illustrationsOutstanding=0,completedOriginalQuestionCount=8,pendingPublicationEvents=len(pub),updatedAt=ts);save(B/'plan.json',plan)
gp=load(ROOT/'docs/imports/more-gpt-progress.json');row=next(s for s in gp['sources'] if s.get('sourceId')=='src-more-074')
row.update(state='partial',sourceCurationComplete=False,contentCurationComplete=False,questionIds=ids,newQuestionIds=ids,newOriginalQuestionCount=10,newQuestionPageCount=10,questionPageCount=10,validatedFourImageQuestionIds=ids,fourImageQuestionIds=complete,pendingFourImageQuestionIds=sorted(pending),newIllustrationCount=40,requiredIllustrationCount=40,illustrationsOutstanding=0,teachingComicState='complete_with_pending_review',pendingContentQuestionIds=sorted(pending),reason='10個指定原問與40張自製圖已收入並通過正式桌手機QA；8題完成，q1176/q1178原AI選項解說訂正待monitor確認，答案A/D不變。未確認不計complete事件；舊工作保持暫停。');gp['updatedAt']=ts;save(ROOT/'docs/imports/more-gpt-progress.json',gp)
sources=load(ROOT/'docs/additional-sources.json');source=next(s for s in sources if s['id']=='src-more-074');source.update(status='read',note=row['reason']);save(ROOT/'docs/additional-sources.json',sources)
pointer=load(ROOT/'monitor/new-source-authorization.json');pointer.update(state='closed',closedAt=ts);save(ROOT/'monitor/new-source-authorization.json',pointer)
pipe=load(ROOT/'docs/comics/pipeline.json');pipe.update(claimsPaused=True,pauseReason='本次第74來源製作與正式QA完成；2項訂正待monitor確認，其餘舊工作維持暫停。');save(ROOT/'docs/comics/pipeline.json',pipe);update_display(ROOT,pipe)
display=load(ROOT/'monitor/parallel.json');display['rootRole']='第74來源10完整原題/40張新圖已發布；2項解說訂正待monitor確認，舊暫停角色不恢復。'
for lane in display['lanes']:lane.update(claimsPaused=True,batchQuestionIds=[],activeTask=None)
save(ROOT/'monitor/parallel.json',display)
save(ROOT/'monitor/activity.json',dict(title='第74來源：10題／40張新圖已驗證，2項解說訂正待確認',detail='979題面；73則訊息與10張原卷已保存，歷史11/21、地科11/22首次提問日期保留。q1176/1178原AI選項解說錯誤附完整原題及前後差異，答案仍A/D。8題計complete、2題不計；舊暫停工作不恢復。',stage='source_pending_confirmation',goalStatus='review',activePlan=str((B/'plan.json').relative_to(ROOT)),updatedAt=ts))
receipt=load(B/'integrated.json')
for item in receipt['items']:item.update(fourImageState='validated_awaiting_confirmation' if item['id'] in pending else 'complete',formalValidation=f"docs/comics/{item['id']}-validation.json")
save(B/'integrated.json',receipt)
print(json.dumps(dict(completedQuestionIds=complete,awaitingConfirmationQuestionIds=sorted(pending),pendingPublicationEvents=len(pub))))
