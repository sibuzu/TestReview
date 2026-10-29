from pathlib import Path
import json
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs>']
for n,c in [('left','#4778a6'),('right','#c2833c'),('friction','#4e885e')]:
 s.append(f'<marker id="{n}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{c}"/></marker>')
s.append('</defs>')
def a(x1,y1,x2,y2,n,c):s.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="6" marker-end="url(#{n})"/>')
def block():s.append('<rect x="135" y="125" width="90" height="85" rx="5" fill="#caa477" stroke="#755941" stroke-width="4"/><path d="M20 214H340" stroke="#75836b" stroke-width="7"/>')
s.append('<g><rect width="360" height="360" fill="#faf6e9"/>');block()
s.append('<path d="M135 150H62Q44 150 44 168V252M225 150H298Q316 150 316 168V252" fill="none" stroke="#727985" stroke-width="4"/>')
for x in [54,306]:s.append(f'<circle cx="{x}" cy="161" r="11" fill="#d7dfe2" stroke="#727985" stroke-width="3"/><circle cx="{x}" cy="161" r="3" fill="#727985"/>')
for x in [25,297]:s.append(f'<rect x="{x}" y="252" width="38" height="48" rx="4" fill="#99a6af" stroke="#586a73" stroke-width="3"/>')
s.append('</g><g transform="translate(360,0)"><rect width="360" height="360" fill="#f4f8fc"/>');block()
a(180,144,136,144,'left','#4778a6');a(180,183,290,183,'right','#c2833c')
s.append('</g><g transform="translate(720,0)"><rect width="360" height="360" fill="#f4f9f0"/>');block()
a(180,135,290,135,'right','#c2833c');a(180,175,136,175,'left','#4778a6');a(180,207,114,207,'friction','#4e885e')
s.append('</g></svg>');Path('docs/comics/art/q-032.svg').write_text(''.join(s))
Path('docs/comics/q-032-force-validation.json').write_text(json.dumps({'rightTensionKgw':5,'leftTensionKgw':2,'frictionKgw':-3,'horizontalNetKgw':5-2-3,'arrowLengthPerKgw':22,'blockMassKg':3,'claim':'物體靜止，水平合力為零；未給摩擦係數，不另求最大靜摩擦力。','allChecksPass':5-2-3==0},ensure_ascii=False,indent=2)+'\n')
