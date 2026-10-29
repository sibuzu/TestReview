from pathlib import Path
import math,json,hashlib
L=math.sqrt(10);A=(1,3);B=(0,0);C=(5,0);D=(6,3);E=(L,0);F=(5-L,0)
u=(E[0]-A[0],-3);v=(F[0]-D[0],-3);cross=lambda a,b:a[0]*b[1]-a[1]*b[0];t=cross((D[0]-A[0],0),v)/cross(u,v);G=(A[0]+t*u[0],A[1]+t*u[1]);P=dict(A=A,B=B,C=C,D=D,E=E,F=F,G=G)
def ang(a,b,c):
 z=(a[0]-b[0],a[1]-b[1]);w=(c[0]-b[0],c[1]-b[1]);return math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(z,w))/math.hypot(*z)/math.hypot(*w)))))
alpha=ang(D,A,E);beta=ang(A,D,F)
assert math.isclose(alpha,ang(E,A,B)) and math.isclose(beta,ang(F,D,C)) and math.isclose(alpha+beta,90)
assert math.isclose(sum(x*y for x,y in zip(u,v)),0,abs_tol=1e-10)
d=lambda a,b:math.dist(P[a],P[b]);assert math.isclose(d('B','E'),d('A','B')) and math.isclose(d('C','F'),d('C','D')) and math.isclose(d('B','F'),d('C','E'))
assert B[0]<F[0]<E[0]<C[0]
bisectorDot=sum(x*y for x,y in zip(u,v))
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=9,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def line(a,b,col='#8b9f90',w=1.8,dash=''):s.append(f'<path d="M{o+a[0]} {a[1]}L{o+b[0]} {b[1]}" fill="none" stroke="{col}" stroke-width="{w}" {dash}/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="Arial,sans-serif">')
 txt(90,20,['鄰角互補，半角之和90°','兩個等腰三角形，換出等長','B、F、E、C：扣同一段FE'][i],9)
 if i<2:
  pp=lambda v:(20+24*v[0],122-24*v[1]);R={z:pp(p) for z,p in P.items()}
  if i==1:
   for ns,col in [('ABE','#dbe9cf'),('DCF','#cbdde7')]:s.append('<polygon points="'+' '.join(f'{o+R[z][0]},{R[z][1]}' for z in ns)+f'" fill="{col}" opacity=".75"/>')
  for a,b in [('A','B'),('B','C'),('C','D'),('D','A'),('A','E'),('D','F')]:line(R[a],R[b])
  if i==0:
   gg=R['G'];a=R['A'];dd=R['D'];ua=(a[0]-gg[0],a[1]-gg[1]);va=(dd[0]-gg[0],dd[1]-gg[1]);ul=math.hypot(*ua);vl=math.hypot(*va);uu=(4*ua[0]/ul,4*ua[1]/ul);vv=(4*va[0]/vl,4*va[1]/vl);line((gg[0]+uu[0],gg[1]+uu[1]),(gg[0]+uu[0]+vv[0],gg[1]+uu[1]+vv[1]),'#b38b4f',1);line((gg[0]+uu[0]+vv[0],gg[1]+uu[1]+vv[1]),(gg[0]+vv[0],gg[1]+vv[1]),'#b38b4f',1)
   txt(62,66,'α',11);txt(140,62,'β',11)
   txt(90,153,'α＋β＝½×180°＝90°',10);txt(90,174,'∠AGD＝90°',10)
  else:
   for a,b,col,n in [('A','B','#81a25f',1),('B','E','#81a25f',1),('C','D','#608faa',2),('C','F','#608faa',2)]:
    line(R[a],R[b],col,2.3);aa,bb=R[a],R[b]; dx,dy=bb[0]-aa[0],bb[1]-aa[1]; ll=math.hypot(dx,dy)
    for offset in ([0] if n==1 else [-2,2]):
     xx=(aa[0]+bb[0])/2+offset*dx/ll;yy=(aa[1]+bb[1])/2+offset*dy/ll;line((xx-3*dy/ll,yy+3*dx/ll),(xx+3*dy/ll,yy-3*dx/ll),col,1.2)
   txt(90,153,'BE＝AB；CF＝CD',10);txt(90,174,'AB＝CD ⇒ BE＝CF',10)
  for z in P:
   if z=='G' and i==1:continue
   xx,yy=R[z];dx,dy={'A':(-7,-5),'B':(-7,12),'C':(7,12),'D':(6,-5),'E':(0,12),'F':(0,12),'G':(0,13)}[z];txt(xx+dx,yy+dy,z,8)
 else:
  bx=lambda v:24+25*v
  for v,z in [(0,'B'),(F[0],'F'),(E[0],'E'),(5,'C')]:
   txt(bx(v),43,z,9);line((bx(v),49),(bx(v),123),'#b5bbae',.7,'stroke-dasharray="2 3"')
  for aa,bb,col,y in [(0,F[0],'#81a25f',73),(F[0],E[0],'#acb6ae',73),(F[0],E[0],'#acb6ae',108),(E[0],5,'#81a25f',108)]:line((bx(aa),y),(bx(bb),y),col,5)
  txt(165,76,'BE',9);txt(165,111,'CF',9);txt((bx(F[0])+bx(E[0]))/2,94,'FE',9)
  txt(90,150,'BE−FE＝CF−FE',10);txt(90,174,'BF＝CE',11)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-007.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-007-geometry-validation.json').write_text(json.dumps({'canonicalCoordinates':P,'alpha':alpha,'beta':beta,'halfAdjacentSum':alpha+beta,'bothBisectorsChecked':True,'dotAE_DF':bisectorDot,'BE':d('B','E'),'AB':d('A','B'),'CF':d('C','F'),'CD':d('C','D'),'BF':d('B','F'),'CE':d('C','E'),'strictBCPointOrder':['B','F','E','C'],'note':'合法例只供精確示意，不把3、5、sqrt10或具體角值新增為原題條件。證明在HTML為一般形式。'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-007','subject':'Math','title':'鄰角平分得垂直，等腰換長再扣公共段','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-007-generate.py','startedAt':'2026-10-29T05:12:49.674211+00:00','panels':[{'heading':'① 兩個鄰角互補，半角合90°','text':'設∠DAE＝α、∠ADF＝β。因∠BAD＋∠ADC＝180°，而AE、DF平分這兩角，所以α＋β＝90°。在△AGD中，∠AGD＝180°−90°＝90°，故AE⊥DF。','alt':'合法平行四邊形中兩角平分線交G，A/D半角αβ及G直角記號，點序沿使用者原圖。'},{'heading':'② 用平行線找出兩個等腰三角形','text':'AD∥BC，配合角平分線，得∠BAE＝∠AEB，故BE＝AB；同理∠CDF＝∠DFC，故CF＝CD。再由對邊AB＝CD，得到BE＝CF。','alt':'兩個等腰三角形ABE/DCF異色，同色及單/雙刻痕分辨BE/AB、CF/CD，不暗示兩三角形必須全等。'},{'heading':'③ BE與CF都扣掉同一段FE','text':'依原圖B、F、E、C的順序，BE＝BF＋FE，CF＝CE＋FE。既然BE＝CF，兩邊同減FE，就得到BF＝CE。灰段FE是同一條公共線段，兩端剩餘綠段才是所求。','alt':'B/F/E/C位置共線，兩條等長BE/CF上下對齊，重疊FE灰色，左右剩餘BF/CE同色等長；不假設F/E為中點。'}],'fourth':{'answer':'得證：AE⊥DF；BF＝CE','points':['鄰角互補，兩個半角之和90°。','兩個等腰三角形，把BE、CF換成相等的兩腰。','BE＝CF後扣掉公共FE，得到BF＝CE。']},'protectedWords':['∠DAE＝α','∠ADF＝β','α＋β＝90°','△AGD','∠AGD','AE⊥DF','AD∥BC','BE＝AB','CF＝CD','AB＝CD','BE＝CF','BF＝CE','B、F、E、C','BE＝BF＋FE','CF＝CE＋FE','90°','180°−90°＝90°'],'rationale':'使用者第16照片與完整證明已確認，親見本對話原圖及given渲染。新精確SVG以αβ互補/兩等腰換長/共同灰段扣除三個證明節點呈現；一般證明不依賴示例數值，不用人物或來源AI。','promptSummary':'原生三格：合法平行四邊形兩角平分線垂直；兩等腰三角形同色邊；點序BFE C的重疊線段視覺減法。','answerCheckedAgainst':'使用者已確認16題原卷/證明；一般鄰角角平分與內錯角等腰、對邊相等及公共FE減法，另用真坐標核實兩平分/垂直/三組等長/點序。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'userProvidedOriginalInConversation':True,'existingFiguresActuallyRendered':['site/dist/assets/questions/q-007-given.svg'],'visualChecked':True,'answer':'AE⊥DF；BF＝CE','notes':'使用者原卷16圖B-F-E-C順序與G交點已確認，given實際渲染吻合。無原卷檔不偽稱images；新構造具體尺寸僅驗算不列學習者題目條件。'},'geometryValidation':'docs/comics/q-007-geometry-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-007.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
