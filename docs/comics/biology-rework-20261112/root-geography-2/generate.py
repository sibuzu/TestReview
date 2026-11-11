from pathlib import Path
import json,math,hashlib
from xml.sax.saxutils import escape
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'root-geography'))
from svg_geometry import compact_ring
R=Path(__file__).resolve().parents[4];P=R/'.cache/four-image-maps/ne_10m_admin_0_countries.geojson';W=json.loads(P.read_text())['features']
T=next(f for f in W if f['properties']['ADMIN']=='Taiwan')
TEAL='#397d7a';INK='#294f4d';GOLD='#d5a15b';BLUE='#65a9bb';LAND='#dcd8bf';SEA='#dfedef'
def polys(g):return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
def area(r):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(r,r[1:])))/2
TW=max(polys(T['geometry']),key=lambda p:area(p[0]))
def text(x,y,t,sz=43,c=INK):return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{sz}" font-weight="650" fill="{c}" stroke="#fff9ee" stroke-width="4" paint-order="stroke">{escape(t)}</text>'
def svg(b,bg='#f8f3e7'):return '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640"><defs><linearGradient id="water" x2="0" y2="1"><stop stop-color="#8bc9d1"/><stop offset="1" stop-color="#4e9fb6"/></linearGradient><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="'+TEAL+'"/></marker></defs><rect width="640" height="640" rx="24" fill="'+bg+'"/><g font-family="Noto Sans CJK TC,sans-serif">'+b+'</g></svg>\n'
def line(x1,y1,x2,y2,c=INK,sw=3):return f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" fill="none" stroke="{c}" stroke-width="{sw}"/>'
def arrow(x1,y1,x2,y2,c=TEAL):
 return line(x1,y1,x2,y2,c,6)+f'<path d="M{x2-14} {y2-12}L{x2} {y2}L{x2-14} {y2+12}" fill="none" stroke="{c}" stroke-width="6"/>'
