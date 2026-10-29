import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#588365"/></marker></defs>']
def rect(x,y,w,h,fill='#faf8ee',r=7):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="#b7cbbd"/>')
def txt(x,y,t,size=17,c='#2c4c39',wt=500):s.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" fill="{c}" font-weight="{wt}">{escape(t)}</text>')
for i in range(3):rect(i*200+2,2,196,196)
txt(100,22,'1872',26,wt=700)
rect(24,47,152,75,'#e3ecf2');txt(100,67,'李仙得',22);txt(100,96,'日本外務省顧問',16)
s.append('<path d="M100 125V149" stroke="#588365" stroke-width="3" marker-end="url(#a)"/>');txt(100,173,'出兵建議 ≠ 已併吞',15,c='#946b43')
txt(300,22,'1874 牡丹社事件',18,wt=700)
rect(216,44,168,43,'#efe4d5');txt(300,65,'藉口琉球漂民遇害',15)
s.append('<path d="M300 89V109" stroke="#588365" stroke-width="2" marker-end="url(#a)"/>')
rect(216,115,168,47,'#e1eddc');txt(300,139,'D 出兵南臺灣',19,wt=700)
txt(300,183,'比1895年乙未戰爭更早',13,c='#946b43')
txt(500,21,'四項依時序排列',17,wt=700)
for i,(lab,yr,event) in enumerate([('D','1874','牡丹社'),('C','1894','甲午'),('B','1895','乙未'),('A','二戰','南洋作戰')]):
 y=40+i*35;rect(410,y,180,29,'#e0eddd' if i==0 else '#edf0e8');txt(426,y+15,lab,17,c='#367d53' if i==0 else '#667466',wt=700);txt(472,y+15,yr,17);txt(548,y+15,event,15)
s.append('</svg>');Path('docs/comics/art/q-546.svg').write_text(''.join(s))
spec={'id':'q-546','subject':'History','title':'題目問率先，先把四項排出年代','art':'docs/comics/art/q-546.svg','protectedWords':['李仙得','外務省顧問','牡丹社事件','琉球漂民','南臺灣','甲午戰爭','乙未戰爭','臺灣民主國','第二次世界大戰','1872','1874','1894','1895','率先'],'panels':[{'heading':'① 先抓1872年，不把建議當既成事實','text':'題幹從李仙得成為日本外務省顧問談起，問日本隨後率先發動哪一行動。引述的是擴張建議，不代表當時已完成併吞所提到的各地。','alt':'1872顧問身分資料卡往下指向建議，不畫各地已被征服或不實疆界，也不虛構歷史人物肖像。'},{'heading':'② 直接接到1874年出兵南臺灣','text':'日本以琉球漂民遇害為藉口，於1874年出兵南臺灣，對應牡丹社事件，也就是D。要分清1871年漂民遇害，與1874年日本出兵是不同時間點。','alt':'1874牡丹社事件卡，琉球漂民遇害作出兵藉口而非同年事件標示；箭頭僅連政策利用，不把遇害與出兵畫成同時。'},{'heading':'③ 排序比對：其他三項都較晚','text':'D在1874年；C的甲午戰爭始於1894年；B臺灣民主國抗日是在1895年乙未戰爭時期；A南洋作戰屬第二次世界大戰背景，所以率先是D。','alt':'四選項按D1874/C1894/B1895/A二戰先後排列表格，不把相同列高誤當同尺度年距。'}],'fourth':{'answer':'答案 D：1874年出兵南臺灣','points':['1872受聘顧問後，比對直接後續事件。','1871遇害與1874出兵不可混成一年。','只因都涉及日本擴張，不能忽略率先的時序。']},'rationale':'實看第42題完整題文與四選項，讀原AI第42題全段；原民會文獻及臺史博官方材料核對1871遇害、1874出兵、1894甲午、1895乙未及二戰動員。新製精確事件比較SVG，避免生成人物肖像、軍服、侵略疆域等難以核對的情境。保留D不新增原題訂正，1871只作核清事件分期。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-546-source-aea91e1f6b.jpg','site/dist/sources/gemini-5WMxlYMpeJnK.txt lines 75–97'],'sourceUrl':'https://share.gemini.google/5WMxlYMpeJnK','sources':[{'url':'https://ihc.cip.gov.tw/EJournal/EJournalCat/99','note':'官方文獻正文實讀1871琉球人遇難、1874遠征軍及事件分期；1872顧問段另由官方搜尋全文摘要核對。'},{'url':'https://collections.nmth.gov.tw/CollectionContent.aspx?a=132&rno=2009.011.0351','note':'臺史博典藏正文141行實讀1894甲午因朝鮮問題、1895馬關條約。'},{'url':'https://the.nmth.gov.tw/nmth/zh-TW/Location/0efd8ce3-ca00-4bcb-8e30-af9a7e9df4b6','note':'臺史博鉅變1895主題官方頁及搜尋摘要，臺灣民主國與民眾抗日脈絡。'},{'url':'https://the.nmth.gov.tw/nmth/zh-TW/Location/e7a16806-c58a-45ee-b983-3d2eaa86d98a','note':'臺史博正文實讀二戰社會轉為戰爭動員與臺灣人走向戰場；未添本題未要求的精確徵召年度。'}],'generationMethod':'precise native SVG historical action chronology and proposal-versus-result distinction','answerCheckedAgainst':'1872後四項最早D1874，C1894、B1895、A二戰皆晚；不把日本所有擴張當同時。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-546.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
