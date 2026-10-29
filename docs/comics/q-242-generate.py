from pathlib import Path
from fractions import Fraction as F
import json,math
# Coordinates are a faithful proportion model for the solved lengths.
U={'A':(1,4),'B':(0,0),'C':(9,0),'D':(6,4),'E':(F(43,10),0),'H':(1,0),'K':(6,0)}
P={k:(45+float(x)*30,270-float(y)*30) for k,(x,y) in U.items()}
def points(ns):return ' '.join(f'{P[n][0]},{P[n][1]}' for n in ns)
def d2(a,b):return sum((U[a][i]-U[b][i])**2 for i in range(2))
checks={'AB_squared':d2('A','B'),'CD_squared':d2('C','D'),'BC':9,'AD':5,'BH':1,'KC':3,'height':4,'ADE_area':F(5*4,2)}
assert checks['AB_squared']==17 and checks['CD_squared']==25 and checks['ADE_area']==10
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for i in range(3):
 s.append(f'<g transform="translate({i*360},0)"><rect width="360" height="360" fill="#f8faf1"/><polygon points="{points("ABCD")}" fill="#eff2e9"/>')
 if i==1:
  s.append(f'<polygon points="{points("ABH")}" fill="#94b9d5"/><polygon points="{points("DKC")}" fill="#edbe7c"/>')
 if i==2:s.append(f'<polygon points="{points("ADE")}" fill="#a7cbb1"/>')
 s.append(f'<polygon points="{points("ABCD")}" fill="none" stroke="#405542" stroke-width="4"/><path d="M{P["A"][0]} 150L{P["E"][0]} 270L{P["D"][0]} 150" stroke="#71836b" stroke-width="2" fill="none"/>')
 if i<2:
  s.append('<path d="M75 150V270M225 150V270" stroke="#7f7057" stroke-width="3" stroke-dasharray="6 5"/><path d="M75 259H86V270M225 259H236V270" fill="none" stroke="#7f7057" stroke-width="2"/>')
 else:
  ex=P['E'][0];s.append(f'<path d="M{ex} 270V150" stroke="#7f7057" stroke-width="3" stroke-dasharray="6 5"/><path d="M{ex} 161H{ex+11}V150" fill="none" stroke="#7f7057" stroke-width="2"/>')
 s.append('<path d="M140 145L148 150L140 155M175 265L183 270L175 275" stroke="#405542" fill="none" stroke-width="2.5"/>')
 for n,(x,y) in P.items():
  if i==2 and n in ['H','K']:continue
  ox,oy={'A':(-8,-18),'B':(-10,27),'C':(12,27),'D':(12,-18),'E':(0,27),'H':(0,27),'K':(0,27)}[n]
  s.append(f'<text x="{x+ox}" y="{y+oy}" font-family="sans-serif" font-size="24" fill="#30452e" text-anchor="middle">{n}</text>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-242.svg').write_text(''.join(s))
Path('docs/comics/q-242-geometry-validation.json').write_text(json.dumps({'id':'q-242','modelUnits':{k:[str(x),str(y)] for k,(x,y) in U.items()},'checks':{k:str(v) for k,v in checks.items()},'independentCalculation':'17-x^2 = 25-(4-x)^2 -> x=1; h^2=16 -> h=4; 5*4/2=10','E_position':'representative 4.3 within [0,9]; not a new given, any base position gives same height/area','userConfirmedLabel':'E, not F; do not reopen'},indent=2)+'\n')
