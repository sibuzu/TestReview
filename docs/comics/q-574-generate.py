from pathlib import Path
import json
# Relative positions faithfully schematic to the printed scatter; no numerical values assigned to the four points.
P={'甲':(150,96),'乙':(114,230),'丙':(260,230),'丁':(222,80)};x0=58;y0=286;y20=52;y10=169;x2500=292
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="ax" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#67775e"/></marker></defs>']
def text(t,x,y,color='#53634c',sz=17,anchor='middle'):return f'<text x="{x}" y="{y}" font-size="{sz}" font-family="sans-serif" text-anchor="{anchor}" fill="{color}">{t}</text>'
for i in range(3):
 s.append(f'<g transform="translate({360*i},0)"><rect width="360" height="360" fill="#f7f9ef"/>')
 if i==1:s.append(f'<rect x="{x0+3}" y="{y10+1}" width="260" height="{y0-y10-3}" fill="#e3edd7"/>')
 s.append(f'<path d="M{x0} {y0}V{y20-17}M{x0} {y0}H327" fill="none" stroke="#67775e" stroke-width="3" marker-end="url(#ax)"/>')
 # Separate y arrowhead because one combined subpath only gets one marker-end.
 s.append(f'<path d="M{x0} {y20}V{y20-17}" stroke="#67775e" stroke-width="3" marker-end="url(#ax)"/>')
 for val,y in [(0,y0),(10,y10),(20,y20)]:s.append(f'<path d="M{x0-4} {y}H{x0}" stroke="#67775e" stroke-width="2"/>');s.append(text(str(val),x0-10,y+5,sz=15,anchor='end'))
 s.append(f'<path d="M{x2500} {y0}V{y0+5}" stroke="#67775e" stroke-width="2"/>');s.append(text('2500',x2500,y0+24,sz=15))
 s.append(text('mm',324,y0+24,sz=14));s.append(text('°C',28,32,sz=15))
 if i==1:s.append(f'<path d="M{x0} {y10}H320" stroke="#90a17d" stroke-width="2" stroke-dasharray="6 5"/>')
 if i==2:s.append(f'<path d="M{x2500} {y20}V{y0}" stroke="#b8b797" stroke-width="2" stroke-dasharray="6 5"/>')
 for n,(x,y) in P.items():
  col='#697567'
  if i==1:col='#5a8959' if n in ['乙','丙'] else '#b2b9a8'
  if i==2:col={'甲':'#b9bdaf','丁':'#b9bdaf','乙':'#658eae','丙':'#c08c46'}[n]
  if i==2 and n=='丙':s.append(f'<circle cx="{x}" cy="{y}" r="14" fill="none" stroke="#c08c46" stroke-width="2"/>')
  s.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{col}"/>');s.append(text(n,x+13,y-8,col,18))
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-574.svg').write_text(''.join(s));assert P['乙'][1]>y10 and P['丙'][1]>y10 and P['甲'][1]<y10 and P['丁'][1]<y10;assert P['乙'][0]<P['丙'][0]<x2500
Path('docs/comics/q-574-graph-validation.json').write_text(json.dumps({'id':'q-574','relativePixelPositions':P,'y10':y10,'x2500':x2500,'lowerAnnualRange':['乙','丙'],'higherAnnualRange':['甲','丁'],'bingRainMoreThanYi':True,'bingStillLeftOf2500':True,'assignExactClimateValuesToPoints':False,'usesCurrentWeatherData':False},ensure_ascii=False,indent=2)+'\n')
