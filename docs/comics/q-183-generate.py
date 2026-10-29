import math,json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
A=(150,26);B=(30,26+120*math.sqrt(3));C=(270,B[1]);t=.65
lerp=lambda a,b,k:(a[0]+k*(b[0]-a[0]),a[1]+k*(b[1]-a[1]))
D=lerp(B,A,t);E=lerp(B,C,t);F=lerp(C,A,1-t)
P=dict(A=A,B=B,C=C,D=D,E=E,F=F)
dist=math.dist
def angle(a,o,b):
 u=(a[0]-o[0],a[1]-o[1]);v=(b[0]-o[0],b[1]-o[1]);return math.degrees(math.acos(sum(x*y for x,y in zip(u,v))/math.hypot(*u)/math.hypot(*v)))
def poly(ps,fill,stroke='#617567',width=2):return '<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
def line(a,b,c,w=5):return f'<path d="M{a[0]:.3f} {a[1]:.3f}L{b[0]:.3f} {b[1]:.3f}" stroke="{c}" stroke-width="{w}" fill="none"/>'
def text(x,y,s,size=19,c='#2b4938'):return f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" fill="{c}" font-size="{size}" font-family="Noto Sans CJK TC,serif">{escape(s)}</text>'
def lab(n,p,dx=0,dy=0):return text(p[0]+dx,p[1]+dy,n,21)
def arc(o,a,b,c,r=22):
 a1=math.atan2(a[1]-o[1],a[0]-o[0]);a2=math.atan2(b[1]-o[1],b[0]-o[0]);da=(a2-a1+3*math.pi)%(2*math.pi)-math.pi;a2=a1+da;x1=o[0]+r*math.cos(a1);y1=o[1]+r*math.sin(a1);x2=o[0]+r*math.cos(a2);y2=o[1]+r*math.sin(a2);return f'<path d="M{x1} {y1}A{r} {r} 0 0 {int(da>0)} {x2} {y2}" stroke="{c}" stroke-width="3" fill="none"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300">']
