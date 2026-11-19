from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, html, sys, math
from PIL import Image
R=Path.cwd(); B=R/'docs/imports/new-gpt-20261119-73/lane2'; URL='https://chatgpt.com/share/6aff02c8-3e8c-83ec-ba50-ab1ab4a030a5'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def rel(p):return str(p.relative_to(R))
items=[
('q-1157',1,'9','化學第9題｜產生二氧化碳的反應',
 '下列哪一組物質反應後，會產生二氧化碳氣體？',
 ['鎂和稀硫酸','碳酸氫鈉和稀硫酸','雙氧水和二氧化錳','醋酸和氫氧化鈉'],'B',
 '答案B。碳酸氫鈉含碳酸氫根，與酸中的氫離子反應會生成二氧化碳和水：HCO₃⁻＋H⁺ → CO₂↑＋H₂O。整體反應可寫成2NaHCO₃＋H₂SO₄ → Na₂SO₄＋2CO₂↑＋2H₂O。\n\nA是金屬鎂與稀硫酸反應：Mg＋H₂SO₄ → MgSO₄＋H₂↑，產生氫氣。C是二氧化錳催化雙氧水分解：2H₂O₂ → 2H₂O＋O₂↑，產生氧氣，二氧化錳不是氧氣的來源。D是醋酸與氫氧化鈉中和：CH₃COOH＋NaOH → CH₃COONa＋H₂O，通常不產生氣體。不能只因反應物含碳，就認為會產生CO₂；要辨認反應種類。',
 ['鎂與稀硫酸產生H₂，不是CO₂。','碳酸氫根與酸反應生成CO₂和水。','雙氧水分解產生O₂，MnO₂為催化劑。','生成醋酸鈉和水，沒有CO₂產物。'],['化學反應','氣體製備'],(45,386,1040,653)),
('q-1158',2,'19','化學第19題｜反應係數與平衡莫耳數',
 '下列關於此反應的敘述，何者錯誤？',
 ['為可逆反應','大量加入H₂，可增加NH₃產量','改變壓力或溫度，會影響平衡狀態','達平衡時，N₂與NH₃的莫耳數比為1：2'],'D',
 '答案D。反應式N₂＋3H₂ ⇌ 2NH₃中的1：3：2，表示反應進行時各物質「消耗或生成的莫耳數比例」，不代表達到平衡時容器內各物質「剩餘的莫耳數比例」。例如在定容、定溫的密閉系統中，原有N₂為2 mol、H₂為6 mol，若某時已淨消耗N₂ 0.5 mol，則H₂淨消耗1.5 mol、NH₃淨生成1 mol；此時N₂與NH₃的量為1.5：1，並非1：2。這只是守恆計算例，不宣稱該組數字一定就是指定條件的平衡組成。真正平衡量仍取決於起始量與反應條件。\n\nA：雙向箭頭表示可逆反應；平衡時正、逆反應仍持續，速率相同，並非反應停止。B：在其他條件適當且不變時，加入H₂會使系統向消耗H₂、生成NH₃的方向調整。C：此反應氣體反應係數總和由左側4變右側2，改變體積造成的壓力變化可影響平衡；溫度也會改變平衡組成。D把反應比例誤當平衡存量，所以是錯誤敘述。\n\n原卷反應條件照錄200 atm、500°C及Fe₂O₃；本題判斷重點是反應係數與平衡量，不需藉更動原卷催化劑標示來作答。',
 ['雙向箭頭表示可逆；平衡不代表反應停止。','增加H₂後，平衡調整可增加NH₃產量。','體積引起的壓力改變及溫度改變都可能影響平衡。','係數1：2是反應變化量比，不是平衡時的存量比。'],['化學平衡','反應係數'],(45,543,985,1020)),
('q-1159',3,'3','化學第3題｜酯化所需試劑',
 '利用酯化反應製造乙酸乙酯時，最不需使用下列何種試劑？',
 ['NaCl','CH₃COOH','C₂H₅OH','H₂SO₄'],'A',
 '答案A。乙酸乙酯由乙酸與乙醇進行酯化而得：CH₃COOH＋C₂H₅OH ⇌ CH₃COOC₂H₅＋H₂O。乙酸提供酸的部分，乙醇提供醇的部分。\n\nB的CH₃COOH是乙酸，C的C₂H₅OH是乙醇，兩者都是反應物。D的H₂SO₄在這類國中酯化實驗中指濃硫酸，常作酸催化劑，促進反應，不能因它不是淨消耗的反應物就選D。A的NaCl不是酯化的反應物或酸催化劑，因此是四者中「最不需」的試劑。氯化鈉可在部分產物分離步驟用於鹽析，但那是後續分離用途，不是本題製備反應的必要試劑。',
 ['不是酯化反應物或酸催化劑，最不需使用。','乙酸是反應物。','乙醇是反應物。','濃硫酸可作酸催化劑。'],['有機化合物','酯化'],(35,486,1040,817)),
('q-1160',4,'7','化學第7題｜酸鹼中和的離子與導電性',
 '酸鹼中和是化學上重要的反應，關於酸鹼中和的敘述，下列何者錯誤？',
 ['反應式可表示為：酸＋鹼→鹽＋水','主要的反應物是酸性物質的陰離子與鹼性物質的陽離子','酸鹼中和反應是一種放熱反應','酸與鹼各自水溶液的導電性雖佳，但酸鹼中和後的水溶液之導電性可能很差'],'B',
 '答案B。國中常見的酸鹼中和，真正形成水的是酸提供的H⁺（陽離子）與鹼提供的OH⁻（陰離子）：H⁺＋OH⁻ → H₂O。B把兩者的離子正負性寫反，故為錯誤敘述。\n\nA：常見酸與鹼中和可表示為酸＋鹼→鹽＋水。C：以常見酸、鹼水溶液的中和而言，反應放熱，溫度可上升。\n\nD用了「可能」，不能把它讀成「一定」。例如HCl與NaOH恰好中和，Na⁺、Cl⁻仍留在水中，因此生成的NaCl水溶液仍可導電；中性不等於不導電。另一方面，H₂SO₄與Ba(OH)₂恰好反應時，同時生成難溶的BaSO₄沉澱和水：H₂SO₄＋Ba(OH)₂ → BaSO₄↓＋2H₂O，溶液中自由移動的離子大幅減少，導電性便可能很差，所以D是合理的可能情況。查核：[美國科羅拉多大學導電滴定示範](https://www.colorado.edu/lab/lecture-demo-manual/e790-acidbase-conductimetric-titration-baoh2-h2so4)。',
 ['為國中常見酸鹼中和的總表示式。','正負離子寫反；形成水的是H⁺與OH⁻。','常見酸鹼水溶液中和是放熱反應。','若同時生成難溶鹽，恰好反應後可少有自由離子；本項只說可能。'],['酸鹼中和','導電性'],(37,298,1003,695)),
('q-1161',5,'8','理化第8題｜兩物體綁合後的加速度',
 '質量m₁的甲物體受合力F作用下，加速度為a₁；質量m₂的乙物體受合力F作用下，加速度為a₂，若將甲、乙兩物體綁在一起，並受合力3F的作用，則其加速度為若干？',
 ['3a₁a₂','3a₁a₂／(a₁＋a₂)','(a₁＋a₂)／(a₁a₂)','a₁a₂'],'B',
 '答案B，a＝3a₁a₂／(a₁＋a₂)。先分別使用F＝ma：甲有m₁＝F／a₁，乙有m₂＝F／a₂。綁在一起時相加的是質量，不是原來兩個加速度；總質量m₁＋m₂＝F／a₁＋F／a₂。\n\n新合力已明確給成3F，因此a＝3F／(m₁＋m₂)＝3F／(F／a₁＋F／a₂)＝3／(1／a₁＋1／a₂)＝3a₁a₂／(a₁＋a₂)。F在分子、分母約掉，不必知道其數值。\n\nA漏掉分母a₁＋a₂；C是a₁、a₂倒數的和，不是本題加速度，也漏掉3；D只是兩加速度的乘積。還可檢查特例：若a₁＝a₂＝a₀，代表兩物體質量相同，綁合後質量變2倍、合力變3倍，故加速度應為1.5a₀，只有B符合。',
 ['漏了除以a₁＋a₂，且量綱也不對。','將m₁＝F／a₁、m₂＝F／a₂代入a＝3F／(m₁＋m₂)可得。','等於1／a₁＋1／a₂，不是本題加速度。','加速度不能直接相乘來代表綁合結果。'],['牛頓第二運動定律','合力與加速度'],(14,826,1068,971)),
('q-1162',6,'10','理化第10題｜由速度時間圖求平均摩擦力',
 'C羅用力一踢，質量0.3 kg的足球在草地上直線前進，場地旁邊的測速器測得其速度對時間關係如右圖所示，由此可以推算出草地的摩擦力大小平均為多少N？',
 ['45','4.5','450','0.45'],'D',
 '答案D，平均摩擦力大小為0.45 N。原圖顯示足球在t＝0時的速度為15 m/s，至t＝10 s降為0；t＝10～20 s則保持停止。求使球減速的草地平均摩擦力，應使用球仍在前進、受摩擦減速的0～10 s，不能把已停止的10～20 s一起當作減速時間。\n\n以前進方向為正，平均加速度a＝(0－15)／10＝－1.5 m/s²。水平方向造成減速的平均合力依題意視為草地摩擦力，F＝ma＝0.3×(－1.5)＝－0.45 N。負號表示摩擦力與前進方向相反；題目問大小，回答0.45 N。\n\nA的45、B的4.5、C的450都不符合0.3×15／10的結果。質量已用kg，無須再乘g；N與kgw也不能混用。球停止後若沒有其他水平推力，沒有必須維持0.45 N的動摩擦力；原圖水平段不是仍在以同一加速度減速。',
 ['比0.45 N大100倍，計算量級不符。','比0.45 N大10倍；需將速度變化除以10 s。','比0.45 N大1000倍，kg不必再轉成g代入。','0.3×(15／10)＝0.45 N。'],['速度時間圖','摩擦力'],(20,286,1040,453))]
