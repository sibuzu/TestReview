from pathlib import Path
import json,math,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def t(x,y,z,size=10,c='#284d4c'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf3e7","#edf1f7","#faf0df"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'從極地方向看緯線圈',10)
  for r,col in [(60,'#80a9b1'),(49,'#abc097'),(34,'#5f896a')]:s.append(f'<circle cx="{o+90}" cy="88" r="{r}" fill="none" stroke="{col}" stroke-width="3"/>')
  t(90,91,'近極地',12);t(90,163,'赤道（最外圈）',10);t(90,177,'示意，非四點精確定位',8)
 elif i==1:
  t(90,18,'同速率：路短就先到',11);t(90,45,'時間＝距離 ÷ 速率',12)
  t(36,77,'短圈',10);box(62,65,42,18,'#75a17a');t(137,78,'較快',10)
  t(36,113,'長圈',10);box(62,101,88,18,'#9db6c7')
  t(90,148,'只比圈長，速率相同',10);t(90,173,'長條示意，非實際飛行時間',8)
 else:
  t(90,18,'同一圈：向東或向西',11)
  s.append(f'<circle cx="{o+90}" cy="91" r="47" fill="none" stroke="#6f9c83" stroke-width="4"/><circle cx="{o+90}" cy="44" r="4" fill="#c0894a"/>')
  s.append(f'<path d="M{o+121} 56q16 12 16 32m-4-4 4 4 4-4 M{o+59} 56q-16 12-16 32m-4-4 4 4 4-4" fill="none" stroke="#426a82" stroke-width="2"/>')
  t(90,88,'方向相反',11);t(90,105,'一圈同長',13);t(90,157,'本題排除風向等其他因素',9);t(90,176,'不是比較經度大小',10)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-398.svg';Path(art).write_text(''.join(s))
rs=[60*math.cos(math.radians(a)) for a in [0,35,55]];assert rs[0]>rs[1]>rs[2]
Path('docs/comics/q-398-geometry-validation.json').write_text(json.dumps({'model':'spherical latitude circle radius R*cos(abs(latitude)); internal geometry only, no trigonometry required in learner text','illustrativeLatitudes':[0,35,55],'illustrativeRadii':rs,'illustrationRadiiRounded':[60,49,34],'notExactSourceLocations':True,'sameSpeedTimeOrderEqualsDistanceOrder':True,'eastWestSameLatitudeCircumference':True,'sourcePositionOrder':'甲離赤道最遠；乙近赤道，丙低緯，丁南緯30多度','answer':'A'},ensure_ascii=False,indent=2)+'\n')
x={'id':'q-398','subject':'Geography','title':'離赤道越遠，緯線圈越短','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-398-generate.py','startedAt':'2026-10-29T06:53:50.328686+00:00','panels':[{'heading':'① 越靠近極地，緯線圈越小','text':'本題始終朝正東或正西飛行，沿同一緯線繞行。赤道的緯線圈最大，離赤道越遠，圈長越短；要比較緯度離赤道多遠，不是經度大小。','alt':'新原生由極地方向看同心緯線圈，赤道最大/近極地較小，明示非四點精確定位；半徑按球面緯度關係計算。'},{'heading':'② 同樣速率，較短的圈先繞完','text':'時間＝距離÷速率。四人速率相同，甲在圖中離赤道最遠，緯線圈最短，因此最先回到起點，選A。平面地圖把緯線畫成差不多長，不能直接拿圖上橫線長度當繞行距離。','alt':'新原生時間關係與同速率短/長圈長條，僅定性示意不造實際距離時間；甲最高絕對緯度依原圖判讀。'},{'heading':'③ 向東、向西，不改變同一圈的長度','text':'沿同一緯線順向或反向繞一圈，距離一樣。丁在南半球也不代表圈長最短，仍須比較離赤道的距離。題目已排除其他因素，不加入風向或時差來改變判斷。','alt':'新原生同圓起點及相反方向箭頭說明一圈同長，非兩飛行員實際航線；保留題目等速排除其他因素的模型。'}],'fourth':{'answer':'答案：A，甲','points':['甲距赤道最遠，緯線圈最短。','等速下，距離短，所需時間就少。','不以南北正負號、經度或地圖橫線長度判圈長。']},'protectedWords':['緯線圈','赤道','正東','正西','南半球','平面地圖','時間＝距離÷速率'],'rationale':'實看原卷5全題四項與必要全球四點圖，甲北高緯比丁南中緯更遠赤道，已核A；原AI錯D已結案不重開。用幾何緯線圈及等速時間/反向同長圖比人物飛行更清楚，無來源AI。','promptSummary':'新原生三格：極地方向觀看的緯線圈尺寸；等速時間距離圖；相反方向繞同圈距離不變。','answerCheckedAgainst':'原卷四點甲離赤道最遠且紅改A；National Geographic/University of Hawaii緯線離赤道越遠越小支持；同速t=d/v獨立核A。','officialReferences':[{'title':'National Geographic Society・Latitude','url':'https://education.nationalgeographic.org/resource/latitude/'},{'title':'University of Hawaii・Locating Points on a Globe','url':'https://manoa.hawaii.edu/exploringourfluidearth/physical/world-ocean/locating-points-globe'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-398-source-ac22993429.jpg'],'necessaryFigures':['site/dist/assets/questions/q-398-figure-516248caac.jpg'],'visualChecked':True,'answer':'A','notes':'親見全球圖甲北高緯/乙近赤道/丙低緯/丁南中緯；不假稱四點都精確落整數緯度。'},'geometryValidation':'docs/comics/q-398-geometry-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-398.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
