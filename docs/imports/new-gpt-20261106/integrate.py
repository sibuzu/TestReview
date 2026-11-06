"""Root-only publication from the four reviewed original-question drafts."""
import json,hashlib,sys,subprocess
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'site/scripts'))
from monitor.comic_pipeline import locked,save,ensure_job_identity,update_display
from importlib.machinery import SourceFileLoader
attach_module=SourceFileLoader('attach_comic',str(ROOT/'site/scripts/attach-comic.py')).load_module()
D=ROOT/'docs/imports/new-gpt-20261106';url='https://chatgpt.com/share/6aede186-c184-83ee-9f74-2d44b77d6587';now=datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(Path(p).read_text())
acq=load(ROOT/'docs/acquisition/new-gpt-20261106.json');originals=[]
for image in acq['downloadedImages']:
 src=ROOT/image['path'];name=f'assets/originals/src-more-061-original-{len(originals)+1:02}-{image["sha256"][:12]}.jpg';(ROOT/'site/dist'/name).write_bytes(src.read_bytes());originals.append(name)
archive=load(ROOT/acq['archive']);parts=[]
for n,m in enumerate(archive['messages']):
 role=m.get('author',{}).get('role');channel=m.get('channel')
 if role not in ('user','assistant') or channel not in (None,'final'):continue
 texts=[p for p in m.get('content',{}).get('parts',[]) if isinstance(p,str)]
 if texts:parts.append(f'[{n}] {role}\n'+'\n'.join(texts))
transcript='\n\n'.join(parts);relative='sources/6aede186-c184-83ee-9f74-2d44b77d6587.txt';(ROOT/'site/dist'/relative).write_text(transcript);(D/'transcript.txt').write_text(transcript)
sources=load(ROOT/'docs/additional-sources.json')
if not any(s['id']=='src-more-061' for s in sources):
 sources.append(dict(id='src-more-061',url=url,status='read',title=archive['title'],platform='ChatGPT',date='2026-11-06',addedAt='2026-11-06',note='已保存完整來源文字及4張真正上傳原卷；逐題核對原問，來源AI錯誤圖不採用，另列Monitor。',content=transcript,images=originals,transcript=relative));save(ROOT/'docs/additional-sources.json',sources)
rows=load(ROOT/'docs/additional-questions.json');ids={q['id'] for q in rows};receipt=load(D/'integrated.json') if (D/'integrated.json').exists() else dict(items=[])
for filename in ('biology11.json','biology13.json','biology29.json','geography1.json'):
 p=D/filename
 if not p.exists():continue
 q=load(p);qid=q['id']
 if qid in ids:continue
 q['sourceId']='src-more-061';q.pop('sourceEvidence',None);q.pop('duplicateReview',None);q.pop('sourceAIErrors',None)
 def publish(value):
  if isinstance(value,str) and value.startswith('docs/') and (ROOT/value).is_file():
   source=ROOT/value;h=hashlib.sha256(source.read_bytes()).hexdigest()[:12];target=f'assets/questions/{qid}-{source.stem}-{h}{source.suffix}';(ROOT/'site/dist'/target).write_bytes(source.read_bytes());return target
  if isinstance(value,list):return [publish(v) for v in value]
  if isinstance(value,dict):return {k:publish(v) for k,v in value.items()}
  return value
 q=publish(q)
 # Normalize only after all original-figure paths refer to published local assets.
 script="import {validateQuestion} from './site/dist/core.js';let s='';for await(const b of process.stdin)s+=b;console.log(JSON.stringify(validateQuestion(JSON.parse(s))));"
 clean=json.loads(subprocess.run(['node','--input-type=module','-e',script],cwd=ROOT,input=json.dumps(q),text=True,capture_output=True,check=True).stdout)
 assert clean and clean['id']==qid and clean['question']==q['question']
 q=clean;rows.append(q);ids.add(qid)
 with locked(ROOT):
  progress=load(ROOT/'docs/comics/progress.json');progress['entries'].append(dict(id=qid,subject=q['subject'],date=q['date'],title=q['title'],state='queued',reason='新來源原問已核對；待全新四格正式整合',freshFourPanelRequired=True));save(ROOT/'docs/comics/progress.json',progress)
  pipeline=load(ROOT/'docs/comics/pipeline.json');job=dict(id=qid,title=q['title'],subject=q['subject'],lane=1,state='claimed',startedAt=load(ROOT/'docs/imports/new-gpt-session-2026-11-06.json')['startedAt'],reason='本批指定來源已核對原卷及獨立新四格稿');ensure_job_identity(job);pipeline['jobs'].append(job);save(ROOT/'docs/comics/pipeline.json',pipeline);update_display(ROOT,pipeline)
 receipt['items'].append(dict(id=qid,draft=str(p.relative_to(ROOT)),publishedAt=now,questionSHA256=hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
save(ROOT/'docs/additional-questions.json',rows);save(D/'integrated.json',receipt)
# Attach only the final per-question specs whose isolated QA is available.
for row in receipt['items']:
 qid=row['id']
 if (ROOT/f'docs/comics/{qid}-preview-validation.json').exists():attach_module.attach(qid)
progress=load(ROOT/'docs/imports/more-gpt-progress.json');source=next(s for s in progress['sources'] if s['order']==61);source.update(questionIds=[i['id'] for i in receipt['items']],originalQuestionIds=[i['id'] for i in receipt['items']],originalQuestionCount=len(receipt['items']),questionPageCount=len(receipt['items']),contentCurationComplete=len(receipt['items'])==4);save(ROOT/'docs/imports/more-gpt-progress.json',progress)
subprocess.run([sys.executable,str(ROOT/'site/scripts/curate.py')],cwd=ROOT,check=True)
print('Published',len(receipt['items']),'reviewed original questions')
