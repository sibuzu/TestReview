"""Twelve independent illustrations, four per original question q581/582/583."""
from pathlib import Path
from xml.sax.saxutils import escape
import math,json,sys,hashlib
R=Path(__file__).resolve().parents[4];O=R/'docs/comics/art'
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'root-geography'))
from svg_geometry import compact_ring
TEAL='#397c7c';BLUE='#347eae';RED='#b65540';ORANGE='#c48534';INK='#2b4f4c';GOLD='#d6a45c'
def txt(x,y,s,sz=42,c=INK):return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="{sz}" font-weight="650" fill="{c}" stroke="#fff9ec" stroke-width="3" paint-order="stroke">{escape(s)}</text>'
def line(x,y,u,v,c=INK,w=3,dash=''):return f'<path d="M{x:.2f} {y:.2f}L{u:.2f} {v:.2f}" fill="none" stroke="{c}" stroke-width="{w}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def arrow(x,y,u,v,c,w=8):
 a=math.atan2(v-y,u-x);ll=25;ww=13;px=u-ll*math.cos(a);py=v-ll*math.sin(a)
 return line(x,y,u,v,c,w)+f'<path d="M{px-ww*math.sin(a):.2f} {py+ww*math.cos(a):.2f}L{u:.2f} {v:.2f}L{px+ww*math.sin(a):.2f} {py-ww*math.cos(a):.2f}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>'
def svg(b,bg='#f7f4e9'):return '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640"><rect width="640" height="640" rx="24" fill="'+bg+'"/><g font-family="Noto Sans CJK TC,sans-serif">'+b+'</g></svg>\n'
def center(x,y,s=1):return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 27H124V133H0Z" fill="#8ab5bc" stroke="#4d7a82" stroke-width="3"/><path d="M-13 27L62-7L137 27Z" fill="#577e89" stroke="#3b626b" stroke-width="3"/><rect x="50" y="76" width="27" height="57" fill="#436671"/><path d="M15 51H42V75H15ZM84 51H111V75H84Z" fill="#e6eee2"/></g>'
def stage(x,y,s=1):return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 20H167V129H0Z" fill="#e1b887" stroke="#ab7956" stroke-width="3"/><path d="M-12 20L83-13L179 20Z" fill="#be7056"/><path d="M20 43H147V111H20Z" fill="#6b6068"/><path d="M0 129H167L183 149H-16Z" fill="#bc9671"/><path d="M40 51V104M126 51V104" stroke="#c5937d" stroke-width="6"/></g>'
def kite(x,y,s=1):return f'<g transform="translate({x} {y}) scale({s})"><path d="M0-65L45 0L0 65L-45 0Z" fill="#dcaa59" stroke="#7c7351" stroke-width="3"/><path d="M0-65V65M-45 0H45" stroke="#fff1cf" stroke-width="3"/><path d="M0 65q-23 22 4 43t-8 42" fill="none" stroke="#bd745d" stroke-width="4"/></g>'
def plan(highlight=False):
 b='<path d="M0 0H640V178Q458 151 320 212T0 198Z" fill="#cee5e7"/><path d="M0 197Q160 244 320 212T640 178V640H0Z" fill="#cbd7b1"/><path d="M0 275Q180 319 322 281T640 244" fill="none" stroke="#e9dab2" stroke-width="34"/>'
 b+='<ellipse cx="203" cy="416" rx="139" ry="43" fill="#c89073" stroke="#9e6a56" stroke-width="3"/><rect x="418" y="365" width="127" height="118" rx="8" fill="#79a5af" stroke="#497986" stroke-width="3"/>'
 b+=txt(200,425,'主舞臺',39)+txt(482,417,'遊客',34)+txt(482,455,'中心',34)
 b+=txt(168,184,'特技區',35)+txt(458,226,'造型區',35)+kite(170,106,.35)+kite(459,135,.35)
 if highlight:b+='<ellipse cx="334" cy="421" rx="254" ry="93" fill="none" stroke="#bc6047" stroke-width="7"/>'
 return b
