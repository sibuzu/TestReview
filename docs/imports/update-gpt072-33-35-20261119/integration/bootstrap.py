"""Freeze exactly two user-requested existing question updates; never restart source72."""
import hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,now,locked,update_display
from monitor.comic_execution import authorized_question_update,assert_work_allowed
from monitor.comic_publish import pending_batch
ids=['q-1153','q-1154'];C=ROOT/'.cache/update-gpt072-33-35';C.mkdir(exist_ok=True)
assert not (D/'execution-scope.json').exists()
(C/'baseline-data.json').write_bytes((ROOT/'site/dist/data.json').read_bytes())
bank=load(C/'baseline-data.json');questions={q['id']:q for q in bank['questions']};assert len(questions)==969
snap=D/'before';snap.mkdir(exist_ok=True)
for qid in ids:
 for directory in ['docs/complete-questions','docs/comics']:
  p=ROOT/directory/f'{qid}.json';dest=snap/directory/f'{qid}.json';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
 for p in (ROOT/'docs/comics/art').glob(f'{qid}-panel-*.svg'):
  dest=snap/'art'/p.name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(p.read_bytes())
# Save current pending-card snapshots before material is filled and cards resolved.
confirmations=load(ROOT/'monitor/confirmations.json');save(snap/'confirmation-requests.json',[r for r in confirmations['requests'] if r.get('questionId') in ids])
_,_,_,events=pending_batch();save(D/'publication-baseline.json',dict(checkedAt=now(),pendingEventIds=[j['integrationEventId'] for j in events],count=len(events)))
for filename,key in [('docs/imports/more-gpt-progress.json','sources'),('docs/comics/progress.json','entries'),('docs/comics/pipeline.json','jobs')]:
 rows=load(ROOT/filename)[key];save(snap/(Path(filename).stem+'-target-records.json'),[r for r in rows if r.get('id') in ids or r.get('sourceId')=='src-more-072'])
acq=D/'acquisition.json';record=load(acq);assert record['state']=='acquired' and len(record['downloadedImages'])==2
scope=dict(version=1,kind='explicit_question_update',authorizedBy='user_update',sourceId='src-more-072',url=record['url'],questionIds=ids,noNewQuestions=True,baselineQuestions={q:{k:questions[q][k] for k in ['id','sourceId','date']} for q in ids},originalsVisualChecked=True,existingQuestionIdentityChecked=True,expectedOriginalImages=2,acquisitionPath=str(acq.relative_to(ROOT)),acquisitionSHA256=hashlib.sha256(acq.read_bytes()).hexdigest(),intent='使用者要求update33-35題組圖片；只補既有錯題33及35共同文與原圖，不加入正常作答34、不恢復其他佇列。')
save(D/'execution-scope.json',scope);save(D/'execution-progress.json',dict(state='active',sourceId='src-more-072',completedQuestionIds=[],startedAt=now()))
with locked(ROOT):
 save(ROOT/'monitor/question-update-authorization.json',dict(state='active',sourceId='src-more-072',url=record['url'],scopePath=str((D/'execution-scope.json').relative_to(ROOT)),scopeSHA256=hashlib.sha256((D/'execution-scope.json').read_bytes()).hexdigest(),progressPath=str((D/'execution-progress.json').relative_to(ROOT)),activatedAt=now()))
 save(ROOT/'monitor/priority-source.json',dict(kind='explicit_question_update',state='active',sourceId='src-more-072',url=record['url'],questionIds=ids,plan=str((D/'execution-scope.json').relative_to(ROOT)),note='只補原卷33、35共同閱讀與圖片；34不新增、舊佇列不恢復。',updatedAt=now()))
 display=load(ROOT/'monitor/parallel.json');lane=next(l for l in display['lanes'] if l['lane']==1);lane.update(claimsPaused=False,activeTask=dict(state='integrating',title='補第33、35題共同閱讀原圖與缺文核對',startedAt=now()));display['rootRole']='只更新q-1153/q-1154共同原卷；其他舊工作維持暫停。';save(ROOT/'monitor/parallel.json',display);update_display(ROOT,load(ROOT/'docs/comics/pipeline.json'))
 save(ROOT/'monitor/activity.json',dict(title='補第33、35題題組原圖與共同閱讀',detail='新分享是第72來源的補充，2張原圖已取得；僅更新既有q-1153/q-1154，保留題號及11/17日期，不新增正常作答第34題。',stage='explicit_question_update',goalStatus='running',activePlan=str((D/'execution-scope.json').relative_to(ROOT)),updatedAt=now()))
for qid in ids:assert_work_allowed(ROOT,qid)
assert not authorized_question_update(ROOT,'q-1155')
try:assert_work_allowed(ROOT,'q-1155')
except ValueError:pass
else:raise AssertionError('Old queue unexpectedly allowed')
save(D/'scope-validation.json',dict(passed=True,checkedAt=now(),allowedQuestionIds=ids,oldQuestionDenied='q-1155',pendingPublicationEvents=len(events)))
print(json.dumps(dict(allowed=ids,oldQuestionDenied=True,pendingPublicationEvents=len(events))))
