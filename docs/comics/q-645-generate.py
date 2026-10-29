from pathlib import Path
import math,json
levels=[.9,.7,.5,.3,.1];xs=[1-math.sqrt(z) for z in levels];gaps=[xs[i+1]-xs[i] for i in range(len(xs)-1)];assert all(gaps[i+1]>gaps[i] for i in range(len(gaps)-1))
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#6e7868"/></marker></defs>']
def profile(f,c,dash=''):
 pts=[(40+280*i/150,285-215*f(i/150)) for i in range(151)];d='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in pts);s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="5" stroke-dasharray="{dash}"/>')
for p in range(3):
 s.append(f'<g transform="translate({360*p},0)"><rect width="360" height="360" fill="#f7f9ee"/>')
 s.append('<path d="M46 38H314" stroke="#6e7868" stroke-width="4" marker-end="url(#a)"/>')
 if p==0:
  for z,x in zip(levels,xs):s.append(f'<path d="M40 {285-215*z:.2f}H{40+280*x:.2f}V300" fill="none" stroke="#aeb6a0" stroke-width="2" stroke-dasharray="4 5"/>')
  profile(lambda x:(1-x)**2,'#b88246')
  s.append('<circle cx="40" cy="70" r="8" fill="#bc8045"/><circle cx="320" cy="285" r="8" fill="#5688b2"/>')
 elif p==1:
  for z,x in zip(levels,xs):s.append(f'<path d="M{40+280*x:.2f} 90V290" stroke="#846e4a" stroke-width="4"/>')
  s.append('<circle cx="40" cy="190" r="8" fill="#bc8045"/><circle cx="320" cy="190" r="8" fill="#5688b2"/>')
 else:
  profile(lambda x:1-x*x,'#5688b2','8 5');profile(lambda x:(1-x)**2,'#b88246')
  s.append('<circle cx="40" cy="70" r="6" fill="#747969"/><circle cx="320" cy="285" r="6" fill="#747969"/>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-645.svg').write_text(''.join(s))
Path('docs/comics/q-645-geometry-validation.json').write_text(json.dumps({'id':'q-645','model':'illustrative h(x)=(1-x)^2; x from top0 to foot1','contourHeights':levels,'equalRelativeHeightInterval':.2,'contourX':xs,'horizontalGapsTopToFoot':gaps,'gapsStrictlyIncreasing':True,'derivativeAbsoluteAtUpperLower':[1.8,.2],'upperSteepLowerGentle':True,'contrastBlueCurve':'h(x)=1-x^2; upper gentle lower steep','realMountainOrNumericAltitudes':False},ensure_ascii=False,indent=2)+'\n')