# q581/44: plan relationships, not geographic sea name/distance or real building facades.
a=plan()+txt(320,78,'海域未標名',38)+txt(320,590,'場地配置關係示意',36);A=[a]
a=stage(65,256,1.38)+center(399,274,1.32)+txt(179,211,'主舞臺',43)+txt(482,218,'遊客中心',43)
a+='<path d="M306 415Q344 430 385 414" fill="none" stroke="#8aa69b" stroke-width="5"/>'+txt(320,530,'相鄰',48,RED)+txt(320,590,'非真實建築立面或距離比例',30);A.append(a)
a='<rect x="42" y="57" width="556" height="501" rx="18" fill="#d5dfbf"/>'
# Broadcast station and market in relative original positions; distance remains unknown.
a+='<path d="M223 174L197 293H248Z" fill="#899b9c" stroke="#566d73" stroke-width="3"/><circle cx="222" cy="154" r="24" fill="#5b7981"/><path d="M257 136Q281 153 257 173M271 117Q315 155 271 193" stroke="#769494" stroke-width="5" fill="none"/>'
a+=txt(216,104,'播報臺',43)
for x,c in [(355,'#bc775c'),(453,'#659a93')]:a+=f'<path d="M{x} 395H{x+76}V469H{x}Z" fill="#ddc29b"/><path d="M{x-9} 395L{x+38} 360L{x+85} 395Z" fill="{c}"/><path d="M{x+12} 415H{x+64}V451H{x+12}Z" fill="#f0e5cb"/>'
a+=txt(432,515,'市集',43)+line(240,268,386,354,TEAL,5,'9 8')+txt(332,330,'?',61,RED)+txt(320,612,'無比例尺，實際距離未知',33);A.append(a)
a=plan(True)+txt(320,86,'圖上可讀：相鄰',43,RED);A.append(a)
# q582/45: all arrows in a north-up view, exact opposite vectors.
def compass():
 b='<circle cx="320" cy="320" r="214" fill="#e7ece0" stroke="#becdbd" stroke-width="2"/>'
 b+=line(320,106,320,534,'#8daba5',3)+line(106,320,534,320,'#8daba5',3)
 b+=txt(320,65,'北',48)+txt(591,337,'東',48)+txt(320,613,'南',48)+txt(48,337,'西',48)
 return b
