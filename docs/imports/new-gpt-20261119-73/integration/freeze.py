"""Freeze the current source only after producers' actual original/duplicate reviews."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,locked,now
from monitor.comic_execution import authorized_new_source
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Each producer writes a durable original-and-duplicate audit before this runs.
records=[]
for n in [2,3]:
 p=D/f'lane{n}/dedupe-review.json';r=load(p)
 assert r['originalVisualChecked'] is True and r['crossSourceDuplicatesChecked'] is True
 records.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),review=r))
ids=[item['id'] for r in records for item in r['review']['items'] if item['disposition']=='new']
assert len(ids)==len(set(ids)) and len(ids)>0
plan=load(D/'plan.json');bank=load(Path('.cache/intake-20261119-6aff02c8/baseline-data.json'));acq=D/'acquisition.json'
save(D/'dedupe-freeze.json',dict(sourceId=plan['sourceId'],checkedAt=now(),records=records,newQuestionIds=ids,originalsVisualChecked=True,crossSourceDuplicatesChecked=True))
scope=dict(version=1,kind='explicit_new_source',authorizedBy='user_add',sourceId=plan['sourceId'],url=plan['url'],newQuestionIds=ids,baselineQuestionIds=[q['id'] for q in bank['questions']],baselineSourceIds=[s['id'] for s in bank['sources']],originalsVisualChecked=True,crossSourceDuplicatesChecked=True,acquisitionPath=str(acq.relative_to(ROOT)),acquisitionSHA256=sha(acq),dedupeFreeze=str((D/'dedupe-freeze.json').relative_to(ROOT)))
save(D/'execution-scope.json',scope)
with locked(ROOT):
 plan.update(newQuestionIds=ids,questionIds=ids,updatedAt=now());save(D/'plan.json',plan)
 progress=load(D/'execution-progress.json');progress.update(state='active',activatedAt=now());save(D/'execution-progress.json',progress)
 save(ROOT/'monitor/new-source-authorization.json',dict(version=1,state='active',sourceId=plan['sourceId'],url=plan['url'],scopePath=str((D/'execution-scope.json').relative_to(ROOT)),scopeSHA256=sha(D/'execution-scope.json'),progressPath=str((D/'execution-progress.json').relative_to(ROOT)),activatedAt=now()))
for qid in ids:assert authorized_new_source(ROOT,qid)
assert not authorized_new_source(ROOT,'q-1156')
print(json.dumps(dict(authorizedNewQuestions=ids,oldQuestionDenied=True),ensure_ascii=False))
