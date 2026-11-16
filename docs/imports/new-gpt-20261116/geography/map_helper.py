"""Eight independent locator maps from pinned Natural Earth data, without invented routes or epicenter coordinates."""
from pathlib import Path
import json,math,hashlib,urllib.request
from xml.sax.saxutils import escape
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'docs/comics/biology-rework-20261112/root-geography'))
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
 for f in json.loads((C/'ne_50m_lakes.geojson').read_text())['features']:
  for p in polygons(f['geometry']):
   r=p[0]
   if max(a[0] for a in r)<lo or min(a[0] for a in r)>hi or max(a[1] for a in r)<bot or min(a[1] for a in r)>top:continue
   body+=path(p,SEA,'#8caeb0',.6)
 body+='</g>'
 return body,xy,path

def xianmark(xy,where=None):
 x,y=xy(*cities['Xian']);u,v=where or (x+54,y-27)
 return point(x,y)+link(x+10,y-5,u-20,v-14)+label(u,v,'西安',46)
