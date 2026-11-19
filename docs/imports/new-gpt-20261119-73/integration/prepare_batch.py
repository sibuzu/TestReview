"""Mechanically consume finalized producer manifests for this source only."""
import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import locked,load,save,now,ensure_job_identity,begin,update_display
from monitor.comic_execution import assert_work_allowed
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=load(D/'plan.json');scope=load(D/'execution-scope.json');allowed=set(scope['newQuestionIds']);combined=[]
lanes=[int(n) for n in sys.argv[1:]] or [2,3]
assert set(lanes)<={2,3} and len(lanes)==len(set(lanes))
for n in lanes:
 mp=D/f'lane{n}/manifest.json';m=load(mp)
 assert m['state'] in ('ready','ready_for_sole_integrator'),f'{mp}: not finalized'
 rows=m.get('questions',m.get('items',[]));assert len(rows)==6
 for r in rows:
  qid=r.get('id',r.get('candidateId'));assert qid in allowed
  draft=r.get('questionPath',r.get('draftPath'));spec=r['specPath'];review=r['reviewPath']
  for asset in r['assets']:
   p=ROOT/asset['sourcePath'];assert p.is_file() and sha(p)==asset['sha256'],str(p)
  q=load(ROOT/draft);s=load(ROOT/spec);v=load(ROOT/review)
  assert q['id']==s['id']==qid and q['sourceId']==plan['sourceId']
  assert v['originalVisualChecked'] and v['completeOriginalAndOptions'] and v['sourceGeneratedArtUsed'] is False
  assert v['actualViewed'] and all((ROOT/p).is_file() for p in v['actualViewed'])
  assert v['inclusionEvidence'] and v['duplicateReview']
  image_paths=[p['image'] for p in s['panels']]+[s['fourth']['image']]
  assert len(image_paths)==len(set(image_paths))==4 and len({sha(ROOT/p) for p in image_paths})==4
  combined.append(dict(candidateId=qid,disposition='new',draftPath=draft,draftSHA256=sha(ROOT/draft),specPath=spec,specSHA256=sha(ROOT/spec),reviewPath=review,reviewSHA256=sha(ROOT/review),producerAgent=m.get('producerAgent',f'/root/comic_lane_{n}'),lane=n))
prepared_ids={r['candidateId'] for r in combined};assert prepared_ids<=allowed
canonical=D/('integration/finalized-manifest-lanes'+''.join(str(n) for n in lanes)+'.json');save(canonical,dict(sourceId=plan['sourceId'],frozenAt=now(),items=combined))
# Reuse the audited per-source question intaker; only the default source path differs.
subprocess.run([sys.executable,str(D/'integrate.py'),str(canonical.relative_to(ROOT)),'--plan',str((D/'plan.json').relative_to(ROOT))],cwd=ROOT,check=True)
# Source AI diagrams are replaced, with a review card; no complete event until confirmed.
pending={'q-1168'}
# Additional producer requests can be marked by the manifest row or per-question review.
for r in combined:
 review=load(ROOT/r['reviewPath'])
 if review.get('requiresConfirmation'):pending.add(r['candidateId'])
plan=load(D/'plan.json');plan['pendingReviewQuestionIds']=sorted(pending);save(D/'plan.json',plan)
for r in combined:
 qid=r['candidateId'];assert_work_allowed(ROOT,qid);spec=load(ROOT/r['specPath'])
 review_path=ROOT/f'docs/comics/{qid}-production-review.json';save(review_path,load(ROOT/r['reviewPath']))
 spec['producerReviewPath']=str(review_path.relative_to(ROOT));spec['producerManifest']=str(canonical.relative_to(ROOT))
 canonical_spec=ROOT/f'docs/comics/{qid}.json'
 if canonical_spec.exists():assert load(canonical_spec).get('producerManifest')==str(canonical.relative_to(ROOT))
 else:save(canonical_spec,spec)
 with locked(ROOT):
  pipeline=load(ROOT/'docs/comics/pipeline.json');previous=next((j for j in pipeline['jobs'] if j['id']==qid),None)
  job=dict(id=qid,title=load(ROOT/r['draftPath'])['title'],subject='Physics-Chemistry',lane=r['lane'],state='blocked' if qid in pending else 'ready',startedAt=spec.get('createdAt',now()),readyAt=now(),decision='awaiting_confirmation' if qid in pending else 'complete',reason='製作代理完整核對原卷與四張新圖並完成隔離桌手機驗版，交唯一整合者技術加入；原AI錯圖另保留確認卡。' if qid in pending else '製作代理完整核對原卷與四張新圖並完成隔離桌手機驗版，交唯一整合者技術加入。',evidence=[str(canonical_spec.relative_to(ROOT)),str(review_path.relative_to(ROOT))],assignmentMethod='source73 fixed qid reservations; finalized producer manifest only',productionTimingIncomplete=True,excludeFromSpeedStatistics=True)
  if previous:
   assert previous.get('assignmentMethod')=='source73 fixed qid reservations; finalized producer manifest only';job=previous
  else:ensure_job_identity(job);pipeline['jobs'].append(job)
  save(ROOT/'docs/comics/pipeline.json',pipeline)
  if qid in pending:job['artQAStartedAt']=now();job['artQAOnly']=True;save(ROOT/'docs/comics/pipeline.json',pipeline)
  update_display(ROOT,pipeline)
 if qid not in pending:begin(ROOT,qid)
 subprocess.run([sys.executable,'site/scripts/attach-comic.py',qid],cwd=ROOT,check=True)
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=ROOT,check=True)
receipt=D/'integration/prepared-batch.json';previous=load(receipt) if receipt.exists() else {};save(receipt,dict(preparedAt=now(),questionIds=sorted(set(previous.get('questionIds',[]))|prepared_ids),pendingReviewQuestionIds=sorted(pending),sourceId=plan['sourceId']))
print(json.dumps(dict(preparedQuestions=sorted(prepared_ids),pendingReviewQuestionIds=sorted(pending)),ensure_ascii=False))
