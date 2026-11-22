"""Sixteen distinct vector teaching images, editable and scientifically explicit."""
from pathlib import Path
import json,html
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;ROOT=B.parents[3];REL=B.relative_to(ROOT).as_posix()
INK='#243f50';BLUE='#377da1';TEAL='#16816e';RED='#bf593b';OLD='#657fae';YOUNG='#e3a350';MANTLE='#ecd0a8'
def text(x,y,t,size=20,color=INK,anchor='middle'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="sans-serif" font-size="{size}" fill="{color}">{html.escape(t)}</text>'
def path(d,fill='none',stroke=INK,w=2):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'
def line(x,y,a,b,color=INK,w=3,arrow=False):return f'<path d="M{x} {y}L{a} {b}" fill="none" stroke="{color}" stroke-width="{w}"'+(' marker-end="url(#arrow)"'if arrow else '')+'/>'
def rect(x,y,w,h,c,stroke='none'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{stroke}"/>'
def dot(x,y,r=5,c=INK):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="1.5"/>'
def svg(body,title):return '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="720" viewBox="0 0 360 360"><title>'+html.escape(title)+'</title><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7Z" fill="context-stroke"/></marker></defs><rect width="360" height="360" fill="#f5f8f7"/>'+body+'</svg>'
def ridge(y=175,arrows=False,ages=False):
 s=rect(15,y-85,330,95,'#d5e9f0')+rect(15,y+18,330,110,MANTLE)
 s+=path(f'M15 {y}H120L176 {y-34}L232 {y}H345V{y+20}H230L176 {y-14}L122 {y+20}H15Z','#8ba9bc',BLUE)
 s+=path(f'M176 {y+115}V{y-15}',stroke=RED,w=9)+line(176,y+65,176,y-10,RED,4,True)
 if arrows:s+=line(142,y-65,48,y-65,BLUE,5,True)+line(210,y-65,308,y-65,BLUE,5,True)
 if ages:s+=text(53,y+55,'較老',21,OLD)+text(143,y+34,'較新',21,RED)+text(212,y+34,'較新',21,RED)+text(305,y+55,'較老',21,OLD)
 return s
def subduction(y=150,volcano=True,quakes=False):
 # Oceanic slab enters from east/right and descends west/left; upper plate is west.
 s=rect(15,y-63,330,65,'#d5e9f0')+rect(15,y+15,330,160,MANTLE)
 s+=path(f'M15 {y}H198L218 {y+12}H345V{y+34}H216L178 {y+64}L82 {y+159}L60 {y+140}L165 {y+37}L190 {y+22}H15Z','#87a5bc',BLUE)
 s+=path(f'M15 {y}H193L172 {y+20}H15Z','#adb88f','#76846a')
 if volcano:
  s+=path(f'M104 {y}L135 {y-49}L166 {y}Z','#ab9a87','#766552')+path(f'M131 {y-35}L135 {y-49}L142 {y-35}Z',RED,RED)+line(135,y+48,135,y-30,RED,5,True)
 s+=line(50,y-70,108,y-70,TEAL,4,True)+line(304,y-70,245,y-70,TEAL,4,True)
 if quakes:
  for x,yy,c in [(216,y+18,'#f5f8f7'),(174,y+59,'#e5b26a'),(130,y+104,INK),(85,y+149,INK)]:s+=dot(x,yy,6,c)
 return s
def plan_quakes():
 s=rect(45,70,270,190,'#d9ebf0')+path('M45 70H125L143 90L118 110L140 137L123 155L155 182L133 204L145 235L120 260H45Z','#b9c8a0','#7d9271')
 for i in range(6):
  y=90+i*28;s+=dot(105,y,6,INK)+dot(185,y+4,6,'#f5f8f7')+dot(265,y+8,2,INK)
 s+=text(178,53,'西 ←                 → 東',19)+text(105,289,'深源',20)+text(185,289,'中源',20)+text(265,289,'淺源',20)
 return s
def mini_ridge(x,y):
 return f'<g transform="translate({x} {y}) scale(.45)">'+ridge(155,True,False)+'</g>'
def image(n,k,body,title):(B/f'art/q-{n}-panel-{k}.svg').write_text(svg(body,title))

# q-1175: Locate P, connect convergence with subduction, identify the volcanic arc,
# and compare with a divergent volcanic setting rather than treating all volcanoes alike.
s=text(180,30,'先定位：太平洋西側',24)+rect(30,55,300,245,'#d9ebf0')+path('M30 55H113L138 99L106 131L112 171L91 215L113 258L90 300H30Z','#b9c8a0','#788d70')
for d in ['M151 83L143 106L148 121L141 134L147 143L158 126L160 111Z','M162 143L154 159L149 170L155 182L163 169L168 154Z']:s+=path(d,'#b9c8a0','#788d70')
s+=dot(170,150,7,RED)+text(204,152,'P',27,RED)+text(90,90,'亞洲',23)+text(245,220,'太平洋',24,BLUE)+line(231,151,182,151,RED,3,True)+text(180,337,'日本附近：聚合邊界',23)
image(1175,1,s,'從原題P位置辨認太平洋西側聚合邊界')
s=text(180,30,'兩板塊靠近與隱沒',24)+subduction(154)+text(75,66,'上方板塊',21)+text(278,66,'海洋板塊',21)+text(278,210,'海溝',20,BLUE)+line(268,200,217,167,BLUE,2)+text(133,340,'向下隱沒',22,BLUE)
image(1175,2,s,'聚合邊界中海洋板塊從右側向左下方隱沒')
s=text(180,30,'隱沒帶上方的火山',24)+subduction(140)+text(63,115,'火山',22,RED)+line(87,113,123,102,RED,2)+text(275,255,'上方部分熔融',19,RED)+line(220,248,142,193,RED,2)
for x,y in [(151,208),(167,191),(181,179)]:s+=line(x,y,x-13,y-24,TEAL,2,True)
s+=text(180,337,'隱沒促使上方產生岩漿',22)
image(1175,3,s,'隱沒與上方部分熔融及火山帶，不畫成整片板塊熔化')
s=text(180,30,'有火山，仍須讀位置',23)+text(90,70,'P：聚合 A',21,TEAL)+text(271,70,'中洋脊：張裂',20,BLUE)
s+='<g transform="translate(0 95) scale(.47 .58)">'+subduction(130)+'</g>'+mini_ridge(180,108)+text(89,325,'靠近、隱沒',20,TEAL)+text(274,325,'分開、新生',20,BLUE)
image(1175,4,s,'P處聚合型火山和中洋脊張裂型火山的構造比較')

# q-1176: All three focal-depth symbols, dipping slab, genuine divergence versus
# transform, and the consistent cross-section. Plan is conceptual, not original.
image(1176,1,text(180,30,'讀圖例與深度排列',24)+plan_quakes()+text(180,337,'向西側，震源逐漸變深',22),'原題震源東淺西深關係的輔助平面示意')
s=text(180,30,'震源沿板塊向深處延伸',22)+subduction(140,False,True)+text(45,67,'西',23)+text(320,67,'東',23)+text(74,313,'深',23)+text(178,275,'中',23)+text(265,205,'淺',23)+text(180,345,'隱沒帶可有淺、中、深源地震',19)
image(1176,2,s,'東側板塊向西下方隱沒且震源深度逐增')
s=text(180,30,'B、C、D不是隱沒',24)+text(90,72,'B：張裂',22)+mini_ridge(0,85)
s+=text(271,72,'C、D：水平錯動',19)+rect(207,150,47,90,'#92b5b3',INK)+rect(264,135,47,90,'#b7bc91',INK)+line(230,215,230,166,TEAL,4,True)+line(288,154,288,203,TEAL,4,True)+text(90,295,'←   →',30,BLUE)+text(270,295,'交界兩側平行錯移',17)+text(180,340,'以淺源地震為主',23)
image(1176,3,s,'原選項B張裂、C與D水平錯動的運動關係')
s=text(180,30,'A：靠近＋向下隱沒',24,TEAL)+subduction(143,False,True)+text(50,73,'西',22)+text(319,73,'東',22)+line(278,228,169,284,BLUE,3,True)+text(266,256,'東淺西深',20,BLUE)+text(180,342,'深度與排列共同支持A',23)
image(1176,4,s,'以板塊向西隱沒和東淺西深震源關係整合答案A')

# q-1177: ridge generation, age bands, trench consumption, entire oceanic life path.
image(1177,1,text(180,30,'中洋脊：新地殼形成',24)+ridge(180,True)+text(176,75,'W 較年輕',23,RED)+text(180,327,'X 張裂，向兩側分開',23,BLUE),'中洋脊的年輕海洋地殼和張裂運動')
s=text(180,30,'離開中洋脊，逐漸變老',23)+rect(20,83,320,170,'#d5e9f0')
for x,c in [(20,OLD),(70,'#8da2b9'),(120,'#c4bba1'),(160,YOUNG),(190,'#c4bba1'),(240,'#8da2b9'),(290,OLD)]:s+=rect(x,150,50 if x!=160 else 30,103,c,INK)
s+=line(170,120,40,120,TEAL,4,True)+line(190,120,322,120,TEAL,4,True)+text(178,288,'脊軸',23,RED)+text(44,320,'較老',21,OLD)+text(178,320,'最新',21,RED)+text(316,320,'較老',21,OLD)
image(1177,2,s,'中洋脊兩側由中心較新向外較老的地殼年齡帶')
s=text(180,30,'海溝：較老地殼隱沒',23)+subduction(145,False)+text(272,63,'Y 較老',23,OLD)+text(276,210,'海溝',23)+line(259,202,218,158,BLUE,2)+text(180,340,'Z 聚合，板塊相互靠近',22,TEAL)
image(1177,3,s,'海溝的相對較老海洋地殼和聚合隱沒')
s=text(180,30,'從中洋脊移向海溝',24)+rect(15,100,330,85,'#d5e9f0')+rect(15,190,330,135,MANTLE)
s+=path('M15 180H56L86 151L116 180H265L285 194L337 280L319 295L270 212H114L86 174L60 202H15Z','#8ba9bc',BLUE)+path('M287 180H345V200H290L278 194Z','#b2ba98','#75856a')
s+=line(86,285,86,179,RED,7,True)+line(130,130,238,130,TEAL,5,True)+line(328,145,293,145,TEAL,4,True)+text(85,72,'較新／張裂',20,RED)+text(276,72,'較老／聚合',20,TEAL)+text(180,344,'C：Y 較老，Z 聚合',23,TEAL)
image(1177,4,s,'新生海洋地殼由中洋脊移向海溝並逐漸變老')

# q-1178: ridge shape, divergence, left-to-right age ordering, correct combined D.
image(1178,1,text(180,30,'圖（一）：海底中央隆起',23)+ridge(180)+text(176,112,'板塊交界',22)+line(176,122,176,143,INK,2,True)+text(62,76,'海水',22,BLUE)+text(180,327,'辨認中洋脊，才判運動',23),'以海底中洋脊隆起定位板塊交界')
image(1178,2,text(180,30,'兩側板塊各自向外',24)+ridge(180,True)+text(79,98,'左側←',23,BLUE)+text(283,98,'右側→',23,BLUE)+text(180,330,'張裂，不能貼成向內聚合',22),'中洋脊兩側向外張裂的方向')
s=text(180,30,'年齡文字要由左至右讀',22)+ridge(150,False,True)+line(30,290,149,290,TEAL,3,True)+line(205,290,326,290,TEAL,3,True)+text(89,324,'較老—較新',21)+text(269,324,'較新—較老',21)+text(177,75,'中心較新',23,RED)
image(1178,3,s,'中洋脊年齡排列左老至新、右新至老')
s=text(180,30,'D：方向與年齡都對',24,TEAL)+ridge(156,True,True)+text(180,74,'←       →',29,BLUE)+text(180,292,'靠近交界較新，往外較老',22)+text(180,330,'C年齡對但方向錯；A兩項錯',19,RED)
image(1178,4,s,'把張裂方向和海底地殼相對年齡組合成D的構造圖')

texts={1175:[('① 先讀P位置','P在日本附近、太平洋西緣的聚合型邊界；不能只看到火山就決定板塊類型。'),('② 板塊靠近並隱沒','海洋板塊向下進入另一板塊之下，對應原選項A的擠壓與隱沒。'),('③ 看火山形成背景','隱沒過程與上方部分熔融、岩漿上升有關，形成火山帶；不把整片隱沒板塊畫成熔掉。')],1176:[('① 核對圖例','黑實心圓是深源、空心圓是中源、點線是淺源；X處呈現東淺西深的排列。'),('② 從震源推隱沒','震源沿傾斜板塊向深處延伸，支持向西側下方隱沒的A。'),('③ 依箭頭排除','B箭頭向外，是張裂；C、D是水平錯動，不能解釋本題的中、深源震源帶。')],1177:[('① 中洋脊新生地殼','海洋地殼在中洋脊形成，W較年輕；板塊向外分離，X張裂。'),('② 年齡隨距離改變','新地殼離開脊軸，向兩側移動並逐漸變老；不是中洋脊處最老。'),('③ 海溝消耗舊地殼','本題比較下，海溝附近Y較老；板塊相互靠近並隱沒，Z聚合。')],1178:[('① 先認地形','原題板塊交界位於海底隆起處，對應新海洋地殼形成的中洋脊。'),('② 再決定方向','中洋脊兩側張裂，左板塊向左、右板塊向右，貼紙應向外。'),('③ 獨立核對年齡','各側文字都由左向右讀：左側較老—較新，右側較新—較老。')]} 
answers={1175:('A',['P位置符合聚合隱沒。','張裂處也可能有火山，仍須按地點判斷。']),1176:('A',['淺、中、深源排列支持隱沒。','B為張裂，C與D為水平錯動。']),1177:('C',['W較年輕，X張裂。','Y較老，Z聚合；每選項兩項皆須正確。']),1178:('D',['方向向外，中心較新。','C與D年齡相同；A方向與年齡都錯。'])}
for n,ps in texts.items():
 q=json.loads((B/f'questions/q-{n}.json').read_text());a,points=answers[n]
 spec=dict(id=f'q-{n}',subject='Earth',title=q['title'].split('｜')[1],art=f'{REL}/art/q-{n}-panel-1.svg',panels=[dict(heading=h,text=t,image=f'{REL}/art/q-{n}-panel-{i}.svg',alt=f'新製地科圖解{i}：{h[2:]}',caption='新製地科構造輔助圖，非原卷、非比例。')for i,(h,t)in enumerate(ps,1)],fourth=dict(answer='答案 '+a,points=points,image=f'{REL}/art/q-{n}-panel-4.svg',alt='第4張新製圖解：'+q['title'].split('｜')[1]),sourceUrl='https://chatgpt.com/share/6b01da76-e42c-83ec-921a-80ff392862c1',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=q['images'],answerCheckedAgainst=q['explanation'],rationale='以新製精確板塊剖面、地殼年齡帶及震源排列呈現推理，不用人物或純文字流程框。',generationMethod='four newly authored exact native SVG geological diagrams',producerAgent='/root/source74_earth_b',layoutVersion='native-four-images-v7',createdAt=datetime.now(timezone.utc).isoformat(),protectedWords=['中洋脊','海洋地殼','板塊交界','深源地震','中源地震','淺源地震','太平洋','較老—較新','較新—較老'])
 (B/f'specs/q-{n}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print('Saved 16 distinct SVG images and four specs.')
