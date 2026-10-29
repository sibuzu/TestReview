from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['從案例到作者的提醒','標題須保留「雖然／但」','逐項看：有無偏離主旨'][i],9)
 if i==0:
  box(16,41,148,35,'#f0e1c6');txt(90,57,'原文案例',9);txt(90,71,'不實指控 → 當事人受損',9)
  s.append(f'<path d="M{o+90} 81v12m-4-4 4 4 4-4" fill="none" stroke="#79999c"/>')
  box(16,102,148,42,'#d6e6cb');txt(90,120,'作者提醒',9);txt(90,136,'言論自由也涉及相應責任',10);txt(90,174,'不能只抓案例，忘了結論',9)
 elif i==1:
  box(19,39,142,37,'#d6e6cc');txt(90,54,'雖然',9);txt(90,70,'言論自由受保障',12)
  txt(90,94,'＋',15)
  box(19,107,142,37,'#d1e0eb');txt(90,122,'但',9);txt(90,138,'仍須守法、承擔責任',11)
  txt(90,174,'B同時保留兩個重點',11)
 else:
  for j,(a,b) in enumerate([('A','已成災：擴大判斷'),('B','自由＋守法：完整'),('C','無保障：與文相反'),('D','亂象：沒有點明提醒')]):
   yy=38+j*29;box(10,yy,160,23,'#d8e7c8' if a=='B' else '#f8f8f0');txt(90,yy+16,a+' '+b,10)
  txt(90,174,'依本文選標題：B',11)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-389.svg';Path(art).write_text(''.join(s))
spec={'id':'q-389','subject':'Chinese','title':'標題合看兩重點：言論自由，仍須守法','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-389-generate.py','startedAt':'2026-10-29T05:54:46.341695+00:00','panels':[{'heading':'① 先有案例，後有真正的提醒','text':'短文先舉網友不實指控、當事人受損的案例，接著用「雖然……但……」提出重點。找標題時要讀到作者最後的提醒，不能只看到社群媒體或案件，就停在表面話題。','alt':'原生文章結構案例→作者提醒兩階圖，無另畫真實判刑流程或把任何假消息一概定罪。'},{'heading':'② 雖然有保障，但仍有責任','text':'依本文，前半肯定言論自由受保障，後半提醒發言仍須守法。B「網路暢所欲言，仍須守法」同時保留這兩個重點，最適合作為標題；這是在判讀原文的主旨。','alt':'原生雖然保障/但須守法兩卡並列整合，B保留兩面，未說一方完全取消另一方。'},{'heading':'③ 不擴大、不反轉，也別過於籠統','text':'A的「氾濫已成災」加入原文未支持的強烈判斷；C說不受保障，直接反轉文意；D只泛稱亂象，沒有點出守法提醒。三者都沒有B準確。','alt':'A-D標題核對卡，B完整高亮，A擴大/C反轉/D籠統區分，不加題外法律構成要件。'}],'fourth':{'answer':'答案：B，網路暢所欲言，仍須守法','points':['標題要概括主旨，不能只重述案例的表面話題。','雖然言論自由受保障，但發言仍有相應責任。','以原文支持的內容作判據，避免過度推論或否定原句。']},'protectedWords':['雖然','仍須守法','言論自由','社群媒體','氾濫已成災','不受保障','相應責任','雖然……但……','不實指控'],'rationale':'親見19題全文與A-D及紅筆B，沿已核定B，按文章案例→轉折結論與標題覆蓋比對。這是閱讀主旨題，選新原生結構/轉折/四項核對圖更直接，不製作會誤教法律機制的人物法庭場景，不新增現行法律判斷，不用來源AI。','promptSummary':'原生三格閱讀論證：案例引到提醒；雖然保障＋但責任雙重點；A擴大/C相反/D籠統與B完整核對。所有字原生可核。','answerCheckedAgainst':'原卷19短文『雖然言論自由受憲法保障，但…仍須承擔法律責任』及A-D，B保留轉折兩面；僅閱讀題不另斷具體法律案件或擴充假消息犯罪構成。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-389-source-25385050dc.jpg'],'visualChecked':True,'answer':'B','notes':'全部原短文與四標題親見，A學生記號非標準；不將原材料簡述擴充成所有言論/假消息法律教學。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-389.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
