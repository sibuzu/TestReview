from pathlib import Path
import json,math,hashlib
lat=22.63;lon=120.31;ly=130-(lat-22)*24;ex=30+(lon-120)*60
assert 22<lat<23.5<25.5 and 120<lon<121<122
assert 130-(23.5-22)*24<ly<130 and 30<ex<90
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def line(x1,y1,x2,y2,col='#829b91',w=1.3,dash=''):s.append(f'<path d="M{o+x1} {y1}L{o+x2} {y2}" fill="none" stroke="{col}" stroke-width="{w}" {dash}/>')
 def dot(x,y):s.append(f'<circle cx="{o+x}" cy="{y}" r="4" fill="#b58a4c"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['緯度先判南北','經度再配合本島輪廓','回原卷圖：行政區丁'][i],11)
 if i==0:
  line(43,135,43,40);line(40,45,43,40);line(43,40,46,45);txt(43,34,'N',8)
  for la,label in [(22,'22°'),(23.5,'約23.5°'),(25.5,'25.5°')]:
   y=130-(la-22)*24;line(39,y,47,y);txt(19,y+3,label,8)
  yy=130-(23.5-22)*24;line(48,yy,162,yy,'#a9b8a0',1,'stroke-dasharray="3 2"');txt(111,yy-7,'北回歸線附近',9)
  dot(43,ly);line(49,ly,77,ly,'#b58a4c');txt(116,ly+4,'22.63°N',13)
  txt(90,157,'在北回歸線以南',11);txt(90,175,'配合臺灣位置判為南部',9)
 elif i==1:
  line(25,102,159,102);line(154,99,159,102);line(159,102,154,105);txt(165,105,'E',8)
  for lo in [120,121,122]:
   xx=30+(lo-120)*60;line(xx,98,xx,106);txt(xx,120,str(lo)+'°',9)
  dot(ex,102);line(ex,59,ex,96,'#b58a4c',1,'stroke-dasharray="3 2"');txt(67,48,'120.31°E',14)
  txt(90,151,'緯度＋經度一起看',11);txt(90,175,'不能只用一個數字猜縣市',9)
 else:
  for j,z in enumerate(['兩個坐標合看','臺灣西南部高雄一帶','對照圖（二）標記','丁 → D']):
   y=34+j*32;s.append(f'<rect x="{o+12}" y="{y}" width="156" height="24" rx="4" fill="{("#d7e6c8" if j==3 else "#f9f9f2")}"/>');txt(90,y+17,z,11)
   if j<3:line(90,y+25,90,y+30);line(87,y+27,90,y+30);line(90,y+30,93,y+27)
  txt(90,176,'題目問行政區，不是山峰',9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-548.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-548-coordinate-validation.json').write_text(json.dumps({'givenLatitude':lat,'givenLongitude':lon,'latitudeAxis':[22,25.5],'longitudeAxis':[120,122],'latitudeMonotonicNorthUp':True,'longitudeMonotonicEastRight':True,'latitudePixel':ly,'longitudePixel':ex,'latitudeBelowApproxTropic':lat<23.5,'longitudeNearWesternSideOfIslandWhenCombinedWithOutline':True,'originalMapLabelsVisuallyChecked':['甲東北','乙中北偏西','丙中部內陸','丁西南高雄'],'noExactMountainCoordinateClaim':True,'originalElevationPreserved':300,'note':'經緯數線精確按數值位置繪，不重造原圖縣市界；行政區字母須回原圖核對。'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-548','subject':'Geography','title':'兩個坐標合看，再回原圖找丁','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-548-generate.py','startedAt':'2026-10-29T06:25:21.016218+00:00','panels':[{'heading':'① 北緯22.63°，先縮到臺灣南部','text':'北緯22.63°在北回歸線以南，配合臺灣位置，先把範圍縮到南部。緯度用來判南北，不能只因某個山區有獼猴，就忽略題目直接給出的定位資訊。','alt':'新原生緯度數線由南22到北25.5，22.63精確落在約23.5北回歸線以南；非新畫臺灣行政界。'},{'heading':'② 東經120.31°，再合看西南側位置','text':'東經120.31°再配合本島輪廓與南部緯度，可定位到高雄一帶。經度和緯度要一起看；300公尺與猴群是情境線索，不能取代坐標或改掉原題高度。','alt':'精確東經數線120→121→122，120.31標在靠120一側，明示合緯度/輪廓才能定西南；不拿單一經度斷行政區。'},{'heading':'③ 回原圖查行政區，丁才對得上','text':'原圖甲在東北、乙在中北部偏西、丙在中部內陸，都不合題給的西南側位置。丁對應高雄所在行政區，故選D。題目只問附近行政區，不必把坐標說成某座山峰的精確位置。','alt':'兩坐標→西南高雄→原卷標記丁→D流程，不新增市界/山名或沿原AI錯置甲乙縣市名。'}],'fourth':{'answer':'答案：D，丁','points':['緯度先判南北，經度再配合輪廓判東西。','兩坐標指向西南部高雄一帶，回圖找丁。','保留附近與約300公尺，不擅自精確到山峰。']},'protectedWords':['北緯22.63°','東經120.31°','北回歸線','獼猴','300公尺','高雄','行政區'],'rationale':'親見5題全文四選項/必要行政圖及4倍放大，甲東北乙中北偏西丙內陸丁西南位置獨立核D。官方高雄市政府定位西南及經緯範圍核對。新原生精確坐標數線/回圖流程，不讓AI亂畫縣市界或獼猴代替定位；不沿用來源AI。','promptSummary':'原生三格：緯度22.63在約23.5南；經度120.31數線精確位置；合坐標高雄對回原卷丁D。精確關係用SVG，不重造行政圖或山峰位置。','answerCheckedAgainst':'原卷22.63N/120.31E/約300與行政甲乙丙丁，放大核丁西南；高雄市政府Knowing Kaohsiung官方經緯範圍與西南位置交叉核對，沿D而不指定山峰。','officialReferences':[{'title':'高雄市政府・Knowing Kaohsiung（經緯位置）','url':'https://www.kcg.gov.tw/En/cp.aspx?n=E5AA72D4F35F91D0'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-548-source-b549489ad9.jpg'],'necessaryFigures':['site/dist/assets/questions/q-548-taiwan-map-9287c59599.jpg'],'visualChecked':True,'answer':'D','notes':'完整題幹四項與必要圖實看，另用/tmp只讀放大確認丁字與相對行政位置；不使用原AI錯置甲台東乙花蓮說法，不改300高度。'},'coordinateValidation':'docs/comics/q-548-coordinate-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-548.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
