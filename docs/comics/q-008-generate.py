from pathlib import Path
import json,math,itertools,hashlib
h=4*math.sqrt(2)/3; A=(2/3,h);B=(0,0);C=(4,0);D=(5/3,h);T=(3,0);H=(2/3,0)
P=dict(A=A,B=B,C=C,D=D,T=T,H=H);dist=lambda a,b:math.dist(P[a],P[b])
assert all(math.isclose(dist(a,b),v) for a,b,v in [('A','B',2),('A','D',1),('D','C',3),('B','C',4),('A','T',3),('B','T',3),('T','C',1)])
combos=[]
for bases in itertools.combinations([1,2,3,4],2):
 legs=[z for z in [1,2,3,4] if z not in bases]; sides=sorted(legs+[bases[1]-bases[0]]);combos.append({'bases':bases,'legs':legs,'difference':bases[1]-bases[0],'triangleValid':sides[0]+sides[1]>sides[2]})
assert [c['bases'] for c in combos if c['triangleValid']]==[(1,4)]
area=(dist('A','D')+dist('B','C'))*h/2;assert math.isclose(area,10*math.sqrt(2)/3)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><g font-family="Arial,sans-serif">']
for i in range(3):
 o=180*i
 def txt(x,y,t,size=9,col='#244b50',anchor='middle'):s.append(f'<text x="{o+x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{col}">{t}</text>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/>')
 txt(90,20,['先檢查：底不一定是3和4','平移一腰，變成底差三角形','底差3，用畢氏定理求高'][i],10)
 if i==0:
  for x,t in [(29,'兩底'),(83,'兩腰、底差'),(145,'能圍三角形？')]:txt(x,42,t,8)
  for j,c in enumerate(combos):
   y=61+j*17
   if c['triangleValid']:s.append(f'<rect x="{o+8}" y="{y-11}" width="164" height="16" rx="3" fill="#d6e5c2"/>')
   txt(29,y,','.join(map(str,c['bases'])),9);txt(83,y,','.join(map(str,c['legs']+[c['difference']])),9)
   txt(145,y,'可以' if c['triangleValid'] else '不行',9,'#3e743f' if c['triangleValid'] else '#8d766b')
  txt(90,174,'三角形：任兩邊和＞第三邊',9)
 else:
  k=31 if i==1 else 40; bx=22 if i==1 else 27; by=121
  def p(v):return(o+bx+k*v[0],by-k*v[1])
  def line(a,b,col='#829789',w=1.8,dash=''):
   aa,bb=p(P[a]),p(P[b]);s.append(f'<path d="M{aa[0]} {aa[1]}L{bb[0]} {bb[1]}" fill="none" stroke="{col}" stroke-width="{w}" {dash}/>')
  poly=['A','B','C','D'] if i==1 else ['A','B','T']
  s.append('<polygon points="'+' '.join(f'{p(P[z])[0]},{p(P[z])[1]}' for z in poly)+'" fill="#f8faf5" stroke="#829789" stroke-width="1.7"/>')
  for z in (['A','B','C','D','T'] if i==1 else ['A','B','T','H']):
   xx,yy=p(P[z]);dx,dy={'A':(-3,-7),'B':(-7,10),'C':(7,10),'D':(3,-7),'T':(2,13),'H':(0,13)}[z];s.append(f'<text x="{xx+dx}" y="{yy+dy}" text-anchor="middle" font-size="8" fill="#244b50">{z}</text>')
  if i==1:
   line('A','T','#588aa3',1.8,'stroke-dasharray="3 2"');line('A','D','#8aa763',2.8);line('T','C','#8aa763',2.8)
   txt(58,53,'1',10);txt(131,141,'1',10);txt(24,92,'2',10);txt(132,90,'3',10);txt(82,95,'3',10)
   txt(66,142,'3',10);txt(90,159,'AT∥DC，AT＝3',10);txt(90,175,'BT＝4−1＝3',10)
  else:
   line('A','H','#588aa3',1.5,'stroke-dasharray="3 2"');xx,yy=p(H);s.append(f'<path d="M{xx} {yy-5}h5v5" fill="none" stroke="#588aa3" stroke-width=".8"/>')
   txt(35,81,'2',10);txt(106,81,'3',10);txt(64,103,'h',10);txt(39,147,'x',10);txt(100,147,'3−x',10)
   txt(90,169,'x＝⅔，h＝4√2／3',11)
