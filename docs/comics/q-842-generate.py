from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def t(x,y,z,size=10,c='#284d4d'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(x,y,w,h,z,c='#dbe8ce',size=9):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>');t(x+w/2,y+h/2+3,z,size)
 def line(x,y,xx,yy):s.append(f'<path d="M{o+x} {y}L{o+xx} {yy}" stroke="#7b9690" stroke-width="1.5" fill="none"/>')
 def atom(x,y,z,c,r=11):s.append(f'<circle cx="{o+x}" cy="{y}" r="{r}" fill="{c}" stroke="#5c7473"/>');t(x,y+4,z,10)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e7","#f8efe6","#eaf1f4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,15,'依原分支讀層級',10)
  box(60,23,60,23,'純物質')
  for x in [36,124]:line(90,46,x,60)
  box(9,60,54,24,'單原子');box(94,60,60,24,'甲：分子')
  line(36,84,36,106);box(12,106,48,24,'例：He','#eff5fa',9)
  for x in [95,149]:line(124,84,x,105)
  box(71,105,48,24,'元素');box(125,105,49,24,'乙：化合物','#b7d6bf',8)
  line(95,129,95,148);line(149,129,149,148)
  box(78,148,34,20,'例丙',size=8);box(132,148,34,20,'例丁',size=8)
 elif i==1:
  t(90,16,'元素種類 ≠ 原子總數',10)
  t(28,39,'O₃',12);line(70,47,90,36);line(90,36,110,47)
  for x,y in [(70,47),(90,36),(110,47)]:atom(x,y,'O','#efb9a7',10)
  t(90,72,'3個O，仍只有1種元素',9)
  t(26,106,'CH₄',11)
  for x,y in [(88,91),(62,117),(114,117),(88,143)]:line(88,117,x,y)
  for x,y in [(88,91),(62,117),(114,117),(88,143)]:atom(x,y,'H','#f5f4e3',8)
  atom(88,117,'C','#d3c9aa',11)
  t(90,165,'C與H → 化合物',10)
  t(90,178,'只示組成，不表示真實鍵角',7)
 else:
  t(90,17,'丁：氨氣 NH₃',12)
  for x,y in [(90,43),(52,105),(128,105)]:line(90,78,x,y)
  for x,y in [(90,43),(52,105),(128,105)]:atom(x,y,'H','#f4f2de',13)
  atom(90,78,'N','#a9cbd6',17)
  t(90,138,'1個N＋3個H',12)
  t(90,158,'含兩種元素 → 化合物',10)
  t(90,177,'組成示意，非實際立體結構',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-842.svg');a.write_text(''.join(s))
d={'id':'q-842','subject':'Physics-Chemistry','title':'先讀分支層級，再分元素與化合物','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-842-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 乙與元素並列，不是與甲並列','text':'沿原圖走：純物質先分成單原子與甲，甲再分元素與乙。乙應是化合物；丙是元素的例子，丁是化合物的例子。不能把甲、乙都讀成最上層分類。','alt':'新製與原樹相同拓樸的直向分類：純物質到單原子He/甲分子，甲再到元素丙/乙化合物丁，沒有混合物分支。'},
{'heading':'② 原子多，不等於元素種類多','text':'臭氧O₃的一個分子有3個氧原子，仍只含氧一種元素，不是雙原子。甲烷CH₄含碳、氫兩種元素，是化合物，不能當丙的元素例子。','alt':'新精確組成圖O3為三O、CH4為一C四H，元素顏色與字母一致；只示組成，不表示實際鍵角或鍵級。'},
{'heading':'③ 氨氣NH₃，正好是丁的例子','text':'氨氣NH₃含氮、氫兩種元素，是化合物，所以乙填化合物、丁填氨氣合理。化合物可以是純物質；空氣才是多種氣體混合，不能放進這棵純物質分類樹。','alt':'新精確NH3組成圖一N三H、兩種元素，平面配置僅組成示意不當真實立體分子結構。'}],
'fourth':{'answer':'答案 D：乙是化合物，丁是氨氣','points':['先看分類層級，再核對例子所屬。','一種元素也能組成多原子分子，例如O₃。','CH₄與NH₃是化合物；空氣是混合物。']},
'protectedWords':['純物質','單原子','化合物','混合物','元素種類','臭氧O₃','甲烷CH₄','氨氣NH₃','O₃','CH₄','NH₃','雙原子','原子總數'],
'originalChecked':{'images':['site/dist/assets/questions/gemini063-9868223408c6d4.jpg'],'necessaryFigures':['site/dist/assets/questions/gemini063-a31647016429ed.jpg'],'visualChecked':True,'answer':'D','notes':'原題2完整四項及分類圖實看，甲是上分支，乙與元素同層、丙丁例子位置，紅D。'},
'sourceUrl':'https://share.gemini.google/SBtc8Pxn9RX4','answerCheckedAgainst':'原樹逐分支與四項獨立核D，甲烷/氨化學組成以NIST原資料對照；原題O3三O非雙原子，C空氣混合不合純物質根。',
'references':[{'title':'NIST Chemistry WebBook: Methane','url':'https://webbook.nist.gov/cgi/cbook.cgi?Name=CH4','supports':'CH4一碳四氫組成','access':'官方搜尋主文摘錄'},{'title':'NIST Chemistry WebBook: Ammonia','url':'https://webbook.nist.gov/cgi/cbook.cgi?ID=C7664417&Mask=2F','supports':'一氮三氫組成，常用式NH3','access':'官方搜尋主文摘錄'}],
'rationale':'本題錯誤來自樹的層級與原子數/元素種類混淆，精確SVG分類和組成圖比人物情境直接；所有標記可核對，不用來源AI，不讓生成模型決定原子數。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,
'diagramChecks':{'selected':'D','treeEdges':[['純物質','單原子'],['純物質','甲分子'],['甲分子','元素'],['甲分子','乙化合物'],['元素','丙'],['乙化合物','丁']], 'atomicCounts':{'O3':{'O':3},'CH4':{'C':1,'H':4},'NH3':{'N':1,'H':3}},'geometryOrBondOrdersClaimed':False,'mixtureUnderPureRoot':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
Path('docs/comics/q-842.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
