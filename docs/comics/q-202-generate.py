import math,json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
L=120;A=(90,43);E=(210,43);C=(150,43+60*math.sqrt(3));B=(90-60*4/9,43+60*math.sqrt(3)*4/9);D=(210+60*5/9,43+60*math.sqrt(3)*5/9)
P=dict(A=A,B=B,C=C,D=D,E=E)
def poly(ps,fill,stroke='#7d8a80',width=2):return '<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
def line(a,b,c,w=3,dash=''):return f'<path d="M{a[0]:.3f} {a[1]:.3f}L{b[0]:.3f} {b[1]:.3f}" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def txt(x,y,s,size=18,c='#314e3d'):return f'<text x="{x:.3f}" y="{y:.3f}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" fill="{c}">{escape(s)}</text>'
def cent(ps):return tuple(sum(p[i] for p in ps)/len(ps) for i in range(2))
s=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300">']
for i in range(3):
 s.append(f'<g transform="translate({i*300},0)"><rect width="300" height="300" fill="#faf8ee"/>')
 if i<2:
  # geometry is translated lower; all points remain exact equilateral and proportional
  s.append('<g transform="translate(0,37)">');s.append(poly([A,B,C,D,E],'none'))
  s.append(poly([A,C,E],'#e7efd9'))
  if i==0:
   s.append(poly([A,B,C],'#dae8f3'));s.extend([line(A,B,'#547fa0',5),line(C,E,'#547fa0',5)])
   H=(60,43+30*math.sqrt(3));s.extend([line(A,(51,43+39*math.sqrt(3)),'#547fa0',1,'4 3'),line(C,H,'#ad7553',2,'5 3')]);s.append(txt(110,130,'h',19,'#ad7553'))
   s.append(txt(*cent([A,B,C]),'12',18));s.append(txt(*cent([A,C,E]),'27',18))
  else:
   s.append(poly([C,D,E],'#f2e2d0'));s.extend([line(A,C,'#b78144',5),line(D,E,'#b78144',5)])
   H=(240,43+30*math.sqrt(3));s.append(line(C,H,'#5a86a7',2,'5 3'));s.append(txt(199,130,'h',19,'#5a86a7'))
   s.append(txt(*cent([A,C,E]),'27',18));s.append(txt(*cent([C,D,E]),'15',18))
  for n,dx,dy in [('A',-9,-13),('B',-15,0),('C',0,19),('D',17,0),('E',8,-13)]:
   p=P[n];s.append(txt(p[0]+dx,p[1]+dy,n,19))
  s.append('</g>')
  s.append(txt(150,26,'AB ∥ CE' if i==0 else 'AC ∥ DE',23))
  s.append(txt(150,231,'AB : CE＝12 : 27' if i==0 else 'AC : DE＝27 : 15',20))
  s.append(txt(150,267,'AB : AE＝4 : 9' if i==0 else 'AE : DE＝9 : 5',21,'#367c56'))
 else:
  s.append(txt(150,28,'AE : AB : DE＝9 : 4 : 5',18))
  for y,label,n,c in [(77,'AE',9,'#83ac73'),(137,'2AB',8,'#7c9fb8'),(197,'2DE',10,'#c39d69')]:
   s.append(txt(31,y+13,label,18));s.append(f'<rect x="66" y="{y}" width="{n*18}" height="26" fill="{c}"/>')
   for j in range(n+1):s.append(line((66+j*18,y),(66+j*18,y+26),'#fff7e8',1))
   s.append(txt(66+n*18+13,y+13,str(n),17))
  s.append(txt(150,266,'8 ＜ 9 ＜ 10',25,'#367c56'))
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-202.svg').write_text(''.join(s))
area=lambda a,b,c:abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
scale=27/area(A,C,E)
areas=[area(A,B,C)*scale,area(A,C,E)*scale,area(C,D,E)*scale]
assert all(abs(a-b)<1e-8 for a,b in zip(areas,[12,27,15]))
assert abs(math.dist(A,B)/math.dist(A,E)-4/9)<1e-9 and abs(math.dist(D,E)/math.dist(A,E)-5/9)<1e-9
assert math.dist(A,E)>2*math.dist(A,B) and math.dist(A,E)<2*math.dist(D,E)
Path('docs/comics/q-202-geometry-validation.json').write_text(json.dumps({'id':'q-202','pass':True,'coordinatesSVG':P,'areaScaleFactorForActualUnits':scale,'triangleAreas':[12,27,15],'computedAreas':areas,'lengthRatiosAB_AE_DE':[4,9,5],'doubleLengthsComparison':[8,9,10],'answer':'B','sourceActuallyViewed':True,'allThreePrintedOptionsChecked':True},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-202','subject':'Math','title':'共高先比底，兩倍再比份數','art':'docs/comics/art/q-202.svg','protectedWords':['共高','面積比','底邊比','正三角形','△ABC','△ACE','△CDE','AB∥CE','AC∥DE','AE＞2AB','AE＜2DE','4：9','9：5','8＜9＜10'],'panels':[{'heading':'① AB與CE平行，兩三角形共高','text':'△ABC以AB為底，△ACE以CE為底，高都是兩條平行線的距離。面積比等於底邊比，AB：CE＝12：27＝4：9；正三角形給出CE＝AE。','alt':'精確五邊形左側三角形面積12、中央正三角形27，AB與CE同藍色；虛線h是兩平行線距離，AB延長線保留。'},{'heading':'② 換另一組底邊，比AC與DE','text':'AC∥DE，△ACE以AC為底，△CDE以DE為底，也有共同的高。AC：DE＝27：15＝9：5。再用AC＝AE，就得AE：DE＝9：5。','alt':'中央正三角形面積27、右側三角形15，平行底AC與DE橘色，h垂直兩底；不把斜邊直接當高。'},{'heading':'③ 同一套份數，再比較兩倍邊長','text':'可統一看成AE有9份、AB有4份、DE有5份。因此2AB有8份，2DE有10份，8＜9＜10，所以AE＞2AB、AE＜2DE。','alt':'精確同單位條：AE九份、2AB八份、2DE十份，條長與每一等份完全一致；不是面積條。'}],'fourth':{'answer':'答案 B：AE＞2AB，AE＜2DE','points':['共高三角形：面積比＝底邊比。','用正三角形三邊相等，把CE、AC換成AE。','統一份數後，8＜9＜10直接比較。']},'rationale':'實看原卷第6題全部三個印刷選項與必要圖；讀來源完整相關段落。按兩組平行線建立實際正三角形及外接兩三角形，標示面積12/27/15。獨立座標面積與邊長比例驗算，9/4大於2、9/5小於2，B不變。新製精確SVG，不沿用來源AI圖，不補造不存在的D選項。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-202-source-cdf1801efa.jpg','site/dist/sources/gemini-GD2msWyGjhx0.txt lines 1120–1280'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG equal-height triangles and same-unit ratio bars','answerCheckedAgainst':'獨立座標areaABC:ACE:CDE=12:27:15，AB:AE:DE=4:9:5，2AB:AE:2DE=8:9:10；B。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-202.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
