from pathlib import Path
import json,math,hashlib
from xml.sax.saxutils import escape
from svg_geometry import compact_ring
R=Path(__file__).resolve().parents[3];OUT=R/'docs/comics/art';CACHE=R/'.cache/four-image-maps'
WORLD=json.load(open(CACHE/'ne_10m_admin_0_countries.geojson'))['features'];PLACES=json.load(open(CACHE/'ne_10m_populated_places.geojson'))['features']
CITY={x['properties']['NAME']:x['geometry']['coordinates'] for x in PLACES}
CITY['Ruijin']=[116.0,25.9] # locality approximation, within official municipal coordinates, not site survey.
INK='#244d56';RED='#bc573a';TEAL='#287c79';GOLD='#ce9e4f';BLUE='#507ca0';LAND='#d8ddc4';SEA='#e7f3f2'
def label(x,y,t,size=42,c=INK,anchor='middle'):
 return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{c}" font-size="{size}" font-weight="650" stroke="#fffaf0" stroke-width="3" paint-order="stroke">{escape(t)}</text>'
def lines(x,y,ls,size=38,c=INK,anchor='middle',gap=46):return ''.join(label(x,y+i*gap,t,size,c,anchor) for i,t in enumerate(ls))
def line(x,y,u,v,c=INK,sw=4,dash=''):
 return f'<path d="M{x:.1f} {y:.1f}L{u:.1f} {v:.1f}" fill="none" stroke="{c}" stroke-width="{sw}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def arrow(x,y,u,v,c=RED):
 a=math.atan2(v-y,u-x);e=20
 return line(x,y,u,v,c,6)+f'<path d="M{u-e*math.cos(a-.5):.1f},{v-e*math.sin(a-.5):.1f}L{u:.1f},{v:.1f}L{u-e*math.cos(a+.5):.1f},{v-e*math.sin(a+.5):.1f}" fill="none" stroke="{c}" stroke-width="6"/>'
def dot(x,y,c=RED,r=9):return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+5}" fill="#fffaf0"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def svg(body,bg='#fffaf0'):
 return '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640"><rect width="640" height="640" rx="22" fill="'+bg+'"/><g font-family="Noto Sans CJK TC,sans-serif">'+body+'</g></svg>\n'
def save(q,n,b,bg='#fffaf0'):
 p=OUT/f'{q}-source72-{n}.svg';p.write_text(svg(b,bg));return str(p.relative_to(R))
def polygons(g):return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
def mapview(bounds):
 lo,bot,hi,top=bounds;co=math.cos(math.radians((bot+top)/2));sc=min(564/((hi-lo)*co),500/(top-bot));ox=(640-sc*(hi-lo)*co)/2;oy=90+(500-sc*(top-bot))/2
 def xy(lon,lat):return ox+(lon-lo)*co*sc,oy+(top-lat)*sc
 body='<defs><clipPath id="m"><rect x="24" y="75" width="592" height="515" rx="12"/></clipPath></defs><g clip-path="url(#m)">'
 for f in WORLD:
  for poly in polygons(f['geometry']):
   rr=poly[0]
   if max(p[0] for p in rr)<lo or min(p[0] for p in rr)>hi or max(p[1] for p in rr)<bot or min(p[1] for p in rr)>top:continue
   pts=[compact_ring([xy(*p[:2]) for p in r],(24,75,616,590)) for r in poly];pts=[p for p in pts if p]
   if pts:body+='<path d="'+''.join('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in r)+'Z' for r in pts)+'" fill="'+LAND+'" stroke="#a6b8a6" stroke-width="1.5"/>'
 return body+'</g>',xy

def city(xy,name,zh,dx=0,dy=-24,c=RED):
 x,y=xy(*CITY[name]);return dot(x,y,c)+label(x+dx,y+dy,zh,43,c)
def timeline(events,start,end,title='',colors=None):
 b=label(320,55,title,42)+line(320,112,320,545,INK,5)
 for yr,lab,side in events:
  y=115+(yr-start)/(end-start)*420;c=(colors or {}).get(yr,TEAL);x=278 if side<0 else 362;a='end' if side<0 else 'start'
  b+=dot(320,y,c,9)+line(307,y,333,y,c,5)+label(x,y-10,str(yr),44,c,a)+lines(x,y+30,lab,34,c,a,gap=39)
 return b+label(320,610,'年代按比例定位',30,'#657e7f')
def book(x,y,w=120,h=120,c=TEAL):
 return f'<path d="M{x} {y}Q{x+w/2} {y-18} {x+w} {y}V{y+h}Q{x+w/2} {y+h-18} {x} {y+h}Z" fill="#f9f2d9" stroke="{c}" stroke-width="5"/>'+line(x+17,y+15,x+17,y+h-10,c,3)+''.join(line(x+32,y+i,x+w-18,y+i,c,2) for i in [24,44,64,84])
def hall(x,y,w=130,c=TEAL):
 b=f'<path d="M{x-8} {y+30}L{x+w/2} {y}L{x+w+8} {y+30}Z" fill="{c}"/>'
 for dx in [10,45,80,115]:b+=f'<rect x="{x+dx-7}" y="{y+37}" width="14" height="78" rx="3" fill="{c}"/>'
 return b+f'<rect x="{x-6}" y="{y+119}" width="{w+12}" height="10" fill="{c}"/>'
def authority():
 b=label(320,58,'1931 訓政體制',44)+hall(255,92,130,GOLD)+label(320,265,'國民黨',48,GOLD)
 for x,title,ls,c in [(110,'政權',['全國代表大會','行使統治權'],TEAL),(320,'組閣權',['中央執委會','選任國府委員'],BLUE),(530,'釋法權',['中央執委會','解釋約法'],RED)]:
  b+=arrow(320,284,x,340,c)+hall(x-65,357,130,c)+label(x,535,title,38,c)+lines(x,577,ls,27,c,gap=31)
 return b
if __name__=='__main__':
 b,xy=mapview((107,21,125,36));b+=label(320,49,'南京與江西瑞金',45)+city(xy,'Nanjing','南京',30,-23,c=BLUE)+city(xy,'Ruijin','瑞金',40,52,c=RED)+label(225,390,'江西',43,TEAL)+label(320,626,'現代底圖僅供定位',29,'#657e7f');save('q-1137',2,b,SEA)
 save('q-1137',4,timeline([(1931,['瑞金政權'], -1),(1945,['戰後美國','開始調停'],1)],1930,1947,'分清兩個歷史階段'))
 save('q-1138',2,authority())
 save('q-1138',3,timeline([(1912,['臨時約法'],-1),(1914,['中華民國約法'],1),(1931,['訓政約法'],-1),(1936,['五五憲草'],1)],1910,1938,'四部文件的年代'))
 prov={'dataSource':'Natural Earth pinned project cache; modern physical locator background, not a historical boundary reconstruction','files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [CACHE/'ne_10m_admin_0_countries.geojson',CACHE/'ne_10m_populated_places.geojson']],'Ruijin':{'coordinate':CITY['Ruijin'],'precision':'city-area approximation only','officialMunicipalRangeURL':'https://www.ruijin.gov.cn/rjsxxgk/rjin79480/202304/410f96b759f64c4db122534696e31974.shtml'},'cityCoordinates':{k:CITY[k] for k in ['Nanjing','Beijing','Guangzhou','Wuhan','Shenyeng','Xian','Shanghai','Chongqing','Hanoi','Ho Chi Minh City']}}
 (Path(__file__).parent/'map-provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
 print('Wrote q1137/q1138 4 native SVGs; no shared bank mutations')
