from pathlib import Path
import math,json
h=lambda r:2*math.exp(-r*r)
levels=[(math.sqrt(math.log(2/z)),c) for z,c in [(0.3,'#70a6c7'),(0.9,'#86ab74'),(1.5,'#d39956')]]
checks=[{'radius':r,'relativeHeight':h(r)} for r,c in levels]
assert checks[0]['relativeHeight']<checks[1]['relativeHeight']<checks[2]['relativeHeight']<h(0)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for panel in range(3):
 s.append(f'<g transform="translate({panel*360},0)"><rect width="360" height="360" fill="#f8faf1"/>')
 if panel==0:
  for r,c in levels:s.append(f'<circle cx="180" cy="180" r="{r*90:.1f}" fill="none" stroke="{c}" stroke-width="4"/>')
  s.append('<circle cx="180" cy="180" r="7" fill="#526e48"/>')
 else:
  scaleX=90 if panel==1 else 155;scaleY=80 if panel==1 else 140;base=288 if panel==1 else 400;extent=1.65 if panel==1 else .88
  pts=[]
  for i in range(251):
   x=-extent+2*extent*i/250;pts.append((180+x*scaleX,base-h(abs(x))*scaleY))
  d='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)
  s.append(f'<path d="{d}L{pts[-1][0]:.2f} 326H{pts[0][0]:.2f}Z" fill="#deebd2"/><path d="{d}" fill="none" stroke="#59744d" stroke-width="4"/>')
  for r,c in (levels if panel==1 else [levels[-1]]):
   y=base-h(r)*scaleY;x1=180-r*scaleX;x2=180+r*scaleX
   s.append(f'<path d="M{x1:.2f} {y:.2f}H{x2:.2f}" stroke="{c}" stroke-width="3" stroke-dasharray="7 5"/>')
   for x in [x1,x2]:s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{c}"/>')
  s.append(f'<circle cx="180" cy="{base-h(0)*scaleY:.2f}" r="7" fill="#526e48" stroke="#fff" stroke-width="2"/>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-637.svg').write_text(''.join(s))
Path('docs/comics/q-637-geometry-validation.json').write_text(json.dumps({'id':'q-637','model':'relative radial height h(r)=2 exp(-r^2), illustrative only','contourRadiiAndHeights':checks,'summitRelativeHeight':h(0),'ascendingInward':True,'equalRelativeContourInterval':0.6,'innerContourBelowSummit':checks[-1]['relativeHeight']<h(0),'numericalLabelsShown':False,'realMountainOrOriginalMap':False},indent=2)+'\n')
