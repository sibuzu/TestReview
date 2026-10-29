import json,datetime,hashlib
from fractions import Fraction as F
from pathlib import Path
from xml.sax.saxutils import escape
A=(-3,0);B=(0,-2);C=(5,0);D=(0,12);P=(F(-35,9),F(-32,9))
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def area(ps):return abs(sum(cross(ps[i],ps[(i+1)%len(ps)]) for i in range(len(ps)))/2)
v={'PAB':area([P,A,B]),'PCD':area([P,C,D]),'ABCD':area([A,B,C,D])}
assert v['PCD']-v['PAB']==v['ABCD']==56
assert 14==2*8-2 and 5+12==17
assert cross((A[0]-P[0],A[1]-P[1]),(D[0]-P[0],D[1]-P[1]))==0
assert cross((B[0]-P[0],B[1]-P[1]),(C[0]-P[0],C[1]-P[1]))==0
Path('docs/comics/q-232-geometry-validation.json').write_text(json.dumps({'id':'q-232','coordinates':{k:[str(x) for x in z] for k,z in dict(A=A,B=B,C=C,D=D,P=P).items()},'exactAreas':{k:str(z) for k,z in v.items()},'areaDifference':56,'nestedSegmentRatios':{'PA_PD':'8/35','PB_PC':'7/16'},'isotropicPlotScale':10,'AC':8,'BD':14,'BD_Equals_2AC_Minus2':True,'quadraticRoots':[8,-7],'negativeLengthRejected':True,'m':5,'n':12,'sum':17,'renderCoordinatesUseSolvedValues_NotExtraGivens':True,'allChecksPass':True},ensure_ascii=False,indent=2)+'\n')
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def ln(ps,c='#789786',w=1.8,d=''):s.append('<polyline points="'+' '.join(f'{float(x):.3f},{float(y):.3f}' for x,y in ps)+f'" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
def poly(ps,fill):s.append('<polygon points="'+' '.join(f'{float(x):.3f},{float(y):.3f}' for x,y in ps)+f'" fill="{fill}"/>')
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
def conv(q,ox,oy):return ox+10*q[0],oy-10*q[1]
g={k:conv(q,77,148) for k,q in dict(A=A,B=B,C=C,D=D,P=P).items()}
poly([g[k] for k in ['P','C','D']],'#f4e3cb');poly([g[k] for k in ['P','A','B']],'#d6e4ee');poly([g[k] for k in ['A','B','C','D']],'#d4e5cb')
ln([g[k] for k in ['P','C','D','P']],'#aa855b',2);ln([g[k] for k in ['A','B','C','D','A']],'#507a5b',2.2)
ln([(22,148),(155,148)],'#a8b9af',1,'3 3');ln([(77,189),(77,16)],'#a8b9af',1,'3 3')
for k,pos in {'P':(24,186),'A':(33,144),'B':(91,175),'C':(141,150),'D':(92,27)}.items():t(*pos,k,17)
t(146,52,'大減小',16);t(142,78,'剩綠色',16);t(139,108,'面積56',16)
g={k:conv(q,277,148) for k,q in dict(A=A,B=B,C=C,D=D).items()}
poly([g[k] for k in ['A','B','C','D']],'#d4e5cb');ln([g[k] for k in ['A','B','C','D','A']],'#507a5b',2)
ln([g['A'],g['C']],'#62869d',2.5);ln([g['B'],g['D']],'#b5824d',2.5)
ln([(277,140),(285,140),(285,148)],'#7d9282',1.3)
for k,pos in {'A':(235,145),'B':(290,171),'C':(340,148),'D':(291,24)}.items():t(*pos,k,17)
ln([(247,177),(327,177)],'#62869d',1.6);t(286,190,'AC＝m＋3',14,c='#557c97')
ln([(352,28),(352,168)],'#b5824d',1.6);t(374,79,'BD',16,c='#a16c3e');t(374,104,'n＋2',15,c='#a16c3e')
t(500,22,'面積列式',18)
t(500,53,'x²−x−56＝0',18)
t(500,84,'(x−8)(x＋7)＝0',16)
t(458,121,'8 ✓',22,c='#507a5b');t(545,121,'−7 ×',21,c='#ab7663')
t(500,149,'長度只能取正',16)
t(500,179,'AC＝8，BD＝14',17)
s.append('</svg>');Path('docs/comics/art/q-232.svg').write_text(''.join(s))
x={'id':'q-232','subject':'Math','title':'三角形面積相減，留下四邊形','art':'docs/comics/art/q-232.svg','protectedWords':['四邊形','三角形','面積差','對角線','共同底邊','正根','負根','AC＝8','BD＝14','m＝5','n＝12'],'panels':[{'heading':'① 大三角形減小三角形，留下56','text':'P、A、D共線，P、B、C共線。大三角形PCD扣掉小三角形PAB，剩下四邊形ABCD，所以四邊形面積是56；不是面積比1：56。','alt':'依解得坐標等比例畫相套三角形，P在左下，PAB藍色、ABCD綠色，共同部分扣除後剩四邊形。'},{'heading':'② 對角線互相垂直，面積可相乘取半','text':'沿AC切成上下兩個三角形，共同底邊是AC，高分別為2與n。因此面積等於AC乘BD再除以2，其中AC＝m＋3，BD＝n＋2。','alt':'同一坐標四邊形，水平AC和垂直BD相交成直角，長度以m＋3與n＋2表示，不靠圖上視覺比例猜數值。'},{'heading':'③ 設AC為x，記得兩倍還要減2','text':'BD＝2x−2，代入面積56得x²−x−56＝0。分解後有8與−7兩根；長度必須為正，所以AC＝8，接著BD＝14。','alt':'完整一元二次方程式、因式分解、正根8及負根−7並列，負根只作代數解，不畫成負邊長。'}],'fourth':{'answer':'答案 17：m＝5，n＝12','points':['AC＝m＋3＝8，所以m＝5。','BD＝n＋2＝14，所以n＝12。','m＋n＝17；回代面積與兩倍少2都成立。']},'rationale':'實看原卷第5題與作答SVG；來源1628–1644僅提共享三角形消去摘要，未冒稱有完整推導。獨立精確分數求P=(-35/9,-32/9)，PAB=56/9、PCD=560/9，相減56；用等比例真坐標畫出相套與對角線，正負根分清，不將圖上解後坐標當新增已知。原答案17不變。','sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-232-source-a74e3d3a0e.jpg','site/dist/assets/questions/q-232-given.svg','site/dist/sources/gemini-GD2msWyGjhx0.txt lines 1628–1644 summary only'],'answerCheckedAgainst':'Exact Fraction intersection and area differences, x roots8/-7, positive8, diagonals8/14, m5+n12=17.','generationMethod':'precise native SVG coordinate nested triangles, perpendicular diagonals and positive quadratic-root selection','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-232.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
