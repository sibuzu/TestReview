from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def text(x,y,z,size=10,c='#284d4d'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def rect(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eef3e7","#edf2f5","#faf1e6"][i]}"/><g font-family="sans-serif">')
 if i==0:
  text(90,18,'西北沿海 → 東南山區',10)
  s.append(f'<path d="M{o+8} 140H{o+43}L{o+62} 129H{o+89}L{o+107} 109L{o+123} 119L{o+142} 61L{o+160} 84L{o+174} 43V157H{o+8}Z" fill="#a4ba8d" stroke="#65866e" stroke-width="2"/>')
  s.append(f'<path d="M{o+5} 143H{o+42}V158H{o+5}Z" fill="#87c9db"/>')
  text(33,117,'沿海',10);text(79,112,'台地',10);text(144,34,'山地',10)
  text(90,176,'概念剖面，非測線或比例圖',9)
 elif i==1:
  text(90,18,'丁：原圖東南端山區',10)
  for y,z in [(36,'地形陡峭'),(80,'可居住與交通條件受限'),(124,'較不利人口密集聚居')]:
   rect(8,y,164,30,'#dce8cf');text(90,y+20,z,10)
  for y in [69,113]:s.append(f'<path d="M{o+90} {y}v8m-3-3 3 3 3-3" fill="none" stroke="#8c9e92"/>')
  text(90,176,'依自然環境比較，不是查人數',8)
 else:
  text(90,18,'密度：人口 ÷ 面積',11)
  for x,n,label in [(12,12,'較密'),(100,3,'較疏')]:
   rect(x,45,68,76,'#e2ead8')
   for k in range(n):
    cx=o+x+13+(k%3)*20;cy=61+(k//3)*16
    s.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#627d62"/>')
   text(x+34,139,label,11)
  text(90,38,'同樣面積的假設示意',9)
  text(90,161,'面積大 ≠ 密度高',11)
  text(90,177,'圓點不代表桃園實際人口',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-363.svg');a.write_text(''.join(s))
d={'id':'q-363','subject':'Geography','title':'先定位東南山區，再比較人口密度','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-363-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 西北臨海，東南深入山區','text':'回原圖定位：乙較靠西北沿海，丙在中段，丁在狹長的東南端。桃園東南部深入山地；新圖只示意地勢變化，不取代原題的行政區輪廓。','alt':'新製西北沿海經台地到東南山地的定性剖面，明示非實測或比例圖；四點精確位置仍回原卷。'},
{'heading':'② 丁的自然條件較不利密集聚居','text':'山區地形較陡，可居住用地與交通條件受限。依題目要求比較自然環境，丁附近最不利大量人口聚集，因此選D；不是說山區完全沒有居民。','alt':'新製東南丁山區到陡坡、可居住與交通條件受限、人口較難密集聚居的條件鏈。'},
{'heading':'③ 比的是密度，不是面積或人口總數','text':'人口密度是人口數除以土地面積。同樣面積內，人較少就較疏；不能因為山區面積廣，便認為密度較高。圓點圖只是定義示意，不是桃園人口統計。','alt':'新製相同大小兩區12與3圓點的假設密度比較，明示非桃園統計、不作人口估算。'}],
'fourth':{'answer':'答案 D：丁，東南部山區','points':['用原輪廓圖定位丁在東南端。','陡峭地形及開發條件限制人口聚集。','原題是2014年升格前背景，不是今日即將升格。']},
'protectedWords':['東南部','東南端','西北沿海','人口密度','人口總數','2014年','自然環境','行政區','桃園','山區'],
'originalChecked':{'images':['site/dist/assets/questions/q-363-source-0828db7916.jpg'],'necessaryFigures':['site/dist/assets/questions/q-363-figure-9240cbf795.jpg'],'visualChecked':True,'answer':'D','notes':'親見45完整2014升格前題幹四點選項及輪廓圖，甲北側乙西北丙中段丁狹長東南端，維持D。'},
'sourceUrl':'https://chatgpt.com/share/6ae05276-e754-83ee-a87a-569980550954',
'answerCheckedAgainst':'原輪廓圖丁東南端與自然環境條件對照，復興區公所官方地理位置佐證桃園東南山區；答案D不變。',
'references':[{'title':'桃園市復興區公所：地理位置','url':'https://www.fuxing.tycg.gov.tw/cp.aspx?Create=1&n=7091','supports':'桃園東南山地位置，不把原丁點精確化成已知實測地點'}],
'rationale':'新精確概念剖面與人口密度同面積示例，比泛用人物情境更直接連結位置、地形及密度定義；不猜丁點坐標，不虛構人口統計，原圖保留。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,
'diagramChecks':{'selected':'D','terrainCrossSectionSurveyed':False,'hypotheticalDotCounts':[12,3],'equalAreaComparison':True,'dotCountsRepresentActualPopulation':False,'originalMapReplaced':False,'2014BackgroundPreserved':True},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
Path('docs/comics/q-363.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
