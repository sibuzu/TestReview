import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
rad=math.radians
M={'B':(0.,0.),'C':(10.,0.),'A':(6/math.tan(rad(66)),6.)}
M['D']=(10+M['A'][0],6.);M['E']=(14.,0.)
x=10*math.tan(rad(132))/(math.tan(rad(132))-math.tan(rad(33)));M['P']=(x,x*math.tan(rad(33)))
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def ln(ps,c='#70877b',w=1.8):s.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="none" stroke="{c}" stroke-width="{w}"/>')
def arc(p,a,b,r,c):ln([(p[0]+r*math.cos(rad(a+(b-a)*i/30)),p[1]-r*math.sin(rad(a+(b-a)*i/30))) for i in range(31)],c,1.7)
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
def q(n):x,y=M[n];return 15+11.8*x,160-11.8*y
ln([q(n) for n in 'ABCDA']);ln([q('B'),q('P'),q('C')]);ln([q('C'),q('E')])
ln([q('B'),q('P')],'#43825d',3)
for n,dx,dy in [('A',-6,-10),('B',-7,11),('C',0,12),('D',8,-5),('E',5,12),('P',0,-10)]:x,y=q(n);t(x+dx,y+dy,n,13)
arc(q('B'),0,33,27,'#43825d');arc(q('B'),33,66,21,'#43825d')
A=q('A');t(A[0]+18,A[1]+21,'114°',14,c='#9c7044')
B=q('B');t(B[0]+46*math.cos(rad(16.5)),B[1]-46*math.sin(rad(16.5)),'33°',14,c='#43825d')
t(100,24,'B內角：66° ÷ 2',16);t(100,188,'BP平分B角',15)
C=(280,154)
B2=(215,154);E2=(385,154);D2=(280+90*math.cos(rad(66)),154-90*math.sin(rad(66)));P2=(280+90*math.cos(rad(132)),154-90*math.sin(rad(132)))
ln([B2,C,E2]);ln([C,D2],'#b6803d',3);ln([C,P2],'#6486a1',2.5)
for p,v,dx,dy in [(B2,'B',-3,12),(C,'C',0,12),(E2,'E',0,12),(D2,'D',9,-5),(P2,'P',-8,-7)]:t(p[0]+dx,p[1]+dy,v,14)
arc(C,0,66,35,'#b6803d');arc(C,66,132,27,'#b6803d');arc(C,132,180,20,'#6486a1')
for a,r,v,c in [(33,62,'66°','#a36e2f'),(99,61,'66°','#a36e2f'),(156,49,'48°','#557b99')]:t(C[0]+r*math.cos(rad(a)),C[1]-r*math.sin(rad(a)),v,15,c)
t(300,24,'C點內角114°、外角66°',14);t(300,188,'∠BCP＝114°−66°',14)
B3=(420,160);C3=(580,160);scale=16;P3=(420+M['P'][0]*scale,160-M['P'][1]*scale)
ln([B3,P3,C3,B3],'#6486a1',2.2)
for p,v,dx,dy in [(B3,'B',-7,12),(C3,'C',7,12),(P3,'P',0,-11)]:t(p[0]+dx,p[1]+dy,v,15)
arc(B3,0,33,24,'#43825d');arc(C3,132,180,24,'#6486a1')
t(453,148,'33°',15,c='#43825d');t(547,145,'48°',15,c='#557b99');t(P3[0]-3,P3[1]+29,'99°',22,c='#a36e2f')
t(500,24,'△BPC內角和',17);t(500,188,'180°−33°−48°＝99°',14)
s.append('</svg>');Path('docs/comics/art/q-212.svg').write_text(''.join(s))
def ang(a,v,b):
 u=[M[a][i]-M[v][i] for i in [0,1]];w=[M[b][i]-M[v][i] for i in [0,1]];return math.degrees(math.acos(sum(u[i]*w[i] for i in [0,1])/(math.hypot(*u)*math.hypot(*w))))
