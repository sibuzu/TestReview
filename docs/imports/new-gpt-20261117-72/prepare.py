"""Sole integrator: attach explicit staged batch members and run formal checks."""
from pathlib import Path
import os,json,subprocess,sys
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent;sys.path.insert(0,str(R))
from monitor.comic_pipeline import begin,load,save,locked,now
from monitor.comic_execution import assert_work_allowed
ids=sys.argv[1:];assert ids
m=json.loads((D/'execution-scope.json').read_text());progress=json.loads((D/'execution-progress.json').read_text());assert progress['state']=='active'
env=dict(os.environ);env['PATH']=str(R/'.cache/qa-tools/bin')+os.pathsep+env['PATH'];env['LD_LIBRARY_PATH']=str(R/'.cache/playwright-system-libs/extracted/usr/lib/x86_64-linux-gnu')
for qid in ids:
 assert qid in m['newQuestionIds'] and qid not in progress['completedQuestionIds'];assert_work_allowed(R,qid)
 spec=json.loads((R/f'docs/comics/{qid}.json').read_text());images=[p.get('image') for p in spec['panels']]+[spec['fourth'].get('image')]
 assert len(images)==len(set(images))==4 and all((R/p).is_file() for p in images)
 review=spec.get('producerReview',{})
 assert spec.get('sourceGeneratedArtUsed') is False and (spec.get('producerVisualChecked') or all(review.get(k) for k in ['originalCropsActuallyViewed','allFourNewImagesActuallyViewed','desktopMobileActuallyViewed']))
 latest=next(j for j in reversed(load(R/'docs/comics/pipeline.json')['jobs']) if j['id']==qid)
 if latest['state']=='blocked':
  # Source72-only art review. Never promote a blocked question to ready/complete.
  plan=load(D/'plan.json');pending=set(plan.get('pendingOriginalMaterialQuestionIds',[])+plan.get('pendingAnswerQuestionIds',[]))
  assert qid in {'q-1135','q-1153','q-1154'} & pending
  assert latest['decision']=='awaiting_confirmation' and not latest.get('integrationEventId')
  with locked(R):
   pipeline=load(R/'docs/comics/pipeline.json');job=next(j for j in pipeline['jobs'] if j.get('jobId')==latest['jobId'])
   assert job['state']=='blocked' and job['decision']=='awaiting_confirmation'
   job.setdefault('artQAStartedAt',now());job['artQAOnly']=True
   save(R/'docs/comics/pipeline.json',pipeline)
 else:job=begin(R,qid)
 receipts_path=D/'prepared-jobs.json';receipts=load(receipts_path) if receipts_path.exists() else {};receipts[qid]={'jobId':job['jobId'],'specPath':f'docs/comics/{qid}.json'};save(receipts_path,receipts)
 subprocess.run([sys.executable,'site/scripts/attach-comic.py',qid],cwd=R,env=env,check=True)
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=R,env=env,check=True)
subprocess.run(['node','site/scripts/check-comics.cjs',*ids],cwd=R,env=env,check=True)
print('Formal layout checks passed; integrator must actually view app/standalone desktop/mobile before finish:',','.join(ids))