a=compass()+arrow(477,477,166,166,BLUE,12)+txt(157,146,'西北',43,BLUE)+txt(480,537,'東南',43,ORANGE)+txt(330,375,'風',57,BLUE);B=[a]
a=compass()+arrow(492,441,213,162,BLUE,10)+arrow(163,224,440,501,ORANGE,10)
a+=txt(431,204,'風',48,BLUE)+txt(206,464,'人',48,ORANGE);B.append(a)
a=compass()+kite(198,196,.72)+line(222,229,369,368,'#6f7770',3)
# Top-view person: head and body, with the hand at the tether endpoint.
a+='<circle cx="393" cy="391" r="22" fill="#dab798"/><path d="M393 416L420 445L390 475L365 447Z" fill="#7aa29b" stroke="#527d79" stroke-width="3"/><path d="M379 421L369 368M414 430L445 417M382 469L365 501M404 470L433 500" fill="none" stroke="#617e7a" stroke-width="10" stroke-linecap="round"/>'
a+=arrow(510,338,362,190,BLUE,9)+arrow(440,473,494,527,ORANGE,9)+txt(181,511,'俯視方位',35);B.append(a)
a=compass()+arrow(479,445,211,177,BLUE,9)+arrow(174,235,425,486,ORANGE,10)
for x,y,t,c in [(503,149,'C 東北','#6d7c75'),(144,149,'D 西北','#6d7c75'),(143,549,'B 西南','#6d7c75'),(495,549,'A 東南',RED)]:a+=txt(x,y,t,40,c)
a+='<circle cx="425" cy="486" r="29" fill="none" stroke="'+RED+'" stroke-width="4"/>';B.append(a)
# q583/46: regional site positions only; no driving route/time or complete culture extent.
p=R/'.cache/four-image-maps/ne_10m_admin_0_countries.geojson';D=json.loads(p.read_text());F=next(f for f in D['features'] if f['properties']['ADMIN']=='Taiwan')
ps=F['geometry']['coordinates'];poly=max(ps,key=lambda p:abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p[0],p[0][1:]))))
def mapbase(bounds):
 lo,bot,hi,top=bounds;co=math.cos(math.radians((top+bot)/2));sc=min(522/((hi-lo)*co),530/(top-bot));ox=(640-(hi-lo)*co*sc)/2;oy=(640-(top-bot)*sc)/2
 def xy(lon,lat):return ox+(lon-lo)*co*sc,oy+(top-lat)*sc
 d=''.join('M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in compact_ring([xy(*v[:2]) for v in ring]))+'Z' for ring in poly if compact_ring([xy(*v[:2]) for v in ring]))
 return '<path d="'+d+'" fill="#c0cfaa" stroke="#91ab84" stroke-width="2"/>',xy
SITES={'石門':(121.55,25.28),'八里':(121.40,25.15),'圓山':(121.52,25.075),'八仙洞':(121.48,23.39)}
def mark(xy,name,c,off=(0,0),label=None):
 x,y=xy(*SITES[name]);u,v=x+off[0],y+off[1]
 return f'<circle cx="{x}" cy="{y}" r="10" fill="{c}" stroke="#fff8e9" stroke-width="4"/>'+line(x,y,u,v,c,3)+txt(u,v-10,label or name,43,c)
a,xy=mapbase((119.4,21.7,122.5,25.7));a+=mark(xy,'石門',ORANGE,(96,30))+txt(313,573,'活動在北部石門',37);C=[a]
a,xy=mapbase((121.18,24.94,121.96,25.47));a+=mark(xy,'石門',ORANGE,(79,-52))+mark(xy,'八里',TEAL,(-90,-24))+mark(xy,'圓山',TEAL,(107,45),label='臺北圓山')
a+=txt(147,414,'十三行／大坌坑',32,TEAL)+txt(320,591,'代表遺址區位，非文化完整範圍',30);C.append(a)
a,xy=mapbase((119.4,21.7,122.5,25.7));a+=mark(xy,'石門',ORANGE,(86,22))+mark(xy,'八仙洞',RED,(126,15),label='臺東長濱')
x,y=xy(*SITES['石門']);u,v=xy(*SITES['八仙洞']);a+=line(x,y,u,v,'#b29675',3,'8 9')+txt(320,602,'區位比較，不是道路或車程',31);C.append(a)
a,xy=mapbase((119.4,21.7,122.5,25.7));a+=mark(xy,'石門',ORANGE,(85,16))+mark(xy,'八仙洞',RED,(128,15),label='A 長濱')
x,y=xy(121.45,25.13);a+=f'<ellipse cx="{x}" cy="{y}" rx="47" ry="31" fill="{TEAL}" fill-opacity=".15" stroke="{TEAL}" stroke-width="3"/>'+line(x-38,y,113,172,TEAL)+txt(120,154,'B／C／D',35,TEAL)
a+=txt(320,596,'就近安排，選不宜的A',37,RED);C.append(a)
for q,arts,bg in [('q-581',A,'#f7f4e9'),('q-582',B,'#faf6e9'),('q-583',C,'#dfedef')]:
 for i,b in enumerate(arts,1):(O/f'{q}-four-image-v2-panel-{i}.svg').write_text(svg(b,bg))
prov={'baseMapURL':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/f1890d9f152c896d250a77557a5751a93d494776/geojson/ne_10m_admin_0_countries.geojson','baseMapSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'mapLicense':'public domain','markers':SITES,'markerMeaning':'Approximate regional positions only; not surveyed site points, travel routes/times, culture extents, or scale measurements.','layoutMeaning':'q581 plan illustrates only relative arrangement checked against original; no added north arrow/sea name/scale or real building facade.','windMeaning':'q582 north-up top view; blue wind SE→NW, orange running NW→SE; not altitude, lift or wind-speed measurement.'}
(Path(__file__).parent/'provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
print('12 independent SVGs written for the 3 original questions')
