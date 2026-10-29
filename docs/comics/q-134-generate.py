import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#647c74"/></marker></defs>']
def rect(x,y,w,h,fill,stroke='#bacbc4',r=8): parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')
def t(x,y,s,size=17,c='#25473b',weight=500): parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" font-weight="{weight}" fill="{c}">{escape(s)}</text>')
def line(x1,y1,x2,y2): parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="#647c74" stroke-width="2" fill="none" marker-end="url(#a)"/>')
for i in range(3): rect(i*200+2,2,196,196,'#faf8ed')
t(100,23,'x²−4',20);t(100,107,'x²＋15x−34',18)
for y in (48,132):
 rect(14,y,76,36,'#dcebe1','#6f9c82');t(52,y+18,'x−2',21,c='#286747',weight=700)
 rect(109,y,77,36,'#f7e7d5');t(148,y+18,'x＋2' if y==48 else 'x＋17',18)
 t(99,y+18,'×',17)
t(100,184,'共有的因式 → 乙',15,c='#286747')
for i,(name,factor,fill) in enumerate([('甲','x＋2','#f7e7d5'),('乙','x−2','#dcebe1'),('丙','x＋17','#dce8f3')]):
 y=22+i*53;rect(217,y,163,41,fill);t(239,y+21,name,19);t(307,y+21,factor,22,weight=700)
t(300,182,'一次項係數皆為1',15)
t(500,23,'甲 ＋ 丙',21,weight=700)
rect(417,45,69,38,'#f7e7d5');t(452,64,'x＋2',19)
rect(516,45,70,38,'#dce8f3');t(551,64,'x＋17',19);t(501,64,'＋',18)
t(500,98,'＝',19)
t(445,124,'(x＋x)',17);t(500,124,'＋',16);t(554,124,'(2＋17)',16)
t(500,154,'＝ 2x＋19',24,c='#286747',weight=700);t(500,182,'求和，不是再相乘',15)
parts.append('</svg>');Path('docs/comics/art/q-134.svg').write_text(''.join(parts))
s={'id':'q-134','subject':'Math','title':'找到共同的乙，最後加甲與丙','art':'docs/comics/art/q-134.svg','protectedWords':['共同因式','一次項','正整數','甲＋丙','乙＝x−2','甲＝x＋2','丙＝x＋17','2x＋19','17＋(−2)＝15','17×(−2)＝−34'],'panels':[{'heading':'① 分解兩個乘積，圈出共有因式','text':'x²−4＝(x−2)(x＋2)。再找兩數相乘為−34、相加為15：17與−2，得x²＋15x−34＝(x−2)(x＋17)。兩列共有x−2。','alt':'兩個符號因式分解列，綠色x−2在同欄配對；圖是代數關係，不把含負號的因式當正邊長。'},{'heading':'② 共同的乙，不是任意倍數','text':'兩乘積的最高次項係數都是1，三個一次項係數又都是正整數，所以只能都是1。共有的乙＝x−2，剩下甲＝x＋2、丙＝x＋17。','alt':'甲、乙、丙依序對應x＋2、x−2、x＋17，同色保持角色一致，乙不與甲互換。'},{'heading':'③ 回到題目：求甲＋丙','text':'(x＋2)＋(x＋17)＝(x＋x)＋(2＋17)＝2x＋19。把兩個x合併，兩個正的常數相加；不要把乙也拿來相加。','alt':'甲與丙的因式卡相加，分別合併一次項及常數，得2x＋19；不再次計算乘積。'}],'fourth':{'answer':'答案 A：2x＋19','points':['兩次乘法都出現乙，先找共同因式。','正整數係數條件排除額外倍數。','最後求甲＋丙，不能錯加乙＋丙。']},'rationale':'原卷第2題、全部四選項及來源完整解說已實看讀取。原AI前段短訊誤說乙＋丙，但後段已自行更正共同因式應乙，題庫正確不新增疑義。新製精確代數關係SVG，刻意不把x−2當實際正邊長；不採用來源AI圖。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-134-source-09c39c91c3.jpg','site/dist/sources/6ae05fad-9794-83ee-8670-0ba0b24b80f1.txt lines 1–125'],'sourceUrl':'https://chatgpt.com/share/6ae05fad-9794-83ee-8670-0ba0b24b80f1','generationMethod':'precise native SVG algebra factor matching and symbolic addition','answerCheckedAgainst':'符號展開驗證兩乘積；正整數一次係數乘積1故均1，共同因式乙x−2，甲x+2丙x+17，相加2x+19。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-134.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
# polynomial multiplication and addition, coefficient tuples in ascending order
mul=lambda a,b:[sum(a[i]*b[k-i] for i in range(len(a)) if 0<=k-i<len(b)) for k in range(len(a)+len(b)-1)]
A=[2,1];B=[-2,1];C=[17,1]
assert mul(A,B)==[-4,0,1] and mul(B,C)==[-34,15,1]
assert [A[i]+C[i] for i in (0,1)]==[19,2]
v={'questionId':'q-134','pass':True,'alpha':A,'beta':B,'gamma':C,'alphaTimesBeta':mul(A,B),'betaTimesGamma':mul(B,C),'alphaPlusGamma':[19,2],'positiveIntegerLeadingCoefficientCheck':'ab=bc=1 with a,b,c positive integers forces all1','geometryNote':'Symbolic cards are not physical areas or potentially negative side lengths.','originalActuallyViewed':True,'answer':'A'}
Path('docs/comics/q-134-algebra-validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
