import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'It took＋人＋時間',17)
for y,v,c in [(45,'It took me','#e6edf3'),(91,'a lot of time','#f0e6d6'),(137,'to find my dream job','#dcebdc')]:r(16,y,168,38,c);t(100,y+20,v,16)
t(300,22,'換spend，整套要改',16)
r(216,47,168,40,'#e6edf3');t(300,68,'I spent time',20)
r(216,111,168,58,'#dcebdc');t(300,130,'finding',20);t(300,153,'my dream job',17)
t(500,22,'decide＋to V',19)
r(420,48,160,38,'#e6edf3');t(500,68,'decide',21)
s.append('<path d="M500 89V112" stroke="#608a72" stroke-width="2"/><path d="M496 107L500 113L504 107" fill="none" stroke="#608a72" stroke-width="2"/>')
r(420,121,160,47,'#dcebdc');t(500,145,'to be a cook',20)
s.append('</svg>');Path('docs/comics/art/q-446.svg').write_text(''.join(s))
x={'id':'q-446','subject':'English','title':'It took與I spent別混用，decide後接to be','art':'docs/comics/art/q-446.svg','protectedWords':['It took','I spent','a lot of time','to find','finding','dream job','decide','to be','being','主詞'],'panels':[{'heading':'① It開頭的花時間句型，選took','text':'原句是It ______ me a lot of time to find my dream job，符合It took＋人＋時間＋to V。找到理想工作花了很多時間，第一格填took。','alt':'It took me、人與時間a lot of time、to find my dream job分層排列，所有部分仍是同一句，不畫虛構精確天數。'},{'heading':'② 若改用spend，主詞和後面的形式也要換','text':'spend的常見句型以人作主詞，可改寫為I spent a lot of time finding my dream job。不能只把took換成spent，卻保留原來It開頭的結構。','alt':'對照I spent time與finding my dream job，明示spend後活動用V-ing，非It spent me time to find混搭。'},{'heading':'③ 第二格看decide，後接to be','text':'decide to V表示決定做某事，所以why did you decide to be a cook，問為什麼決定當廚師。D雖然第一格took正確，第二格being仍不合本句。','alt':'decide與to be a cook相連，清楚區別to be而非being，角色為本題廚師而非杜撰其他職業。'}],'fourth':{'answer':'答案 C：took；to be','points':['It took＋人＋時間＋to V。','I spent＋時間＋V-ing，勿與It took混搭。','decide to be a cook：決定當廚師。']},'rationale':'實看原卷31題完整兩句及四組選項。封存來源僅搜尋到其他題took a plane，未有本題完整解答；依原卷與獨立句型核對。新精確SVG並排It took及I spent主詞/補語形式，再核decide to be，避免人物職涯圖無法說明語法。C答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-446-source-ab69453181.jpg','site/dist/sources/6ae053e4-e970-83ee-b3d3-0c236904b680.txt (scoped search did not find this question31 solution)'],'sourceUrl':'https://chatgpt.com/share/6ae053e4-e970-83ee-b3d3-0c236904b680','sources':[{'url':'https://learnenglish.britishcouncil.org/free-resources/grammar/english-grammar-reference/verbs-followed-infinitive','note':'前題已實讀正文34–44，decide列to-infinitive常見動詞。'},{'url':'https://dictionary.cambridge.org/it/grammatica/grammatica-britannico/take','note':'官方搜尋摘要take表示time/duration且例示It took us a week to paint the house；未宣稱正文實讀。'}],'generationMethod':'precise native SVG alternative sentence patterns and decide-to-infinitive relation','answerCheckedAgainst':'原It took me a lot of time to find，decide to be，兩格C唯一吻合；I spent finding僅同義改寫，不替換原題。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-446.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
