import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#4c8068"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,23,'stop making fun',18)
r(20,51,160,40,'#f0e6d6');t(100,71,'原本的取笑行為',16)
s.append('<path d="M25 119H137" stroke="#bf9477" stroke-width="9"/><path d="M141 100V139" stroke="#9b6558" stroke-width="5"/>');t(100,165,'不再繼續這件事',17)
t(300,23,'stop to V：語意對照',15)
r(220,46,160,35,'#e6edf3');t(300,64,'先停下原活動',16)
s.append('<path d="M300 85V111" stroke="#4c8068" stroke-width="2" marker-end="url(#a)"/>')
r(220,121,160,44,'#dcebdc');t(300,143,'再去做另一件事',16);t(300,183,'不合本句勸阻語意',15,c='#9b6949')
t(500,23,"It's = It is",20)
r(420,48,160,37,'#e6edf3');t(500,67,'not right',19)
s.append('<path d="M500 89V109" stroke="#4c8068" stroke-width="2" marker-end="url(#a)"/>')
r(420,119,160,61,'#dcebdc');t(500,138,'to treat people',17);t(500,162,'like that',18)
s.append('</svg>');Path('docs/comics/art/q-444.svg').write_text(''.join(s))
x={'id':'q-444','subject':'English','title':'停止取笑用making，評論行為用It','art':'docs/comics/art/q-444.svg','protectedWords':['stop','making fun','to V','It\'s','It is','not right','to treat','形式主詞','取笑','一般動詞'],'panels':[{'heading':'① 勸人別再取笑，用stop making','text':'make fun of是取笑。這句要對方停止取笑同學這件事，所以用stop making fun of，讓原本的取笑行為不再繼續。','alt':'取笑行為長條遇到停止線即中止，呈現stop making的停止原活動，不畫傷害同學的具體欺凌情節。'},{'heading':'② stop to V是停下來，再做另一件事','text':'stop to V表示先停下原本做的事，再去做V這件事。若寫stop to make fun，會變成停下來去取笑，不符合本句要勸阻的意思。','alt':'先停原活動再進行另一件事的順序流程，標明僅作語意對照且不合本題，沒有指示讀者去取笑他人。'},{'heading':'③ 第二句是在評論怎樣待人','text':"It's not right to treat people like that.表示那樣對待別人是不對的。It是形式主詞，後面的to treat people like that才是被評論的行為，不是指某位男性或一群人。",'alt':"It's還原It is，not right評價卡連到to treat people like that行為卡，避免把形式主詞解作He或They。"}],'fourth':{'answer':"答案 B：making；It's",'points':['停止原本的行為：stop V-ing。','停下原活動去做別事：stop to V。','It is＋形容詞＋to V，評論後面的行為。']},'rationale':'實看原卷29題完整兩句與四選項。封存來源未搜尋到本題stop making/fun/29對應段，本題以原卷與獨立句法解讀；Cambridge官方搜尋結果核stop doing與stop to do語意差別。新SVG以活動中止與轉換流程、形式主詞評價關係解釋，避免為文法題重演同儕嘲笑。B答案不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-444-source-740695d9cc.jpg','site/dist/sources/6ae053e4-e970-83ee-b3d3-0c236904b680.txt (scoped search found no corresponding stop making fun / question29 segment)'],'sourceUrl':'https://chatgpt.com/share/6ae053e4-e970-83ee-b3d3-0c236904b680','sources':[{'url':'https://dictionary.cambridge.org/grammar/british-grammar/stop-ing-form-or-to-infinitiv','note':'官方搜尋結果完整列明stop-ing停止原活動、stop to-infinitive停下以做另一件事；未宣稱已讀網頁正文。'}],'generationMethod':'precise native SVG action-cessation versus action-switch sequence and dummy-subject structure','answerCheckedAgainst':"原句勸止取笑stop making；第二句It's not right to treat...，It形式主詞而非They/He，B兩格正確。",'visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-444.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
