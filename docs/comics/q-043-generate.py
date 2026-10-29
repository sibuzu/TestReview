import math,json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300"><defs><marker id="up" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#3f8558"/></marker><marker id="down" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#b07746"/></marker></defs>']
def rect(x,y,w,h,fill,stroke='#bdc9be',r=5):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')
def text(x,y,t,size=22,c='#2b493a',wt=500):s.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" fill="{c}" font-weight="{wt}">{escape(t)}</text>')
def water(top=92):
 rect(14,top,272,250-top,'#dceef7',r=0);s.append(f'<path d="M14 {top}V250H286V{top}M14 {top}H286" fill="none" stroke="#638ba3" stroke-width="2"/>')
for i in range(3):
 s.append(f'<g transform="translate({i*300},0)">');rect(0,0,300,300,'#faf8ee',stroke='none')
 if i==0:
  text(150,25,'密度＝質量÷體積',23,wt=700)
  for y,label,form,res,state,c in [(54,'甲','40÷50','0.8','浮','#dfeadb'),(119,'乙','30÷60','0.5','浮','#e1eaf2'),(184,'丙','60÷30','2','沉','#f0e3d2')]:
   rect(15,y,270,51,c);text(35,y+25,label,23);text(118,y+25,form+'＝'+res,21);text(258,y+25,state,22,wt=700)
  text(150,272,'與水的1 g/cm³比較',19)
 elif i==1:
  water(92)
  for x,m,v,label,color in [(40,40,50,'甲','#92b781'),(174,30,60,'乙','#d9b477')]:
   size=20*v**(1/3);f=m/v;top=92-size*(1-f);rect(x,top,size,size,color,stroke='#5f745d',r=0)
   # dashed liquid level crossing square makes submerged height apparent
   s.append(f'<path d="M{x} 92H{x+size}" stroke="#467d99" stroke-width="2" stroke-dasharray="4 3"/>');text(x+size/2,top-18,label,24);text(x+size/2,190,str(m)+' gw',25,wt=700)
  text(150,225,'漂浮：B＝物重',24,c='#36784d');text(150,278,'浸水比例：甲80% · 乙50%',18)
 else:
  water(55);text(150,25,'丙：完全浸水',23,wt=700)
  size=20*30**(1/3);x=78;y=103;rect(x,y,size,size,'#d8ac85',stroke='#8e725b',r=0);text(x+size/2,y+size/2,'30 cm³',18)
  # force diagram placed to the side; both shafts share origin and same force scale
  s.append('<path d="M214 137V101" stroke="#3f8558" stroke-width="4" marker-end="url(#up)"/><path d="M214 137V209" stroke="#b07746" stroke-width="4" marker-end="url(#down)"/>')
  text(213,78,'B＝30 gw',19,c='#3f8558');text(216,233,'W＝60 gw',19,c='#9c693c')
  text(104,189,'排水30 cm³',18);text(150,278,'B＜物重，仍會下沉',21,c='#9c693c')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-043.svg').write_text(''.join(s))
rows=[]
for name,m,v in [('甲',40,50),('乙',30,60),('丙',60,30)]:
 rho=m/v;floating=rho<1;disp=m if floating else v;b=disp;rows.append({'name':name,'mass':m,'volume':v,'density':rho,'floating':floating,'displacedCm3':disp,'buoyancyGw':b,'cubeSideSVG':20*v**(1/3),'submergedFraction':min(rho,1)})
assert [r['buoyancyGw'] for r in rows]==[40,30,30]
assert 40>30==30
assert rows[0]['submergedFraction']==.8 and rows[1]['submergedFraction']==.5
Path('docs/comics/q-043-physics-validation.json').write_text(json.dumps({'id':'q-043','pass':True,'rows':rows,'waterDensity':1,'correctOption':'C','cubeView':'upright square cross sections side lengths proportional to cbrt(volume), submerged height fractions0.8/0.5','Cstate':'fully immersed snapshot not contacting bottom, no false equilibrium B=W','CforceArrows':{'upwardBshaft':36,'downwardWshaft':72,'forceRatio':.5},'originalTableAndAllOptionsActuallyViewed':True},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-043','subject':'Physics-Chemistry','title':'先判浮沉，浮力不等於全部都用物重','art':'docs/comics/art/q-043.svg','protectedWords':['密度','漂浮','排水體積','甲、乙','40 gw','30 gw','60 gw','30 cm³','0.8','0.5','水密度','B甲＞B乙＝B丙'],'panels':[{'heading':'① 先算三個密度，分清浮與沉','text':'甲40÷50＝0.8，乙30÷60＝0.5，丙60÷30＝2，單位是g/cm³。和水密度1比較，甲、乙漂浮，丙下沉；不能先把三物體全當成完全浸水。','alt':'三列原表質量除以體積，甲0.8浮、乙0.5浮、丙2沉，對照水密度1；沒有把質量大小直接排成浮力大小。'},{'heading':'② 漂浮甲、乙：浮力等於自身重量','text':'甲漂浮時B甲＝40 gw，乙漂浮時B乙＝30 gw。甲只需排開40 cm³的水，乙排開30 cm³；不是把整個50、60 cm³都當排水體積。','alt':'正立方體剖面同尺度邊長依體積開三次方；甲80%高度浸水、乙50%，浮力40及30gw，不用整個體積。'},{'heading':'③ 沉入的丙：排開水重才是浮力','text':'丙完全浸水時，排開30 cm³的水，所以B丙＝30 gw。圖示未碰杯底的浸水片刻，物重60 gw大於浮力，會繼續下沉，不能把60 gw直接當浮力。','alt':'丙完全浸水且與杯底有間隙，方塊體積30cm³；旁列同尺度浮力向上30、物重向下60不等長箭頭，無靜止平衡或杯底支持力假象。'}],'fourth':{'answer':'答案 C：B甲＞B乙＝B丙','points':['甲40 gw，乙30 gw，丙30 gw。','漂浮體的排水體積只取浸水部分。','沉體浮力取排開水重，不直接等於物重。']},'rationale':'完整實看自然四原卷第10題質量40/30/60、體積50/60/30及四選項，讀原AI本題完整推導。獨立計密度與排水，B=40/30/30。新精確SVG依立方體邊長cbrt(V)、浮體浸水比例0.8/0.5、沉體完整浸水且不碰底的瞬間，避免畫成下沉也B=W或落底水壓歧義。OpenStax正文核阿基米德原理及浮體浸水比例，C不變，不採來源AI圖。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-043-source-c8108e8b9a.jpg','site/dist/sources/gemini-science.txt lines 933–1065'],'sourceUrl':'https://share.gemini.google/4y9jAamQ8xdh','sources':[{'url':'https://openstax.org/books/college-physics-2e/pages/11-7-archimedes-principle','note':'正文31–58浮力等於排開液體重、沉浮取決與物重比較；113–126浮體浸水比例。'}],'generationMethod':'precise native SVG cubic cross sections, submergence fractions, and unequal buoyancy-weight force diagram','answerCheckedAgainst':'密度0.8/0.5/2，甲乙漂浮排水40/30，丙全浸排30；浮力40>30=30，C。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-043.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
