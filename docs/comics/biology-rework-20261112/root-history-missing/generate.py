from pathlib import Path
import json,math,hashlib,sys
R=Path(__file__).resolve().parents[4];D=Path(__file__).parent;A=R/'docs/comics/art';A.mkdir(exist_ok=True)
sys.path.insert(0,str(D.parent/'root-geography'))
from svg_geometry import compact_ring
geo=R/'.cache/four-image-maps/ne_10m_admin_0_countries.geojson'
f=next(f for f in json.loads(geo.read_text())['features'] if f['properties']['ADMIN']=='Taiwan')
polys=f['geometry']['coordinates'];ring=max((p[0] for p in polys),key=len)
ink='#193f49';gold='#bd7747';teal='#2d7a7c';cream='#faf3dd';red='#b3463d'
def text(x,y,s,size=43,fill=ink,anchor='middle'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{s}</text>'
def path(d,stroke=ink,fill='none',sw=7,extra=''):
 return f'<path d="{d}" stroke="{stroke}" fill="{fill}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'
def line(x,y,xx,yy,c=ink,sw=6):return f'<path d="M{x} {y}L{xx} {yy}" stroke="{c}" stroke-width="{sw}" fill="none"/>'
def dot(x,y,c=red,r=11):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="#fff" stroke-width="4"/>'
def arrow(x,y,xx,yy,c=gold):
 a=math.atan2(yy-y,xx-x);u=xx-21*math.cos(a)+13*math.sin(a);v=yy-21*math.sin(a)-13*math.cos(a);uu=xx-21*math.cos(a)-13*math.sin(a);vv=yy-21*math.sin(a)+13*math.cos(a)
 return line(x,y,xx,yy,c,9)+path(f'M{u} {v}L{xx} {yy}L{uu} {vv}',c,sw=8)
def book(x,y,w=350,h=215,labels=None):
 s=f'<ellipse cx="{x+w/2}" cy="{y+h+16}" rx="{w*.54}" ry="17" fill="#d6cfb6"/>'
 s+=path(f'M{x} {y+12}Q{x+w*.22} {y-25} {x+w/2} {y+15}Q{x+w*.76} {y-25} {x+w} {y+12}L{x+w} {y+h}Q{x+w*.75} {y+h-35} {x+w/2} {y+h+5}Q{x+w*.24} {y+h-35} {x} {y+h}Z',ink,'#ead3a0',6)
 s+=path(f'M{x+12} {y+3}Q{x+w*.22} {y-34} {x+w/2} {y+8}Q{x+w*.76} {y-34} {x+w-12} {y+3}L{x+w-12} {y+h-16}Q{x+w*.75} {y+h-48} {x+w/2} {y+h-8}Q{x+w*.24} {y+h-48} {x+12} {y+h-16}Z',ink,'#fffaf0',4)
 s+=path(f'M{x+w/2} {y+8}L{x+w/2} {y+h-8}',gold,sw=5)
 for side in [0,1]:
  for k in range(4):s+=line(x+30+side*w/2,y+52+k*30,x+w/2-30+side*w/2,y+52+k*30,'#c8c0a7',3)
 if labels:
  s+=text(x+w*.25,y+h*.57,labels[0],36)+text(x+w*.75,y+h*.57,labels[1],36)
 return s
def closedbook(x,y,w=150,h=180,colour=teal,label=''):
 s=path(f'M{x} {y}L{x+w} {y}L{x+w} {y+h}L{x} {y+h}Q{x-12} {y+h/2} {x} {y}Z',ink,colour,5)
 s+=line(x+20,y+5,x+20,y+h-5,'#eadcb8',4)
 s+=path(f'M{x+25} {y+h-14}L{x+w-7} {y+h-14}', '#e4dbbc',sw=6)
 if label:s+=text(x+w*.58,y+h*.5,label,38,'#fff8e9')
 return s
def seal(x,y):
 return path(f'M{x-30} {y+15}L{x+30} {y+15}L{x+25} {y+40}L{x-25} {y+40}Z',ink,gold,5)+path(f'M{x-16} {y+15}L{x-13} {y-17}Q{x} {y-35} {x+13} {y-17}L{x+16} {y+15}',ink,'#a45846',5)
def brush(x,y):
 return path(f'M{x} {y}L{x+16} {y+4}L{x-35} {y+165}L{x-51} {y+161}Z',ink,'#987049',4)+path(f'M{x-51} {y+161}Q{x-56} {y+205} {x-35} {y+165}Z',ink,'#303d41',3)
def building(x,y,w=210,h=160):
 s=path(f'M{x+22} {y+54}L{x+w-22} {y+54}L{x+w-22} {y+h}L{x+22} {y+h}Z',ink,'#e4b77d',5)
 s+=path(f'M{x-5} {y+60}Q{x+w*.2} {y+42} {x+w*.5} {y}Q{x+w*.8} {y+42} {x+w+5} {y+60}Z',ink,'#576e72',5)
 s+=path(f'M{x+85} {y+h}L{x+85} {y+92}Q{x+w*.5} {y+72} {x+w-85} {y+92}L{x+w-85} {y+h}',ink,'#805341',4)
 for u in [x+45,x+w-60]:s+=f'<rect x="{u}" y="{y+86}" width="25" height="32" fill="#4f7479" stroke="{ink}" stroke-width="4"/>'
 return s+line(x-4,y+h+4,x+w+4,y+h+4,ink,7)
def calendar(x,y,w,h,year):
 s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#fffaf0" stroke="{ink}" stroke-width="6"/><path d="M{x} {y+40}H{x+w}" stroke="{gold}" stroke-width="20"/>'
 for xx in [x+w*.25,x+w*.75]:s+=path(f'M{xx} {y-10}V{y+18}',ink,sw=8)
 return s+text(x+w/2,y+h*.66,year,56)
def twmap(box=(130,100,400,450),dots=[]):
 x,y,w,h=box;lon0,lon1=119.9,122.1;lat0,lat1=21.8,25.4;cx=math.cos(math.radians(23.6));scale=min(w/((lon1-lon0)*cx),h/(lat1-lat0));ox=x+(w-(lon1-lon0)*cx*scale)/2;oy=y+(h-(lat1-lat0)*scale)/2
 def project(lon,lat):return (ox+(lon-lon0)*cx*scale,oy+(lat1-lat)*scale)
 p=compact_ring([project(*a[:2]) for a in ring],(x,y,x+w,y+h),.25)
 s=path('M'+'L'.join(f'{u:.1f} {v:.1f}' for u,v in p)+'Z',teal,'#bdd0b8',5)
 for lon,lat,label,dx,dy in dots:
  u,v=project(lon,lat);s+=dot(u,v)+line(u,v,u+dx,v+dy,red,3)+text(u+dx,v+dy-8,label,41,ink,'start' if dx>0 else 'end')
 # north arrow
 s+=line(x+w-15,y+70,x+w-15,y+20,ink,5)+path(f'M{x+w-26} {y+35}L{x+w-15} {y+17}L{x+w-4} {y+35}',ink,sw=5)+text(x+w-15,y+9,'北',28)
 return s,project

def save(q,n,title,body,note='新製教學示意'):
 p=A/f'{q}-four-image-v2-panel-{n}.svg';p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" role="img" aria-label="{title}"><defs><linearGradient id="paper" x2="1" y2="1"><stop stop-color="#fffdf3"/><stop offset="1" stop-color="#efe5cc"/></linearGradient></defs><rect width="640" height="640" rx="20" fill="url(#paper)"/><g font-family="Noto Sans CJK TC, Noto Sans TC, sans-serif">'+text(320,59,title,47)+body+text(320,611,note,28)+'</g></svg>')
# 608: actual illustrated archival objects and a geographically grounded chronological locator.
save('q-608',1,'先辨清代統治分類',book(84,230,440,255)+brush(559,187)+seal(91,475)+text(320,137,'內附、輸餉',47)+text(320,193,'由賦稅線索判時代',39), '新製文書聯想，非原始檔案')
m,_=twmap((60,123,310,420))
save('q-608',2,'接續清代：日治',m+closedbook(398,170,165,176,teal,'清代')+closedbook(398,389,165,176,gold,'日治')+arrow(480,355,480,375)+text(205,564,'臺灣定位',38),'今海岸定位，非歷史疆界')
save('q-608',3,'1935：戶籍欄更名',calendar(56,129,236,180,'1935')+book(107,370,430,184)+seal(553,478)+text(454,179,'高砂族',47,red)+text(454,239,'戶籍用語',35)+line(304,270,422,345,gold,7),'新製示意，非仿真戶籍證件')
m,pr=twmap((65,135,305,420))
save('q-608',4,'答案 C：高砂族',m+book(329,244,255,208)+text(455,173,'日治時期',42)+text(457,505,'高砂族',48,red)+text(320,566,'歷史舊稱 ≠ 今日身分',35),'圖解不表示族群分布或文化高低')
# 612: locate cities, locate centre, separate years, integrate start vs continuity.
m,_=twmap((120,112,380,440),[(120.21,23.0,'臺南',-48,25),(120.435,24.056,'鹿港',-62,-9),(121.5,25.036,'艋舺',80,90)])
save('q-612',1,'一府、二鹿、三艋舺',m+text(320,565,'俗諺中的三個市鎮',39),'今海岸定位，非今日城市排名')
m,pr=twmap((49,127,308,410));u,v=pr(120.21,23.0)
save('q-612',2,'鄭氏：臺南統治中心',m+dot(u,v)+line(u,v,410,283,gold,6)+building(367,164,218,172)+text(477,401,'承天府',45,red)+text(476,461,'今臺南',38),'建築是通用示意，非遺址復原')
save('q-612',3,'1661 與 1662 分開',calendar(51,140,224,154,'1661')+calendar(355,140,224,154,'1662')+arrow(287,217,333,217)+building(73,371,200,145)+closedbook(390,358,152,157,teal)+text(164,340,'來臺進攻',38)+text(464,340,'荷蘭投降',38)+text(320,565,'事件分年，不混成同時',38),'新製年代圖，不是戰役或投降實錄')
m,pr=twmap((62,129,313,417));u,v=pr(120.21,23.0)
save('q-612',4,'答案 B：鄭氏時期',m+dot(u,v)+f'<circle cx="{u}" cy="{v}" r="26" stroke="{red}" stroke-width="5" fill="none"/>'+building(386,193,183,146)+text(480,395,'臺南',45)+text(480,460,'首府起點',38)+text(320,563,'清代延續 ≠ 最早開始',37),'今海岸只定位，不表示鄭氏統治範圍')
prov={'generator':str(D.relative_to(R)/'generate.py'),'generatedQuestions':['q-608','q-612'],'artCount':8,'method':'eight independent native SVG geographical/archival teaching diagrams','baseMap':{'file':str(geo.relative_to(R)),'sha256':hashlib.sha256(geo.read_bytes()).hexdigest(),'pinnedCommit':'f1890d9f152c896d250a77557a5751a93d494776','license':'Public domain','terms':'https://www.naturalearthdata.com/about/terms-of-use/'},'mapsAre':'Modern outline locator only, not historical jurisdiction, settlements completeness or ethnicity distribution','coordinates':{'Tainan':[120.21,23.0],'Lukang':[120.435,24.056],'Wanhua':[121.5,25.036]},'illustrationsAre':'Generic newly authored archival-book, seal, calendar and government-building diagrams, not archive reproduction or identity documents','sources':[{'url':'https://historic.tainan.gov.tw/index.php?belongid=45&id=89&index=1&lang=cht&option=module&task=pageinfo','support':'Read official chronology:1661 expedition and1662 Dutch surrender; not used to override differing summaries of administrative establishment year.'},{'url':'https://art.archives.gov.tw/tw/art/2092.html','support':'Read main text: Qing tax-based political categories, Japanese usage retained older names initially; 1935 legal household registration change to 高砂族. Do not claim first coining in1935.'},{'url':'https://thcts.sinica.edu.tw/themes/rb02.php','support':'Read whole article: 1661 administrative seat 承天府 in current Tainan area; administrative continuity into Qing. Do not infer all modern Taiwan under actual control.'}]}
(D/'provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
print('Created8SVG')
