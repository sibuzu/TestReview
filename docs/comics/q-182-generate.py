from pathlib import Path
import math,json
v=lambda d:(math.cos(math.radians(d)),math.sin(math.radians(d)))
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
B=(45,295);C=(210,295);r=v(-48);D=(C[0]+165*r[0],C[1]+165*r[1]);d=v(-62);e=v(194);w=sub(D,B);t=cross(w,e)/cross(d,e);A=(B[0]+t*d[0],B[1]+t*d[1]);E=(A[0]+.52*(D[0]-A[0]),A[1]+.52*(D[1]-A[1]));k=(225-E[1])/math.sin(math.radians(48));F=(E[0]-k*r[0],225);G=(C[0]+(295-225)/math.tan(math.radians(48)),225)
P=dict(A=A,B=B,C=C,D=D,E=E,F=F,G=G)
def angle(a,o,b):
 u=sub(a,o);v=sub(b,o);return math.degrees(math.acos(max(-1,min(1,(u[0]*v[0]+u[1]*v[1])/(math.hypot(*u)*math.hypot(*v))))))
checks={'angleB':angle(A,B,C),'angleD':angle(C,D,E),'angleEFG':angle(E,F,G),'angleC':angle(B,C,D),'angleA':angle(B,A,D),'EFparallelCD':abs(cross(sub(E,F),sub(D,C)))<1e-8,'FGparallelBC':abs(cross(sub(G,F),sub(C,B)))<1e-8,'EonAD':abs(cross(sub(E,A),sub(D,A)))<1e-8,'GonCD':abs(cross(sub(G,C),sub(D,C)))<1e-8}
for n,num in [('angleB',62),('angleD',62),('angleEFG',48),('angleC',132),('angleA',104)]:assert abs(checks[n]-num)<1e-7
assert all(checks[n] for n in ['EFparallelCD','FGparallelBC','EonAD','GonCD'])
# Diagram coordinates translated as one whole: no nonuniform scaling of angles.
P={n:(p[0],p[1]-30) for n,p in P.items()}
def line(a,b,c='#65775e',w=3,dash=''):return f'<path d="M{a[0]:.2f} {a[1]:.2f}L{b[0]:.2f} {b[1]:.2f}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}"/>'
def polygon(ns,fill):return '<polygon points="'+' '.join(f'{P[n][0]:.2f},{P[n][1]:.2f}' for n in ns)+f'" fill="{fill}"/>'
def label(n,p,dx=0,dy=0):return f'<text x="{p[0]+dx:.2f}" y="{p[1]+dy:.2f}" font-family="serif" font-size="18" text-anchor="middle" fill="#364b3c">{n}</text>'
def arc(o,a,b,c,rad=24):
 q1=math.atan2(a[1]-o[1],a[0]-o[0]);q2=math.atan2(b[1]-o[1],b[0]-o[0]);d=(q2-q1+math.pi*3)%(2*math.pi)-math.pi;q2=q1+d;x1=o[0]+rad*math.cos(q1);y1=o[1]+rad*math.sin(q1);x2=o[0]+rad*math.cos(q2);y2=o[1]+rad*math.sin(q2);return f'<path d="M{x1:.2f} {y1:.2f}A{rad} {rad} 0 0 {int(d>0)} {x2:.2f} {y2:.2f}" fill="none" stroke="{c}" stroke-width="3"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for p in range(3):
 s.append(f'<g transform="translate({360*p},0)"><rect width="360" height="360" fill="#f5f8ee"/>')
 if p==2:s.append(polygon('ABC','#e9ddc4'));s.append(polygon('ACD','#dce7ed'))
 for u,z in zip('ABCD','BCDA'):s.append(line(P[u],P[z]))
 if p<2:
  for u,z,c in [('E','F','#5e89ac'),('C','D','#5e89ac'),('F','G','#b8894e'),('B','C','#b8894e')]:s.append(line(P[u],P[z],c,4))
  for n,dx,dy in [('A',-8,-9),('B',-12,18),('C',0,22),('D',14,2),('E',4,-9),('F',-12,-6),('G',-3,-9)]:s.append(label(n,P[n],dx,dy))
  if p==0:
   for o,a,b in [('B','A','C'),('D','C','E'),('F','E','G')]:s.append(arc(P[o],P[a],P[b],'#81956d',21))
   for text,n,dx,dy in [('62°','B',26,-6),('62°','D',-30,13),('48°','F',35,-7)]:s.append(label(text,P[n],dx,dy))
  else:
   H=(346,P['C'][1]);s.append(line(P['C'],H,'#b8894e',3,'6 5'));s.append(arc(P['C'],P['B'],P['D'],'#5c88aa',30));s.append(arc(P['C'],P['D'],H,'#b8894e',23));s.append(arc(P['F'],P['E'],P['G'],'#b8894e',21))
 else:
  s.append(line(P['A'],P['C'],'#9aa28b',2,'6 5'))
  for o,a,b in [('A','B','D'),('B','A','C'),('C','B','D'),('D','C','A')]:s.append(arc(P[o],P[a],P[b],'#6a895a',23))
  for n,dx,dy in [('A',-8,-9),('B',-12,18),('C',0,22),('D',14,2)]:s.append(label(n,P[n],dx,dy))
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-182.svg').write_text(''.join(s));Path('docs/comics/q-182-geometry-validation.json').write_text(json.dumps({'id':'q-182','coordinates':P,'checks':checks,'angleSum':checks['angleA']+checks['angleB']+checks['angleC']+checks['angleD'],'formula':'360-62-(180-48)-62=104','allPass':True,'modelLengthsShownAsGiven':False},ensure_ascii=False,indent=2)+'\n')
