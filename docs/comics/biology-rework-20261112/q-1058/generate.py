"""New coordinate and direction diagrams; original island shapes are preserved separately."""
import hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/comics/art'
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson'
CACHE=ROOT/'.cache/q1058-natural-earth-50m.geojson'
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

b1='''<text x="300" y="45" font-weight="bold">日出、山脈、斷崖一起判讀</text><path d="M0 370L80 225L127 284L187 152L242 257V600H0Z" fill="#8da582"/><path d="M242 257V600H193V289Z" fill="#8b927e"/>
<path d="M242 373H600V600H242Z" fill="#73b7cd"/><path d="M260 435q35-15 70 0t70 0t70 0t70 0M260 499q35-15 70 0t70 0t70 0t70 0" fill="none" stroke="#c8e9ed" stroke-width="5"/>
<path d="M435 370A50 50 0 0 1 535 370Z" fill="#e5b456"/><path d="M485 305V286M440 321L427 305M530 322L545 307" stroke="#d9a03c" stroke-width="6"/>
<text x="484" y="274" font-size="34" font-weight="bold">東方</text><text x="135" y="411" font-size="29">山脈、斷崖</text><text x="423" y="539" font-size="29">海域</text><text x="300" y="572" font-size="23">方位概念剖面，不是指定活動地點的重建</text>'''

# A's coordinates are taken directly from the original choice.
b2='<text x="300" y="45" font-weight="bold">A：北緯24.84°、東經121.95°</text><path d="M120 130V470H520" fill="none" stroke="#547780" stroke-width="4"/>'
def gridxy(lon,lat):return 120+(lon-121.8)/.3*360,470-(lat-24.7)/.3*300
for lon in [121.8,121.9,122.0,122.1]:
 x,_=gridxy(lon,24.7);b2+=f'<path d="M{x:.2f} 130V470" stroke="#8fb5c1" stroke-width="2"/><text x="{x:.2f}" y="510" font-size="23">{lon:.1f}</text>'
for lat in [24.7,24.8,24.9,25.0]:
 _,y=gridxy(121.8,lat);b2+=f'<path d="M120 {y:.2f}H480" stroke="#8fb5c1" stroke-width="2"/><text x="74" y="{y+9:.2f}" font-size="23">{lat:.1f}</text>'
x,y=gridxy(121.95,24.84)
b2+=f'<path d="M120 {y:.2f}H{x:.2f}V470" fill="none" stroke="#b57632" stroke-width="5" stroke-dasharray="8 6"/><circle cx="{x:.2f}" cy="{y:.2f}" r="13" fill="#3c816d"/><text x="{x+36:.2f}" y="{y-14:.2f}" font-size="34" font-weight="bold">A</text><text x="472" y="549" font-size="25">東經 °E</text><text x="69" y="108" font-size="25">北緯 °N</text><text x="300" y="581" font-size="22">座標由原卷A讀取，不推算海上活動點</text>'

b3,xy=mapbase((117.7,21.7,123,26.9))
b3='<text x="300" y="45" font-weight="bold">用四組原座標比較位置</text>'+b3
for lon,lat,label,col in [(121.95,24.84,'A','#3e856e'),(118.37,24.45,'B','#ad7b48'),(119.91,26.15,'C','#ad7b48'),(120.36,22.33,'D','#ad7b48')]:
 x,y=xy(lon,lat);b3+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="18" fill="{col}" stroke="white" stroke-width="3"/><text x="{x:.2f}" y="{y+10:.2f}" font-size="30" fill="white" font-weight="bold">{label}</text>'
b3+='<text x="413" y="403" font-size="31">臺灣</text><text x="300" y="573" font-size="23">字母在原座標中心；點的大小不表示島面積</text>'

b4,xy=mapbase((121.0,23.9,122.5,25.5))
b4='<text x="300" y="45" font-weight="bold">A在宜蘭外海：龜山島</text>'+b4
x,y=xy(121.95,24.84)
b4+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="12" fill="#367d69" stroke="white" stroke-width="4"/><path d="M{x+12:.2f} {y:.2f}H485" stroke="#367d69" stroke-width="3"/><text x="461" y="{y-22:.2f}" font-size="29" font-weight="bold">A 龜山島</text>'
x2,y2=xy(121.75,24.75)
b4+=f'<path d="M{x2-8:.2f} {y2:.2f}L170 385" stroke="#48644a" stroke-width="3"/><text x="143" y="415" font-size="29">宜蘭一帶</text><text x="439" y="468" font-size="29">太平洋</text><text x="300" y="573" font-size="23">海岸為Natural Earth概略底圖，島形看原卷</text>'

