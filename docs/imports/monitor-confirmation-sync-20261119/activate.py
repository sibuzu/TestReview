"""Activate one already-resolved monitor instruction; no source or queue resumption."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent;sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,locked,now,update_display
from monitor.comic_execution import assert_work_allowed
qid=sys.argv[1];mapping={'q-1122':('q-1122','docs/acquisition/new-gpt-20261116-71.json'),'q-1135':('correction-q-1135-dbb2272b4b03','docs/imports/new-gpt-20261117-72/acquisition.json'),'q-1168':('correction-q-1168-cbcb504cd143','docs/imports/new-gpt-20261119-73/acquisition.json')};requestid,acqpath=mapping[qid];D=BASE/qid;D.mkdir(exist_ok=True)
assert load(ROOT/'monitor/question-update-authorization.json')['state']=='closed'
assert not (D/'execution-scope.json').exists()
bank=load(ROOT/'site/dist/data.json');q=next(q for q in bank['questions'] if q['id']==qid);spec=load(ROOT/f'docs/comics/{qid}.json');records=load(ROOT/'monitor/confirmations.json');record=next(r for r in records['resolved'] if r['id']==requestid);assert record['state']=='resolved' and (record.get('questionId') or record['id'])==qid
C=ROOT/'.cache/monitor-confirmation-sync-20261119';C.mkdir(exist_ok=True);(C/(qid+'-baseline-data.json')).write_bytes((ROOT/'site/dist/data.json').read_bytes())
save(D/'before-question.json',q);save(D/'before-spec.json',spec);save(D/'confirmation-snapshot.json',record)
images=[p['image'] for p in spec['panels']]+[spec['fourth']['image']];save(D/'before-art-hashes.json',[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in images])
for p in images:
 if Path(p).suffix=='.svg':dest=D/'before-art'/Path(p).name;dest.parent.mkdir(exist_ok=True);dest.write_bytes((ROOT/p).read_bytes())
acq=load(ROOT/acqpath);assert acq['state']=='acquired' and acq['sourceId']==q['sourceId'];save(D/'acquisition.json',acq)
scope=dict(version=1,kind='explicit_question_update',authorizedBy='monitor_confirmation',sourceId=q['sourceId'],url=acq['url'],questionIds=[qid],noNewQuestions=True,baselineQuestions={qid:{k:q[k] for k in ['id','sourceId','date']}},originalsVisualChecked=True,existingQuestionIdentityChecked=True,expectedOriginalImages=acq['imagesExpected'],acquisitionPath=str((D/'acquisition.json').relative_to(ROOT)),acquisitionSHA256=hashlib.sha256((D/'acquisition.json').read_bytes()).hexdigest(),confirmationEvidence=[dict(questionId=qid,requestId=requestid,snapshotSHA256=hashlib.sha256(json.dumps(record,ensure_ascii=False,sort_keys=True).encode()).hexdigest())],intent='同步已在monitor明確確認的內容／使用者留言，不重新請求同項確認、不重作舊圖、不恢復其他工作。')
save(D/'execution-scope.json',scope);save(D/'execution-progress.json',dict(state='active',sourceId=q['sourceId'],completedQuestionIds=[],startedAt=now()))
with locked(ROOT):
 save(ROOT/'monitor/question-update-authorization.json',dict(state='active',sourceId=q['sourceId'],url=acq['url'],scopePath=str((D/'execution-scope.json').relative_to(ROOT)),scopeSHA256=hashlib.sha256((D/'execution-scope.json').read_bytes()).hexdigest(),progressPath=str((D/'execution-progress.json').relative_to(ROOT)),activatedAt=now()))
 save(ROOT/'monitor/priority-source.json',dict(kind='explicit_question_update',state='active',sourceId=q['sourceId'],url=acq['url'],questionIds=[qid],plan=str((D/'execution-scope.json').relative_to(ROOT)),note='僅同步此題monitor已確認內容，其他舊佇列仍暫停。',updatedAt=now()))
 display=load(ROOT/'monitor/parallel.json');lane=next(l for l in display['lanes'] if l['lane']==1);lane.update(claimsPaused=False,activeTask=dict(state='integrating',questionId=qid,title='同步已在monitor確認：'+qid,startedAt=now()));save(ROOT/'monitor/parallel.json',display);update_display(ROOT,load(ROOT/'docs/comics/pipeline.json'))
assert_work_allowed(ROOT,qid)
print(json.dumps(dict(allowed=[qid],sourceId=q['sourceId'],authorization='resolved monitor snapshot',requestId=requestid),ensure_ascii=False))