res={name:ang(a,v,b) for name,a,v,b in [('A','B','A','D'),('ABC','A','B','C'),('ABP','A','B','P'),('PBC','P','B','C'),('BCD','B','C','D'),('DCE','D','C','E'),('PCD','P','C','D'),('BCP','B','C','P'),('BPC','B','P','C')]}
expect={'A':114,'ABC':66,'ABP':33,'PBC':33,'BCD':114,'DCE':66,'PCD':66,'BCP':48,'BPC':99}
assert all(abs(res[k]-v)<1e-8 for k,v in expect.items())
Path('docs/comics/q-212-geometry-validation.json').write_text(json.dumps({'id':'q-212','coordinates':M,'onlyGivenAngleA':114,'measuredAngles':res,'expectedAngles':expect,'triBPCSum':sum(res[k] for k in ['PBC','BCP','BPC']),'CP_not_internal_C_bisector':abs(res['PCD']-res['BCP'])>1e-8,'C_externalEqualPair':abs(res['DCE']-res['PCD'])<1e-8,'q217PenMarkAlreadyConfirmed':True,'independentCoordinatesPass':True},ensure_ascii=False,indent=2)+'\n')
x={'id':'q-212','subject':'Math','title':'B平分內角，C先分清外角，再求P','art':'docs/comics/art/q-212.svg','protectedWords':['∠PCD＝∠DCE','∠PBC','∠BCP','∠BPC','114°','66°','33°','48°','99°','△BPC','外角','內角'],'panels':[{'heading':'① 鄰角互補，B角66°再平分','text':'平行四邊形的鄰角互補，∠ABC＝180°−114°＝66°。BP平分B角，所以△BPC的B內角∠PBC＝33°。','alt':'由A114度精確建立平行四邊形與BP33度方向，B角雙弧示平分，標半角33；P為BP與正確CP方向交點。'},{'heading':'② C外角66°，但△BPC的C角是48°','text':'對角相等，∠BCD＝114°。CE是BC延長線，∠DCE＝66°；已知∠PCD＝∠DCE，因此∠BCP＝114°−66°＝48°。CP並非平分C內角。','alt':'C處放大，B/C/E水平依序共線，CD向66度、CP向132度，兩個橘66在CD兩側，剩餘BCP藍48，不誤畫CP內角平分。'},{'heading':'③ 最後只用△BPC的三角形內角和','text':'已知△BPC在B點33°、C點48°，因此∠P＝∠BPC＝180°−33°−48°＝99°。不要把C點的66°外角直接當成三角形內角。','alt':'精確33/48/99度△BPC，P處99標於三角形內部，B/C不對調，無把外角66放入三角形。'}],'fourth':{'answer':'答案：99°','points':['B內角66°，被BP分成33°。','C點先求外角66°，三角形內角剩48°。','∠BPC＝180°−33°−48°＝99°。']},'rationale':'實看第7及第8題兩份原卷同條件，讀given SVG精確線段；第8題筆跡與重複合併為使用者已確認，不再重開或把筆跡當係數。原封存來源無PCD/DCE/114對應逐字解答，獨立取B(0,0),C(10,0),A(6cot66°,6)，BP33°、CP132°，驗ABC66/ABP33/PBC33/BCD114/DCE66/PCD66/BCP48/BPC99。新精確SVG分B內角、C放大外角、三角形內角和，答案99不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-212-source-77a6ce70ed.jpg','site/dist/assets/questions/q-217-source-8c92cc856d.jpg','site/dist/assets/questions/q-212-given.svg (geometry read)','site/dist/sources/gemini-GD2msWyGjhx0.txt (scoped search no PCD/DCE/114 exact solution)'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG validated parallelogram internal B bisection, enlarged C exterior-angle equality and final BPC triangle','answerCheckedAgainst':'B66半33，C內114外66且PCD66→BCP48，P180−33−48=99。q217筆跡不是係數與合併均已確認，不改原題。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-212.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
