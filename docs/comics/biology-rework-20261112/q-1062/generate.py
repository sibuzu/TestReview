"""Quantitative annual readings and explicitly qualitative climate diagrams."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/comics/art'

def svg(body):
 return '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#dff2f8"/><stop offset="1" stop-color="#fff1d9"/></linearGradient><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#257ca4"/></marker></defs><rect width="600" height="600" rx="22" fill="url(#sky)"/><g font-family="Noto Sans CJK TC,sans-serif" font-size="30" text-anchor="middle" fill="#25444a">'+body+'</g></svg>'

b1='<text x="300" y="48" font-weight="bold">年降水量：26 mm</text><path d="M200 110V510H350V110" fill="#f7fcff" stroke="#517a88" stroke-width="7"/><rect x="204" y="406" width="142" height="104" fill="#62b9d1"/><path d="M204 406Q240 398 275 406T346 406" fill="none" stroke="#287e9f" stroke-width="5"/>'
for v in [0,25,50,75,100]:
 y=510-4*v;b1+=f'<path d="M355 {y}h22" stroke="#517a88" stroke-width="4"/><text x="417" y="{y+10}">{v}</text>'
b1+='<text x="417" y="93">mm</text><path d="M100 406H195" stroke="#a76b2a" stroke-width="5"/><text x="104" y="388" font-size="38" font-weight="bold">26</text><text x="300" y="559" font-size="24">全年總量的量尺示意，非原量雨器</text>'

b2='''<text x="300" y="47" font-weight="bold">河水與當地降雨，來源不同</text>
<path d="M0 105H600V600H0Z" fill="#e6c993"/>
<path d="M300 600Q250 500 300 410T300 265L155 100H445L300 265Q330 385 325 428Q285 525 340 600Z" fill="#8fb278"/>
<path d="M320 600Q270 505 310 420T300 265L185 102M300 265L414 102" fill="none" stroke="#3e9cb5" stroke-width="20"/>
<path d="M310 520L305 448M302 361L302 296" stroke="#257ca4" stroke-width="10" marker-end="url(#a)"/>
<path d="M0 72H600V105Q450 124 300 105T0 105Z" fill="#82c6d6"/>
<circle cx="300" cy="265" r="11" fill="#c76d37" stroke="white" stroke-width="3"/><text x="425" y="268" font-weight="bold">開羅</text><path d="M350 258H317" stroke="#25444a" stroke-width="3"/>
<text x="80" y="226" font-size="26">乾燥地區</text><text x="492" y="402" font-size="26">上游來水</text><path d="M426 397L328 411" stroke="#25444a" stroke-width="3"/>
<path d="M62 445C18 441 24 389 65 393C60 347 125 338 140 380C184 351 226 397 200 424C231 464 180 476 149 462H62Z" fill="#f5fbff" stroke="#9eb9c4" stroke-width="3"/>
<path d="M60 475l-10 26M88 477l-10 26M116 477l-10 26M145 477l-10 26" stroke="#3584ad" stroke-width="6"/>
<path d="M105 512Q165 542 289 555" fill="none" stroke="#3e9cb5" stroke-width="8"/>
<text x="154" y="582" font-size="22">上游降雨示意</text><text x="450" y="573" font-size="22">非比例河道圖</text>'''

b3='<text x="300" y="45" font-weight="bold">比較雨季的概念形狀</text><text x="300" y="81" font-size="23">非測站數據；柱高只示相對多寡</text>'
for title,y,heights,col in [('全年少雨',208,[7,5,3,5],'#bc8f4b'),('溫帶季風：夏雨',366,[10,24,65,25],'#5c9cb1'),('地中海型：冬雨',524,[66,35,6,31],'#558ca5')]:
 b3+=f'<text x="305" y="{y-92}" font-size="29" font-weight="bold">{title}</text><path d="M145 {y-76}V{y}H520" fill="none" stroke="#5a7780" stroke-width="3"/>'
 for x,h,season in zip([190,275,360,445],heights,['冬','春','夏','秋']):
  b3+=f'<rect x="{x}" y="{y-h}" width="45" height="{h}" fill="{col}"/><text x="{x+22}" y="{y+29}" font-size="25">{season}</text>'

# x=annual temperature, y=annual precipitation; labelled axes are display scales,
# not climatic boundaries. The only plotted station values come from the original.
x=115+21.4*9.5;y=480-26*1.6
b4='''<text x="300" y="45" font-weight="bold">合看兩個全年數字</text><text x="153" y="92" font-size="25">年降水量 mm</text><path d="M115 125V480H535" fill="none" stroke="#4e737c" stroke-width="5"/>'''
for v in [0,50,100,150,200]:
 yy=480-v*1.6;b4+=f'<path d="M107 {yy}H115" stroke="#4e737c" stroke-width="3"/><text x="70" y="{yy+9}" font-size="24">{v}</text>'
for v in [0,10,20,30,40]:
 xx=115+v*9.5;b4+=f'<path d="M{xx} 480V488" stroke="#4e737c" stroke-width="3"/><text x="{xx}" y="517" font-size="24">{v}</text>'
b4+=f'<path d="M115 {y}H{x}V480" fill="none" stroke="#bd7f31" stroke-width="3" stroke-dasharray="8 7"/><circle cx="{x}" cy="{y}" r="12" fill="#b76630" stroke="white" stroke-width="4"/><path d="M{x+10} {y-11}L430 338" stroke="#b76630" stroke-width="3"/><text x="388" y="288" font-size="33" font-weight="bold">21.4°C</text><text x="388" y="332" font-size="33" font-weight="bold">26 mm</text><text x="368" y="558" font-size="26">年均溫 °C</text>'

for i,b in enumerate([b1,b2,b3,b4],1):(OUT/f'q-1062-four-image-v2-panel-{i}.svg').write_text(svg(b))
imgs=[f'docs/comics/art/q-1062-four-image-v2-panel-{i}.svg' for i in range(1,5)]
s=dict(id='q-1062',subject='Geography',title='全年僅26mm，河水不能代替當地雨量',art=imgs[0],panels=[
dict(heading='① 年降水量只有26 mm',text='原圖明印年降水量26 mm，月降水柱全年都很低。第一圖將全年總量畫在量尺上；不是猜補各月雨量。極乾燥是本題最重要的線索。',caption='新製量尺圖｜0～100 mm為顯示刻度，不是氣候分類門檻。',alt='年總雨量26 mm在0至100 mm量尺上以藍色水面精確標在26的位置。',image=imgs[0]),
dict(heading='② 有尼羅河，不等於當地多雨',text='第二圖分開畫上游降雨與流向開羅的河水。河流可把上游水帶到乾燥地區；看到尼羅河，不能直接推論開羅當地降水豐富。',caption='新製河水來源示意｜不是地圖、實際河道或降雨位置圖。',alt='下方上游降雨匯入河水，藍色河流由上游流向下游開羅，開羅位於分流前；周圍為乾燥地區。',image=imgs[1]),
dict(heading='③ 全年少雨，不能只憑冬季選地中海型',text='第三圖只比較雨季形狀：溫帶季風常見較明顯夏雨，地中海型有冬雨、夏乾。本題全年總共僅26 mm，不能只因冬季有一點雨就選D。',caption='新製概念比較｜柱高沒有數值，不冒充原卷月資料或真實測站。',alt='三列分別為全年雨柱都低、夏季雨柱較高、冬季雨柱較高的概念圖，標明冬春夏秋。',image=imgs[2])
],fourth=dict(answer='答案 B：教材的熱帶沙漠氣候',points=['第四圖只畫原卷兩個全年數字：21.4°C、26 mm。','最突出的判讀線索是極乾燥，依本題教材分類選B。','保留原說明：熱帶沙漠名稱不代表每個月均溫都高於18°C。'],image=imgs[3],alt='以年均溫為橫軸、年降水量為縱軸，只標原卷21.4°C與26 mm的單一點；未新增其他城市或分類界線。'),protectedWords=['26 mm','21.4°C','熱帶沙漠氣候','地中海型','尼羅河','開羅','18°C'],generationMethod='four authored native SVG quantitative annual gauge, river-source diagram, qualitative seasonal comparison, and two-variable annual plot',generatorFile='docs/comics/biology-rework-20261112/q-1062/generate.py',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/assets/originals/q-1062-original-b71eecfe94ce.jpg','site/dist/assets/questions/q-1062-figure-35fee275dca5.jpg'],answerCheckedAgainst='完整原卷第7題及氣候附圖實看：年均溫21.4°C、年降水26 mm；原B不變，四選項保持。',rationale='四張分開表示年雨量、河水來源、雨季概念差異與全年溫雨資料。只引用原卷可確讀的兩個年數字，不杜撰月雨量/溫度；圖3是無數值概念比較而非新氣候資料。',producerAgent='/root/comic_lane_1',visualChecked=False,sources=[dict(url='https://science.nasa.gov/earth/earth-observatory/cairo-egypt-2813/',support='NASA：開羅在尼羅河沿岸，河流綠帶外為乾旱撒哈拉，不能以河流代表多雨。'),dict(url='https://nileresearch.org/about-the-nile-basin/climate_and_hydrometeorology/',support='ENRUC流域研究資料：尼羅流域上游與下游雨量不同，下游受上游來水影響。'),dict(url='https://weather.metoffice.gov.uk/climate/climate-explained/climate-zones',support='Met Office：沙漠極乾燥，地中海型夏乾冬雨。'),dict(url='https://soilhealth.ucdavis.edu/climatic-zones/mediterranean',support='UC Davis：地中海型雨季在冬季、夏乾；用作無數值概念比較，不移用外站數據。')])
(ROOT/'docs/comics/q-1062.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
