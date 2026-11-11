"""New wind/moisture/relief diagrams; the question's original point map stays intact."""
import hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/comics/art'
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson'
CACHE=ROOT/'.cache/q1064-natural-earth-countries.geojson'
if not CACHE.exists():urllib.request.urlretrieve(URL,CACHE)
DATA=json.loads(CACHE.read_text())
def svg(body):
 return '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#d9eff7"/><stop offset="1" stop-color="#fff6e8"/></linearGradient><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#2b819e"/></marker></defs><rect width="600" height="600" rx="22" fill="url(#sky)"/><g font-family="Noto Sans CJK TC,sans-serif" font-size="29" text-anchor="middle" fill="#28454e">'+body+'</g></svg>'
def mapbase(bounds):
 l,b,r,t=bounds;s=min(520/(r-l),430/(t-b));ox=(600-s*(r-l))/2;oy=100+(430-s*(t-b))/2
 def xy(lon,lat):return ox+(lon-l)*s,oy+(t-lat)*s
 result='<defs><clipPath id="m"><rect x="35" y="95" width="530" height="440" rx="12"/></clipPath></defs><g clip-path="url(#m)">'
 for f in DATA['features']:
  if f['properties']['CONTINENT']!='Asia':continue
  g=f['geometry'];polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
  for poly in polys:
   ring=poly[0]
   if max(p[0] for p in ring)<l or min(p[0] for p in ring)>r or max(p[1] for p in ring)<b or min(p[1] for p in ring)>t:continue
   result+='<path d="M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in [xy(*p[:2]) for p in ring])+'Z" fill="#b5c098" stroke="#b5c098" stroke-width="1.2" stroke-linejoin="round"/>'
 return result+'</g>',xy
def cloud(x,y,s=1):
 return f'<g transform="translate({x} {y}) scale({s})"><path d="M-75 35C-120 35-122-17-80-22C-85-65-28-80-9-47C20-90 84-57 70-18C122-12 115 40 70 40H-75Z" fill="#f6fcff" stroke="#93b4c3" stroke-width="3"/></g>'
def snow(x,y):
 return f'<g transform="translate({x} {y})" stroke="#3280a2" stroke-width="4" stroke-linecap="round"><path d="M-10 0H10M0-11V11M-8-8L8 8M-8 8L8-8"/></g>'

