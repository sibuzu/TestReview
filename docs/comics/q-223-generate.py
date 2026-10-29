import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
rad=math.radians
L=10;s=L/(2*math.cos(rad(22)))
M={'B':(0.,0.),'C':(L,0.),'A':(s*math.cos(rad(66)),s*math.sin(rad(66)))}
M['D']=(L+M['A'][0],M['A'][1]);u=[v/math.hypot(*M['D']) for v in M['D']];dot=sum(u[i]*M['A'][i] for i in [0,1]);M['Ap']=tuple(2*dot*u[i]-M['A'][i] for i in [0,1]);f=-M['Ap'][1]/(M['D'][1]-M['Ap'][1]);M['E']=(M['Ap'][0]+f*(M['D'][0]-M['Ap'][0]),0.)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def ln(ps,c='#70877b',w=1.8,dash=''):s.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def arc(p,a,b,r,c):ln([(p[0]+r*math.cos(rad(a+(b-a)*i/30)),p[1]-r*math.sin(rad(a+(b-a)*i/30))) for i in range(31)],c,1.5)
def tr(n,o=0,k=13,base=130):x,y=M[n];return o+18+k*x,base-k*y
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
for o in [0,400]:
 s.append('<polygon points="'+' '.join(f'{tr(n,o)[0]},{tr(n,o)[1]}' for n in ['B','D','Ap'])+'" fill="#f1e6d5"/>')
 ln([tr('A',o),tr('B',o)],'#9aa99b',1.5,'4 3');ln([tr('A',o),tr('D',o)],'#9aa99b',1.5,'4 3')
 ln([tr('B',o),tr('C',o),tr('D',o)])
 ln([tr('B',o),tr('D',o)],'#3e855e',2.7,'5 3')
 ln([tr('B',o),tr('Ap',o),tr('D',o)],'#a77e4e',2.2)
 for n,lab,dx,dy in [('A','A',0,-11),('B','B',-9,9),('C','C',7,10),('D','D',8,-11),('Ap','A′',0,13),('E','E',0,12)]:x,y=tr(n,o);t(x+dx,y+dy,lab,13)
 if o==0:
  t(100,23,'BD是摺線',17)
  D=tr('D');arc(D,180,202,26,'#3e855e');arc(D,202,224,33,'#3e855e')
  for a,R in [(191,47),(213,47)]:t(D[0]+R*math.cos(rad(a)),D[1]-R*math.sin(rad(a)),'x',15,c='#3e855e')
  B=tr('B');arc(B,0,22,29,'#3e855e');t(B[0]+53*math.cos(rad(11)),B[1]-53*math.sin(rad(11)),'x',15,c='#3e855e')
  t(B[0]+33*math.cos(rad(44)),B[1]-33*math.sin(rad(44)),'44°',13,c='#9b7042')
  E=tr('E');t(E[0]+28*math.cos(rad(22)),E[1]-28*math.sin(rad(22)),'44°',13,c='#9b7042')
 else:
  t(500,23,'摺疊保留角度',17)
  B=tr('B',o);arc(B,0,66,30,'#3e855e');t(B[0]+47*math.cos(rad(33)),B[1]-47*math.sin(rad(33)),'66°',15,c='#3e855e')
  Ap=tr('Ap',o);arc(Ap,44,158,20,'#a77e4e');t(Ap[0]+31*math.cos(rad(101)),Ap[1]-31*math.sin(rad(101)),'114°',19,c='#996f43')
  t(500,190,'∠A′＝∠A＝114°',16)
# isolated BDE plus original EC extension
O=197;K=13.5;base=155
T={n:tr(n,O,K,base) for n in ['B','D','E','C']}
s.append('<polygon points="'+' '.join(f'{T[n][0]},{T[n][1]}' for n in ['B','D','E'])+'" fill="#e2eddd"/>')
ln([T[n] for n in ['B','D','E','B']]);ln([T['E'],T['C']])
for n,dx,dy in [('B',-7,11),('D',9,-8),('E',0,13),('C',7,12)]:x,y=T[n];t(x+dx,y+dy,n,14)
B,D,E=T['B'],T['D'],T['E'];arc(B,0,22,27,'#3e855e');arc(D,202,224,25,'#3e855e');arc(E,44,180,21,'#a77e4e');arc(E,0,44,30,'#a77e4e')
t(B[0]+46*math.cos(rad(11)),B[1]-46*math.sin(rad(11)),'x',17,c='#3e855e')
t(D[0]+42*math.cos(rad(213)),D[1]-42*math.sin(rad(213)),'x',17,c='#3e855e')
t(E[0]+31*math.cos(rad(112)),E[1]-31*math.sin(rad(112)),'136°',18,c='#996f43')
t(E[0]+37*math.cos(rad(22)),E[1]-37*math.sin(rad(22)),'44°',14,c='#996f43')
t(300,23,'2x＋136°＝180°',17);t(300,190,'x＝22°',21,c='#3e855e')
s.append('</svg>');Path('docs/comics/art/q-223.svg').write_text(''.join(s))
def ang(a,v,b):
 u=[M[a][i]-M[v][i] for i in [0,1]];w=[M[b][i]-M[v][i] for i in [0,1]];return math.degrees(math.acos(max(-1,min(1,sum(u[i]*w[i] for i in [0,1])/(math.hypot(*u)*math.hypot(*w))))))
