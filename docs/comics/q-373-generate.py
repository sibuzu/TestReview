from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def line(x,y,xx,yy,col='#829b8c',w=1.5):s.append(f'<path d="M{o+x} {y}L{o+xx} {yy}" fill="none" stroke="{col}" stroke-width="{w}"/>')
 def box(y,t,color='#dce8d0'):s.append(f'<rect x="{o+10}" y="{y}" width="160" height="29" rx="5" fill="{color}"/>');txt(90,y+19,t,11)
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#edf2f5","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  txt(90,18,'原有地形面，後來抬升',10);box(34,'聯合沖積扇')
  line(90,65,90,83);line(86,78,90,83);line(94,78,90,83)
  s.append(f'<path d="M{o+14} 146L{o+31} 140L{o+48} 106L{o+139} 106L{o+158} 139L{o+170} 146V155H{o+14}Z" fill="#c0d1aa" stroke="#78936d" stroke-width="1.5"/>')
  txt(93,99,'較平緩的抬升地形面',9);txt(90,174,'形狀概念示意，非原圖',9)
 elif i==1:
  txt(90,18,'依題幹比較北、南高度',10)
  line(31,143,166,143);line(31,143,31,40)
  for h in [0,200,400]:
   y=143-h*.2;txt(18,y+3,str(h),8);line(29,y,33,y)
  txt(22,32,'公尺',8)
  for x,h,l in [(54,200,'北'),(111,440,'南')]:
   s.append(f'<rect x="{o+x}" y="{143-h*.2}" width="29" height="{h*.2}" fill="{ "#9bb58c" if h==200 else "#83a8b6"}"/>');txt(x+14.5,143-h*.2-8,str(h),12);txt(x+14.5,158,l,10)
  txt(90,176,'約200 → 440公尺',10)
 else:
  txt(90,18,'把形狀與標高一起核對',10)
  for y,t in [(32,'A 中心較低'),(66,'B 標高達千餘公尺'),(100,'C 中央明顯高起'),(134,'D 較平緩面、200/400')]:box(y,t,'#dce8d0' if y==134 else '#f8f7ef')
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-373.svg';Path(art).write_text(''.join(s))
q={'id':'q-373','subject':'Geography','title':'台地要合看地形面與實際標高','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-373-generate.py','layoutVersion':'native-fluid-v6','panels':[{'heading':'① 沖積扇後來隆升，留下較平緩地形面','text':'題幹說這裡原是濁水溪與大肚溪的聯合沖積扇，後來因板塊運動隆升。這組線索指向台地，不是只因種鳳梨、做鳳梨酥就判地形。','alt':'新製沖積扇到抬升地形面流程與概念剖面，不重畫四選項地形，也不宣稱台地每一處都完全平坦。'},{'heading':'② 依題給高度，北約200、南到440公尺','text':'除了地形種類，還要核對題幹的200至440公尺高度線索。不能只看到某圖有平緩面，就忽略它實際標到千餘公尺；這題須同時符合形狀與高度。','alt':'新製依題幹北200南440兩條同刻度柱，比例440/200=2.2；不是測量整個台地的真實連續剖面或所有北端點高度。'},{'heading':'③ 回原卷四圖，D兩條件最符合','text':'D有廣而較平緩的面，圖上200、400公尺也接近題給範圍。A中心較低，B標高遠高於題目，C是中央明顯高起的山體，因此選D。','alt':'新製A中心低/B高度過高/C山體/D平緩面加200400的文字核對卡；原四張等高線圖仍用原卷，不以生成圖替換。'}],'fourth':{'answer':'答案 D：較平緩地形面，標高也相符','points':['原為聯合沖積扇，後來隆升成台地。','形狀之外，還要讀200至440公尺的高度線索。','D圖有200、400標高；不把台地誤說成低平平原。']},'protectedWords':['聯合沖積扇','濁水溪','大肚溪','板塊運動','鳳梨酥','200公尺','440公尺','200至440公尺','千餘公尺','地形面','台地','等高線','低平平原'],'originalChecked':{'images':['site/dist/assets/questions/q-373-source-9e9c3ad40f.jpg'],'necessaryFigures':['site/dist/assets/questions/q-373-figure-bbb59a589f.jpg'],'visualChecked':True,'answer':'D','notes':'親見完整4題與四圖A中心較低、B千餘標高/C山體/D200400平緩面；依題幹北200南440線索，不改原題或沿AI誤認B。'},'answerCheckedAgainst':'原卷D地形面與200400標高同時吻合，A/B/C依中心起伏及高度排除；已核定D不重問。外部官方資料支持八卦台地地形面與北低南高概念，圖中200/440明限題幹不充整區實測。','rationale':'新原生隆升概念剖面、題給高度同比柱、四圖核對三步，直接教會合看形狀與數值；保留原卷四選項而不AI重製地形，沒有把平緩等於低海拔。','references':[{'title':'彰化縣志：地理篇','url':'https://files.chcg.gov.tw/files/04_58_1090307.pdf','access':'official search-result excerpt read','supports':'八卦台地位大肚溪南濁水溪北、平坦地形面概念'}],'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selected':'D','heightScope':'原題描述，不是台地所有點真實高度','northGivenM':200,'southGivenM':440,'barHeightRatio':2.2,'originalOptionsReplaced':False},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
D=json.loads(Path('site/dist/data.json').read_text());sid=next(x['sourceId'] for x in D['questions'] if x['id']=='q-373');q['sourceUrl']=next(x['url'] for x in D['sources'] if x['id']==sid)
Path('docs/comics/q-373.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
