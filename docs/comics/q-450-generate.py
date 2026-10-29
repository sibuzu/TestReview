import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#4c8068"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,23,'今晚不一定是未來',16)
r(17,45,166,45,'#e6edf3');t(100,68,'tonight：同一晚',16)
s.append('<path d="M24 119H181" stroke="#4c8068" stroke-width="2" marker-end="url(#a)"/><circle cx="54" cy="119" r="5" fill="#bc977e"/><circle cx="147" cy="119" r="5" fill="#608a72"/>')
t(54,145,'稍早活動',14);t(147,145,'現在對話',14);t(100,178,'I had a great time.',16)
t(300,23,'回顧已結束的經驗',16)
r(218,47,164,43,'#e6edf3');t(300,69,'I had a great time.',16)
s.append('<path d="M300 94V115" stroke="#4c8068" stroke-width="2" marker-end="url(#a)"/>')
r(218,125,164,43,'#dcebdc');t(300,146,'Did you have ...?',18)
t(500,23,'明日再去的安排',16)
s.append('<path d="M422 66H581" stroke="#4c8068" stroke-width="2" marker-end="url(#a)"/><circle cx="440" cy="66" r="5" fill="#608a72"/><circle cx="559" cy="66" r="5" fill="#bc977e"/>')
t(440,92,'現在',15);t(555,92,'tomorrow',15)
r(418,116,164,64,'#dcebdc');t(500,138,'I am going there',18);t(500,163,'again tomorrow.',17)
s.append('</svg>');Path('docs/comics/art/q-450.svg').write_text(''.join(s))
x={'id':'q-450','subject':'English','title':'先看had再判今晚，用am going表明日安排','art':'docs/comics/art/q-450.svg','protectedWords':['tonight','tomorrow','Did','have','had','am going','Were you have','現在進行式','明日安排'],'panels':[{'heading':'① 同樣是今晚，活動可以已經結束','text':'回答I had a great time說的是已經玩得很開心。因此對話發生在活動之後，即使還在tonight的範圍，也是在回顧今晚稍早的經驗。','alt':'同一晚的區間包含稍早活動與現在對話兩點，不編造時鐘讀數，不把tonight直接等同未來。'},{'heading':'② 一般動詞過去問句用Did加原形','text':'肯定回答用了had，對應的問句是Did you have a good time ...?。Did已標示過去，後面保留have；不能用Were you have。','alt':'回答I had a great time連到問句Did you have，保留一般動詞原形，不出現Did had或Were have錯誤搭配。'},{'heading':'③ 明天再去，可以用am going表安排','text':'I am going there again tomorrow用現在進行式表明日的安排，不是說此刻正在去。先靠had把第一格定為Did，再選同時合適的B。','alt':'現在對話點位於tomorrow之前，完整I am going there again tomorrow卡指向明天，不畫成現在正在移動或誤稱be going to句型。'}],'fourth':{'answer':'答案 B：Did；am going','points':['tonight仍可包含今晚稍早的過去活動。','I had對應Did you have。','am going配tomorrow可以表示已安排的未來行程。']},'rationale':'已實看原卷37題整段對話與四組選項。來源封存未搜尋到Laura/本題had或tomorrow段，獨立以原卷、回答had與官方一般問句及進行式未來安排規則核對，不冒稱有本題來源AI詳解。新精確SVG分清同晚的過去活動、現在對話和明日安排；不把Will本身說成永不合tomorrow，B答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-450-source-2888b0f567.jpg','site/dist/sources/6ae053e4-e970-83ee-b3d3-0c236904b680.txt (scoped search found no Laura / target had or tomorrow passage)'],'sourceUrl':'https://chatgpt.com/share/6ae053e4-e970-83ee-b3d3-0c236904b680','sources':[{'url':'https://learnenglish.britishcouncil.org/free-resources/grammar/a1-a2/question-forms','note':'正文44–57實讀，一般動詞過去問句did且例示原形。'},{'url':'https://dictionary.cambridge.org/grammar/british-grammar/future-present-continuous-to-talk-about-the-future-i-m-working-tomorrow','note':'官方搜尋結果完整說明已決定及通常有安排的未來用現在進行式；直接open403，僅記搜尋核對。'}],'generationMethod':'precise native SVG same-evening event timeline and future arrangement contrast','answerCheckedAgainst':'had明示第一格Did而非Do/Were/Will；B第二格am going there tomorrow是現在進行式未來安排，與題庫及原卷一致。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-450.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
