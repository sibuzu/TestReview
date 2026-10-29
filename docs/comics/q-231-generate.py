from pathlib import Path
import json,math,hashlib
P=(6,8);Q=(14,0);H=(6,0);left=[(0,8),(0,0),Q,P];right=[(20,8),P,Q,(20,0)]
rot=lambda v:(20-v[0],8-v[1])
assert set(map(rot,left))==set(right)
angle=math.degrees(math.acos(8/math.hypot(8,8)))
assert math.isclose(angle,45) and Q[0]-P[0]==8 and P[1]-H[1]==8
assert 20-2*6==8
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def p(v):return(o+27+6*v[0],112-6*v[1])
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{col}">{t}</text>')
 def line(a,b,col='#7f9988',w=1.5,dash=''):
  aa,bb=p(a),p(b);s.append(f'<path d="M{aa[0]},{aa[1]}L{bb[0]},{bb[1]}" fill="none" stroke="{col}" stroke-width="{w}" {dash}/>')
 def poly(vs,col):s.append(f'<polygon points="'+ ' '.join(f'{p(v)[0]},{p(v)[1]}' for v in vs)+f'" fill="{col}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="Arial, sans-serif">')
 txt(90,23,['全等：短底x，長底20−x','45°讓水平差也等於8','長底14，短底6'][i],10)
 poly(left,'#dce9d0');poly(right,'#f4e0bc')
 for a,b in zip([(0,8),(0,0),(20,0),(20,8)],[(0,0),(20,0),(20,8),(0,8)]):line(a,b)
 line(P,Q,'#5b8599',1.7,'stroke-dasharray="3 2"')
 txt(87,48,'20',10);txt(158,91,'8',10)
 if i==0:
  txt(45,59,'x',10);txt(105,59,'20−x',10);txt(69,129,'20−x',10);txt(129,129,'x',10)
  txt(90,158,'同一片：長底 − 短底',10)
 elif i==1:
  poly([P,H,Q],'#b9cddc');line(P,H,'#5b8599',1.7);line(H,Q,'#5b8599',2)
  for v,dx,dy,t in [(P,-6,-5,'P'),(H,-7,9,'H'),(Q,8,9,'Q')]:
   xx,yy=p(v);s.append(f'<text x="{xx+dx}" y="{yy+dy}" font-size="8" fill="#244b50">{t}</text>')
  x,y=p(H);s.append(f'<path d="M{x} {y-5}h5v5" fill="none" stroke="#5b8599" stroke-width=".8"/>')
  txt(56,90,'8',10);txt(87,131,'8',10)
  x,y=p(Q);r=22;s.append(f'<path d="M{x-r} {y}A{r} {r} 0 0 1 {x-r/math.sqrt(2)} {y-r/math.sqrt(2)}" fill="none" stroke="#af804b"/>')
  txt(90,105,'45°',8)
  txt(90,155,'水平差＝長底−短底＝8',10)
 else:
  txt(45,59,'6',11);txt(105,59,'14',11);txt(69,129,'14',11);txt(129,129,'6',11)
  txt(90,155,'14＋6＝20',11);txt(90,173,'14−6＝8',11)
 s.append('</g>')
s.append('</svg>'); art='docs/comics/art/q-231.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-231-geometry-validation.json').write_text(json.dumps({'P':P,'Q':Q,'H':H,'rectangle':[20,8],'horizontalDifference':8,'verticalDifference':8,'cutAngleFromLeftwardBase':angle,'rotationAboutCenterMapsPieces':True,'rotationCenter':[10,4],'shortBase':6,'longBase':14,'sum':20,'difference':8,'independentCheck':'180度旋轉逐頂點映射兩梯形；45度用真坐標餘弦核對，長短底和差同時核對。'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-231','subject':'Math','title':'短底用x，長底用20−x，再看45°','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-231-generate.py','startedAt':'2026-10-29T05:04:12.317659+00:00','panels':[{'heading':'① 全等的兩片，長短底互相對應','text':'設較短的底為x，較長的底為20−x。兩片全等，所以短底相等、長底也相等；上、下整條邊都是20，恰好各由一段長底和一段短底組成。','alt':'同一20x8矩形兩梯形異色，剪線上端左段x、右段20−x，下端左段20−x、右段x。'},{'heading':'② 從上端作垂線，找水平差','text':'另將剪線上端標P、下端標Q，過P向下底作垂線PH。PH＝8，∠PQH＝45°，所以△PHQ是等腰直角三角形，HQ＝8；這段水平差正是長底減短底。','alt':'完整矩形中加入P/H/Q和精確45度弧，垂直8與水平8形成直角三角形，不把剪線長當8。'},{'heading':'③ 利用長短底相差8，解出x','text':'(20−x)−x＝8，得20−2x＝8，所以x＝6。另一條底是14；檢查14＋6＝20、14−6＝8，兩個條件都符合。','alt':'同一矩形兩片底邊依序標6和14，長短底和20、差8雙重核對；角度和原圖方向一致。'}],'fourth':{'answer':'答案：較短的底邊長6','points':['兩片全等，長底與短底合起來是20。','45°配高度8，得到水平差8。','長底減短底為8，而不是剪線長等於8。']},'protectedWords':['20−x','長底','短底','PH＝8','HQ＝8','∠PQH＝45°','△PHQ','(20−x)−x＝8','20−2x＝8','x＝6','14＋6＝20','14−6＝8'],'rationale':'親見原卷及必要given渲染；新精確SVG以全等對應、垂線等腰直角、長短底和差三步解6。獨立180度旋轉映射頂點/坐標角度驗證；不以圖形猜中點，不將斜邊誤當8。','promptSummary':'精確20x8矩形剪線從(6,8)到(14,0)，三格依序對應長短底、作垂線形成45度直角三角形、標6與14驗算。','answerCheckedAgainst':'原卷矩形20/8及剪線下端左向45度、全等條件；獨立長短底6/14、旋轉全等和真45度坐標核對。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-231-source-249b6cead8.jpg'],'existingFiguresActuallyRendered':['site/dist/assets/questions/q-231-given.svg'],'visualChecked':True,'answer':'6','notes':'親見20、8、剪線與下底左向45度及完整題幹，given方向一致。P/Q/H明確為新輔助點而非偽稱原卷標名。'},'geometryValidation':'docs/comics/q-231-geometry-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-231.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
