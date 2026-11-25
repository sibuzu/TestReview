"""Root consumes one frozen local handoff without resuming generic claims."""
import argparse,hashlib,json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent
sys.path.insert(0,str(R))
from monitor.comic_pipeline import load,save,locked,now,ensure_job_identity,begin,update_display
from monitor.comic_execution import assert_work_allowed
p=argparse.ArgumentParser();p.add_argument('handoff');a=p.parse_args();hp=R/a.handoff;h=load(hp)
qid=h.get('id',h.get('questionId'));assert qid in load(D/'manifest.json')['questionIds'];assert_work_allowed(R,qid)
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
sp=R/h['specPath'];rp=R/h['reviewPath'];assert sha(sp)==h['specSHA256'] and sha(rp)==h['reviewSHA256']
for asset in h.get('assets',[]):
 assert sha(R/asset.get('sourcePath',asset.get('path')))==asset['sha256']
for name in ['prompts','generation']:
 if h.get(name+'SHA256'):assert sha(R/h[name+'Path'])==h[name+'SHA256']
s=load(sp);v=load(rp);assert s['id']==qid and s['subject']=='Biology'
assert s.get('sourceGeneratedArtUsed') is False
images=[i['image'] for i in s['panels']]+[s['fourth']['image']]
assert len(images)==len(set(images))==len({sha(R/i) for i in images})==4
assert all(Path(i).suffix.lower() in ['.png','.webp','.jpg','.jpeg'] for i in images)
assert v.get('passed') is True
assert v.get('originalVisualChecked',v.get('originalCropsActuallyViewed')) is True
assert v.get('allFourNewImagesActuallyViewed') is True
assert v.get('desktopMobileActuallyViewed') is True
baseline=load(D/'questions-before.json');old=next(q for q in baseline['questions']if q['id']==qid);live=next(q for q in load(R/'site/dist/data.json')['questions']if q['id']==qid)
assert {k:v for k,v in old.items()if k!='teachingComic'}=={k:v for k,v in live.items()if k!='teachingComic'}
evidence=R/f'docs/comics/{qid}-biology-20261122-production-review.json';save(evidence,v)
s.update(producerReviewPath=str(evidence.relative_to(R)),producerManifest=str(hp.relative_to(R)),producerVisualChecked=True,rootReview={},visualChecked=False)
save(R/f'docs/comics/{qid}.json',s)
with locked(R):
 pipe=load(R/'docs/comics/pipeline.json')
 previous=next((j for j in pipe['jobs'] if j.get('limitedBatch')=='biology-ten-20261122' and j['id']==qid),None)
 if previous:assert previous['state']=='ready' and qid not in load(D/'manifest.json')['completedQuestionIds']
 job=dict(id=qid,title=old['title'],subject='Biology',lane=1,state='ready',decision='complete',startedAt=s.get('createdAt',now()),readyAt=now(),reason='本批生物舊圖四張全新類真實科學教材插畫；原卷/答案及製作線隔離桌手機檢查通過，交root正式驗收。',evidence=[f'docs/comics/{qid}.json',str(evidence.relative_to(R))],limitedBatch='biology-ten-20261122',producerAgent=s.get('producerAgent'),assignmentMethod='explicit 10 biology frozen handoff; no generic queue claim',productionTimingIncomplete=True,excludeFromSpeedStatistics=True)
 if previous:job=previous
 else:ensure_job_identity(job);pipe['jobs'].append(job)
 save(R/'docs/comics/pipeline.json',pipe);update_display(R,pipe)
job=begin(R,qid)
receipt_path=D/'prepared-jobs.json';receipts=load(receipt_path)if receipt_path.exists()else{};receipts[qid]=dict(jobId=job['jobId'],handoff=str(hp.relative_to(R)),handoffSHA256=sha(hp));save(receipt_path,receipts)
env=dict(os.environ);env['LD_LIBRARY_PATH']=str(R/'.cache/playwright-system-libs/extracted/usr/lib/x86_64-linux-gnu')
subprocess.run([sys.executable,'site/scripts/attach-comic.py',qid],cwd=R,env=env,check=True)
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=R,env=env,check=True)
subprocess.run(['node','site/scripts/check-comics.cjs',qid],cwd=R,env=env,check=True)
print('Formal automatic checks passed; root must actually view the screenshots before acceptance:',qid)