def mapbase(bounds):
 lo,bot,hi,top=bounds;co=math.cos(math.radians((top+bot)/2));sc=min(570/((hi-lo)*co),550/(top-bot));ox=(640-(hi-lo)*co*sc)/2;oy=(640-(top-bot)*sc)/2
 def xy(lon,lat):return ox+(lon-lo)*co*sc,oy+(top-lat)*sc
 def path(p,fill=LAND,stroke=LAND):return '<path d="'+''.join('M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in compact_ring([xy(*v[:2]) for v in r]))+'Z' for r in p if compact_ring([xy(*v[:2]) for v in r]))+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="1"/>'
 body='<defs><clipPath id="view"><rect x="22" y="22" width="596" height="596" rx="18"/></clipPath><clipPath id="africa">'
 for f in W:
  if f['properties'].get('CONTINENT')=='Africa':
   for p in polys(f['geometry']):body+=path(p)
 body+='</clipPath></defs><g clip-path="url(#view)">'
 for f in W:
  for p in polys(f['geometry']):
   r=p[0]
   if max(v[0] for v in r)<lo or min(v[0] for v in r)>hi or max(v[1] for v in r)<bot or min(v[1] for v in r)>top:continue
   body+=path(p)
 body+='</g>'
 return body,xy,path,sc,co
# Taiwan plateau/pond: conceptual elevation and land-use graphics, not parcel/pond counts.
a='<path d="M0 495Q170 455 345 490T640 487V640H0Z" fill="#c8d8bc"/>'
a+='<path d="M90 250L430 170L580 280L240 360Z" fill="#a9c18b" stroke="#8aa578" stroke-width="3"/><path d="M90 250L240 360V440L90 330Z" fill="#b29872"/><path d="M240 360L580 280V360L240 440Z" fill="#c3aa7d"/>'
a+='<ellipse cx="230" cy="250" rx="86" ry="39" fill="#7f9c67"/><ellipse cx="230" cy="246" rx="70" ry="27" fill="url(#water)"/><path d="M183 244Q207 231 234 242T277 241" fill="none" stroke="#d2eef0" stroke-width="4"/>'
a+='<path d="M370 260L515 293L443 335L299 302Z" fill="#83ae6d" stroke="#557c55" stroke-width="3"/>'
for i in range(1,5):
 a+=line(370-i*14,260+i*8.4,515-i*14.4,293+i*8.4,'#b7d690',3)
a+='<path d="M294 249Q338 248 368 281" fill="none" stroke="#347d9d" stroke-width="7"/><path d="M350 271L369 283L365 263" fill="none" stroke="#347d9d" stroke-width="5"/>'
a+=text(266,111,'平坦台地',46)+line(266,127,306,193)+text(173,529,'埤塘蓄水',43)+line(198,492,226,272)+text(449,516,'農田灌溉',43)+line(451,475,432,326)
arts57=[a]
def pond(x,y,rx=49,ry=32):return f'<ellipse cx="{x}" cy="{y}" rx="{rx+7}" ry="{ry+6}" fill="#7f9c67"/><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#water)"/>'
a='<rect x="36" y="162" width="244" height="350" rx="16" fill="#c8d9b0"/><rect x="360" y="162" width="244" height="350" rx="16" fill="#d5d0bf"/>'
for x in [68,122,176,230]:a+=line(x,178,x,490,'#a1bd8a',3)
for y in [207,270,333,396,459]:a+=line(48,y,265,y,'#a1bd8a',3)
a+=pond(152,250,62,41)+pond(166,411,57,38)+pond(472,250,62,41)
a+='<path d="M376 344H590M407 331V491M558 331V491" stroke="#a8aaa3" stroke-width="18"/>'
for x,y in [(428,378),(489,406)]:
 a+=f'<rect x="{x}" y="{y}" width="55" height="60" fill="#8aa5aa" stroke="#617e86" stroke-width="3"/><path d="M{x} {y}L{x+16} {y-16}H{x+70}L{x+55} {y}Z" fill="#64848d"/><path d="M{x+8} {y+18}H{x+46}M{x+8} {y+36}H{x+46}" stroke="#d9e7e9" stroke-width="5"/>'
a+=text(158,121,'農業用地',43)+text(482,121,'用地改變',43)+arrow(298,337,338,337)+text(320,572,'埤塘減少／都市工業增加',37)
arts57.append(a)
a='<ellipse cx="320" cy="386" rx="262" ry="134" fill="#90ad78"/><ellipse cx="320" cy="378" rx="236" ry="112" fill="url(#water)"/>'
for x,y in [(105,397),(123,415),(142,392),(158,420)]:
 a+=f'<path d="M{x} {y}q-5-44-18-65M{x} {y}q6-54 22-79M{x} {y}v-76" fill="none" stroke="#4d8258" stroke-width="6"/>'
for x,y in [(220,320),(330,341),(440,362)]:
 a+=f'<path d="M{x} {y}L{x+91} {y-10}L{x+73} {y+40}L{x-18} {y+50}Z" fill="#466f8b" stroke="#e0e9e5" stroke-width="3"/>'
 for z in [1,2,3]:a+=line(x-4+z*21,y+1,x-22+z*21,y+43,'#91b3ca',1.5)
 a+=line(x-9,y+54,x-9,y+76,'#6e8583',4)
a+='<circle cx="144" cy="144" r="43" fill="#e3b857"/><path d="M463 124L424 180H454L439 225L493 161H463Z" fill="#d1a144" stroke="#ad8034" stroke-width="3"/>'
a+='<path d="M159 246Q180 221 202 244Q225 221 247 246M300 214Q319 192 338 214Q357 191 376 213" fill="none" stroke="#465e58" stroke-width="5"/>'
a+=text(119,554,'棲地',45)+text(489,271,'發電',45)+line(119,520,150,420)
arts57.append(a)
a,xy,path,sc,co=mapbase((119.3,21.6,122.5,25.65));a=path(TW,'#bdcc9f','#8ca87b')
for t,ll in [('甲',(120.2,22.7)),('乙',(120.55,24.0)),('丙',(120.9,24.65)),('丁',(121.2,24.98))]:
 x,y=xy(*ll);c='#b75439' if t=='丁' else '#697670';a+=f'<circle cx="{x}" cy="{y}" r="8" fill="{c}" stroke="#fff8e9" stroke-width="4"/>'+text(x-34,y+14,t,48,c)
 if t=='丁':a+=f'<circle cx="{x}" cy="{y}" r="23" fill="none" stroke="{c}" stroke-width="4"/>'+line(x+22,y,482,140,c)+text(489,119,'桃園',47,c)
arts57.append(a)
# Sahara: broad geographic zone and schematic exchange, never imperial borders or exact routes.
def sahara(xy,sc,co):
 x,y=xy(10,24);return f'<g clip-path="url(#africa)"><ellipse cx="{x}" cy="{y}" rx="{27*sc*co}" ry="{9*sc}" fill="#dfb876" fill-opacity=".68"/></g>'
def region(xy,ll,txt,off=(0,0),c='#b75439',r=18):
 x,y=xy(*ll);return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" fill-opacity=".15" stroke="{c}" stroke-width="4"/>'+text(x+off[0],y+off[1],txt,45,c)
a,xy,path,sc,co=mapbase((-22,-36,56,40));a+=sahara(xy,sc,co)+region(xy,(-6,13),'馬利',(-48,49));a+=text(324,160,'撒哈拉',49)+text(233,561,'非洲',49);arts63=[a]
a,xy,path,sc,co=mapbase((-21,3,21,38));a+=sahara(xy,sc,co)
x1,y1=xy(-6,13);x2,y2=xy(-6,31)
a+=f'<path d="M{x1-15} {y1-30}Q{x1-59} {(y1+y2)/2} {x2-15} {y2+35}" stroke="{TEAL}" stroke-width="7" fill="none"/><path d="M{x2-27} {y2+52}L{x2-15} {y2+35}L{x2-5} {y2+54}" stroke="{TEAL}" stroke-width="6" fill="none"/>'
a+=f'<path d="M{x2+25} {y2+30}Q{x1+74} {(y1+y2)/2} {x1+30} {y1-25}" stroke="#ac7c45" stroke-width="7" fill="none"/><path d="M{x1+18} {y1-44}L{x1+30} {y1-25}L{x1+44} {y1-42}" stroke="#ac7c45" stroke-width="6" fill="none"/>'
a+=text(303,91,'北非',45)+text(177,531,'西非馬利',45)+text(467,269,'商路',45)
# Trade-goods symbols in an explicit inset legend, not geographically located mines.
a+='<rect x="406" y="302" width="143" height="256" rx="15" fill="#fffaf0" stroke="#b9bbac" stroke-width="2"/>'
a+='<path d="M426 371L470 358L508 378L465 391Z" fill="#f3d26f" stroke="#b1873b" stroke-width="3"/><path d="M426 371V397L465 416L508 403V378L465 391Z" fill="#d5a54b" stroke="#b1873b" stroke-width="3"/>'
a+='<path d="M438 452L473 440L507 453L473 466Z" fill="#fff9e9" stroke="#b4b4a2" stroke-width="3"/><path d="M438 452V475L473 489L507 475V453L473 466Z" fill="#e6e7d8" stroke="#b4b4a2" stroke-width="3"/>'+text(473,349,'金',35)+text(473,534,'鹽',35)
arts63.append(a)
a,xy,path,sc,co=mapbase((-20,-2,64,45));a+=sahara(xy,sc,co)
for t,ll,c,off in [('A',(54,32),'#65797f',(0,-25)),('B',(45,22),'#65797f',(18,47)),('C',(8,23),'#b75439',(0,-25)),('D',(33,39),'#65797f',(0,-25))]:a+=region(xy,ll,t,off,c,14)
a+=region(xy,(-6,13),'馬利',(-11,48))+text(476,573,'西亞',45)+text(158,573,'西非',45);arts63.append(a)
a,xy,path,sc,co=mapbase((-20,2,38,38));a+=sahara(xy,sc,co)+region(xy,(-6,13),'馬利',(-14,58))+text(366,199,'撒哈拉',48)+text(462,251,'C',60,'#b75439')
x,y=xy(-6,13);u,v=xy(0,29);a+=f'<path d="M{x+7} {y-28}Q{x+85} {(y+v)/2} {u} {v+20}" fill="none" stroke="{TEAL}" stroke-width="7" stroke-dasharray="12 9"/>'
a+=text(326,555,'跨沙漠貿易',45);arts63.append(a)
for q,arts,bg in [('q-1057',arts57,'#f7f3e8'),('q-1063',arts63,SEA)]:
 for i,a in enumerate(arts,1):(R/f'docs/comics/art/{q}-four-image-v2-panel-{i}.svg').write_text(svg(a,bg))
prov={'data':'Natural Earth v5.1.2 author repository pinned f1890d9f152c896d250a77557a5751a93d494776','url':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/f1890d9f152c896d250a77557a5751a93d494776/geojson/ne_10m_admin_0_countries.geojson','sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'license':'public domain','geometryOptimization':'Visible-view clipping; RDP max perpendicular tolerance 0.25 native pixels; raw source SHA retained','conceptualRegions':'Sahara oval is qualitative, not desert/empire boundary; Mali circle not modern national extent; trade arrows not exact routes or mine locations','q1057':'Pond/field/urbanization/solar scenes conceptual, not cadastral map/count/area/coverage/bird census; Taiwan markers match original relative positions, not surveyed sites'}
(Path(__file__).parent/'map-data-provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n');print('Wrote 8 SVGs, no source data mutation.')
