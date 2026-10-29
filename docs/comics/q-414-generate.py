from pathlib import Path
import math,json,hashlib
from decimal import Decimal
assert Decimal('81.9')+Decimal('18.1')==Decimal('100.0')
r=45;circ=2*math.pi*r;minor=circ*.181;major=circ*.819;assert math.isclose(minor+major,circ)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 def arrow(y):s.append(f'<path d="M{o+90} {y}v9m-3-3 3 3 3-3" fill="none" stroke="#819c99"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,19,['本題圖示：兩項都叫礦產品','從貨種，連回腹地產業','括號不是自行推論的憑據'][i],9)
 if i==0:
  s.append(f'<circle cx="{o+90}" cy="79" r="45" fill="none" stroke="#91ae70" stroke-width="18"/><circle cx="{o+90}" cy="79" r="45" fill="none" stroke="#6798ac" stroke-width="18" stroke-dasharray="{minor} {circ-minor}" transform="rotate(-90 {o+90} 79)"/>')
  txt(90,77,'礦產品',13);txt(90,94,'2014年題圖',8)
  box(16,140,9,9,'#91ae70');txt(97,149,'（國內）81.9%',11);box(16,159,9,9,'#6798ac');txt(97,168,'（國外）18.1%',11)
 elif i==1:
  for yy,a,b in [(37,'東部腹地','礦產與相關加工產業'),(86,'貨物特色','石材、砂石、水泥等'),(135,'本題港口判讀','花蓮港')]:
   box(12,yy,156,33,'#d7e6c8' if yy==135 else '#f8faf4');txt(90,yy+13,a,8);txt(90,yy+27,b,11)
   if yy<135:arrow(yy+36)
 elif i==2:
  box(13,39,154,34,'#dbe6d2');txt(90,52,'原圖括號',8);txt(90,68,'國內／國外',15);arrow(78)
  box(13,94,154,29,'#f6e5c5');txt(90,113,'圖未註明完整統計口徑',10)
  txt(90,149,'不能自行斷言原產地',11);txt(90,173,'也不能猜成外貨復出口',11)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-414.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-414-chart-validation.json').write_text(json.dumps({'sourcePeriod':2014,'sourceLabels':['礦產品（國內）','礦產品（國外）'],'sourcePercentages':[81.9,18.1],'exactDecimalSum':'100.0','newDonutArcsDegrees':[294.84,65.16],'twoLabelsSameCommodity':True,'minorSectorIsNotOtherGoods':True,'noOriginOrReExportInference':True,'notCurrentWholePortCargoClaim':True,'officialCargoEvidence':'花蓮港裝卸砂石/礦石/水泥等，官方設施/發展定位相合；不以新年統計取代2014題圖。'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-414','subject':'Geography','title':'先看礦產品貨種，再連花蓮的礦產腹地','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-414-generate.py','startedAt':'2026-10-29T06:34:40.875595+00:00','panels':[{'heading':'① 81.9與18.1兩部分，都是礦產品','text':'題圖標「礦產品（國內）81.9%」和「礦產品（國外）18.1%」。兩者合為100%，本題先抓共同貨種礦產品；小部分不是其他產品，也不能改成今天整個港口的貨運占比。','alt':'新精確環圖81.9/18.1，兩扇色皆礦產品，中心明2014題圖；比例由數值計算而非imagegen猜，不當今日全港貨種資料。'},{'heading':'② 礦產品，連到東部礦產與加工腹地','text':'花蓮及東部腹地有石材、石灰石等礦產與相關產業，花蓮港運輸礦石、砂石、水泥等貨物的特色最符合，故選B。解題是在比貨種與腹地，不是在選規模最大的港。','alt':'原生腹地產業→貨物特色→花蓮港流程，官方貨種特色支持，不畫虛構港界或礦點精確位置。'},{'heading':'③ 國內與國外，別擅自補成原產地','text':'圖中沒有註明這組括號的完整統計口徑，不能自行斷言18.1%是外國原料再出口。保留原標籤與2014年時點，作答依有根據的礦產品貨種與腹地關係。','alt':'國內/國外原標籤→口徑未註明→不猜原產地/復出口，保持既有已核對限制，無新不實統計方向箭頭。'}],'fourth':{'answer':'答案：B，花蓮港','points':['本題兩塊都屬礦產品，81.9%＋18.1%＝100%。','以花蓮東部礦產與相關產業，連到港口貨種特色。','不把國內、國外直接等同原產地，也不猜復出口。']},'protectedWords':['81.9%','18.1%','100%','2014年','礦產品','花蓮港','石灰石','原產地','統計口徑','復出口'],'rationale':'親見36全文四項及必要圖，兩標籤和81.9/18.1逐字核對，沿已確認B與既有口徑限制。官方港務/交通年鑑交叉核花蓮礦砂石水泥特色。新精確環圖/腹地貨種流程/口徑限制圖，避免imagegen造百分比或錯指18.1其他/外貨復出口，不用來源AI。','promptSummary':'新原生三格：依原數81.9/18.1的2014礦產品環圖；東部礦產腹地貨種港口連結；國內外口徑不臆測。精確文字原生，不假造當前貨運資料。','answerCheckedAgainst':'原卷36兩扇均礦產品，四港B花蓮；官方交通部及港務公司發展定位/裝卸設備支持礦砂石水泥，保留2014與國內外未明口徑限制。','officialReferences':[{'title':'交通部107年交通年鑑・港埠設施','url':'https://www.motc.gov.tw/uploaddowndoc?file=yearbook%2F107%2F107YB09%2F107YB090101.pdf&filedisplay=107YB090101.pdf&flag=doc'},{'title':'花蓮港務分公司・裝卸設備（砂石、礦石、水泥）','url':'https://hl.twport.com.tw/zh-TW/port/Articles?a=1107'},{'title':'臺灣港務公司・花蓮港發展定位','url':'https://www.twport.com.tw/fapi/AttFile?id=3518&l=1&type=AttFile'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-414-source-9517a58701.jpg'],'necessaryFigures':['site/dist/assets/questions/q-414-figure-98d7884893.jpg'],'visualChecked':True,'answer':'B','notes':'全題及必要百分比圖實看，兩項礦產品國內81.9/國外18.1無誤；已結案原AI錯口徑不重問，不新增當前礦產100%等全港概括。'},'chartValidation':'docs/comics/q-414-chart-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-414.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
