from pathlib import Path
import json,math,hashlib,datetime,sys
from svg_geometry import compact_ring
R=Path(__file__).resolve().parents[4];P=Path(__file__).parent;A=R/'docs/comics/art';G=P.parent/'geography';TARGETS=set(map(int,sys.argv[1:])) if len(sys.argv)>1 else {1121,1123,1125,1127}
ink='#31566a';ocean='#dcecf3';land='#e5e5d8';red='#ce765d';blue='#6d9db7';green='#9dbca4';gold='#d3ad5b'
def text(x,y,t,size=22,col=ink,anchor='middle',halo=False):
 from html import escape
 return f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" fill="{col}"'+(' stroke="#f8faf8" stroke-width="3" paint-order="stroke"' if halo else '')+'>'+escape(t)+'</text>'
def line(x,y,X,Y,col=ink,w=3,dash=''):return f'<path d="M{x:.2f} {y:.2f}L{X:.2f} {Y:.2f}" fill="none" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def path(d,col=ink,w=3,fill='none'):return f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}"/>'
def circle(x,y,r,fill,stroke='#fff',w=2):return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def arrow(x,y,X,Y,col=red,w=4):
 a=math.atan2(Y-y,X-x);k=10;return line(x,y,X,Y,col,w)+path(f'M{X-k*math.cos(a-.5):.2f} {Y-k*math.sin(a-.5):.2f}L{X:.2f} {Y:.2f}L{X-k*math.cos(a+.5):.2f} {Y-k*math.sin(a+.5):.2f}',col,w)
def rect(x,y,w,h,fill,stroke='none',rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
features=json.load(open(R/'.cache/four-image-maps/ne_10m_admin_0_countries.geojson'))['features'];countries={f['properties']['ADMIN']:f for f in features}
states=json.load(open(R/'.cache/four-image-maps/ne_10m_admin_1_states_provinces.geojson'))['features'];places=json.load(open(R/'.cache/four-image-maps/ne_10m_populated_places.geojson'))['features']
cities={f['properties']['NAME']:f['geometry']['coordinates'] for f in places if f['properties']['NAME'] in ['Rio de Janeiro','Brasília']}
assert cities['Rio de Janeiro'][0]>cities['Brasília'][0] and cities['Rio de Janeiro'][1]<cities['Brasília'][1]
def rings(f):
 g=f['geometry'];return g['coordinates'] if g['type']=='Polygon' else [r for p in g['coordinates'] for r in p]
boxes={}
for f in features:
 pts=[p for r in rings(f) for p in r];boxes[f['properties']['ADMIN']]=(min(p[0] for p in pts),max(p[0] for p in pts),min(p[1] for p in pts),max(p[1] for p in pts))
def geometry(f,xy,bounds=(15,55,345,305)):
 ps=[]
 for ring in rings(f):
  z=compact_ring([xy(*p[:2]) for p in ring],bounds=bounds,tolerance=.22)
  if z:ps.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in z)+'Z')
 return ''.join(ps)
def map_base(bbox,highlights={},area=(15,55,345,305),grid=False):
 lo,hi,la,ha=bbox;l,t,r,b=area;phi=math.radians((la+ha)/2);s=min((r-l)/((hi-lo)*math.cos(phi)),(b-t)/(ha-la));cx=(lo+hi)/2;cy=(la+ha)/2
 def xy(lon,lat):return ((l+r)/2+(lon-cx)*math.cos(phi)*s,(t+b)/2-(lat-cy)*s)
 out=rect(l,t,r-l,b-t,ocean,ink,2)
 for f in features:
  nm=f['properties']['ADMIN'];bl,bh,ba,bt=boxes[nm]
  if bh<lo or bl>hi or bt<la or ba>ha:continue
  d=geometry(f,xy,area)
  if d:out+=f'<path d="{d}" fill="{highlights.get(nm,land)}" stroke="#829395" stroke-width=".75" fill-rule="evenodd"/>'
 if grid:
  for lat in range(-60,81,20):
   if la<lat<ha:
    x,y=xy(lo,lat);X,Y=xy(hi,lat);out+=line(max(l,x),y,min(r,X),Y,'#b9cdd7',.8,'3 4')
 out+=arrow(r-16,t+40,r-16,t+12,ink,2)+text(r-16,t+9,'N',16)
 return out,xy
