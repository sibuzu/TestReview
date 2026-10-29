from pathlib import Path
import math,json
A=(180,40);B=(45,40+135*math.sqrt(3));C=(315,B[1]);t=.35
lerp=lambda a,b,k:(a[0]+k*(b[0]-a[0]),a[1]+k*(b[1]-a[1]))
D=lerp(A,B,t);F=lerp(A,C,t);E=lerp(F,(F[0]-135,F[1]+135*math.sqrt(3)),1-t)
P=dict(A=A,B=B,C=C,D=D,E=E,F=F)
dist=lambda a,b:math.dist(a,b)
def angle(a,o,b):
 u=(a[0]-o[0],a[1]-o[1]);v=(b[0]-o[0],b[1]-o[1]);return math.degrees(math.acos((u[0]*v[0]+u[1]*v[1])/(math.hypot(*u)*math.hypot(*v))))
def poly(ps,fill,stroke='#56684f',w=3):return '<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in ps)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def line(a,b,c,w=5):return f'<path d="M{a[0]:.2f} {a[1]:.2f}L{b[0]:.2f} {b[1]:.2f}" fill="none" stroke="{c}" stroke-width="{w}"/>'
def label(n,p,dx=0,dy=0):return f'<text x="{p[0]+dx:.2f}" y="{p[1]+dy:.2f}" font-family="serif" font-size="20" text-anchor="middle" fill="#364b3c">{n}</text>'
def arc(o,a,b,c,r=22):
 q1=math.atan2(a[1]-o[1],a[0]-o[0]);q2=math.atan2(b[1]-o[1],b[0]-o[0]);d=(q2-q1+math.pi*3)%(2*math.pi)-math.pi;q2=q1+d;x1=o[0]+r*math.cos(q1);y1=o[1]+r*math.sin(q1);x2=o[0]+r*math.cos(q2);y2=o[1]+r*math.sin(q2);return f'<path d="M{x1:.2f} {y1:.2f}A{r} {r} 0 0 {int(d>0)} {x2:.2f} {y2:.2f}" fill="none" stroke="{c}" stroke-width="3"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for p in range(3):
 s.append(f'<g transform="translate({360*p},0)"><rect width="360" height="360" fill="#f6f9ef"/>')
 if p<2:
  s.append(poly([A,B,C],'none'));s.append(poly([D,F,E],'none'))
  if p==0:
   for u,v,c in [('A','B','#5d88ad'),('F','E','#5d88ad'),('B','C','#ba8448'),('D','F','#ba8448')]:s.append(line(P[u],P[v],c,4))
   s.append(arc(F,D,E,'#62885b'));s.append(label('1',F,-26,25))
  else:
   s.append(poly([A,D,F],'#dce9f3','#5d88ad'));s.append(poly([C,F,E],'#f0ddbf','#ba8448'))
   for u,v,c in [('A','F','#5d88ad'),('D','F','#5d88ad'),('F','C','#ba8448'),('F','E','#ba8448')]:s.append(line(P[u],P[v],c,5))
  for n,dx,dy in [('A',0,-11),('B',-13,18),('C',13,18),('D',-14,-7),('F',15,-7),('E',0,23)]:s.append(label(n,P[n],dx,dy))
 else:
  cv=lambda p:(80+1.5*(p[0]-D[0]),70+1.5*(p[1]-D[1]));d,f,e=map(cv,[D,F,E]);s.append(poly([d,f,e],'#e5eddc'))
  s.append(line(d,f,'#5d88ad'));s.append(line(f,e,'#ba8448'));s.append(arc(d,f,e,'#5d8857',28));s.append(arc(e,d,f,'#9b79a7',30));s.append(arc(f,d,e,'#8a8f80',23));s.append(label('2',d,31,32));s.append(label('1',f,-31,25))
  for n,p,dx,dy in [('D',d,-15,-4),('F',f,15,-4),('E',e,0,25)]:s.append(label(n,p,dx,dy))
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-178.svg').write_text(''.join(s))
checks={'AF':dist(A,F),'FC':dist(F,C),'DF':dist(D,F),'FE':dist(F,E),'angle1':angle(D,F,E),'angle2':angle(F,D,E),'otherAngleE':angle(D,E,F)};assert checks['AF']<checks['FC'];assert abs(checks['AF']-checks['DF'])<1e-8 and abs(checks['FC']-checks['FE'])<1e-8;assert abs(checks['angle1']-60)<1e-7 and checks['angle2']>60;assert abs(checks['angle2']+checks['otherAngleE']-120)<1e-7
Path('docs/comics/q-178-geometry-validation.json').write_text(json.dumps({'id':'q-178','illustrativeParameter':t,'coordinates':P,'checks':checks,'allPass':True,'numericLengthsAndNonGivenAnglesShownToUser':False},ensure_ascii=False,indent=2)+'\n')
