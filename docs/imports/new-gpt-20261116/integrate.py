"""Publish a frozen source manifest. Only this intake's integration owner runs it."""
from pathlib import Path
import argparse,json,hashlib,datetime,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import locked,save

def read(p):return json.loads((ROOT/Path(p)).read_text())
def rel(p):return Path(p).resolve().relative_to(ROOT) if Path(p).is_absolute() else Path(p)
def digest(p):return hashlib.sha256((ROOT/rel(p)).read_bytes()).hexdigest()
def publish(p,prefix=''):
 if str(p).startswith('assets/'):
  assert (ROOT/'site/dist'/p).is_file();return p
 p=rel(p);assert str(p).startswith('docs/') and (ROOT/p).is_file(),str(p)
 target=f'assets/originals/{prefix}{p.stem}-{digest(p)[:12]}{p.suffix.lower()}';dest=ROOT/'site/dist'/target;dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():assert dest.read_bytes()==(ROOT/p).read_bytes()
 else:dest.write_bytes((ROOT/p).read_bytes())
 return target

def normalize(q):
 js="import {validateQuestion} from './site/dist/core.js';let t='';for await(const x of process.stdin)t+=x;console.log(JSON.stringify(validateQuestion(JSON.parse(t))));"
 p=subprocess.run(['node','--input-type=module','-e',js],cwd=ROOT,input=json.dumps(q),text=True,capture_output=True,check=True);return json.loads(p.stdout)

def main(manifest_path,plan_path):
 plan=read(plan_path);sourceid=plan['sourceId'];m=read(manifest_path);assert m['sourceId']==sourceid
 reservations={r['candidateId']:r for r in read(plan['qidReservations'])['items']};acq=read(plan['acquisition']);assert len(acq['downloadedImages'])==acq['imagesExpected']==28
 receipt_path=ROOT/Path(plan_path).parent/'integrated.json';receipt=read(receipt_path) if receipt_path.exists() else {'items':[]};published=[]
 for item in m['items']:
  if item['disposition']!='new':continue
  qid=item['candidateId'];assert qid in reservations
  assert digest(item['draftPath'])==item['draftSHA256'],'Frozen draft changed: '+qid
  old=next((r for r in receipt['items'] if r['id']==qid),None)
  if old:assert old['draftSHA256']==item['draftSHA256'];continue
  q=read(item['draftPath']);review=read(item['reviewPath']);assert q['id']==qid and q['sourceId']==sourceid
  assert all(review.get(k) is True for k in ['originalVisualChecked','completeOriginalAndOptions'])
  assert review.get('sourceGeneratedArtUsed') is False and review.get('actualViewed') and all((ROOT/Path(p)).is_file() for p in review['actualViewed'])
  assert review.get('inclusionEvidence') and review.get('duplicateReview')
  assert q['contentStatus']=='完整原題' and not q.get('explanationFigures')
  assert q['date']==reservations[qid]['date'],'First question date must follow user timestamp'
  q['images']=[publish(p,qid+'-') for p in q.get('images',[])];q['questionFigures']=[dict(f,src=publish(f['src'],qid+'-')) for f in q.get('questionFigures',[])];q=normalize(q)
  now=datetime.datetime.now(datetime.timezone.utc).isoformat()
  with locked(ROOT):
   rows=read('docs/additional-questions.json');assert not any(r['id']==qid for r in rows)
   bank=read('site/dist/data.json');originals=[c for p in bank['questions'] for c in (p.get('groupQuestions') or [p])];comparable={r['id']:r for r in rows+originals};compact=lambda t:''.join(t.split())
   matches=[r['id'] for r in comparable.values() if r.get('subject')==q['subject'] and compact(r.get('question',''))==compact(q['question']) and compact(r.get('passage',''))==compact(q.get('passage','')) and r.get('tables',[])==q.get('tables',[])];assert not matches or review.get('sameTextDifferentFiguresExplained'),matches
   rows.append(q);save(ROOT/'docs/additional-questions.json',rows);save(ROOT/f'docs/complete-questions/{qid}.json',q)
   sources=read('docs/additional-sources.json');src=next((s for s in sources if s['id']==sourceid),None)
   if src is None:
    assert not any(s.get('url')==plan['url'] for s in sources);transcript=(ROOT/Path(plan_path).parent/'transcript.txt').read_text();target='sources/'+plan['url'].rsplit('/',1)[-1]+'.txt';(ROOT/'site/dist'/target).write_text(transcript);src={'id':sourceid,'url':plan['url'],'title':plan['title'],'platform':'ChatGPT','date':min(r['date'] for r in reservations.values()),'addedAt':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat(),'status':'pending','note':'28張真正原卷已取得，正在逐題核對收入及製作每新原問四張實際圖解；來源AI圖與未指定鄰題不收入。','transcript':target,'images':[publish(im['path']) for im in acq['downloadedImages']],'content':''};sources.append(src)
   save(ROOT/'docs/additional-sources.json',sources)
   gp=read('docs/imports/more-gpt-progress.json');entry=next(s for s in gp['sources'] if s.get('sourceId')==sourceid);entry['questionIds']=list(dict.fromkeys(entry['questionIds']+[qid]));entry['newQuestionIds']=list(dict.fromkeys(entry.get('newQuestionIds',[])+[qid]));entry.update(state='partial',newOriginalQuestionCount=len(entry['newQuestionIds']),newQuestionPageCount=len(entry['newQuestionIds']),questionPageCount=len(entry['questionIds']),contentCurationComplete=False);gp['updatedAt']=now;save(ROOT/'docs/imports/more-gpt-progress.json',gp)
   cp=read('docs/comics/progress.json');assert not any(e['id']==qid for e in cp['entries']);cp['entries'].append({'id':qid,'subject':q['subject'],'title':q['title'],'date':q['date'],'sourceId':sourceid,'state':'queued','questionPublished':True,'freshFourPanelRequired':True,'requiredImageCount':4,'reason':'新來源完整原題已收入；四張實際圖及隔離/正式QA仍待製，不算整體完成。'});cp['updatedAt']=now;save(ROOT/'docs/comics/progress.json',cp)
   receipt['items'].append({'id':qid,'draftPath':str(rel(item['draftPath'])),'draftSHA256':item['draftSHA256'],'reviewPath':str(rel(item['reviewPath'])),'reviewSHA256':digest(item['reviewPath']),'publishedAt':now,'fourImageState':'queued'});save(receipt_path,receipt)
   plan=read(plan_path);plan['newQuestionIds']=list(dict.fromkeys(plan['newQuestionIds']+[qid]));plan['publishedQuestionIds']=list(dict.fromkeys(plan['publishedQuestionIds']+[qid]));plan['updatedAt']=now;save(ROOT/plan_path,plan)
  published.append(qid)
 print(json.dumps({'published':published,'manifest':str(manifest_path)},ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--plan',default='docs/imports/new-gpt-20261116/plan.json');a=p.parse_args();main(a.manifest,a.plan)
