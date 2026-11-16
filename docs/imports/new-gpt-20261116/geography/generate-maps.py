"""24 distinct teaching maps from pinned Natural Earth coastlines, not exam replacements."""
from map_helper import *
OUT=R/'docs/comics/art'
arts={}
def highlight(a,path,names,color=GOLD):
 for f in world:
  if f['properties']['ADMIN'] in names:
   a+='<g clip-path="url(#map)">'+''.join(path(p,color,INK,1.5) for p in polygons(f['geometry']))+'</g>'
 return a
def dotlabel(a,xy,ll,t,off=(0,-18),size=35,c=RED):
 x,y=xy(*ll);return a+point(x,y,c,7)+label(x+off[0],y+off[1],t,size,c)
def route(xy,coords,c=RED,dash=False):
 pts=[xy(*p) for p in coords];return '<polyline points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'" fill="none" stroke="'+c+'" stroke-width="6" stroke-linejoin="round" '+('stroke-dasharray="12 9"' if dash else '')+'/>'
def footer(a,t):return a+label(320,604,t,27)
# 1122: possible routes remain conditional; no route is claimed unique or to scale.
a,xy,path=mapper((-90,-58,145,65));a=highlight(a,path,['Brazil','China']);a=dotlabel(a,xy,(-50,-10),'巴西',(0,45));a=dotlabel(a,xy,(105,35),'中國',(0,-25));arts[1122]=[footer(a,'原題未指定船型或通道')]
a,xy,path=mapper((-60,-58,140,40));a+=route(xy,[(-43,-23),(-25,-35),(5,-42),(25,-40),(65,-33),(100,-25),(110,-8),(113,8),(120,24)]);a=dotlabel(a,xy,(18.5,-34.4),'好望角',(5,-24),31);a+=label(370,280,'印度洋',43,c=TEAL);arts[1122].append(footer(a,'可行方向示意，非航跡資料'))
a,xy,path=mapper((-106,-5,-60,31));a=dotlabel(a,xy,(-79.7,9.1),'巴拿馬運河',(0,-30),34);a+=label(155,395,'太平洋',40,c=TEAL)+label(480,260,'大西洋',40,c=TEAL);arts[1122].append(footer(a,'通航須核船寬、船長與吃水'))
a,xy,path=mapper((-80,-55,135,55));a+=route(xy,[(-43,-23),(-25,-35),(5,-42),(25,-40),(65,-33),(100,-25),(110,-8),(113,8),(120,24)],TEAL,True);a+=label(130,240,'大西洋',34,c=TEAL)+label(390,330,'印度洋',34,c=TEAL);arts[1122].append(footer(a,'保留原卷B；航路答案待核'))
# 1124: exact border geography and latitude; circle denotes region, not a park boundary.
a,xy,path=mapper((-170,-58,-28,78));a=highlight(a,path,['Panama','Colombia']);x,y=xy(-77.7,8);a+=ring(x,y,22)+link(x,y,425,300)+label(435,280,'達連缺口',39);arts[1124]=[footer(a,'泛美公路系統在此不連續')]
a,xy,path=mapper((-85,3,-72,12));a=highlight(a,path,['Panama'],GOLD);a=highlight(a,path,['Colombia'],'#a4c1a0');a+=label(225,220,'巴拿馬',41)+label(415,440,'哥倫比亞',38);x,y=xy(-77.7,8);a+=ring(x,y,34)+label(320,550,'國境附近缺口',33);arts[1124].append(a)
a,xy,path=mapper((-100,-10,-54,30));p=xy(-100,8);s=xy(-54,8);a+=link(*p,*s,RED)+label(490,p[1]-20,'約8°N',36);p=xy(-100,0);s=xy(-54,0);a+=link(*p,*s,TEAL)+label(480,p[1]+40,'赤道',34);arts[1124].append(footer(a,'低緯度，非極地文化環境'))
a,xy,path=mapper((-82,5,-75,11));a=highlight(a,path,['Panama','Colombia'],'#8eaf83');x,y=xy(-77.7,8);a+=ring(x,y,52)+label(230,180,'熱帶保育區',40)+label(360,530,'缺口區域',37);arts[1124].append(footer(a,'區位圈示，非保育區精確邊界'))
# 1129: continental labels and forced movement, not port/quantity reconstructions.
a,xy,path=mapper((-180,-60,180,80));
for ll,t in [((-105,43),'甲'),((-62,-15),'乙'),((18,8),'丙'),((80,45),'丁')]:
 x,y=xy(*ll);a+=label(x,y,t,54,RED)
