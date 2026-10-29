from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def t(x,y,z,size=10,c='#284d4d'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(y,z,c='#dae6cd',size=10):s.append(f'<rect x="{o+8}" y="{y}" width="164" height="28" rx="4" fill="{c}"/>');t(90,y+18,z,size)
 def atom(x,y,z,c,stage):s.append(f'<circle cx="{o+x}" cy="{y}" r="12" fill="{c}" stroke="#658581" data-element="{z}" data-stage="{stage}"/>');t(x,y+4,z,10)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e7","#faf0e6","#eaf1f4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'不同元素：質量、性質不同',10)
  s.append(f'<circle cx="{o+53}" cy="55" r="21" fill="#d5a99a"/><circle cx="{o+125}" cy="55" r="21" fill="#99bccb"/>')
  t(53,60,'A',13);t(125,60,'B',13)
  t(90,91,'不是以不同幾何形狀分類',10)
  s.append(f'<path d="M{o+39} 143L{o+53} 113L{o+67} 143Z" fill="#d3d8d1"/><rect x="{o+113}" y="115" width="27" height="27" fill="#d3d8d1"/><path d="M{o+24} 107L{o+153} 153M{o+153} 107L{o+24} 153" stroke="#b67963" stroke-width="2"/>')
  t(90,176,'圓球是模型示意，非真實外觀',8)
 elif i==1:
  t(90,17,'當時理論 ≠ 今日全部結論',10)
  box(32,'B：同元素原子質量相同',size=9)
  box(66,'C：原子不可分割',size=10)
  s.append(f'<path d="M{o+90} 101v12m-3-3 3 3 3-3" stroke="#8b9c91" fill="none"/>')
  box(121,'後來：同位素、次原子粒子','#e0e8ef',9)
  t(90,175,'本題核對道耳頓當時的內容',9)
 else:
  t(90,18,'D：化學反應重新排列',10)
  for stage,y in [('before',53),('after',125)]:
   pairs=[(42,'A','#d5a99a'),(67,'A' if stage=='before' else 'B','#d5a99a' if stage=='before' else '#99bccb'),(114,'B' if stage=='before' else 'A','#99bccb' if stage=='before' else '#d5a99a'),(139,'B','#99bccb')]
   s.append(f'<path d="M{o+42} {y}H{o+67}M{o+114} {y}H{o+139}" stroke="#587977" stroke-width="2"/>')
   for x,z,c in pairs:atom(x,y,z,c,stage)
  s.append(f'<path d="M{o+90} 78v19m-4-4 4 4 4-4" stroke="#587977" fill="none" stroke-width="2"/>')
  t(90,157,'前後A各2、B各2',11)
  t(90,176,'假設組合，非特定化學反應',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-843.svg');a.write_text(''.join(s))
d={'id':'q-843','subject':'Physics-Chemistry','title':'辨認道耳頓當時理論，不混用後來修正','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-843-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① A的不同形狀，不是本題理論內容','text':'道耳頓用不同質量與性質區分不同元素的原子，不是說一種元素是三角形、另一種是正方形。A把差異說成形狀不同，因此是本題要找的錯誤卡片。','alt':'新製同為圓球但不同色的假設原子模型，以及被叉掉的三角形方形分類，明示模型非真實原子外觀或定量大小。'},
{'heading':'② B、C要放回當時的原子說','text':'相同元素原子質量相同、原子不可分割，都是當時原子說的觀點。後來同位素與次原子粒子知識會修正它們，但題目問歷史理論內容，不能因此改選B或C。','alt':'新製B/C當時理論到後來同位素與次原子粒子修正的概念對照，沒有宣稱當時說法至今全部正確。'},
{'heading':'③ D重排原子，種類與數量守恆','text':'化學反應把原子重新排列組合，符合道耳頓原子說。示意圖前後都有2個A原子、2個B原子，只改變組合；不是把原子消滅或憑空生出新原子。','alt':'新製假設A2+B2重新組成兩組AB，前後A/B各二，無指定真實元素反應或精確鍵角，符號為抽象計數。'}],
 'fourth':{'answer':'答案 A：第一組的形狀說法錯誤','points':['題目問哪張卡片不屬道耳頓當時理論。','B、C可在現代被修正，仍是當時觀點。','D只重組原子，化學反應前後種類與數量不變。']},
'protectedWords':['道耳頓','原子說','三角形','正方形','同位素','次原子粒子','重新排列組合','2個A原子','2個B原子','化學反應','當時理論'],
'originalChecked':{'images':['site/dist/assets/questions/gemini063-a82209115fea51.jpg'],'visualChecked':True,'answer':'A','notes':'親見第4題幹問道耳頓原子說寫法錯誤，四卡全句與黑C紅A；B/C歷史條件不以現代概念改答。'},
'sourceUrl':'https://share.gemini.google/SBtc8Pxn9RX4','answerCheckedAgainst':'原卷四卡與題幹歷史理論範圍，OpenStax早期原子說與現代原子結構主文交叉核對；選A，B/C後來修正界線保留。',
'references':[{'title':'OpenStax Chemistry 2e 2.1 Early Ideas in Atomic Theory','url':'https://openstax.org/books/chemistry-2e/pages/2-1-early-ideas-in-atomic-theory','supports':'道耳頓元素原子質量性質、化學變化重排不創生消滅','access':'主文已讀'},{'title':'OpenStax Chemistry 2e 2.3 Atomic Structure and Symbolism','url':'https://openstax.org/books/chemistry-2e/pages/2-3-atomic-structure-and-symbolism','supports':'現代次原子結構及同元素依質子數定義，不混問歷史','access':'主文已讀'}],
'rationale':'用精確原生原子模型/歷史現代對照/重組守恆計數，比人物更清楚避免選C；圖標都可核對，無來源AI、不讓模型決定原子數。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selectedWrongCard':'A','historicalBAndCPreserved':True,'hypotheticalReaction':{'before':{'A':2,'B':2},'after':{'A':2,'B':2}},'realAtomicShapeClaimed':False,'specificChemicalReactionClaimed':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
Path('docs/comics/q-843.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
