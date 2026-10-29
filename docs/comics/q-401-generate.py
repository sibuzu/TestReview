from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,t,color='#dce8d0',size=11):
  s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{color}"/>');txt(x+w/2,y+h/2+4,t,size)
 def arrow(x,y,yy):s.append(f'<path d="M{o+x} {y}V{yy}m-4 -5 4 5 4-5" fill="none" stroke="#7f9a8e" stroke-width="1.5"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#edf2f5","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  txt(90,18,'比較幼年人口的底部',10)
  for cx,ws,year in [(47,[8,12,20,28,32,23,15,14],'2022'),(133,[8,19,27,30,23,17,10,9],'2050推估')]:
   txt(cx,39,year,10)
   for j,w in enumerate(ws):s.append(f'<rect x="{o+cx-w}" y="{52+j*9}" width="{2*w}" height="7" fill="{ "#b17c3c" if j>=6 else "#91ad8b"}"/>')
   s.append(f'<path d="M{o+cx} 47V125" stroke="#eff3ec" stroke-width="1"/>')
  txt(90,146,'2050推估底部更窄',11);txt(90,163,'幼年人口減少的線索',10);txt(90,178,'趨勢概念，非數值重繪',8)
 elif i==1:
  txt(90,18,'政策如何對應問題？',10)
  box(15,34,150,28,'提供幼兒照顧服務');arrow(90,65,82)
  box(15,87,150,28,'減輕家庭育兒負擔','#dbe7ef');arrow(90,118,135)
  txt(90,151,'對應少子化的政策方向',10);txt(90,176,'不保證單一措施必增出生',9)
 else:
  txt(90,18,'圖中有什麼，沒什麼？',10)
  box(10,32,160,33,'A 提早退休：不合方向','#f8f7ef',9)
  box(10,73,160,33,'B 普遍增校：缺需求支持','#f8f7ef',9)
  box(10,114,160,33,'D 山區醫療：無區域資料','#f8f7ef',9)
  txt(90,174,'年齡分布 ≠ 山區分布',11)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-401.svg';Path(art).write_text(''.join(s))
spec={'id':'q-401','subject':'Geography','title':'先讀人口趨勢，再對應托育政策','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-401-generate.py','layoutVersion':'native-fluid-v6','panels':[{'heading':'① 底部變窄，幼年人口減少','text':'原圖比較2022年與2050年推估的人口金字塔。2050年底部更窄，顯示幼年人口減少；較高年齡層的比重提高，可讀出少子化、高齡化趨勢。','alt':'新製兩個簡化人口形狀，底部標色、2050標推估，明示趨勢概念非數值重繪，不冒充原圖統計柱高。'},{'heading':'② 提供托育，減輕家庭照顧負擔','text':'四項中，提供幼兒照顧服務可以減輕家庭育兒負擔，最直接對應少子化，選C。這是政策方向的比較，不表示單靠托育就保證出生率一定提高。','alt':'幼兒照顧服務到減輕育兒負擔的政策邏輯鏈，不加入補助金額、成功率或保證出生增加。'},{'heading':'③ 別把年齡圖，當成山區醫療分布圖','text':'A鼓勵提早退休不合勞動人口占比下降的方向；B增建各地小學缺乏幼年人口需求支持。D雖談醫療，卻限定山區，圖中沒有這種區域資料，不能直接推成優先政策。','alt':'A提早退休/B普遍增校/D山區醫療三項依證據比較，強調圖無山區分布，不否定山區醫療本身的重要。'}],'fourth':{'answer':'答案 C：提供幼兒照顧服務','points':['2050是人口推估，不是已發生的統計。','托育支援與減輕育兒負擔直接相關。','依圖判方向，不保證單一措施有效，也不加圖中沒有的地區資訊。']},'protectedWords':['2022年','2050年','人口金字塔','幼年人口','少子化','高齡化','幼兒照顧服務','育兒負擔','出生率','勞動人口','山區醫療','區域資料'],'originalChecked':{'images':['site/dist/assets/questions/q-401-source-6521fb9fa6.jpg'],'necessaryFigures':['site/dist/assets/questions/q-401-figure-253c40d0c4.jpg'],'visualChecked':True,'answer':'C','notes':'親見18題全文及2022/2050推估雙圖、四選項，2050底部較窄高齡段較多，圖無山區位置資料；維持C。'},'sourceUrl':'https://chatgpt.com/share/6ae0533b-4b48-83ec-ba36-0b7b3759f90a','answerCheckedAgainst':'雙人口圖少子高齡趨勢與四項政策對應，C托育減負擔最直接，D山區限定無圖據；沿現有C與單項措施不保證出生率限制，不增加現行政策補助或數字。','rationale':'判讀重點為年齡形狀趨勢與政策關聯，採新原生簡化雙形/政策鏈/資料範圍比較SVG，比泛用親子圖片更直接；趨勢圖明示非精確數值重繪，原卷保留必要圖，不用來源AI。','sourceAIUsed':False,'manualLineBreaks':False,'generationCalls':0,'diagramChecks':{'selected':'C','2050Projection':True,'newShapeExactPopulationData':False,'singlePolicyGuaranteesBirths':False,'mountainMedicalSpatialDataInOriginal':False},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-401.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
