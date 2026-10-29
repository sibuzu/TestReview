from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="flow" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="#438eaa"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,size=11,c='#294f50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def rect(x,y,w,h,fill='#dce9dc'):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}"/>')
 def box(y,z):rect(11,y,158,30);t(90,y+20,z,12)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#f5eee2","#eaf2f4","#edf0e5"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,19,'先讀題組，再看甲點',11)
  rect(15,31,150,124,'#fffdf5')
  for y,z in [(54,'題組：濁水溪水系'),(86,'圖中：甲點水庫'),(118,'任務：核對四個名稱')]:t(90,y,z,11)
  t(90,173,'位置以原卷必要圖為準',9)
 elif i==1:
  t(90,18,'引水關係：非地理比例',10)
  rect(8,35,72,25,'#d2e7ef');t(44,52,'濁水溪',11)
  rect(8,82,72,26,'#ded4bb');t(44,100,'武界壩',11)
  rect(8,138,72,26,'#d2e7ef');t(44,156,'主流續行',10)
  rect(113,82,61,27,'#c6e5ec');t(143.5,100,'日月潭',11)
  for x1,y1,x2,y2 in [(44,60,44,80),(44,108,44,136),(80,95,111,95)]:s.append(f'<path d="M{o+x1} {y1}L{o+x2} {y2}" stroke="#438eaa" stroke-width="2.5" marker-end="url(#flow)"/>')
  t(131,72,'引水道',9);t(126,137,'離槽水庫',10)
  s.append(f'<path d="M{o+143} 110V122" stroke="#7b9d9a"/>')
  t(90,178,'主流不直接流入日月潭',9)
 elif i==2:
  t(90,19,'水庫與水系配對',11)
  for j,(a,b) in enumerate([('A 翡翠','淡水河系'),('B 曾文','曾文溪'),('C 德基','大甲溪'),('D 日月潭','引濁水溪水')]):
   y=31+j*33;rect(6,y,168,29,'#c1d7ad' if j==3 else '#e3e6d8');t(47,y+19,a,10);t(129,y+19,b,10)
  t(90,178,'本題選 D，保留原卷圖的位置',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-367.svg');a.write_text(''.join(s))
d={'id':'q-367','subject':'Geography','title':'同屬濁水溪系統，不等於主流穿過潭面','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-367-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 題組已告訴你：這是濁水溪水系','text':'先連同共同說明讀題：原圖是濁水溪水系圖，再找甲點對應的水庫。不能只憑水庫名稱或都在山區，就把另一個河系的水庫放到這裡。位置仍以原卷附圖為準。','alt':'新製讀題資訊卡只列濁水溪水系、甲點、水庫名稱任務，不重畫或擅改必要原圖地理位置。'},
{'heading':'② 日月潭靠引水道連結濁水溪','text':'日月潭是離槽水庫：濁水溪的水經武界壩與引水道送入日月潭蓄存。它不是把濁水溪主流直接攔成整個潭面。關係圖只示引水連結，不表示真實方位或各水流的比例。','alt':'新精確拓樸圖濁水溪至武界壩，主流繼續往下游，側支引水道至日月潭，避免畫成天然主河道流經潭面。'},
{'heading':'③ 把四個選項各自配回水系','text':'翡翠屬淡水河水系，曾文屬曾文溪，德基屬大甲溪，都不符合題組給的濁水溪。日月潭從濁水溪引水，與原圖甲點及題設相符，因此選D。','alt':'新製四水庫水系對照：翡翠淡水河系、曾文曾文溪、德基大甲溪、日月潭引濁水溪水，D突出。'}],
'fourth':{'answer':'答案 D：日月潭水庫','points':['濁水溪水系是題組提供的重要線索。','武界壩透過引水道，把水送入日月潭。','離槽水庫不是天然主流直接流過潭面。']},
'protectedWords':['濁水溪','日月潭','武界壩','引水道','離槽水庫','淡水河','曾文溪','大甲溪','日月潭水庫','翡翠','甲點'],
'originalChecked':{'images':['site/dist/assets/questions/q-367-reading-a0cc5c5c48.jpg','site/dist/assets/questions/q-367-source-7dfbce1bb1.jpg'],'necessaryFigures':['site/dist/assets/questions/q-367-figure-5d80a56c4d.jpg'],'visualChecked':True,'answer':'D','notes':'共同說明與水系圖、甲點、原62四項均親見；D為使用者已明確確認，不重開原AI曾文B誤答或既有離槽釐清。'},
'sourceUrl':'https://chatgpt.com/share/6ae05276-e754-83ee-a87a-569980550954','answerCheckedAgainst':'使用者已確認D；官方觀光署原文濁水溪未直接流入日月潭、武界引水及水利署武界壩運用主文第一三點核對。',
'references':[{'title':'水力發電：日月潭國家風景區管理處','url':'https://www.sunmoonlake.gov.tw/zh-tw/guides/ArticlesText?a=35','supports':'濁水溪本不直接流入日月潭，武界引水蓄潭','access':'web主文抽取不完整，另以Python urllib取官方HTML實讀潭水哪裡來段；不引用該頁不同河長數字'}, {'title':'武界壩水庫運用要點','url':'https://www.wra.gov.tw/wralaw/Law_Content.aspx?n=9302&s=10844&sms=9191','supports':'濁水溪上游武界壩水量引注日月潭','access':'web工具逾時後urllib完整HTML實讀第一至四點'}, {'title':'翡翠水庫','url':'https://www.wra.gov.tw/wranb/News_Content.aspx?n=36734&s=189890','supports':'北勢溪/新店溪屬淡水河系','access':'Python urllib官方HTML主文實讀'}, {'title':'德基水庫集水區組織沿革','url':'https://web.wra.gov.tw/techi/cp.aspx?n=7535','supports':'德基大甲溪','access':'官方搜尋摘要，web抽取未含主文，不冒稱全文'}, {'title':'曾文水庫','url':'https://www.wra.gov.tw/wrasb/cp.aspx?n=31313','supports':'曾文溪水系','access':'官方搜尋主文摘要，web頁逾時未冒稱全文'}],
'rationale':'原題易誤把流域相關水庫當主流直接穿越，以精確拓樸和水系對照防誤解；不生成改形的臺灣地圖或攔河位置。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'D','edges':[['濁水溪','武界壩'],['武界壩','主流續行'],['武界壩','日月潭']],'directMainstreamIntoLake':False,'arrowMeansFlowProportion':False,'geographicScale':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
Path('docs/comics/q-367.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
