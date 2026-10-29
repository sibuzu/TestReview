import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
rad=math.radians
r=math.sin(rad(28))/math.sin(rad(92))
M={'B':(0.,0.),'C':(1.,0.),'A':(.5,math.sqrt(3)/2),'D':(r,0.),'E':(r/2,-r*math.sqrt(3)/2)}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def ln(ps,c='#70877b',w=1.8,dash=''):s.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def poly(ps,c):s.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="{c}"/>')
def arc(p,a,b,R,c='#b1c6b7',w=1.5):ln([(p[0]+R*math.cos(rad(a+(b-a)*i/40)),p[1]-R*math.sin(rad(a+(b-a)*i/40))) for i in range(41)],c,w)
def tr(n,origin=(25,130),k=120):x,y=M[n];return origin[0]+k*x,origin[1]-k*y
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
ln([tr(n) for n in 'ABCA']);ln([tr('A'),tr('D')]);ln([tr('C'),tr('E')]);arc(tr('B'),-75,65,r*120,'#9baf9c')
ln([tr('B'),tr('D')],'#3e8560',3);ln([tr('B'),tr('E')],'#3e8560',3)
for n,dx,dy in [('A',0,-11),('B',-10,9),('C',10,8),('D',9,-9),('E',-3,12)]:x,y=tr(n);t(x+dx,y+dy,n,14)
t(44,21,'同一圓心B',13);t(145,47,'BD＝BE',16,c='#3e8560')
E=tr('E');arc(E,28,120,18,'#a87942');t(E[0]+28*math.cos(rad(74)),E[1]-28*math.sin(rad(74)),'92°',15,c='#a87942')
# SAS pair in separated positions, using the same scale80
p1={n:tr(n,(214,100),80) for n in ['A','B','D']}
p2={n:tr(n,(306,116),80) for n in ['C','B','E']}
poly([p1[n] for n in ['A','B','D']],'#e3edf3');poly([p2[n] for n in ['C','B','E']],'#f1e3cd')
for p,names in [(p1,['A','B','D']),(p2,['C','B','E'])]:ln([p[n] for n in names+[names[0]]])
ln([p1['A'],p1['B']],'#6288a0',3);ln([p2['C'],p2['B']],'#6288a0',3)
ln([p1['B'],p1['D']],'#3e8560',3);ln([p2['B'],p2['E']],'#3e8560',3)
for p,n,dx,dy in [(p1,'A',0,-11),(p1,'B',-8,9),(p1,'D',8,9),(p2,'C',7,-8),(p2,'B',-9,6),(p2,'E',4,12)]:x,y=p[n];t(x+dx,y+dy,n,13)
arc(p1['B'],0,60,14,'#b58240');arc(p2['B'],-60,0,14,'#b58240')
t(p1['B'][0]+25*math.cos(rad(30)),p1['B'][1]-25*math.sin(rad(30)),'60°',13,c='#a87942')
t(p2['B'][0]+25*math.cos(rad(30)),p2['B'][1]+25*math.sin(rad(30)),'60°',13,c='#a87942')
t(339,24,'SAS全等',17);t(300,184,'AB＝BC；BD＝BE',15)
# transfer D92 and supplementary88 in full-sized triangle
O=(420,165);K=155
p3={n:tr(n,O,K) for n in ['A','B','C','D']}
ln([p3[n] for n in 'ABCA']);ln([p3['A'],p3['D']],'#6288a0',2.8)
for n,dx,dy in [('A',0,-11),('B',-8,9),('C',8,9),('D',0,13)]:x,y=p3[n];t(x+dx,y+dy,n,14)
D=p3['D'];arc(D,88,180,20,'#a87942');arc(D,0,88,29,'#6288a0')
t(D[0]-26,D[1]-26,'92°',16,c='#a87942');t(D[0]+27,D[1]-26,'88°',20,c='#557b99')
t(500,190,'180°−92°＝88°',15)
s.append('</svg>');Path('docs/comics/art/q-215.svg').write_text(''.join(s))
def d(a,b):return math.dist(M[a],M[b])
def ang(a,v,b):
 u=[M[a][i]-M[v][i] for i in [0,1]];w=[M[b][i]-M[v][i] for i in [0,1]];return math.degrees(math.acos(max(-1,min(1,sum(u[i]*w[i] for i in [0,1])/(math.hypot(*u)*math.hypot(*w))))))