ac=json.loads((R/'docs/imports/new-gpt-20261119-73/acquisition.json').read_text())
for qid,idx,num,title,stem,opts,ans,exp,analyses,tags,box in items:
 original=R/ac['downloadedImages'][idx-1]['path'];crop=B/'crops'/f'{qid}-original.png';im=Image.open(original);im.crop(box).save(crop)
 q=dict(id=qid,sourceId='src-more-073',subject='Physics-Chemistry',title=title,chapter='綜合',volume='綜合',date='2026-11-19',dateLabel='首次出題日期',addedAt='2026-11-19',question=stem+'\n'+'\n'.join(f'({chr(65+i)}) {v}' for i,v in enumerate(opts)),answer=f'({ans}) {opts[ord(ans)-65]}',explanation=exp,trap='',verification='原卷逐題核對',verificationNote='已實開真正User原卷、完整題幹及全部選項；日期取首次提問台灣日，非實際考試日。冊次章節無證據，歸綜合。',diagram='',notes='',status='todo',starred=False,tags=tags,images=[rel(crop)],sourceLabel=f'分享原卷｜第{num}題',studentAnswer=ac['downloadedImages'][idx-1]['userText'],contentStatus='完整原題',correctOption=ans,passage='',originalQuestionNumber=num,optionAnalysis=[dict(label=chr(65+i),text=v,wordClass='應選' if chr(65+i)==ans else '不選',meaning='',explanation=analyses[i]) for i,v in enumerate(opts)],tables=[],questionFigures=[],explanationFigures=[])
 if qid=='q-1158':q['passage']='「氨」是工業常用的原料，目前主要是利用哈伯法製造，反應式如下。試回答下列問題：\nN₂＋3H₂ ⇌ 2NH₃\n箭頭上方：200 atm、500°C；箭頭下方：Fe₂O₃（原卷標示照錄）。'
 if qid=='q-1162':
  fig=B/'crops'/f'{qid}-vt-original.png';im.crop((790,248,1040,453)).save(fig);q['questionFigures']=[dict(src=rel(fig),alt='原卷速度時間圖：0秒15 m/s，10秒降至0，20秒仍為0',caption='原卷作答必要速度時間圖，保留原始筆跡，非AI重製。')]
 save(B/'questions'/f'{qid}.json',q)
