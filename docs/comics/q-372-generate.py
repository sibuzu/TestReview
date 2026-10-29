from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=11,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(y,t,color='#dce8d0',size=12):s.append(f'<rect x="{o+12}" y="{y}" width="156" height="30" rx="5" fill="{color}"/>');txt(90,y+20,t,size)
 def line(x,y,xx,yy,col='#8ba193',w=1.5):s.append(f'<path d="M{o+x} {y}L{o+xx} {yy}" stroke="{col}" stroke-width="{w}" fill="none"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#edf2f5","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  txt(90,18,'里程是位置，距離要相減',10)
  line(27,72,153,72,'#759384',3)
  for x,t in [(27,'197'),(153,'198')]:
   line(x,62,x,82);txt(x,51,t,14)
  line(27,96,153,96);line(27,90,27,101);line(153,90,153,101)
  txt(90,119,'198 − 197 = 1公里',12);txt(90,149,'不是197：198',12);txt(90,176,'距離關係示意，非實測圖',9)
 elif i==1:
  txt(90,18,'先統一成公分',11)
  for y,t in [(35,'1公里'),(88,'1,000公尺'),(141,'100,000公分')]:
   box(y,t)
   if y<141:
    line(90,y+32,90,y+49);line(86,y+44,90,y+49);line(94,y+44,90,y+49)
  txt(132,78,'×1,000',10);txt(132,131,'×100',10)
 else:
  txt(90,18,'圖上距離：實地距離',11)
  box(34,'10：100,000','#dce7ef',15);txt(90,85,'兩邊同除以10',11)
  line(90,90,90,107);line(86,102,90,107);line(94,102,90,107)
  box(115,'1：10,000','#dce8d0',17)
  txt(90,173,'單位一致，才可以約分',10)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-372.svg';Path(art).write_text(''.join(s))
q={'id':'q-372','subject':'Geography','title':'先求兩點間距，再用同單位求比例尺','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-372-generate.py','layoutVersion':'native-fluid-v6','panels':[{'heading':'① 先把里程位置，變成兩點間距','text':'197公里與198公里是道路上的里程位置。兩處相差198－197＝1公里；不能把197與198直接相除，也不能拿198公里當兩點距離。','alt':'新精確里程兩標點與差值1公里，線段只表兩點關係、不是按螢幕長度實測10公分。'},{'heading':'② 公里換成公分，兩邊單位一致','text':'題給圖上距離是10公分，實地距離也要換成公分。1公里＝1,000公尺，每公尺100公分，所以1公里＝100,000公分。','alt':'新製公里到公尺到公分換算階梯，第一步乘1000、第二步乘100，數字精確不跳錯零。'},{'heading':'③ 圖上距離比實地距離，再約分','text':'比例尺是圖上距離：實地距離。代入同單位的10：100,000，兩邊都除以10，得到1：10,000，所以選C。','alt':'新精確比值10比100000同除10，約成1比10000，不把比例尺倒成實地比圖上。'}],'fourth':{'answer':'答案 C：1：10,000','points':['先相減：198－197＝1公里。','再換單位：1公里＝100,000公分。','最後約分：10：100,000＝1：10,000。']},'protectedWords':['197公里','198公里','1公里','10公分','1,000公尺','100公分','100,000公分','圖上距離','實地距離','1：10,000','10：100,000','比例尺'],'originalChecked':{'images':['site/dist/assets/questions/q-372-source-8679fbe73e.jpg'],'visualChecked':True,'answer':'C','notes':'親見原卷2題197至198公里/10公分與A197:198 B1:10 C1:10000 D1:1980000，C維持。'},'answerCheckedAgainst':'獨立計算198−197=1km=100000cm，圖上10cm約成1:10000；以原題距離而非198總里程，無更改已核定C。','rationale':'新精確里程差線段、單位階梯、同除10比值三步SVG配HTML，直接減少把GPS情境當解法或漏換單位的負擔；不用人物或來源AI，線段只關係示意非實際圖上公分長度。','generationCalls':0,'sourceAIUsed':False,'manualLineBreaks':False,'diagramChecks':{'firstKilometreMarker':197,'secondKilometreMarker':198,'differenceKm':1,'actualDistanceCm':100000,'mapDistanceCm':10,'scaleDenominator':10000,'displayLineIsMeasuredMap':False},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
D=json.loads(Path('site/dist/data.json').read_text());sid=next(x['sourceId'] for x in D['questions'] if x['id']=='q-372');q['sourceUrl']=next(x['url'] for x in D['sources'] if x['id']==sid)
q['protectedWords'] += ['198－197＝1公里','1公里＝100,000公分']
Path('docs/comics/q-372.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
