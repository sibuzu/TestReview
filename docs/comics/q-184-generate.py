from pathlib import Path
import json,math,hashlib,xml.etree.ElementTree as ET
q=math.sqrt(24);A=(5/q,5);B=(0,0);C=(20/q,0);D=(17/q,3);W=(10/q,10);V=(35/q,0)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def mul(a,k):return(a[0]*k,a[1]*k)
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def norm(a):return math.hypot(*a)
def project(P,X,Y):v=sub(Y,X);return add(X,mul(v,dot(sub(P,X),v)/dot(v,v)))
def angle(P,Q,R):u=sub(P,Q);v=sub(R,Q);return math.degrees(math.acos(max(-1,min(1,dot(u,v)/norm(u)/norm(v)))))
T=[lambda p:(40+24*p[0],146-24*p[1]),lambda p:(65+11*p[0],139-11*p[1]),lambda p:(15+20*p[0],136-20*p[1])]
def xy(p):return f'{p[0]:.3f},{p[1]:.3f}'
def line(p,r,col='#66847b',w=1.6,dash=''):return f'<path d="M{xy(p)}L{xy(r)}" stroke="{col}" stroke-width="{w}" fill="none"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def poly(ps,fill,stroke='#66847b',w=1.6):return f'<polygon points="{" ".join(map(xy,ps))}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def txt(x,y,t,size=12,col='#234344'):return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>'
def label(p,t,dx=0,dy=0):return f'<circle cx="{p[0]}" cy="{p[1]}" r="2"/>'+txt(p[0]+dx,p[1]+dy,t)
def rightmark(F,P,Q):
 u=mul(sub(P,F),5/norm(sub(P,F)));v=mul(sub(Q,F),5/norm(sub(Q,F)));return f'<path d="M{xy(add(F,u))}L{xy(add(add(F,u),v))}L{xy(add(F,v))}" fill="none" stroke="#8d9a98"/>'
def arc(P,Q,R,color,r=13):
 u=sub(P,Q);v=sub(R,Q);a=math.atan2(u[1],u[0]);b=math.atan2(v[1],v[0]);d=(b-a)%(2*math.pi)
 if d>math.pi:d-=2*math.pi
 p=add(Q,(r*math.cos(a),r*math.sin(a)));z=add(Q,(r*math.cos(a+d),r*math.sin(a+d)))
 return f'<path d="M{xy(p)}A{r} {r} 0 0 {1 if d>0 else 0} {xy(z)}" fill="none" stroke="{color}" stroke-width="2.6"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><g font-family="Noto Sans CJK TC,sans-serif" fill="#234344">']
for i,col in enumerate(['#eef3e9','#edf1f7','#f5efdf']):
 s.append(f'<g transform="translate({180*i},0)"><path d="M0 0h180v180H0Z" fill="{col}"/>');t=T[i];a,b,c,d,w,v=map(t,[A,B,C,D,W,V])
 if i==0:
  s.append(poly([a,b,c,d],'#e0e8d5'));s.append(line(t((C[0]-5.7/q,5.7)),c,'#9aa9b2',1.2,'4 2'))
  for P,n,labeloff in [(A,5,(-9,0)),(D,3,(-9,0))]:
   f=t((P[0],0));p=t(P);s.append(line(p,f,'#55856b',2,'4 2'));s.append(rightmark(f,p,t((P[0]-.4,0))));s.append(txt((p[0]+f[0])/2+labeloff[0],(p[1]+f[1])/2,str(n),13,'#3d7656'))
  for P,n in [(A,2),(B,4)]:
   f=project(P,C,D);p=t(P);ff=t(f);s.append(line(p,ff,'#587fa4',2,'4 2'));s.append(rightmark(ff,p,d));s.append(txt((p[0]+ff[0])/2,(p[1]+ff[1])/2-6,str(n),13,'#587fa4'))
  for p,name,dx,dy in [(a,'A',-8,-5),(b,'B',-8,13),(c,'C',8,13),(d,'D',8,-2)]:s.append(label(p,name,dx,dy))
  s.append(txt(90,175,'綠：到BC；藍：到CD',11))
 elif i==1:
  s.append(poly([w,b,c],'#d6e2ee','#6b8aa2'));s.append(poly([a,b,c,d],'#e1e8d6'));s.append(line(a,w,'#6b8aa2',1.7,'4 2'));s.append(line(d,w,'#6b8aa2',1.7,'4 2'));s.extend([arc(w,b,c,'#b98548',12),arc(b,c,w,'#b98548',12),arc(b,w,c,'#b98548',17)])
  for p,name,dx,dy in [(w,'W',0,-9),(a,'A',-9,-3),(b,'B',-7,13),(c,'C',8,13),(d,'D',9,-2)]:s.append(label(p,name,dx,dy))
  s.append(txt(90,165,'∠B＋∠C＝180°−∠W',11));s.append(txt(90,178,'＜180°',11))
 else:
  s.append(poly([a,b,c,d],'#e1e8d6'));s.append(poly([c,d,v],'#ead9b3','#b78e53'));s.append(line(d,v,'#b78e53',1.7,'4 2'));s.append(line(c,v,'#b78e53',1.7,'4 2'));s.extend([arc(b,c,d,'#58836a',13),arc(c,d,a,'#58836a',13),arc(c,v,d,'#b98548',17)])
  for p,name,dx,dy in [(a,'A',-7,-5),(b,'B',-7,13),(c,'C',-2,14),(d,'D',-9,-5),(v,'V',7,14)]:s.append(label(p,name,dx,dy))
  s.append(txt(90,165,'∠C＋∠D＝180°＋∠V',11));s.append(txt(90,178,'＞180°',11))
 s.append('</g>')
