"""Record the integrator's actual formal screenshot review, then count one event.
Call only after opening the desktop/mobile screenshots from both reading views.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import integrated,locked,load,save
p=argparse.ArgumentParser(description=__doc__);p.add_argument('id');p.add_argument('--note',required=True);args=p.parse_args();qid=args.id
spec_path=ROOT/'docs/comics'/f'{qid}.json';spec=load(spec_path);validation=ROOT/'docs/comics'/f'{qid}-validation.json';v=load(validation)
assert len(v['results'])>=6 and {1440,1120,390}.issubset({r['viewport'] for r in v['results']})
assert all(not r.get('overflow') and not r.get('docOverflow') and not r.get('wrapErrors') and not r.get('protectedBreaks') for r in v['results'])
shots=[f'/tmp/weirugo-comic-checks/{qid}-{view}-{w}.png' for view in ['app','standalone'] for w in [1440,390]];assert all(Path(s).is_file() for s in shots)
spec['rootReview']=dict(visualChecked=True,desktopMobileActuallyViewed=True,reviewerAgent='/root/comic_lane_1',checkedAt=datetime.now(timezone.utc).isoformat(),screenshots=shots,note=args.note)
spec['validationFile']=str(validation.relative_to(ROOT));save(spec_path,spec)
job=integrated(ROOT,qid)
with locked(ROOT):
 plan_path=ROOT/'docs/comics/remaining-20261109/plan.json';plan=load(plan_path);scope=set(plan['questionIds']);progress=load(ROOT/'docs/comics/progress.json');done=[e['id'] for e in progress['entries'] if e['id'] in scope and e['state']=='complete'];plan.update(completedQuestionIds=done,completedCount=len(done),updatedAt=datetime.now(timezone.utc).isoformat());save(plan_path,plan)
 save(ROOT/'monitor/activity.json',dict(title=f'剩餘47題四格：已正式整合{len(done)}/47',detail=f'剛完成{qid}；包含原題核對、全新四格、隔離預覽與正式桌機/手機實看，app及單頁三寬QA通過。其餘持續製作；ready或queued均不計完成。',goalStatus='active',updatedAt=datetime.now(timezone.utc).isoformat()))
print(json.dumps(dict(id=qid,completed=len(done),total=47,integrationEventId=job['integrationEventId']),ensure_ascii=False))
