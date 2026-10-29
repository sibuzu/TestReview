from pathlib import Path
import json
out=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
blue='#3d82b1';orange='#c67b44'
checks=[]
def rod(x,y,L,color,dup=False,w=18):
 if dup:
  out.append(f'<path d="M{x-w/2} {y-L/2}L{x+w/2} {y+L/2}M{x+w/2} {y-L/2}L{x-w/2} {y+L/2}" fill="none" stroke="{color}" stroke-width="8" stroke-linecap="round"/>')
  out.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#3c4955"/>')
 else:
  out.append(f'<path d="M{x} {y-L/2}V{y+L/2}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round"/>')
  out.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#3c4955"/>')
for i in range(3):
 out.append(f'<g transform="translate({360*i},0)"><rect width="360" height="360" fill="#f7fbf4"/>')
 if i<2:
  out.append('<circle cx="180" cy="180" r="151" fill="#edf3fb" stroke="#5a7562" stroke-width="4"/>')
  lengths=[84,64,44,24]; coords=[(96,116),(236,116),(96,246),(236,246)]
  for L,(x,y) in zip(lengths,coords):
   rod(x,y,L,blue,i==1);rod(x+40,y,L,orange,i==1)
  checks.append({'panel':i+1,'chromosomes':8,'pairs':4,'sets':2,'duplicated':i==1,'chromatids':16 if i==1 else 8})
 else:
  for c,dup in [(90,False),(270,True)]:
   out.append(f'<circle cx="{c}" cy="180" r="79" fill="#fff7e9" stroke="#977750" stroke-width="4"/>')
   for dx,L in zip([-45,-15,15,45],[62,46,30,16]):rod(c+dx,180,L,blue,dup,w=14)
   checks.append({'panel':3,'side':'right' if dup else 'left','chromosomes':4,'sets':1,'duplicated':dup,'chromatids':8 if dup else 4})
 out.append('</g>')
out.append('</svg>')
Path('docs/comics/art/q-349.svg').write_text(''.join(out))
assert [c['chromosomes'] for c in checks]==[8,8,4,4]
assert [c['sets'] for c in checks]==[2,2,1,1]
Path('docs/comics/q-349-count-validation.json').write_text(json.dumps({'id':'q-349','diagramType':'simplified conceptual chromosome count; colors distinguish homolog copies, not genes or parents','panels':checks,'countConvention':'one connected chromosome/centromere before sister chromatids separate','notDrawn':'not continuous mitosis stage timing; no anaphase or exact fruit-fly karyotype'},ensure_ascii=False,indent=2)+'\n')