b1,xy=mapbase((120,29,147,48))
a,z=xy(127,44.5),xy(137,37.0)
b1='<text x="300" y="45" font-weight="bold">冬季西北風：從大陸往日本</text>'+b1+f'<path d="M{a[0]} {a[1]}L{z[0]} {z[1]}" stroke="#2b819e" stroke-width="13" marker-end="url(#a)"/>'
b1+='<text x="142" y="174" font-size="28">大陸冷空氣</text><text x="264" y="354" font-size="30" font-weight="bold">日本海</text><text x="459" y="460" font-size="28">太平洋</text><text x="300" y="573" font-size="23">新製地理關係圖，非原卷甲乙丙丁點位重繪</text>'
b2='''<text x="300" y="45" font-weight="bold">經過海面，增添水氣</text><path d="M0 422Q60 402 120 422T240 422T360 422T480 422T600 422V600H0Z" fill="#66b6ce"/><path d="M0 467Q45 445 90 467T180 467T270 467T360 467T450 467T540 467M0 530Q45 508 90 530T180 530T270 530T360 530T450 530T540 530" fill="none" stroke="#c6eaf0" stroke-width="5"/>
<path d="M44 207H509" fill="none" stroke="#2b819e" stroke-width="13" marker-end="url(#a)"/>
<path d="M160 403C130 363 189 334 163 286M280 410C250 370 309 340 283 292M400 401C370 361 429 331 403 283" fill="none" stroke="#2b819e" stroke-width="6" marker-end="url(#a)"/>
<text x="153" y="155" font-size="28">原來寒冷、較乾</text><text x="443" y="256" font-size="28">沿海面取得水氣</text><text x="300" y="488" font-size="32" font-weight="bold">日本海</text><text x="300" y="572" font-size="23">向上箭頭表示水氣由海面進入空氣</text>'''
b3='''<text x="300" y="45" font-weight="bold">山地兩側的冬季差異</text><path d="M0 480H110L205 355L291 237L330 186L380 277L458 382L520 450H600V600H0Z" fill="#9eb087"/><path d="M291 237L330 186L380 277L345 259L322 284L307 252Z" fill="#f8fdff"/>
<path d="M110 480L205 355L291 237" fill="none" stroke="#f8fdff" stroke-width="13"/>
<path d="M0 480H85V600H0Z" fill="#6bb7ce"/>
<path d="M25 350Q135 334 208 237" fill="none" stroke="#2b819e" stroke-width="12" marker-end="url(#a)"/>
<path d="M369 179Q425 248 540 301" fill="none" stroke="#ae8856" stroke-width="8"/>
<circle cx="498" cy="140" r="31" fill="#e7bf60"/><path d="M498 94V78M498 186V202M451 140H435M545 140H561" stroke="#d4a447" stroke-width="6"/>
<text x="150" y="523" font-size="28">日本海側</text><text x="473" y="523" font-size="28">太平洋側</text><text x="300" y="573" font-size="23">迎風坡抬升降雪；越山後氣流較乾</text>'''+cloud(232,145,.65)+''.join(snow(x,y) for x,y in [(190,205),(221,222),(250,207),(175,255),(207,276),(238,256)])
b4,xy=mapbase((128,30,147,46))
points=[xy(*p) for p in [(135.2,35.5),(136.1,36),(137,37),(138.1,37.2),(139,38.5),(139.8,40)]]
b4='<text x="300" y="45" font-weight="bold">丙：本州的日本海迎風側</text>'+b4+'<path d="M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" fill="none" stroke="#3c8d9f" stroke-width="17" stroke-linecap="round" opacity=".7"/>'
b4+='<text x="146" y="282" font-size="30" font-weight="bold">日本海</text><text x="434" y="423" font-size="27">太平洋</text>'
x,y=xy(137,37)
b4+=f'<path d="M100 163Q173 212 {x-15} {y-13}" fill="none" stroke="#2b819e" stroke-width="10" marker-end="url(#a)"/><text x="179" y="130" font-size="26">冬季冷氣流</text><text x="300" y="559" font-size="23">粗色帶只示海側區域，不是降雪量或原卷精確點位</text>'
for i,b in enumerate([b1,b2,b3,b4],1):(OUT/f'q-1060-four-image-v2-panel-{i}.svg').write_text(svg(b))
imgs=[f'docs/comics/art/q-1060-four-image-v2-panel-{i}.svg' for i in range(1,5)]
s=dict(id='q-1060',subject='Geography',title='大陸冷氣流過海增濕，迎風側遇山降雪',art=imgs[0],panels=[
dict(heading='① 先看冬季風的來向',text='第一圖以大陸、日本海及日本的地理位置，表示冬季西北風從大陸吹向日本。起初是寒冷、較乾的氣流，不是一開始就暖濕。',caption='新製風向定位圖｜海陸依Natural Earth，不重繪原卷四點。',alt='東亞海陸與日本輪廓，藍箭頭由西北大陸經日本海吹向日本。',image=imgs[0]),
dict(heading='② 水氣主要在過海時補充',text='第二圖把海面放大：氣流通過日本海，從海面取得水氣。向上的細箭頭表示海面供應水氣，之後濕冷氣流再移向本州。',caption='新製海氣交換示意｜向上為海面供應水氣，向右為氣流。',alt='冷氣流水平通過日本海，三支向上曲箭頭表示海面向空氣補充水氣。',image=imgs[1]),
dict(heading='③ 日本海側迎風，遇山抬升降雪',text='第三圖以本州山地剖面比較兩側：日本海側濕冷氣流被抬升、冷卻降雪；越過山脈後水氣減少，太平洋側常較乾晴。不是日本所有海岸都一樣。',caption='新製機制剖面｜非特定山峰、積雪量或當日天氣圖。',alt='左日本海側有氣流抬升、雲與雪花；中間本州山地，右太平洋側氣流越山後較乾晴。',image=imgs[2])
],fourth=dict(answer='答案 C：原圖的丙',points=['第四圖只強調本州日本海側的地理關係，精確四點保留在原卷附圖。','丙的海側、季風與山地組合符合本題；不是單純比較緯度。','甲北海道也會下雪；不能把選丙誤說成甲沒有雪。'],image=imgs[3],alt='日本海側以粗色帶概示本州海側區域，冷空氣箭頭從日本海移入；不把色帶當實測雪區或原卷丙的精確座標。'),protectedWords=['日本海側','太平洋側','本州','北海道','西北風','迎風坡','冷氣流'],generationMethod='four authored native SVG geographic wind map, sea-air moisture transfer, snowfall cross-section and regional summary',generatorFile='docs/comics/biology-rework-20261112/q-1060/generate.py',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/assets/originals/q-1060-original-2c0fc728797e.jpg','site/dist/assets/questions/q-1060-figure-a6e4f48c62dc.jpg'],answerCheckedAgainst='實看完整17題與圖九甲乙丙丁：甲北海道、丙本州日本海側、乙太平洋側、丁九州；原C及原A改C記錄保持。',rationale='四張真實風向與物理關係圖取代舊文字框；冬季大陸冷氣流經日本海補水氣、迎風抬升形成降雪。保留原卷點位，不將粗色帶冒稱精確原點或雪區，不說北海道無雪。',producerAgent='/root/comic_lane_1',visualChecked=False,sources=[dict(url='https://www.data.jma.go.jp/cpd/longfcst/en/tourist_japan.html',support='JMA日本氣候：冬季西北風使日本海側迎風降雪、太平洋側下風較晴。'),dict(url='https://www.jamstec.go.jp/jdb/ronbun/Ks00039171.pdf',support='JAMSTEC保存的JMSJ原論文引言：大陸寒冷乾燥季風過日本海，海面供給水氣並使氣團改變。'),dict(url='https://www.naturalearthdata.com/about/terms-of-use/',support='Natural Earth公開領域海陸幾何，未標國界。')],mapData=dict(url=URL,sha256=hashlib.sha256(CACHE.read_bytes()).hexdigest(),projection='regional equirectangular with common degree scale',originalPointMapReconstructed=False))
(ROOT/'docs/comics/q-1060.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
