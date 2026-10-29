from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(y,t,color='#dce8d0'):s.append(f'<rect x="{o+12}" y="{y}" width="156" height="29" rx="5" fill="{color}"/>');txt(90,y+19,t,11)
 def path(d,col,w=1.5,extra=''):s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" {extra}/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#edf2f5","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  txt(90,18,'先讀題幹因果',11)
  for y,t in [(35,'產業用水需求增加'),(89,'超量抽取地下水'),(143,'地層下陷')]:
   box(y,t)
   if y<143:path(f'M{o+90} {y+31}v18m-4-5 4 5 4-5','#7b9988')
 elif i==1:
  txt(90,18,'海面不變，陸地下陷',11)
  s.append(f'<path d="M{o+10} 70L{o+170} 150V160H{o+10}Z" fill="#d4c19e"/><path d="M{o+50} 90H{o+170}V150Z" fill="#a9d2e0"/>')
  path(f'M{o+10} 45L{o+170} 125','#a78c6a',1.5,'stroke-dasharray="4 3"');path(f'M{o+10} 70L{o+170} 150','#956b36',2)
  path(f'M{o+48} 90H{o+171}','#3e819b',1.2)
  for x,col in [(100,'#927b60'),(50,'#a36132')]:s.append(f'<circle cx="{o+x}" cy="90" r="3" fill="{col}"/>')
  path(f'M{o+96} 106H{o+55}m5-4-5 4 5 4','#ad6f37',2)
  txt(113,79,'同一海面',10);txt(102,124,'岸線往陸側',10);txt(42,46,'原地面',9);txt(45,145,'下陷後',9)
  txt(90,177,'概念剖面，非實際比例',9)
 else:
  txt(90,18,'沿海相對高度降低',11)
  box(34,'受淹、海水入侵風險增加','#dce8ef');path(f'M{o+90} 66v19m-4-5 4 5 4-5','#7b9988')
  box(90,'海岸線可能向陸側後退');txt(90,147,'不是所有災害都能推得',10);txt(90,174,'D 與題幹因果最直接',11)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-057.svg';Path(art).write_text(''.join(s))
q={'id':'q-057','subject':'Geography','title':'陸地下陷後，海岸線可能向陸側退縮','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-057-generate.py','layoutVersion':'native-fluid-v6','panels':[{'heading':'① 用水需求增加，超抽造成下陷','text':'題幹先說用水需求增加，地面水不足、地下水使用成本較低，接著出現超抽與地層下陷。題目問後續環境災害，要沿這條因果鏈推理。','alt':'新製用水需求增加到超抽地下水再到地層下陷的三步關係圖，不以裂縫或山崩代替下陷機制。'},{'heading':'② 即使海面不變，陸地相對變低','text':'沿海地面下陷後，相對海面高度降低，更容易受海水影響。剖面用同一條海面與下移的地面比較，岸線可能向陸側移，不必先假設海水面真的上升。','alt':'新精確概念剖面固定海面，虛線原地面與實線下陷地面坡度相同，海面交點向左陸側移；圖不代表真實下陷數值或比例。'},{'heading':'③ D最直接；別只選常見的災害','text':'沿海受淹與海水入侵的可能提高，海岸線可能向陸地後退，最符合D。C土石流主要連到坡地、鬆散土石和大量水流；A白化、B汙染，也不能僅從這條因果鏈直接推得。','alt':'沿海相對變低到受淹風險再到岸線向陸側的結果圖，不聲稱任何內陸下陷都必然造成海岸後退。'}],'fourth':{'answer':'答案 D：海岸線後退','points':['超抽地下水 → 地層下陷。','沿海陸地相對海面變低，岸線可能向陸側移。','海岸後退是可能影響，不是把所有災害都歸給下陷。']},'protectedWords':['超抽地下水','地層下陷','相對海面','海岸線','海水入侵','陸側','因果鏈','土石流','鬆散土石','地面水','地下水'],'originalChecked':{'images':['site/dist/assets/questions/q-057-source-d880e4b001.jpg'],'visualChecked':True,'answer':'D','notes':'親見3題完整段落及四項珊瑚白化/重金屬汙染/土石流/海岸線後退，題幹用水增加超抽下陷順序清楚，D維持。'},'rationale':'題目重陸地下陷與相對海面/岸線的關係，選新精確SVG剖面與因果流程，比人物淹水情境更能說清不必實際海面上升；不使用來源AI，不混淆地下含水層侵入與地表海岸所有機制。','answerCheckedAgainst':'原題因果與四項比對，D沿海相對高度下降最直接；水利署官方海岸/下陷資訊及林業保育署地景資料支持，僅表可能影響，不假造範圍或速度。','sourceUrl':'https://chatgpt.com/share/6ae05333-3804-83eb-9608-4aaec1763e54','references':[{'title':'水利署電子報：外傘頂洲變遷與嘉義海岸防護','url':'https://www.wra.gov.tw/epaper/Article_Detail.aspx?n=30173&s=3464','checked':'沿岸地層下陷與近岸海水相對抬升、海岸後退關係，官方搜尋結果主文摘要已讀。'},{'title':'林業保育署臺灣地景保育網：海岸地形與開發影響','url':'https://landscape.forest.gov.tw/Front/LandscapeNews/communication/Periodicals.aspx?Cn=20&Sn=146&id=7KShBTi6PLM%3D','checked':'沿海超抽地下水引致地層下陷、海岸線後退。'}],'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'seaLevelY':90,'oldLandYAtX10':45,'newLandYAtX10':70,'slope':0.5,'oldShorelineX':100,'newShorelineX':50,'landwardIsLeft':True,'seaLevelIncreasedInDiagram':False,'coordinatesAreActualMeasurements':False},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
# Read canonical source rather than guessing a share URL.
D=json.loads(Path('site/dist/data.json').read_text());sourceId=next(x['sourceId'] for x in D['questions'] if x['id']=='q-057');q['sourceUrl']=next(x['url'] for x in D['sources'] if x['id']==sourceId)
Path('docs/comics/q-057.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