trip=[('ABD','A','B','D'),('DEC','D','E','C'),('DBC','D','B','C'),('ADB','A','D','B'),('BDAp','B','D','Ap'),('BDE','B','D','E'),('BED','B','E','D'),('ABC','A','B','C'),('BAD','B','A','D'),('BApD','B','Ap','D')]
angles={k:ang(a,v,b) for k,a,v,b in trip};expected={'ABD':44,'DEC':44,'DBC':22,'ADB':22,'BDAp':22,'BDE':22,'BED':136,'ABC':66,'BAD':114,'BApD':114}
assert all(abs(angles[k]-v)<1e-8 for k,v in expected.items())
assert 0<M['E'][0]<10 and 0<f<1
assert abs(math.dist(M['A'],M['B'])-math.dist(M['Ap'],M['B']))<1e-10
assert abs(math.dist(M['A'],M['D'])-math.dist(M['Ap'],M['D']))<1e-10
Path('docs/comics/q-223-geometry-validation.json').write_text(json.dumps({'id':'q-223','coordinates':M,'baseLength10IllustrationOnly':True,'reflectionAxis':'BD','reflectionComputedBy':'A′=2u(u·A)−A with B at origin and u unit alongBD','B_D_fixedByReflection':True,'ABequalsApB':True,'ADequalsApD':True,'EonApDSegmentParameter':f,'EinsideBC':True,'measuredAngles':angles,'expectedAngles':expected,'independentReflectionAndAnglesPass':True},ensure_ascii=False,indent=2)+'\n')
x={'id':'q-223','subject':'Math','title':'摺疊給兩個x，先求22°再回到A′','art':'docs/comics/art/q-223.svg','protectedWords':['BD','A′','∠DBC','∠ADB','∠BDE','∠BED','∠DEC','∠ABC','44°','136°','22°','66°','114°','△BDE','摺疊'],'panels':[{'heading':'① 先設BD與BC的夾角為x','text':'設∠DBC＝x。AD平行BC，得∠ADB＝x；沿BD摺疊，DA映到DA′，所以∠BDA′也等於x。E在DA′上，因此∠BDE＝x。','alt':'依真正BD鏡射構造A′，原AB/AD虛線、BD綠摺線、A′下方實線，B處x及D兩側相等x；B/D固定不移，E是DA′交BC。'},{'heading':'② E點先求補角，再用三角形內角和','text':'B、E、C共線，外角44°的補角是136°，所以∠BED＝136°。△BDE其餘兩角都是x，兩個x合計44°，解得x＝22°。','alt':'同幾何單獨放大△BDE，E的136在三角內、44在EC一側外角，B/D各x；角標未互換，x22由內角和求得。'},{'heading':'③ B內角66°，摺前摺後A角都114°','text':'B點44°再加上22°，完整內角為66°。平行四邊形鄰角互補，180°扣掉66°得到A角114°。摺疊保留角度，因此∠A′＝114°，選A。','alt':'完整反射形的B角標66度、A′的BA′D角標114，原A仍在虛線摺前位置，不把折後A′錯畫成平行四邊形頂點或改變角度。'}],'fourth':{'answer':'答案 A：114°','points':['△BDE兩個相等小角，皆為22°。','B角的44°加上22°，合成66°。','A角與A′角都等於114°。']},'rationale':'實看原卷第6題完整句、四選項及摺前虛線附圖，讀givenSVG與來源1460–1497摺疊公式摘要。獨立取BC10僅供繪圖，AB=10/(2cos22)，A方向66，D=A+C，A′以BD真鏡射2u(u·A)−A構造，E求線交；驗ABD=DEC44、DBC=ADB=BDA′=BDE22、BED136、ABC66、BAD=BA′D114。新精確SVG鏡射/三角形補角/角度保留，不新增邊長題設，114答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-223-source-33cb93cd85.jpg','site/dist/assets/questions/q-223-given.svg (source fold geometry read)','site/dist/sources/gemini-GD2msWyGjhx0.txt lines 1460–1497'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG true reflection across BD, line intersection E and validated angle partitions','answerCheckedAgainst':'AD∥BC與摺疊→BDE兩角x，BED136→x22，ABC44+22=66，A=A′114。鏡射等距與所有角另驗。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-223.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
