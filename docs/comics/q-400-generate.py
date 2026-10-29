from pathlib import Path
import json,hashlib,datetime,time,socket
start=time.monotonic_ns()
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,t,color='#dce8d0',size=11):
  s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{color}"/>');txt(x+w/2,y+h/2+4,t,size)
 def line(x,y,xx,yy,col='#819e90',w=1.5):s.append(f'<path d="M{o+x} {y}L{o+xx} {yy}" stroke="{col}" stroke-width="{w}" fill="none"/>')
 def arrow(x,y,xx,yy):
  line(x,y,xx,yy);line(xx-4,yy-5,xx,yy);line(xx+4,yy-5,xx,yy)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#edf2f5","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  txt(90,18,'先看分布，再推區位需求',10)
  s.append(f'<path d="M{o+0} 32H{o+61}Q{o+48} 69 {o+61} 103T{o+58} 166H{o}Z" fill="#bed8df"/>')
  txt(27,90,'海',14);txt(124,90,'陸',14)
  for y,x in [(49,70),(123,76),(151,69)]:
   s.append(f'<rect x="{o+x}" y="{y}" width="17" height="13" fill="#668975"/><path d="M{o+x} {y}v-7l5 4 5-4v7" fill="#668975"/>')
  txt(120,52,'沿海點位',10);txt(104,114,'回原圖判讀',10);txt(90,177,'概念示意，非原圖位置',9)
 elif i==1:
  txt(90,18,'易腐原料：減少運送等待',10)
  box(18,33,144,30,'原料來源', '#dce8d0');arrow(90,65,90,84)
  box(18,89,144,30,'靠近原料的加工廠','#d7e6ef');arrow(90,122,90,141)
  txt(90,158,'縮短運輸與等待時間',11);txt(90,177,'水產加工只是理解例子',9)
 else:
  txt(90,18,'比較哪項最能解釋分布',9)
  for y,a,b in [(34,'A 體積','主要看運輸負擔'),(66,'B 易腐','靠近原料，快處理'),(98,'C 技術','看人才與研發'),(130,'D 電能','看供電等條件')]:
   box(10,y,160,29,'', '#dce8d0' if a.startswith('B') else '#f8f7ef');txt(47,y+18,a,10);txt(120,y+18,b,9)
  txt(90,177,'不能只因沿海就武斷命名',9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-400.svg';Path(art).write_text(''.join(s))
spec={'id':'q-400','subject':'Geography','title':'易腐原料要快處理，工廠靠近原料來源','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-400-generate.py','layoutVersion':'native-fluid-v6','panels':[{'heading':'① 從原圖找出沿海分布線索','text':'原圖點位多在沿海附近。先觀察整組分布，再想哪種區位需求能解釋它；不要看到某一個點，就替所有工廠指定同一個未提供的名稱。','alt':'新製海陸分界與沿海工廠概念示意，明示非原圖位置，不冒充臺灣比例地圖或增加真實工廠數量。'},{'heading':'② 原料容易腐壞，運送等待要縮短','text':'易腐原料不宜長時間運送與等待，工廠便傾向靠近取得原料的地方，盡快處理。水產加工可幫助理解這種需求，但原題沒有逐點列出工廠名稱。','alt':'原料來源到附近加工廠再縮短運輸等待的關係圖，不加溫度、保鮮時限或聲稱全是水產加工廠。'},{'heading':'③ 比較特性，不是斷言所有沿海工廠一樣','text':'A體積大偏向運輸負擔，C高技術要看人才與研發，D大量用電要看供電等條件。就本題整組分布比較，B原料易腐、靠近來源地最符合。','alt':'A體積/B易腐/C技術/D電能四種判斷線索對照，B高亮，不宣稱其他產業不能位於沿海。'}],'fourth':{'answer':'答案 B：原料容易腐壞','points':['觀察整組點位，再連到原料區位。','易腐原料須快處理，縮短運送與等待。','水產加工是理解例子，不是圖中每點的已知名稱。']},'protectedWords':['原料容易腐壞','易腐原料','原料來源','水產加工','運輸負擔','高技術','研發','區位需求','沿海','等待時間'],'sourceUrl':'https://chatgpt.com/share/6ae0533b-4b48-83ec-ba36-0b7b3759f90a','originalChecked':{'images':['site/dist/assets/questions/q-400-source-8e0f831f66.jpg'],'necessaryFigures':['site/dist/assets/questions/q-400-figure-131c4178dc.jpg'],'visualChecked':True,'answer':'B','notes':'親見16題四項及必要臺灣沿海點位圖，東北、西南等沿海多群點；原黑A紅B，不替點位杜撰工廠名稱。'},'answerCheckedAgainst':'完整題圖與四項獨立比較，維持B易腐原料須靠來源地快處理；既有詳解水產只是例子與非所有沿海工廠限定均保留。','rationale':'新製海陸點位概念、易腐原料與處理時間關係、四選項區位線索SVG，原圖仍作位置依據。精確邏輯比泛用港口工廠圖片更能避免武斷指定產業；不使用來源AI圖。','sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selected':'B','preciseFactoryLocationsInvented':False,'allCoastalFactoriesAreSeafoodClaim':False,'illustrativeFactoryCountIsOriginalCount':False},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-400.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
Path('docs/comics/q-400-timing.json').write_text(json.dumps({'measurementMethod':'monotonic_ns','host':socket.gethostname(),'startNs':start,'endNs':time.monotonic_ns(),'scope':'僅原生SVG與spec寫入，不是整題審查或模型產圖秒數','excludeFromImageGenerationAverage':True},ensure_ascii=False,indent=2)+'\n')