for i in range(3):
 s.append(f'<g transform="translate({i*300},0)"><rect width="300" height="300" fill="#faf8ee"/>')
 if i<2:
  s.append(poly([A,B,C],'none'))
  s.append(poly([B,D,E],'#dfeaf4'));s.append(poly([C,E,F],'#f5e6d3'));s.append(poly([D,E,F],'#f5f5e9'))
  if i==0:
   s.extend([line(D,E,'#678eaf',4),line(A,C,'#678eaf',4),line(E,F,'#bd8c4f',4),line(A,B,'#bd8c4f',4),arc(E,B,D,'#678eaf'),arc(E,F,C,'#bd8c4f'),arc(E,D,F,'#538563',30)])
   s.append(text(E[0],E[1]-42,'60°',18,'#447854'))
  else:
   for u,v in [('B','D'),('D','E'),('B','E')]:s.append(line(P[u],P[v],'#527fa1',5))
   for u,v in [('A','D'),('E','C'),('E','F')]:s.append(line(P[u],P[v],'#b9813f',5))
  for n,dx,dy in [('A',0,-14),('B',-10,19),('C',10,19),('D',-14,-6),('E',0,24),('F',18,0)]:s.append(lab(n,P[n],dx,dy))
  s.append(text(150,281,'平行線 → 兩個正三角形' if i==0 else 'DE＝BD ＞ AD＝EF',17))
 else:
  cv=lambda q:(50+1.3*(q[0]-D[0]),50+1.3*(q[1]-D[1]))
  d,e,f=map(cv,[D,E,F]);s.append(poly([d,e,f],'#e6efdf'));s.append(line(d,e,'#527fa1',6));s.append(line(e,f,'#b9813f',6));s.extend([arc(d,e,f,'#b9813f',29),arc(f,d,e,'#527fa1',25),arc(e,d,f,'#538563',24)])
  s.extend([lab('D',d,-18,-4),lab('E',e,0,22),lab('F',f,20,0),text(d[0]+28,d[1]+32,'α',21,'#b9813f'),text(f[0]-22,f[1]+4,'β',21,'#527fa1'),text(e[0]-5,e[1]-40,'60°',18)])
  s.append(text(150,273,'α＜β，α＋β＝120°',18))
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-183.svg').write_text(''.join(s))
checks={'AB':dist(A,B),'BC':dist(B,C),'CA':dist(C,A),'BD':dist(B,D),'AD':dist(A,D),'DE':dist(D,E),'BE':dist(B,E),'EF':dist(E,F),'EC':dist(E,C),'DEF':angle(D,E,F),'EDF':angle(E,D,F),'DFE':angle(D,F,E)}
assert abs(checks['AB']-checks['BC'])<1e-9 and abs(checks['BC']-checks['CA'])<1e-9
assert checks['BD']>checks['AD'] and abs(checks['BD']-checks['DE'])<1e-9 and abs(checks['AD']-checks['EF'])<1e-9
assert abs(checks['DEF']-60)<1e-9 and checks['EDF']<60<checks['DFE']
cross=lambda u,v:u[0]*v[1]-u[1]*v[0]
vec=lambda u,v:(v[0]-u[0],v[1]-u[1])
assert abs(cross(vec(D,E),vec(A,C)))<1e-8 and abs(cross(vec(E,F),vec(A,B)))<1e-8
Path('docs/comics/q-183-geometry-validation.json').write_text(json.dumps({'id':'q-183','pass':True,'illustrativeBDfraction':t,'coordinates':P,'checks':checks,'parallelCrossProducts':[cross(vec(D,E),vec(A,C)),cross(vec(E,F),vec(A,B))],'givenOnlyAnglesShown':'Only60 shown; alpha/beta not arbitrary numeric angles','answer':'C','sourceTextAndExistingGivenFigureActuallyViewed':True},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-183','subject':'Math','title':'先比較對邊，才能判斷角度大小','art':'docs/comics/art/q-183.svg','protectedWords':['正三角形','△BDE','△CEF','△DEF','DE∥AC','EF∥AB','BD＞AD','DE＞EF','∠DEF','∠EDF','∠DFE','60°','120°','α＜β'],'panels':[{'heading':'① 平行線先找出兩個正三角形','text':'DE∥AC、EF∥AB，外框又是正三角形，因此△BDE與△CEF都是正三角形。在直線BC上，∠DEF＝180°−60°−60°＝60°。','alt':'依正確平行條件精確構圖，BDE藍色、CEF橘色，E點內角60度；不套用別題DF平行BC條件。'},{'heading':'② 用相等線段，把已知不等式搬進來','text':'△BDE給出DE＝BD＝BE；△CEF給出EF＝EC。又BC＝AB，扣掉BE＝BD，得EC＝AD。所以BD＞AD就變成DE＞EF。','alt':'藍色BD/DE/BE等長，橘色AD/EC/EF等長；藍色大於橘色，由完整正三角形的邊長關係推出。'},{'heading':'③ 同一三角形，短邊對較小角','text':'在△DEF內，EF較短，所對的∠EDF＝α較小；DE較長，所對的∠DFE＝β較大。α＋β＝120°且α＜β，所以α＜60°。','alt':'只保留精確比例的DEF三角形，長邊DE藍色對F點β，短邊EF橘色對D點α，E角60度；非特定角度數值範例。'}],'fourth':{'answer':'答案 C：∠DEF＝60°，∠EDF＜60°','points':['先由平行線得到兩個小正三角形。','把BD＞AD轉為DE＞EF。','大邊對大角，小邊對小角；不能只憑圖猜。']},'rationale':'讀完整延伸練習4與四選項，實看既有作答附圖，依DE平行AC／EF平行AB／BD大於AD獨立構圖。以精確幾何著色將邊長不等式與對角對應，保留C答；不沿用來源AI圖。示例BD/AB取0.65只是構圖參數，未給的角度與邊長數值不出現在圖文。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-183-given.svg','site/dist/sources/gemini-fIG3raRmygwQ.txt lines 1064–1215,1510–1810'],'sourceUrl':'https://share.gemini.google/fIG3raRmygwQ','generationMethod':'precise native SVG equilateral subtriangles and opposite side-angle correspondence','answerCheckedAgainst':'任意1/2<t<1均DE=tL、EF=(1−t)L，E角60；短邊EF對D角，D小於60。實際座標驗證所有平行及角和。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-183.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
