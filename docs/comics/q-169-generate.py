from pathlib import Path
from fractions import Fraction as F
import json
A=(F(4),F(-6));R=(F(-4),F(-6));B=(F(3),F(8));P=(F(0),F(2));Q=(F(3),F(-6));T=(F(0),F(0))
xy=lambda a:(180+17*float(a[0]),205-17*float(a[1]))
def d2(a,b):return sum((a[i]-b[i])**2 for i in range(2))
t=F(4,7);at=(R[0]+t*(B[0]-R[0]),R[1]+t*(B[1]-R[1]));assert at==P
assert d2(A,P)==80 and d2(B,P)==45 and d2(R,B)==245 and d2(R,P)==d2(A,P)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
def line(a,b,color,w=3,dash=False):
 x,y=xy(a);u,v=xy(b);s.append(f'<path d="M{x} {y}L{u} {v}" fill="none" stroke="{color}" stroke-width="{w}"'+(' stroke-dasharray="6 5"' if dash else '')+'/>')
def label(a,n,col='#405c44',ox=11,oy=-7):
 x,y=xy(a);s.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{col}"/><text x="{x+ox}" y="{y+oy}" font-family="sans-serif" font-size="23" fill="#30432f">{n}</text>')
for i in range(3):
 s.append(f'<g transform="translate({360*i},0)"><rect width="360" height="360" fill="#f8faf1"/>')
 s.append('<path d="M65 205H309M180 345V20" stroke="#b5bdae" stroke-width="2"/><path d="M174 30L180 20L186 30M299 199L309 205L299 211" stroke="#89967f" fill="none" stroke-width="2"/><text x="193" y="35" font-family="sans-serif" font-size="20" fill="#677761">y</text><text x="312" y="210" font-family="sans-serif" font-size="20" fill="#677761">x</text>')
 if i==0:
  line(A,T,'#ce9757');line(T,B,'#ce9757');line(A,B,'#a7afa0',2,True)
  label(A,'A');label(B,'B');label(T,'P','#b57d3d',-25,25)
 elif i==1:
  line(A,R,'#acb5a7',2,True);line(R,B,'#528bab',4);line(A,P,'#d3934f',3);line(P,B,'#d3934f',3)
  for a,n,col,ox,oy in [(A,'A','#405c44',10,22),(R,'A′','#528bab',-37,22),(B,'B','#405c44',10,-8),(P,'P','#b57d3d',-25,-9)]:label(a,n,col,ox,oy)
 else:
  line(R,Q,'#aab29f',2,True);line(Q,B,'#aab29f',2,True);line(R,B,'#528bab',4)
  x,y=xy(Q);s.append(f'<path d="M{x-12} {y}V{y-12}H{x}" stroke="#7c896e" fill="none" stroke-width="2"/>')
  for a,n,ox,oy in [(R,'A′',-37,22),(B,'B',10,-8),(P,'P',-25,-9)]:label(a,n,'#528bab',ox,oy)
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-169.svg').write_text(''.join(s))
Path('docs/comics/q-169-geometry-validation.json').write_text(json.dumps({'id':'q-169','A':[4,-6],'B':[3,8],'A_reflected':[-4,-6],'intersectionParameter':'4/7','P':[0,2],'squaredDistances':{'AP':str(d2(A,P)),'PB':str(d2(B,P)),'reflectedToP':str(d2(R,P)),'reflectedToB':str(d2(R,B)),'directAB':str(d2(A,B))},'backSubstitution':'sqrt80 + sqrt45 = 4sqrt5+3sqrt5 =7sqrt5','directABNotFeasible':'whole segment has x in [3,4], does not meet y axis','minimumProof':'reflection preserves PA, triangle inequality equality at axis intersection','prototypePInPanel1':[0,0]},indent=2)+'\n')
