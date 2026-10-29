import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#4c8068"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'Each：逐一每條',18)
for y,label in [(52,'左腿'),(112,'右腿')]:
 r(15,y,71,39,'#e6edf3');t(50,y+20,label,19);s.append(f'<path d="M89 {y+20}H108" stroke="#608a72" stroke-width="2" marker-end="url(#a)"/>');r(118,y,65,39,'#dcebdc');t(151,y+20,'was',22)
t(100,180,'每條都是單數觀點',15)
t(300,22,'Both：兩條一起',18)
r(220,47,70,37,'#e6edf3');t(255,66,'左腿',18)
r(310,47,70,37,'#e6edf3');t(345,66,'右腿',18)
s.append('<path d="M230 90V101H370V90M300 102V127" fill="none" stroke="#608a72" stroke-width="2" marker-end="url(#a)"/>')
r(250,140,100,38,'#dcebdc');t(300,160,'were',23)
t(500,22,'原題固定是 was',17)
r(418,45,164,40,'#dcebdc');t(500,66,'Each of ... was ✓',17)
r(418,102,164,40,'#f1e6da');t(500,123,'Every of ... ×',18,c='#9b6756')
t(500,174,'不能把was改were作答',14)
s.append('</svg>');Path('docs/comics/art/q-197.svg').write_text(''.join(s))
x={'id':'q-197','subject':'English','title':'Each逐一配was，Both整組則配were','art':'docs/comics/art/q-197.svg','protectedWords':['Each','Both','Every','Some','of his legs','was','were','單數觀點','複數','原題'],'panels':[{'heading':'① Each逐一說每條腿，用單數was','text':'Each of his legs指他的每一條腿。雖然legs是複數，Each仍是單數核心；左腿、右腿各自說明時都配was，所以原句可用Each。','alt':'左腿與右腿各自獨立連到was，表示Each逐一分配的單數觀點，不畫受傷肢體、不新增傷勢程度或醫療處置。'},{'heading':'② Both雖可表示兩腿都，動詞卻要were','text':'若主詞改成Both of his legs，就把兩條腿一起當複數，應寫were hurt。中文都能說兩腿受傷，不代表英文主詞與動詞形式相同；原題已固定was。','alt':'左腿和右腿共同括起，Both複數連到were，與前格Each各自was對照，不改寫原題既有was選答案。'},{'heading':'③ 再看能否直接接of','text':'Each可以直接接of his legs。Every不能直接接of；Some of his legs在這裡也是複數，不合was。因此同時符合句型與單數動詞的是A。','alt':'原題was條件下Each of was標可行，Every of標錯；不新增Every one of his legs例或把Some用於所有不可數情境也判複數。'}],'fourth':{'answer':'答案 A：Each','points':['Each of his legs作單數主詞，配was。','Both of his legs為複數，需配were。','保留原題was，再核對Each可以直接接of。']},'rationale':'實看第3頁綜合9原卷完整句與四選項；封存全文前已讀，無legs/football/was hurt對應本題解答，獨立依Each/of/was核A。新精確SVG左右腿概念卡逐一vs共同分組，可示主謂一致而不畫傷口；對照Both須were，不以中文兩腿都受傷直接挑Both，不更動原問答。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-197-source-754fd9d61b.jpg','site/dist/sources/gemini-m6pmkxQwUTM8.txt (entire source read for q-186; scoped search no legs/football target solution)'],'sourceUrl':'https://share.gemini.google/m6pmkxQwUTM8','sources':[{'url':'https://dictionary.cambridge.org/uk/grammar/british-grammar/each','note':'本輪官方搜尋Each of完整段核單數動詞規則，僅記搜尋核對。'},{'url':'https://dictionary.cambridge.org/grammar/british-grammar/each-or-every.','note':'本輪官方搜尋完整例核Each可直接of而Every of不成立；不延伸非本題語域差異。'}],'generationMethod':'precise native SVG distributive versus grouped subject agreement with fixed original was constraint','answerCheckedAgainst':'Each單數可接of、配was；Both/Some在legs語境複數，Every不能直接of，A。Both were只為對照，不改題。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-197.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