# SVG primitives: newly authored exact scientific diagrams, no source AI assets.
C={'ink':'#18324b','blue':'#2268b0','red':'#b5493c','green':'#287d65','light':'#edf5fc','gold':'#b27b16'}
def txt(x,y,t,size=19,fill=None,anchor='middle',weight=500):return f'<text x="{x}" y="{y}" fill="{fill or C["ink"]}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}">{html.escape(t)}</text>'
def line(x,y,x2,y2,color=None,w=3,dash=''):return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color or C["ink"]}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def arrow(x,y,x2,y2,color=None,w=5):
 dx,dy=x2-x,y2-y;length=math.hypot(dx,dy);ux,uy=dx/length,dy/length;px,py=-uy,ux
 a,b=x2-ux*12+px*7,y2-uy*12+py*7;c,d=x2-ux*12-px*7,y2-uy*12-py*7
 return line(x,y,x2,y2,color,w)+f'<path d="M{a} {b}L{x2} {y2}L{c} {d}" fill="none" stroke="{color or C["ink"]}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def circle(x,y,r,fill,stroke='#18324b'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def rect(x,y,w,h,fill,stroke=None,rx=8):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke or C["ink"]}" stroke-width="2"/>'
def beaker(x,y,label,bubbles=False,color='#c0dff1'):
 s=f'<path d="M{x} {y}V{y+126}Q{x} {y+140} {x+15} {y+140}H{x+109}Q{x+124} {y+140} {x+124} {y+126}V{y}" fill="none" stroke="#42627a" stroke-width="4"/>'+rect(x+4,y+61,116,74,color,stroke=color,rx=0)+txt(x+62,y+167,label,18)
 if bubbles:
  for bx,by,br in [(28,84,8),(73,98,7),(92,53,9),(55,30,7),(82,8,8)]:s+=circle(x+bx,y+by,br,'white',C['green'])
 return s

