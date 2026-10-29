from pathlib import Path
from fractions import Fraction as F
import json
A=(F(-2),F(5));B=(F(6),F(11));P=(F(2),F(8));T=(F(2),F(5));R=(F(6),F(5));L=F(2)
xy=lambda a:(130+19*float(a[0]),330-19*float(a[1]))
d2=lambda a,b:sum((a[i]-b[i])**2 for i in range(2))
assert A[0]<L<B[0] and P==((A[0]+B[0])/2,(A[1]+B[1])/2)
assert d2(A,B)==100 and d2(A,P)==d2(P,B)==25 and d2(R,B)==36 and R[0]==B[0]!=L
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
def line(a,b,c,w=3,dash=False):
 x,y=xy(a);u,v=xy(b);s.append(f'<path d="M{x} {y}L{u} {v}" fill="none" stroke="{c}" stroke-width="{w}"'+(' stroke-dasharray="6 5"' if dash else '')+'/>')
def mark(a,n,c='#4c6950',ox=10,oy=-8):
 x,y=xy(a);s.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{c}"/><text x="{x+ox}" y="{y+oy}" font-family="sans-serif" font-size="23" fill="#33482f">{n}</text>')
for i in range(3):
 s.append(f'<g transform="translate({i*360},0)"><rect width="360" height="360" fill="#f8faf1"/><path d="M25 330H300M130 345V30" stroke="#b4bdac" stroke-width="2"/><path d="M168 345V30" stroke="#9984a7" stroke-width="3" stroke-dasharray="7 5"/><text x="175" y="52" font-family="sans-serif" font-size="23" fill="#82648b">L</text><text x="138" y="40" font-family="sans-serif" font-size="20" fill="#8d9a82">y</text><text x="305" y="337" font-family="sans-serif" font-size="20" fill="#8d9a82">x</text>')
 if i==0:
  line(A,T,'#d4964f');line(T,B,'#d4964f');line(A,B,'#a5b09a',2,True);mark(T,'P','#bd8a47',8,23)
 elif i==1:line(A,B,'#4e8ab0',4);mark(P,'P','#4e8ab0',-26,-8)
 else:
  line(A,R,'#b5baac',2,True);line(R,B,'#c07b59',4);mark(R,'A′','#c07b59',9,24)
 mark(A,'A');mark(B,'B')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-173.svg').write_text(''.join(s))
Path('docs/comics/q-173-geometry-validation.json').write_text(json.dumps({'id':'q-173','A':[-2,5],'B':[6,11],'lineL':'x=2','P':[2,8],'midpoint':True,'squaredDistances':{'AB':str(d2(A,B)),'AP':str(d2(A,P)),'PB':str(d2(P,B)),'wrongReflectedToB':str(d2(R,B))},'wrongReflectionLine':'A reflected (6,5) to B (6,11) has x=6, parallel to L, never meets x=2','correctMinimum':10,'existingDataCorrectionRetained':True,'prototypePInPanel1':[2,5]},indent=2)+'\n')
