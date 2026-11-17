"""28 distinct authored graphic illustrations; no source-AI art is used."""
import json,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parents[4];A=R/'docs/comics/art'
DATA=json.loads((R/'.cache/q1058-natural-earth-50m.geojson').read_text())['features']
def text(x,y,t,size=32,color='#294b58'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="middle" font-weight="600">{t}</text>'
def arrow(x,y,xx,yy,col='#d27842'):
 return f'<path d="M{x} {y}L{xx} {yy}" fill="none" stroke="{col}" stroke-width="7" marker-end="url(#arr)"/>'
def image(n,p,body):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600"><defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#e9f4f6"/><stop offset="1" stop-color="#fff4df"/></linearGradient><linearGradient id="stone" x2="0" y2="1"><stop stop-color="#f9ead0"/><stop offset="1" stop-color="#c4a67b"/></linearGradient><linearGradient id="sea" x2="0" y2="1"><stop stop-color="#d7edf5"/><stop offset="1" stop-color="#a9d3e5"/></linearGradient><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#d27842"/></marker><filter id="shadow"><feDropShadow dx="0" dy="5" stdDeviation="3" flood-opacity=".13"/></filter></defs><rect width="600" height="600" rx="22" fill="url(#bg)"/><g font-family="Noto Sans CJK TC,sans-serif">'+body+'</g></svg>'
 (A/f'q-{n}-panel-{p}.svg').write_text(s)
def building(x,y,s=1,label='法院',color='#b59669'):
 b='<g filter="url(#shadow)"><path d="M0 95L160 12L320 95Z" fill="'+color+'" stroke="#75614b" stroke-width="3"/><path d="M20 96H300V246H20Z" fill="url(#stone)" stroke="#907b61" stroke-width="3"/>'
 for xx in [42,90,210,258]:
  b+=f'<rect x="{xx}" y="110" width="20" height="131" fill="#f1e7d3" stroke="#9f8968" stroke-width="2"/><path d="M{xx-4} 110h28M{xx-4} 239h28" stroke="#9f8968" stroke-width="7"/>'
 b+='<path d="M133 144Q160 120 187 144V242H133Z" fill="#668996"/><path d="M160 140V241" stroke="#d3e3e8" stroke-width="3"/><path d="M10 249H310M0 262H320M-10 275H330" stroke="#b49670" stroke-width="13"/>'+text(160,86,label,30,'#fff9ed')+'</g>'
 return f'<g transform="translate({x} {y}) scale({s})">'+b+'</g>'
def paper(x,y,label,s=1,col='#df9561'):
 return f'<g transform="translate({x} {y}) scale({s})" filter="url(#shadow)"><path d="M0 0H110L145 36V190H0Z" fill="#fffdf7" stroke="#708c95" stroke-width="4"/><path d="M110 0V36H145" fill="#dce9ec" stroke="#708c95" stroke-width="3"/>'+text(72,78,label,29)+f'<path d="M22 104H121M22 122H121M22 140H105" stroke="#b7c6cb" stroke-width="5"/><circle cx="105" cy="164" r="15" fill="none" stroke="{col}" stroke-width="4"/></g>'
def ballot(x,y,label,s=1):
 return f'<g transform="translate({x} {y}) scale({s})">'+paper(0,0,label,1)+ '<circle cx="72" cy="144" r="20" fill="none" stroke="#2e896f" stroke-width="5"/><path d="M60 145l9 9 18-24" fill="none" stroke="#2e896f" stroke-width="6"/></g>'
def box(x,y,label,s=1):
 return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 55L65 15L210 30L160 75Z" fill="#7aa1af"/><path d="M0 55L160 75V235L0 210Z" fill="#4b7c91"/><path d="M160 75L210 30V191L160 235Z" fill="#31566b"/><path d="M58 48L156 57" stroke="#173f50" stroke-width="10"/>'+text(81,157,label,30,'#fff')+'</g>'
def bench(x,y,s=1,label='審判'):
 return f'<g transform="translate({x} {y}) scale({s})"><rect x="30" y="30" width="190" height="115" rx="14" fill="#4d5d6a"/><path d="M0 145H250V240H0Z" fill="#9e744e" stroke="#6f5039" stroke-width="4"/><path d="M15 165H235M15 218H235" stroke="#d1ac81" stroke-width="4"/><circle cx="125" cy="88" r="26" fill="#efc6a4"/><path d="M88 139Q90 105 125 109Q159 105 163 139" fill="#3f4860"/>'+text(125,199,label,31,'#fff5e7')+'</g>'
def chamber(x,y,s=1,label='議會'):
 b='<path d="M0 165Q160-80 320 165V240H0Z" fill="#e6ddc7" stroke="#a4a081" stroke-width="3"/>'
 for row in range(3):
  for j in range(5):
   xx=36+j*58;yy=105+row*43;b+=f'<rect x="{xx}" y="{yy}" width="33" height="24" rx="6" fill="#5f8d99" stroke="#416c79" stroke-width="2"/>'
 bw=max(90,30*len(label)+24)
 b+=f'<rect x="{160-bw/2}" y="20" width="{bw}" height="55" fill="#a77f58"/>'+text(160,58,label,27,'#fff8e7')
 return f'<g transform="translate({x} {y}) scale({s})">'+b+'</g>'
def mapbase(bounds,selection=None,fill='#d6c79e',borders=True,frame=(35,90,530,445)):
 left,bottom,right,top=bounds;xx,yy,w,h=frame;k=min(w/(right-left),h/(top-bottom));ox=xx+(w-(right-left)*k)/2;oy=yy+(h-(top-bottom)*k)/2
 def xy(lon,lat):return ox+(lon-left)*k,oy+(top-lat)*k
 result=f'<rect x="{xx}" y="{yy}" width="{w}" height="{h}" rx="16" fill="url(#sea)"/><defs><clipPath id="mf"><rect x="{xx}" y="{yy}" width="{w}" height="{h}" rx="16"/></clipPath></defs><g clip-path="url(#mf)">'
 chosen=[]
 for f in DATA:
  if selection and not selection(f):continue
  geom=f['geometry'];polys=[geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates']
  for poly in polys:
   ring=poly[0]
   if max(p[0] for p in ring)<left or min(p[0] for p in ring)>right or max(p[1] for p in ring)<bottom or min(p[1] for p in ring)>top:continue
   d='M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in [xy(*p[:2]) for p in ring])+'Z';chosen.append(d)
   result+=f'<path d="{d}" fill="{fill}" stroke="#839791" stroke-width="{1.1 if borders else .25}"/>'
 return result+'</g>',xy,chosen
def taiwan(pin,label):
 b,xy,_=mapbase((119.2,21.7,122.2,25.5),lambda f:f['properties']['ADMIN']=='Taiwan',frame=(70,85,330,430));x,y=xy(*pin)
 return b+f'<circle cx="{x}" cy="{y}" r="12" fill="#bd5c42" stroke="white" stroke-width="3"/><path d="M{x+12} {y}H480" stroke="#bd5c42" stroke-width="3"/>'+text(468,y-12,label,31)

# Juvenile justice: architectural/role illustrations, rather than text boxes.
image(1136,1,building(85,130,1.3,'少年法庭')+paper(40,375,'調查',.68)+text(300,63,'甲：先調查少年事件',34))
image(1136,2,building(275,105,.75,'檢察署')+paper(75,210,'偵查',1.2)+paper(300,330,'起訴',.95)+arrow(235,350,305,375)+text(300,60,'乙：檢察官',37))
image(1136,3,paper(60,155,'起訴',1.35)+bench(310,190,.9,'判決')+text(300,90,'起訴 ≠ 判決',40)+text(150,500,'檢察官',34)+text(430,500,'法官',34))
image(1136,4,building(30,90,.74,'少年法庭')+building(345,290,.68,'檢察署')+arrow(245,230,392,330)+paper(90,345,'卷宗',.65)+text(300,63,'B：少年法庭 → 檢察官',31)+text(230,561,'裁定移送後，偵查及起訴',29))

# Voting eligibility: two physical ballot papers, age line and residence graph.
image(1153,1,ballot(75,130,'罷免',1.2)+ballot(345,130,'公投',1.2)+text(300,65,'同一天，不同資格規定',35))
age='<path d="M65 290H545" stroke="#476f82" stroke-width="8"/>'
for ageval,x in [(14,85),(18,245),(20,325),(24,485)]:age+=f'<path d="M{x} 275V305" stroke="#476f82" stroke-width="5"/>'+text(x,345,str(ageval),35)
age+=arrow(245,234,535,234)+arrow(325,405,535,405)+text(355,194,'公投：18歲起',35)+text(405,459,'公職選罷：20歲起',30)
image(1153,2,text(300,70,'比較兩個年齡門檻',35)+age)
res=taiwan((121.46,25.01),'新北')+text(300,61,'搬家與國內居住不同',33)
res+=text(300,541,'選區居住／國內居住須分開',28)
image(1153,3,res)
image(1153,4,ballot(90,165,'罷免',1.05)+paper(345,165,'公投',1.05)+text(170,430,'監護不排除',31)+text(420,430,'須未受監護',31)+text(300,80,'原卷A；共同閱讀待補',34)+text(300,535,'其他投票資格仍須符合',29))

# Central versus local and district representation versus party lists.
image(1154,1,building(25,145,.83,'立法院')+chamber(320,210,.75,'市議會')+text(160,480,'中央',40)+text(450,480,'地方',40)+text(300,64,'先辨中央民意代表',34))
district='<path d="M75 160L212 115L315 197L265 360L82 337Z" fill="#d4e6c8" stroke="#5c8269" stroke-width="5"/><path d="M212 115L315 197L265 360L395 405L528 267L450 122Z" fill="#e5dab9" stroke="#9e8b63" stroke-width="4"/>'
image(1154,2,district+box(100,215,'選區票',.68)+arrow(280,325,390,430)+text(300,70,'區域立委與原選舉區',33)+text(420,490,'依法罷免',32))
image(1154,3,ballot(60,115,'政黨票',1.1)+arrow(225,260,330,260)+paper(365,110,'名單',1.05)+chamber(315,355,.72,'席次')+text(300,64,'名單立委不適用罷免',33))
image(1154,4,building(150,90,.95,'立法院')+box(65,365,'原選區',.72)+paper(380,365,'罷免',.75)+text(300,61,'中央 ＋ 可依法罷免',35)+text(300,558,'原卷A；共同閱讀仍待補',30))

# Pingtung is a county-administered city; images show location and two chambers.
image(1155,1,taiwan((120.487,22.676),'屏東市')+text(300,61,'屏東縣內的縣轄市',35)+text(300,561,'位置點不是縣市邊界',28))
image(1155,2,building(95,140,1.25,'縣議會')+chamber(175,370,.72,'縣議員')+text(300,61,'縣：縣議員',40))
image(1155,3,chamber(70,170,1.45,'市民代表會')+paper(55,410,'議案',.65)+text(300,65,'縣轄市：市民代表',35)+text(300,553,'不同於市公所行政機關',29))
image(1155,4,building(32,110,.82,'縣議會')+chamber(300,285,.88,'市民代表會')+arrow(213,329,357,350)+text(300,62,'D：縣議員 ＋ 市民代表',32)+text(155,465,'縣層級',33)+text(440,550,'縣轄市層級',30))

# Three local ballots; the final chart counts checks from the actual table.
image(1156,1,taiwan((120.2,23.12),'臺南西港')+text(300,60,'直轄市內的一般區',35))
image(1156,2,ballot(25,165,'市長',1)+ballot(225,165,'市議員',1)+ballot(425,165,'里長',1)+text(300,73,'地方選舉：三種公職',35))
image(1156,3,building(30,120,.78,'市政府')+building(340,300,.72,'一般區公所')+paper(285,165,'任用',.7)+arrow(230,260,388,340)+text(300,63,'一般區長依法任用',36)+text(300,560,'西港不是山地原住民自治區',27))
bars=text(300,60,'比較原表的票種',36)
for j,(label,number,col) in enumerate([('甲',3,'#a5a89b'),('乙',5,'#c69e80'),('丙',3,'#a5a89b'),('丁',3,'#3e997e')]):
 x=60+j*137;h=number*55;bars+=f'<rect x="{x}" y="{430-h}" width="84" height="{h}" rx="8" fill="{col}"/>'+text(x+42,470,label,35)+text(x+42,415-h,str(number),34)
bars+=text(300,535,'丁：三項都是西港可領票種',28)
image(1156,4,bars)

# Africa: actual geometry, qualitative water bands and two landscape scenes.
af,xy,paths=mapbase((-20,-36,53,38),lambda f:f['properties']['CONTINENT']=='Africa',borders=False)
latlines=''
for lat,label in [(23.5,'23.5°N'),(0,'赤道'),(-23.5,'23.5°S')]:
 x,y=xy(-20,lat);xx,_=xy(53,lat);latlines+=f'<path d="M{x} {y}H{xx}" stroke="#477b8a" stroke-width="2" stroke-dasharray="6 7"/>'+text(105,y-8,label,25)
image(1151,1,af+latlines+text(300,58,'先看非洲整體分布',35))
wet=af
for lon,lat,col,label in [(14,23,'#c89a56','較乾'),(22,0,'#4d9873','較濕')]:
 x,y=xy(lon,lat);wet+=f'<circle cx="{x}" cy="{y}" r="31" fill="{col}" stroke="white" stroke-width="3"/>'+text(x+67,y+12,label,31)
wet+=text(300,57,'雨量差異：水分限制',35)+text(300,556,'概略定位，非精確氣候界線',27)
image(1151,2,wet)
scenes='<path d="M20 320Q125 265 280 320V510H20Z" fill="#d6bc84"/><path d="M320 320Q450 260 580 320V510H320Z" fill="#83aa79"/><circle cx="110" cy="150" r="45" fill="#efc765"/>'
for x in [355,430,505]:scenes+=f'<path d="M{x} 180q-30 35 0 45q30-10 0-45" fill="#599bbd"/>'
# Livestock silhouettes and cultivated plants, not a label-only comparison.
for x in [80,165]:scenes+=f'<path d="M{x} 350q30-35 60 0v38h-60z" fill="#8c7657"/><circle cx="{x+66}" cy="343" r="14" fill="#8c7657"/><path d="M{x+12} 380v45M{x+45} 380v45" stroke="#735e44" stroke-width="8"/>'
for x in [350,400,450,500,550]:scenes+=f'<path d="M{x} 447v-90m0 30q-35-45-30-25m30 48q35-45 30-25" stroke="#3d7952" stroke-width="7" fill="none"/>'
image(1151,3,scenes+text(150,550,'乾燥：放牧',29)+text(450,550,'較濕：耕作',29)+text(300,63,'因水分選擇生產方式',35))
plants='<path d="M80 415Q250 365 520 415V520H80Z" fill="#a6b98a"/>'
for x in [170,290,410]:plants+=f'<path d="M{x} 440V300m0 55q-70-85-50-42m50 80q70-85 50-42" stroke="#3d7c55" stroke-width="12" fill="none"/>'
for x in [170,290,410]:plants+=f'<path d="M{x} 150q-55 75 0 92q55-17 0-92" fill="#5f9fbc"/>'
image(1151,4,plants+text(300,66,'B：雨量多寡',44)+text(300,570,'不是降雨形成類型，也非虛構數據',25))

# West Asia: four differently framed geographic reasoning pictures.
NAMES={'Iraq':('乙',44,33), 'Iran':('甲',54,32), 'Turkey':('丙',35,39),'Saudi Arabia':('丁',45,24)}
def middle(bounds,highlight=None):
 b,xy,_=mapbase(bounds,None)
 for f in DATA:
  if f['properties']['ADMIN'] not in NAMES:continue
  if highlight and f['properties']['ADMIN']==highlight:
   g=f['geometry'];polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
   for poly in polys:b+='<path d="M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in [xy(*p[:2]) for p in poly[0]])+'Z" fill="#97c5b2" stroke="#3c7c69" stroke-width="3"/>'
 for name,(letter,lon,lat) in NAMES.items():
  if bounds[0]<lon<bounds[2] and bounds[1]<lat<bounds[3]:x,y=xy(lon,lat);b+=text(x,y,letter,40)
 return b,xy
b,xy=middle((24,14,65,45),'Iraq')
for pts in [[(39,39),(40,37),(42,35),(44,33),(47,30)],[(38,39),(36,36),(39,35),(42,33),(47,30)]]:
 b+='<path d="M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in [xy(*p) for p in pts])+'" stroke="#4b94bc" stroke-width="4" fill="none"/>'
image(1152,1,b+text(300,57,'X：乙伊拉克與兩河',35)+text(300,570,'河道概略示意，不表占領區',26))
b,xy=middle((37,28,50,39),'Iraq');x,y=xy(43.2,36)
b+=f'<circle cx="{x}" cy="{y}" r="12" fill="#bf7d45"/><path d="M75 120q-30 45 0 56q30-11 0-56" fill="#3a4850"/>'+arrow(92,160,x-8,y)+text(300,61,'題文的北部石油線索',34)+text(300,566,'不是油田或勢力範圍實測圖',26)
image(1152,2,b)
b,xy=middle((18,28,56,46),'Turkey');x,y=xy(44,34);xx,yy=xy(34,39);ex,ey=xy(23,42)
b+=arrow(x,y,xx,yy)+arrow(xx,yy,ex,ey)+text(300,57,'Y：丙土耳其，赴歐方向',32)+text(300,570,'僅方向示意，非精確逃難路線',26)
image(1152,3,b)
b,xy=middle((24,14,65,45));b+=text(300,57,'B：X乙 → Y丙',39)+text(300,562,'伊拉克 → 土耳其',35)
image(1152,4,b)

provenance={'dataset':'Natural Earth 50m admin0 countries','url':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson','sha256':hashlib.sha256((R/'.cache/q1058-natural-earth-50m.geojson').read_bytes()).hexdigest(),'license':'Public domain; https://www.naturalearthdata.com/about/terms-of-use/','projection':'regional equirectangular, equal scale longitude/latitude for schematic location; no measured routes or rainfall values','authoredImages':28,'sourceAIArtUsed':False}
(Path(__file__).parent/'native-art-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print('28 new native SVG maps/role illustrations/ballot and age diagrams')
