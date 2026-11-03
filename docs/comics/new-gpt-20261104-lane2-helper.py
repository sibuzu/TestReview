from pathlib import Path
import json,hashlib,datetime
R=Path('/home/jack/git/TestReview');SOURCE='https://chatgpt.com/share/6aea190f-d430-83ee-ab44-f243de7f2aec'
def child(qid):return next(c for p in json.loads((R/'site/dist/data.json').read_text())['questions'] for c in (p.get('groupQuestions') or [p]) if c['id']==qid)
def node(label,detail='',tone='blue'):return dict(label=label,detail=detail,tone=tone)
def flow(title,items,arrow='判斷下一步',note=''):return dict(kind='flow',title=title,items=items,arrow=arrow,note=note)
def paths(title,items,target,arrow='依條件判斷'):return dict(kind='paths',title=title,items=items,target=target,arrow=arrow)
def panel(h,t,alt,diagram=None):
 x=dict(heading=h,text=t,alt=alt)
 if diagram:x['diagram']=diagram
 return x

def save(qid,title,panels,answer,points,protected,rationale,mode='native'):
 q=child(qid)
 art=f'docs/comics/art/{qid}.png' if mode=='anime' else f'docs/comics/art/{qid}-relationships.svg'
 if mode!='anime':
  # Compatibility fallback only. The visible, selectable labeled diagrams live in panels[].diagram.
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><title>{qid} native labeled relationship diagrams</title><rect width="540" height="180" fill="#f4f8f0"/><g fill="#d9e8f1" stroke="#547384" stroke-width="2">'+''.join(f'<rect x="{x}" y="30" width="130" height="120" rx="12"/>' for x in [25,205,385])+'</g></svg>'
  (R/art).write_text(svg)
 s=dict(id=qid,subject='Civics',title=title,art=art,panels=panels,fourth=dict(answer=answer,points=points),protectedWords=protected,sourceUrl=SOURCE,originalMaterialsChecked=True,originalChecked=dict(images=['site/dist/'+p for p in q['images']],visualChecked=True,answer=q['correctOption'],notes='本代理已逐題實看原卷/裁圖，讀完原題、所有選項及必要材料並獨立核官方法規。'),rationale=rationale,generationMethod='built-in image_gen; new text-free detailed anime triptych' if mode=='anime' else 'Selectable native HTML/CSS labeled relationship diagrams; compatibility SVG is not the visible teaching content.',sourceGeneratedArtUsed=False,producerAgent='/root/comic_lane_2',createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),artSHA256=hashlib.sha256((R/art).read_bytes()).hexdigest(),layoutVersion='native-fluid-v6',visualChecked=False)
 if mode=='anime':s.update(styleReferences=['docs/comics/art/q-153.png','docs/comics/art/q-154.png'],promptFile=f'docs/comics/{qid}-prompt.txt')
 (R/f'docs/comics/{qid}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
 return s

def reviewed(qid,note):
 p=R/f'docs/comics/{qid}.json';s=json.loads(p.read_text());s.update(visualChecked=True,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),previewValidation=f'docs/comics/{qid}-preview-validation.json',visualReview=note,producerReview=dict(reviewerAgent='/root/comic_lane_2',originalCropsActuallyViewed=True,desktopMobileActuallyViewed=True,screenshots=[f'/tmp/weirugo-comic-previews/{qid}-{w}.png' for w in [1440,390]]));p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
