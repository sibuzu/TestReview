from pathlib import Path
import json,hashlib
mapping={'甲':{'period':2,'group':1,'symbol':'Li','Z':3},'乙':{'period':4,'group':2,'symbol':'Ca','Z':20},'丙':{'period':2,'group':17,'symbol':'F','Z':9},'丁':{'period':2,'group':18,'symbol':'Ne','Z':10},'戊':{'period':3,'group':17,'symbol':'Cl','Z':17}}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def t(x,y,z,size=10,c='#284d4d'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(x,y,w,h,z,c='#dce7cf',size=11,tag=''):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}" {tag}/>');t(x+w/2,y+h/2+4,z,size)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eef3e7","#eaf1f4","#faf0e6"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,16,'位置核對（省略中間族）',10)
  groups=[1,2,17,18]
  for j,g in enumerate(groups):t(43+j*32,36,str(g),10)
  for p in [2,3,4]:
   t(13,64+(p-2)*32,str(p),10)
   for j,g in enumerate(groups):
    hits=[k for k,v in mapping.items() if v['period']==p and v['group']==g];label=hits[0] if hits else ''
    tag=f'data-marker="{label}" data-period="{p}" data-group="{g}"' if label else ''
    box(27+j*32,44+(p-2)*32,30,30,label,'#c4d8b3' if label else '#f7f8f1',12,tag)
  t(90,154,'戊在丙下方，不在丁下方',10)
  t(90,176,'左側為週期，上方為族號',8)
 elif i==1:
  t(90,18,'同一週期：向右原子序增',10)
  for x,z in [(10,'甲'),(70,'丙'),(130,'丁')]:box(x,35,40,29,z)
  t(60,55,'＜',11);t(120,55,'＜',11)
  t(90,82,'甲、丙、丁都在第2週期',9)
  box(16,100,148,27,'第3週期：戊更大','#d1e1e6',11)
  box(16,137,148,27,'第4週期：乙又更大','#b8d1db',11)
 elif i==2:
  t(90,18,'由大到小，用序號複核',10)
  order=sorted(mapping,key=lambda k:mapping[k]['Z'],reverse=True)
  for j,k in enumerate(order):
   v=mapping[k];box(12,29+28*j,156,25,f'{k}　{v["symbol"]}　{v["Z"]}',size=13,tag=f'data-rank="{j+1}" data-marker="{k}" data-Z="{v["Z"]}"')
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-846.svg');a.write_text(''.join(s))
d={'id':'q-846','subject':'Physics-Chemistry','title':'按週期與左右順序，比較原子序','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-846-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 先核對五點位置，戊在丙下方','text':'甲在第2週期左端；丙、丁在同列最右側，丁在丙右方。戊在丙下方的第17族，乙在第4週期。新圖省略中間族，只放本題需要的位置。','alt':'新精確省略中間族表列1/2/17/18族與2/3/4週期，甲2/1乙4/2丙2/17丁2/18戊3/17，位置同原卷而非完整週期表。'},
{'heading':'② 同列向右增加，再接下一週期','text':'原子序在同一週期由左向右增加，所以甲＜丙＜丁。戊在下一週期，原子序大於丁；乙又在第4週期，比這四個都大。不是單看整張圖的左右位置排序。','alt':'新製甲小於丙小於丁同列關係，再接第3戊與第4乙，明示按週期接續，非只讀幾何左右坐標。'},
{'heading':'③ 由大到小：乙、戊、丁、丙、甲','text':'按位置可直接得到乙＞戊＞丁＞丙＞甲，選B。也可用實際原子序複核：乙20、戊17、丁10、丙9、甲3；用的是原子序，不是原子量。','alt':'新精確由大至小20/17/10/9/3卡，對應Ca/Cl/Ne/F/Li與乙戊丁丙甲，不拿平均原子量排序。'}],
'fourth':{'answer':'答案 B：乙＞戊＞丁＞丙＞甲','points':['同週期由左向右，原子序逐一增加。','看完本週期，才接下一週期。','戊在第17族，丙正下方；不是丁正下方。']},
'protectedWords':['第2週期','第3週期','第4週期','第17族','第18族','原子序','原子量','甲＜丙＜丁','乙＞戊＞丁＞丙＞甲'],
'originalChecked':{'images':['site/dist/assets/questions/gemini063-e04978fb4a5b20.jpg'],'necessaryFigures':['site/dist/assets/questions/gemini063-e768e299e0bbae.jpg'],'visualChecked':True,'answer':'B','notes':'完整15四排序與必要表實看，戊確在丙第17族下方、乙4週期2族，紅B；不重開原AI欄位誤讀已訂正。'},
'sourceUrl':'https://share.gemini.google/SBtc8Pxn9RX4','answerCheckedAgainst':'原位置逐點對照，IUPAC2022週期表原子序Li3/F9/Ne10/Cl17/Ca20核實，降序乙戊丁丙甲B。',
'references':[{'title':'IUPAC Periodic Table of the Elements（4 May 2022）','url':'https://iupac.org/wp-content/uploads/2022/07/IUPAC_Periodic_Table-04May22_CRA.pdf','supports':'五位置元素與原子序3/9/10/17/20','access':'官方PDF全文數值與截圖調用核對'},{'title':'IUPAC：Periodic Table of Elements','url':'https://iupac.org/what-we-do/periodic-table-of-elements/','supports':'官方週期表及族號1–18','access':'官方主文已讀'}],
'rationale':'原錯誤風險是週期表欄位與排序規則，精確SVG縮列位置/同列增序/實際Z值最直接，不需人物或模型拼表，必要原卷表仍保留。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selected':'B','positionMapping':mapping,'descendingOrder':sorted(mapping,key=lambda k:mapping[k]['Z'],reverse=True),'compressedGroups':[1,2,17,18],'middleGroupsExplicitlyOmitted':True,'atomicWeightsUsed':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
assert d['diagramChecks']['descendingOrder']==['乙','戊','丁','丙','甲']
Path('docs/comics/q-846.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
