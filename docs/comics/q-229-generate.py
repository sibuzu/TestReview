from pathlib import Path
import json,math,hashlib
A=(9,12);B=(0,0);C=(30,0);D=(21,12);E=(9,0);F=(21,0)
P={'A':A,'B':B,'C':C,'D':D,'E':E,'F':F}
side=lambda a,b: math.dist(P[a],P[b])
checks={'AE':side('A','E'),'EF':side('E','F'),'FD':side('F','D'),'AD':side('A','D'),'AB':side('A','B'),'CD':side('C','D'),'BF':side('B','F'),'BE':side('B','E'),'CF':side('C','F'),'BC':side('B','C')}
assert all(math.isclose(checks[z],12) for z in ['AE','EF','FD','AD'])
assert checks['AB']==checks['CD'] and checks['BF']==2*checks['AE']-3
assert checks['CF']*checks['FD']/2==54 and checks['BC']==30
assert (12-12)*(12+9)==0 and (-9-12)*(-9+9)==0
assert all((x*x-3*x-108)==(x-12)*(x+9) for x in [-10,-9,0,12,20])
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def p(v): return (o+22+4.5*v[0],109-4.5*v[1])
 def line(a,b,col='#8fa18d',w=1.7):
  aa,bb=p(P[a]),p(P[b]);s.append(f'<path d="M{aa[0]} {aa[1]}L{bb[0]} {bb[1]}" stroke="{col}" stroke-width="{w}" fill="none"/>')
 def txt(x,y,t,size=9,col='#244b50',anchor='middle'):s.append(f'<text x="{o+x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{col}">{t}</text>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/>')
 s.append('<g font-family="Arial, sans-serif">')
 txt(90,22,['先認出相等的底邊兩端','以直角三角形面積列式','整條BC是三段相加'][i],10)
 poly=lambda names:' '.join(f'{p(P[z])[0]},{p(P[z])[1]}' for z in names)
 s.append(f'<polygon points="{poly("ABCD")}" fill="#fbfcf8" stroke="#8fa18d" stroke-width="1.6"/>')
 if i==0:s.append(f'<polygon points="{poly("ABED")}" fill="none"/>')
 if i==1:s.append(f'<polygon points="{poly("DCF")}" fill="#d6dfc0"/>')
 if i==2:
  for aa,bb,col in [('B','E','#b49253'),('E','F','#759ca4'),('F','C','#b49253')]:line(aa,bb,col,3.5)
 for aa,bb in [('A','E'),('D','F')]:line(aa,bb)
 for z in ['E','F']:
  x,y=p(P[z]);s.append(f'<path d="M{x} {y-5}h5v5" fill="none" stroke="#8fa18d" stroke-width=".8"/>')
 for z in P:
  x,y=p(P[z]); dx,dy={'A':(-3,-7),'B':(-7,7),'C':(8,7),'D':(3,-7),'E':(0,13),'F':(0,13)}[z]
  s.append(f'<text x="{x+dx}" y="{y+dy}" font-size="8" text-anchor="middle" fill="#244b50">{z}</text>')
 if i==0:
  txt(54,86,'x');txt(89,100,'正方形',9)
  for xx,t in [(42,'x−3'),(89,'x'),(137,'x−3')]:txt(xx,135,t,9)
  s.append(f'<path d="M{o+22} 143v4h94.5v-4" fill="none" stroke="#6f9195"/>')
  txt(69,162,'BF＝2x−3',11)
 elif i==1:
  txt(108,85,'x');txt(134,101,'54',10);txt(138,135,'x−3',10)
  txt(90,155,'½ × x(x−3)＝54',11);txt(90,173,'(x−12)(x＋9)＝0',10)
 else:
  for xx,t in [(42,'9'),(89,'12'),(137,'9')]:txt(xx,135,t,11)
  s.append(f'<path d="M{o+22} 145v5h135v-5" fill="none" stroke="#6f9195"/>')
  txt(90,170,'BC＝9＋12＋9＝30',11)
 s.append('</g>')
s.append('</svg>')
art='docs/comics/art/q-229.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-229-geometry-validation.json').write_text(json.dumps({'checkedLengths':checks,'canonicalCoordinates':P,'rightTriangleArea':54,'squareEdgesEqual':True,'equalLegs':True,'quadraticFactoringCheckedAtFiveValues':True,'roots':[12,-9],'positiveRoot':12,'finalBC':30,'note':'同一精確30x12合法等腰梯形三格共用；非來源圖，不用圖形相似當等腰結論。'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-229','subject':'Math','title':'BF還不是BC：正方形邊長算出後，再加右段','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-229-generate.py','startedAt':'2026-10-29T05:02:15.791776+00:00','panels':[{'heading':'① 設正方形邊長x，兩端各是x−3','text':'正方形的AE＝EF＝FD＝AD＝x。BF＝2x−3，扣掉EF＝x，得BE＝x−3。等腰梯形兩腰相等，兩側直角三角形斜邊相等、高也相等，故全等，CF＝BE＝x−3。','alt':'精確等腰梯形內接正方形，底邊分成x−3、x、x−3，以下括線單獨指出BF並非BC。'},{'heading':'② 面積54，列出x的方程式','text':'△CDF的底CF＝x−3、高DF＝x，所以½×x(x−3)＝54。整理得x²−3x−108＝0，即(x−12)(x＋9)＝0；邊長須為正，取x＝12。','alt':'同一等腰梯形右側直角三角形上色，底x−3及高x對應面積54，無不相干人物。'},{'heading':'③ 把BE、EF、FC三段都算入','text':'x＝12，所以BE＝CF＝9、EF＝12。BC＝BE＋EF＋FC＝9＋12＋9＝30公分。若只算BF＝2×12−3＝21，仍少了右端CF＝9。','alt':'三段底邊上色，左右各9，中間12，全長括線為30；仍沿同一12高30底精確座標。'}],'fourth':{'answer':'答案：BC＝30公分','points':['BE＝CF＝x−3，先用兩側全等找出右段。','54＝½×x(x−3)，取正根x＝12。','題目問BC，不是BF；21＋9＝30。']},'protectedWords':['BF','BC','BE','CF','x−3','2x−3','½×x(x−3)＝54','x²−3x−108＝0','(x−12)(x＋9)＝0','x＝12','CF＝9','BE＋EF＋FC'],'rationale':'親見原卷全文及必要given實際渲染，標準30與獨立代數/坐標核對一致。新精確SVG將BF/BC範圍、等腰兩端、面積與三段相加具象化；不使用人物、來源AI或重製題圖。','promptSummary':'三格同一精確等腰梯形：設x和BF括線；右三角面積54；底邊9+12+9，以HTML解全等/方程式。','answerCheckedAgainst':'原卷BF比AE2倍少3、△CDF54及求BC；獨立解x12/BE9/CF9/BC30，正負根與平方等腰坐標皆驗證。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-229-source-c019052cbe.jpg'],'existingFiguresActuallyRendered':['site/dist/assets/questions/q-229-given.svg'],'visualChecked':True,'answer':'30公分','notes':'親見原卷完整題幹與小圖及given渲染，x12圖合題意；BF21是部分底邊，不誤作BC。'},'geometryValidation':'docs/comics/q-229-geometry-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-229.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
