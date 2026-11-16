"""Attach only this source's staged four-image specs and run formal QA, without counting completion."""
from pathlib import Path
import os,json,subprocess,sys
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R));from monitor.comic_pipeline import begin
ids=sys.argv[1:];assert ids
scope=set(json.load(open(Path(__file__).parent/'plan.json'))['candidateQuestionIds'])
env=dict(os.environ);env['PATH']=str(R/'.cache/qa-tools/bin')+os.pathsep+env['PATH'];env['LD_LIBRARY_PATH']=str(R/'.cache/playwright-system-libs/extracted/usr/lib/x86_64-linux-gnu')+(os.pathsep+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
for qid in ids:
 assert qid in scope;s=json.load(open(R/f'docs/comics/{qid}.json'));imgs=[p.get('image') for p in s['panels']]+[s['fourth'].get('image')];assert len(imgs)==4 and all(imgs) and len(set(imgs))==4;assert all((R/p).is_file() for p in imgs);assert s.get('sourceGeneratedArtUsed') is False
 begin(R,qid);subprocess.run([sys.executable,'site/scripts/attach-comic.py',qid],cwd=R,env=env,check=True)
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=R,env=env,check=True)
subprocess.run(['node','site/scripts/check-comics.cjs',*ids],cwd=R,env=env,check=True)
print('Formal checks passed; actual app/standalone desktop/mobile inspection required before integration:',','.join(ids))
