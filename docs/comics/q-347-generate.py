from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="b" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="#507f95"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=10,c='#35564f'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="{c}">{z}</text>')
 def r(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#e8f0f2","#f6eddf","#edf1e6"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(99,17,'本島在島的哪一側？',10)
  t(26,31,'北',11);s.append(f'<path d="M{o+26} 78V42" stroke="#507f95" stroke-width="2" marker-end="url(#b)"/>')
  r(92,49,80,27,'#c5ddcf');t(132,67,'龜山島',12)
  r(8,124,88,28,'#c8d5b3');t(52,143,'蘭陽平原',12)
  s.append(f'<path data-direction="island-to-plain" data-start="125,82" data-end="68,118" d="M{o+125} 82L{o+68} 118" stroke="#507f95" stroke-width="3" marker-end="url(#b)"/>')
  t(137,141,'西～西南',10);t(90,176,'方位關係示意，非比例地圖',8)
 elif i==1:
  t(90,18,'等高距相同：線密處較陡',10)
  t(41,42,'較密、較陡',10);t(133,42,'較疏、較緩',10)
  for kind,xs in [('dense',[18,29,40,51]),('sparse',[103,123,143,163])]:
   for j,x in enumerate(xs):s.append(f'<path data-density="{kind}" data-level="{50*(j+1)}" data-x="{x}" d="M{o+x} 56Q{o+x+4} 87 {o+x} 120" stroke="#a68e64" stroke-width="1.7" fill="none"/>')
   t(xs[0],136,'50',8);t(xs[-1],136,'200',8)
  t(90,159,'相同圖尺與等高距的比較',9);t(90,177,'高度為示例，不重畫原島形',8)
 else:
  t(90,18,'方向和地形，兩條件一起看',10)
  for y,z in [(35,'西至西南：朝本島一側'),(82,'臨海、等高線密集'),(131,'原圖丙最符合 → C')]:r(8,y,164,28,'#bfd5ad' if y==131 else '#dce4d0');t(90,y+19,z,11)
  t(90,75,'＋',16);t(90,122,'↓',16);t(90,177,'800 公尺是坑道長，不是射程',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-347.svg');a.write_text(''.join(s))
d={'id':'q-347','subject':'Geography','title':'先定方向，再合看臨海峭壁：丙最符合','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-347-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 北向上，找臺灣本島的那一側','text':'依原圖指北針，上方是北、左方是西。龜山島在宜蘭外海，蘭陽平原在其西方至西南方的臺灣本島一側；要先找符合這個方向的位置，不是看畫面哪座山最高。','alt':'新精確北上方位關係圖，龜山島至蘭陽平原箭頭向左下西南分量，明標非比例地圖，不重製島形或砲臺位置。'},
{'heading':'② 線密而且臨海，符合峭壁條件','text':'同一圖尺、相同等高距下，等高線越密，代表地勢越陡。回原卷看，丙在西南側臨海密線處，符合題幹峭壁內的條件；示例線只解釋疏密，不取代原圖。','alt':'新精確兩組50至200示例等高線，共同等高距與圖尺，密組間隔11、疏組間隔20，明示不是原島實測值。'},
{'heading':'③ 丙同時符合方向與地形，選C','text':'丙同時符合朝本島一側與臨海峭壁兩個條件。甲偏北，乙靠湖區，丁在東側且隔著島內高地，都不如丙。800公尺指坑道長度，不能直接當作射程來選位置。','alt':'新方向＋臨海密線條件合成圖，對回原卷丙選C，不重繪舊AI多出乙點的島圖或猜造射程。'}],
'fourth':{'answer':'答案 C：丙','points':['先用指北針判斷西至西南、本島一側。','再看臨海密集等高線，找符合峭壁的部位。','合看兩條件；不選最高峰，也不把坑道長當射程。']},
'protectedWords':['龜山島','蘭陽平原','臺灣本島','西南側','西南方','西至西南','指北針','等高線','等高距','800公尺','坑道長度','射程'],
'originalChecked':{'images':['site/dist/assets/questions/q-347-source-8f3bc43cf4.jpg'],'necessaryFigures':['site/dist/assets/questions/q-347-figure-2ef31f8250.jpg'],'visualChecked':True,'answer':'C','notes':'完整11題幹/四點四選、原北箭頭、島西南丙密線臨海部位親見；使用者已確認correction-q347，沿C不重問方向。原AI轉正重畫錯圖不採，不改原島輪廓或高度。'},
'sourceUrl':'https://chatgpt.com/share/6ae05208-3ffc-83ee-be7e-99cc4705ab6d','answerCheckedAgainst':'使用者已確認C與原卷紅C，原圖指北針與丙方位/密線交叉判斷；蘭陽博物館主文頭城東方海域地理背景佐證。',
'references':[{'title':'蘭陽博物館020期：龜山島海域地質','url':'https://www.lym.gov.tw/ch/collection/epaper/epaper-detail/138041f0-1180-11ea-8482-2760f1289ae7/','supports':'龜山島位於宜蘭頭城東方海域，平原可見島的位置背景','access':'官方HTML主文145行及urllib實讀；不引用與題目無關精確高程面積'}],
'rationale':'精確方向箭頭與同等高距線密比較，讓方向及坡度兩條件合併，不讓AI改原島或增加乙點；不推測武器射程或作現地部署建議。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'C','arrowStart':[125,82],'arrowEnd':[68,118],'towardPlainWestAndSouth':True,'denseContourX':[18,29,40,51],'sparseContourX':[103,123,143,163],'sameDemoElevations':[50,100,150,200],'originalMapReconstructed':False,'tunnelLengthMeansRange':False,'oldConfirmationReopened':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-347.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
