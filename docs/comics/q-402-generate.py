import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#5a8164"/></marker></defs>']
def rect(x,y,w,h,fill='#faf8ee',r=7):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="#b7cbbb"/>')
def txt(x,y,st,size=17,c='#2c4d39',wt=500):s.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" fill="{c}" font-weight="{wt}">{escape(st)}</text>')
for i in range(3):rect(i*200+2,2,196,196)
txt(100,22,'1683 · 澎湖',24,wt=700)
rect(17,48,166,49,'#e2edf3');txt(100,64,'清軍水師',17);txt(100,84,'擊敗鄭氏水軍',16)
s.append('<path d="M100 101V125" stroke="#5a8164" stroke-width="3" marker-end="url(#a)"/>')
rect(17,137,166,44,'#e2eddf');txt(100,159,'鄭氏投降',21,wt=700)
txt(300,23,'戰後：如何處理臺灣？',15,wt=700)
rect(237,46,126,36,'#e3edf2');txt(300,64,'清廷討論',19)
s.append('<path d="M300 84V103H250V120M300 103H350V120" fill="none" stroke="#6b8a72" stroke-width="2"/>')
rect(213,121,75,48,'#f1e4d3');txt(250,145,'棄',28,c='#986e43')
rect(312,121,75,48,'#dfeadc');txt(350,145,'留',28,c='#397a50')
txt(300,185,'B 臺灣棄留爭議',17,wt=700)
txt(500,21,'先配對時代，再看因果',14,wt=700)
for i,(lab,period,event) in enumerate([('A','荷鄭交替','較早'),('B','清初','本題'),('C','日治','較晚'),('D','二戰後','較晚')]):
 y=40+i*35;rect(410,y,180,29,'#e0eddf' if i==1 else '#edf0e6');txt(424,y+15,lab,17,wt=700);txt(486,y+15,period,16);txt(561,y+15,event,15,c='#397a50' if i==1 else '#7b775f')
s.append('</svg>');Path('docs/comics/art/q-402.svg').write_text(''.join(s))
spec={'id':'q-402','subject':'History','title':'清軍戰勝鄭氏後，才問臺灣留不留','art':'docs/comics/art/q-402.svg','protectedWords':['澎湖海戰','劉國軒','鄭氏投降','清廷','臺灣棄留','荷鄭交替','總督府','行政長官公署','1683','二戰後'],'panels':[{'heading':'① 先辨識：1683年的澎湖海戰','text':'題幹的1683年、澎湖與劉國軒，指向清軍水師擊敗鄭氏水軍，接著鄭氏投降。先把事件放回清初，不要與較早的荷鄭交替混在一起。','alt':'1683澎湖關鍵線索及清軍水師擊敗鄭氏水軍、鄭氏投降的先後卡；不假造實際交戰船數、肖像或戰場地理。'},{'heading':'② 問後續影響：清廷討論棄留','text':'戰勝後要處理的是臺灣是否保留、如何治理。清廷內部出現棄留討論，正是B。不能把後來其他政權的接收機關，移到清初來回答。','alt':'清廷討論框分到棄與留兩個分支，表達爭議而不是所有人立場一致；不虛構官員名單或具體會議畫面。'},{'heading':'③ 四項都像政權轉換，年代卻不同','text':'A屬較早的荷鄭交替；C的總督府是日治統治機關；D的行政長官公署屬1945年戰後接收。它們不是這次清軍戰勝鄭氏後的直接影響。','alt':'A荷鄭較早／B清初本題／C日治較晚／D二戰後較晚對照表，依時代辨析而非暗示所有轉換同時發生。'}],'fourth':{'answer':'答案 B：臺灣棄留問題成為爭議焦點','points':['1683澎湖海戰，清軍戰勝鄭氏。','鄭氏投降後，清廷討論臺灣棄留。','先排時代與政權，再判斷戰事後的直接影響。']},'rationale':'實看原卷第34題完整題文及四選項、讀來源完整本題解答。桃園市文化資源官方大事紀核1683棄留討論；臺史博總督府典藏與國家檔案接收原始訓令資料核不同時代機關。新原生SVG呈現事件順序、棄留分支與時代配對，避免生成不實戰場或歷史人物。B答不變，不更改原題政治用語或額外推測清廷各人立場。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-402-source-755ee0c301.jpg','site/dist/sources/6ae0533b-4b48-83ec-ba36-0b7b3759f90a.txt lines 1684–1754'],'sourceUrl':'https://chatgpt.com/share/6ae0533b-4b48-83ec-ba36-0b7b3759f90a','sources':[{'url':'https://daxiculture2.tycg.gov.tw/memorabilia?id=1298','note':'官方大事紀1683清廷臺灣棄留討論與施琅上疏；網頁已取回，搜尋摘要對應。'},{'url':'https://collections.nmth.gov.tw/CollectionContent.aspx?RNO=T2018.001.3253&a=132','note':'臺史博官方典藏說明1895設立臺灣總督府。'},{'url':'https://art.archives.gov.tw/tw/art/1794-15264.html','note':'國家檔案原始訓令教學說明1945戰後接收總督府機關，非清初機構。'}],'generationMethod':'precise native SVG event succession, policy branches, and cross-era option comparison','answerCheckedAgainst':'1683澎湖海戰鄭氏降清後清廷討論棄留B；A更早、C日治、D二戰後，不同時代。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-402.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
