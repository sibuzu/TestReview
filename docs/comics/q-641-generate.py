from pathlib import Path
import math,json
h1=lambda t:.3+1.5*math.exp(-((t-.5)/.18)**2)
h2=lambda t:.3+1.5*(math.exp(-((t-.03)/.13)**2)+math.exp(-((t-.97)/.13)**2))+.8*math.exp(-((t-.5)/.14)**2)
h3=lambda t:.7+1.4*t+.4*math.sin(2*math.pi*t)
cases=[(h1,.7,.7,True),(h2,h2(0)+.2,h2(1)+.2,False),(h3,1.4,2.8,False)]
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">'];checks=[]
for i,(h,a,b,blocked) in enumerate(cases):
 def xy(t,z):return (40+280*t,320-90*z)
 samples=[(j/2000,h(j/2000)-(a+(b-a)*j/2000)) for j in range(2001)]
 maxDiff=max(x[1] for x in samples)
 assert (maxDiff>0)==blocked
 checks.append({'panel':i+1,'expectedBlocked':blocked,'maxTerrainAboveSightLine':maxDiff,'minimumClearance':-maxDiff,'eyeHeightsRelative':[a,b],'noRealAltitudeValues':True})
 s.append(f'<g transform="translate({360*i},0)"><rect width="360" height="360" fill="#f8faf1"/>')
 ps=[xy(j/250,h(j/250)) for j in range(251)];d='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in ps)
 s.append(f'<path d="{d}L320 336H40Z" fill="#dce9cf"/><path d="{d}" fill="none" stroke="#5f7b50" stroke-width="4"/>')
 for t,z in [(0,a),(1,b)]:
  x,y=xy(t,z);gx,gy=xy(t,h(t));s.append(f'<path d="M{gx} {gy}V{y}" stroke="#9ba59b" stroke-width="3"/>')
 x1,y1=xy(0,a);x2,y2=xy(1,b)
 s.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{"#bd7553" if blocked else "#4a89b1"}" stroke-width="3.5" stroke-dasharray="7 5"/>')
 for x,y in [(x1,y1),(x2,y2)]:s.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#4a89b1" stroke="#fff" stroke-width="2"/>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-641.svg').write_text(''.join(s))
Path('docs/comics/q-641-geometry-validation.json').write_text(json.dumps({'id':'q-641','model':'three illustrative terrain profiles, not original altitude data','samplesPerProfile':2001,'checks':checks,'decision':'Original states actual terrain obstruction, hence true; other panels distinguish ridge name from actual blockage','thirdProfileLocalPointAboveLowObserver':h3(.25)>1.4,'earthCurvatureOrTreesModelled':False},indent=2)+'\n')
