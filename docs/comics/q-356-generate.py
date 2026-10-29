import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#4c8068"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,23,'saw：過去看見',18)
s.append('<path d="M22 94H180" stroke="#608a72" stroke-width="2" marker-end="url(#a)"/><circle cx="62" cy="94" r="5" fill="#a98366"/><circle cx="155" cy="94" r="5" fill="#608a72"/>');t(62,69,'I saw him',16);t(155,122,'現在',16)
t(76,136,'今早看見他',16);t(100,174,'時間點在過去',16)
t(300,23,'看到時，談話正在持續',15)
s.append('<path d="M220 89H380" stroke="#b9d7b7" stroke-width="16" stroke-dasharray="5 3"/><path d="M236 89H364" stroke="#b9d7b7" stroke-width="16"/><path d="M300 59V136" stroke="#a98366" stroke-width="2"/><circle cx="300" cy="89" r="5" fill="#a98366"/>');t(300,51,'was talking',18);t(300,153,'when I saw him',17);t(300,182,'不表示談話被打斷',14)
t(500,23,'再核對主詞與be',17)
r(420,46,160,39,'#e6edf3');t(500,66,'Kevin：單數',19)
s.append('<path d="M500 89V111" stroke="#608a72" stroke-width="2" marker-end="url(#a)"/>')
r(420,125,160,47,'#dcebdc');t(500,149,'was talking',22)
s.append('</svg>');Path('docs/comics/art/q-356.svg').write_text(''.join(s))
x={'id':'q-356','subject':'English','title':'看到的那一刻，Kevin正在談話','art':'docs/comics/art/q-356.svg','protectedWords':['Kevin','saw','when','was talking','were talking','is talking','talked','過去進行式','談話','單數'],'panels':[{'heading':'① 先由saw確定是在回顧過去','text':'when I saw him this morning是今天早上我看見他時。saw已把這次看見定位在過去，不是現在正在發生，所以不能用is talking。','alt':'今早I saw him在現在對話之前的時間點，無時鐘數字或精確間隔，不把this morning機械等同任何時態。'},{'heading':'② 看見是事件點，談話是當時正在進行的背景','text':'這句要表達我看見Kevin時，他正在和英文老師談話，因此選過去進行式。事件點落在談話的持續範圍內，不代表他因被看見就停止談話。','alt':'看見事件點位在was talking背景帶之內，背景延伸到事件兩側且起訖未定，不畫成看見造成中斷或兩件事完全先後。'},{'heading':'③ Kevin單數，用was而非were','text':'過去進行式是was或were加V-ing，Kevin是單數，搭配was talking。talked本身不是壞文法，但C更直接表達本題看見時正在談話的意思。','alt':'Kevin單數主詞對應was talking結構卡，未把所有when句一律當進行式，也未宣稱一般過去式talked永遠錯。'}],'fourth':{'answer':'答案 C：was talking','points':['saw提供過去事件點。','當時正在談話，用過去進行式。','Kevin單數，選was talking，不選were talking。']},'rationale':'實看原卷11完整句及四選項，讀來源919–937行；官方British Council正文39–72核過去時間進行中動作及兩時態關係。新原生SVG分過去事件點/持續背景/主詞一致，不把when當自動觸發詞、不加談話被打斷情節；保留題庫talked合法形式但C最合本題的界線。C答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-356-source-a26c391409.jpg','site/dist/sources/6ae05238-7b84-83ec-b2f2-9a46aa7cb340.txt lines 919–937'],'sourceUrl':'https://chatgpt.com/share/6ae05238-7b84-83ec-b2f2-9a46aa7cb340','sources':[{'url':'https://learnenglish.britishcouncil.org/free-resources/grammar/a1-a2/past-continuous-past-simple','note':'實讀正文39–72：過去某時進行中動作、was/were-ing與過去事件點，過去式和過去進行式所呈現的關係不同。'}],'generationMethod':'precise native SVG past-event point inside ongoing background interval and singular-subject agreement','answerCheckedAgainst':'saw過去、看見當下背景談話進行中、Kevin單數，C was talking最貼題。沒有把when一律當固定公式或宣稱talked結構非法。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-356.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
