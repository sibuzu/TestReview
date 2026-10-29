from pathlib import Path
from fractions import Fraction as F
import json
P={'A':(90,95),'B':(40,275),'C':(310,275),'D':(270,95),'E':(178,167)}
def points(ns):return ' '.join(f'{P[n][0]},{P[n][1]}' for n in ns)
def area(ns):
 q=[P[n] for n in ns];return abs(F(sum(q[i][0]*q[(i+1)%len(q)][1]-q[(i+1)%len(q)][0]*q[i][1] for i in range(len(q))),2))
scale=F(10,area('ABD'));checks={k:str(area(k)*scale) for k in ['ABD','ABC','BCD','ABCD','ABE','CDE']}
assert checks=={'ABD':'10','ABC':'15','BCD':'15','ABCD':'25','ABE':'6','CDE':'6'}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for i in range(3):
 s.append(f'<g transform="translate({i*360},0)"><rect width="360" height="360" fill="#f8faf1"/><polygon points="{points("ABCD")}" fill="#eff1e7"/>')
 if i==0:s.append(f'<polygon points="{points("ABC")}" fill="#91b9d7"/>')
 elif i==1:s.append(f'<polygon points="{points("BCD")}" fill="#91b9d7"/>')
 else:
  s.append(f'<polygon points="{points("ABD")}" fill="#efbc75"/><polygon points="{points("BCD")}" fill="#91b9d7"/>')
 if i<2:
  s.append('<path d="M90 95V275M270 95V275" fill="none" stroke="#94764e" stroke-width="2" stroke-dasharray="6 5"/><path d="M90 264H101V275M270 264H281V275" fill="none" stroke="#94764e" stroke-width="2"/>')
 s.append(f'<polygon points="{points("ABCD")}" fill="none" stroke="#3d5140" stroke-width="4"/>')
 s.append('<path d="M90 95L310 275" stroke="#657565" stroke-width="2" stroke-dasharray="6 5"/>')
 s.append(f'<path d="M40 275L270 95" stroke="#3d5140" stroke-width="{4 if i==2 else 2}"/>')
 # Matching parallel marks on AD, BC.
 s.append('<path d="M175 90L183 95L175 100M170 270L178 275L170 280" stroke="#3d5140" fill="none" stroke-width="2.5"/>')
 for n,(x,y) in P.items():
  ox,oy={'A':(-6,-18),'B':(-15,25),'C':(14,25),'D':(10,-18),'E':(2,24)}[n]
  s.append(f'<text x="{x+ox}" y="{y+oy}" font-family="sans-serif" font-size="25" fill="#30432e" text-anchor="middle">{n}</text>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-240.svg').write_text(''.join(s))
Path('docs/comics/q-240-geometry-validation.json').write_text(json.dumps({'id':'q-240','vertices':P,'areaScale':str(scale),'areas':checks,'sharedBase':'ABC and BCD share BC, apex A/D on AD parallel BC','validPartition':'ABCD=ABD+BCD interiors disjoint','invalidClaim':'ABD and ABC overlap in ABE; numerical areas sum to 25 but that alone is not a partition proof','sourceSideLengthsAdded':False},indent=2)+'\n')
