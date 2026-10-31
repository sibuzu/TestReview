import json,math
from fractions import Fraction as F
from pathlib import Path
import xml.etree.ElementTree as ET
P=Path('docs/imports/new-gpt-20261031-a/agent3-math');r={}
def record(qid,data):r['q-'+str(qid)]={'passed':True,**data}
delta={a:a*a-40 for a in [-9,-7,8,6]};assert [a for a,d in delta.items() if d<0]==[6];record(890,{'discriminants':delta,'domainClosedEndpoints':[-math.sqrt(40),math.sqrt(40)],'parabolaA6Minimum':.5})
pairs=[(a,b) for a in range(-12,13) for b in range(-12,13) if a*b==-12];vals=sorted(set(a+b for a,b in pairs));assert vals==[-11,-4,-1,1,4,11];record(892,{'integerFactorPairs':pairs,'allowedK':vals,'scope':'整係數因式分解'})
a=-(4-5);b=-2*3;assert (a,b,a-b)==(1,-6,7);record(894,{'甲CorrectConstant':b,'乙CorrectXCoefficient':a,'difference':a-b})
ps=[(x,(4*x+3)**2-(3*x+5)**2) for x in range(3,101)];prime=[(x,v) for x,v in ps if all(v%d for d in range(2,math.isqrt(v)+1))];assert prime==[(3,29)];record(896,{'factorization':[[1,-2],[7,8]],'checkedPositiveIntegerX3Through100PrimeCases':prime,'proof':'x>2令兩因數正整數，7x+8>1，因此x−2=1','x3OuterSide':15,'x3InnerSide':14,'unitLCells':15+14})
def mul(a,b):return [a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1]]
assert mul([3,1],[2,-5])==[6,-13,-5];assert mul([3,1],[4,-6])==[12,-14,-6];assert [2*(2+4),2*(-5-6)]==[12,-22];record(898,{'factorProducts':[[6,-13,-5],[12,-14,-6]],'resultPolynomial':[12,-22],'geometricDomain':'x>5/2','SVGExampleX':4,'SVGLengths':{'height':13,'leftWidth':3,'rightWidth':10,'totalWidth':13,'AEplusBF':26}})
a,b=12,-2;assert F(a+b,2)==5 and F((a+b)+(2*a-b),2)==18 and a-b==14;record(900,{'a':a,'b':b,'midpoint1':5,'midpoint2':18,'difference':14})
for ratio in [3,-3]:
 a1=F(-35,ratio);seq=[a1*ratio**i for i in range(7)];assert seq[1]==-35 and seq[3]==-315;new=[-5*v for v in seq];assert all(new[i+1]/new[i]==ratio for i in range(6))
record(902,{'rSquared':9,'validOriginalAndScaledRatios':[3,-3],'scale':-5})
d=F(2,5);seq=[-1+i*d for i in range(6)];assert seq[-1]==(-1)**6 and seq[2]==F(-1,5);record(904,{'terms':[str(x) for x in seq],'gaps':5,'a3':str(seq[2])})
n=8;d=F(38,9);seq=[-7+i*d for i in range(n+2)];assert seq[-1]==31 and sum(seq[1:-1])==96;record(906,{'insertedCount':8,'totalTerms':10,'totalGaps':9,'difference':str(d),'insertedSum':96,'insertedAverage':12})
vertical=[-10+4*i for i in range(4)];assert vertical[-1]==2 and vertical[1]==-6
for h in [F(-7,3),0,F(2,5),11]:
 horizontal=[-6+(i-3)*h for i in range(7)];assert horizontal[0]+horizontal[-1]==-12
record(908,{'vertical':vertical,'intersectionVerticalIndex':2,'intersectionHorizontalIndex':4,'endpointSum':-12,'horizontalRatioNotNeeded':True})
ns={'s':'http://www.w3.org/2000/svg'}
for qid,panelIndex,count,tag in [(896,2,29,'rect'),(906,2,96,'rect'),(908,0,4,'rect'),(908,1,7,'rect'),(908,2,7,'rect')]:
 root=ET.parse(f'docs/comics/art/q-{qid}.svg').getroot();g=root.findall('s:g',ns)[panelIndex];actual=len(g.findall('s:'+tag,ns))-1;assert actual==count,(qid,actual,count);r['q-'+str(qid)].setdefault('nativeSVGCountChecks',[]).append({'panel':panelIndex+1,'shape':tag,'excludingBackground':actual,'expected':count})
(P/'independent-calculation-validation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('10 calculations + geometric counts PASS')
