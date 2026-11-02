from pathlib import Path
import json, shutil, hashlib
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3]
colors=['#e6f2f5','#eaf3ed','#f7eee0']
def document(x,y,color='#e3b76a'):
 return f'<g transform="translate({x} {y})"><rect x="-13" y="-19" width="26" height="36" rx="4" fill="white" stroke="{color}" stroke-width="2"/><path d="M-6-9H6M-6-2H6M-6 5H2" stroke="{color}" stroke-width="2" stroke-linecap="round"/></g>'
def person(x,y,color):
 return f'<g transform="translate({x} {y})"><circle r="22" fill="white" stroke="{color}" stroke-width="2"/><circle cy="-6" r="7" fill="{color}"/><path d="M-12 15V11a12 12 0 0 1 24 0v4" fill="{color}"/></g>'
def courthouse(x,y,color='#56817a'):
 return f'<g transform="translate({x} {y})"><rect x="-27" y="-31" width="54" height="62" rx="9" fill="white" stroke="{color}" stroke-width="1.5"/><path d="M-20-10L0-23 20-10ZM-20 19H20M-22 24H22" fill="{color}" stroke="{color}" stroke-width="3" stroke-linejoin="round"/><path d="M-13-6V14M0-6V14M13-6V14" stroke="{color}" stroke-width="5"/></g>'
def arrow(x1,y1,x2,y2,color='#528a83'):
 return f'<path d="M{x1} {y1}H{x2}" stroke="{color}" stroke-width="3.5" fill="none" marker-end="url(#arrow)"/>'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 540 180"><defs><marker id="arrow" viewBox="0 0 8 8" markerWidth="6" markerHeight="6" refX="6.5" refY="4" orient="auto"><path d="M1 1L7 4L1 7" fill="none" stroke="#528a83" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker><pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#7c9a97" opacity=".15"/></pattern></defs>']
for i,bg in enumerate(colors):
 svg.append(f'<g transform="translate({180*i})"><rect width="180" height="180" rx="14" fill="{bg}"/><rect x="5" y="5" width="170" height="170" rx="11" fill="url(#dots)"/><rect x="12" y="30" width="156" height="120" rx="15" fill="white" opacity=".55"/>')
 if i==0:
  svg.append(person(42,65,'#558dba'));svg.append(person(42,114,'#789774'))
  svg.append('<path d="M64 65H76V90H98M64 114H76V90" fill="none" stroke="#528a83" stroke-width="2.5"/>')
  svg.append(arrow(85,90,100,90));svg.append(courthouse(135,90));svg.append(document(88,52))
 elif i==1:
  svg.append(person(38,90,'#558dba'));svg.append(document(89,55));svg.append(arrow(66,90,108,90));svg.append(person(138,90,'#bd9652'))
  svg.append('<rect x="117" y="119" width="42" height="14" rx="4" fill="#e6c991" stroke="#bd9652"/><path d="M132 119v-4h12v4" fill="none" stroke="#bd9652" stroke-width="2"/>')
 else:
  svg.append(person(38,90,'#bd9652'));svg.append(arrow(66,90,100,90));svg.append(courthouse(135,90));svg.append(document(86,52))
  svg.append('<path d="M16 128H58" stroke="#bd9652" stroke-width="3" stroke-linecap="round"/>')
 svg.append('</g>')
svg.append('</svg>')
art=ROOT/'docs/comics/art/q-875-polish-flow.svg';art.write_text(''.join(svg)+'\n')
p=ROOT/'docs/comics/q-875.json'
backup=ROOT/'docs/comics/civics-polish-20261101/q-875-anime-attempt.json'
if not backup.exists(): shutil.copyfile(p,backup)
s=json.loads(p.read_text());s.update(art=str(art.relative_to(ROOT)),generationMethod='authored native SVG procedure diagram; all labels/rules in selectable HTML',rationale='使用者2026-11-01補充：流程與關係依內容用SVG。此題教學重點是兩條提告途徑及公訴角色，故將已產出的動漫留作本機素材，改為精確分流/送交路徑。原題、答案B與所有解說文字保留。',sourceAIUsed=False,artSHA256=hashlib.sha256(art.read_bytes()).hexdigest(),visualChecked=False,updatedAt=datetime.now(timezone.utc).isoformat())
for k in ['rootReview','nativeArt','validationFile']:s.pop(k,None)
for p,alt in zip(s['panels'],['藍色被害人與綠色律師的兩個節點合流，再向右送交法院；自訴角色與名稱見右側HTML。','藍色被害人向右送交資料至金色檢察官節點；這是告訴，不將箭頭直接連到法院。','金色檢察官向右送交法院的公訴路徑；提起者與另一種自訴的差別見HTML。']):p['alt']=alt
p=ROOT/'docs/comics/q-875.json';p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
