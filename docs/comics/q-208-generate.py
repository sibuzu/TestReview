import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
P={'A':(20,30),'B':(170,30)}
P['C']=(70,30+100*math.tan(math.radians(20)))
P['D']=(150,P['C'][1]+80*math.tan(math.radians(30)))
P['E']=(70,P['D'][1]+80*math.tan(math.radians(28)))
P['F']=(180,P['E'][1])
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def line(pts,c='#70877b',w=2,dash=''):
 s.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)+f'" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def arc(x,y,a,b,r,c):line([(x+r*math.cos(math.radians(a+(b-a)*i/24)),y+r*math.sin(math.radians(a+(b-a)*i/24))) for i in range(25)],c,1.6)
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
line([P[x] for x in 'ABCDEF'])
for n in ['C','D']:line([(20,P[n][1]),(180,P[n][1])],'#bdcdbf',1.3,'4 4')
for n,dx,dy in [('A',-9,-4),('B',9,-5),('C',-11,0),('D',11,0),('E',-11,11),('F',5,3)]:x,y=P[n];t(x+dx,y+dy,n,13)
for v,a,b,r,lab in [('B',160,180,50,'1'),('C',-20,30,26,'2'),('D',152,210,27,'3'),('E',-28,0,36,'4')]:
 x,y=P[v];arc(x,y,a,b,r-10,'#a5805b');mid=(a+b)/2;t(x+r*math.cos(math.radians(mid)),y+r*math.sin(math.radians(mid)),lab,14,c='#9a6945')
t(100,188,'AB ∥ EF',16)
t(300,20,'拆開中間的兩個角',16)
C=(256,62);D=(356,142)
line([C,(C[0]+77*math.cos(math.radians(-20)),C[1]+77*math.sin(math.radians(-20)))])
line([C,(C[0]+77*math.cos(math.radians(30)),C[1]+77*math.sin(math.radians(30)))])
line([C,(380,C[1])],'#b9cbbd',1.5,'4 4')
arc(*C,-20,0,40,'#4b8463');arc(*C,0,30,32,'#b17c40');t(306,53,'α',16,c='#4b8463');t(300,78,'β',16,c='#a9773d');t(245,62,'C',14)
line([D,(D[0]+77*math.cos(math.radians(210)),D[1]+77*math.sin(math.radians(210)))])
line([D,(D[0]+77*math.cos(math.radians(152)),D[1]+77*math.sin(math.radians(152)))])
line([D,(220,D[1])],'#b9cbbd',1.5,'4 4')
arc(*D,180,210,34,'#b17c40');arc(*D,152,180,40,'#688aa8');t(308,129,'β',16,c='#a9773d');t(307,154,'γ',16,c='#688aa8');t(368,142,'D',14)
t(300,188,'∠2＝α＋β；∠3＝β＋γ',13)
t(500,22,'代入後，b消去',18)
t(500,58,'(a＋5)−b＋(b＋8)',17)
t(453,96,'＝a＋5',16);t(497,96,'−b',16);t(535,96,'＋b',16);t(575,96,'＋8',16)
line([(485,88),(509,104)],'#b08163',1.5);line([(523,88),(547,104)],'#b08163',1.5)
t(500,144,'＝a＋13',28,c='#3e805a')
t(500,181,'常數5與8仍要相加',15)
s.append('</svg>');Path('docs/comics/art/q-208.svg').write_text(''.join(s))
def angle(a,v,b):
 u=(P[a][0]-P[v][0],P[a][1]-P[v][1]);w=(P[b][0]-P[v][0],P[b][1]-P[v][1]);return math.degrees(math.acos(sum(u[i]*w[i] for i in [0,1])/(math.hypot(*u)*math.hypot(*w))))
ang=[angle('A','B','C'),angle('B','C','D'),angle('C','D','E'),angle('D','E','F')]
assert all(abs(a-b)<1e-9 for a,b in zip(ang,[20,50,58,28]));assert abs(ang[0]-ang[1]+ang[2]-ang[3])<1e-9
# symbolic coefficients [a,b,constant] of (a+5)-b+(b+8)
coef=[1+0+0,0-1+1,5+0+8];assert coef==[1,0,13]
v={'id':'q-208','illustrativeCoordinates':P,'sampleOnlyNotAddedQuestionData':{'a':15,'b':50},'measuredFourAngles':ang,'AB_EF_HorizontalParallel':P['A'][1]==P['B'][1] and P['E'][1]==P['F'][1],'alpha_beta_gamma':[20,30,28],'angle2_alphaPlusBeta':50,'angle3_betaPlusGamma':58,'identityResidual':ang[0]-ang[1]+ang[2]-ang[3],'symbolicPolynomialCoefficients_a_b_constant':coef,'independentAlgebraAndGeometryPass':True}
Path('docs/comics/q-208-geometry-validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
x={'id':'q-208','subject':'Math','title':'共同平行線拆角，消去b後留下a＋13','art':'docs/comics/art/q-208.svg','protectedWords':['AB∥EF','∠1','∠2','∠3','∠4','α＋β','β＋γ','a＋13','角度','平行線','共同基準'],'panels':[{'heading':'① 過C、D作共同的平行基準','text':'過C、D作AB的平行線，也都平行EF。設BC、CD、DE與共同平行線所成的銳角為α、β、γ，由移角可知∠1＝α、∠4＝γ。','alt':'精確方向角鋸齒ABCDEF與AB平行EF，過C/D的虛線同為水平，標原四角1至4；樣例座標僅實現原方向，不額外指定a或b值。'},{'heading':'② 中間兩折角分別是α＋β、β＋γ','text':'依圖，∠2＝α＋β，∠3＝β＋γ。因此∠1−∠2＋∠3＝α−(α＋β)＋(β＋γ)＝γ，正好就是∠4。','alt':'C的上下分角α/β與D的左上/左下分角β/γ兩處放大圖，各用同方向平行虛線，沒有把補角誤當同位銳角。'},{'heading':'③ 代回原式，b消去，但5與8不消失','text':'∠4＝(a＋5)°−b°＋(b＋8)°。−b與＋b相消，常數仍是5＋8＝13，所以得到(a＋13)°，選D。','alt':'只將b的負正項相消，結果a+13；不把a、5或8劃掉，不把角度關係用生成模型猜測。'}],'fourth':{'answer':'答案 D：(a＋13)°','points':['共同平行基準把中間兩角拆為和。','∠4＝∠1−∠2＋∠3。','(a＋5)−b＋(b＋8)＝a＋13。']},'rationale':'實看原卷3題完整圖、a/b條件及四選項（含手寫補列），讀作答SVG與來源關鍵字搜尋，未找本題鋸齒逐行解答；獨立構造α20 β30 γ28樣例，四原角20/50/58/28且符合a15 b50，驗共同平行線與交錯角關係；另以符號係數核a1,b0,常數13。樣例值只用程式驗證不寫成題目條件。新原生SVG完整折線、分角放大及代數消元，D答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-208-source-f5a9c1e9c5.jpg','site/dist/assets/questions/q-208-given.svg (exact source figure read)','site/dist/sources/gemini-GD2msWyGjhx0.txt (scoped search no exact zigzag/angle1-angle2 solution; broader parallel-angle module read with q-205)'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG validated zigzag directions, two enlarged angle partitions and symbolic cancellation','answerCheckedAgainst':'α−(α+β)+(β+γ)=γ→∠4=∠1−∠2+∠3→a+5−b+b+8=a+13，D。精確方向及係數另驗。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-208.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
