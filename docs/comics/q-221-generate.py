from pathlib import Path
import math,json,hashlib,xml.etree.ElementTree as ET
D=(0.,0.);C=(12.,0.);A=(3.,-8.);B=(15.,-8.);P=(7.5,-4.)
dist=math.dist
upper=dist(P,C)+dist(P,D);remaining=29-upper;a=remaining/2;ellipseB2=a*a-36
qx=8.5;qy=math.sqrt(ellipseB2*(1-(qx-6)**2/a**2));Q=(qx,qy);E=(2*qx-12,2*qy);F=(2*qx,2*qy)
mid=lambda a,b:((a[0]+b[0])/2,(a[1]+b[1])/2)
assert dist(P,mid(A,C))<1e-10 and dist(P,mid(B,D))<1e-10
assert dist(Q,mid(C,E))<1e-10 and dist(Q,mid(D,F))<1e-10
pairs={'PA_PC':(dist(P,A),dist(P,C)),'PB_PD':(dist(P,B),dist(P,D)),'QE_QC':(dist(Q,E),dist(Q,C)),'QF_QD':(dist(Q,F),dist(Q,D))}
assert all(abs(x-y)<1e-10 for x,y in pairs.values())
cd=dist(C,D);ab=dist(A,B);ef=dist(E,F);assert max(abs(x-12) for x in [cd,ab,ef])<1e-10
quad=dist(C,P)+dist(P,D)+dist(D,Q)+dist(Q,C);tri1=dist(P,A)+dist(A,B)+dist(B,P);tri2=dist(Q,E)+dist(E,F)+dist(F,Q)
assert abs(quad-29)<1e-9 and abs(tri1+tri2-53)<1e-9 and abs(tri1-tri2)>.01
for x,y,z,w in [(A,B,C,D),(C,D,E,F)]:assert dist((x[0]+z[0],x[1]+z[1]),(y[0]+w[0],y[1]+w[1]))<1e-10
proof={'id':'q-221','coordinates':dict(zip('ABCDEF PQ'.replace(' ',''),[A,B,C,D,E,F,P,Q])),'equalHalfPairs':pairs,'CD':cd,'AB':ab,'EF':ef,'quadrilateralCPDQPerimeter':quad,'trianglePABPerimeter':tri1,'triangleQEFPerimeter':tri2,'trianglePerimeterSum':tri1+tri2,'differentTrianglePerimetersAvoidCongruenceAssumption':abs(tri1-tri2)>.01,'allChecksPassed':True,'note':'選一合法非對稱配置使中央周長真為29；不使用其額外個別半長作解題條件，證明只靠對角線平分與AB=EF=CD。'}
Path('docs/comics/q-221-geometry-validation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
col={'AC':'#ba9357','BD':'#5f9594','CE':'#6689b3','DF':'#b77f70'};parts=[]
def txt(x,y,t,size=12,color='#234344'):
 parts.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color}" text-anchor="middle">{t}</text>')
