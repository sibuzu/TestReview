"""Geographic positions from Natural Earth; conceptual relief is labelled."""
import hashlib,json,urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/comics/art'
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson'
CACHE=ROOT/'.cache/q1064-natural-earth-countries.geojson'
if not CACHE.exists(): urllib.request.urlretrieve(URL,CACHE)
DATA=json.loads(CACHE.read_text())

def svg(body):
 return '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#d8eff6"/><stop offset="1" stop-color="#fff4df"/></linearGradient><marker id="blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#2c819f"/></marker><marker id="warm" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#b4743a"/></marker></defs><rect width="600" height="600" rx="22" fill="url(#sky)"/><g font-family="Noto Sans CJK TC,sans-serif" font-size="29" text-anchor="middle" fill="#2c484b">'+body+'</g></svg>'

def mapbase(bounds):
 left,bottom,right,top=bounds;scale=min(520/(right-left),430/(top-bottom));ox=(600-scale*(right-left))/2;oy=100+(430-scale*(top-bottom))/2
 def xy(lon,lat):return (ox+(lon-left)*scale,oy+(top-lat)*scale)
 result='<defs><clipPath id="map"><rect x="35" y="95" width="530" height="442" rx="12"/></clipPath></defs><g clip-path="url(#map)">'
 for f in DATA['features']:
  if f['properties']['CONTINENT'] not in ['Africa','Europe','Asia']:continue
  geom=f['geometry'];polys=[geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates']
  for poly in polys:
   ring=poly[0]
   if max(p[0] for p in ring)<left or min(p[0] for p in ring)>right or max(p[1] for p in ring)<bottom or min(p[1] for p in ring)>top:continue
   coords=[xy(*p[:2]) for p in ring]
   result+='<path d="M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in coords)+'Z" fill="#d7bf85" stroke="#d7bf85" stroke-width="1.2" stroke-linejoin="round"/>'
 result+='</g>'
 return result,xy

b1,xy=mapbase((-20,19,20,47))
b1='<text x="300" y="45" font-weight="bold">摩洛哥在非洲西北部</text>'+b1
x,y=xy(-6.5,32.0)
b1+=f'<circle cx="{x}" cy="{y}" r="12" fill="#367b68" stroke="white" stroke-width="4"/><path d="M{x-8} {y-10}L105 222" stroke="#365b57" stroke-width="3"/><text x="109" y="205" font-weight="bold">摩洛哥</text>'
pts=[xy(*p) for p in [(-9.2,30.1),(-6,31.6),(-3,33),(0,34),(3,35),(6,35.5),(9,36)]]
b1+='<path d="M'+'L'.join(f'{a:.2f},{b:.2f}' for a,b in pts)+'" fill="none" stroke="#a16c35" stroke-width="12" stroke-linecap="round"/>'
b1+='<text x="374" y="285" font-size="27">亞特拉斯山脈</text><text x="355" y="431" font-size="32" fill="#946c34">撒哈拉</text><text x="87" y="360" font-size="26">大西洋</text><text x="341" y="166" font-size="26">地中海</text><text x="300" y="573" font-size="22">Natural Earth海陸；山脈為概略走向，無國界主張</text>'

b2='''<text x="300" y="45" font-weight="bold">山地改變氣流，不是密閉牆</text>
<path d="M0 480H105L179 387L261 267L315 200L363 280L449 389L520 455H600V600H0Z" fill="#a5b17e"/>
<path d="M315 200L363 280L449 389L520 455H600V600H452Z" fill="#c9ac70"/>
<path d="M0 480H87V600H0Z" fill="#6eb7cc"/>
<path d="M25 348C104 345 162 274 220 217" fill="none" stroke="#2c819f" stroke-width="12" marker-end="url(#blue)"/>
<path d="M550 372Q450 361 397 311" fill="none" stroke="#b4743a" stroke-width="12" marker-end="url(#warm)"/>
<path d="M393 310Q376 232 337 159Q304 104 250 128" fill="none" stroke="#b4743a" stroke-width="5" stroke-dasharray="10 9" marker-end="url(#warm)"/>
<text x="109" y="307" font-size="25">海上濕氣</text><text x="501" y="426" font-size="24">南側熱乾氣流</text>
<text x="314" y="80" font-size="23">仍可能越山，影響隨條件而變</text>
<text x="293" y="526" font-weight="bold">亞特拉斯山地</text><text x="300" y="572" font-size="23">新製機制剖面，左右非精確方位比例</text>'''

b3,xy=mapbase((-20,-35,60,47))
b3='<text x="300" y="45" font-weight="bold">四個選項的所在區域</text>'+b3
for lon,lat,label,col in [(-4,32,'C','#2f856f'),(43,24,'A','#a5713c'),(35,-3,'B','#a5713c'),(33,39,'D','#a5713c')]:
 x,y=xy(lon,lat);b3+=f'<circle cx="{x}" cy="{y}" r="21" fill="{col}" stroke="white" stroke-width="3"/><text x="{x}" y="{y+10}" fill="white" font-size="30" font-weight="bold">{label}</text>'
b3+='<text x="116" y="204" font-size="24">西北非</text><text x="478" y="141" font-size="24">西亞</text><text x="300" y="572" font-size="23">位置標記只定位區域，不畫實際完整地形範圍</text>'

b4='''<text x="300" y="45" font-weight="bold">海拔也是氣候影響因素</text><path d="M0 505H85L155 424L212 324L291 190L335 151L393 267L457 373L546 470L600 491V600H0Z" fill="#a4b482"/><path d="M335 151L308 239L342 220L393 267" fill="#e1dfc2"/>
<path d="M460 423V190" stroke="#5d7d84" stroke-width="5" marker-end="url(#blue)"/><text x="512" y="323" font-size="25">海拔</text>
<g transform="translate(114 338)"><path d="M0 0V110" stroke="#567e8b" stroke-width="31" stroke-linecap="round"/><path d="M0 0V110" stroke="#f9fcfd" stroke-width="23" stroke-linecap="round"/><path d="M0 28V110" stroke="#bd7544" stroke-width="13" stroke-linecap="round"/><circle cy="120" r="23" fill="#bd7544" stroke="#567e8b" stroke-width="4"/></g>
<g transform="translate(364 88)"><path d="M0 0V110" stroke="#567e8b" stroke-width="31" stroke-linecap="round"/><path d="M0 0V110" stroke="#f9fcfd" stroke-width="23" stroke-linecap="round"/><path d="M0 76V110" stroke="#6b9db1" stroke-width="13" stroke-linecap="round"/><circle cy="120" r="23" fill="#6b9db1" stroke="#567e8b" stroke-width="4"/></g>
<text x="157" y="528" font-size="26">較低處</text><text x="261" y="122" font-size="26">較高處</text><text x="300" y="572" font-size="23">通常較高處較涼；未指定實測溫差</text>'''

for i,b in enumerate([b1,b2,b3,b4],1):(OUT/f'q-1064-four-image-v2-panel-{i}.svg').write_text(svg(b))
imgs=[f'docs/comics/art/q-1064-four-image-v2-panel-{i}.svg' for i in range(1,5)]
s=dict(id='q-1064',subject='Geography',title='先定位西北非，再理解山地氣候影響',art=imgs[0],panels=[
dict(heading='① 找到摩洛哥與亞特拉斯山脈',text='第一圖標出摩洛哥在非洲西北部；亞特拉斯山脈穿越西北非，南側與東南側接近撒哈拉。題目的甲地應先從這個位置找。',caption='新製定位圖｜海陸依Natural Earth；山脈為概略走向，非國界。',alt='西北非海陸定位圖，摩洛哥以點標出，山脈帶概略從西南往東北延伸，撒哈拉在南側。',image=imgs[0]),
dict(heading='② 屏障會影響氣流，但不完全阻絕',text='第二圖以山地剖面表示海上濕氣與南側熱乾氣流。地形會改變氣流路徑，減弱部分熱乾影響；細虛線保留氣流仍可能越山的情形，不把山畫成密閉牆。',caption='新製氣流機制圖｜不對應特定天氣、風速或精確剖面。',alt='藍色濕氣沿海側抬升，橘色南側熱乾氣流遇山改變方向，細虛線仍可越山，不是完全阻隔。',image=imgs[1]),
dict(heading='③ 其他三個選項位置不符',text='第三圖C在西北非，A阿拉伯高原與D安納托力亞高原在西亞，B東非大裂谷在非洲東部。題目指向摩洛哥，因此C最符合。',caption='新製區域定位圖｜字母對應原選項，標記不代表整個地形範圍。',alt='非洲及鄰近西亞輪廓，C位於西北非，A阿拉伯半島，D安納托力亞，B東非。',image=imgs[2])
],fourth=dict(answer='答案 C：亞特拉斯山脈',points=['第四圖以不同高度的溫度計示海拔影響；未給虛構溫度數字。','位置、緯度、海洋與山地共同影響氣候，不能用單一因素概括全國。','山脈是地形屏障，不代表沙漠空氣絕對無法越過。'],image=imgs[3],alt='同一概念山坡較低處及較高處各一支無數值溫度計，高處表示通常較涼；非實測溫差。'),protectedWords=['亞特拉斯山脈','阿拉伯高原','安納托力亞高原','東非大裂谷','摩洛哥','撒哈拉','西北非'],generationMethod='four authored native SVG regional maps, airflow cross-section and altitude comparison',generatorFile='docs/comics/biology-rework-20261112/q-1064/generate.py',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/assets/originals/q-1064-original-a706c080ed6d.jpg'],answerCheckedAgainst='原卷13題完整題幹及四選項實看；D→C原筆跡保留，題述摩洛哥地形選C亞特拉斯山脈，既有屏障非完全封閉限制照留。',rationale='四圖以真實海陸幾何定位、氣流剖面、選項區域比較及高度氣溫關係解釋原C；地圖不顯示國界，區域標點不假冒地形完整範圍。不新增風速、溫差或絕對阻隔斷言。',producerAgent='/root/comic_lane_1',visualChecked=False,sources=[dict(url='https://eol.jsc.nasa.gov/Collections/EarthObservatory/articles/WetAndDryMorocco.htm',support='NASA/JSC：Atlas穿越摩洛哥/阿爾及利亞/突尼西亞，山地影響沿岸與撒哈拉之間水氣及氣候。'),dict(url='https://www.visitmorocco.com/en/travel-info/climate-and-seasons',support='摩洛哥觀光局官方：北地中海、西大西洋、Rif/Atlas山地等多因素氣候，南側開向撒哈拉。'),dict(url='https://www.naturalearthdata.com/about/terms-of-use/',support='Natural Earth 110m公開領域海陸幾何，SVG不標國界。')],mapData=dict(url=URL,sha256=hashlib.sha256(CACHE.read_bytes()).hexdigest(),projection='regional equirectangular with common degree scale',bordersDisplayed=False))
(ROOT/'docs/comics/q-1064.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
