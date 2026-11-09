"""Publish exactly one staged comic, refresh group embedding and run formal QA.
Does not count completion; the integrator must actually open the saved renders
before calling finish-integration.py.
"""
from pathlib import Path
import argparse,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import begin,load,save,locked
p=argparse.ArgumentParser(description=__doc__);p.add_argument('id');args=p.parse_args();qid=args.id
begin(ROOT,qid)
env=dict(os.environ);env['PATH']=str(ROOT/'.cache/qa-tools/bin')+os.pathsep+env['PATH'];env['LD_LIBRARY_PATH']=str(ROOT/'.cache/playwright-system-libs/extracted/usr/lib/x86_64-linux-gnu')+(os.pathsep+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
subprocess.run([sys.executable,'site/scripts/attach-comic.py',qid],cwd=ROOT,env=env,check=True)
groups=load(ROOT/'docs/question-groups.json')
for parent,group in groups.items():
    if qid not in group['members']:continue
    path=ROOT/'docs/complete-questions'/f'{parent}.json'
    with locked(ROOT):
        wrapper=load(path)
        if qid==parent:
            child=next(c for c in wrapper['groupQuestions'] if c['id']==qid)
            child['teachingComic']=wrapper.pop('teachingComic')
        else:
            latest=load(ROOT/'docs/complete-questions'/f'{qid}.json')
            wrapper['groupQuestions']=[latest if c['id']==qid else c for c in wrapper['groupQuestions']]
        save(path,wrapper)
subprocess.run([sys.executable,'site/scripts/curate.py'],cwd=ROOT,env=env,check=True)
subprocess.run(['node','docs/comics/remaining-20261109/check-formal.cjs',qid],cwd=ROOT,env=env,check=True)
print('Formal QA passed; actual desktop/mobile screenshot inspection still required:',qid)
