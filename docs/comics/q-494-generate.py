from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11,c='#34564b'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="{c}">{z}</text>')
 def r(x,y,w,h,c='#d2e1c3'):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf3e9","#f8efdf","#ebf1ec"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'A的兩個要點，都見於甲文',10)
  r(8,35,164,28);t(90,54,'獨立發展',14)
  t(90,83,'＋',17);r(8,96,164,29);t(90,115,'適於熱帶及亞熱帶',12)
  t(90,145,'↓',16);r(35,151,110,24,'#b6cda4');t(90,168,'直接對應 A',12)
 elif i==1:
  t(90,18,'第4個有範圍限制',11)
  r(6,33,168,113,'#e2dfd4');t(90,52,'全部綠建築評估系統',10)
  r(21,70,138,58,'#c8d9b4');t(90,91,'其中：具科學量化者',10);t(90,115,'原文說第 4 個',13)
  t(90,163,'不能放大成所有系統的排名',9);t(90,178,'框只示範圍，不表示實際數量比例',8)
 elif i==2:
  t(90,18,'B、D與甲文明文相反',11)
  for y,z1,z2 in [(35,'原文：獨立發展','B：全盤移植美國'),(102,'原文：在英、美、加之後','D：全球首套')]:
   r(7,y,166,54,'#d9e3cf');t(90,y+20,z1,10);t(90,y+43,z2,10)
  t(90,178,'只依本篇資訊，不冒充今日統計',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-494.svg');a.write_text(''.join(s))
d={'id':'q-494','subject':'Chinese','title':'A對應明文，C不能擴張具科學量化的範圍','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-494-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 獨立發展、適於熱帶亞熱帶，直接對應A','text':'甲文明寫臺灣系統獨立發展，且適於熱帶與亞熱帶。A把這兩個要點放在一起，兩者都有文字依據。閱讀題先找能直接對應原文的敘述，不先加入自己推測的排名或制度來源。','alt':'新精確兩條明文加總對應A的關係圖，不用虛構建築取得標章或今日制度。'},
{'heading':'② C漏掉具科學量化的比較範圍','text':'原文第4個實施，限定的是具科學量化的系統；C卻擴成全世界系統實施時間第四長。關鍵是比較範圍被放大，不是先後與多久永遠無關。相同群體、持續實施且同時點比較，兩者可以有關。','alt':'新精確外框全部系統、內框具科學量化者，原文第4個限內框；框面積不代表數量百分比，不畫錯誤年表。'},
{'heading':'③ B的全盤移植、D的全球首套均不合文意','text':'原文稱獨立發展，B說全盤移植美國，方向相反；甲文已說在英、美、加之後，D說全球首套，也不合。文中29套、目前等資訊仍屬文章情境，不拿來宣稱今天最新制度統計。','alt':'新兩組原文與選項矛盾對照，獨立對移植、先有三國對首套，未新增實施年份或當前評估規定。'}],
'fourth':{'answer':'答案 A：獨立發展且適用熱帶與亞熱帶','points':['兩個條件都能直接在甲文找到。','C不能省掉具科學量化的範圍限制。','B、D與明文相反；不拿文章數據當今日現況。']},
'protectedWords':['獨立發展','熱帶','亞熱帶','具科學量化','第4個實施','實施時間','第四長','比較範圍','全盤移植美國','全球首套'],
'originalChecked':{'images':['site/dist/assets/questions/q-494-reading-source-aac84df9e9.jpg','site/dist/assets/questions/q-494-source-4ba6ad40d7.jpg'],'visualChecked':True,'answer':'A','notes':'親見甲乙完整材料與九指標表、27四項；本題僅問甲文。按獨立/適於/具科學量化限定核A；不重開既有C先後與多久關係的解說，也不改乙表或當前技術標準。'},
'sourceUrl':'https://share.gemini.google/4TSQakuIUwvo','answerCheckedAgainst':'原甲文和四項逐句比對，A兩要點明文成立；C的問題限範圍擴張，不錯稱先後與多久一定無關。',
'rationale':'用明文加總與集合範圍框清楚呈現閱讀推論，比人物或標章建築示意更能定位C的範圍問題；無新增當前綠建築標準、法律或世界排名。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'A','directSourcePoints':['獨立發展','適於熱帶及亞熱帶'],'fourthRestrictedToQuantitativeSystems':True,'setAreaRepresentsCount':False,'startOrderAlwaysUnrelatedToDuration':False,'todaySystemCountAsserted':False,'newStandardOrCertificationClaim':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-494.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
