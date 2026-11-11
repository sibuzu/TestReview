"""Eight independent locator maps from pinned Natural Earth data, without invented routes or epicenter coordinates."""
from pathlib import Path
import json,math,hashlib,urllib.request
from xml.sax.saxutils import escape
from svg_geometry import compact_ring
R=Path(__file__).resolve().parents[4];C=R/'.cache/four-image-maps';C.mkdir(exist_ok=True)
PIN='f1890d9f152c896d250a77557a5751a93d494776'
FILES=['ne_10m_admin_0_countries','ne_10m_admin_1_states_provinces','ne_10m_populated_places']
Ds={}
for name in FILES:
 p=C/(name+'.geojson')
 if not p.exists():urllib.request.urlretrieve(f'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/{PIN}/geojson/{name}.geojson',p)
 Ds[name]=json.loads(p.read_text())
world=Ds[FILES[0]]['features'];states=Ds[FILES[1]]['features'];places=Ds[FILES[2]]['features']
J=next(f for f in world if f['properties']['ADMIN']=='Japan')
S=next(f for f in states if f['properties'].get('name')=='Shaanxi')
cities={f['properties']['NAME']:f['geometry']['coordinates'] for f in places if f['properties'].get('ADM0NAME')=='China' and f['properties']['NAME'] in ['Xian','Beijing','Shanghai']}
SEA='#e1eff0';LAND='#d9d6bf';EDGE='#afbaa9';TEAL='#337c77';GOLD='#d69b4e';RED='#ba563a';INK='#244b4b'
def polygons(g):return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
def area(r):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(r,r[1:])))/2
HON=max(polygons(J['geometry']),key=lambda p:area(p[0]))
def label(x,y,t,size=43,c=INK,anchor='middle'):
 return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{c}" font-size="{size}" font-weight="650" stroke="#fff9ed" stroke-width="5" paint-order="stroke" stroke-linejoin="round">{escape(t)}</text>'
