from pathlib import Path
import json
from fractions import Fraction as F
# Drawing proportions preserve the area relations; no side lengths are provided or claimed.
A=(82,205);B=(82,305);C=(262,305);D=(262,205);E=(82,65)
P={'A':A,'B':B,'C':C,'D':D,'E':E}
pts=lambda names:' '.join(f'{P[k][0]},{P[k][1]}' for k in names)
def area(names):
 ps=[P[k] for k in names]
 return abs(sum(F(ps[i][0]*ps[(i+1)%len(ps)][1]-ps[(i+1)%len(ps)][0]*ps[i][1]) for i in range(len(ps))))/2
ratio=F(20,area('ABCD'))
check={k:str(area(k)*ratio) for k in ['ABCD','ABD','BCD','ADE','BDE']}
assert check=={'ABCD':'20','ABD':'10','BCD':'10','ADE':'14','BDE':'24'}
Path('docs/comics/q-234-geometry-validation.json').write_text(json.dumps({'pixelVertices':P,'areaScale':'20 / drawn rectangle area','scaledAreas':check,'partition':'BDE = ABD + ADE, with only edge AD shared','overlapInterior':False},indent=2)+'\n')
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for i in range(3):
 s.append(f'<g transform="translate({360*i},0)"><rect width="360" height="360" fill="#f8faf1"/>')
 s.append(f'<polygon points="{pts("BCD")}" fill="#e4e7df"/>')
 s.append(f'<polygon points="{pts("ABD")}" fill="{["#82b6d9","#82b6d9","#cee0ed"][i]}"/>')
 s.append(f'<polygon points="{pts("ADE")}" fill="{["#fffaf0","#f1c578","#f2bb60"][i]}"/>')
 s.append(f'<polygon points="{pts("ABCD")}" fill="none" stroke="#41533d" stroke-width="{5 if i==0 else 3}"/>')
 s.append(f'<path d="M{E[0]} {E[1]}L{B[0]} {B[1]}L{D[0]} {D[1]}Z" fill="none" stroke="#41533d" stroke-width="3"/>')
 s.append(f'<path d="M{A[0]} {A[1]}H{D[0]}" stroke="#41533d" stroke-width="4"/>')
 s.append(f'<path d="M82 218H95V205" fill="none" stroke="#697660" stroke-width="2"/>')
 for name,(x,y) in P.items():
  dx,dy={'A':(-23,2),'B':(-19,22),'C':(15,22),'D':(20,6),'E':(0,-18)}[name]
  s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#344431"/><text x="{x+dx}" y="{y+dy}" fill="#2d3c2a" font-family="sans-serif" font-size="27" text-anchor="middle">{name}</text>')
 s.append('</g>')
s.append('</svg>')
Path('docs/comics/art/q-234.svg').write_text(''.join(s))