def label_country(f,xy,name,dx=0,dy=0,size=22):
 p=countries[f]['properties'];x,y=xy(p['LABEL_X'],p['LABEL_Y']);return (line(x,y,x+dx,y+dy,'#6b858b',1.4) if dx or dy else '')+text(x+dx,y+dy,name,size,ink,halo=True)
def point(xy,coords,label,dx=15,dy=-13,col=red,anchor='start'):
 x,y=xy(*coords);return circle(x,y,5,col)+line(x,y,x+dx,y+dy,col,2)+text(x+dx,y+dy-3,label,20,ink,anchor,True)
def save(n,j,s):
 if n not in TARGETS:return
 (A/f'q-{n}-panel-{j}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 360 360"><rect width="360" height="360" fill="#f5f8f7"/>{s}</svg>')
def spec(n,title,panels,fourth,alts,rationale,sources,protected=[]):
 if n not in TARGETS:return
 q=json.load(open(G/f'q-{n}.json'));im=[f'docs/comics/art/q-{n}-panel-{j}.svg' for j in range(1,5)]
 d=dict(id=f'q-{n}',subject='Geography',title=title,art=im[0],layoutVersion='native-four-images-v7',generationMethod='four independent new native SVG maps/physical-geography diagrams; Natural Earth boundaries and city points',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=q['images']+[x['src'] for x in q.get('questionFigures',[])],answerCheckedAgainst=q['explanation'],rationale=rationale,producerAgent='/root/comic_lane_3',visualChecked=False,panels=[dict(heading=h,text=t,image=im[i],alt=alts[i]) for i,(h,t) in enumerate(panels)],fourth=dict(answer=fourth[0],points=fourth[1],image=im[3],alt=alts[3]),protectedWords=protected,manualLineBreaks=False,createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),artHashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in im},supportingSources=sources,mapData=dict(boundaries='.cache/four-image-maps/ne_10m_admin_0_countries.geojson',cities='.cache/four-image-maps/ne_10m_populated_places.geojson',projection='north-up equirectangular with standard parallel at view midpoint; aspect preserved in that projection',simplification='Sutherland-Hodgman clipping and Douglas-Peucker ≤0.22 native pixel perpendicular error',borderSHA256=hashlib.sha256((R/'.cache/four-image-maps/ne_10m_admin_0_countries.geojson').read_bytes()).hexdigest()))
 (R/f'docs/comics/q-{n}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# q1121: different extents and geographic structures, not one repeated colored image.
s,xy=map_base((-128,-65,23,51),{'United States of America':blue});s+=text(180,29,'US：United States',24)+label_country('United States of America',xy,'美國本土',0,0,25)+text(180,337,'本格為本土48州及鄰區局部',18);save(1121,1,s)
s,xy=map_base((-119,-85,13,34),{'Mexico':gold});s+=text(180,29,'M：Mexico',25)+label_country('Mexico',xy,'墨西哥',7,10,24)+text(180,337,'美國以南，連接中美地峽',19);save(1121,2,s)
s,xy=map_base((-145,-50,40,84),{'Canada':green});s+=text(180,29,'C：Canada',25)+label_country('Canada',xy,'加拿大',0,6,25)+text(180,337,'美國本土以北，含北方群島',18);save(1121,3,s)
s,xy=map_base((-180,-50,5,84),{'United States of America':blue,'Canada':green,'Mexico':gold});s+=text(180,29,'USMCA：三國協定',24)
for f,lab,dx,dy in [('Canada','加拿大',0,0),('United States of America','美國',0,0),('Mexico','墨西哥',6,12)]:s+=label_country(f,xy,lab,dx,dy,19)
s+=text(180,337,'A＝Agreement（協定）',22);save(1121,4,s)
spec(1121,'用三國位置，記住USMCA完整名稱',[('① US：美國 United States','先認美國本土在北美的位置。本格只畫本土48州及鄰區；整體圖另可見阿拉斯加，不能把本土圖當成全部領土。'),('② M：墨西哥 Mexico','墨西哥位於美國以南，國土向中美地峽延伸。原作答「美墨加」已知道三個國家，但本題訂正要求USMCA這個形式。'),('③ C：加拿大 Canada','加拿大位於美國本土以北，含北方群島。完整名稱為United States–Mexico–Canada Agreement，末尾A代表Agreement。')],('答案：USMCA',['2018是新協定簽署年；2020年7月1日才生效。三國位置與縮寫對照，不把兩種年份混為一談。']),['新製美國本土48州/加拿大南緣/墨西哥北緣的真國界局部圖，美國本土單獨定位。','新製墨西哥本土區位圖，含下加利福尼亞半島和相鄰國界，不是第一圖只改色。','新製加拿大完整主體與北方群島圖，含鄰近阿拉斯加/格陵蘭灰色背景。','新製北美三締約國整體圖，含阿拉斯加及夏威夷範圍；US/M/C及A Agreement完整整合。'],'四張各自不同視野/國界組合定位美、墨、加及三國整體；非同一底圖只換色。國界與海岸取真GeoJSON，文字依使用者明確USMCA訂正；原題未加英文二字。',[{'url':'https://ustr.gov/issue-areas/industry-manufacturing/industrial-tariffs/free-trade-agreements','finding':'USMCA2018/11/30簽署，2020/7/1生效；NAFTA1994生效。'},{'url':'https://ustr.gov/trade-agreements/free-trade-agreements/united-states-mexico-canada-agreement','finding':'全名United States-Mexico-Canada Agreement。'}],['48州','USMCA','United States','Mexico','Canada','Agreement','2020年7月1日'])
# q1123: exact city coordinates sourced from Natural Earth populated places.
s,xy=map_base((-84,-32,-57,15),{'Brazil':gold});s+=text(180,29,'先辨國家：巴西',24)+label_country('Brazil',xy,'巴西',0,0,26)+text(180,337,'位於南美洲東部',21);save(1123,1,s)
s,xy=map_base((-47.5,-38.5,-27,-18),{'Brazil':'#e4d3a9'})
for f in states:
 if f['properties'].get('admin')=='Brazil' and f['properties'].get('name')=='Rio de Janeiro':s+=f'<path d="{geometry(f,xy)}" fill="#dfb696" stroke="{ink}" stroke-width="1" fill-rule="evenodd"/>'
s+=text(180,29,'原首都：里約熱內盧',23)+point(xy,cities['Rio de Janeiro'],'里約熱內盧',12,-24)+text(279,263,'大西洋',23,ink,halo=True)+text(180,337,'城市點依資料定位；東南沿海',18);save(1123,2,s)
s,xy=map_base((-60,-35,-30,0),{'Brazil':'#e4d3a9'})
for f in states:
 if f['properties'].get('admin')=='Brazil':
  fill=green if f['properties'].get('name')=='Distrito Federal' else 'none'
  s+=f'<path d="{geometry(f,xy)}" fill="{fill}" stroke="#b9aa83" stroke-width=".8" fill-rule="evenodd"/>'
s+=text(180,29,'新首都：巴西利亞',24)+point(xy,cities['Brasília'],'巴西利亞',10,-18,col='#63896b')+text(180,337,'巴西中部內陸，不是沿海港口',19);save(1123,3,s)
s,xy=map_base((-76,-32,-35,7),{'Brazil':'#e7d7ac'});s+=text(180,29,'政治中心：沿海→內陸',23)
x,y=xy(*cities['Rio de Janeiro']);X,Y=xy(*cities['Brasília']);s+=arrow(x,y,X,Y,red,4)+point(xy,cities['Rio de Janeiro'],'原首都',23,31)+point(xy,cities['Brasília'],'新首都',-25,-30,col='#63896b',anchor='end')+text(180,337,'遷都帶動內陸，是政策目的',19);save(1123,4,s)
spec(1123,'看清沿海到內陸，理解遷都目的',[('① 地圖的兩座城市，都在巴西','原卷標示里約熱內盧與巴西利亞，可辨國家是巴西。先確認國家與位置，再連結政策原因。'),('② 里約熱內盧是東南沿海舊都','城市靠近大西洋沿岸。圖中只按真實國界、州界與城市點說明位置，不以自畫人口密度推論集中程度。'),('③ 巴西利亞把政治中心移向內陸','新都位於中部內陸。遷都希望帶動內陸開發、促進國土整合，最符合A均衡區域發展，而非只避災、找礦或找濕潤氣候。')],('答案A：均衡區域發展',['箭頭表示政治中心由里約移向巴西利亞；不表示全體人口移動，或區域差距立即消失。']),['新製南美洲國界圖突出巴西，辨認兩城所屬國家。','新製巴西東南沿海局部真海岸及里約州界，城市點取NaturalEarth Rio de Janeiro坐標。','新製中部內陸局部圖與聯邦區真界，巴西利亞點依NaturalEarth坐標。','新製巴西全圖兩城市真點位及遷都方向箭頭，非人口遷移或交通路線。'],'四張採南美國家辨認、沿海城市近景、內陸新都近景、全國前後比較，城市取資料點、不同尺度不杜撰位置或經濟統計。',[{'url':'https://www.gov.br/sudeco/pt-br/assuntos/ride-df','finding':'遷都與中西部內陸人口/生產活動開發、國土整合相關。'},{'url':'https://www.camara.leg.br/noticias/139678-transferencia-da-capital-para-o-interior-foi-proposta-em-1821','finding':'1960移至Brasilia，面對原先發展/人口主要沿海的國土情況。'}],['里約熱內盧','巴西利亞','均衡區域發展','大西洋','內陸'])
# q1125: exact latitude geometry, actual Mexico, circulation concept, hemispheric summary.
s=text(180,27,'先分半球，再分回歸線與極圈',20)+circle(180,181,124,ocean,ink,3)
for deg,lab in [(66.5,'甲 66.5°N'),(23.5,'乙 23.5°N'),(-23.5,'丙 23.5°S'),(-66.5,'丁 66.5°S')]:
 y=181-124*math.sin(math.radians(deg));h=124*math.cos(math.radians(deg));s+=line(180-h,y,180+h,y,gold if deg==23.5 else blue,3)+text(180,y-5,lab,19)
s+=line(57,181,303,181,ink,2,'5 5')+text(314,186,'0°',17)+arrow(325,102,325,66,ink,2)+text(325,57,'N',16)+text(180,332,'上北下南；乙＝北回歸線',21);save(1125,1,s)
s,xy=map_base((-119,-85,13,34),{'Mexico':gold});x,y=xy(-119,23.5);X,Y=xy(-85,23.5);s+=line(16,y,344,y,red,4,'8 4')+text(180,29,'北回歸線穿過墨西哥',24)+text(176,y-10,'23.5°N',23,red,halo=True)+text(180,337,'國土跨多個緯度，不是只在一線上',17);save(1125,2,s)
s=text(180,28,'副熱帶高壓：下沉不利雲雨',21)
s+=path('M32 262Q180 240 328 262V285Q180 263 32 285Z',ink,2,'#c1d2b8')+text(180,309,'地表',19)
s+=arrow(75,246,75,105,red,5)+arrow(99,91,263,91,red,4)+arrow(280,106,280,225,blue,5)+arrow(259,230,98,230,blue,4)
for y in [132,176,215]:s+=circle(65,y,6,'#ddb0a1',red,1)+circle(290,y-5,6,'#b4cedc',blue,1)
for x,y,r in [(59,92,12),(75,80,15),(93,91,12)]:s+=circle(x,y,r,'#c9d3d8','#8b9ea9',1)
s+=text(75,299,'赤道0°',21)+text(280,299,'約30°N',21)+text(320,181,'下沉',18)+text(37,183,'上升',18)+text(180,342,'南北環流剖面概念，非全國氣候分區',16);save(1125,3,s)
s,xy=map_base((-130,-30,-40,65),{'Mexico':gold});s+=text(180,29,'北半球的墨西哥→乙',24)
for lat,col,lab in [(0,ink,'赤道'),(23.5,red,'北回歸線')]:
 x,y=xy(-130,lat);X,Y=xy(-30,lat);s+=line(max(16,x),y,min(344,X),Y,col,2,'5 4')+text(335,y-6,lab,17,col,'end',True)
s+=label_country('Mexico',xy,'墨西哥',-5,-14,19)+text(180,337,'B乙，不選南回歸線或極圈',20);save(1125,4,s)
spec(1125,'先定位墨西哥，再選北回歸線',[('① 四緯線先按N、S分半球','甲66.5°N是北極圈、乙23.5°N是北回歸線；丙23.5°S、丁66.5°S在南半球。緯度依原題近似值保留。'),('② 北回歸線確實穿過墨西哥','真實國界圖上23.5°N穿過墨西哥。國家有南北範圍，不能說整個國家都落在一條緯線上。'),('③ 乾燥線索是輔助，不是全國氣候','副熱帶高壓常見於約30°附近，下沉空氣不利雲雨。題文可輔助聯想北回歸線附近，但海拔、地形、海流仍影響當地氣候。')],('答案B：乙，北回歸線',['墨西哥在北半球；不把原文概括擴大成全國終年高溫、同一種沙漠氣候。']),['新製正視球面四緯線弦長依Rcosφ、南北位置依Rsinφ繪，保留原甲乙丙丁和66.5/23.5度。','新製墨西哥真國界與23.5N緯線，顯示線穿國土而非全國在單一緯度。','新製赤道上升/約30N下沉的南北垂直環流剖面，省略地轉偏向，不作精確氣候分界。','新製美洲局部真國界、赤道及北回歸線，把墨西哥放回北半球背景後對乙。'],'四張為球面緯線幾何、局部真墨西哥、環流物理剖面、美洲半球整合；不是四個近似同圖換色，不擅改原卷緯度或全國氣候。',[{'url':'https://www.noaa.gov/jetstream/global/global-atmospheric-circulations','finding':'赤道附近上升、約30度高壓下沉，為Hadley環流概念。'},{'url':'https://cuentame.inegi.org.mx/explora/geografia/ubicacion/','finding':'INEGI地理教育：北回歸線穿越墨西哥。'},{'url':'https://cuentame.inegi.gob.mx/explora/geografia/climas/','finding':'墨西哥氣候多樣，北回歸線分主要氣候區域，不能全國視單一氣候。'}],['66.5°N','23.5°N','23.5°S','66.5°S','北回歸線','約30°','墨西哥'])
# q1127: use country positions and conceptual long-term tectonics, never an incident epicenter.
s,xy=map_base((-123,-29,-57,38),{'Mexico':gold,'Cuba':green,'Brazil':'#cab48e','Chile':red});s+=text(180,29,'先用洲別比較四國',24)
for nm,lab,dx,dy in [('Mexico','墨西哥',-10,-9),('Cuba','古巴',20,-10),('Brazil','巴西',10,0),('Chile','智利',-18,0)]:s+=label_country(nm,xy,lab,dx,dy,19)
s+=text(180,337,'墨西哥、古巴不在南美洲',20);save(1127,1,s)
s,xy=map_base((-81,-63,-57,-15),{'Chile':red});s+=text(180,29,'智利：南美洲西側狹長國土',21)+label_country('Chile',xy,'智利',54,0,24)+text(76,190,'太平洋',22,ink,halo=True)+text(180,337,'西臨太平洋，東側鄰安地斯山區',17);save(1127,2,s)
s=text(180,28,'長期構造背景，不是礦災成因圖',19)+rect(15,57,330,252,'#f1e4ce',ink,0)
s+=path('M15 144H131L165 173H15Z',blue,1,ocean)+path('M15 183H133L163 192L209 224L270 264L345 302V321L258 282L196 241L151 211L128 203H15Z',ink,3,'#9eaeb9')+path('M160 174L187 156L211 123L230 150L251 106L280 151L345 148V298L270 259L212 220L166 189Z',ink,3,'#d9b88e')
s+=arrow(49,168,117,168,red,5)+arrow(212,229,255,258,red,4)+text(77,101,'太平洋',22)+text(75,241,'納茲卡板塊',18)+text(284,198,'南美洲',19)+text(284,223,'板塊',19)+text(251,88,'安地斯山',18)+text(180,342,'海洋板塊向東隱沒：概念剖面非比例',16);save(1127,3,s)
s,xy=map_base((-84,-31,-57,15),{'Chile':red});s+=text(180,29,'智利區位＋銅礦線索',23)+label_country('Chile',xy,'智利',-23,0,24)+rect(249,79,77,81,'#f0d2ac',ink,3)+text(287,125,'Cu',35)+text(287,150,'銅',19)+text(180,337,'不補造礦坑、震央或事故現場',18);save(1127,4,s)
spec(1127,'南美洲西側、銅礦線索，辨認智利',[('① 南美洲條件，先排兩個選項','古巴在加勒比海、墨西哥在北美，均不符合題文南美洲。巴西與智利都在南美洲，還要比較礦業與區位線索。'),('② 狹長智利沿太平洋東岸延伸','智利位於南美洲西側，東側鄰安地斯山區，銅礦產業著名。原題地下銅礦事件對應智利，選C。'),('③ 板塊圖只解釋長期區域背景','納茲卡海洋板塊向東隱沒至南美洲板塊下方，是長期地體背景。這不能直接證明本次礦災成因，也不能由題文推造震央。')],('答案C：智利',['位置與銅礦線索共同判讀；原題新聞文字照留，圖不重建救援或傷亡現場。']),['新製美洲真國界圖同時定位墨西哥、古巴、巴西、智利，依洲別排除。','新製智利狹長國土近景及太平洋方位，無礦坑或震央點。','新製太平洋東緣板塊隱沒剖面，納茲卡往東向下、安地斯在大陸側，明示非本次事故成因。','新製南美洲全圖智利位置及Cu銅元素圖例，Cu不代表特定礦坑或礦石外觀。'],'四圖為四國區位比較、智利近景、板塊物理構造、全南美洲銅礦線索整合；沒有虛構精確礦坑/震央，也不以自然隱沒解釋本次礦場事件。',[{'url':'https://www.codelco.com/prensa/2025/sernageomin-autoriza-reinicio-parcial-y-progresivo-de-operaciones','finding':'Codelco確認ElTeniente在2025/7/31發生事故，國家為智利；不據此推原因。'},{'url':'https://www.diariooficial.interior.gob.cl/publicaciones/2025/08/03/44215-B/01/2681587.pdf','finding':'智利官方公報確認7/31 ElTeniente礦災及罹難者。'},{'url':'https://pubs.usgs.gov/publication/ofr20151031E','finding':'USGS南美地體摘要：納茲卡相對南美向東略偏北移動，長期隱沒背景；網頁直讀403但官方搜尋摘要可核。'}],['納茲卡','南美洲','太平洋','安地斯山','墨西哥','智利'])
