import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def rect(x,y,w,h,fill='#e4ecdc',stroke='#bdcdbc'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>')
def ln(x1,y1,x2,y2):s.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="#95ad9d" stroke-width="2"/>')
for i in range(3):rect(i*200+2,2,196,196,'#faf8ee')
t(100,23,'不分軒輊',21)
t(100,51,'比較實力或成就',16)
rect(27,74,146,23,'#cbdfe9');rect(27,112,146,23,'#e3cfb3')
t(100,86,'甲',16);t(100,124,'乙',16)
t(100,162,'分不出高下',19);t(100,185,'條帶只示意詞義',12,'#7b9183')
t(300,23,'本文：朋友互相分享',17)
for x,y in [(238,65),(362,65),(238,146),(362,146)]:
 s.append(f'<circle cx="{x}" cy="{y}" r="17" fill="#e0e9d6" stroke="#8fa78f"/>');t(x,y,'友',16)
for a,b in [((249,76),(284,98)),((351,76),(316,98)),((249,135),(284,114)),((351,135),(316,114))]:ln(*a,*b)
rect(270,89,60,36,'#f0dfc7');t(300,107,'分享',17)
t(300,180,'不分彼此',20,'#a16c3e')
t(500,23,'A、B、C各有相合語境',15)
for y,a,b in [(56,'往事多','不可勝數'),(105,'感動難言','不可言喻'),(154,'謠言自破','不攻自破')]:
 rect(412,y-19,176,42);t(500,y-5,a,14);t(500,y+13,b+' ✓',16)
s.append('</svg>');Path('docs/comics/art/q-509.svg').write_text(''.join(s))
j={'id':'q-509','subject':'Chinese','title':'比較高下，和朋友分享是兩種語境','art':'docs/comics/art/q-509.svg','protectedWords':['不分軒輊','不分彼此','不可勝數','不可言喻','不攻自破','歷歷在目','數量','實力','高下','互相分享'],'panels':[{'heading':'① 不分軒輊，重點是比較高下','text':'這個成語比喻雙方實力或成就相當，分不出高下。它談的是比較優劣，不是單純表示朋友相處融洽或願意互相分享。','alt':'甲乙兩條等長語意條帶，只示意高下相當，沒有原題分數、勝負或實際測量資料。'},{'heading':'② D的互相分享，較接近不分彼此','text':'D先說各自在不同領域發展，後說互相分享，重點在朋友不分彼此。把「不分軒輊」放進來，轉成比較誰強誰弱，與本句想表達的意思不合。','alt':'四個抽象朋友節點連至中央分享，不畫成競賽排名；不冒稱角色肖像或原題實際事件細節。'},{'heading':'③ A、B、C把意思放回句子都通順','text':'A往事多得數不清，與記憶清楚並不衝突。B重聚感動難以言表。C朋友真實重聚，讓不和謠言自行瓦解。三句都能對應各自成語。','alt':'往事多、感動難言、謠言自破依序對應不可勝數、不可言喻、不攻自破，與原四選項A/B/C順序一致。'}],'fourth':{'answer':'答案 D：不分軒輊用錯語境','points':['不分軒輊：實力相當，難分高下。','互相分享：本句要表達朋友不分彼此。','A的不可勝數指數量多；「勝」讀ㄕㄥ，指盡。']},'rationale':'實看完整第2題四句及最不恰當設問，讀來源48–80，教育部成語典/簡編本比對不分軒輊高下義與勝讀音。採精確語意SVG比較條帶/分享網絡/ABC配對，比隨意聚會人物更直接揭示比較與分享差異；等長條帶僅詞義示意非原題新增分數。角色原名保留題目不另畫肖像，D答案不變，A記憶清晰與數量多不相斥。','sourceUrl':'https://share.gemini.google/hQs2FZHTr4er','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-509-source-78da1945ba.jpg','site/dist/sources/gemini-hQs2FZHTr4er.txt lines48–80'],'references':[{'url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=1942&la=0&powerMode=0','access':'official Ministry of Education full search-result entry excerpt','supports':'不分軒輊比喻分不出高下、實力相當'},{'url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=20760&la=0&powerMode=0','access':'official Ministry of Education full search-result entry excerpt','supports':'不可勝數讀ㄕㄥ，數量非常多'}],'answerCheckedAgainst':'D的互相分享並非比較實力，最不恰當；ABC語境分別數量多/感動難言/謠言自行破除，成立。','generationMethod':'precise native SVG lexical contrast, four-person sharing graph and ordered phrase-context matches','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-509.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
