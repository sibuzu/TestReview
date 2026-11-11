"""Four native regional/seasonal climate illustrations; no station data invented."""
import hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/comics/art'
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson'
CACHE=ROOT/'.cache/q1064-natural-earth-countries.geojson'
if not CACHE.exists():urllib.request.urlretrieve(URL,CACHE)
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

def cloud(x,y,s=1):
 return f'<g transform="translate({x} {y}) scale({s})"><path d="M-75 35C-120 35-122-17-80-22C-85-65-28-80-9-47C20-90 84-57 70-18C122-12 115 40 70 40H-75Z" fill="#f6fcff" stroke="#91b2c2" stroke-width="3"/></g>'

b1,xy=mapbase((-19,20,10,43))
b1='<text x="300" y="45" font-weight="bold">題述亞特拉斯以西沿海</text>'+b1
pts=[xy(*p) for p in [(-9.2,30.1),(-6,31.6),(-3,33),(0,34),(3,35),(6,35.5),(9,36)]]
b1+='<path d="M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'" fill="none" stroke="#9d713e" stroke-width="11" stroke-linecap="round"/>'
x,y=xy(-8,33)
b1+=f'<circle cx="{x}" cy="{y}" r="26" fill="#6b9b81" fill-opacity=".45" stroke="#4b7c68" stroke-width="4"/><path d="M{x-20} {y-15}L108 209" stroke="#426658" stroke-width="3"/>'
b1+='<text x="111" y="189" font-size="27">沿海位置</text><text x="389" y="288" font-size="28">亞特拉斯</text><text x="328" y="433" font-size="30">乾燥內陸</text><text x="91" y="381" font-size="26">大西洋</text><text x="300" y="573" font-size="23">圈只示題目討論位置，非整個馬格里布界線</text>'

b2='''<text x="300" y="45" font-weight="bold">夏季：炎熱、較乾燥</text><path d="M0 455Q115 434 220 456T440 456T600 448V600H0Z" fill="#d8bd83"/>
<circle cx="465" cy="128" r="43" fill="#e5b953"/><path d="M465 66V49M465 190V207M403 128H385M527 128H545M422 86L410 73M507 171L520 184" stroke="#d7a442" stroke-width="7"/>
<path d="M170 130V338M292 130V338" stroke="#b77530" stroke-width="12" marker-end="url(#warm)"/>
<text x="238" y="100" font-size="28">副熱帶高氣壓</text><text x="241" y="385" font-size="27">下沉氣流，較不易成雨</text>
<path d="M70 504L130 478L180 505L249 478L296 510M177 505L164 539M249 478L260 455M296 510L348 536" fill="none" stroke="#b2915f" stroke-width="4"/>
<text x="300" y="572" font-size="23">夏乾概念圖，不是每個地點都無雨</text>'''

b3='''<text x="300" y="45" font-weight="bold">冬半年：西風較易帶來降水</text><path d="M0 443Q130 416 245 447T480 444T600 434V600H0Z" fill="#8fa57d"/>
<path d="M0 443H132V600H0Z" fill="#73b7c8"/>
<path d="M25 252Q147 245 250 242" fill="none" stroke="#2c819f" stroke-width="12" marker-end="url(#blue)"/>
<text x="128" y="208" font-size="28">西風帶來水氣</text>
<path d="M315 313l-18 44M350 316l-18 44M385 316l-18 44M420 312l-18 44" stroke="#378ba7" stroke-width="7" stroke-linecap="round"/>
<path d="M17 488q25-15 50 0t50 0M0 536q25-15 50 0t50 0" fill="none" stroke="#bfe5ec" stroke-width="5"/>
<text x="80" y="407" font-size="25">海洋</text><text x="375" y="499" font-size="27">沿海較有雨</text><text x="300" y="572" font-size="23">冬雨指較多雨的季節，不是每天必定下雨</text>'''+cloud(375,245,.8)

b4='<text x="300" y="45" font-weight="bold">夏乾、冬雨的季節對比</text><text x="300" y="88" font-size="23">概念柱高：不代表測站數值</text><path d="M115 150V475H540" fill="none" stroke="#4f7480" stroke-width="4"/><text x="89" y="145" font-size="23">雨較多</text><text x="74" y="470" font-size="23">較少</text>'
for x,h,season,c in [(165,100,'春','#7aa8b4'),(265,22,'夏','#c69d50'),(365,165,'秋','#7aa8b4'),(465,250,'冬','#4a8fa7')]:
 b4+=f'<rect x="{x}" y="{475-h}" width="48" height="{h}" rx="3" fill="{c}"/><text x="{x+24}" y="516">{season}</text>'
