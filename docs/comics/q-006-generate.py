import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
u=8+math.sqrt(14);side=math.sqrt(u)
A=(0,0);B=(0,-side);C=(side,-side);D=(side,0);P=((u-6)/(2*side),(8-u)/(2*side));Q=(-P[1],P[0]);v=(D[0]-P[0],D[1]-P[1]);t=-(P[0]*v[0]+P[1]*v[1])/7;H=(P[0]+t*v[0],P[1]+t*v[1])
def d(a,b):return math.dist(a,b)
def dot(a,b):return sum(a[i]*b[i] for i in [0,1])
def angle(a,o,b):
 aa=[a[i]-o[i] for i in [0,1]];bb=[b[i]-o[i] for i in [0,1]];return math.degrees(math.acos(max(-1,min(1,dot(aa,bb)/(math.hypot(*aa)*math.hypot(*bb))))))
vals={'PA':d(P,A),'PB':d(P,B),'PD':d(P,D),'AQ':d(A,Q),'QD':d(Q,D),'PQ':d(P,Q),'AH':d(A,H),'PH':d(P,H),'DH':d(D,H),'APQ':angle(A,P,Q),'QPD':angle(Q,P,D),'APD':angle(A,P,D),'APH':angle(A,P,H),'AHD':angle(A,H,D),'area':side**2,'heightProjectionParameterOnPtoD':t}
for key,want in {'PA':1,'PB':3,'PD':math.sqrt(7),'AQ':1,'QD':3,'PQ':math.sqrt(2),'AH':math.sqrt(.5),'PH':math.sqrt(.5),'APQ':45,'QPD':90,'APD':135,'APH':45,'AHD':90}.items():assert abs(vals[key]-want)<1e-8,(key,vals[key])
assert t<0 and d(D,H)>d(D,P) and abs(d(D,H)-d(D,P)-d(P,H))<1e-9
assert 0<P[0]<side and -side<P[1]<0 and Q[1]>0
assert abs(vals['AH']**2+vals['DH']**2-u)<1e-8
Path('docs/comics/q-006-geometry-validation.json').write_text(json.dumps({'id':'q-006','coordinates':dict(A=A,B=B,C=C,D=D,P=P,Q=Q,H=H),'checks':vals,'rotation':'CCW90 A fixed B maps D P maps Q','H_P_D_orderVerified':True,'Q_above_square':True,'distanceAndAngleChecksPass':True,'allThreePlotsUseSameExactCoordinatesWithIsotropicScale':True},ensure_ascii=False,indent=2)+'\n')
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def tx(x,y,z,f=16,c='#2d4d3a'):s.append(f'<text x="{x:.2f}" y="{y:.2f}" font-family="Noto Sans CJK TC,sans-serif" font-size="{f}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(z)}</text>')
def ln(ps,c='#678a77',w=1.8,d=''):s.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{d}"' if d else '')+'/>')
def poly(ps,fill):s.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="{fill}"/>')
def grid(ox,oy,k):return {n:(ox+k*p[0],oy-k*p[1]) for n,p in dict(A=A,B=B,C=C,D=D,P=P,Q=Q,H=H).items()}
def right(g,o,a,b,k=7):
 O=g[o];aa=[g[a][i]-O[i] for i in [0,1]];bb=[g[b][i]-O[i] for i in [0,1]];aa=[z/math.hypot(*aa)*k for z in aa];bb=[z/math.hypot(*bb)*k for z in bb];ln([(O[0]+aa[0],O[1]+aa[1]),(O[0]+aa[0]+bb[0],O[1]+aa[1]+bb[1]),(O[0]+bb[0],O[1]+bb[1])],'#9b7956',1.3)
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
g=grid(28,66,32)
poly([g[k] for k in ['P','A','B']],'#dae7ee');poly([g[k] for k in ['Q','A','D']],'#f1dfc4')
ln([g[k] for k in ['A','B','C','D','A']],'#719984',1.8);ln([g[k] for k in ['A','P','B']],'#6689a0',2);ln([g[k] for k in ['A','Q','D']],'#b5824d',2)
ln([g['P'],g['D']],'#93a7a1',1,'3 3')
for k,pos in {'A':(16,64),'B':(17,181),'C':(149,182),'D':(149,67),'P':(67,93),'Q':(42,23)}.items():tx(*pos,k)
tx(27,88,'1',14,c='#557c97');tx(29,132,'3',17,c='#557c97');tx(91,34,'3',17,c='#a16c3e');tx(144,127,'繞A旋轉',14);tx(144,150,'90°',17)
g=grid(220,76,45)
poly([g[k] for k in ['A','P','Q']],'#dce8d4');poly([g[k] for k in ['P','Q','D']],'#f3e0c5')
ln([g[k] for k in ['A','P','Q','A']],'#6b9373',2);ln([g[k] for k in ['P','Q','D','P']],'#a98255',2)
right(g,'P','Q','D')
for k,pos in {'A':(211,82),'P':(260,114),'Q':(238,28),'D':(383,83)}.items():tx(*pos,k)
tx(312,35,'QD＝3',16);tx(314,107,'PD＝√7',16);tx(299,151,'PQ²＋PD²＝QD²',16);tx(299,178,'2＋7＝9',18)
g=grid(420,59,45)
poly([g[k] for k in ['A','H','D']],'#dce8d4');ln([g[k] for k in ['A','H','D','A']],'#6b9373',2);ln([g['A'],g['P']],'#9b7956',1.7);right(g,'H','A','D',6)
for k,pos in {'A':(414,45),'H':(418,106),'P':(467,94),'D':(581,47)}.items():tx(*pos,k)
tx(509,50,'AD',17);tx(511,83,'√7',17);tx(447,108,'h',16);tx(408,77,'h',16)
tx(501,135,'AH＝PH＝h',16);tx(501,161,'DH＝√7＋h',18);tx(501,186,'AD²＝h²＋DH²',16)
s.append('</svg>');Path('docs/comics/art/q-006.svg').write_text(''.join(s))
x={'id':'q-006','subject':'Math','title':'旋轉構造直角，再作高求正方形面積','art':'docs/comics/art/q-006.svg','protectedWords':['正方形','等腰直角三角形','畢氏定理','逆定理','延長線','90°','135°','45°','8＋√14'],'panels':[{'heading':'① 繞A逆時針旋轉，B到D、P到Q','text':'將三角形PAB逆時針旋轉90°，得到QAD。對應邊相等，所以AQ＝AP＝1、QD＝PB＝3；Q在正方形上方，且角PAQ是直角。','alt':'真實等比例正方形，A左上B左下D右上，P內部，繞A逆時針90度映至外部上方Q，原三角形與旋轉三角形分色。'},{'heading':'② 用逆定理找出P點的直角','text':'等腰直角三角形PAQ給出PQ²＝2、角APQ為45°。再由2＋7＝9，可知角QPD是90°。射線PQ在角APD內，因此角APD為135°。','alt':'沿同一精確座標畫PAQ及PQD，PQ與PD在P垂直，以右角記號及QD3、PD根號7核對逆畢氏。'},{'heading':'③ 向延長線作高，注意H、P、D次序','text':'將DP越過P延長，作AH垂直於DH。角APH為45°，所以AH＝PH＝h，且h²＝1／2。H在P外側，因此DH＝√7＋h，要相加，不是相減。','alt':'精確投影得到H在DP越過P的延長線，H、P、D共線依序，AH垂直DH；標同長h，AD為斜邊。'}],'fourth':{'answer':'正方形面積＝AD²＝8＋√14','points':['AD²＝h²＋(√7＋h)²。','h²＝1／2，展開得1／2＋7＋√14＋1／2。','所以面積為8＋√14，不使用錯誤的距離平方和公式。']},'rationale':'依使用者已提供且確認的第21題文字與旋轉幾何解法製作；原卷為純文字，當前題庫未保存附件，不冒稱從來源下載原圖。對話原圖可見完整PA1/PB3/PD根號7及內點條件。原AI141–183最初座標答8+根14，287–354後段錯答8已在既有訂正，未重開。獨立精確數值座標驗證逆時針B→D、P→Q、各邊角、H投影及三點順序；全新SVG替代舊AI示意，不更改已確認答案。','originalMaterialsChecked':True,'originalMaterials':['user supplied original第21題 visible in inherited conversation, pure text no given diagram','docs/complete-questions/q-006.json user-confirmed rotation proof','site/dist/sources/6ae04e07-ac08-83e8-a547-b5a07976b7d8.txt lines 141–183 and 287–354'],'sourceUrl':'https://chatgpt.com/share/6ae04e07-ac08-83e8-a547-b5a07976b7d8','generationMethod':'precise native SVG true-square rotation, converse Pythagoras and perpendicular altitude on extended DP','answerCheckedAgainst':'Numerical independent distances PA1 PB3 PDsqrt7, QD3 PQsqrt2, angles45/90/135, H outside P, area8+sqrt14. Existing user confirmation retained.','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-006.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
