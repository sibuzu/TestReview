"""Register only the current explicitly delivered source; old queues stay paused."""
import datetime, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import locked,load,save,now,update_display
from monitor.comic_publish import pending_batch
D=Path(__file__).resolve().parents[1];sid='src-more-073';url='https://chatgpt.com/share/6aff02c8-3e8c-83ec-ba50-ab1ab4a030a5'
acq=load(D/'acquisition.json');bank=load(ROOT/'site/dist/data.json');ts=now()
assert acq['state']=='acquired' and len(acq['downloadedImages'])==acq['imagesExpected']==12
_,_,_,pending=pending_batch()
save(D/'publication-baseline.json',dict(checkedAt=ts,baselineEventIds=[j['integrationEventId'] for j in pending],pendingEventCount=len(pending)))
ids=[f'q-{n}' for n in range(1157,1169)];assert not set(ids)&{q['id'] for q in bank['questions']}
reservations=[]
for qid,im in zip(ids,acq['downloadedImages']):
 reservations.append(dict(candidateId=qid,assignedProducer='lane2' if im['index']<=6 else 'lane3',imageIndices=[im['index']],messageIndex=im['messageIndex'],messageId=im['messageId'],firstQuestionTimestamp=im['firstQuestionTimestamp'],date='2026-11-19',intakeLabel=im['userText'],state='reserved_pending_dedupe',duplicatePolicy='同題沿用既有ID與最早日期；若重複保留空號，不搬動後續。'))
save(D/'qid-reservations.json',dict(sourceId=sid,candidateRange=[ids[0],ids[-1]],reservedAt=ts,nextUnallocatedId='q-1169',items=reservations))
plan=dict(kind='explicit_new_source',state='active',sourceId=sid,order=73,url=url,title=acq['title'],worknerdTaskId='t_bb5243ec763a4bd08696',startedAt=ts,questionIds=ids,candidateQuestionIds=ids,newQuestionIds=[],publishedQuestionIds=[],originalsExpected=12,originalsAvailable=12,requiredImagesPerOriginal=4,oldBiologyResume=False,oldOtherReworkResume=False,baselineQuestionPageCount=len(bank['questions']),baselineOriginalQuestionCount=sum(len(q.get('groupQuestions') or [q]) for q in bank['questions']),baselineCommit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),baselinePendingPublicationEvents=len(pending),acquisitionMethod='user_authorized_Windows_Chrome_CDP_no_Playwright',note='12張真正User原卷已取回且已由root逐張實開；兩製作線核對指定題、跨來源查重及新四圖。未指定鄰題與來源AI圖不收入。舊佇列不恢復。',archiveMessages=80,candidateOriginalQuestionCount=12,acquisition=str((D/'acquisition.json').relative_to(ROOT)),qidReservations=str((D/'qid-reservations.json').relative_to(ROOT)),stage='source_curation',validatedFourImageQuestionIds=[],completedFourImageQuestionIds=[],integrationEvents=[],pendingOriginalMaterialQuestionIds=[],pendingAnswerQuestionIds=[],validatedIllustrationCount=0,illustrationsOutstanding=48)
save(D/'plan.json',plan)
save(D/'execution-progress.json',dict(state='preparing',sourceId=sid,completedQuestionIds=[],awaitingConfirmationQuestionIds=[],createdAt=ts))
monitor_plan=dict(kind='explicit_new_source',showAgents=True,expectedOriginalQuestions=12,duplicateQuestionIds=[],sources=[dict(key='gpt073',batch='gpt',suggestedOrder=73,sourceId=sid,url=url,questionIds=ids,expectedOriginalQuestions=12,acquisitionRecord=str((D/'acquisition.json').relative_to(ROOT)))],note='只處理本次新分享12個指定原問；原卷已取得，新四圖及逐題QA整理中。')
save(D/'monitor-plan.json',monitor_plan)
with locked(ROOT):
 gp=load(ROOT/'docs/imports/more-gpt-progress.json');assert not any(s.get('order')==73 or s.get('url')==url for s in gp['sources'])
 gp['sources'].append(dict(order=73,sourceId=sid,url=url,title=acq['title'],state='partial',archiveImages=12,downloadedImages=acq['downloadedImages'],questionIds=[],newQuestionIds=[],createdDate='2026-11-19',acquisitionRecord=str((D/'acquisition.json').relative_to(ROOT)),sourceCurationComplete=False,contentCurationComplete=False,reason='原圖與對話已取回；只核對使用者指定12原問，跨來源去重及每新題四圖製作中。',requiredIllustrationCount=48,newIllustrationCount=0,illustrationsOutstanding=48))
 gp.update(totalLinks=len(gp['sources']),uniqueLinks=len({s['url'] for s in gp['sources']}),updatedAt=ts);save(ROOT/'docs/imports/more-gpt-progress.json',gp)
 todo=ROOT/'todo/more_gpt.md';text=todo.read_text();assert url not in text;todo.write_text(text.rstrip()+'\n'+url+'\n')
 save(ROOT/'monitor/active-source-plan.json',dict(path=str((D/'monitor-plan.json').relative_to(ROOT)),updatedAt=ts))
 save(ROOT/'monitor/priority-source.json',dict(kind='explicit_new_source',state='active',sourceId=sid,url=url,plan=str((D/'plan.json').relative_to(ROOT)),questionIds=ids,laneAssignments={'1':[],'2':ids[:6],'3':ids[6:]},note='本批12指定原問整理中；舊佇列持續暫停。',updatedAt=ts))
 display=load(ROOT/'monitor/parallel.json');display['rootRole']='第73來源12張原卷已取回；Agent2/3各自核對六題與四圖，Agent1唯一技術整合。'
 for lane in display['lanes']:
  n=lane['lane'];lane.update(claimsPaused=False,batchQuestionIds=ids[:6] if n==2 else ids[6:] if n==3 else [],activeTask=dict(state='curating' if n!=1 else 'preparing',title='第73來源原卷、原題與四圖整理' if n!=1 else '第73來源接稿、凍結去重及技術整合',startedAt=ts))
  lane.pop('pauseReason',None)
 save(ROOT/'monitor/parallel.json',display);update_display(ROOT,load(ROOT/'docs/comics/pipeline.json'))
 save(ROOT/'monitor/activity.json',dict(title='第73來源：12張原卷取得，逐題核對與四圖製作中',detail='80訊息與12張1080×1440真正User原卷已保存；Agent2/3各處理六個指定原問，Agent1依次技術收入。原有暫停工作未恢復。',stage='source_curation',goalStatus='running',activePlan=str((D/'plan.json').relative_to(ROOT)),updatedAt=ts))
print(json.dumps(dict(sourceId=sid,candidates=ids,baselinePages=len(bank['questions']),pendingPublicationEvents=len(pending)),ensure_ascii=False))
