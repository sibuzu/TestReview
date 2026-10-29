from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><pattern id="h" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M-1 1L1 -1M0 5L5 0M4 6L6 4" stroke="#7d8c73" stroke-width="1"/></pattern><marker id="a" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0 0L4 2L0 4Z" fill="#739c8d"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="#35574e">{z}</text>')
 def sq(x,y,w):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{w}" fill="#e7e5d7"/><rect x="{o+x}" y="{y}" width="{w}" height="{w}" fill="url(#h)" stroke="#718571"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#faf0e1","#eaf0e7"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'先讀原圖圖例',12)
  s.append(f'<circle cx="{o+90}" cy="49" r="17" fill="#d4e2c7" stroke="#779b82"/>');t(90,81,'圓：各項成本因素',11)
  sq(75,103,30);t(90,154,'斜線方塊：工廠或生產基地',10)
  t(90,177,'先認符號，再比較哪個圓最大',8)
 elif i==1:
  t(90,18,'鮮乳供應，要連到消費者',10)
  s.append(f'<path d="M{o+80} 35H{o+100}V45L{o+108} 53V85H{o+72}V53L{o+80} 45Z" fill="#fffdf4" stroke="#9ea781" stroke-width="2"/><rect x="{o+79}" y="30" width="22" height="7" rx="2" fill="#acc4c0"/>');t(90,72,'鮮乳',11)
  t(90,112,'保鮮＋及時配送',13);s.append(f'<path d="M{o+90} 119V133" stroke="#739c8d" stroke-width="2" marker-end="url(#a)"/>')
  s.append(f'<rect x="{o+15}" y="139" width="150" height="25" rx="5" fill="#c8d9b8"/>');t(90,157,'消費市場',13)
  t(90,178,'本題分類：市場指向',9)
 elif i==2:
  t(90,18,'D：市場因素較突出',11)
  s.append(f'<path d="M{o+90} 73V92M{o+44} 107H{o+75}M{o+105} 107H{o+136}" stroke="#7e9688" stroke-width="1.7"/>')
  for x,y,rad,z in [(90,54,18,'市場'),(35,107,8,'技術'),(145,107,8,'資金')]:s.append(f'<circle data-factor="{z}" cx="{o+x}" cy="{y}" r="{rad}" fill="#bfd6ac" stroke="#759885"/>')
  t(90,31,'市場',11);t(35,132,'技術',10);t(145,132,'資金',10);sq(75,92,30);t(90,155,'工廠／生產基地',10);t(90,178,'大小只示突出因素，非實際百分比',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-837.svg');a.write_text(''.join(s))
d={'id':'q-837','subject':'Geography','title':'先認成本因素，再用鮮乳特性判市場指向','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-837-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 圓是成本因素，斜線方塊是基地','text':'先讀四圖旁的圖例：圓表示各項成本因素，斜線方塊表示工廠或生產基地位置。接著比較每個選項哪個因素圓最大，不要把最大的圓看成工廠規模或某一座城市。','alt':'新精確圖例：圓為成本因素、斜線方塊為基地，保留符號區別，不把圓當人口數或工廠。'},
{'heading':'② 鮮乳要保鮮、及時送到消費市場','text':'題目問這類商業化農業的區位類型。鮮乳需要保鮮與及時配送，消費市場對區位相當重要，因此依教材分類判斷為市場指向；不是看報導提到哪個縣市，就改選另一因素。','alt':'新原生鮮乳瓶至保鮮配送至消費市場的需求關係圖，無品牌、時事統計、保冷溫度時數或商品療效宣稱。'},
{'heading':'③ D的市場因素最大，最符合題意','text':'A突出原料，B突出勞工，C突出能源，D突出市場，所以選D。圖D其他兩個小圓是技術與資金。市場指向是相對分類，並非說牧場一定在都市內，或不用考慮土地、飼料與冷鏈。','alt':'新精確D關係示意保留市場大圓、技術資金小圓與斜線基地；不換成其他選項的原料勞工，不捏造實際成本百分比。'}],
'fourth':{'answer':'答案 D：市場指向','points':['讀圖例，找哪個成本因素最突出。','鮮乳保鮮及配送，連結消費市場需求。','D的市場因素最大；不代表牧場必在都市內。']},
'protectedWords':['商業化農業','成本因素','生產基地','消費市場','市場指向','鮮乳','技術','資金','原料','勞工','能源','冷鏈'],
'originalChecked':{'images':['site/dist/assets/questions/gemini062-b2f7eb56c7260d.jpg'],'necessaryFigures':['site/dist/assets/questions/gemini062-ef1f1ae84ebec6.jpg'],'visualChecked':True,'answer':'D','notes':'親見原34全報導/四圖/圓與斜線方塊圖例，A原料B勞工C能源D市場最大；D小圓技術資金，黑B紅D。題內政策當時情境原文保留，不當今日現況。'},
'sourceUrl':'https://share.gemini.google/lEdStGcomTed','answerCheckedAgainst':'原紅D與完整四圖逐項讀最大因素，鮮乳保鮮配送特性及原題商業化農業教材分類核D。',
'references':[{'title':'農業部公開：鮮乳產品生命週期材料','url':'https://agrinetzero.moa.gov.tw/zh-TW/UploadFile/Download/e8b1111c-93e0-41f4-b3c0-0ee10cc2ce91','supports':'配送銷售過程須冷藏，僅佐證保鮮配送特性，非區位選項的直接答案','access':'官方PDF下載確認檔頭並pdftotext實讀表1配送段與10.4；不提供飲用或冷藏操作數據，也不稱法規'}],
'rationale':'原題是抽象成本因素圖，精確圖例與D三因素關係可防把符號/最大因素讀反，比人物或乳牛場景更直接；不代替原題必要圖、不AI捏造百分比。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'D','dominantFactor':'市場','otherDFactors':['技術','資金'],'factorCircleRadius':{'市場':18,'技術':8,'資金':8},'circleSizeIsActualCostPercentage':False,'farmMustBeInCity':False,'policyCurrentStatusAsserted':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-837.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