s.append('</g></svg>');p=Path('docs/comics/art/q-184.svg');p.write_text(''.join(s));ET.fromstring(p.read_text())
angles={'A':angle(D,A,B),'B':angle(A,B,C),'C':angle(B,C,D),'D':angle(C,D,A),'W':angle(B,W,C),'V':angle(C,V,D)}
checks={'worldCoordinates':dict(zip(['A','B','C','D','W','V'],[A,B,C,D,W,V])),'distances':{'A_to_BC':A[1],'D_to_BC':D[1],'A_to_CD':norm(sub(A,project(A,C,D))),'B_to_CD':norm(sub(B,project(B,C,D)))},'anglesDegrees':angles,'sumBC':angles['B']+angles['C'],'sumCD':angles['C']+angles['D'],'correctOption':'C','passed':True}
assert abs(checks['distances']['A_to_CD']-2)<1e-9 and abs(checks['distances']['B_to_CD']-4)<1e-9
assert abs(checks['sumBC']-(180-angles['W']))<1e-9 and abs(checks['sumCD']-(180+angles['V']))<1e-9
assert checks['sumBC']<180<checks['sumCD']
Path('docs/comics/q-184-geometry-validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
d={'id':'q-184','subject':'Math','title':'距離變化先定位交點，再分辨內外角','art':str(p),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-184-generate.py','startedAt':'2026-10-29T02:29:33.208861+00:00','panels':[{'heading':'① 兩組垂距，分開比較','text':'A、B到CD的距離為2、4，從B往A更靠近CD；A、D到BC的距離為5、3，從A往D更靠近BC。距離都指垂直距離，不是沿邊走的長度。','alt':'同一精確四邊形，綠色A/D至BC垂距5/3，藍色A/B至CD垂距2/4；垂足直角標示，CD為斜線不是特例直角。'},{'heading':'② 延長BA、CD，得到上方的W','text':'依圖延長BA與CD，在A、D上方交於W。原四邊形的∠B、∠C，就是△WBC的兩個底角，所以∠B＋∠C＝180°−∠W＜180°。','alt':'W在A與D上方、A在線段WB上、D在線段WC上，三角形WBC底角正是原四邊形B/C；不採原AI錯位ASCII圖。'},{'heading':'③ 延長AD、BC，在外側交於V','text':'V在D、C外側。原∠C與∠VCD互補，原∠D與∠VDC互補；兩個原內角相加，得到∠C＋∠D＝180°＋∠V＞180°。','alt':'右側三角形VCD著金色，原四邊形C/D內角以綠弧標示，分清兩對互補角，V位於延長AD與BC的交點。'}],'fourth':{'answer':'答案 C：B＋C＜180°；C＋D＞180°','points':['先找延長線交點在哪一側，不能只背角和方向。','W三角形：B、C是其中兩內角，和小於180°。','V三角形：原C、D各補一個內角，和大於180°。']},'protectedWords':['垂直距離','直線BC','線段WB','線段WC','△WBC','∠VCD','∠VDC','∠B＋∠C','∠C＋∠D','180°−∠W','180°＋∠V'],'rationale':'來源Gemini延伸練習5全文及全部四選項實讀，必要given圖已render實看，C不變。新精確座標同時滿足四垂距5/3/2/4，三圖呈現垂距/上方W/右側V，區分原內角與輔助三角形內角。既有ASCII不一致早已註明，不重問、不改已核對答案。','promptSummary':'原生SVG同一四邊形、四垂距與直角腳；延長BA/CD至W和AD/BC至V，兩三角形/原內角色分。原生座標與角和有獨立程式驗證，不讓imagegen決定精確圖。','answerCheckedAgainst':'延伸原文A/D至BC5/3、A/B至CD2/4與C選項；獨立座標驗垂距及B+C=180−W、C+D=180+V，無來源AI圖。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'transcript':'site/dist/sources/gemini-fIG3raRmygwQ.txt lines1817–2466','images':['site/dist/assets/questions/q-184-given.svg'],'visualChecked':True,'answer':'C','notes':'此題是來源新編延伸，無原卷照片；全文及4選項與完整解析實讀，必要given圖render實看。舊ASCII錯位不沿用，現答案C與網站詳解保持。'},'artSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'geometryValidation':'docs/comics/q-184-geometry-validation.json'}
Path('docs/comics/q-184.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
