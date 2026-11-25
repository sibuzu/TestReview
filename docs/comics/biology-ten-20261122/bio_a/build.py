"""Build only this producer's isolated specs; root publishes the shared bank."""
import hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[4];D=Path(__file__).parent
def load(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
for qid in sys.argv[1:]:
 q=load(D/f'{qid}-baseline.json');c=load(D/f'{qid}-content.json');g=load(D/f'{qid}-generation.json');assert len(g)==4
 imgs=[x['destination']for x in g];assert len(set(x['sha256']for x in g))==4
 s=dict(id=qid,subject='Biology',title=c['title'],art=imgs[0],layoutVersion='native-four-images-v7',generationMethod='four separate built-in image_gen calls; new near-realistic high-quality biology textbook illustrations',sourceGeneratedArtUsed=False,reusedOldGeneratedArt=False,originalMaterialsChecked=True,originalMaterials=['site/dist/'+p for p in q['images']]+['site/dist/'+f['src']for f in q.get('questionFigures',[])],answerCheckedAgainst=q['explanation'],rationale=c['rationale'],producerAgent='/root/bio_a',visualChecked=False,panels=[dict(heading=x[0],text=x[1],image=imgs[i],alt=c['alts'][i])for i,x in enumerate(c['panels'])],fourth=dict(answer=c['answer'],points=c['points'],image=imgs[3],alt=c['alts'][3]),protectedWords=c['protectedWords'],manualLineBreaks=False,promptFile=str((D/f'{qid}-prompts.json').relative_to(R)),generationEvidence=str((D/f'{qid}-generation.json').relative_to(R)),artHashes={x['destination']:x['sha256']for x in g},supportingSources=c.get('sources',[]),createdAt=datetime.now(timezone.utc).isoformat())
 s['panels'][0]['caption']='新製科學教材插畫，非原卷或實拍；圖中文字說明以本頁為準。'
 save(D/f'{qid}-spec.json',s)
 print(qid)