def molecule(x,y,kind,scale=1):
 def bond(a,b,c,d):return line(x+a*scale,y+b*scale,x+c*scale,y+d*scale,'#60738a',6*scale)
 def atom(a,b,r,t,col):return circle(x+a*scale,y+b*scale,r*scale,col)+txt(x+a*scale,y+b*scale+6*scale,t,int(18*scale))
 if kind=='co2':return bond(-48,0,48,0)+atom(-48,0,23,'O','#f2b1a7')+atom(0,0,23,'C','#d9e2ec')+atom(48,0,23,'O','#f2b1a7')
 if kind=='water':return bond(0,0,-31,29)+bond(0,0,31,29)+atom(0,0,24,'O','#f2b1a7')+atom(-31,29,17,'H','#edf5fc')+atom(31,29,17,'H','#edf5fc')
 if kind in ['n2','h2','o2']:
  atomn,col={'n2':('N','#a5c8ee'),'h2':('H','#eff6fc'),'o2':('O','#f2b1a7')}[kind];return bond(-20,0,20,0)+atom(-20,0,22,atomn,col)+atom(20,0,22,atomn,col)
 if kind=='nh3':return bond(0,0,0,-36)+bond(0,0,-32,24)+bond(0,0,32,24)+atom(0,0,23,'N','#a5c8ee')+atom(0,-36,16,'H','#eff6fc')+atom(-32,24,16,'H','#eff6fc')+atom(32,24,16,'H','#eff6fc')
 return ''
def axes(x=63,y=300,w=292,h=215,xlabel='t (s)',ylabel='v (m/s)'):
 return arrow(x,y,x+w,y,C['ink'],3)+arrow(x,y,x,y-h,C['ink'],3)+txt(x+w-4,y+55,xlabel,19,anchor='end')+txt(x+5,y-h-16,ylabel,18,anchor='start')+txt(x-13,y+24,'0',16)
def panel(q,n,body):
 p=B/'art'/f'{q}-panel-{n}.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 420" role="img"><defs><style>text{font-family:"Noto Sans CJK TC","Noto Sans TC",sans-serif}</style></defs><rect width="420" height="420" rx="22" fill="#f8fbfe"/>'+body+'</svg>');return rel(p)
ART={}
# 1157: different products, reaction bubbles, molecular product, matched pairs.
ART['q-1157']=[
 txt(210,39,'看反應種類，辨認氣體',23,weight=700)+beaker(32,95,'酸＋NaHCO₃',True)+molecule(290,155,'co2',.85)+txt(290,225,'CO₂',27)+txt(210,355,'碳酸氫鹽遇酸',25,fill=C['green'])+txt(210,389,'生成二氧化碳與水',22),
 txt(210,40,'B：碳酸氫根＋酸',23,weight=700)+rect(29,87,150,94,'#e6f0fb')+txt(104,145,'HCO₃⁻',28)+txt(210,145,'＋',29)+circle(307,130,42,'#f7d3cb')+txt(307,140,'H⁺',29)+arrow(210,190,210,236,C['green'])+molecule(121,297,'co2',.7)+molecule(304,283,'water',.8)+txt(210,383,'CO₂↑ ＋ H₂O',28,fill=C['green']),
 txt(210,40,'別把不同氣體混在一起',22,weight=700)+beaker(27,96,'A：Mg＋酸',True)+beaker(250,96,'C：H₂O₂',True)+molecule(89,82,'h2',.55)+molecule(312,82,'o2',.55)+txt(89,310,'H₂',29)+txt(312,310,'O₂',29)+txt(210,371,'C有MnO₂催化',22),
 txt(210,40,'B產CO₂；D只中和',24,weight=700)+beaker(30,130,'B：碳酸氫鈉',True)+beaker(262,130,'D：醋酸',False)+molecule(92,94,'co2',.5)+molecule(324,94,'water',.6)+txt(92,340,'＋稀硫酸',21)+txt(324,340,'＋NaOH',21)+txt(210,392,'選B；反應不同，產物不同',22)]