res={name:ang(a,v,b) for name,a,v,b in [('ABD','A','B','D'),('CBE','C','B','E'),('BEC','B','E','C'),('ADB','A','D','B'),('ADC','A','D','C')]}
assert all(abs(res[k]-v)<1e-8 for k,v in {'ABD':60,'CBE':60,'BEC':92,'ADB':92,'ADC':88}.items())
assert abs(d('B','D')-d('B','E'))<1e-10 and abs(d('A','B')-d('B','C'))<1e-10
assert 0<r<1
Path('docs/comics/q-215-geometry-validation.json').write_text(json.dumps({'id':'q-215','coordinateSide1_NotGivenLength':1,'constructionRadius':r,'radiusDerivedOnlyToRealizeGiven92':'sin28/sin92','coordinates':M,'measuredAngles':res,'AB_BC':[d('A','B'),d('B','C')],'BD_BE':[d('B','D'),d('B','E')],'SAS_correspondence':['A↔C','B↔B','D↔E'],'BE_parallel_AC_crossProduct':(M['E'][0]-M['B'][0])*(M['C'][1]-M['A'][1])-(M['E'][1]-M['B'][1])*(M['C'][0]-M['A'][0]),'D_inside_BC':0<r<1,'radiusNotAssumedEqualSide':True,'independentPass':True},ensure_ascii=False,indent=2)+'\n')
x={'id':'q-215','subject':'Math','title':'同半徑加60°夾角，全等後用平角','art':'docs/comics/art/q-215.svg','protectedWords':['BD＝BE','AB＝BC','∠ABD','∠CBE','△ABD','△CBE','∠ADB','∠BEC','∠ADC','SAS','60°','92°','88°','適當長'],'panels':[{'heading':'① 同圓心的圓弧，給出BD＝BE','text':'D與E在以B為圓心的同一圓弧上，所以BD＝BE。這個相等關係來自半徑，不必知道半徑數值；題目只說適當長，沒有給半徑等於正三角形邊長。','alt':'精確正三角形與B圓心弧通過D/E，BD/BE同綠，E在BC下方，原92度標在E；弧半徑約邊長0.4698僅供實現原角，不冒充題設。'},{'heading':'② 兩邊與夾角對上，SAS證全等','text':'正三角形有AB＝BC，且∠ABD＝60°。BE平行AC，依圖∠CBE也等於60°。加上BD＝BE，得到△ABD≅△CBE，對應為A對C、B對B、D對E。','alt':'分離畫出的ABD與CBE採相同尺度，AB/BC同藍、BD/BE同綠，兩個B處60度；不把相等兩邊與非夾角誤當SAS。'},{'heading':'③ D點92°與所求角互補','text':'由全等對應角，∠ADB＝∠BEC＝92°。B、D、C共線，∠ADC與∠ADB合成180°，所以∠ADC＝180°−92°＝88°。','alt':'只放大正三角形及AD，D在BC中間，92在DB一側、88在DC一側，兩角共線互補，非把92與88標在同一側。'}],'fourth':{'answer':'答案：88°','points':['同圓半徑：BD＝BE。','AB＝BC且夾角60°，SAS得全等。','∠ADB＝92°，∠ADC＝180°−92°＝88°。']},'rationale':'實看原卷11完整題幹及附圖、讀givenSVG與來源1370–1398不變量摘要；源只留角和摘要，未有逐行完整證明，獨立完成SAS。取等邊長1供繪圖，r=sin28/sin92實現BEC92，驗BD=BE、AB=BC、兩B夾角60、ADB92及ADC88，BE與AC叉積0。新精確SVG同半徑/分離同尺度全等/補角三步，無須把半徑算入教學，答案88不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-215-source-c4fdba3417.jpg','site/dist/assets/questions/q-215-given.svg (exact source construction read)','site/dist/sources/gemini-GD2msWyGjhx0.txt lines 1370–1398'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG equal-radius arc, same-scale SAS correspondence and linear-pair angle transfer','answerCheckedAgainst':'AB=BC、BD=BE、角ABD=CBE60→ABD≅CBE，ADB=BEC92；ADC補角88。精確半徑只是繪圖驗角，非原題新增長度。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-215.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
