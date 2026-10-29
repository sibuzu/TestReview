import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#4c8068"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def a(x,y):s.append(f'<path d="M{x} {y}V{y+19}" stroke="#608a72" stroke-width="2" marker-end="url(#a)"/>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'remember to bring',17)
r(18,44,164,38,'#e6edf3');t(100,64,'記得要帶',20);a(100,87)
r(18,120,164,43,'#dcebdc');t(100,142,'接著執行：帶傘',17)
t(100,184,'不忘去做',15)
t(300,22,'remember bringing',17)
r(218,44,164,38,'#dcebdc');t(300,64,'之前已經帶過傘',17);a(300,87)
r(218,120,164,43,'#e6edf3');t(300,142,'現在回想這件事',17)
t(300,184,'記得做過',15)
t(500,22,'always：一向如此',17)
r(418,46,164,39,'#e6edf3');t(500,66,'預報說要下雨時',17);a(500,89)
r(418,122,164,53,'#dcebdc');t(500,139,'記得去帶傘',18);t(500,160,'to bring',18)
s.append('</svg>');Path('docs/comics/art/q-052.svg').write_text(''.join(s))
x={'id':'q-052','subject':'English','title':'記得去帶與回想帶過，時間方向不同','art':'docs/comics/art/q-052.svg','protectedWords':['Cathy','remember','to bring','bringing','always','記得去做','記得做過','時間方向','天氣預報'],'panels':[{'heading':'① to bring：記得去帶，不忘執行','text':'本句是天氣預報說要下雨時，Cathy總記得去帶傘。關心的是不忘採取帶傘這個行動，所以用remember to bring，選D。','alt':'記得要帶在前、接著執行帶傘在後，表示remember to bring的不忘執行關係，不虛構具體日期或斷言習慣中的動作從沒發生。'},{'heading':'② bringing：回想自己曾經帶過','text':'remember bringing an umbrella是記得自己曾帶過傘，帶傘的經驗在回想之前。它和本題記得去帶的重點不同，不能只因看到remember就一律選V-ing。','alt':'之前已帶過傘在前、現在回想在後，與第一格方向對照；只示意remember doing的相對先後，不是原題另有一次特定過去事件。'},{'heading':'③ always說的是習慣，不改變兩種搭配的意思','text':'always表示她一向會記得，並不把to bring變成回想過去的bringing。回到整句預報要下雨、記得帶傘的語意，仍用remembers to bring。','alt':'always習慣框將預報要下雨與記得去帶傘連起，不編造實際次數或把always錯當決定動名詞形式的關鍵字。'}],'fourth':{'answer':'答案 D：to bring','points':['remember to V：記得去做，不忘執行。','remember V-ing：回想已發生的經驗。','always表示習慣，仍要看所接動作的意思。']},'rationale':'實看第10題原卷完整句及四個選項，讀來源891–919行兩種remember時間關係。新精確SVG將不忘執行與回想已做的先後並排，再單獨辨always習慣，不泛稱to-infinitive永遠是絕對未來。Cambridge官方搜尋核兩種搭配語意；D答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-052-source-e80acd306d.jpg','site/dist/sources/6ae05238-7b84-83ec-b2f2-9a46aa7cb340.txt lines 891–919'],'sourceUrl':'https://chatgpt.com/share/6ae05238-7b84-83ec-b2f2-9a46aa7cb340','sources':[{'url':'https://dictionary.cambridge.org/grammar/british-grammar/remember-or-remind','note':'官方搜尋結果完整說明remember to-infinitive不忘做，remember-ing記憶過去做過；未宣稱正文實讀。'}],'generationMethod':'precise native SVG relative event-order comparison and habitual context','answerCheckedAgainst':'預報要下雨時不忘帶傘，remember to bring D；bringing表示回想曾帶過，always習慣不推翻兩者語意，無原題改動。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-052.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