s.append('</g></svg>');art='docs/comics/art/q-008.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-008-geometry-validation.json').write_text(json.dumps({'coordinates':P,'baseCandidates':combos,'allSevenSideAndTranslationLengthsChecked':True,'height':h,'projection':2/3,'pythagoras':[dist('A','B')**2,dist('A','T')**2],'area':area,'expectedArea':10*math.sqrt(2)/3,'strictNondegenerateTriangleTest':True},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-008','subject':'Math','title':'先找兩底，再把底差三角形的高算出來','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-008-generate.py','startedAt':'2026-10-29T05:06:03.839032+00:00','panels':[{'heading':'① 六種配底，只剩1與4可行','text':'兩腰與兩底之差必須能圍成有面積的三角形。六種底邊配法逐一檢查，只有底1、4和腰2、3可行；其餘不是退化，就是不符合三角形不等式。','alt':'逐列列出六種底邊組合及對應兩腰和底差，只有1/4那列通過嚴格三角形不等式。'},{'heading':'② 平移長3的腰，留下底差3','text':'將梯形標為ABCD，AD＝1、BC＝4。在BC上取T，使TC＝AD＝1，則ADCT為平行四邊形，AT＝DC＝3。△ABT的三邊為2、3、3，且與梯形同高。','alt':'新精確梯形AB2/AD1/DC3/BC4，補AT平行DC，TC1與AD1同色，底差BT3；內三角形與梯形共用同高。'},{'heading':'③ 作高h，兩式相減求投影x','text':'作AH⊥BT，設BH＝x、AH＝h。x²＋h²＝4，(3−x)²＋h²＝9；相減得9−6x＝5，所以x＝2／3。再得h²＝4−4／9＝32／9，即h＝4√2／3。','alt':'底差三角形ABT的真坐標高AH，BH=x、HT=3−x，高同時滿足腰長2/3的畢氏定理。'}],'fourth':{'answer':'面積＝10√2／3平方單位','points':['兩底為1與4，兩腰為2與3。','高h＝4√2／3。','面積＝(1＋4)×h÷2＝10√2／3。']},'protectedWords':['三角形不等式','AD＝1','BC＝4','TC＝AD＝1','ADCT','AT＝DC＝3','△ABT','AH⊥BT','BH＝x','AH＝h','x²＋h²＝4','(3−x)²＋h²＝9','9−6x＝5','x＝2／3','h＝4√2／3','10√2／3','h²'],'rationale':'親見原卷無圖完整1/2/3/4題幹；獨立枚舉六種底配及7長度/平行平移/畢氏與面積核定。新精確SVG把容易假設最長兩邊為底的陷阱及底差三角形具體呈現，不用人物或來源AI。','promptSummary':'原生三格：六組底配嚴格不等式表；合法梯形及平移腰作BT3；抽出精確2/3/3三角形作高x/3−x並求h。','answerCheckedAgainst':'原卷四邊1/2/3/4；窮舉唯一底1/4，真坐標兩腰2/3、高4√2/3、面積10√2/3，與既有答案一致。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-008-source-9690790e2a.jpg'],'visualChecked':True,'answer':'10√2／3','notes':'原卷只有完整一句無選項/必要圖，點名A/B/C/D/T/H均為新解題構造並明示，未假稱原卷標記。'},'geometryValidation':'docs/comics/q-008-geometry-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-008.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
