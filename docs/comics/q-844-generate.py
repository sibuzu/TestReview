from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def t(x,y,z,size=10,c='#284d4d'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def rect(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 def p(x,y):s.append(f'<circle cx="{o+x}" cy="{y}" r="6" fill="#dca28c" data-proton="true"/>');t(x,y+3,'+',9)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eef3e7","#eaf1f4","#faf0e6"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,19,'題目問：質子總數',11)
  for y,vals,c in [(37,['元素','氫','氧'],'#e6eadd'),(68,['原子序','1','8'],'#bfd7b0'),(99,['質量數','1','16'],'#f0eee6')]:
   rect(8,y,164,29,c)
   for x,z in zip([45,107,148],vals):t(x,y+20,z,11)
  t(90,151,'用原子序，不用質量數',11)
  t(90,176,'資料照原卷，不換欄位',8)
 elif i==1:
  t(90,20,'H₂O：2個H＋1個O',12)
  s.append(f'<path d="M{o+90} 76L{o+44} 112M{o+90} 76L{o+136} 112" stroke="#72958e" stroke-width="3"/>')
  for x,y,z,num,col in [(90,76,'O',8,'#dca28c'),(44,112,'H',1,'#d8e7e9'),(136,112,'H',1,'#d8e7e9')]:
   s.append(f'<circle cx="{o+x}" cy="{y}" r="23" fill="{col}" stroke="#698880" data-atom="{z}" data-protons="{num}"/>');t(x,y-2,z,12);t(x,y+14,f'{num}個質子',8)
  t(90,160,'別漏掉H的下標2',11)
  t(90,177,'僅組成示意，非實際鍵角',8)
 else:
  t(90,20,'把每個原子的質子加總',10)
  rect(8,36,59,54,'#e5eacf');rect(91,36,80,54,'#e5eacf')
  p(25,62);p(51,62);t(79,68,'+',13)
  for y in [50,75]:
   for x in [105,122,139,156]:p(x,y)
  t(38,108,'2個H：2',10);t(131,108,'1個O：8',10)
  t(90,142,'2×1＋8＝10',18)
  t(90,169,'每個小圓點代表1個質子',9)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-844.svg');a.write_text(''.join(s))
d={'id':'q-844','subject':'Physics-Chemistry','title':'水分子算質子，要用原子序乘原子個數','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-844-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 質子數，對照原子序那一列','text':'原子序就是原子含有的質子數。原表氫的原子序是1，氧是8；質量數1和16則包括質子與中子，不能拿來算本題的質子總數。','alt':'新製原卷表原子序1/8、質量數1/16完整摘錄，高亮原子序，不混兩列。'},
{'heading':'② 一個H₂O，有2個氫和1個氧','text':'化學式H₂O的下標2，表示每個水分子裡有2個氫原子；氧沒有另寫下標，表示1個。每個氫有1個質子，每個氧有8個，兩個氫都要算。','alt':'新精確H2O組成示意一O兩H，各標8或1個質子，不畫實際次原子位置或聲稱鍵角比例。'},
{'heading':'③ 分別加總，得到10個質子','text':'兩個氫提供2×1＝2個質子，一個氧提供8個，總共2×1＋8＝10。算成9是漏掉一個氫；算成18則用了質量數，回答的是別的數量。','alt':'新精確2個氫質子點加8個氧質子點共10，圓點同色同符號，獨立顯示原子來源分組，不代表質子有不同種類。'}],
'fourth':{'answer':'答案 B：10個質子','points':['先認清問質子總數，不是質量數或電子數。','H₂O有2個H、1個O，不能漏算氫。','原子序計算：2×1＋8＝10。']},
'protectedWords':['質子總數','原子序','質量數','質子與中子','H₂O','2個氫原子','1個質子','8個質子','10個質子','2×1＋8＝10','2×1＝2','電子數'],
'originalChecked':{'images':['site/dist/assets/questions/gemini063-774ab725ca4693.jpg'],'visualChecked':True,'answer':'B','notes':'原第5完整四數選項/表格與紅圈文字親見，清楚是質子總數，原子序1/8質量數1/16，黑D紅B。'},
'sourceUrl':'https://share.gemini.google/SBtc8Pxn9RX4','answerCheckedAgainst':'原卷表與H2O組成獨立計算2*1+8=10選B，原子序/質量數定義核OpenStax原子結構。',
'references':[{'title':'OpenStax Chemistry 2e 2.3 Atomic Structure and Symbolism','url':'https://openstax.org/books/chemistry-2e/pages/2-3-atomic-structure-and-symbolism','supports':'原子序為質子數，質量數為質子與中子總數','access':'前題已實讀同頁主文48-50段'}],
'rationale':'用精確SVG表格欄位/水分子原子個數/10質子點計數，直接降低混質量數與漏下標的錯誤，不需人物或AI猜數量；原卷保留。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selected':'B','atomicNumbers':{'H':1,'O':8},'massNumbersNotUsed':{'H':1,'O':16},'atoms':{'H':2,'O':1},'protons':10,'diagramDotCount':10,'molecularGeometryClaimed':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
assert 2*1+8==10 and 2*1+16==18
Path('docs/comics/q-844.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
