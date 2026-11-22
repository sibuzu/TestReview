"""Consume only finalized source 74 handoffs; root owns shared publication."""
import hashlib,json,runpy,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
B=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import locked,load,save,now,ensure_job_identity,begin,update_display
from monitor.comic_execution import assert_work_allowed
support=runpy.run_path(str(B/'integrate.py'),run_name='intake_support')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pending={'q-1176','q-1178'}
for producer in sys.argv[1:]:
 mp=B/producer/'manifest.json';manifest=load(mp)
 assert manifest.get('state',manifest.get('status')) in ('ready','ready_for_sole_integrator')
 rows=manifest.get('items',manifest.get('questions'))
 for item in rows:
  qid=item.get('candidateId',item.get('id'))
  assert qid in {f'q-{n}' for n in range(1169,1179)}
  assert_work_allowed(ROOT,qid)
  qp=ROOT/item.get('draftPath',item.get('questionPath'));sp=ROOT/item['specPath'];rp=ROOT/item['reviewPath']
  for path,expected in [(qp,item.get('draftSHA256',item.get('questionSHA256'))),(sp,item['specSHA256']),(rp,item['reviewSHA256'])]:
   assert path.is_file() and sha(path)==expected,str(path)
  for asset in item['assets']:
   assert sha(ROOT/asset['sourcePath'])==asset['sha256']
  q=load(qp);spec=load(sp);review=load(rp)
  assert q['id']==spec['id']==qid and q['sourceId']=='src-more-074'
  assert review['originalVisualChecked'] and review['completeOriginalAndOptions'] and not review['sourceGeneratedArtUsed']
  images=[p['image'] for p in spec['panels']]+[spec['fourth']['image']]
  assert len(images)==len(set(images))==len({sha(ROOT/p) for p in images})==4
  assert not q.get('explanationFigures')
  # Preserve the early content handoff and record any producer revisions.
  receipt=load(B/'integrated.json');entry=next(r for r in receipt['items'] if r['id']==qid)
  if entry['draftSHA256']!=sha(qp) or entry['reviewSHA256']!=sha(rp):
   entry.setdefault('revisions',[]).append(dict(previousDraftSHA256=entry['draftSHA256'],previousReviewSHA256=entry['reviewSHA256'],revisedAt=now(),reason='Finalized producer handoff after early content publication; neutral title and explicit auxiliary diagram transcription.'))
   entry.update(draftSHA256=sha(qp),reviewSHA256=sha(rp))
  entry.update(finalProducerManifest=str(mp.relative_to(ROOT)),fourImageState='formal_qa_pending')
  save(B/'integrated.json',receipt)
  q['images']=[support['publish'](p,qid+'-') for p in q.get('images',[])]
  q['questionFigures']=[dict(f,src=support['publish'](f['src'],qid+'-')) for f in q.get('questionFigures',[])]
  q=support['normalize'](q)
  previous=load(ROOT/f'docs/complete-questions/{qid}.json')
  assert all(previous[k]==q[k] for k in ('id','sourceId','date','studentAnswer'))
  save(ROOT/f'docs/complete-questions/{qid}.json',q)
  allq=load(ROOT/'docs/additional-questions.json');allq=[q if r['id']==qid else r for r in allq];save(ROOT/'docs/additional-questions.json',allq)
  review_path=ROOT/f'docs/comics/{qid}-production-review.json';save(review_path,review)
  spec.update(producerReviewPath=str(review_path.relative_to(ROOT)),producerManifest=str(mp.relative_to(ROOT)))
  save(ROOT/f'docs/comics/{qid}.json',spec)
  with locked(ROOT):
   pipeline=load(ROOT/'docs/comics/pipeline.json');assert not any(j['id']==qid for j in pipeline['jobs'])
   job=dict(id=qid,title=q['title'],subject=q['subject'],lane={'history':1,'earth-a':2,'earth-b':3}[producer],state='blocked' if qid in pending else 'ready',startedAt=spec.get('createdAt',now()),readyAt=now(),decision='awaiting_confirmation' if qid in pending else 'complete',reason='完整原題、原圖與四張新圖已製作核對；正式app/單頁桌手機QA待root驗收。'+('原AI選項解說實錯另列monitor，待確認不計complete。' if qid in pending else ''),evidence=[f'docs/comics/{qid}.json',str(review_path.relative_to(ROOT))],assignmentMethod='source74 explicit finalized producer manifest; root sole integrator',productionTimingIncomplete=True,excludeFromSpeedStatistics=True)
   ensure_job_identity(job);pipeline['jobs'].append(job);save(ROOT/'docs/comics/pipeline.json',pipeline);update_display(ROOT,pipeline)
  if qid not in pending:begin(ROOT,qid)
  subprocess.run([sys.executable,'site/scripts/attach-comic.py',qid],cwd=ROOT,check=True)
  print('Attached',qid,flush=True)
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=ROOT,check=True)
