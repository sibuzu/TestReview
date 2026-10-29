from pathlib import Path
import json,math,hashlib
x=(math.sqrt(3)-1)/2;P={'A':(0,1),'B':(0,0),'C':(1,0),'D':(1,1),'E':(x,1+x),'F':(0,1+x)}
dist=lambda a,b:math.dist(P[a],P[b]);AE=dist('A','E')
assert math.isclose(dist('B','E'),dist('B','D')) and math.isclose(dist('B','E'),math.sqrt(2))
assert P['E'][0]-P['A'][0]==P['E'][1]-P['A'][1] and P['D'][0]-P['B'][0]==P['D'][1]-P['B'][1]
assert math.isclose(dist('A','F'),dist('E','F')) and math.isclose(AE,(math.sqrt(6)-math.sqrt(2))/2)
assert math.isclose(x*x+(1+x)**2,2) and x>0
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def p(v):return(o+51+82*v[0],146-82*v[1])
 def txt(xx,y,t,size=9,col='#244b50'):s.append(f'<text x="{o+xx}" y="{y}" font-size="{size}" text-anchor="middle" fill="{col}">{t}</text>')
 def line(a,b,col='#8da18e',w=1.8,dash=''):
  aa,bb=p(P[a]),p(P[b]);s.append(f'<path d="M{aa[0]} {aa[1]}L{bb[0]} {bb[1]}" fill="none" stroke="{col}" stroke-width="{w}" {dash}/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="Arial,sans-serif">')
 txt(90,17,['E在正方形外，BE＝BD','向上延長BA，從E作垂線','大直角三角形：BF＝1＋x'][i],9)
 if i<2:
  for a,b in [('A','B'),('B','C'),('C','D'),('D','A')]:line(a,b)
  line('B','D','#799ea3',1.3,'stroke-dasharray="3 2"');line('A','E','#8aaa63',2);line('B','E','#b58a55',2)
  if i==1:
   line('A','F','#799ea3',1.5);line('F','E','#799ea3',1.5)
   xx,yy=p(P['F']);s.append(f'<path d="M{xx} {yy+5}h5v-5" fill="none" stroke="#799ea3" stroke-width=".8"/>')
   for xx,yy,t in [(38,52,'x'),(66,28,'x'),(38,111,'1')]:txt(xx,yy,t,9)
  else:
   txt(39,111,'1');txt(109,116,'√2',9);txt(79,107,'√2',9)
 else:
  line('B','F','#799ea3',2);line('F','E','#799ea3',2);line('E','B','#b58a55',2)
  xx,yy=p(P['F']);s.append(f'<path d="M{xx} {yy+5}h5v-5" fill="none" stroke="#799ea3" stroke-width=".8"/>')
  txt(37,96,'1＋x',10);txt(66,28,'x',9);txt(97,95,'√2',10)
 names=['A','B','C','D','E'] if i==0 else ['A','B','C','D','E','F'] if i==1 else ['B','E','F']
 for z in names:
  xx,yy=p(P[z]);dx,dy={'A':(-10,4),'B':(-7,12),'C':(8,12),'D':(8,4),'E':(8,-4),'F':(-9,-4)}[z];s.append(f'<text x="{xx+dx}" y="{yy+dy}" font-size="8" text-anchor="middle" fill="#244b50">{z}</text>')
 txt(90,175,['AE∥BD，都是斜向45°','AF＝EF＝x，AE＝√2x','x²＋(1＋x)²＝2'][i],10)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-003.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-003-geometry-validation.json').write_text(json.dumps({'canonicalCoordinates':P,'unitSquare':True,'EAboveAD':P['E'][1]>1,'parallelSlopes':[1,1],'BE':dist('B','E'),'BD':dist('B','D'),'AF':dist('A','F'),'EF':dist('E','F'),'BF':dist('B','F'),'xPositiveRoot':x,'negativeRoot':(-math.sqrt(3)-1)/2,'bigPythagoras':x*x+(1+x)**2,'AE':AE,'expectedAE':(math.sqrt(6)-math.sqrt(2))/2,'allChecksPassed':True},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-003','subject':'Math','title':'先算兩段x，再換回AE＝√2x','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-003-generate.py','startedAt':'2026-10-29T05:07:41.292037+00:00','panels':[{'heading':'① 正方形對角線給出BE＝√2','text':'AB＝1，所以BD²＝1²＋1²＝2，BD＝√2。又BE＝BD，故BE＝√2。E在AD上方的正方形外，不能把它放到正方形裡面計算。','alt':'新精確單位正方形外點E，AE平行BD，BE與BD標同長√2，位置沿使用者已確認原圖。'},{'heading':'② 作垂線，把AE拆成兩條相等段','text':'將BA向上延長，從E作垂線交於F。因AE∥BD，△AFE為45°等腰直角三角形。設AF＝EF＝x，則BF＝1＋x，而題目要求的AE＝√2x。','alt':'同一正方形向上延長BA至F，E垂足F，AF/EF皆x、AB1，F為直角，AE才是小三角形斜邊。'},{'heading':'③ 在△BFE用畢氏，再乘回√2','text':'x²＋(1＋x)²＝2，整理得2x²＋2x−1＝0。取正根x＝(√3−1)／2，再算AE＝√2x＝(√6−√2)／2；不要把AF的長度x直接當成AE。','alt':'抽出同一真坐標大直角三角形BFE，兩直角邊x/1+x、斜邊√2，與小等腰直角三角形區分。'}],'fourth':{'answer':'AE＝(√6−√2)／2','points':['大三角形BF＝1＋x，EF＝x，BE＝√2。','先得到AF＝x＝(√3−1)／2。','所求是小三角形斜邊AE，還要乘√2。']},'protectedWords':['BE＝√2','BD＝√2','BD²','△AFE','△BFE','AF＝EF＝x','BF＝1＋x','AE＝√2x','x²＋(1＋x)²＝2','2x²＋2x−1＝0','(√3−1)／2','(√6−√2)／2','AF','AE'],'rationale':'沿使用者已核對第17題原圖，親見對話原圖及given渲染，獨立合法坐標驗證E外部/平行/BE=BD/兩直角三角形與正根。新精確SVG特別分辨中間x與所求AE，不用人物、來源AI或重製原卷。','promptSummary':'真坐標三格：外點E與等長√2；BA延長到F的等腰直角AFE；抽出大直角BFE列x²+(1+x)²2，再乘√2回AE。','answerCheckedAgainst':'使用者提供原卷17圖與已確認AE∥BD、BE=BD、AB1，獨立坐標/兩次畢氏與正根求(√6−√2)/2。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'userProvidedOriginalInConversation':True,'existingFiguresActuallyRendered':['site/dist/assets/questions/q-003-given.svg'],'visualChecked':True,'answer':'(√6−√2)／2','notes':'原卷照片由使用者本對話提供，E在AD上方，已確認不重問；本機given已實際渲染看過，資料images空不偽稱另有原卷檔。'},'geometryValidation':'docs/comics/q-003-geometry-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-003.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