#1158 stoichiometry illustrated with balanced molecular counts, equilibrium exchange, added H2, inventory change bar graph.
ART['q-1158']=[
 txt(210,38,'每一反應份的比例',24,weight=700)+molecule(82,120,'n2',.65)+txt(82,175,'1 N₂',21)+molecule(222,105,'h2',.55)+molecule(317,105,'h2',.55)+molecule(270,167,'h2',.55)+txt(272,219,'3 H₂',21)+arrow(102,240,315,240,C['green'],4)+molecule(133,312,'nh3',.65)+molecule(280,312,'nh3',.65)+txt(210,388,'2 NH₃',24),
 txt(210,38,'平衡仍有雙向反應',24,weight=700)+molecule(77,103,'n2',.55)+molecule(45,185,'h2',.4)+molecule(108,185,'h2',.4)+molecule(77,244,'h2',.4)+molecule(325,108,'nh3',.55)+molecule(325,238,'nh3',.55)+arrow(145,143,271,143,C['blue'],4)+arrow(271,210,145,210,C['red'],4)+txt(210,308,'正反應速率＝逆反應速率',22)+txt(210,363,'存量恆定；反應仍持續',21),
 txt(210,38,'增加H₂後重新調整',23,weight=700)+rect(33,171,132,149,'#f5f9fc',C['ink'],23)+molecule(73,218,'n2',.42)+molecule(124,266,'h2',.4)+molecule(65,282,'h2',.4)+txt(99,344,'氣態反應系統',18)+molecule(99,111,'h2',.55)+arrow(99,143,99,180,C['blue'],4)+arrow(183,238,234,238,C['green'],4)+molecule(316,222,'nh3',.8)+txt(307,310,'NH₃增加',23,fill=C['green'])+txt(210,377,'其他條件適當且不變',20),
 txt(210,37,'變化量，不是平衡存量',23,weight=700)+txt(82,94,'例：起始',19)+txt(282,94,'反應後',19)+rect(67,150,48,160,'#a5c8ee')+rect(253,190,48,120,'#a5c8ee')+rect(315,230,48,80,'#b9decf')+txt(91,341,'N₂ 2',20)+txt(277,341,'1.5',20)+txt(339,341,'1',20)+txt(277,367,'N₂',18)+txt(339,367,'NH₃',18)+arrow(127,220,231,220,C['ink'],4)+txt(210,397,'mol；守恆計算例，非指定平衡',14)]
#1159 structures + reaction mapping + catalyst energy + NaCl lattice not participant.
ART['q-1159']=[
 txt(210,38,'先找酸與醇兩種反應物',23,weight=700)+txt(108,111,'乙酸',24)+txt(311,111,'乙醇',24)+txt(47,184,'CH₃',23)+line(73,177,91,177)+txt(109,184,'C',24)+line(124,177,144,177)+txt(169,184,'OH',23,fill=C['red'])+line(105,199,105,220,C['red'],3)+line(113,199,113,220,C['red'],3)+txt(109,252,'O',26,fill=C['red'])+txt(279,184,'C₂H₅',23)+line(308,177,327,177)+txt(353,184,'OH',23)+txt(210,328,'CH₃COOH＋C₂H₅OH',25)+txt(210,375,'兩者都是必要反應物',22),
 txt(210,38,'酯化生成乙酸乙酯與水',22,weight=700)+txt(52,126,'CH₃',24)+line(83,119,108,119)+txt(127,126,'C',25)+line(145,119,184,119)+txt(203,126,'O',25,fill=C['red'])+line(223,119,266,119)+txt(310,126,'C₂H₅',24)+line(122,141,122,178,C['red'],3)+line(132,141,132,178,C['red'],3)+txt(127,208,'O',27,fill=C['red'])+molecule(210,274,'water',1)+txt(210,372,'酯 ＋ 水',25),
 txt(210,38,'D：濃硫酸促進反應',23,weight=700)+axes(55,306,307,206,'反應進行','能量')+f'<path d="M60 267 Q112 30 180 125 T350 273" fill="none" stroke="{C["red"]}" stroke-width="4"/><path d="M60 267 Q128 118 190 207 T350 273" fill="none" stroke="{C["blue"]}" stroke-width="5"/>'+txt(280,100,'未催化',18,fill=C['red'])+txt(270,203,'酸催化',18,fill=C['blue'])+txt(210,389,'降低反應能障的概念圖',21),
 txt(210,38,'A：NaCl不參與這個酯化',22,weight=700)+''.join(circle(113+x*65,111+y*65,23,'#d0e5f7' if (x+y)%2 else '#d8eace')+txt(113+x*65,117+y*65,'Na⁺' if (x+y)%2 else 'Cl⁻',16) for x in range(4) for y in range(3))+txt(210,333,'氯化鈉晶格概念圖',21)+txt(210,378,'不是反應物或酸催化劑',21)]
