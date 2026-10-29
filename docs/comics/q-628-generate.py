import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#51816b"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,23,'找出 be 動詞',16)
r(20,53,68,42,'#e6edf3');t(54,75,'You',21)
r(104,53,72,42,'#dcebdc');t(140,75,'are',21)
t(100,127,'from Taiwan.',19);t(100,174,'主詞     be',15)
t(300,23,'are 移到主詞前',16)
r(216,64,70,40,'#e6edf3');t(251,84,'You',20)
r(308,64,72,40,'#dcebdc');t(344,84,'are',20)
s.append('<path d="M344 109 Q300 160 240 116" fill="none" stroke="#51816b" stroke-width="3" marker-end="url(#a)"/>')
r(216,151,70,32,'#dcebdc');t(251,167,'Are',19)
r(306,151,74,32,'#e6edf3');t(343,167,'you',19)
t(500,23,'句首大寫、句尾問號',15)
r(420,54,70,40,'#dcebdc');t(455,74,'Are',21)
r(510,54,70,40,'#e6edf3');t(545,74,'you',21)
t(493,124,'from Taiwan',19);t(570,124,'?',26,c='#a16a3b')
t(500,174,'不另外加 Do',16,c='#9a684c')
s.append('</svg>');Path('docs/comics/art/q-628.svg').write_text(''.join(s))
x={'id':'q-628','subject':'English','title':'be疑問句：移動are，不另加Do','art':'docs/comics/art/q-628.svg','protectedWords':['You','are','Are','you','from Taiwan','Do you are','一般疑問句','主詞','句首','問號'],'panels':[{'heading':'① 先找到句中已有的are','text':'You是主詞，are是be動詞；from Taiwan說明來自臺灣。先確認句子的動詞，不要一看到疑問句就直接加入Do。','alt':'原句You are from Taiwan.中You與are分色標示，地名片語保留原序，不把be當一般實義動詞。'},{'heading':'② 讓are移到you前面','text':'改成一般疑問句時，把are移到主詞you前面。原本的You are變成Are you，其餘from Taiwan保持原順序。','alt':'are卡片的移動箭頭指向You前，下一行呈Are you，沒有刪去主詞或重複are。'},{'heading':'③ 調整大小寫與標點','text':'句首寫Are，移到句中的you改為小寫，句尾改問號。完整寫成Are you from Taiwan?，不寫成Do you are。','alt':'完整疑問句Are you from Taiwan?，Are和you分色、問號另外突出，沒有再添加Do。'}],'fourth':{'answer':'參考答案：Are you from Taiwan?','points':['be動詞are移到主詞you前。','from Taiwan的順序不變。','句首大寫，句尾用問號，不另外加Do。']},'rationale':'完整來源文字延伸題及改寫解答已讀。be疑問句有詞序移動和標點變化，精確SVG比人物情境更能呈現解題動作。原題原問句措辭照留，依既有詳解解作一般Yes/No疑問句，不更改題幹或已核答案。','originalMaterialsChecked':True,'originalMaterials':['site/dist/sources/gemini-0KrY8NZ0TTP2.txt lines 80–104 and 160–176'],'sourceUrl':'https://share.gemini.google/0KrY8NZ0TTP2','generationMethod':'precise native SVG token movement and HTML punctuation explanation','answerCheckedAgainst':'原肯定句You are from Taiwan.，be動詞are前移、You轉you、首字Are大寫且句末問號，Are you from Taiwan?與來源及題庫一致。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-628.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