b4+='<text x="300" y="573" font-size="24">題目沿海氣候特徵，不能代表所有族人居住地</text>'
for i,b in enumerate([b1,b2,b3,b4],1):(OUT/f'q-1061-four-image-v2-panel-{i}.svg').write_text(svg(b))
imgs=[f'docs/comics/art/q-1061-four-image-v2-panel-{i}.svg' for i in range(1,5)]
s=dict(id='q-1061',subject='Geography',title='沿海地中海型氣候：夏乾、冬雨',art=imgs[0],panels=[
dict(heading='① 先用山脈位置定位沿海',text='第一圖以亞特拉斯山脈概略位置，指出題目討論的西北非沿海。依這個位置判讀氣候，不以民族名稱推定每個人的生活都相同。',caption='新製定位圖｜圈示討論位置，不畫整個馬格里布界線。',alt='西北非海陸輪廓、亞特拉斯概略山脈線與其西側沿海位置圓圈；內陸另標較乾燥區域。',image=imgs[0]),
dict(heading='② 夏季受副熱帶高氣壓影響',text='第二圖用下沉氣流與晴朗地表，表示夏季較炎熱乾燥、較不易成雨。這符合A的前半句，不是D所說的每天午後雷陣雨。',caption='新製夏季機制示意｜不對應某個日期或指定降雨量。',alt='副熱帶高氣壓下的下沉氣流箭頭、太陽及乾燥地表，沒有每日午後雷雨。',image=imgs[1]),
dict(heading='③ 之後冬半年，西風帶來水氣',text='第三圖表示冬半年西風較易把海上水氣帶入，形成較多雨的季節。A所說的陰雨半年是季節特徵，不是每一天都一定下雨。',caption='新製冬雨機制示意｜海上水氣隨西風移入沿海。',alt='西風從海洋往沿海移動，帶入水氣，沿海上方雲層及雨線示冬半年較多雨。',image=imgs[2])
],fourth=dict(answer='答案 A：夏季炎熱乾燥，之後較多雨',points=['第四圖以季節柱高總結夏乾冬雨；沒有新增測站數值。','題目最直接對應地中海型氣候，不以遷徙或午後雷雨取代判讀。','區域內仍有山地與內陸差異，不把A當成所有居住地一致的實況。'],image=imgs[3],alt='春夏秋冬四根無數值概念雨柱，夏較低、冬較高，強調地中海型氣候的季節差異。'),protectedWords=['副熱帶高氣壓','亞特拉斯山脈','地中海型','馬格里布','夏乾冬雨','冬半年','西北非'],generationMethod='four authored native SVG coastal map, summer subsidence, winter maritime airflow and qualitative seasonal rainfall comparison',generatorFile='docs/comics/biology-rework-20261112/q-1061/generate.py',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/assets/originals/q-1061-original-57322028e564.jpg','site/dist/assets/questions/q-1061-figure-211d3ab8b6c9.jpg'],answerCheckedAgainst='完整原卷19題及圖十實看，山脈在非洲西北部；A夏乾冬雨不變，保留不概括全部居住地及非天天雨限制。',rationale='四張實際地理/氣流/季節圖替換舊文字框。沿海位置以點圈概示不猜族群完整居住界，季節雨量只有概念形狀不捏造數據；不畫族群服飾與刻板生活形象。',producerAgent='/root/comic_lane_1',visualChecked=False,sources=[dict(url='https://www.fao.org/4/T0122E/t0122e03.htm',support='FAO：乾燥下沉氣流與副熱帶反氣旋；摩洛哥Rabat例夏乾、冬雨，季節差異明確。'),dict(url='https://weather.metoffice.gov.uk/climate/climate-explained/climate-zones',support='Met Office：地中海型為夏乾、冬季溫和較濕。'),dict(url='https://eol.jsc.nasa.gov/Collections/EarthObservatory/articles/WetAndDryMorocco.htm',support='NASA/JSC：Atlas分隔較濕海岸及乾燥內陸；地域差異不能抹平。'),dict(url='https://www.naturalearthdata.com/about/terms-of-use/',support='Natural Earth公開領域海陸幾何。')],mapData=dict(url=URL,sha256=hashlib.sha256(CACHE.read_bytes()).hexdigest(),projection='regional equirectangular with common degree scale'))
(ROOT/'docs/comics/q-1061.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
