import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#5c8064"/></marker></defs>']
def rect(x,y,w,h,fill='#faf8ee',r=7):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="#bacbbe"/>')
def txt(x,y,st,size=17,c='#2c4b39',wt=500):s.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" fill="{c}" font-weight="{wt}">{escape(st)}</text>')
for i in range(3):rect(i*200+2,2,196,196)
txt(100,20,'先定最早、最晚',17,wt=700)
rect(15,40,170,58,'#dfeadf');txt(100,57,'乙 郭錫瑠',20);txt(100,83,'18世紀 · 水利',16)
s.append('<path d="M100 101V120" stroke="#5c8064" stroke-width="2" marker-end="url(#a)"/>')
rect(15,128,170,57,'#e4ecf3');txt(100,145,'丙 吳三連',20);txt(100,170,'1951 · 民選市長',16)
txt(300,20,'再比中間兩位',17,wt=700)
rect(215,40,170,58,'#f1e4d3');txt(300,57,'甲 沈葆楨',20);txt(300,83,'1875 · 臺北府',16)
s.append('<path d="M300 101V120" stroke="#5c8064" stroke-width="2" marker-end="url(#a)"/>')
rect(215,128,170,57,'#e2eddf');txt(300,145,'丁 劉銘傳',20);txt(300,170,'1880年代 · 建設',16)
txt(500,20,'表格順序 ≠ 年代',16,wt=700)
for i,(n,who,period) in enumerate([('乙','郭錫瑠','18世紀'),('甲','沈葆楨','1870年代'),('丁','劉銘傳','1880年代'),('丙','吳三連','1951')]):
 y=40+i*35;rect(410,y,180,29,'#e0ebdf' if i in (0,3) else '#e9eee3');txt(424,y+15,n,17,wt=700);txt(476,y+15,who,16);txt(550,y+15,period,13)
s.append('</svg>');Path('docs/comics/art/q-063.svg').write_text(''.join(s))
spec={'id':'q-063','subject':'History','title':'先定最早與最晚，再比較沈與劉','art':'docs/comics/art/q-063.svg','protectedWords':['郭錫瑠','沈葆楨','劉銘傳','吳三連','臺北府','民選市長','18世紀','1870年代','1880年代','1951','乙甲丁丙','1875'],'panels':[{'heading':'① 抓兩端：水利最早，民選市長最晚','text':'乙郭錫瑠的水利建設在18世紀，四人中最早。丙吳三連的事蹟直接標出1951年，是戰後民選市長，應排最後。不是依樓層或表格順序排。','alt':'兩端年代卡：乙郭錫瑠18世紀水利，丙吳三連1951民選市長，箭頭表示先後而非人物直接傳承或等尺度年距。'},{'heading':'② 中間比較：沈葆楨先，劉銘傳後','text':'甲沈葆楨在1870年代奏設臺北府，官方記載為1875年。丁劉銘傳的鐵路、電報等建設，屬1880年代清治後期，因此甲在丁之前。','alt':'兩筆不同年代事蹟卡，沈葆楨1875臺北府早於劉銘傳1880年代建設；不把劉所有建設限定同一年完成。'},{'heading':'③ 回填代號，再核對選項','text':'人物先後是郭錫瑠、沈葆楨、劉銘傳、吳三連，換成原表代號就是乙甲丁丙，選D。C雖把兩端放對，中間甲、丁仍然顛倒。','alt':'原表代號與姓名及年代並排按乙甲丁丙重排，保留原代號不依新列位置重新改名。'}],'fourth':{'answer':'答案 D：乙甲丁丙','points':['先定乙最早、丙最晚，減少比較負擔。','沈葆楨臺北府早於劉銘傳現代化建設。','題目排在臺事蹟，不是排表格或廳堂樓層。']},'rationale':'實看完整原卷閱讀說明、四人物表與51題四選項，讀來源51題原解。臺北文化局正文核1875沈葆楨設臺北府與1885劉銘傳建設背景，市府歷任市長正文核1951吳三連；郭錫瑠18世紀由市府官方志書及圖書館官方搜尋摘要核對，不爭論本題無需的開圳不同階段年度。新製精確事蹟排序SVG，不生成人物肖像，不當成年份同尺度數線。D不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-063-source-f37bd59c23.jpg','site/dist/sources/6ae0534e-2698-83ec-9f59-eecd8dafed5d.txt lines 1729–1790'],'sourceUrl':'https://chatgpt.com/share/6ae0534e-2698-83ec-9f59-eecd8dafed5d','sources':[{'url':'https://culture.gov.taipei/cp.aspx?n=EA99D09460E4AFB8','note':'正文286、289行實讀1875沈葆楨臺北府、1885後劉銘傳建設。'},{'url':'https://www.gov.taipei/cp.aspx?n=C1304E1985BE745E','note':'正文737–739行實讀民國40年吳三連當選民選首任市長。'},{'url':'https://tpml.gov.taipei/News_Content.aspx?n=16B1C97B7BB71624&s=544120F5DF33136F&sms=72544237BBE4C5F6','note':'官方搜尋摘要載1739開始／1767後續幹線完成，均18世紀；正文後續定位逾時，不冒稱已讀其整段。'},{'url':'https://www.th.gov.tw/Epaper_Content/236/6901/','note':'文獻館官方搜尋摘要載1887劉銘傳鐵路；直接頁面只回sys-root外殼，不冒稱正文可讀。'}],'generationMethod':'precise native SVG historical event sorting cards and extremes-first strategy','answerCheckedAgainst':'郭18世紀 < 沈1875 < 劉1880年代 < 吳1951，原代號乙甲丁丙D；以事蹟而非生卒或樓層。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-063.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
