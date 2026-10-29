from pathlib import Path
import math,json,hashlib,xml.etree.ElementTree as ET
from math import cos,sin,radians,hypot,acos,degrees
A=(0.,0.);P=[A]
for angle in [156,84,12,-60]:
 x,y=P[-1];P.append((x+cos(radians(angle)),y+sin(radians(angle))))
A,B,C,D,E=P
# AB extended through B, DC extended through C; solve intersection independently.
u=(B[0]-A[0],B[1]-A[1]);v=(C[0]-D[0],C[1]-D[1]);w=(D[0]-A[0],D[1]-A[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
t=cross(w,v)/cross(u,v);z=cross(w,u)/cross(u,v);H=(A[0]+t*u[0],A[1]+t*u[1])
def angle(a,b,c):
 u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);return degrees(acos(max(-1,min(1,(u[0]*v[0]+u[1]*v[1])/hypot(*u)/hypot(*v)))))
F=(-2.,A[1]);G=(-2.,D[1]);R=(H[0]+1,H[1])
angles={'ABC':angle(A,B,C),'HBC':angle(H,B,C),'HCB':angle(H,C,B),'BHC':angle(B,H,C),'CDG':angle(C,D,G),'FAB':angle(F,A,B),'BHR':angle(B,H,R),'RHC':angle(R,H,C)}
expected={'ABC':108,'HBC':72,'HCB':72,'BHC':36,'CDG':12,'FAB':24,'BHR':24,'RHC':12}
for k,val in expected.items():assert abs(angles[k]-val)<1e-8,(k,angles[k])
assert t>1 and z>1
sides=[math.dist(P[i],P[(i+1)%5]) for i in range(5)];assert max(sides)-min(sides)<1e-10
proof={'id':'q-210','vertices':dict(zip('ABCDE',P)),'H':H,'ABExtensionParameter':t,'DCExtensionParameter':z,'BInsideAH':t>1,'CInsideDH':z>1,'sideLengths':sides,'anglesDegrees':angles,'expectedDegrees':expected,'parallelHorizontalY':{'L':A[1],'M':D[1],'throughH':H[1]},'allChecksPassed':True,'note':'獨立生成正五邊形邊方向156/84/12/-60/-132度；H位AB與DC延長線，H向右水平確實位HB與HC之間。'}
Path('docs/comics/q-210-geometry-validation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
parts=[]
def txt(x,y,text,size=12,color='#234344',anchor='middle'):
 parts.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{text}</text>')
def path(points,color='#57766a',width=1.5,dash=None,fill='none'):
 d='M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in points);parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def arc(o,r,a,b,col='#95ae80',fill=False):
 p=(o[0]+r*cos(radians(a)),o[1]+r*sin(radians(a)));q=(o[0]+r*cos(radians(b)),o[1]+r*sin(radians(b)))
 d=(f'M{o[0]:.3f} {o[1]:.3f}L{p[0]:.3f} {p[1]:.3f}' if fill else f'M{p[0]:.3f} {p[1]:.3f}')+f'A{r} {r} 0 0 1 {q[0]:.3f} {q[1]:.3f}'+('Z' if fill else '')
 parts.append(f'<path d="{d}" stroke="{col}" stroke-width="1" fill="{col if fill else "none"}" fill-opacity=".3"/>')
# Panel 1: same regular pentagon and original horizontal lines.
T=lambda p:(94+p[0]*62,42+p[1]*62);q=list(map(T,P));a,b,c,d,e=q
path([(12,a[1]),(165,a[1])], '#8d9eac',1);path([(12,d[1]),(165,d[1])],'#8d9eac',1);path(q+[q[0]],width=1.8)
arc(b,13,-24,84,fill=True);txt(b[0]+18,b[1]+13,'108°',10)
arc(a,18,156,180);txt(a[0]-21,a[1]+9,'x',10)
arc(d,23,180,192,col='#b89761');path([(d[0]-22,d[1]-2),(d[0]-30,d[1]-8)],'#8c988d',.8);txt(d[0]-32,d[1]-13,'12°',10)
for pos,label,off in zip(q,'ABCDE',[(0,-7),(-10,1),(-10,0),(5,15),(9,4)]):txt(pos[0]+off[0],pos[1]+off[1],label,11)
txt(16,a[1]-5,'F',10);txt(16,d[1]-5,'G',10);txt(168,a[1]+3,'L',10);txt(168,d[1]+3,'M',10)
txt(90,20,'正五邊形內角108°',14);txt(90,175,'180°−108°＝72°',12)
# Panel 2: HB and HC are extensions of the exact pentagon edges.
T=lambda p:(195+(p[0]-H[0])*47,110+(p[1]-H[1])*47);q=list(map(T,P));a,b,c,d,e=q;h=T(H)
path(q+[q[0]],'#91a393',1)
path([h,b,c,h], '#638863',1.7,fill='#dce8d3')
path([h,a],'#638863',1.2);path([h,d],'#638863',1.2)
arc(b,12,84,156);arc(c,12,-168,-96);arc(h,26,-24,12)
txt(b[0]-12,b[1]+17,'72°',10);txt(c[0]-15,c[1]-12,'72°',10);txt(h[0]+34,h[1]+1,'36°',11)
for pos,label,off in zip(q,'ABCDE',[(0,-6),(-7,-7),(-1,14),(7,13),(9,3)]):txt(pos[0]+off[0],pos[1]+off[1],label,10)
txt(h[0]-6,h[1]+5,'H',11);txt(270,20,'延長AB、DC交於H',14);txt(270,175,'△HBC：72°＋72°＋36°',11)
# Panel 3: exact local directions at H, with a horizontal parallel through H.
h=(384.,111.);upper=(h[0]+122*cos(radians(-24)),h[1]+122*sin(radians(-24)));lower=(h[0]+122*cos(radians(12)),h[1]+122*sin(radians(12)))
arc(h,50,-24,0,fill=True);arc(h,50,0,12,col='#c39c61',fill=True)
path([h,upper],'#5e7d64',1.8);path([h,lower],'#5e7d64',1.8);path([(373,111),(530,111)],'#b08c57',1.2,'4 3')
txt(378,119,'H',11);txt(upper[0]+4,upper[1]-7,'HB',10);txt(lower[0]+2,lower[1]+15,'HC',10);txt(450,99,'x',14);txt(469,124,'12°',12);txt(488,106,'平行L、M',9)
txt(450,20,'36°分成x與12°',14);txt(450,175,'x＝36°−12°＝24°',12)
p=Path('docs/comics/art/q-210.svg');p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><g font-family="Noto Sans CJK TC,sans-serif"><path d="M0 0h180v180H0Z" fill="#eff3e8"/><path d="M180 0h180v180H180Z" fill="#edf1f7"/><path d="M360 0h180v180H360Z" fill="#f8f0e2"/>'+''.join(parts)+'</g></svg>');ET.fromstring(p.read_text())
spec={'id':'q-210','subject':'Math','title':'先求延長線36°，再以平行線扣掉12°','art':str(p),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-210-generate.py','startedAt':'2026-10-29T04:36:37.892984+00:00','panels':[{'heading':'① 正五邊形內角108°，補角72°','text':'每個內角為(5−2)×180°÷5＝108°。把AB與DC延長，三角形在B、C處用到的是內角的補角，所以兩角各為180°−108°＝72°。設所求∠FAB為x。','alt':'新精確正五邊形A–E與水平L/M、F/G，A標x、D標12°，B內角108°；相同正五邊形條件由等邊/角獨立驗證。'},{'heading':'② H是延長線交點，△HBC頂角36°','text':'AB經B延長、DC經C延長，交於H；B在AH上、C在DH上。△HBC兩底角各72°，因此∠BHC＝180°−72°−72°＝36°。','alt':'H向B/A、C/D兩延長線與原五邊形，△HBC淡綠高亮，B/C各72°、H36°，所有點位按同一精確坐標計算。'},{'heading':'③ 過H作平行線，分成x與12°','text':'過H作與L、M平行的直線。它在∠BHC內，上方角等於∠FAB＝x，下方角等於∠CDG＝12°。所以x＋12°＝36°，得x＝24°。','alt':'H局部放大圖的兩射線方向精確為水平上24°、下12°，水平平行線分割總36°；兩弧同半徑，按真實24°/12°夾角標示。'}],'fourth':{'answer':'答案 D：24°','points':['正五邊形內角108°，延長處補角72°。','△HBC的頂角＝36°。','平行線移角：x＋12°＝36°，x＝24°。']},'protectedWords':['108°','72°','36°','12°','24°','∠FAB','∠CDG','∠BHC','△HBC','L、M','x＋12°＝36°'],'rationale':'親見原卷與現有given/proof原生圖，沿已核定D。全新精確SVG同一正五邊形、延長線H、局部水平移角；獨立生成頂點/交點/等邊/角度並驗證B在AH/C在DH/水平位兩射線內，不用人物或來源AI圖，不改必要作答附圖。','promptSummary':'新原生幾何三格：正五邊形內角補角、延長形成72/72/36三角形、H水平平行線上24下12合36。540×180三方原生，精確數學文字HTML，無點陣重繪原卷。','answerCheckedAgainst':'原卷L∥M/正五邊形/∠CDG12°/求FAB與A18 B20 C22 D24；獨立坐標驗證內角108、補角72、H36、平行切分24+12，D不變。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-210-source-1b0793a8fe.jpg'],'existingFiguresActuallyRendered':['site/dist/assets/questions/q-210-given.svg','site/dist/assets/questions/q-210-proof.svg'],'visualChecked':True,'answer':'D 24°','notes':'親見原卷含右側正五邊形可見A/B/C/D/E與L/M線、12條件及全部A–D；現有原生given/proof實際渲染看過。依已核定條件生成新圖，非猜補新疑點。'},'geometryValidation':'docs/comics/q-210-geometry-validation.json','artSHA256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('docs/comics/q-210.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
