"""Freeze the user's missing-illustration and Biology rework scope; audit actual visuals."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent

def visuals(comic):
    if not isinstance(comic,dict):return []
    panels=comic.get('panels') or []
    return [p.get('image') for p in panels]+[comic.get('fourth',{}).get('image')]

def run():
    data=json.loads((ROOT/'site/dist/data.json').read_text())
    bio=[q for q in data['questions'] if q['subject']=='Biology']
    def missing_visual(q):
        for c in q.get('groupQuestions') or [q]:
            comic=c.get('teachingComic') or q.get('teachingComic')
            if not comic:return True
            panels=comic.get('panels',[])
            if len(panels)==3 and all(p.get('diagram',{}).get('kind') in ('flow','paths','nested') and not p.get('image') for p in panels):return True
        return False
    missing=[q for q in data['questions'] if missing_visual(q)]
    now=datetime.now(timezone.utc).isoformat()
    plan_path=HERE/'plan.json'
    if not plan_path.exists():
        ids={q['id'] for q in bio+missing};baseline=[q for q in data['questions'] if q['id'] in ids]
        (HERE/'original-content-baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
        history=HERE/'previous-specs';history.mkdir(exist_ok=True)
        for q in baseline:
            for item in q.get('groupQuestions') or [q]:
                spec=ROOT/f'docs/comics/{item["id"]}.json'
                if spec.exists():(history/spec.name).write_bytes(spec.read_bytes())
        entries=[]
        for q in baseline:
            children=q.get('groupQuestions') or [q]
            entries.append(dict(id=q['id'],subject=q['subject'],title=q['title'],originalQuestionIds=[c['id'] for c in children],reasons=(['biology_quality_upgrade'] if q['subject']=='Biology' else [])+(['missing_illustration'] if q in missing else []),state='queued',requiredImagesPerOriginal=4,completedImages=0))
        entries.sort(key=lambda e:(0 if e['id']=='q-046' else 1 if e['subject']=='Biology' else 2,int(e['id'][2:])))
        plan=dict(kind='four_image_biology_and_missing_rework',state='active',createdAt=now,updatedAt=now,worknerdTaskId='t_a87b51180cc247a88d16',goalActive=True,scope='生物及實際缺圖題面（含只有文字流程框），題組保留全部原問及各問圖解；以凍結清單和個別核查為準。',qualityReference='todo/image.png',qualityReferenceSHA256=hashlib.sha256((ROOT/'todo/image.png').read_bytes()).hexdigest(),biologyQuestionPageCount=len(bio),missingQuestionPageCount=len(missing),overlapQuestionPageIds=[q['id'] for q in bio if q in missing],questionPageCount=len(entries),originalQuestionCount=sum(len(e['originalQuestionIds']) for e in entries),requiredImageCount=sum(4*len(e['originalQuestionIds']) for e in entries),completedQuestionPages=0,questionIds=[e['id'] for e in entries],completionRule='每原問4張實際有教學內容的新圖；生物類真實品質；核對原卷與科學正確性、正式桌手機QA、唯一整合者integrated後才complete。舊not_suitable不自動豁免；真正缺資料另記不可猜補。',execution='Agent1唯一題庫整合與renderer；Agent3逐題生物四圖製作，root維護技能/範圍與機動製作；Agent2維持使用者指定暫停。',publishRule='沿用20個正式整合事件commit/push；不足20不擅自宣稱已推送，全部GOAL完成時依當時授權收尾。',entries=entries)
        plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    plan=json.loads(plan_path.read_text());index={q['id']:q for q in data['questions']};checks=[]
    for entry in plan['entries']:
        q=index.get(entry['id']);children=(q.get('groupQuestions') or [q]) if q else []
        results=[]
        for c in children:
            comic=c.get('teachingComic') or q.get('teachingComic');images=visuals(comic);valid=len(images)==4 and all(isinstance(p,str) and p.startswith('assets/') and (ROOT/'site/dist'/p).is_file() for p in images) and len(set(images))==4
            results.append(dict(id=c['id'],independentImages=images,fourDistinctExistingImages=valid))
        checks.append(dict(id=entry['id'],state=entry['state'],originals=results))
    report=dict(checkedAt=now,scopeFrozen=True,questionPages=plan['questionPageCount'],originalQuestions=plan['originalQuestionCount'],requiredImages=plan['requiredImageCount'],fourImageStructureComplete=sum(all(c['fourDistinctExistingImages'] for c in e['originals']) for e in checks),note='結構檢查不是科學或美術驗收；只有人工實看與正式QA後才可標complete。',entries=checks)
    (HERE/'structure-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='entries'},ensure_ascii=False))
if __name__=='__main__':run()
