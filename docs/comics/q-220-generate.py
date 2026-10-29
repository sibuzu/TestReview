import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
L=6.;tau=.4;h=L*math.sqrt(3)/2
M={'A':(L/2,h),'B':(0.,0.),'C':(L,0.),'D':(L*tau,0.),'F':(L*tau/2,tau*h),'E':(L*(1+tau)/2,(1-tau)*h)}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def ln(ps,c='#70877b',w=1.8):s.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="none" stroke="{c}" stroke-width="{w}"/>')
def xy(n,o):x,y=M[n];return o+25+24*x,165-24*y
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
for o in [0,200]:
 if o==0:
  s.append('<polygon points="'+' '.join(f'{xy(n,o)[0]},{xy(n,o)[1]}' for n in ['B','F','D'])+'" fill="#e0eddc"/>')
 else:
  s.append('<polygon points="'+' '.join(f'{xy(n,o)[0]},{xy(n,o)[1]}' for n in ['A','F','D','E'])+'" fill="#e3edf3"/>')
 ln([xy(n,o) for n in 'ABCA']);ln([xy('D',o),xy('F',o)]);ln([xy('D',o),xy('E',o)])
 if o==0:
  for a,b in [('B','F'),('F','D'),('B','D')]:ln([xy(a,o),xy(b,o)],'#43855e',3)
  B=xy('B',o);arc=[(B[0]+22*math.cos(math.radians(a)),B[1]-22*math.sin(math.radians(a))) for a in range(61)];ln(arc,'#43855e',1.5);t(B[0]+31*math.cos(math.radians(30)),B[1]-31*math.sin(math.radians(30)),'60°',13,c='#43855e')
 else:
  for a,b,c in [('A','F','#61859e'),('D','E','#61859e'),('A','E','#43855e'),('F','D','#43855e'),('B','F','#43855e')]:ln([xy(a,o),xy(b,o)],c,3.3)
 for n,dx,dy in [('A',0,-11),('B',-10,10),('C',10,10),('D',-7,13),('F',-11,0),('E',10,-2)]:x,y=xy(n,o);t(x+dx,y+dy,n,14)
 if o==0:t(42,24,'等角60°',15)
 else:t(251,24,'同綠等長',15)
t(500,22,'2 × AB＝12',20)
for y in [45,68]:
 s.append(f'<rect x="435" y="{y}" width="78" height="16" fill="#b7ccda"/><rect x="513" y="{y}" width="52" height="16" fill="#a9caaa"/><rect x="435" y="{y}" width="130" height="16" fill="none" stroke="#7d9a87"/>');t(500,y+9,'6',14)
t(500,105,'3 × AB＝18',20)
for y in [129,152,175]:
 s.append(f'<rect x="435" y="{y}" width="78" height="16" fill="#b7ccda"/><rect x="513" y="{y}" width="52" height="16" fill="#a9caaa"/><rect x="435" y="{y}" width="130" height="16" fill="none" stroke="#7d9a87"/>');t(500,y+9,'6',14)
s.append('</svg>');Path('docs/comics/art/q-220.svg').write_text(''.join(s))
def d(a,b):return math.dist(M[a],M[b])
assert all(abs(d(a,b)-6)<1e-9 for a,b in [('A','B'),('B','C'),('C','A')])
assert all(abs(d(a,b)-2.4)<1e-9 for a,b in [('B','F'),('B','D'),('F','D'),('A','E')])
assert abs(d('A','F')-3.6)<1e-9
per=sum(d(a,b) for a,b in [('A','F'),('F','D'),('D','E'),('E','A')]);assert abs(per-12)<1e-9
checks=[]
for u in [.2,.4,.7]:checks.append({'chosenInternalBaseFraction_NotGiven':u,'AF':6*(1-u),'AE':6*u,'AFplusAE':6*(1-u)+6*u,'parallelogramPerimeter':2*(6*(1-u)+6*u)})
Path('docs/comics/q-220-geometry-validation.json').write_text(json.dumps({'id':'q-220','coordinates':M,'illustrativeDfraction_NotAdditionalCondition':tau,'BF_BD_DF_AE':[d('B','F'),d('B','D'),d('D','F'),d('A','E')],'AFplusAE':d('A','F')+d('A','E'),'AFDEPerimeter':per,'trianglePerimeter':18,'adjacentSidesDifferent':[3.6,2.4],'variablePointChecks':checks,'symbolic':'AF=(1−t)L, AE=tL, AF+AE=L, quadrilateralPerimeter=2L=12, L=6, trianglePerimeter=3L=18','barCopiesTop':2,'barCopiesBottom':3,'independentPass':True},ensure_ascii=False,indent=2)+'\n')
x={'id':'q-220','subject':'Math','title':'平行四邊形相鄰邊和，正好是一條大三角形邊','art':'docs/comics/art/q-220.svg','protectedWords':['△BFD','正三角形','平行四邊形','BF＝BD＝DF','AE＝DF＝BF','AF＋AE','AF＋BF','AB','12公分','18公分'],'panels':[{'heading':'① 平行線讓△BFD也成正三角形','text':'BF在BA上，BD在BC上，FD平行AC，所以△BFD的三個角都是60°。因此BF＝BD＝DF，先把這組相等短邊找出來。','alt':'精確等邊ABC內部D取BC的0.4位置作示意，BFD淡綠、三邊同綠並標60度，F/E不交換，不把D當固定中點。'},{'heading':'② 用AE＝BF，把相鄰邊拼回AB','text':'AF平行DE、AE平行DF，AFDE為平行四邊形，對邊相等，AE＝DF。結合前格，AE＝DF＝BF，因此AF＋AE＝AF＋BF＝AB。','alt':'相同座標以AF/DE藍色與AE/DF綠色分辨兩組對邊，BF也綠色，AF加BF正好完整AB；相鄰邊長3.6/2.4不同，非菱形假設。'},{'heading':'③ 12是兩份AB，先求出一份AB','text':'12＝2(AF＋AE)＝2AB，所以AB＝6公分。△ABC三邊都等於AB，周長就是3×6＝18公分，選A。','alt':'兩份同長6的條帶合12，三份同長6合18；每份藍綠分段仍保持相鄰邊比例，只表示已推得的AB，不把12當單邊。'}],'fourth':{'answer':'答案 A：18公分','points':['△BFD正三角形，BF＝DF。','平行四邊形AE＝DF，所以AF＋AE＝AB。','12＝2AB，AB＝6；大三角形周長＝18。']},'rationale':'實看4-2第3題完整原卷、四選項及givenSVG；來源封存未搜尋到AFDE/BFD/周長12對應逐行解答，獨立核幾何。取邊6、D在BC0.4示意，AF3.6 AE2.4，相鄰不等；驗BF=BD=DF=AE2.4、AF+AE6、四邊周長12、三角18，另以t=.2/.4/.7核不變式。新精確SVG等邊/對邊轉換/2份對3份條帶，18答不變，不把示意t當條件。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-220-source-02365895f1.jpg','site/dist/assets/questions/q-220-given.svg (source geometry read)','site/dist/sources/gemini-GD2msWyGjhx0.txt (scoped search no AFDE/BFD/perimeter12 target solution)'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG equilateral subtriangle and parallelogram side recombination with exact two-versus-three unit bars','answerCheckedAgainst':'BFD正三角BF=DF，平四AE=DF→AF+AE=AF+BF=AB，四周長12=2AB→AB6，正三角周長18，A。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-220.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
