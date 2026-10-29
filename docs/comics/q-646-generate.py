from pathlib import Path
import math,json
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="flow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#5a8ca7"/></marker></defs>']
# Local valley, north/top is higher. The V apex points toward higher ground, water flows downward.
s.append('<g><rect width="360" height="360" fill="#f5f8ed"/>')
for i in range(5):
 y=125+35*i;s.append(f'<path d="M30 {y}L180 {y-80}L330 {y}" fill="none" stroke="#8b784f" stroke-width="3"/>')
s.append('<path d="M180 53V320" fill="none" stroke="#5a8ca7" stroke-width="5" marker-end="url(#flow)"/></g>')
# Two local dangers: tightly spaced contours and an illustrative cliff cross-section.
s.append('<g transform="translate(360,0)"><rect width="360" height="360" fill="#faf5e9"/><path d="M180 30V330" stroke="#ded4bc" stroke-width="2" stroke-dasharray="4 5"/>')
for r in [30,38,46,54,62,70]:s.append(f'<ellipse cx="94" cy="170" rx="{r}" ry="{r*1.35}" fill="none" stroke="#8b784f" stroke-width="3"/>')
s.append('<path d="M209 70H283V245H332V313H209Z" fill="#dac6a2"/><path d="M209 70H283V245H332" fill="none" stroke="#897453" stroke-width="5"/><path d="M296 170l10 4-5 12-11-7Z M310 211l10 3-7 10-9-5Z" fill="#a18a68"/></g>')
# Exact contour level sets on a smooth twin-peak model, highlighting the saddle but making no camp-safety assertion.
h=lambda x,y:.2+2*math.exp(-((x-1.2)**2+y*y)/.8)+2*math.exp(-((x+1.2)**2+y*y)/.8)
s.append('<g transform="translate(720,0)"><rect width="360" height="360" fill="#f5f8ed"/>')
for lev in [.5,.8,1.1,1.4,1.7,2.0]:
 seg=[]
 for ix in range(100):
  for iy in range(72):
   x=-2.8+ix*.056;y=-2+iy*(4/72);dx=.056;dy=4/72;cs=[(x,y),(x+dx,y),(x+dx,y+dy),(x,y+dy)];vs=[h(*p) for p in cs];hits=[]
   for e in range(4):
    a=e;b=(e+1)%4
    if (vs[a]<lev)!=(vs[b]<lev):
     t=(lev-vs[a])/(vs[b]-vs[a]);hits.append((cs[a][0]+t*(cs[b][0]-cs[a][0]),cs[a][1]+t*(cs[b][1]-cs[a][1])))
   if len(hits)==2:
    p,q=hits;seg.append(f'M{180+p[0]*55:.2f} {180-p[1]*55:.2f}L{180+q[0]*55:.2f} {180-q[1]*55:.2f}')
   elif len(hits)==4:raise RuntimeError('ambiguous marching square')
 s.append('<path d="'+''.join(seg)+'" fill="none" stroke="#6f875b" stroke-width="2.5"/>')
s.append('<circle cx="180" cy="180" r="9" fill="#d69a4e" stroke="#fff" stroke-width="3"/></g></svg>');Path('docs/comics/art/q-646.svg').write_text(''.join(s))
c=h(0,0);checks={'center':c,'alongLeft':h(-.2,0),'alongRight':h(.2,0),'crossUp':h(0,.2),'crossDown':h(0,-.2)};assert checks['alongLeft']>c and checks['alongRight']>c and checks['crossUp']<c and checks['crossDown']<c
Path('docs/comics/q-646-geometry-validation.json').write_text(json.dumps({'id':'q-646','valleyVPointsHigh':'up','streamFlowDirection':'down','saddleRelativeHeightChecks':checks,'equalContourInterval':.3,'contoursGeneratedFromHeightFunction':True,'originalExamMapOrRealCampsite':False,'noSafetyCheckmarkOrTent':True},ensure_ascii=False,indent=2)+'\n')
