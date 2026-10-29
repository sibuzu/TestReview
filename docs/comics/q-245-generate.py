from pathlib import Path
import math,json
from math import sin,cos,radians
P=(sin(radians(60))*cos(radians(62)),sin(radians(60))*sin(radians(62)))
Q=(0.,0.);R=(sin(radians(58)),0.);k=1.7
add=lambda a,b:(a[0]+b[0],a[1]+b[1])
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
mul=lambda a,t:(a[0]*t,a[1]*t)
outer=lambda a,c:add(c,mul(sub(a,c),k))
parts={'甲':{'inner':(P,Q),'center':R,'color':'#dfab73'},'乙':{'inner':(Q,R),'center':P,'color':'#84b4d2'},'丙':{'inner':(R,P),'center':Q,'color':'#a5c9a0'}}
xs=[outer(a,g['center'])[0] for g in parts.values() for a in g['inner']]
offset=180-(min(xs)+max(xs))/2*145
pix=lambda a:(offset+145*a[0],232-145*a[1])
pts=lambda aa:' '.join(f'{pix(a)[0]:.3f},{pix(a)[1]:.3f}' for a in aa)
def area(a):return abs(sum(a[i][0]*a[(i+1)%len(a)][1]-a[(i+1)%len(a)][0]*a[i][1] for i in range(len(a)))/2)
checks={}
for n,g in parts.items():
 a,b=g['inner'];c=g['center'];d=sub(b,a);t=sum(sub(c,a)[i]*d[i] for i in range(2))/sum(v*v for v in d);f=add(a,mul(d,t));fo=outer(f,c)
 g['heightLine']=(f,fo);g['poly']=[a,b,outer(b,c),outer(a,c)]
 base=math.dist(a,b);height=math.dist(f,fo)
 checks[n]={'upperBase':base,'lowerBase':base*k,'baseSum':base*(1+k),'height':height,'area':area(g['poly']),'triangleArea':area([c,outer(a,c),outer(b,c)]),'rightAngleDot':sum(sub(fo,f)[i]*d[i] for i in range(2))}
assert len({round(v['area'],9) for v in checks.values()})==1
assert sorted(checks,key=lambda n:checks[n]['height'],reverse=True)==['乙','甲','丙']
assert sorted(checks,key=lambda n:checks[n]['baseSum'],reverse=True)==['丙','甲','乙']
assert all(abs(v['rightAngleDot'])<1e-12 for v in checks.values())
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for panel in range(3):
 s.append(f'<g transform="translate({panel*360},0)"><rect width="360" height="360" fill="#f8faf1"/>')
 if panel==1:
  # Enlarge the central triangle for clear mapping of opposite edges; all exact numbers in HTML.
  def cxy(a):return (65+a[0]*270,280-a[1]*270)
  pp=lambda aa:' '.join(f'{cxy(a)[0]:.2f},{cxy(a)[1]:.2f}' for a in aa)
  s.append(f'<polygon points="{pp([P,Q,R])}" fill="#e6e6e0"/>')
  for n,g in parts.items():
   a,b=g['inner'];s.append(f'<path d="M{cxy(a)[0]:.2f} {cxy(a)[1]:.2f}L{cxy(b)[0]:.2f} {cxy(b)[1]:.2f}" stroke="{g["color"]}" stroke-width="10" stroke-linecap="round"/>')
  for a in [P,Q,R]:s.append(f'<circle cx="{cxy(a)[0]:.2f}" cy="{cxy(a)[1]:.2f}" r="4" fill="#5e695b"/>')
 else:
  for n,g in parts.items():
   s.append(f'<polygon points="{pts(g["poly"])}" fill="{g["color"]}" stroke="#596b54" stroke-width="2.5"/>')
  s.append(f'<polygon points="{pts([P,Q,R])}" fill="#d3d5ce" stroke="#596b54" stroke-width="3"/>')
  if panel==2:
   for n,g in parts.items():
    a,b=g['heightLine'];ax,ay=pix(a);bx,by=pix(b)
    s.append(f'<path d="M{ax:.2f} {ay:.2f}L{bx:.2f} {by:.2f}" stroke="#354638" stroke-width="3.3" stroke-dasharray="6 4"/>')
    for x,y in [(ax,ay),(bx,by)]:s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="#354638"/>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-245.svg').write_text(''.join(s))
Path('docs/comics/q-245-geometry-validation.json').write_text(json.dumps({'id':'q-245','smallTriangleAngles':{'top':58,'bottomLeft':62,'bottomRight':60},'homothetyRatio':k,'scaleIsIllustrative':True,'trapezoidChecks':checks,'heightOrder':['乙','甲','丙'],'baseSumOrder':['丙','甲','乙'],'mapping':'甲 orange left opposite60; 乙 blue bottom opposite58; 丙 green right opposite62','newOriginalSideLengths':False},ensure_ascii=False,indent=2)+'\n')
