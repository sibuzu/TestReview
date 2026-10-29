from pathlib import Path
import json,hashlib,math,xml.etree.ElementTree as ET
out=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><g font-family="Noto Sans CJK TC,sans-serif" fill="#234344" font-size="12">']
def line(a,b,color='#6d8583',width=1.7,dash=''):
 return f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}" fill="none" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def txt(x,y,t,size=12,color='#234344',anchor='middle'):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{t}</text>'
A=(20,30);B=(20,126);D=(148,30);C=(148,126);P=(96.8,68.4);E=(20,68.4);F=(96.8,30);H=(66.08,91.44)
def outer():return '<path d="M20 30H148V126H20Z" fill="none" stroke="#9eafab" stroke-width="1.5"/>'
def dot(p):return f'<circle cx="{p[0]}" cy="{p[1]}" r="2.3"/>'
for i,bg in enumerate(['#eef3e9','#edf1f7','#f5efdf']):
 out.append(f'<g transform="translate({180*i},0)"><path d="M0 0h180v180H0Z" fill="{bg}"/>')
 if i==0:
  out.append(outer());out.append('<path d="M20 30H96.8V68.4H20Z" fill="#d1dfc5" stroke="#55795f" stroke-width="2"/>');out.extend([line(B,D,dash='4 3'),line(A,P,'#527da2',2.7),line(E,F,'#b98745',2.7)])
  for p,label,x,y in [(A,'A',15,23),(B,'B',13,141),(D,'D',155,23),(C,'C',155,141),(P,'P',106,78),(E,'E',11,73),(F,'F',97,22)]:out.extend([dot(p),txt(x,y,label)])
  out.append(txt(87,163,'矩形對角線：EF＝AP',13))
 elif i==1:
  out.append(outer());out.extend([line(B,D,'#6d8583',2),line(A,(109.6,58.8),'#9eaab5',1.5,'4 3'),line(A,H,'#568269',3)])
  out.append('<path d="M61.28 85.04L67.68 80.24L72.48 86.64" fill="none" stroke="#568269" stroke-width="1.5"/>')
  for p,label,x,y in [(A,'A',14,23),(B,'B',12,141),(D,'D',155,23),(H,'H',74,106),((109.6,58.8),'P',119,61)]:out.extend([dot(p),txt(x,y,label)])
  out.append(txt(90,160,'垂線最短：AP ≥ AH',13));out.append(txt(90,175,'P可移到線段內的H',10.5))
 else:
  out.append('<path d="M20 30L20 126L148 30Z" fill="#e6e3ca"/>');out.extend([line(A,B,'#b98745',2.7),line(A,D,'#b98745',2.7),line(B,D,'#527da2',2.7),line(A,H,'#568269',2.7)])
  out.append('<path d="M30 30V40H20M61.28 85.04L67.68 80.24L72.48 86.64" fill="none" stroke="#6d8583" stroke-width="1.5"/>')
  for p,label,x,y in [(A,'A',14,23),(B,'B',13,141),(D,'D',155,23),(H,'H',74,106)]:out.extend([dot(p),txt(x,y,label)])
  out.extend([txt(10,84,'6',14),txt(83,23,'8',14),txt(107,83,'10',14,'#527da2'),txt(90,160,'同一面積：24＝5AH',13),txt(90,176,'AH＝24/5',12)])
 out.append('</g>')
out.append('</g></svg>');p=Path('docs/comics/art/q-237.svg');p.write_text(''.join(out));ET.fromstring(p.read_text())
Ax,Ay=0,0;Bx,By=0,6;Dx,Dy=8,0;Hx,Hy=72/25,96/25
assert abs((Hx-Ax)*(Dx-Bx)+(Hy-Ay)*(Dy-By))<1e-10
assert abs(Hy-(6-.75*Hx))<1e-10
assert 0<Hx<8 and 0<Hy<6
proof={'BD':math.hypot(8,6),'areaABD':6*8/2,'footH':[Hx,Hy],'AH':math.hypot(Hx,Hy),'projectionParameterFromB':.36,'perpendicularDotProduct':(Hx-Ax)*(Dx-Bx)+(Hy-Ay)*(Dy-By),'minEF':'24/5','genericP':[4.8,2.4],'genericAP':math.hypot(4.8,2.4),'genericEF':math.hypot(4.8,-2.4),'midpointEF':5,'passed':True}
Path('docs/comics/q-237-geometry-validation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
s={'id':'q-237','subject':'Math','title':'把EF換成AP，再找垂線最短','art':str(p),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-237-generate.py','startedAt':'2026-10-29T02:20:19.844891+00:00','panels':[{'heading':'① 小矩形的兩條對角線等長','text':'E、F是垂足，AEPF構成矩形。藍色AP與金色EF是它的兩條對角線，所以EF＝AP；求EF最小，就改求AP最小。','alt':'完整8比6外矩形內的AEPF小矩形著色，AP藍、EF金兩對角線同長，P確在線段BD上。'},{'heading':'② P移到垂足H，AP才最短','text':'P沿BD移動，A到BD的垂線段AH最短。H在線段BD內，P確實可以移到H；此時AP＝AH，也就是EF的最小值。','alt':'A到BD的綠色垂線AH與直角記號，灰色另一位置AP較長；H在線段內，不假定P是中點。'},{'heading':'③ 同一三角形，換底與高計面積','text':'畢氏定理得BD＝√(6²＋8²)＝10。△ABD面積為6×8÷2＝24，也等於10×AH÷2＝5AH，所以AH＝24/5。','alt':'ABD直角三角形兩直角邊6及8，斜邊10藍色、高AH綠色，兩個底高算法算同一面積24。'}],'fourth':{'answer':'答案：EF最小為24/5（4.8）','points':['矩形對角線等長：EF＝AP。','點到直線以垂線最短，P與H重合時取到。','BD中點對應EF＝5，並不是最小值4.8。']},'protectedWords':['AEPF','EF＝AP','AP＝AH','線段BD','垂線段AH','畢氏定理','BD＝10','24/5','同一三角形','√(6²＋8²)＝10','6×8÷2＝24','10×AH÷2＝5AH'],'rationale':'原卷全文及必要given/proof圖實看，24/5維持。用全新精確小矩形對角線/垂線最短/同面積底高三圖，保留P在線段內可達H，不以人物無助為由略過四格，也不把中點5當最小。','promptSummary':'原生SVG8:6矩形與BD，genericP在BD；小矩形對角線同長，最短垂足H=(72/25,96/25)，ABD面積24、斜邊10與高24/5。','answerCheckedAgainst':'原卷AB6/AD8、P沿BD、E/F垂足，幾何獨立驗證AP=EF、投影內點、垂直dot0、面積24，答案24/5。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-237-source-58714f7193.jpg','site/dist/assets/questions/q-237-given.svg','site/dist/assets/questions/q-237-proof.svg'],'visualChecked':True,'answer':'24/5','notes':'原卷動點沿BD及兩垂線條件、手寫24/5均實看，兩原生附圖render實看；新圖重新座標生成，不修改原題或舊附圖。'},'artSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'geometryValidation':'docs/comics/q-237-geometry-validation.json'}
Path('docs/comics/q-237.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