def path(pts,c='#8ea192',w=1.2,fill='none'):
 parts.append('<path d="M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in pts)+f'" stroke="{c}" stroke-width="{w}" fill="{fill}"/>')
def rect(x,y,w,h,c):parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
# Panel 1: full two parallelograms, color the whole diagonals so paired halves match.
T=lambda p:(20+p[0]*7.5,103+p[1]*7.5)
a1,b1,c1,d1,e1,f1,p1,q1=map(T,[A,B,C,D,E,F,P,Q])
path([a1,b1,c1,d1,a1],fill='#e4ebde');path([c1,d1,e1,f1,c1],fill='#e4ebde')
for v,w,key in [(a1,c1,'AC'),(b1,d1,'BD'),(c1,e1,'CE'),(d1,f1,'DF')]:path([v,w],col[key],1.9)
path([d1,c1],'#5b7465',1.5)
for point,label,off in [(a1,'A',(-3,-6)),(b1,'B',(4,-6)),(c1,'C',(9,2)),(d1,'D',(-9,2)),(e1,'E',(-3,13)),(f1,'F',(5,13)),(p1,'P',(0,-6)),(q1,'Q',(1,13))]:
 parts.append(f'<circle cx="{point[0]:.3f}" cy="{point[1]:.3f}" r="1.7" fill="#36544a"/>');txt(point[0]+off[0],point[1]+off[1],label,11)
txt((d1[0]+c1[0])/2,d1[1]-4,'12',11);txt(90,20,'對角線互相平分',14)
# Panel 2: the four exact colored inner lengths, no central diagonal counted.
T=lambda p:(201+p[0]*11.5,100+p[1]*11.5);c2,p2,d2,q2=map(T,[C,P,D,Q])
path([c2,p2,d2,q2,c2],fill='#f3e8cf')
for v,w,key in [(c2,p2,'AC'),(p2,d2,'BD'),(d2,q2,'DF'),(q2,c2,'CE')]:path([v,w],col[key],2.8)
for point,label,off in [(c2,'C',(9,3)),(p2,'P',(0,-7)),(d2,'D',(-9,3)),(q2,'Q',(0,14))]:txt(point[0]+off[0],point[1]+off[1],label,12)
txt(270,20,'四段斜邊換成中央周界',14);txt(272,105,'四段合計29',14);txt(270,176,'PC＋PD＋DQ＋QC＝29',11)
# Panel 3: add only the two bases that are missing from the known quadrilateral.
txt(450,20,'29再加兩條底邊12',14);rect(398,39,104,35,'#e9dcc0');txt(450,64,'四段29',19);txt(450,96,'＋',22)
rect(376,108,68,34,'#c4d7b1');rect(458,108,68,34,'#c4d7b1');txt(410,131,'AB＝12',15);txt(492,131,'EF＝12',15);txt(451,131,'＋',14);txt(450,175,'29＋12＋12＝53',14)
p=Path('docs/comics/art/q-221.svg');p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><g font-family="Noto Sans CJK TC,sans-serif"><path d="M0 0h180v180H0Z" fill="#eff3e8"/><path d="M180 0h180v180H180Z" fill="#edf1f7"/><path d="M360 0h180v180H360Z" fill="#f8f0e2"/>'+''.join(parts)+'</g></svg>');ET.fromstring(p.read_text())
spec={'id':'q-221','subject':'Math','title':'把四段斜邊換成中央周界，再補兩條12','art':str(p),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-221-generate.py','startedAt':'2026-10-29T04:49:16.885339+00:00','panels':[{'heading':'① P、Q都把各自對角線平分','text':'平行四邊形對角線互相平分，所以PA＝PC、PB＝PD；另一個平行四邊形則QE＝QC、QF＝QD。圖中同一對角線的兩半以相同顏色對應，不能把兩條不同對角線都當等長。','alt':'兩個合法平行四邊形與四條不同色對角線，交點P/Q按真實中點；同條對角線的兩半同色，沒有用同刻痕誤認所有斜邊等長。'},{'heading':'② 四條三角形斜邊，正好換成CPDQ四邊','text':'把△PAB的PA、PB換成PC、PD；把△QEF的QE、QF換成QC、QD。四段加起來就是四邊形CPDQ周長29，這一步還沒有加AB與EF。','alt':'只畫中央C-P-D-Q周界，四段顏色對應第一圖各對角線半長；沒有把中間CD也算進四邊形周長。'},{'heading':'③ 還有兩條底邊，各等於CD＝12','text':'AB與CD是平行四邊形對邊，EF與CD也是對邊，因此AB＝EF＝12。把29再加這兩條底邊：29＋12＋12＝53，選C，無須先求每一條對角線。','alt':'中央四段合計29，另加AB12與EF12兩個相等底邊，得53；各加一次，不重算CD。'}],'fourth':{'answer':'答案 C：53','points':['對角線平分，把三角形斜邊換成中央四段。','PC＋PD＋DQ＋QC＝29。','再加AB與EF各12，周長和53。']},'protectedWords':['PA＝PC','PB＝PD','QE＝QC','QF＝QD','△PAB','△QEF','CPDQ','AB＝EF＝12','CD＝12','29＋12＋12＝53'],'rationale':'親見原卷/四選項與既有given渲染，C維持。全新精確SVG對角線同色半長→中央四段→補兩底邊；選合法非對稱坐標，CD真12、CPDQ真29、兩三角形不全等而和真53，獨立驗證中點/對邊/替換長度。無人物或來源AI圖，不改必要原題圖。','promptSummary':'新原生雙平行四邊形彩色對角線、中央CPDQ四段29、加AB/EF各12。保持真坐標比例與不同上下配置，不以所有斜邊同刻痕或假全等簡化。','answerCheckedAgainst':'原卷兩平行四邊形ABCD/CDEF、P/Q對角線中點、CD12/CPDQ周長29與A49 B51 C53 D55；獨立幾何配置與長度替換得53，C不變。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-221-source-f69ca22424.jpg'],'existingFiguresActuallyRendered':['site/dist/assets/questions/q-221-given.svg'],'visualChecked':True,'answer':'C 53','notes':'親見完整原卷兩圖共享CD、對角線P/Q、CD12與中央周長29、全四選項；現有given已實際渲染。新圖僅另一合法示意，不用上下額外全等或等高作證明。'},'geometryValidation':'docs/comics/q-221-geometry-validation.json','artSHA256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('docs/comics/q-221.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
