from pathlib import Path
import math,json,hashlib,xml.etree.ElementTree as ET
from math import cos,sin,radians
x=7.;y=24.;u=(cos(radians(115)),sin(radians(115)))
A=(0.,0.);D=(35.,0.);B=(y*u[0],y*u[1]);C=(B[0]+35,B[1]);E=(7.,0.);F=(x*u[0],x*u[1]);G=(B[0]+17,B[1]);H=(C[0]-18*u[0],C[1]-18*u[1])
d=math.dist
values={'AE':d(A,E),'DE':d(D,E),'AD':d(A,D),'AB':d(A,B),'AF':d(A,F),'BF':d(B,F),'BG':d(B,G),'BC':d(B,C),'CG':d(C,G),'CH':d(C,H),'DH':d(D,H),'CD':d(C,D)}
expect={'AE':7,'DE':28,'AD':35,'AB':24,'AF':7,'BF':17,'BG':17,'BC':35,'CG':18,'CH':18,'DH':6,'CD':24}
for k,v in expect.items():assert abs(values[k]-v)<1e-9,(k,values[k])
assert abs(values['AE']/values['DE']-.25)<1e-9 and abs(values['CH']/values['DH']-3)<1e-9 and abs(values['AD']/values['AB']-35/24)<1e-9
assert 0<x/y<1 and 0<17/35<1 and 0<18/24<1
proof={'id':'q-225','coordinateExample':{'x':7,'y':24,'angleDABDegrees':115,'vertices':dict(zip('ABCDEFGH',[A,B,C,D,E,F,G,H]))},'lengths':values,'expectedLengths':expect,'onSegmentParameters':{'E_on_AD':.2,'F_on_AB':7/24,'G_on_BC':17/35,'H_on_CD':18/24},'arcRadiusEqualities':{'A':[values['AE'],values['AF']],'B':[values['BF'],values['BG']],'C':[values['CG'],values['CH']]},'ratios':{'AE_DE':values['AE']/values['DE'],'CH_DH':values['CH']/values['DH'],'AD_AB':values['AD']/values['AB']},'algebraCheck':{'24x':24*x,'7y':7*y},'allChecksPassed':True,'note':'以使用者已確認35:24為準，取x7/y24驗證合法圖；115度只選一種合法斜度，不是新增已知條件，也不重開學生7:4誤答確認。'}
Path('docs/comics/q-225-geometry-validation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
parts=[]
def txt(a,b,t,size=12,col='#234344'):
 parts.append(f'<text x="{a:.3f}" y="{b:.3f}" font-size="{size}" fill="{col}" text-anchor="middle">{t}</text>')
def line(p,q,c='#8da08d',w=1.3):parts.append(f'<path d="M{p[0]:.3f} {p[1]:.3f}L{q[0]:.3f} {q[1]:.3f}" stroke="{c}" stroke-width="{w}" fill="none"/>')
def arc(o,r,a,b,c='#a9b5a8',w=1.1):
 p=(o[0]+r*cos(radians(a)),o[1]+r*sin(radians(a)));q=(o[0]+r*cos(radians(b)),o[1]+r*sin(radians(b)))
 parts.append(f'<path d="M{p[0]:.3f} {p[1]:.3f}A{r} {r} 0 0 1 {q[0]:.3f} {q[1]:.3f}" stroke="{c}" stroke-width="{w}" fill="none"/>')
def diagram(offset,phase):
 s=3.1;T=lambda p:(offset+48+p[0]*s,54+p[1]*s)
 a,b,c,d,e,f,g,h=map(T,[A,B,C,D,E,F,G,H])
 for v,z in [(a,b),(b,c),(c,d),(d,a)]:line(v,z)
 # Previous exact arcs remain pale; current arc/radius pair is colored.
 arc(a,x*s,0,115,'#80a571' if phase==1 else '#bdc6b8',1.8 if phase==1 else .8)
 if phase>=2:arc(b,17*s,-65,0,'#6b969f' if phase==2 else '#bdc6b8',1.8 if phase==2 else .8)
 if phase==3:arc(c,18*s,180,295,'#6c89b2',1.8)
 if phase==1:line(a,e,'#80a571',2.2);line(a,f,'#80a571',2.2)
 if phase==2:line(b,f,'#6b969f',2.2);line(b,g,'#6b969f',2.2);line(g,c,'#b59460',2.2)
 if phase==3:line(c,g,'#6c89b2',2.2);line(c,h,'#6c89b2',2.2);line(h,d,'#bd9460',2.2)
 items=[(a,'A',(-6,-6)),(b,'B',(-7,13)),(c,'C',(7,13)),(d,'D',(7,-6)),(e,'E',(1,-7)),(f,'F',(-9,2))]
 if phase>=2:items.append((g,'G',(0,14)))
 if phase==3:items.append((h,'H',(9,2)))
 for p,l,o in items:
  parts.append(f'<circle cx="{p[0]:.3f}" cy="{p[1]:.3f}" r="1.7" fill="#426457"/>');txt(p[0]+o[0],p[1]+o[1],l,10)
 return (a,b,c,d,e,f,g,h)
diagram(0,1);txt(90,20,'第一弧：AE＝AF',14);txt(90,156,'AF＝x，BF＝y−x',12);txt(90,175,'AD＝BC＝5x，AB＝y',11)
diagram(180,2);txt(270,20,'第二弧：BF＝BG',14);txt(270,156,'BG＝y−x',12);txt(270,175,'CG＝5x−(y−x)＝6x−y',11)
diagram(360,3);txt(450,20,'第三弧：CG＝CH',14);txt(450,156,'CH＝6x−y',12);txt(450,175,'DH＝2y−6x',12)
p=Path('docs/comics/art/q-225.svg');p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><g font-family="Noto Sans CJK TC,sans-serif"><path d="M0 0h180v180H0Z" fill="#eff3e8"/><path d="M180 0h180v180H180Z" fill="#edf1f7"/><path d="M360 0h180v180H360Z" fill="#f8f0e2"/>'+''.join(parts)+'</g></svg>');ET.fromstring(p.read_text())
spec={'id':'q-225','subject':'Math','title':'三弧半徑逐段換，AD：AB＝35：24','art':str(p),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-225-generate.py','startedAt':'2026-10-29T04:54:45.279023+00:00','panels':[{'heading':'① 設AE＝x、AB＝y，先求第一段半徑','text':'AE：DE＝1：4，所以DE＝4x、AD＝BC＝5x。第一弧以A為圓心，故AF＝AE＝x，剩下BF＝AB−AF＝y−x；別把整條AD當成4x。','alt':'完整平行四邊形與A圓心真圓弧，AE/AF同綠色等半徑，E在AD上且F在AB上；同一合法35/24配置三格共用。'},{'heading':'② 第二弧把BF換成BG，再扣出CG','text':'以B為圓心，第二弧給出BG＝BF＝y−x。因此CG＝BC−BG＝5x−(y−x)＝6x−y。先算整段再減已知部分，每步都對回圖中的線段。','alt':'B中心真圓弧BF/BG同藍綠色，BC剩餘CG另色，前一弧只留淡線；不把BG或CG誤當整條BC。'},{'heading':'③ 第三弧把CG換成CH，套入3：1','text':'以C為圓心，CH＝CG＝6x−y。又CD＝AB＝y，所以DH＝y−CH＝2y−6x。由CH：DH＝3：1，得6x−y＝3(2y−6x)，整理成24x＝7y。','alt':'C中心真圓弧連G與H，CG/CH同藍色、剩餘DH橙色，原圖條件CH:DH3:1由HTML列式，不沿用學生誤答。'}],'fourth':{'answer':'答案：AD：AB＝35：24','points':['24x＝7y，所以y＝24x÷7。','AD：AB＝5x：y＝35：24。','取x＝7檢查：AD35、AB24、CH18、DH6，符合3：1。']},'protectedWords':['AE：DE','1：4','AF＝AE＝x','y−x','6x−y','2y−6x','CH：DH','3：1','6x−y＝3(2y−6x)','24x＝7y','AD：AB','35：24','5x：y'],'rationale':'親見原卷/必要given實際渲染，沿使用者已確認AD:AB35:24、手寫7:4是學生誤答，不重開確認。全新精確SVG依三圓心分步真圓弧與同色等半徑，x7/y24例獨立驗證13長度/所有點在線段內/兩比值與代數；不把115度示意斜度新增成題目條件。無人物或來源AI圖，不改必要作答圖。','promptSummary':'新原生三格同一平行四邊形依A/B/C畫真圓弧，逐步AF=AE、BG=BF、CH=CG及各剩餘長；三格不同色聚焦當前半徑，前弧淡色。35:24已確認，無點陣改原圖或來源AI圖。','answerCheckedAgainst':'原卷AE:DE1:4、依A/B/C三弧交F/G/H、CH:DH3:1及求AD:AB；代數24x7y及獨立x7/y24合法坐標/點序驗證35:24，沿使用者確認。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-225-source-1ae4da4904.jpg'],'existingFiguresActuallyRendered':['site/dist/assets/questions/q-225-given.svg'],'visualChecked':True,'answer':'35：24','notes':'親見全題、三圓弧、AE:DE1:4及CH:DH3:1，現有given已實際渲染看過。7:4為使用者確認學生誤答，未重問；新圖所有F/G/H均在指定邊上。'},'geometryValidation':'docs/comics/q-225-geometry-validation.json','artSHA256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('docs/comics/q-225.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
