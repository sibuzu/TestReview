from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=9,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="Arial,sans-serif">')
 txt(90,20,['問題是水況改變，仍沿用舊法','用渡河失敗，類比照搬古法','「豈不悲哉？」是明確批評'][i],9)
 if i==0:
  for y,hh,caption in [(45,8,'先前：原標記可導'),(103,22,'後來：水已變而益多')]:
   box(21,y,138,37,'#fafbf8');s.append(f'<rect x="{o+21}" y="{y+37-hh}" width="138" height="{hh}" fill="#a9cbd3"/>');txt(90,y+14,caption,9)
  txt(90,165,'變的是水，未調整的是做法',10)
 elif i==1:
  txt(46,39,'故事',9);txt(134,39,'類比',9)
  for y,a,b in [(48,'水已變','時勢已變'),(89,'仍循舊標記','仍照搬古法'),(130,'渡河失敗','治理不合')]:
   box(10,y,72,26,'#d8e7ce');box(98,y,72,26,'#d3e0ea');txt(46,y+17,a,9);txt(134,y+17,b,9)
   if y<130:
    for xx in [46,134]:s.append(f'<path d="M{o+xx} {y+29}v7m-3-3 3 3 3-3" fill="none" stroke="#769295"/>')
  txt(90,174,'共同點：條件變，做法不變',9)
 else:
  for j,(a,b) in enumerate([('A','不明就裡：不懂內情'),('B','不置可否：不表態'),('C','不敢苟同：不能隨便贊同'),('D','不容分說：不許解釋')]):
   y=43+29*j;box(9,y,162,24,'#dce8cb' if a=='C' else '#f7f7f0');txt(90,y+16,a+' '+b,8)
  txt(90,174,'提出理由，反對機械照搬',10)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-522.svg';Path(art).write_text(''.join(s))
spec={'id':'q-522','subject':'Chinese','title':'用故事作類比，再讀出結尾反詰的態度','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-522-generate.py','startedAt':'2026-10-29T05:29:30.877276+00:00','panels':[{'heading':'① 原本可用，後來條件已改變','text':'先表之時可導，表示舊標記原本可以帶路。但「今水已變而益多」，楚軍仍循舊標記夜渡，造成失敗。作者批評的是不察變化，並非說標記一開始就毫無用處。','alt':'原生水況比較示意，先前低水、後來水增，不標虛構水深/時間或標記位置；文字清楚說原可導而後條件變。'},{'heading':'② 從水況改變，類比時勢改變','text':'「今世之主，法先王之法也，有似於此」把兩件事連起來：水變了卻循舊標記，好比時代條件不同，仍不調整地照搬古法。作者反對的是機械套用，不是否定所有古法。','alt':'新精確兩欄論證流程：故事水已變→仍循舊標記→渡河失敗，類比時勢已變→仍照搬古法→治理不合；同列對應不是另造事件。'},{'heading':'③ 反問「豈不悲哉」，不是不表態','text':'結尾的反詰表達清楚批評，最合C「不敢苟同」：不能隨便贊同這種做法。作者已理解問題並提出理由，不是A不懂內情、B不表態，也不是D禁止別人解釋。','alt':'四種態度詞義卡，C不能隨便贊同高亮，扣結尾反詰的批評；其他三項精確列義，沒有把不敢苟同畫成膽小。'}],'fourth':{'answer':'答案：C，不敢苟同','points':['先判斷作者是否表態，再分辨支持或反對。','「豈不悲哉」已表明反對照搬古法。','批評不知因時調整，不等於古法一律不能參考。']},'protectedWords':['先表之時可導','今水已變而益多','先王之法','豈不悲哉','不敢苟同','不明就裡','不置可否','不容分說','機械套用','照搬古法'],'rationale':'親見原卷全文/2註釋與42題A-D及鉛筆C，獨立循前後水況/類比/反詰核定C。作者態度重點是論證結構，因此新原生SVG以水況示意、雙欄類比流程、態度詞卡，比再演溺水戰爭更能直接呈現文本理由；未沿用來源AI。','promptSummary':'原生三格論證圖：前後水況示意無精確數據；渡河失敗與今主古法對位流程；A-D態度詞義卡及C批評，不用人物/來源AI。','answerCheckedAgainst':'原卷『嚮其先表之時可導』『今水已變而益多』『有似於此』『豈不悲哉』，42題四選項完整核對，C不同意機械照搬。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-522-reading-source-5190c71acb.jpg','site/dist/assets/questions/q-522-source-b721317c86.jpg'],'visualChecked':True,'answer':'C','notes':'全文與註①荊人/②表及42四選項親見；不加白天設標記或所有古法全錯的概括，原卷千餘溺亡不以新圖誇張重演。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-522.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
