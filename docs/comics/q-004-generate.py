from pathlib import Path
import math,json,hashlib
w=1+math.sqrt(2);A=(0,1);B=(0,0);C=(w,0);D=(w,1);O=(w/2,.5);t=1/(w*w+1);E=(t*w,t);P=dict(A=A,B=B,C=C,D=D,O=O,E=E)
def angle(a,b,c):
 u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);return math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(u,v))/math.hypot(*u)/math.hypot(*v)))))
angles={n:angle(*[P[z] for z in n]) for n in ['BAE','DAE','ADB','DAC','EAC','AED']}
for n,v in [('BAE',22.5),('DAE',67.5),('ADB',22.5),('DAC',22.5),('EAC',45),('AED',90)]:assert math.isclose(angles[n],v)
assert math.isclose(math.dist(A,O),math.dist(D,O))
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=9,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{col}">{t}</text>')
 def line(a,b,col='#7e988a',ww=1.8):s.append(f'<path d="M{o+a[0]} {a[1]}L{o+b[0]} {b[1]}" fill="none" stroke="{col}" stroke-width="{ww}"/>')
 def arc(r,a,b,col):
  point=lambda d:(o+30+r*math.cos(math.radians(d)),42+r*math.sin(math.radians(d)))
  aa,bb=point(a),point(b);s.append(f'<path d="M{aa[0]} {aa[1]}A{r} {r} 0 0 1 {bb[0]} {bb[1]}" fill="none" stroke="{col}" stroke-width="1.3"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="Arial,sans-serif">')
 txt(90,18,['放大A角：三份＋一份＝90°','對角線等長平分：OA＝OD','AC在DAE內，所以相減'][i],9)
 if i!=1:
  line((30,42),(150,42));line((30,42),(68.268,134.388),'#b08b4f',2);txt(20,40,'A');txt(157,45,'D');txt(74,146,'E')
  if i==0:
   line((30,42),(30,146));txt(24,157,'B');arc(40,0,67.5,'#b08b4f');arc(74,67.5,90,'#7196a2');txt(86,80,'67.5°',10);txt(47,132,'22.5°',9);txt(90,174,'∠BAE＝22.5°',10)
  else:
   line((30,42),(137.17,86.39),'#7196a2',2);txt(146,95,'C');arc(40,0,22.5,'#7196a2');arc(65,22.5,67.5,'#b08b4f');txt(93,59,'22.5°',9);txt(98,105,'45°',11);txt(90,174,'67.5°−22.5°＝45°',10)
 else:
  pp=lambda v:(27+52*v[0],62+52*(1-v[1]));rr={z:pp(v) for z,v in P.items()}
  s.append('<polygon points="'+' '.join(f'{o+rr[z][0]},{rr[z][1]}' for z in ['A','O','D'])+'" fill="#d7e4c9"/>')
  for a,b in [('A','B'),('B','C'),('C','D'),('D','A'),('A','C'),('B','D')]:line(rr[a],rr[b])
  line(rr['A'],rr['E'],'#b08b4f',1.6)
  ee=rr['E']; ua=(rr['A'][0]-ee[0],rr['A'][1]-ee[1]); va=(rr['D'][0]-ee[0],rr['D'][1]-ee[1]); ul=math.hypot(*ua); vl=math.hypot(*va); u=(4*ua[0]/ul,4*ua[1]/ul); v=(4*va[0]/vl,4*va[1]/vl); line((ee[0]+u[0],ee[1]+u[1]),(ee[0]+u[0]+v[0],ee[1]+u[1]+v[1]),'#b08b4f',.8); line((ee[0]+u[0]+v[0],ee[1]+u[1]+v[1]),(ee[0]+v[0],ee[1]+v[1]),'#b08b4f',.8)
  for a,b in [('A','O'),('O','D')]:
   aa,bb=rr[a],rr[b];mx,my=(aa[0]+bb[0])/2,(aa[1]+bb[1])/2;dx,dy=bb[0]-aa[0],bb[1]-aa[1];l=math.hypot(dx,dy);line((mx-3*dy/l,my+3*dx/l),(mx+3*dy/l,my-3*dx/l),'#7196a2',1.4)
  for z in P:
   xx,yy=rr[z];dx,dy={'A':(-8,-6),'B':(-6,13),'C':(7,13),'D':(7,-6),'O':(4,14),'E':(-7,12)}[z];txt(xx+dx,yy+dy,z,8)
  txt(90,150,'∠ADB＝90°−67.5°',10);txt(90,171,'∠DAC＝∠ADB＝22.5°',9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-004.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-004-geometry-validation.json').write_text(json.dumps({'canonicalCoordinates':P,'rectangleRatio':w,'computedAngles':angles,'OA':math.dist(A,O),'OD':math.dist(D,O),'rayOrderFromAD':['AD','AC','AE','AB'],'newRaysEnlargedButSameAngles':True,'answer':45},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-004','subject':'Math','title':'先分直角，再用對角線，最後相減','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-004-generate.py','startedAt':'2026-10-29T05:10:15.546435+00:00','panels':[{'heading':'① 90°分成三份與一份','text':'∠BAD＝90°，而∠DAE＝3∠BAE，所以4∠BAE＝90°。得∠BAE＝22.5°，∠DAE＝67.5°；圖中先放大A角看清楚這兩部分。','alt':'A角局部精確射線AD/AE/AB，67.5與22.5合90；沒有把紙上任意量角當條件。'},{'heading':'② OA＝OD，對應兩個底角相等','text':'AE⊥BD，故∠ADB＝90°−67.5°＝22.5°。對角線交於O；矩形對角線等長且互相平分，所以OA＝OD。△AOD等腰，得∠DAC＝∠ADB＝22.5°。','alt':'精確矩形全圖，對角線交O、AE垂足E，三角形AOD底角相等；OA與OD等長刻痕，不泛稱所有對角線段皆相等。'},{'heading':'③ 依射線順序，從大角扣小角','text':'AC位在∠DAE內，∠DAE由∠DAC與∠CAE組成。因此∠EAC＝∠DAE−∠DAC＝67.5°−22.5°＝45°；不是把兩個角直接相加。','alt':'局部放大AD/AC/AE三射線，AC位於DAE內；先22.5後45兩段，總67.5，符合原圖。'}],'fourth':{'answer':'答案：∠EAC＝45°','points':['直角按3：1分，得到22.5°與67.5°。','矩形對角線等長且平分，推出∠DAC＝22.5°。','∠EAC＝67.5°−22.5°，由圖中射線順序決定。']},'protectedWords':['∠BAD＝90°','∠BAE＝22.5°','∠DAE＝67.5°','OA＝OD','△AOD','∠DAC','∠ADB','∠EAC＝45°','67.5°−22.5°＝45°','22.5°','67.5°','3：1'],'rationale':'使用者已確認第19題原圖/45度，親見對話照片與given渲染；新精確SVG局部放大A角及合法矩形全圖，獨立6角/等長半對角線/垂足/射線順序核定，無人物或來源AI。','promptSummary':'三格原生幾何：A直角分3:1；矩形對角線交O等腰AOD；AC在DAE內的角差67.5−22.5。','answerCheckedAgainst':'使用者提供第19原圖與確認解法；真坐標矩形寬1+√2、高1、E為正射影，6角獨立算得45。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'userProvidedOriginalInConversation':True,'existingFiguresActuallyRendered':['site/dist/assets/questions/q-004-given.svg'],'visualChecked':True,'answer':'45°','notes':'使用者本對話第19照片已確認，E在BD上，AC位於DAE內；本機given已實際渲染實看，未偽稱有獨立原卷檔。'},'geometryValidation':'docs/comics/q-004-geometry-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-004.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