#1160 ions and water, sodium chloride remains, sulfate precipitate and ionic counts.
ART['q-1160']=[
 txt(210,39,'先辨認形成水的離子',23,weight=700)+circle(104,137,45,'#f6c6bc')+txt(104,146,'H⁺',30)+circle(312,137,45,'#b9d9f2')+txt(312,146,'OH⁻',29)+arrow(104,200,167,261,C['green'],4)+arrow(312,200,250,261,C['green'],4)+molecule(210,291,'water',.95)+txt(210,390,'陽離子 ＋ 陰離子 → 水',22),
 txt(210,39,'HCl＋NaOH：鹽仍可導電',22,weight=700)+beaker(148,115,'NaCl水溶液',False)+circle(178,213,18,'#d0e5f7')+txt(178,219,'Na⁺',14)+circle(239,229,18,'#d8eace')+txt(239,235,'Cl⁻',14)+arrow(175,189,194,181,C['blue'],3)+arrow(243,206,225,197,C['green'],3)+txt(210,92,'仍有可移動離子',22)+txt(210,369,'中性不等於沒有離子',23),
 txt(210,39,'可能低導電：沉澱也生成',22,weight=700)+beaker(148,106,'恰好反應時',False)+''.join(circle(165+x*19,231+(y%2)*9,7,'#e8e3da','#a69e8f') for x in range(5) for y in range(2))+txt(210,301,'BaSO₄沉澱',23)+txt(210,346,'H₂SO₄＋Ba(OH)₂',22)+txt(210,384,'同時生成水，離子大幅減少',19),
 txt(210,38,'B把離子的正負寫反',23,weight=700)+circle(114,131,40,'#f6c6bc')+txt(114,141,'H⁺',29)+circle(306,131,40,'#b9d9f2')+txt(306,141,'OH⁻',28)+txt(114,213,'酸的陽離子',21)+txt(306,213,'鹼的陰離子',21)+arrow(114,236,171,292,C['green'],4)+arrow(306,236,249,292,C['green'],4)+molecule(210,315,'water',.7)+txt(210,398,'這才是中和形成水的組合',21)]
#1161 independent objects, joined object, reciprocal mass rods, consistency special case.
ART['q-1161']=[
 txt(210,39,'相同合力，先各自求質量',22,weight=700)+rect(45,111,103,64,'#d5e7fa')+txt(97,150,'甲 m₁',24)+arrow(155,144,301,144,C['blue'])+txt(238,122,'F',25)+txt(339,150,'a₁',25)+rect(45,246,103,64,'#f7dfaf')+txt(97,285,'乙 m₂',24)+arrow(155,279,301,279,C['blue'])+txt(238,257,'F',25)+txt(339,285,'a₂',25)+txt(210,381,'m₁＝F/a₁；m₂＝F/a₂',23),
 txt(210,39,'綁合後，相加的是質量',22,weight=700)+rect(45,169,123,85,'#d5e7fa')+rect(176,169,123,85,'#f7dfaf')+line(168,196,176,196,C['ink'],4)+line(168,226,176,226,C['ink'],4)+txt(107,219,'m₁',27)+txt(237,219,'m₂',27)+arrow(95,116,339,116,C['green'])+txt(215,93,'合力 3F',25)+txt(210,321,'a＝3F/(m₁＋m₂)',25)+txt(210,377,'不是把a₁、a₂相加',22),
 txt(210,39,'將質量的表示式代回',23,weight=700)+rect(57,129,120,103,'#d5e7fa')+rect(177,129,154,103,'#f7dfaf')+txt(116,190,'F/a₁',27)+txt(253,190,'F/a₂',27)+arrow(54,101,334,101,C['green'],4)+txt(210,78,'3F',25)+txt(210,296,'a＝3/(1/a₁＋1/a₂)',24)+txt(210,357,'＝3a₁a₂/(a₁＋a₂)',25)+txt(210,396,'F可約去',21),
 txt(210,39,'檢查：兩個質量若相同',23,weight=700)+rect(62,146,101,79,'#d5e7fa')+rect(170,146,101,79,'#f7dfaf')+txt(112,193,'m',30)+txt(220,193,'m',30)+arrow(48,113,358,113,C['green'])+txt(210,90,'合力3F',24)+arrow(144,275,283,275,C['blue'],4)+txt(210,315,'a＝3F/(2m)',26)+txt(210,367,'＝1.5a₀',28)+txt(210,400,'B符合；不是3a₀²',20)]
