import math,json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
B=(50,270);C=(310,270);h=260/(1/math.tan(math.radians(55))+1/math.tan(math.radians(60)));A=(50+h/math.tan(math.radians(55)),270-h)
lerp=lambda a,b,k:(a[0]+k*(b[0]-a[0]),a[1]+k*(b[1]-a[1]))
P=lerp(A,C,(154-A[1])/(C[1]-A[1]));Q=lerp(A,C,.72);u=(math.cos(math.radians(55)),-math.sin(math.radians(55)));Mu=(Q[0]+85*u[0],Q[1]+85*u[1]);Md=(Q[0]-90*u[0],Q[1]-90*u[1]);Ll=(25,154);Lr=(335,154)
def path(a,b,c='#8b968c',w=2):return f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}" stroke="{c}" stroke-width="{w}" fill="none"/>'
def txt(x,y,s,size=23,c='#304b3b'):return f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="{size}" fill="{c}" font-family="Noto Sans CJK TC,serif">{escape(s)}</text>'
def arc(o,a,b,c,r=25):
 a1=math.atan2(a[1]-o[1],a[0]-o[0]);a2=math.atan2(b[1]-o[1],b[0]-o[0]);da=(a2-a1+3*math.pi)%(2*math.pi)-math.pi;a2=a1+da;return f'<path d="M{o[0]+r*math.cos(a1)} {o[1]+r*math.sin(a1)}A{r} {r} 0 0 {int(da>0)} {o[0]+r*math.cos(a2)} {o[1]+r*math.sin(a2)}" stroke="{c}" stroke-width="3" fill="none"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for i in range(3):
 s.append(f'<g transform="translate({i*360},0)"><rect width="360" height="360" fill="#faf8ee"/>')
 s.append(f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#eef1e3" stroke="#708172" stroke-width="2"/>')
 if i<2:
  s.append(path(Ll,Lr,'#5783a5' if i==0 else '#b7c4ba',4 if i==0 else 2));s.append(path(Md,Mu,'#b98149' if i==1 else '#b7c4ba',4 if i==1 else 2))
  s.extend([txt(20,154,'L',22),txt(Md[0],Md[1]+18,'M',22)])
 if i==0:
  s.append(path(B,C,'#5783a5',4));s.extend([arc(P,Ll,C,'#b98149',25),txt(P[0]-30,P[1]+33,'120°',21,'#b98149'),arc(P,A,Ll,'#417f59',31),txt(P[0]-25,P[1]-28,'60°',21,'#417f59'),arc(C,A,B,'#417f59',27),txt(C[0]-43,C[1]-25,'60°',21,'#417f59')]);s.append(txt(180,333,'180°−120°＝60°',23))
 elif i==1:
  s.append(path(A,B,'#b98149',4));s.extend([arc(Q,A,Md,'#b98149',27),txt(Q[0]-48,Q[1]-2,'115°',21,'#b98149'),arc(Q,A,Mu,'#417f59',33),txt(Q[0]-3,Q[1]-45,'65°',21,'#417f59'),arc(A,B,C,'#417f59',29),txt(A[0]-3,A[1]+50,'65°',21,'#417f59')]);s.append(txt(180,333,'180°−115°＝65°',23))
 else:
  s.extend([arc(A,B,C,'#5683a3',29),txt(A[0]-3,A[1]+50,'65°',24,'#5683a3'),arc(C,A,B,'#b98149',29),txt(C[0]-46,C[1]-26,'60°',24,'#b98149'),arc(B,C,A,'#417f59',32),txt(B[0]+45,B[1]-28,'55°',25,'#417f59')]);s.append(txt(180,333,'180°−65°−60°＝55°',22,'#417f59'))
 for n,p,dx,dy in [('A',A,0,-20),('B',B,-16,17),('C',C,16,17)]:s.append(txt(p[0]+dx,p[1]+dy,n,23))
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-204.svg').write_text(''.join(s))
def angle(a,o,b):
 v=(a[0]-o[0],a[1]-o[1]);w=(b[0]-o[0],b[1]-o[1]);return math.degrees(math.acos(sum(x*y for x,y in zip(v,w))/math.hypot(*v)/math.hypot(*w)))
checks={'A':angle(B,A,C),'B':angle(A,B,C),'C':angle(A,C,B),'Lgiven':angle(Ll,P,C),'Ladjacent':angle(A,P,Ll),'Mgiven':angle(A,Q,Md),'Madjacent':angle(A,Q,Mu)}
assert all(abs(checks[k]-v)<1e-9 for k,v in {'A':65,'B':55,'C':60,'Lgiven':120,'Ladjacent':60,'Mgiven':115,'Madjacent':65}.items())
Path('docs/comics/q-204-geometry-validation.json').write_text(json.dumps({'id':'q-204','pass':True,'coordinates':dict(A=A,B=B,C=C,P=P,Q=Q,Lleft=Ll,Lright=Lr,Mup=Mu,Mdown=Md),'angles':checks,'parallelConditions':['L horizontal as BC','M unit direction same as BA'],'originalPrintAndAllThreeOptionsActuallyViewed':True,'answer':'A'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-204','subject':'Math','title':'先找補角，再把角度搬回三角形','art':'docs/comics/art/q-204.svg','protectedWords':['補角','對應角','L∥BC','M∥AB','120°','115°','180°','60°','65°','55°','∠A','∠B','∠C','內角和'],'panels':[{'heading':'① 120°先取補角，再找C角','text':'L∥BC。在L與AC交點，120°旁邊的補角是60°，這個角與∠C互為對應角，所以∠C＝60°。不能把120°直接當C角。','alt':'精確L水平且平行BC，交點下方鈍角120度與左上銳角60度相鄰互補，C角同為60度，藍色顯示平行底。'},{'heading':'② 115°也先取補角，得到A角','text':'M∥AB。圖示115°的補角是65°；由平行線可把它對應到∠A，所以∠A＝65°。先確認兩條射線，再辨認內外方向。','alt':'精確M平行AB，與AC交點左側115度及上方65度相鄰互補，A內角65度；不把鈍角標在錯誤扇形。'},{'heading':'③ 只留三角形，使用內角和','text':'三角形內角和是180°。扣除已求得的65°與60°，剩下∠B＝55°，選A。60°和65°分別是C、A，不是B。','alt':'同一精確三角形移除輔助平行線，A65度、C60度、B55度，弧線與射線角度吻合。'}],'fourth':{'answer':'答案 A：∠B＝55°','points':['兩個已知鈍角都要先找相鄰補角。','依平行線，把60°與65°對應回C、A。','三角形內角和180°，剩下B角55°。']},'rationale':'實看原卷第8題數字與弧角位置及印刷A55/B60/C65三選項；來源相關文字僅介紹此類角度模組。以A65/B55/C60獨立座標構形，L∥BC、M∥AB及兩個鈍角120/115均數值驗證，A答不變；重新製作三張精確角度步驟SVG，不採來源AI圖。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-204-source-d533f6a255.jpg','site/dist/sources/gemini-GD2msWyGjhx0.txt lines 1120–1280 (module discussion)'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG parallel-line angle sectors and triangle angle sum','answerCheckedAgainst':'120補60，115補65，內角和得55。實際向量內積計算各標示扇形角度全符。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-204.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
