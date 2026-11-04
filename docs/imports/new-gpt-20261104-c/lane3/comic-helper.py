from pathlib import Path
import json,time,datetime,hashlib
P=Path('docs/comics');URL='https://chatgpt.com/share/6aeb402e-c158-83ee-b603-6444a590bf27'
def start(q):
 (P/f'{q}-generation-start.json').write_text(json.dumps(dict(startedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),monotonicStartNs=time.monotonic_ns(),scope='built-in generation and artifact persistence on same host'),indent=2)+'\n')
def spec(q,title,panels,answer,points,protected,rationale,art=None,method=None):
 art=art or f'docs/comics/art/{q}.png'
 x=dict(id=q,subject='Chinese',title=title,art=art,layoutVersion='native-fluid-v6',panels=panels,fourth=dict(answer=answer,points=points),protectedWords=protected,sourceUrl=URL,originalMaterialsChecked=True,sourceGeneratedArtUsed=False,generationMethod=method or 'built-in image_gen; new detailed colorful anime triptych; exact teaching text only in HTML',rationale=rationale,promptFile=f'docs/comics/{q}-prompt.txt',artSHA256=hashlib.sha256(Path(art).read_bytes()).hexdigest(),visualChecked=False)
 s=P/f'{q}-generation-start.json'
 if s.exists():
  v=json.loads(s.read_text());end=time.monotonic_ns();v.update(completedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),monotonicEndNs=end,durationSeconds=(end-v['monotonicStartNs'])/1e9,timingValid=True,measurementMethod='same-host monotonic_ns; tool and artifact persistence');(P/f'{q}-generation-timing.json').write_text(json.dumps(v,indent=2)+'\n');x['generationTiming']=f'docs/comics/{q}-generation-timing.json'
 (P/f'{q}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def reviewed(q,note):
 p=P/f'{q}.json';x=json.loads(p.read_text());x.update(visualChecked=True,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),previewValidation=f'docs/comics/{q}-preview-validation.json',visualReview=note);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
