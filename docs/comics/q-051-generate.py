from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="a" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="#779a91"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11,c='#355a50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="{c}">{z}</text>')
 def r(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#f7efe0","#eef2e7","#ebf0ee"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,20,'原文第一句',11)
  r(14,35,152,45,'#fffdf5');t(90,53,'藝師館位於',11);t(90,71,'普濟路五十二號',12)
  r(12,95,90,35,'#d1dfc2');t(57,117,'路名：普濟路',10)
  r(108,95,60,35,'#dfd8b6');t(138,117,'52 號',13)
  t(90,157,'路名 ≠ 唯一館舍',12);t(90,174,'門牌仍須配合導覽圖核對',8)
 elif i==1:
  t(90,20,'對齊共同地標，再比較',10)
  t(43,42,'原卷圖',11);t(137,42,'官方圖',11)
  for j,z in enumerate(['大漢溪','普濟路','大溪國小']):
   y=54+j*34
   for x in [5,99]:r(x,y,76,25,'#d7e4ce');t(x+38,y+17,z,10)
   s.append(f'<path d="M{o+82} {y+12}H{o+97}" stroke="#779a91" stroke-width="1.5" marker-end="url(#a)"/>')
  t(90,174,'這是地標配對，非地理位置圖',8)
 elif i==2:
  t(90,20,'官方館名對回原卷區域',10)
  r(8,33,164,55,'#cbddba');t(90,52,'⑥ 藝師館 → C 區',13);t(90,75,'普濟路 52 號',10)
  r(8,101,164,55,'#e0dfd0');t(90,121,'⑫ 溪小宿舍 → B 附近',10);t(90,144,'普濟路 84 巷 3、4 號',10)
  t(90,175,'館舍編號來自補充官方圖',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-051.svg');a.write_text(''.join(s))
d={'id':'q-051','subject':'Geography','title':'先讀完整地址，用共同地標把兩張圖對齊','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-051-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 藝師館：普濟路五十二號','text':'文章第一句直接給出目的地與完整地址。找到普濟路是第一步，還要確認52號是哪一棟。原卷圖沒有逐棟標門牌，不能看到同一條路旁的館舍，就直接判定答案。','alt':'新地址拆讀圖把原文普濟路五十二號分成路名與52號兩塊，不推算不存在的地圖門牌刻度。'},
{'heading':'② 兩圖視角不同，先對齊共同地標','text':'補充官方導覽圖有館名，可用大漢溪、普濟路與大溪國小，和原卷圖交叉核對方向與位置。畫面左右不能直接對貼；必須先確認兩張圖講的是哪些相同地標。','alt':'新原生三組同名地標的配對關係圖，左右欄是原卷與官方圖，不代表地標真實上下方位或街廓距離。'},
{'heading':'③ 官方⑥藝師館，對應原卷C區','text':'官方圖的⑥藝師館與原卷C區相符；B附近則是⑫溪小宿舍，兩者不是同一棟。官方資料也可核對：藝師館在普濟路52號，溪小宿舍在普濟路84巷3、4號。這是解說補充，仍保留原題地圖。','alt':'新館名地址對照卡突出藝師館52號C，區別溪小宿舍84巷3及4號B附近；館舍編號引用親見官方補充圖，不是原卷自帶。'}],
'fourth':{'answer':'答案 C：C區','points':['文章給完整地址：普濟路五十二號。','共同地標對齊兩圖，不能只照畫面左右。','官方⑥藝師館與⑫溪小宿舍分開辨認。']},
'protectedWords':['藝師館','普濟路','五十二號','普濟路52號','普濟路84巷3、4號','大漢溪','大溪國小','溪小宿舍','C區','B附近'],
'originalChecked':{'images':['site/dist/assets/questions/q-051-reading-5453a670a8.jpg','site/dist/assets/questions/q-051-source-19858cdeee.jpg'],'necessaryFigures':['site/dist/assets/questions/q-051-figure-735915f833.jpg'],'supplementaryOfficialFigure':'site/dist/assets/questions/q-051-official-guide-6c49ed2255.jpg','visualChecked':True,'answer':'C','notes':'親見文章全文、28題四區與原卷地圖/官方彩色圖，⑥藝師館與⑫溪小宿舍對照確認。既有C不重問。兩圖方向不同，不能只依路名推門牌。'},
'sourceUrl':'https://chatgpt.com/share/6ae05238-7b84-83ec-b2f2-9a46aa7cb340','answerCheckedAgainst':'原卷28紅筆C、親見官方圖⑥藝師館/⑫溪小宿舍，官方館舍地址兩頁另實讀。',
'references':[{'title':'大溪木藝生態博物館：藝師館','url':'https://wem.tycg.gov.tw/Photo_News_Content_Museums.aspx?n=14933&s=1157540','supports':'藝師館普濟路52號','access':'官方HTML urllib主文地址段實讀'}, {'title':'大溪國小日式宿舍（溪小宿舍）','url':'https://wem.tycg.gov.tw/News_Content.aspx?n=14933&s=1462911&sms=17238','supports':'普濟路84巷3號、4號','access':'官方HTML urllib主文地址段實讀'}],
'rationale':'本題需學會比對不同視角真實導覽圖，精確地址拆讀與地標配對比人物情境更直接；新SVG不重畫街廓，不虛構門牌與館舍立體外觀。保留官方解說圖供逐點查核，不因新增四格刪去官方圖。',
'integrationNotes':{'preserveOfficialExplanationFigure':'assets/questions/q-051-official-guide-6c49ed2255.jpg','reason':'這是非AI官方必要補充材料，新四格是判讀方法，不取代真實地圖'},
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'C','artistHouse':{'guideNumber':6,'address':'普濟路52號','originalZone':'C'},'schoolDorm':{'guideNumber':12,'address':'普濟路84巷3、4號','originalZone':'B附近'},'anchorRowsAreGeographicPositions':False,'mapsHaveSamePageOrientation':False,'inventedDoorNumberOnOriginalMap':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
Path('docs/comics/q-051.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
