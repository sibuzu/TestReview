from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def t(x,y,z,size=10,c='#284f50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{c}">{z}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eef3e6","#eaf0f3","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'先讀方向，再讀高度',11);t(26,38,'西',12);t(156,38,'東',12)
  s.append(f'<path d="M{o+20} 137 L{o+48} 135 L{o+65} 129 L{o+77} 123 L{o+87} 128 L{o+102} 101 L{o+115} 116 L{o+128} 68 L{o+140} 87 L{o+158} 48 L{o+158} 138 Z" fill="#8eac74"/><path d="M{o+19} 44V139H{o+163}" fill="none" stroke="#577565"/>')
  t(44,154,'低地',10);t(99,154,'丘陵',10);t(148,154,'山地',10);t(90,173,'起伏趨勢示意，非測量重繪',8)
 elif i==1:
  t(90,18,'苗栗：由西往東的排列',10)
  for y,a,b in [(34,'西部','平原、低地'),(79,'中間','丘陵'),(124,'東部','山地')]:
   box(15,y,150,34,'#d8e7cc');t(90,y+13,a,8);t(90,y+28,b,12)
   if y<124:s.append(f'<path d="M{o+90} {y+36}v7m-3-3 3 3 3-3" fill="none" stroke="#78918c"/>')
  t(90,174,'低 → 高，符合圖中趨勢',9)
 else:
  t(90,18,'方向與高度一起比',11)
  for y,a,b in [(34,'宜蘭典型剖面','西高東低：方向相反'),(79,'彰化八卦臺地','不合東側二千多公尺'),(124,'臺北市域','不合本圖的高度組合')]:
   box(10,y,160,34,'#f5e3c3');t(90,y+13,a,10);t(90,y+28,b,9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-420.svg';Path(art).write_text(''.join(s))
q={'id':'q-420','subject':'Geography','title':'先讀西東方向，再看地形高低','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-420-generate.py','startedAt':'2026-10-29T06:43:33.717436+00:00','panels':[{'heading':'① 左西右東，整體西低東高','text':'先看原圖方向：左端西、右端東。西側低地向東經丘陵，再進入二千多公尺的山地。中途仍有谷地起伏，不能把整體升高誤讀成每一步都變高。','alt':'新原生趨勢剖面，方向西到東，西低地/丘陵/東山地，明標趨勢示意非測量重繪；保留原圖精確數據。'},{'heading':'② 苗栗的地形排列最吻合','text':'苗栗西濱臺灣海峽，地形由西向東依序可見平原、丘陵與山地，與本圖的整體趨勢吻合。應把方向與高度合起來判斷，選D。','alt':'新原生三層平原低地→丘陵→山地關係圖，對照苗栗官方地理環境，不畫虛構縣界或精確測線。'},{'heading':'③ 有山還不夠，還要比較方向與高度','text':'宜蘭典型地形由西側山地向東側平原降低，方向不合；彰化的八卦臺地不合圖中二千多公尺的東側山地；臺北市域也不符本圖的高度組合。','alt':'三選項對照卡：宜蘭方向、彰化高度、臺北高度組合，各自比本題剖面，不把所有東部縣市方向一概而論。'}],'fourth':{'answer':'答案：D，苗栗縣','points':['方向：西側低地，東側山地。','排列：平原、丘陵、山地，符合苗栗。','原圖56.6公里是此測線長度，不是全縣東西寬。']},'protectedWords':['苗栗縣','臺北市','宜蘭縣','八卦臺地','西低東高','56.6公里','二千多公尺','臺灣海峽'],'rationale':'實看原卷48完整題幹四項與必要剖面，左西右東、東側2000至2500公尺、56.6公里；官方苗栗地理環境由西往東平原丘陵山地支持D。新SVG地形趨勢與分類流程更利於方向高度判讀，不用人物或來源AI圖，不假造測量值/測線位置。','promptSummary':'新精確原生三格：定性西低東高剖面；苗栗西到東地形排列；宜蘭方向/彰化高度/臺北組合排除。','answerCheckedAgainst':'親見原卷A臺北/B宜蘭/C彰化/D苗栗與必要剖面；官方地理環境四地形由西往東排列支持D，既有原AI國別/選項OCR訂正不重問。','officialReferences':[{'title':'苗栗縣政府・地理環境','url':'https://www.miaoli.gov.tw/cp.aspx?n=260','evidence':'平原、丘陵、臺地及山脈；除臺地外由西向東依序排列。全縣約64公里不同本題56.6公里測線。'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-420-source-8be9e962ee.jpg'],'necessaryFigures':['site/dist/assets/questions/q-420-figure-53d589d1a5.jpg'],'visualChecked':True,'answer':'D','notes':'實看全文及必要剖面，方向/高度/56.6均核對；新剖面是概念示意，無測線實測冒充。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-420.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
