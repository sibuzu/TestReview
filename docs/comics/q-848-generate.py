from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def t(x,y,z,size=10,c='#284d4d'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(x,y,w,h,z,c='#dce7cf',size=12,tag=''):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}" {tag}/>');t(x+w/2,y+h/2+4,z,size)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eef3e7","#eaf1f4","#faf0e6"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,19,'一個鈉配一組氫氧根',11)
  box(9,42,64,40,'Na⁺','#c2d8e2',18,'data-ion="Na" data-charge="1"')
  box(105,42,65,40,'OH⁻','#d3e3bb',18,'data-ion="OH" data-charge="-1"')
  t(89,68,'+',16);t(90,111,'(+1)＋(−1)＝0',15)
  box(33,131,114,30,'NaOH','#bfd6a8',20)
  t(90,178,'配比示意，非分子或晶格形狀',7)
 elif i==1:
  t(90,19,'不能只見OH就加下標2',10)
  box(8,35,164,30,'Na⁺：OH⁻＝1：1',size=13)
  t(90,83,'NaOH',20)
  box(8,102,164,30,'Mg²⁺：OH⁻＝1：2','#c9dce3',12)
  t(90,156,'Mg(OH)₂',20)
  t(90,178,'先看陽離子電荷，再配平',8)
 else:
  t(90,18,'另外三式都能配成中性',10)
  for y,ion,formula in [(32,'Ca²⁺＋2Cl⁻','CaCl₂'),(79,'Cu²⁺＋SO₄²⁻','CuSO₄'),(126,'Ag⁺＋NO₃⁻','AgNO₃')]:
   box(9,y,162,43,'','#e3e7d5',10)
   t(90,y+16,ion,11);t(90,y+35,formula,15)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-848.svg');a.write_text(''.join(s))
d={'id':'q-848','subject':'Physics-Chemistry','title':'氫氧化物的下標，要看陽離子電荷','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-848-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 鈉與氫氧根，1：1就能中性','text':'Na⁺帶+1電，OH⁻帶−1電，一個對一組正好相抵，應寫NaOH。原卷A的Na(OH)₂多配一組OH，電荷總和成為−1，不是中性的氫氧化鈉配比。','alt':'新精確一Na+一OH−配平圖，電荷1減1為0、式NaOH；僅化學式比例非分子晶體結構。'},
{'heading':'② 和氫氧化鎂比較，不能硬套公式','text':'Mg²⁺帶+2電，才要兩組OH⁻，寫Mg(OH)₂；Na⁺只要一組，寫NaOH。不是所有氫氧化物都要括號加2，而是按離子電荷決定最簡比例。','alt':'新製Na+與Mg2+兩種陽離子對照：OH配比分別1比1與1比2，化學式不混用。'},
{'heading':'③ 再核對B、C、D的正確組合','text':'Ca²⁺配2個Cl⁻，是CaCl₂；Cu²⁺配一組SO₄²⁻，是CuSO₄；Ag⁺配一組NO₃⁻，是AgNO₃。三者電荷都可相抵，所以本題寫錯的是A。','alt':'新精確三列正確離子配比及化學式，Cu明用二價，SO4和NO3視為完整原子團，不分拆改下標。'}],
'fourth':{'answer':'答案 A：應寫NaOH，不是Na(OH)₂','points':['鈉+1、氫氧根−1，1：1就電中性。','鎂+2才需要兩組OH，與鈉不同。','化學式下標配整組原子團，先核對電荷。']},
'protectedWords':['Na⁺','OH⁻','NaOH','Na(OH)₂','Mg²⁺','Mg(OH)₂','Ca²⁺','Cl⁻','CaCl₂','Cu²⁺','SO₄²⁻','CuSO₄','Ag⁺','NO₃⁻','AgNO₃','氫氧化鈉','氫氧化鎂','電中性','原子團','最簡比例'],
'originalChecked':{'images':['site/dist/assets/questions/gemini063-bb640e3cb75fc3.jpg'],'visualChecked':True,'answer':'A','notes':'親見原第23全四名式與A確印Na(OH)2、紅A；原題錯式不改，解說訂正NaOH。'},
'sourceUrl':'https://share.gemini.google/SBtc8Pxn9RX4','answerCheckedAgainst':'原題四式獨立離子電荷相抵驗算A錯；OpenStax離子與原子團表及CaCl2主文核Na/Mg/Ca/Cu/Ag與OH/NO3/SO4。',
'references':[{'title':'OpenStax Chemistry 2e 2.6 Ionic and Molecular Compounds','url':'https://openstax.org/books/chemistry-2e/pages/2-6-ionic-and-molecular-compounds','supports':'常見離子電荷、OH/NO3/SO4原子團表、CaCl2與最簡離子比例','access':'主文與表2.5已讀'}],
'rationale':'新精確配平卡、鈉鎂反例、三個正例降低只背OH2的錯誤；不需人物或AI畫化學式，電荷與括號HTML可核對，原錯題保留。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selectedWrongOption':'A','correctFormula':'NaOH','neutralChargeChecks':{'NaOH':1-1,'Mg(OH)2':2-2,'CaCl2':2-2,'CuSO4':2-2,'AgNO3':1-1},'wrongNaOH2Charge':1-2,'claimsDiscreteMoleculeOrLattice':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
assert all(x==0 for x in d['diagramChecks']['neutralChargeChecks'].values()) and d['diagramChecks']['wrongNaOH2Charge']==-1
Path('docs/comics/q-848.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
