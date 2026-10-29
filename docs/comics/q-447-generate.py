import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#4c8068"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def a(x,y):s.append(f'<path d="M{x} {y}V{y+16}" stroke="#4c8068" stroke-width="2" marker-end="url(#a)"/>')
for i in range(3):r(i*200+2,2,196,196)
t(100,21,'錢花在哪件事？',17)
r(18,45,164,38,'#e6edf3');t(100,64,'Ted spent money',17)
a(100,87);t(100,117,'on',22,c='#a16c41')
r(18,139,164,42,'#dcebdc');t(100,160,'an English program',15)
t(300,21,'錢付給誰？',17)
r(218,45,164,38,'#e6edf3');t(300,64,'he paid a tutor',18)
a(300,87);t(300,117,'to teach',21,c='#a16c41')
r(218,139,164,42,'#dcebdc');t(300,160,'his son',19)
t(500,21,'兩格的線索不同',17)
r(418,45,164,54,'#e6edf3');t(500,62,'money on + 課程',16);t(500,86,'spent',21)
r(418,116,164,64,'#dcebdc');t(500,134,'a tutor + to teach',15);t(500,163,'paid',21)
s.append('</svg>');Path('docs/comics/art/q-447.svg').write_text(''.join(s))
x={'id':'q-447','subject':'English','title':'花錢在課程上，付錢請家教','art':'docs/comics/art/q-447.svg','protectedWords':['Ted','spent','paid','money on','a tutor','to teach','English program','spend','pay','家教','八歲兒子'],'panels':[{'heading':'① 先看第一格後面的money與on','text':'Ted是花錢的人，第一格後面接a lot of money on an English program。依人＋spend＋金錢＋on＋事物的句型，這裡用過去式spent。','alt':'Ted spent money經on連到English program課程卡，表示花費在何事；省略a lot of只為結構圖縮寫，原題HTML保留完整。'},{'heading':'② 第二格先看到付款對象a tutor','text':'第二格後面是家教a tutor，再接to teach his eight-year-old son，表示付錢請家教教八歲兒子。用paid a tutor to teach，不能用spent直接接家教。','alt':'he paid a tutor連到to teach his son，明確付費對象是家教、學習者是兒子，不把兒子當付款對象。'},{'heading':'③ 同樣談花費，仍要對準各自句型','text':'第一格的金錢＋on指向spent；第二格的人＋to teach指向paid。A第二格錯，B第一格錯，D兩格都不合；只有C同時符合。','alt':'兩個獨立結構並排比較，money on課程對spent、a tutor to teach對paid，不將pay所有用法限於接人。'}],'fourth':{'answer':'答案 C：spent；paid','points':['人＋spend＋金錢＋on＋事物。','pay＋人＋to V：付費請人做某事。','本題選過去式spent與paid，分別核對兩格。']},'rationale':'實看第34題原卷全部題幹、四選項。來源封存文字未搜尋到Ted/tutor/spent/paid，本題判斷以清楚原卷與獨立句型核對，不冒稱讀過來源未留存的本題AI解答。新SVG把花費項目與付款對象分開，避免只背花費動詞中文意思，C答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-447-source-8fbb9a8f61.jpg','site/dist/sources/6ae053e4-e970-83ee-b3d3-0c236904b680.txt (scoped search found no Ted/tutor/spent/paid passage)'],'sourceUrl':'https://chatgpt.com/share/6ae053e4-e970-83ee-b3d3-0c236904b680','sources':[{'url':'https://dictionary.cambridge.org/dictionary/english/pay?topic=paying-money','note':'官方搜尋結果完整列pay + object + to-infinitive及paid詞形；直接open回403，僅記搜尋核對。'},{'url':'https://dictionary.cambridge.org/dictionary/english/spend?topic=paying-money','note':'官方搜尋結果與Cambridge English365官方詞表核spend money on something；直接open詞條403，未冒稱正文讀取。'}],'generationMethod':'precise native SVG money-on-course and payment-recipient syntax relations','answerCheckedAgainst':'第一格主詞Ted且money on課程選spent，第二格paid a tutor to teach，C。未把pay可接金額等其他用法否定，僅談本題句型。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-447.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
