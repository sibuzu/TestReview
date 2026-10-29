import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
from fractions import Fraction as F
M={'A':(F(9),F(12)),'B':(F(0),F(0)),'C':(F(14),F(0)),'P':(F(8),F(4)),'D':(F(3),F(4)),'E':(F(37,3),F(4))}
def xy(n,o=0):x,y=M[n];return o+20+float(x)*11,168-float(y)*11
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def line(a,b,o,c='#71857d',w=1.7,dash=''):
 x,y=xy(a,o);X,Y=xy(b,o);s.append(f'<path d="M{x} {y}L{X} {Y}" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def poly(ns,o,c):s.append('<polygon points="'+' '.join(f'{xy(n,o)[0]},{xy(n,o)[1]}' for n in ns)+f'" fill="{c}"/>')
def arc(v,a,b,o,rad,c):
 x,y=xy(v,o);X,Y=xy(a,o);U,V=xy(b,o);aa=math.atan2(Y-y,X-x);bb=math.atan2(V-y,U-x);delta=(bb-aa+math.pi)%(2*math.pi)-math.pi
 pts=[(x+rad*math.cos(aa+delta*i/20),y+rad*math.sin(aa+delta*i/20)) for i in range(21)]
 s.append('<polyline points="'+' '.join(f'{p:.3f},{q:.3f}' for p,q in pts)+f'" stroke="{c}" stroke-width="1.5" fill="none"/>')
for i in range(3):
 o=i*200;s.append(f'<rect x="{o+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
 if i==0:poly(['B','D','P'],o,'#dcebdc')
 elif i==1:poly(['C','E','P'],o,'#f0e1c8')
 else:poly(['A','D','E'],o,'#e3edf3')
 for a,b in [('A','B'),('B','C'),('C','A'),('B','P'),('C','P'),('D','E')]:line(a,b,o)
 if i==0:
  for a,b in [('B','D'),('D','P')]:line(a,b,o,'#3a8760',3.5)
  arc('B','A','P',o,16,'#3a8760');arc('B','P','C',o,22,'#3a8760');arc('P','B','D',o,16,'#3a8760')
 elif i==1:
  for a,b in [('C','E'),('E','P')]:line(a,b,o,'#b57e3a',3.5)
  arc('C','B','P',o,18,'#b57e3a');arc('C','P','A',o,24,'#b57e3a');arc('P','E','C',o,16,'#b57e3a')
 else:
  for a,b in [('A','D'),('A','E')]:line(a,b,o,'#57819b',3)
  for a,b,c in [('D','P','#3a8760'),('B','D','#3a8760'),('P','E','#b57e3a'),('C','E','#b57e3a')]:line(a,b,o,c,3)
 for n,dx,dy in [('A',0,-11),('B',-10,10),('C',10,10),('D',-11,-3),('E',11,-3),('P',0,13)]:
  x,y=xy(n,o);t(x+dx,y+dy,n,14)
 if i==0:t(o+63,24,'BD = DP',16,c='#397f5a')
 elif i==1:t(o+63,24,'CE = EP',16,c='#a76f31')
 else:t(o+63,24,'周長重組',16)
 if i<2:t(o+100,190,'DE ∥ BC',14)
 else:t(o+100,190,'拼回 AB＋AC',16)
s.append('</svg>');Path('docs/comics/art/q-205.svg').write_text(''.join(s))
def dist(a,b):return math.dist(tuple(map(float,M[a])),tuple(map(float,M[b])))
def angle(a,v,b):
 u=[float(M[a][i]-M[v][i]) for i in [0,1]];w=[float(M[b][i]-M[v][i]) for i in [0,1]];return math.degrees(math.acos(sum(u[i]*w[i] for i in [0,1])/(math.hypot(*u)*math.hypot(*w))))
assert all(abs(dist(a,b)-val)<1e-9 for a,b,val in [('A','B',15),('B','C',14),('A','C',13),('B','D',5),('D','P',5),('C','E',13/3),('E','P',13/3)])
assert abs(angle('A','B','P')-angle('P','B','C'))<1e-8
assert abs(angle('B','C','P')-angle('P','C','A'))<1e-8
small=sum(dist(a,b) for a,b in [('A','D'),('D','E'),('E','A')]);big=42;assert abs(small-28)<1e-9
val={'id':'q-205','mathematicalCoordinates':{k:list(map(str,v)) for k,v in M.items()},'svgTransform':'x=panelOffset+20+11*x; y=168-11*y','AB':dist('A','B'),'BC':dist('B','C'),'AC':dist('A','C'),'DPEonY':4,'BhalfAngles':[angle('A','B','P'),angle('P','B','C')],'BPD':angle('B','P','D'),'ChalfAngles':[angle('B','C','P'),angle('P','C','A')],'CPE':angle('C','P','E'),'BD_equals_DP':5,'CE_equals_EP':'13/3','AD':10,'AE':'26/3','DE':'28/3','largePerimeter':big,'smallPerimeter':small,'difference':big-small,'independentSubstitutionPassed':True}
Path('docs/comics/q-205-geometry-validation.json').write_text(json.dumps(val,ensure_ascii=False,indent=2)+'\n')
x={'id':'q-205','subject':'Math','title':'兩個等腰關係，把小周長拼回AB＋AC','art':'docs/comics/art/q-205.svg','protectedWords':['BD＝DP','CE＝EP','DE＝DP＋PE','AB＋AC','AD＋BD','AE＋CE','△BDP','△CEP','△ADE','角平分線','內錯角','周長差'],'panels':[{'heading':'① B角平分線加平行，得到BD＝DP','text':'BP平分B角，∠DBP＝∠PBC。又DP平行BC，∠BPD＝∠PBC，所以△BDP有兩個相等的角，是等腰三角形，得到BD＝DP。','alt':'依AB15、BC14、AC13精確座標作圖，△BDP淡綠、BD與DP同綠，B的兩半角與P處相等內錯角用綠弧標出。'},{'heading':'② C角也同樣處理，得到CE＝EP','text':'CP平分C角，配合EP平行BC，可得∠ECP＝∠CPE。△CEP為等腰三角形，所以CE＝EP；左右兩側的短邊，都能替換成DE上的一段。','alt':'相同座標下△CEP淡橘、CE與EP同橘，C的兩半角及P處內錯角橘弧；不把兩組不同長邊畫成同長。'},{'heading':'③ 把DE拆開，再各自補回大三角形兩側','text':'P在DE上，DE＝DP＋PE＝BD＋CE。因此小周長AD＋AE＋DE，重組為AD＋BD加上AE＋CE，正好是AB＋AC，不是大周長的一半。','alt':'△ADE上方藍色，DE分成綠DP及橘PE，分別和兩側綠BD、橘CE對應；圖未把P放成DE中點，各段長度依實算。'}],'fourth':{'answer':'(1) 小周長＝AB＋AC；(2) 周長差＝14','points':['△ABC周長＝15＋14＋13＝42。','△ADE周長＝15＋13＝28。','相差42−28＝14，也就是BC。']},'rationale':'實看原卷9題完整兩問及附圖，讀來源1210–1243及1284–1318模組摘要，不假稱來源留有逐行完整證明。獨立取B(0,0)、C(14,0)、A(9,12)，角平分交點P(8,4)、D(3,4)、E(37/3,4)，驗BD=DP=5、CE=EP=13/3，兩周長42/28。新原生SVG按同尺度三格展示兩等腰/周長重組，精確弧度數據另存，答案14不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-205-source-4b4e4b2a5c.jpg','site/dist/assets/questions/q-205-given.svg (read exact supplied source geometry)','site/dist/sources/gemini-GD2msWyGjhx0.txt lines 1210–1243,1284–1318'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG 13-14-15 triangle, angle-bisector equal arcs and side-length perimeter rearrangement','answerCheckedAgainst':'內錯角配角平分線→BD=DP、CE=EP；DE=BD+CE；小周長AB+AC=28，大周長42，差14。精確座標及角度/長度獨立驗證。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-205.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