arts[1129]=[footer(a,'依原圖洲別判讀')]
a,xy,path=mapper((-22,-38,55,39));a=highlight(a,path,[f['properties']['ADMIN'] for f in world if f['properties'].get('CONTINENT')=='Africa']);a+=label(320,320,'丙：非洲',51);arts[1129].append(footer(a,'不是把丁歐亞大陸誤作非洲'))
a,xy,path=mapper((-110,-45,35,55));a+=route(xy,[(-10,8),(-25,16),(-45,20),(-65,15)],RED);x,y=xy(-65,15);a+=f'<path d="M{x+20} {y-13}L{x} {y}L{x+22} {y+12}" fill="none" stroke="{RED}" stroke-width="7"/>';a+=label(210,410,'美洲',43)+label(505,310,'非洲',42);arts[1129].append(footer(a,'強迫運送方向，不是自由移工'))
a,xy,path=mapper((-105,-55,45,55));a=highlight(a,path,[f['properties']['ADMIN'] for f in world if f['properties'].get('CONTINENT')=='Africa']);a+=route(xy,[(-10,8),(-30,15),(-55,10)],RED,True);a+=label(440,300,'丙',60,RED)+label(185,460,'大西洋',43,TEAL);arts[1129].append(footer(a,'C非洲；不補原文人口統計範圍'))
# 1130: conventional triangle, with no official bounded hazard-zone claim.
tri=[(-80.19,25.76),(-64.75,32.3),(-66.1,18.47),(-80.19,25.76)]
a,xy,path=mapper((-120,0,-40,60));a+=label(420,300,'北大西洋',43,c=TEAL);a+=route(xy,tri,RED);arts[1130]=[footer(a,'北美洲東側海域')]
a,xy,path=mapper((-88,12,-58,37));a+=route(xy,tri,RED)
for ll,t,off in [(tri[0],'邁阿密',(-5,50)),(tri[1],'百慕達',(-35,-26)),(tri[2],'聖胡安',(0,45))]:a=dotlabel(a,xy,ll,t,off,34)
arts[1130].append(footer(a,'俗稱三角區，沒有官方界線'))
a,xy,path=mapper((-112,12,-52,68));a+=label(245,380,'墨西哥灣',37,TEAL)+label(320,180,'哈得孫灣',36,TEAL)+label(475,390,'大西洋',39,TEAL);a+=route(xy,tri,RED);arts[1130].append(footer(a,'佛羅里達兩側海域不同'))
a,xy,path=mapper((-96,8,-52,43));a+=route(xy,tri,RED);a+=label(405,300,'B大西洋',45,TEAL);arts[1130].append(footer(a,'非河口三角洲；傳說不當事實'))
# 1131: state polygon, surrounding lakes/country, north/south comparisons.
MN=next(f for f in states if f['properties'].get('name')=='Minnesota')
def mn(a,path):return a+'<g clip-path="url(#map)">'+''.join(path(p,TEAL,INK,2) for p in polygons(MN['geometry']))+'</g>'
a,xy,path=mapper((-126,23,-66,51));a=mn(a,path);a=dotlabel(a,xy,(-94.5,46),'明尼蘇達',(20,-34),35);arts[1131]=[footer(a,'美國北部；原印20州另訂正50州')]
a,xy,path=mapper((-101,38,-73,52));a=mn(a,path);a+=label(220,180,'明尼蘇達',37)+label(420,400,'五大湖區',39,TEAL);arts[1131].append(footer(a,'位於五大湖地區西側'))
a,xy,path=mapper((-126,24,-66,51));a=mn(a,path);a+=label(400,180,'北部較冷涼',37,TEAL)+label(420,490,'南部較暖熱',37,RED);arts[1131].append(footer(a,'比較位置，不畫虛構農業帶界線'))
a,xy,path=mapper((-105,39,-80,51));a=mn(a,path);a+=label(270,260,'酪農帶',44,TEAL)+label(410,430,'湖區周邊',37);arts[1131].append(footer(a,'A：代表性分區，非全州僅乳業'))
# 1132: no fabricated density dots; actual city coordinates and qualitative region.
can=['Canada']
a,xy,path=mapper((-145,40,-50,83));a=highlight(a,path,can);a+=label(320,235,'加拿大',49);arts[1132]=[footer(a,'先分南北，再辨東西')]
a,xy,path=mapper((-145,39,-50,80));a=highlight(a,path,can);p=xy(-140,50);s=xy(-55,50);a+=route(xy,[(-140,50),(-55,50)],RED,True)+label(320,p[1]-25,'南部鄰近美國',40);arts[1132].append(footer(a,'相對溫暖；非以此線作人口界線'))
a,xy,path=mapper((-94,40,-58,54));
for ll,t,off in [((-79.383,43.653),'多倫多',(-40,55)),((-73.567,45.502),'蒙特婁',(45,-25)),((-71.208,46.814),'魁北克市',(40,-60))]:a=dotlabel(a,xy,ll,t,off,34)
a+=label(320,515,'五大湖—聖羅倫斯河',34,TEAL);arts[1132].append(footer(a,'城市點只表位置，非人口點子數'))
a,xy,path=mapper((-140,40,-50,73));a=highlight(a,path,can);x,y=xy(-77,46);a+=ring(x,y,55)+label(x,y-70,'東南部',43,RED);a=dotlabel(a,xy,(-123.12,49.28),'溫哥華',(-5,-30),32);arts[1132].append(footer(a,'D東南部；不否定西南部也有城市'))
for q,aa in arts.items():
 assert len(aa)==4
 for i,a in enumerate(aa,1):(OUT/f'q-{q}-panel-{i}.svg').write_text(svg(a))
prov={'dataset':'Natural Earth pinned author repository','commit':PIN,'license':'public domain','licenseURL':'https://www.naturalearthdata.com/about/terms-of-use/','projection':'regional equirectangular with cosine correction; routes/circles qualitative teaching only','sourceFiles':[{'path':str(C/(f+'.geojson')),'sha256':hashlib.sha256((C/(f+'.geojson')).read_bytes()).hexdigest()} for f in FILES],'outputHashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for q in arts for p in sorted(OUT.glob(f'q-{q}-panel-*.svg'))}}
(Path(__file__).parent/'map-data-provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
print('Created',sum(map(len,arts.values())),'distinct teaching maps')