for i,b in enumerate([b1,b2,b3,b4],1):(OUT/f'q-1058-four-image-v2-panel-{i}.svg').write_text(svg(b))
imgs=[f'docs/comics/art/q-1058-four-image-v2-panel-{i}.svg' for i in range(1,5)]
s=dict(id='q-1058',subject='Geography',title='合看東岸景觀與座標，選宜蘭外海龜山島',art=imgs[0],panels=[
dict(heading='① 日出與山脈、斷崖合看',text='第一圖將日出、山脈與海邊斷崖分別表示，幫助連結臺灣東北至東岸的景觀線索。單靠日出不能指定海域；還要與山脈、斷崖及選項位置核對。',caption='新製方位概念圖｜不新增觀察者站位、航線或指定活動點。',alt='東方海面日出，陸側有山脈及臨海斷崖的概念剖面，不重建某處實景。',image=imgs[0]),
dict(heading='② 讀A的兩個座標',text='第二圖把原卷A的24.84°N、121.95°E，定位到經緯格交會處。先分清北緯與東經，不能把兩個數字顛倒。',caption='新製座標定位圖｜只用原卷數字，不推算活動地點。',alt='經緯網中A精確在東經121.95度、北緯24.84度交會處，兩軸及輔助虛線明示。',image=imgs[1]),
dict(heading='③ B、C、D與A位在不同海域',text='第三圖用四組原座標比較：A宜蘭外海、B金門、C馬祖、D小琉球。D在臺灣西南側，不能因為也是離島就符合本題東北、東岸山海線索。',caption='新製位置比較圖｜字母按原座標，不重繪四幅原島形。',alt='臺灣周邊海陸底圖上，四個字母中心均依原卷經緯度，A東北外海、B西側金門、C西北馬祖、D西南小琉球。',image=imgs[2])
],fourth=dict(answer='答案 A：龜山島',points=['第四圖放大A與宜蘭海岸的地理關係，A是龜山島。','景觀方向與原座標相互支持，不能只憑島名或單一日出線索。','四幅原島圖與座標保留，不以新製概略底圖代替必要原圖。'],image=imgs[3],alt='宜蘭一帶與太平洋的概略海岸底圖，A依原卷座標點示龜山島在宜蘭外海；不描新島形或活動航線。'),protectedWords=['24.84°N','121.95°E','龜山島','小琉球','經緯度','東北','宜蘭外海'],generationMethod='four authored native SVG direction cross-section, exact coordinate grid, four-option locator and coastal summary',generatorFile='docs/comics/biology-rework-20261112/q-1058/generate.py',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/assets/originals/q-1058-original-4d53b5877037.jpg','site/dist/assets/questions/q-1058-figure-bd0cf30f8df5.jpg'],answerCheckedAgainst='實看原卷4題全文與A/B/C/D四幅島圖：A24.84N121.95E、B24.45N118.37E、C26.15N119.91E、D22.33N120.36E；原A龜山島保持。',rationale='四張實際方位及座標圖取代舊文字框。所有四選項座標依原卷，不猜活動點、城市到島距離、航線或新島形；Natural Earth 50m海岸僅位置輔助，原島形保留。',producerAgent='/root/comic_lane_1',visualChecked=False,sources=[dict(url='https://media.taiwan.net.tw/zh-tw/portal/travel/details/attraction_a15011300h_010073',support='觀光署開放資料：龜山島由東北角及宜蘭海岸管理處提供，相關頭城/烏石港與太平洋島嶼位置資料。'),dict(url='https://www.necoast-nsa.gov.tw/Articles.aspx?a=2656&l=1',support='搜尋結果可讀：龜山島在頭城海岸以東；直開遇redirect loop，未宣稱讀到完整頁。'),dict(url='https://www.naturalearthdata.com/about/terms-of-use/',support='Natural Earth公開領域50m海陸幾何。')],mapData=dict(url=URL,sha256=hashlib.sha256(CACHE.read_bytes()).hexdigest(),projection='regional equirectangular with common degree scale',originalIslandShapesReconstructed=False),originalChoiceCoordinates=dict(A=[121.95,24.84],B=[118.37,24.45],C=[119.91,26.15],D=[120.36,22.33]))
(ROOT/'docs/comics/q-1058.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
