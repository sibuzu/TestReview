from pathlib import Path
import json
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
def txt(t,x,y,sz=19,c='#45583e'):return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{sz}" text-anchor="middle" fill="{c}">{t}</text>'
def dot(x,y,c):return f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" stroke="{c}" stroke-width="4"/>'
def line(x1,y1,x2,y2,c,w=7):return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
for p in range(3):
 s.append(f'<g transform="translate({360*p},0)"><rect width="360" height="360" fill="#f4f8ef"/>')
 if p==0:
  s.append(line(65,185,295,185,'#c28c48',9))
  for name,x in [('枋寮',65),('臺東',295)]:s.append(dot(x,185,'#c28c48'));s.append(txt(name,x,222))
 elif p==1:
  s.append(line(45,185,145,185,'#5c88a9'));s.append(line(145,185,310,185,'#c28c48',9))
  for name,x,c in [('高雄',45,'#5c88a9'),('枋寮',145,'#c28c48'),('臺東',310,'#c28c48')]:s.append(dot(x,185,c));s.append(txt(name,x,222))
 else:
  P={'臺北':(180,50),'花蓮':(283,130),'臺東':(277,264),'枋寮':(111,295),'高雄':(70,218)}
  for a,b in [('臺北','花蓮'),('花蓮','臺東'),('臺北','高雄'),('高雄','枋寮'),('枋寮','臺東')]:s.append(line(*P[a],*P[b],'#bdc6b2',4))
  s.append(line(*P['高雄'],*P['枋寮'],'#5c88a9',7));s.append(line(*P['枋寮'],*P['臺東'],'#c28c48',9))
  for n,(x,y) in P.items():
   c='#c28c48' if n in ['枋寮','臺東'] else '#5c88a9' if n=='高雄' else '#829173';s.append(dot(x,y,c));s.append(txt(n,x,y-17 if n!='枋寮' else y+31,18,c))
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-563.svg').write_text(''.join(s));Path('docs/comics/q-563-network-validation.json').write_text(json.dumps({'id':'q-563','formalSouthLinkEndpoints':['枋寮','臺東'],'choiceCTrip':['高雄','枋寮','臺東'],'formalLineHighlightedOrange':['枋寮','臺東'],'previousConnectingSegmentBlue':['高雄','枋寮'],'schematicNotToScale':True,'exactRunningTimesInvented':False,'lineOriginNotKaohsiung':True},ensure_ascii=False,indent=2)+'\n')
