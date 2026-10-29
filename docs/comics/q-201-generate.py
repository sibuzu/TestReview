import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def person(x,y,c):s.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}"/><path d="M{x-13} {y+40}V{y+25}Q{x} {y+9} {x+13} {y+25}V{y+40}Z" fill="{c}"/>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'three daughters',18)
for x in [47,100,153]:person(x,66,'#8b9cae')
s.append('<path d="M24 121V133H176V121" fill="none" stroke="#608a72" stroke-width="2"/>');t(100,165,'總共 3 位女兒',20)
t(300,22,'the other one：另外1位',14)
for x in [240,290]:person(x,62,'#86a888')
person(355,62,'#be977a')
r(217,116,103,42,'#e3eddf');t(268,138,'小學：2位',17)
r(326,116,60,42,'#f0e6d6');t(356,131,'高中',15);t(356,149,'1位',15)
t(300,181,'兩種學段要分開',15)
t(500,25,'3 − 1 = 2',29)
person(467,71,'#86a888');person(533,71,'#86a888')
s.append('<path d="M439 123V135H561V123" fill="none" stroke="#608a72" stroke-width="2"/>');t(500,164,'Both：兩者都',22)
s.append('</svg>');Path('docs/comics/art/q-201.svg').write_text(''.join(s))
x={'id':'q-201','subject':'English','title':'三位扣除另外一位，前半句指兩人','art':'docs/comics/art/q-201.svg','protectedWords':['Mr. Wang','three daughters','the other one','Both','Both of them','All of them','Two of them','自由填空','小學','高中'],'panels':[{'heading':'① 先讀清楚：Mr. Wang有三位女兒','text':'原句是three daughters，總共三人。空格所指的人數，還要配合後半句的另外一位來判斷；不要只看到總數three，就立刻認定三人全都在小學。','alt':'三個等大小抽象人物圖標共同括起，精確對應原文字three daughters，不使用另一題two daughters的圖片或條件。'},{'heading':'② the other one另外分出一位高中生','text':'後半句說另外一位在高中，所以前半句在小學的人數是三減一，剩下兩人。不能把All of them代入，否則會變成三位全在小學，與後句衝突。','alt':'同樣三個圖標中兩個綠色小學、一個橘色高中，學段分組數量為2及1，不假定實際年齡、年級或其他家族關係。'},{'heading':'③ 兩位都符合，用Both配are','text':'Both of them表示所指的兩位都符合，接複數動詞are。這是自由填空，Two of them也能表達其中兩人，不能把它當成文法錯誤或補造選項限制。','alt':'精確3減1等2與兩個綠色圖標共同括起Both，表示兩位都在小學；不把Two作自由填空錯答或杜撰單選選項。'}],'fourth':{'answer':'可填 Both；自由填空也可用Two','points':['總共三位，the other one所指另外一位在高中。','3−1＝2，前半句是兩位小學生。','Both of them are；不用All指三人全都。']},'rationale':'無圖的完整文字追問，原來源最後一段Mr. Wang三女兒及Both答已實讀；不誤用原卷Mrs. Wang兩女兒題。新精確SVG固定三個圖標、2/1分組及3-1=2，避免生成模型決定數量。保留自由填空Two也可，Both原答不變，未增選項。','originalMaterialsChecked':True,'originalMaterials':['site/dist/sources/gemini-m6pmkxQwUTM8.txt (entire94 lines read; final user text and answer at lines78–84)'],'sourceUrl':'https://share.gemini.google/m6pmkxQwUTM8','generationMethod':'precise native SVG three-person partition and exact subtraction with native HTML free-fill grammar','answerCheckedAgainst':'文字總數3，另1高中→2小學，Both及Two皆符合自由填空；All三位全小學與另1高中矛盾，沒有原卷照片需求。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-201.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert 3-1==2
Path('docs/comics/q-201-count-validation.json').write_text(json.dumps({'id':'q-201','originalTotal':3,'highSchoolOtherOne':1,'elementary':3-1,'panelOnePeople':3,'panelTwoGroupCounts':[2,1],'panelThreeBothCount':2,'notTheTwoDaughterPhotoQuestion':True,'freeFillTwoAlsoAccepted':True},indent=2)+'\n')
