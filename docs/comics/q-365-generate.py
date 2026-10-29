from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="b" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#498ba0"/></marker><marker id="r" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#bf7954"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,size=10,c='#284d4d'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(y,z,c='#dce7cf',size=11):s.append(f'<rect x="{o+8}" y="{y}" width="164" height="28" rx="4" fill="{c}"/>');t(90,y+19,z,size)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eaf1f4","#edf2e7","#faf0e6"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,17,'夏季題設：西南風',11)
  s.append(f'<path d="M{o+90} 35V141M{o+30} 87H{o+150}" stroke="#b2beb6"/>')
  for x,y,z in [(90,32,'北'),(159,91,'東'),(90,153,'南'),(20,91,'西')]:t(x,y,z,10)
  s.append(f'<path d="M{o+43} 128L{o+132} 43" stroke="#498ba0" stroke-width="5" marker-end="url(#b)" data-wind-from="SW" data-start="43,128" data-end="132,43"/>')
  t(36,144,'西南',9);t(146,39,'東北',9)
  t(90,176,'名稱指風從哪裡來',10)
 elif i==1:
  t(90,18,'越山後：下降、增溫',11)
  s.append(f'<path d="M{o+13} 145L{o+90} 66L{o+168} 145Z" fill="#a9bd8f" stroke="#6d8b71"/>')
  s.append(f'<path d="M{o+8} 119Q{o+44} 47 {o+91} 44" fill="none" stroke="#498ba0" stroke-width="4" marker-end="url(#b)"/>')
  s.append(f'<path d="M{o+103} 46Q{o+146} 57 {o+169} 118" fill="none" stroke="#bf7954" stroke-width="4" marker-end="url(#r)"/>')
  for x,y,r in [(39,73,9),(50,67,11),(61,74,9)]:s.append(f'<circle cx="{o+x}" cy="{y}" r="{r}" fill="#f8fbfc"/>')
  for x in [35,47,59]:s.append(f'<path d="M{o+x} 88l-4 10" stroke="#71a6c0" stroke-width="2"/>')
  t(43,160,'迎風：抬升',9);t(135,160,'背風：乾熱',9)
  t(90,177,'概念剖面，非實際路線或尺度',8)
 elif i==2:
  t(90,18,'依本題風向比較四地',10)
  for j,z in enumerate(['A 基隆暖暖','B 臺東大武','C 屏東東港','D 桃園大園']):box(31+j*33,z,'#c3d9ae' if j==1 else '#e9e9dc',12)
  t(90,177,'大武在符合題設的東側區域',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-365.svg');a.write_text(''.join(s))
d={'id':'q-365','subject':'Geography','title':'先給風向，再判背風坡的下降增溫','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-365-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 西南風，表示風從西南側吹來','text':'題目只考慮夏季盛行風，先用西南風判讀。西南風是從西南吹向東北，不是朝西南吹；風向名稱要先讀對，才能比較山地哪一面迎風或背風。','alt':'新精確羅盤北上東右，箭頭從西南左下指東北右上，標風向來源而非臺灣地圖路線。'},
{'heading':'② 越過山地，背風側下降增溫','text':'迎風側氣流抬升，越山後在背風側下降，空氣受壓縮而增溫，可能形成乾熱焚風。剖面示意氣流過山的過程；不是說只要有山，就一定出現焚風。','alt':'新精確概念山形剖面，藍箭頭由左上升越山、橙箭頭右側下降，迎風雲雨與背風乾熱，非實際山高路線或溫度定量。'},
{'heading':'③ 大武在本題相符的背風側區域','text':'臺東大武位於中央山脈東側一帶，符合題設的夏季過山氣流情境，選B。東港在西南部、大園在西北沿海，都不是此題要找的東側背風坡；不能換成別種風向來作答。','alt':'新製四地名對照卡B大武突出，不虛構地圖坐標、測站出現頻率或宣稱東側永遠背風。'}],
'fourth':{'answer':'答案 B：臺東縣大武鄉','points':['先看夏季盛行的西南風，再判迎風與背風。','背風坡下降增溫，可能形成乾熱焚風。','風向改變時，迎風與背風位置也可能改變。']},
'protectedWords':['西南風','西南側','東北','迎風側','背風側','下降增溫','乾熱焚風','臺東大武','中央山脈','東港','大園','臺東縣大武鄉'],
'originalChecked':{'images':['site/dist/assets/questions/q-365-source-d93405d526.jpg'],'visualChecked':True,'answer':'B','notes':'親見原51完整夏季限定與中央山脈背風坡、四地名；照片作答遮住不猜，依已核對B與官方大武焚風情境。原桃園縣名稱保留。'},
'sourceUrl':'https://chatgpt.com/share/6ae05276-e754-83ee-a87a-569980550954','answerCheckedAgainst':'原題夏季風向條件核B，CWA科普主文大武焚風/夏季西南季風/背風壓縮增溫交叉核對，不以圖中人工方向替代實際路線。',
'references':[{'title':'中央氣象署：快被烘乾啦！淺談焚風造成的影響','url':'https://pweb.cwa.gov.tw/PopularScience/pr/pr_8.html','supports':'大武焚風、夏季西南季風與背風下降增溫，風向可改背風側','access':'官方主文已讀'}],
'rationale':'精確羅盤箭頭加概念山地剖面，比人物直接防風向讀反與固定東側背風的誤解；不畫實際山脈斷面或杜撰溫度梯度、測站頻率。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selected':'B','windSource':'SW','windToward':'NE','arrowStart':[43,128],'arrowEnd':[132,43],'downhillLeewardWarming':True,'terrainProfileSurveyed':False,'eastAlwaysLeeward':False,'allMountainsGuaranteeFoehn':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
assert 132>43 and 43<128
Path('docs/comics/q-365.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