#1162 graph, delta-v, vector force on ball, slope separation.
ART['q-1162']=[
 txt(210,37,'從原圖讀減速區間',23,weight=700)+axes(68,302,290,205)+line(68,117,206,302,C['blue'],5)+line(206,302,341,302,C['blue'],5)+txt(47,123,'15',19)+txt(206,331,'10',18)+txt(337,331,'20',18)+line(206,117,206,302,C['ink'],2,'5 5')+txt(210,380,'0～10 s：15 → 0 m/s',23),
 txt(210,37,'斜率就是加速度',23,weight=700)+axes(68,300,290,205)+line(68,115,208,300,C['blue'],5)+line(68,115,208,115,C['red'],3,'6 4')+line(208,115,208,300,C['red'],3,'6 4')+txt(157,94,'Δt＝10 s',19)+txt(294,201,'Δv＝−15 m/s',16)+txt(210,375,'a＝−15/10＝−1.5 m/s²',21),
 txt(210,37,'用F＝ma求摩擦力',23,weight=700)+circle(218,211,55,'white')+f'<path d="M218 171 l24 18 -9 28 h-30 l-9 -28Z" fill="#60738a"/><path d="M165 211l30 6 7 29-14 13 M271 211l-30 6-7 29 14 13" fill="none" stroke="#60738a" stroke-width="3"/>'+line(32,268,386,268,C['green'],4)+arrow(162,209,52,209,C['red'])+txt(87,181,'摩擦力',20,fill=C['red'])+arrow(213,113,347,113,C['blue'],4)+txt(275,90,'原前進方向',20)+txt(218,307,'m＝0.3 kg',23)+txt(210,370,'|F|＝0.3×1.5＝0.45 N',23),
 txt(210,37,'只用仍在減速的10秒',23,weight=700)+axes(68,302,290,205)+f'<path d="M68 302V117L206 302Z" fill="#e1edf9"/>'+line(68,117,206,302,C['blue'],5)+line(206,302,341,302,C['green'],5)+txt(47,123,'15',18)+txt(206,332,'10',18)+txt(337,332,'20',18)+txt(128,244,'減速',23,fill=C['blue'])+txt(278,277,'已停止',22,fill=C['green'])+txt(210,385,'答案D：0.45 N，方向向後',22)]
