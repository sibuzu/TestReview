from pathlib import Path
import math,json,hashlib,xml.etree.ElementTree as ET
from math import sin,cos,radians,degrees,acos,hypot
add=lambda p,a:(p[0]+cos(radians(a)),p[1]+sin(radians(a)))
D=(0.,0.);E=add(D,-96);F=add(E,-36);G=add(F,24);H=add(G,84);I=add(H,144)
A=add(E,-168);B=add(A,120);C=add(B,48)
P=[A,B,C,D,E];Q=[D,E,F,G,H,I];J=(F[0]-1.6,F[1]);X=(F[0]+D[0]-I[0],F[1]+D[1]-I[1])
def angle(a,b,c):
 u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);return degrees(acos(max(-1,min(1,(u[0]*v[0]+u[1]*v[1])/hypot(*u)/hypot(*v)))))
def vec(a,b):return(b[0]-a[0],b[1]-a[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
angles={'CDE':angle(C,D,E),'EDI':angle(E,D,I),'CDI':angle(C,D,I),'DCI':angle(D,C,I),'DIC':angle(D,I,C),'EFG':angle(E,F,G),'XFE':angle(X,F,E),'XFJ':angle(X,F,J),'JFE':angle(J,F,E)}
expect={'CDE':108,'EDI':120,'CDI':132,'DCI':24,'DIC':24,'EFG':120,'XFE':60,'XFJ':24,'JFE':36}
for k,v in expect.items():assert abs(angles[k]-v)<1e-8,(k,angles[k])
ps=[math.dist(P[i],P[(i+1)%5]) for i in range(5)];qs=[math.dist(Q[i],Q[(i+1)%6]) for i in range(6)];assert max(ps+qs)-min(ps+qs)<1e-9
parallel={'FJ_CI_cross':cross(vec(F,J),vec(C,I)),'FX_ID_cross':cross(vec(F,X),vec(I,D)),'FG_DI_cross':cross(vec(F,G),vec(D,I)),'EF_DI_cross_not_zero':cross(vec(E,F),vec(D,I))}
assert max(abs(parallel[k]) for k in ['FJ_CI_cross','FX_ID_cross','FG_DI_cross'])<1e-9 and abs(parallel['EF_DI_cross_not_zero'])>.5
pentAngles=[angle(P[(i-1)%5],P[i],P[(i+1)%5]) for i in range(5)]
hexAngles=[angle(Q[(i-1)%6],Q[i],Q[(i+1)%6]) for i in range(6)]
assert all(abs(a-108)<1e-8 for a in pentAngles) and all(abs(a-120)<1e-8 for a in hexAngles)
inside=abs(angles['XFJ']+angles['JFE']-angles['XFE'])<1e-8
assert inside
head=lambda p:degrees(math.atan2(p[1]-F[1],p[0]-F[0]))%360
directions={k:head(p) for k,p in [('FE',E),('FJ',J),('FX',X),('FG',G)]}
assert directions['FE']<directions['FJ']<directions['FX']
proof={'id':'q-214','vertices':dict(zip('ABCDEFGHI',[A,B,C,D,E,F,G,H,I])),'J':J,'X':X,'pentagonSides':ps,'hexagonSides':qs,'anglesDegrees':angles,'expectedDegrees':expect,'parallelChecks':parallel,'pentagonInteriorAngles':pentAngles,'hexagonInteriorAngles':hexAngles,'FJInsideXFE':inside,'angleDirectionsAtF':directions,'allChecksPassed':True,'note':'共DE長1；兩正多邊形在共邊兩側。CI精確水平，FX與ID同向且與FG反向；禁止將EF誤作DI平行。'}
Path('docs/comics/q-214-geometry-validation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
parts=[]
def txt(x,y,t,size=12,col='#234344'):
 parts.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{col}" text-anchor="middle">{t}</text>')
def path(pts,col='#5d7c6b',width=1.5,dash=None,fill='none'):
 parts.append('<path d="M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in pts)+f'" stroke="{col}" stroke-width="{width}" fill="{fill}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def arc(o,r,a,b,col='#97b17f',fill=False):
 p=(o[0]+r*cos(radians(a)),o[1]+r*sin(radians(a)));q=(o[0]+r*cos(radians(b)),o[1]+r*sin(radians(b)))
 d=(f'M{o[0]:.3f} {o[1]:.3f}L{p[0]:.3f} {p[1]:.3f}' if fill else f'M{p[0]:.3f} {p[1]:.3f}')+f'A{r} {r} 0 0 1 {q[0]:.3f} {q[1]:.3f}'+('Z' if fill else '')
 parts.append(f'<path d="{d}" stroke="{col}" stroke-width="1" fill="{col if fill else "none"}" fill-opacity=".35"/>')
# Panel 1: exact three angles around D, all drawn with equal radius.
o=(90.,96.);r=43
arc(o,r,24,156,'#d1ae6c',True);arc(o,r,156,264,'#9bb67e',True);arc(o,r,264,384,'#9bb7d0',True)
for a,l in [(24,'I'),(156,'C'),(264,'E')]:
 endpoint=(o[0]+r*cos(radians(a)),o[1]+r*sin(radians(a)));path([o,endpoint]);lab=(o[0]+(r+11)*cos(radians(a)),o[1]+(r+11)*sin(radians(a)));txt(lab[0],lab[1]+4,l,12)
txt(96,102,'D',11);txt(65,84,'108°',11);txt(114,83,'120°',11);txt(90,129,'132°',12)
txt(90,20,'D點周圍一周360°',14);txt(90,175,'360°−108°−120°＝132°',11)
# Panel 2: exact aspect ratio of isosceles CDI, not an exaggerated apex.
T=lambda p:(270+p[0]*82,77+p[1]*82);c,d,i=map(T,[C,D,I]);path([c,d,i,c],fill='#dbe7d3',width=1.7)
arc(d,15,24,156,'#b39160');arc(c,19,-24,0);arc(i,19,180,204)
txt(d[0],d[1]-8,'D',12);txt(c[0]-5,c[1]+15,'C',12);txt(i[0]+5,i[1]+15,'I',12);txt(d[0],d[1]+27,'132°',11);txt(c[0]+31,c[1]-3,'24°',11);txt(i[0]-31,i[1]-3,'24°',11)
for q in [c,i]:
 mid=((q[0]+d[0])/2,(q[1]+d[1])/2);u=(q[0]-d[0],q[1]-d[1]);v=(-u[1]/hypot(*u)*4,u[0]/hypot(*u)*4);path([(mid[0]-v[0],mid[1]-v[1]),(mid[0]+v[0],mid[1]+v[1])],width=1.5)
txt(270,20,'CD＝DI：等腰三角形',14);txt(270,148,'兩腰等長，兩底角相等',12);txt(270,175,'(180°−132°)÷2＝24°',12)
# Panel 3: zoom at F. FJ points left, FX points upper-left, FE lower-left.
f=(489.,82.);x=(f[0]+100*cos(radians(204)),f[1]+100*sin(radians(204)));e=(f[0]+110*cos(radians(144)),f[1]+110*sin(radians(144)));g=(f[0]+35*cos(radians(24)),f[1]+35*sin(radians(24)));j=(377.,82.)
arc(f,42,144,180,'#d0ab6c',True);arc(f,42,180,204,'#96b180',True)
path([x,f,g],'#b59360',1.5,'4 3');path([j,f],'#64879b',1.6);path([f,e],'#527b64',1.7)
txt(f[0]+9,f[1]-6,'F',12);txt(x[0]-6,x[1]-6,'X',11);txt(e[0]-5,e[1]+13,'E',11);txt(g[0]+5,g[1]+5,'G',10);txt(j[0]-5,j[1]-5,'J',11)
txt(425,72,'24°',12);txt(420,111,'36°',12);txt(451,95,'FJ∥CI',9)
txt(450,20,'F點：60°−24°＝36°',14);txt(450,174,'FX∥ID，且FG∥DI',11)
p=Path('docs/comics/art/q-214.svg');p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><g font-family="Noto Sans CJK TC,sans-serif"><path d="M0 0h180v180H0Z" fill="#eff3e8"/><path d="M180 0h180v180H180Z" fill="#edf1f7"/><path d="M360 0h180v180H360Z" fill="#f8f0e2"/>'+''.join(parts)+'</g></svg>');ET.fromstring(p.read_text())
spec={'id':'q-214','subject':'Math','title':'共邊先求底角24°，移到F再用60°相減','art':str(p),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-214-generate.py','startedAt':'2026-10-29T04:42:57.771596+00:00','panels':[{'heading':'① D點一周扣掉兩內角，得到132°','text':'兩正多邊形共用DE，所以CD＝DE＝DI。正五邊形在D的內角是108°，正六邊形是120°；D點剩下的∠CDI＝360°−108°−120°＝132°。','alt':'D局部三射線DC/DE/DI，三個等半徑扇形108/120/132度按實際角度構圖，合成一周，非任意圓餅比例。'},{'heading':'② CD＝DI，△CDI的底角都是24°','text':'由共邊可知CD與DI等長，所以△CDI是等腰三角形。頂角132°，兩底角各為(180°−132°)÷2＝24°，特別記住∠DIC＝24°。','alt':'精確比例的鈍角等腰△CDI，頂132度/底各24度、兩腰有等長記號；沒有把扁三角任意拉高。'},{'heading':'③ 將FG經F反向延長至X，再移角','text':'FX與ID同向平行，且FJ與IC同向平行，所以∠XFJ＝24°。正六邊形的FG∥DI，FX是FG的反向延長；∠XFE＝180°−120°＝60°。FJ在兩射線內，故∠JFE＝60°−24°＝36°。','alt':'F局部射線FE下左144度、FJ左180度、FX上左204度與FG右下24度，精確顯示FJ在60度外角內分24/36；不把EF誤作DI平行。'}],'fourth':{'answer':'答案 C：36°','points':['共邊得CD＝DI，D點剩餘角132°。','等腰△CDI底角24°，移角到F。','真正平行的是FG與DI；60°−24°＝36°。']},'protectedWords':['108°','120°','132°','24°','60°','36°','△CDI','∠CDI','∠DIC','∠XFJ','∠XFE','∠JFE','FG∥DI','CD＝DE＝DI'],'rationale':'親見原卷與既有given渲染，沿已核對C。全新精確SVG D一周三角/鈍角等腰三角/F點同向平行三圖，獨立生成兩正多邊形等邊/角度/平行與射線順序驗證；明確FG∥DI而非EF。採局部放大避免180方全圖角標擁擠，不改必要作答圖。無人物或來源AI圖。','promptSummary':'新原生D局部108+120+132、△CDI頂132底24、F局部60被FJ分24+36。等比例真角度/同半徑角弧，非點陣重製原圖或來源AI解說圖。','answerCheckedAgainst':'原卷正五/正六共DE、JF∥CI、求JFE與A34 B35 C36 D37。獨立坐標驗證全部等邊、D132/I24/F60/24/36及FG∥DI、EF不平行DI，C不變。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-214-source-05cd94a846.jpg'],'existingFiguresActuallyRendered':['site/dist/assets/questions/q-214-given.svg'],'visualChecked':True,'answer':'C 36°','notes':'親見完整原卷題文/四選項及共邊圖，現有given實際渲染查看；J在F左、CI水平，FX沿FG反方向，絕不翻轉FJ選錯補角。'},'geometryValidation':'docs/comics/q-214-geometry-validation.json','artSHA256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('docs/comics/q-214.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
