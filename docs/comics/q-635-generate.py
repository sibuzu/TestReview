from pathlib import Path
import math,json
A=1.2;K=.8
def h(x,y):return .2+2*math.exp(-((x-A)**2+y*y)/K)+2*math.exp(-((x+A)**2+y*y)/K)
# Educational symmetric twin-peak model, not an original exam map or real altitude dataset.
checks={'center':h(0,0),'leftComparison':h(-.15,0),'rightComparison':h(.15,0),'crossNear1':h(0,-.15),'crossNear2':h(0,.15),'farEdge':h(2.8,0)}
assert checks['leftComparison']>checks['center'] and checks['rightComparison']>checks['center']
assert checks['crossNear1']<checks['center'] and checks['crossNear2']<checks['center']
assert checks['farEdge']<checks['center']
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
# Along the connecting ridge: a central relative low point between higher summits.
def profile(cross=False):
 ps=[]
 for i in range(281):
  t=-2.8+i*.02;z=h(0,t) if cross else h(t,0);ps.append((180+t*55,285-z*83))
 d='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in ps)
 s.append(f'<path d="{d}L334 310H26Z" fill="#deebd1"/>')
 s.append(f'<path d="{d}" fill="none" stroke="#5b7954" stroke-width="5"/>')
 s.append(f'<circle cx="180" cy="{285-h(0,0)*83:.2f}" r="7" fill="#d7893d" stroke="#fff" stroke-width="2"/>')
for panel in range(3):
 s.append(f'<g transform="translate({panel*360},0)"><rect width="360" height="360" fill="#f8faf1"/>')
 if panel==0:profile()
 elif panel==2:profile(True)
 else:
  # Linear-interpolated marching squares for true level sets of the same height function.
  nx=100;ny=72;x0=-2.8;y0=-2.0;dx=5.6/nx;dy=4/ny
  for lev in [.4,.6,.8,1.0,1.3,1.6,1.9]:
   seg=[]
   for ix in range(nx):
    for iy in range(ny):
     x=x0+ix*dx;y=y0+iy*dy
     cs=[(x,y),(x+dx,y),(x+dx,y+dy),(x,y+dy)];vs=[h(*p) for p in cs];hits=[]
     for e in range(4):
      a=e;b=(e+1)%4
      if (vs[a]<lev)<(vs[b]<lev) or (vs[b]<lev)<(vs[a]<lev):
       t=(lev-vs[a])/(vs[b]-vs[a]);hits.append((cs[a][0]+t*(cs[b][0]-cs[a][0]),cs[a][1]+t*(cs[b][1]-cs[a][1])))
     if len(hits)==2:
      p,q=hits;seg.append(f'M{180+p[0]*55:.2f} {180-p[1]*55:.2f}L{180+q[0]*55:.2f} {180-q[1]*55:.2f}')
     elif len(hits)==4:raise RuntimeError('ambiguous cell; refine or disambiguate')
   s.append('<path d="'+''.join(seg)+'" stroke="#6b8b5a" fill="none" stroke-width="2.5"/>')
  s.append('<path d="M35 180H325" stroke="#7d8fa4" stroke-dasharray="7 6" stroke-width="2"/><path d="M180 60V300" stroke="#ae987c" stroke-dasharray="7 6" stroke-width="2"/><circle cx="180" cy="180" r="7" fill="#d7893d" stroke="#fff" stroke-width="2"/>')
 s.append('</g>')
s.append('</svg>')
Path('docs/comics/art/q-635.svg').write_text(''.join(s))
Path('docs/comics/q-635-geometry-validation.json').write_text(json.dumps({'id':'q-635','surface':'0.2+2 exp(-((x-1.2)^2+y^2)/0.8)+2 exp(-((x+1.2)^2+y^2)/0.8)','relativeHeightChecks':checks,'saddleCheck':'local minimum on peak-to-peak axis, local maximum on cross axis, not regional global minimum','heightLabelsUsed':False,'originalMap':False},indent=2)+'\n')