DESCS={
'q-1157':('從反應物辨認生成的氣體',[('① 先鎖定碳酸氫鹽','碳酸氫鈉遇酸會產生CO₂。看到含碳的物質仍要判斷反應種類，不能只看有沒有碳元素。'),('② 碳酸氫根與酸反應','HCO₃⁻＋H⁺ → CO₂＋H₂O；B確實產生題目所問的二氧化碳。'),('③ A、C產生的是別種氣體','鎂遇稀硫酸產生H₂；雙氧水受MnO₂催化分解產生O₂。兩者有氣泡，但都不是CO₂。')],['B：碳酸氫鈉和稀硫酸。','D為醋酸與NaOH中和，沒有CO₂。','有氣泡不等於產生二氧化碳。']),
'q-1158':('反應係數與平衡存量不能混用',[('① 係數說的是反應比例','N₂＋3H₂ ⇌ 2NH₃；每消耗1 mol N₂與3 mol H₂，會生成2 mol NH₃。'),('② 平衡是動態的','平衡時正反應與逆反應速率相等，各物質存量維持不變；不是反應停止。'),('③ 加入H₂可增加NH₃','在其餘條件適當且不變時，系統向消耗H₂、生成NH₃的方向調整。')],['D錯：係數比不是平衡存量比。','第四圖只是守恆計算例，非指定平衡組成。','原卷200 atm、500°C、Fe₂O₃照留。']),
'q-1159':('乙酸與乙醇酯化，NaCl最不需要',[('① 找到兩個反應物','乙酸CH₃COOH與乙醇C₂H₅OH酯化，兩者都是製備乙酸乙酯的反應物。'),('② 生成酯和水','CH₃COOH＋C₂H₅OH ⇌ CH₃COOC₂H₅＋H₂O；產物是乙酸乙酯及水。'),('③ 濃硫酸有催化作用','濃硫酸提供酸催化，促進反應。圖僅表示催化降低能障，不是實測能量曲線。')],['A：NaCl不是本題酯化反應的必要試劑。','B、C是反應物；D可作酸催化劑。','後續分離的鹽析用途不等於酯化必要試劑。']),
'q-1160':('形成水的是H⁺與OH⁻',[('① 正確的離子組合','酸提供的H⁺是陽離子，鹼提供的OH⁻是陰離子；兩者結合形成水。'),('② 中性仍可能導電','HCl與NaOH恰好中和後，Na⁺、Cl⁻仍在水中移動，NaCl水溶液仍可導電。'),('③ D只說導電性可能很差','H₂SO₄與Ba(OH)₂恰好反應，同時產生水和BaSO₄沉澱，可大幅減少自由離子。')],['B把酸、鹼離子的正負性寫反。','常見酸鹼中和放熱、可生成鹽和水。','D是可能情形，不是每次中和都不導電。']),
'q-1161':('綁合後以總質量及新合力計算',[('① 分別列F＝ma','同一合力F作用下，m₁＝F/a₁、m₂＝F/a₂。不能直接相加或相乘原加速度。'),('② 綁合後總質量相加','兩物體一起加速，總質量是m₁＋m₂；題目新給的合力是3F。'),('③ 代入並約去F','a＝3F/(F/a₁＋F/a₂)＝3a₁a₂/(a₁＋a₂)。質量與加速度的關係要先代清楚。')],['B：3a₁a₂/(a₁＋a₂)。','相同質量特例會得到1.5倍原加速度。','合力變3倍，總質量也變大，不能只乘3。']),
'q-1162':('從v–t圖的斜率求摩擦力',[('① 讀出減速的兩端','0秒速度15 m/s，10秒降為0。10～20秒保持停止，不能當成仍在減速。'),('② 求平均加速度','以前進為正：a＝(0−15)/10＝−1.5 m/s²。負號表示加速度向後。'),('③ 用質量乘加速度','F＝0.3×(−1.5)＝−0.45 N；摩擦力與前進方向相反，大小取0.45 N。')],['D：0.45 N。','用0～10 s減速期間計算。','已停止的水平圖線代表速度不再下降。'])}
manifest=[]
for row in items:
 qid=row[0];paths=[panel(qid,i+1,a) for i,a in enumerate(ART[qid])];title,texts,points=DESCS[qid]
 spec=dict(id=qid,subject='Physics-Chemistry',title=title,art=paths[0],panels=[dict(heading=head,text=text,image=paths[i],alt=f'第{i+1}張新製科學示意：{head[2:]}',caption='新製精確科學／力學輔助圖，非原卷。') for i,(head,text) in enumerate(texts)],fourth=dict(answer=f'答案 {row[6]}',points=points,image=paths[3],alt=f'第4張新製圖解：{title}'),sourceUrl=URL,sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=[rel(B/'crops'/f'{qid}-original.png')],answerCheckedAgainst=row[7],rationale='原卷完整題幹/全部選項及必要圖文逐項核對，四張新圖分別讀條件、辨關係、推導與整合；不使用來源AI圖。',generationMethod='four newly authored exact native SVG scientific diagrams',producerAgent='/root/comic_lane_2',layoutVersion='native-four-images-v7',createdAt=datetime.now(timezone.utc).isoformat(),protectedWords=['二氧化碳','碳酸氫鈉','乙酸乙酯','濃硫酸','氫氧化鈉','牛頓第二運動定律','加速度','摩擦力','CH₃COOC₂H₅','CH₃COOH','C₂H₅OH','NaHCO₃','HCO₃⁻','Ba(OH)₂','BaSO₄'])
 save(B/'specs'/f'{qid}.json',spec)
 manifest.append(dict(id=qid,questionPath=rel(B/'questions'/f'{qid}.json'),specPath=rel(B/'specs'/f'{qid}.json'),assets=[dict(sourcePath=rel(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [B/'crops'/f'{qid}-original.png',*[R/x for x in paths]]]))
save(B/'manifest.json',dict(sourceId='src-more-073',sourceUrl=URL,producerAgent='/root/comic_lane_2',state='draft',questions=manifest))
save(B/'original-review.json',dict(actualViewedOriginals=[ac['downloadedImages'][i]['path'] for i in range(6)],originalCropBoxes={r[0]:r[-1] for r in items},scope='Only six actual User questions; no other printed questions added.',sourceGeneratedArtUsed=False,notes=['q-1158 preserves printed Fe₂O₃ condition; answer D independent of catalyst label.','q-1162 graph from original crop retained; 0–10 s deceleration, 10–20 s rest.']))
print('Created six drafts/specs, 24 independent SVGs and seven crops; visual QA pending.')
