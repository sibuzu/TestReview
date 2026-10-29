from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11,c='#34554c'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="{c}">{z}</text>')
 def r(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#f8efdf","#edf2e7","#eaf0ed"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'比較範圍：東南亞來源',11)
  r(8,33,164,35,'#e3e0d6');t(90,55,'中國（含港澳）67%',11)
  t(90,83,'不納入這一題的東南亞比較',9)
  r(8,98,164,55,'#c7d9b7');t(90,119,'越南 19%',14);t(90,144,'印尼 6%',13)
  t(90,177,'原文列舉來源，未重算分母',9)
 elif i==1:
  t(90,18,'東南亞兩來源，同尺度比較',10)
  for y,name,value in [(47,'越南',19),(91,'印尼',6)]:
   t(26,y+16,name,11);s.append(f'<rect data-country="{name}" data-percent="{value}" x="{o+50}" y="{y}" width="{value*5}" height="21" fill="{"#88b183" if value==19 else "#b9c7ae"}"/>');t(50+value*5+14,y+16,f'{value}%',10)
  s.append(f'<path d="M{o+50} 125H{o+150}" stroke="#9ba894"/>')
  for v in [0,10,20]:x=50+5*v;s.append(f'<path d="M{o+x} 125V129" stroke="#9ba894"/>');t(x,142,f'{v}%',9)
  t(90,163,'分母：全部新住民',10);t(90,178,'數據沿原題 2024 年底情境',8)
 elif i==2:
  t(90,18,'先選國名，再回原圖標號',10)
  for y,z in [(34,'越南：中南半島東側'),(78,'狹長沿海，不是內陸寮國'),(128,'原圖丁 → 選 D')]:r(8,y,164,29,'#c4d8b3' if y==128 else '#d9e4d3');t(90,y+20,z,11 if y!=78 else 10)
  t(90,119,'↓',14);t(90,177,'保留原卷國界圖，不另畫國界',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-839.svg');a.write_text(''.join(s))
d={'id':'q-839','subject':'Geography','title':'先限定東南亞來源，再把越南對回丁','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-839-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 問東南亞來源，不是全部來源最大者','text':'文章說中國含港澳占67%，但本題限定東南亞來源。先在正確範圍找答案：文中列出的越南19%、印尼6%，越南較多；不能因67%最大，就忽略題目限定。','alt':'新精確比較範圍圖將中國含港澳67%與東南亞越南19印尼6分開，不修改原題分類或冒充完整來源分布。'},
{'heading':'② 19%大於6%，先選出越南','text':'原文越南19%、印尼6%共用全部新住民這個分母，不能改說成越南占東南亞新住民19%。依文章提供的東南亞來源比較，先選越南，再處理地圖位置。數據仍是原題2024年底情境。','alt':'新精確零基準同尺度長條19與6，單位%、每百分點5圖像單位，明示分母全部新住民及原題2024年情境，不換當前統計。'},
{'heading':'③ 越南在半島東側沿海，原圖標丁','text':'越南沿中南半島東側海岸狹長分布，原圖對應丁，因此選D。甲是緬甸、乙是泰國、丙是內陸寮國，別把乙猜成越南或柬埔寨。國界與標號仍以原題附圖核對。','alt':'新國名至地理特徵至丁D的精確資訊鏈，沒有AI重畫中南半島國界或對人物外觀作國籍推論，必要原圖保留。'}],
'fourth':{'answer':'答案 D：丁（越南）','points':['先看題目限定的東南亞來源。','依原文越南19%與印尼6%比較，先選越南。','回地圖找東側狹長沿海的丁，不把百分比分母改掉。']},
'protectedWords':['東南亞','中國含港澳','67%','越南19%','印尼6%','全部新住民','2024年底','越南','中南半島','狹長沿海','內陸寮國','緬甸','泰國','柬埔寨'],
'originalChecked':{'images':['site/dist/assets/questions/gemini062-63520bbebea1fd.jpg','site/dist/assets/questions/gemini062-ceb10fdc6eb356.jpg'],'necessaryFigures':['site/dist/assets/questions/gemini062-d39b8c13f0ab9a.jpg'],'visualChecked':True,'answer':'D','notes':'親見三階段表全文/2024年底約60萬與67、19、6等表後文/45四項及甲緬甸乙泰國丙寮國丁越南地圖。原紅D，按題目東南亞限定與原圖核。'},
'sourceUrl':'https://share.gemini.google/lEdStGcomTed','answerCheckedAgainst':'原紅D、原表後19%越南大於6%印尼且分母全部新住民，原圖丁位東側沿海；外交部地理位置主文佐越南狹長東側位置。',
'references':[{'title':'外交部：越南國家資料','url':'https://www.mofa.gov.tw/CountryInfo.aspx?CASN=5&n=5&s=128&sms=33','supports':'位於中南半島東側，西臨寮國柬埔寨，東濱海而全境狹長','access':'官方HTML urllib實讀地理位置主文，未引用頁面當前人口外交政策等資料'}],
'rationale':'精確範圍篩選與同尺度百分比條圖解決主要讀題錯誤，再回必要原圖定位；不AI重畫國界、不用各族人物外觀影射來源、不把2024題內數字當今天最新統計。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'D','country':'越南','originalMapLabel':'丁','percentages':{'中國含港澳':67,'越南':19,'印尼':6},'barBaseline':0,'barUnitsPerPercent':5,'barSourceDenominator':'全部新住民','chartShowsOnlyTwoNamedSEAsianSources':True,'inventedFullSourceDistribution':False,'currentStatsAsserted':False,'countryBordersRedrawn':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-839.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
