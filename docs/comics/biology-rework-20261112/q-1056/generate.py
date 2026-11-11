"""Reading-exercise coding and age plots; do not represent real DOT tire labeling."""
from pathlib import Path
import math
from xml.sax.saxutils import escape
R=Path(__file__).resolve().parents[4];OUT=R/'docs/comics/art';ID='q-1056'
RED='#b3543d';TEAL='#397b7c';GOLD='#ba8a3e';INK='#294d4d'
def txt(x,y,s,sz=42,c=INK):return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{sz}" font-weight="650" fill="{c}">{escape(s)}</text>'
def tire(x,y,r,c=None):
 b=f'<g transform="translate({x} {y})"><circle r="{r}" fill="url(#rubber)" stroke="{c or "#343b3d"}" stroke-width="{7 if c else 3}"/><circle r="{r*.84}" fill="none" stroke="#63696a" stroke-width="3"/><circle r="{r*.59}" fill="#b8c1bf" stroke="#353d3e" stroke-width="6"/>'
 for k in range(10):
  a=k*math.tau/10;b+=f'<path d="M{r*.23*math.cos(a):.2f} {r*.23*math.sin(a):.2f}L{r*.5*math.cos(a):.2f} {r*.5*math.sin(a):.2f}" stroke="#647575" stroke-width="{r*.09}"/>'
 return b+f'<circle r="{r*.18}" fill="#6e8181" stroke="#dce3dc" stroke-width="3"/></g>'
def camera(x,y,s=1):return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 15H24L38 0H74L88 15H112V91H0Z" fill="#6d9190" stroke="#365b5d" stroke-width="3"/><circle cx="56" cy="51" r="29" fill="#d5e1db"/><circle cx="56" cy="51" r="19" fill="#547c82"/><rect x="89" y="24" width="13" height="9" fill="#f2e8c9"/></g>'
def line(x1,y1,x2,y2,c=INK,w=3,dash=''):return f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}" fill="none" stroke="{c}" stroke-width="{w}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def svg(body):return '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640"><defs><radialGradient id="rubber"><stop stop-color="#677274"/><stop offset=".65" stop-color="#343d3f"/><stop offset=".85" stop-color="#505a5d"/><stop offset="1" stop-color="#303638"/></radialGradient></defs><rect width="640" height="640" rx="24" fill="#faf6eb"/><g font-family="Noto Sans CJK TC,sans-serif">'+body+'</g></svg>\n'
a=tire(165,372,122)+'<path d="M267 137H547L583 174V483H267Z" fill="#fffdf6" stroke="#bbb4a3" stroke-width="3"/><path d="M547 137V174H583" fill="#e6e1d4" stroke="#bbb4a3" stroke-width="3"/>'
a+=txt(419,206,'本文規則',43)+txt(354,294,'83',74,TEAL)+txt(484,294,'50',74,GOLD)+line(418,237,418,310,'#c6c0ad',2)
a+=line(354,314,354,350,TEAL,4)+line(484,314,484,350,GOLD,4)+txt(354,399,'年份',37,TEAL)+txt(484,399,'週數',37,GOLD)+txt(320,566,'閱讀圖解，不是實際胎側標記',34)
arts=[a]
# Exact photo date is unknown: the complete 1990 year is shown as a band.
X=lambda y:78+(y-1983)*61
start=X(1983+50/52);expiry=X(1988+50/52);photo=X(1990)
a=txt(320,68,'依本文的五年期限',43)+camera(437,112,.8)+txt(487,235,'1990',43)
a+='<rect x="'+str(photo)+'" y="268" width="61" height="252" fill="#ecd8ab" opacity=".65"/>'
a+=f'<rect x="{start}" y="323" width="{expiry-start}" height="48" rx="8" fill="#93b5a1"/><rect x="{expiry}" y="323" width="{X(1991)-expiry}" height="48" fill="#dfae97"/>'
a+=line(68,422,584,422)+line(expiry,279,expiry,447,RED,3,'7 6')+line(photo,259,photo,447,GOLD,3,'7 6')
for year in [1983,1985,1988,1990]:a+=line(X(year),416,X(year),435)+txt(X(year),478,str(year),32)
a+=txt(284,303,'五年',37,TEAL)+txt(470,302,'已超過',34,RED)+tire(start,546,36)+txt(320,606,'C：1983年第50週製造',34)
arts.append(a)
a=txt(320,69,'按製造年份排列',44)
cut=X(1985);a+=f'<rect x="78" y="117" width="{cut-78}" height="415" fill="#edd4c4" opacity=".7"/>'+line(cut,114,cut,535,RED,3,'7 6')
for year in [1983,1985,1988,1990]:a+=txt(X(year),574,str(year),32)
for k,(lab,code,year) in enumerate([('A','8638',1986),('B','8849',1988),('C','8350',1983),('D','9001',1990)]):
 y=165+k*105;xx=X(year)
 a+=line(78,y,584,y,'#c3c8ba',2)+tire(xx,y,28,RED if lab=='C' else None)+txt(74,y-40,lab,34,RED if lab=='C' else TEAL)+txt(350,y-17,code,34,RED if lab=='C' else INK)
a+=txt(320,621,'圖點按年份，不指定照片日期',29);arts.append(a)
a=txt(320,67,'閱讀題選已過期者',44)
for lab,code,x,y in [('A','8638',167,216),('B','8849',468,216),('C','8350',167,456),('D','9001',468,456)]:
 a+=tire(x,y,78,RED if lab=='C' else None)+txt(x,y+122,lab+' '+code,39,RED if lab=='C' else INK)
 if lab=='C':a+=f'<circle cx="{x}" cy="{y}" r="94" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="10 7"/>'
a+=txt(320,626,'碼號依本文解讀，非現實DOT範例',28);arts.append(a)
for i,b in enumerate(arts,1):(OUT/f'{ID}-four-image-v2-panel-{i}.svg').write_text(svg(b))
print('4 SVG reading diagrams written')
