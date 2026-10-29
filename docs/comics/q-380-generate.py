from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def t(x,y,z,size=10,c='#284d4c'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eef3e6","#eaf1f5","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'從原行程地名定位',11)
  for y,z in [(36,'四草砲臺'),(64,'鹿耳門溪口'),(92,'鹿耳門天后宮、安平')]:box(11,y,158,23,'#dde8d1');t(90,y+16,z,10)
  s.append(f'<path d="M{o+90} 119v10m-3-3 3 3 3-3" fill="none" stroke="#6d8c82"/>');box(25,138,130,30,'#aac89a');t(90,158,'臺南 → 南部',14)
 elif i==1:
  t(90,18,'回表找出南部的代號',10);t(90,39,'人口占全臺比例',9);t(57,58,'1893',9);t(106,58,'2010',9)
  for y,a,b,c,d in [(75,'甲','30%','45%','北'),(98,'乙','0%','2%','東'),(121,'丙','43%','28%','南'),(144,'丁','27%','25%','中')]:
   if a=='丙':box(8,y-16,164,22,'#bfd6a7')
   t(20,y,a,12);t(57,y,b,11);t(106,y,c,11);t(155,y,d,11)
  t(90,174,'比例＋開發史等線索合看',9)
 else:
  t(90,18,'比例變小，數量未必減少',10);t(90,38,'假設例，非臺灣歷史人口',8)
  box(12,51,156,43,'#e3ecd7');t(90,68,'全體100人，占43%',11);t(90,86,'區域人口＝43人',12)
  s.append(f'<path d="M{o+90} 99v10m-3-3 3 3 3-3" fill="none" stroke="#8b9585"/>')
  box(12,117,156,43,'#d0dfb7');t(90,134,'全體200人，占28%',11);t(90,152,'區域人口＝56人',12)
  t(90,176,'43% → 28%，43人 → 56人',9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-380.svg';Path(art).write_text(''.join(s))
assert 100*.43==43 and round(200*.28)==56
Path('docs/comics/q-380-data-validation.json').write_text(json.dumps({'source1893':[30,0,43,27],'source2010':[45,2,28,25],'sums':[100,100],'regionMapping':{'甲':'北','乙':'東','丙':'南','丁':'中'},'mappingRequiresHistoricalAndGeographicalContext':True,'notSolePercentageDeduction':True,'hypotheticalCountExample':{'populationTotals':[100,200],'regionShares':[43,28],'regionCounts':[43,56]},'hypotheticalNotHistoricalCounts':True,'itineraryOnlyUsesOriginalPlaces':True,'noInventedRouteOrDistance':True},ensure_ascii=False,indent=2)+'\n')
x={'id':'q-380','subject':'Geography','title':'先定位臺南，再回表找南部代號','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-380-generate.py','startedAt':'2026-10-29T06:51:53.976843+00:00','panels':[{'heading':'① 四草、鹿耳門、安平，指向臺南','text':'從原行程找地名：四草砲臺、鹿耳門溪口、鹿耳門天后宮與安平都在臺南一帶。先定位為南部，再查表找代號；不必把行程沒有列的景點補進來。','alt':'新原生地名線索卡集中指向臺南南部，未冒充實際路線圖，不新增景點或猜距離。'},{'heading':'② 回到表格，丙對應南部','text':'合看開發史與人口分布：南部早期開發較早，丙在1893年占43%，後降至2010年的28%；甲後期占比上升對應北部，乙對應東部，丁對應中部。因此臺南行程選丙，也就是C。','alt':'新原生表格核對1893/2010四區人口份額30/45、0/2、43/28、27/25；丙南高亮，合看歷史地理脈絡不把比例單獨當唯一證明。'},{'heading':'③ 人口占比下降，不等於人口變少','text':'比例的分母是全臺人口。用假設例來看：全體100人時，43%是43人；全體增加為200人時，28%是56人。比例雖降，區域人數仍可能增加，不能只看占比就判人口減少。','alt':'新原生純假設100×43%=43與200×28%=56，明示非歷史人數，說明分母變動；無虛構真實人口時間序列。'}],'fourth':{'answer':'答案：C，丙（南部）','points':['原行程地名定位臺南，屬南部。','結合開發史與表格，南部對應丙。','人口份額與實際人口數要分開判讀。']},'protectedWords':['四草砲臺','鹿耳門溪口','鹿耳門天后宮','1893年','2010年','43%','28%','100人','200人','43人','56人','臺南','南部','北部','東部','中部'],'rationale':'親見原卷56完整四項、原行程必要附圖與共用表七，數值完整核對。官方台江一日遊/四草村史佐證臺南地名。新原生定位卡＋兩年比例表＋假設人數反例比人物更能教定位/代號/份額差別，無來源AI也不加原AI誤添景點。','promptSummary':'新原生三格：原行程地名匯入臺南南部；表七1893/2010數值與四區代號；明示假設的比例下降人數增加反例。','answerCheckedAgainst':'原卷行程四草/鹿耳門/安平，表丙43%→28%，結合臺灣早期南部開發與人口北移脈絡核C，四選項甲乙丙丁不改。','officialReferences':[{'title':'台江國家公園・一日遊行程','url':'https://www.tjnp.gov.tw/ch/sglarticle/one-day-tour-itinerary-1'},{'title':'台江國家公園・四草村','url':'https://www.tjnp.gov.tw/ch/sglarticle/sicao-village'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-380-table-82d7a637b7.jpg','site/dist/assets/questions/q-380-source-8bbf3e76d7.jpg'],'necessaryFigures':['site/dist/assets/questions/q-380-figure-2186211422.jpg'],'visualChecked':True,'answer':'C','notes':'三圖均實看，原表七兩年值對應，原行程地名核對；不加億載金城/德記洋行/安平古堡。假設例非歷史人數。'},'dataValidation':'docs/comics/q-380-data-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-380.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