def point(x,y,c=RED,r=9):return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+5}" fill="#fff9ed"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def ring(x,y,r=25,c=RED):return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" fill-opacity=".15" stroke="{c}" stroke-width="4"/>'
def link(x,y,u,v,c=INK):return f'<path d="M{x:.1f} {y:.1f}L{u:.1f} {v:.1f}" fill="none" stroke="{c}" stroke-width="3"/>'
def svg(b):return '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640"><rect width="640" height="640" rx="24" fill="'+SEA+'"/><g font-family="Noto Sans CJK TC,sans-serif">'+b+'</g></svg>\n'
def mapper(bounds):
 lo,bot,hi,top=bounds;co=math.cos(math.radians((bot+top)/2));sc=min(564/((hi-lo)*co),540/(top-bot));ox=(640-sc*(hi-lo)*co)/2;oy=(640-sc*(top-bot))/2
 def xy(lon,lat):return ox+(lon-lo)*co*sc,oy+(top-lat)*sc
 def path(poly,fill=LAND,stroke=EDGE,sw=1):
  return '<path d="'+''.join('M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in compact_ring([xy(*p[:2]) for p in r]))+'Z' for r in poly if compact_ring([xy(*p[:2]) for p in r]))+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="'+str(sw)+'" stroke-linejoin="round"/>'
 body='<defs><clipPath id="map"><rect x="22" y="22" width="596" height="596" rx="20"/></clipPath></defs><g clip-path="url(#map)">'
 for f in world:
  for p in polygons(f['geometry']):
   r=p[0]
   if max(a[0] for a in r)<lo or min(a[0] for a in r)>hi or max(a[1] for a in r)<bot or min(a[1] for a in r)>top:continue
   body+=path(p)
 body+='</g>'
 return body,xy,path

def xianmark(xy,where=None):
 x,y=xy(*cities['Xian']);u,v=where or (x+54,y-27)
 return point(x,y)+link(x+10,y-5,u-20,v-14)+label(u,v,'西安',46)
# q096: continental inland direction, province, contrast cities, focused province/land context.
a,xy,path=mapper((20,7,143,63));a+=xianmark(xy,(491,366))
x,y=xy(*cities['Xian']);u,v=xy(75,39)
a+=f'<path d="M{x-14:.1f} {y:.1f}Q{(x+u)/2:.1f} {v+10:.1f} {u:.1f} {v:.1f}" stroke="{RED}" stroke-width="6" fill="none"/><path d="M{u+20:.1f} {v-9:.1f}L{u:.1f} {v:.1f}L{u+18:.1f} {v+12:.1f}" fill="none" stroke="{RED}" stroke-width="6"/>'
a+=label(267,220,'陸上方向',43)+label(344,544,'海洋',43,c='#3a8292')
arts96=[a]
a,xy,path=mapper((73,17,136,55));a+='<g clip-path="url(#map)">'+''.join(path(p,GOLD,'#a57137',2) for p in polygons(S['geometry']))+'</g>'
x,y=xy(109,36);a+=label(x+48,y-50,'陝西',47)+xianmark(xy,(395,420));arts96.append(a)
a,xy,path=mapper((99,26,126,44))
for name,t,c in [('Xian','西安',RED),('Beijing','北京',TEAL),('Shanghai','上海','#576da0')]:
 x,y=xy(*cities[name]);a+=point(x,y,c,10)+label(x+2,y-24,t,48,c)
a+=label(154,548,'內陸',46)+label(519,548,'沿海',46,c='#3a8292');arts96.append(a)
a,xy,path=mapper((102,29,119,40));a+='<g clip-path="url(#map)">'+''.join(path(p,GOLD,'#a57137',2) for p in polygons(S['geometry']))+'</g>'
a+=xianmark(xy,(367,405))+label(272,165,'陝西',49)+label(320,570,'屬西部地區',45);arts96.append(a)
# q143: Honshu among islands, Japan Sea/Pacific sides, real Noto coast zoom, source-point comparison.
a,xy,path=mapper((128,29,147,47));a+=path(HON,GOLD,'#a57137',2)
a+=label(349,365,'本州',52)+label(490,117,'北海道',42)+label(139,535,'九州',45)+label(263,505,'四國',43);arts143=[a]
a,xy,path=mapper((128,29,147,47));a+=path(HON,'#e1b16e','#a57137',2)
a+=label(189,274,'日本海',49,c='#367e93')+label(474,451,'太平洋',49,c='#367e93')
x,y=xy(136.9,37.2);a+=ring(x,y,27)+link(x-18,y-20,240,300)
a+=label(401,353,'本州',45);arts143.append(a)
a,xy,path=mapper((135.6,35.7,138.3,38.2));x,y=xy(136.95,37.25);a+=ring(x,y,55)+link(x+38,y-37,455,152)+label(455,134,'能登半島',43)
u,v=xy(136.7,36.6);a+=label(140,220,'日本海',45,c='#367e93')+link(u,v,435,498)+label(471,536,'石川縣',44);arts143.append(a)
a,xy,path=mapper((128,29,147,47));a+=path(HON,'#e1b16e','#a57137',2)
# Match relative original-map sites only; these are not measured earthquake epicenters.
markers=[('甲',(130.6,31.4),(-12,55),'#6b7474'),('乙',(133.3,34.6),(26,38),'#6b7474'),('丙',(136.9,37.2),(-51,-7),RED),('丁',(141.8,39),(47,18),'#6b7474')]
for t,ll,off,c in markers:
 x,y=xy(*ll);a+=point(x,y,c,9)+label(x+off[0],y+off[1],t,54,c)
 if t=='丙':a+=ring(x,y,26,RED)
a+=label(178,219,'日本海',44,c='#367e93')+label(465,520,'太平洋',44,c='#367e93');arts143.append(a)
for q,arts in [('q-096',arts96),('q-143',arts143)]:
 for i,a in enumerate(arts,1):(R/f'docs/comics/art/{q}-four-image-v2-panel-{i}.svg').write_text(svg(a))
prov={'dataset':'Natural Earth v5.1.2, pinned author repository','commit':PIN,'license':'public domain','licenseURL':'https://www.naturalearthdata.com/about/terms-of-use/','projection':'regional equirectangular, x corrected by cos(mid-latitude), no distance measurement claimed','geometryOptimization':'Visible-view clipping, RDP max perpendicular tolerance 0.25 native pixels; raw source SHA retained','dataFiles':[{'url':f'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/{PIN}/geojson/{n}.geojson','sha256':hashlib.sha256((C/(n+'.geojson')).read_bytes()).hexdigest()} for n in FILES],'cities':cities,'q143Markers':'Relative approximations from the original map, not instrumentally measured epicenters; Noto circle denotes region.'}
(Path(__file__).parent/'map-data-provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
print('Wrote 8 independent SVGs and pinned data provenance.')
