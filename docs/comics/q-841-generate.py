from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="a" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="#608da0"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11,c='#33564c'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="{c}">{z}</text>')
 def r(x,y,w,h,c='#d5e2ca'):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eaf1f4","#eef2e7","#f8efdf"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(102,18,'與那國島向西看臺灣',10);t(20,38,'北',10)
  s.append(f'<path d="M{o+20} 73V47" stroke="#608da0" stroke-width="1.7" marker-end="url(#a)"/>')
  r(7,86,57,28);t(35.5,105,'蘇澳一帶',10)
  r(105,86,69,28,'#d0e2e5');t(139.5,105,'與那國島',10)
  s.append(f'<path data-looking="west" d="M{o+103} 100H{o+68}" stroke="#608da0" stroke-width="2.5" marker-end="url(#a)"/>');t(86,85,'向西',9)
  s.append(f'<path d="M{o+35} 128V133H{o+140}V128" fill="none" stroke="#a4b4a6"/>');t(87.5,152,'題示相距約 110 公里',10)
  t(90,178,'僅方位關係，非地圖與光學剖面',8)
 elif i==1:
  t(90,18,'中央山脈：北端近蘇澳',11)
  r(25,35,130,28);t(90,55,'蘇澳附近',13)
  s.append(f'<path d="M{o+90} 67V136" stroke="#87a478" stroke-width="20"/>');t(90,91,'中央山脈',12);t(90,115,'北段',11)
  s.append(f'<path d="M{o+90} 137V153" stroke="#608da0" stroke-width="2" marker-end="url(#a)"/>')
  t(90,171,'山脈向南延伸（概念示意）',9)
 else:
  t(90,18,'按本題主要相對位置比較',10)
  for j,z in enumerate(['A 雪山：較偏西北','B 中央：北段近蘇澳','C 海岸：較偏南','D 玉山：內陸且偏南']):r(8,31+j*32,164,27,'#bfd5ae' if j==1 else '#e3e4d6');t(90,50+j*32,z,10)
  t(90,178,'不代表任何天氣只看得見一山脈',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-841.svg');a.write_text(''.join(s))
d={'id':'q-841','subject':'Geography','title':'從與那國島向西，對應蘇澳附近中央山脈北段','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-841-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 與那國島在東，向西對應蘇澳一帶','text':'先讀原圖的相對位置：與那國島在臺灣以東，題目以蘇澳東部外海約110公里定位。從島上最西端看臺灣，方向朝西，不要把蘇澳看出去的方向和島上看回來的方向弄反。','alt':'新精確北上方位圖，與那國在右東、蘇澳在左西，觀看箭頭由右向左；110公里僅沿題示，不畫成視距光學剖面。'},
{'heading':'② 中央山脈北段，接近蘇澳與東部海岸','text':'再把臺灣主要山脈放回位置。中央山脈北起蘇澳附近，北段鄰近東部海岸，和題目從島上向西對應蘇澳一帶的方向相符，因此選B。新圖只示位置關係，不是山峰實測剖面。','alt':'新原生中央山脈北端蘇澳至向南延伸的概念圖，不虛構海拔、精確峰名或觀測可見角度。'},
{'heading':'③ 按題示位置選B，不作絕對遮擋斷言','text':'雪山山脈較偏西北，海岸山脈較偏南，玉山山脈較內陸且偏南。本題主要位置最符合中央山脈；這不代表其他山脈在所有地點、天氣與能見度條件下都完全看不到。','alt':'新四山脈題意比較表B突出，保留本題定位推論界線，不作其他山脈永遠遮住或保證晴天可見的光學斷言。'}],
'fourth':{'answer':'答案 B：中央山脈','points':['從與那國島往西，對應臺灣蘇澳一帶。','中央山脈北段接近蘇澳與東部海岸。','按本題定位判讀，不推論所有觀測條件下的可見性。']},
'protectedWords':['與那國島','蘇澳','110公里','中央山脈','北段','雪山山脈','海岸山脈','玉山山脈','東部海岸','能見度','實測剖面'],
'originalChecked':{'images':['site/dist/assets/questions/gemini062-c3b6978a5ad4a0.jpg'],'necessaryFigures':['site/dist/assets/questions/gemini062-4ead957197b0d4.jpg'],'visualChecked':True,'answer':'B','notes':'親見完整29題四山脈/指北針/臺灣及與那國島相對位置、110公里及原紅B。使用者已允許保留本題必要圖筆跡，不裁不遮不重繪；原圖與既有B均不動。'},
'sourceUrl':'https://share.gemini.google/lEdStGcomTed','answerCheckedAgainst':'原紅B與題示蘇澳東側位置；行政院地文主文中央山脈北起蘇澳佐證，原解說不絕對遮擋的界線保留。',
'references':[{'title':'行政院國情簡介：地文','url':'https://www.ey.gov.tw/state/4447F4A951A1EC45/52515c49-bcc0-45f5-bd5f-78c22c9d3f45','supports':'中央山脈北起蘇澳，南至鵝鑾鼻，臺灣主幹位置','access':'官方HTML urllib實讀中央山脈主文，不引用其他海拔或地理最高排名'}],
'rationale':'精確觀看方向與北端位置概念可防東西反讀；不生成照片冒稱與那國實見山形、不以未提供光學條件推斷全遮擋，保留必要原圖紅筆。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'B','observer':'與那國島','directionToTaiwan':'west','northUp':True,'distanceFromQuestionKm':110,'northernCentralRangeNearSuao':True,'anyOtherRangeAlwaysInvisible':False,'guaranteedClearDaySight':False,'originalMapInkRemoved':False,'opticalProfileDrawn':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-841.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
