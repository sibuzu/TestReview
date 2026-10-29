import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#4c8068"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def person(x,y,c):s.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}"/><path d="M{x-16} {y+47}V{y+28} Q{x} {y+6} {x+16} {y+28}V{y+47}Z" fill="{c}"/>')
for i in range(3):r(i*200+2,2,196,196)
t(100,23,'Both：兩者都',18)
person(58,68,'#8197b3');person(142,68,'#bd957e')
s.append('<path d="M29 132V143H171V132" fill="none" stroke="#4c8068" stroke-width="2"/>');t(100,171,'my sisters',20)
t(300,23,'複數主詞',18)
r(220,51,160,40,'#e6edf3');t(300,71,'Both of my sisters',16)
s.append('<path d="M300 94V120" stroke="#4c8068" stroke-width="2" marker-end="url(#a)"/>')
r(257,129,86,43,'#dcebdc');t(300,151,'are',25)
t(500,23,'主詞與後面的描述',16)
r(416,49,168,41,'#e6edf3');t(500,70,'Both of my sisters',16)
r(465,98,70,35,'#dcebdc');t(500,116,'are',22)
r(423,143,154,36,'#f0e6d6');t(500,162,'tall and thin',19)
s.append('</svg>');Path('docs/comics/art/q-631.svg').write_text(''.join(s))
x={'id':'q-631','subject':'English','title':'Both指兩位，複數主詞配are','art':'docs/comics/art/q-631.svg','protectedWords':['Both','my sisters','are','am','is','be','tall and thin','兩者都','複數主詞'],'panels':[{'heading':'① Both不是挑其中一人','text':'Both of my sisters指我的兩位姊妹，而且兩位都包括在內。圖中兩人一起被括起，對應Both所指的範圍；不是只選其中一位。','alt':'兩個抽象人物圖標被同一括號括住，對應Both of my sisters的兩位皆包括，不讓人物外形決定語法。'},{'heading':'② 把整個主詞看成複數','text':'Both of my sisters是複數主詞，所以一般現在式選are。am搭配I；is用於第三人稱單數，這裡都不合適。','alt':'完整主詞Both of my sisters作一組，箭頭連到are，不把介詞of後單一字誤當主詞。'},{'heading':'③ tall and thin是兩人的描述','text':'完整句為Both of my sisters are tall and thin.，意思是我的兩位姊妹都又高又瘦。tall and thin描述兩人的特徵，不改變主詞為複數的判斷。','alt':'主詞Both of my sisters、動詞are、形容詞片語tall and thin分層呈現，沒有多添人物或暗示只有一位符合。'}],'fourth':{'answer':'答案 C：are','points':['Both表示兩者都，主詞為複數。','現在式複數主詞使用are。','be是原形，這句要使用變化後的形式。']},'rationale':'來源完整文字延伸及四選項、逐項答案已核。Both的兩位共同範圍是本題易錯點，採精確SVG雙人圖標與主詞群組，數量由程式控制而不用生成模型；用原生HTML解析語法，C答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/sources/gemini-0KrY8NZ0TTP2.txt lines 118–134 and 179–190'],'sourceUrl':'https://share.gemini.google/0KrY8NZ0TTP2','generationMethod':'precise SVG two-member grouping and subject-verb agreement structure','answerCheckedAgainst':'Both of my sisters為兩位姊妹共同作主詞，複數現在式are，原形be及am/is皆不合本句，C與來源題庫一致。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-631.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
