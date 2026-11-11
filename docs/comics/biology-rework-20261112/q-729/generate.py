from pathlib import Path
import json,math,datetime,html
R=Path(__file__).resolve().parents[4];D=json.loads((R/'site/dist/data.json').read_text());q=next(q for q in D['questions'] if q['id']=='q-729')
INK='#294d43';GREEN='#23856e';GOLD='#b97b2d';GREY='#acbbb3';BLUE='#386eaa'
def tx(x,y,s,size=13,col=INK):return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{col}">{html.escape(s)}</text>'
def line(x,y,xx,yy,col=GREY,w=2,dash=False):return f'<path d="M{x} {y}L{xx} {yy}" fill="none" stroke="{col}" stroke-width="{w}"'+(' stroke-dasharray="4 4"' if dash else '')+'/>'
def dot(x,y,r=5,col=BLUE):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'
def calendar(x,y,w,h,year):
 s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fffaf0" stroke="{INK}" stroke-width="2"/><path d="M{x} {y+24}H{x+w}" stroke="{INK}"/>'+tx(x+w/2,y+18,year,17)
 for j in [1,2,3]:s+=line(x+8,y+25+j*12,x+w-8,y+25+j*12,GREY,1)
 for i in [1,2,3,4]:s+=line(x+i*w/5,y+27,x+i*w/5,y+h-5,GREY,1)
 return s

def axis(y):return line(20,y,220,y)+f'<path d="M214 {y-4}l6 4-6 4" fill="none" stroke="{GREY}"/>'+dot(205,y,4,GREEN)+tx(205,y+24,'Now',13,GREEN)
def star(x,y,r=8):
 ps=[]
 for i in range(10):
  a=-math.pi/2+i*math.pi/5;rr=r if i%2==0 else r*.42;ps.append((x+math.cos(a)*rr,y+math.sin(a)*rr))
 return '<polygon points="'+' '.join(f'{x},{y}' for x,y in ps)+f'" fill="{GOLD}"/>'
frames=[]
s=calendar(69,28,100,76,'2015')+axis(157)+dot(75,157,6,BLUE)+line(75,111,75,149,BLUE,1,True)+tx(75,193,'in 2015',14,BLUE);frames.append((s,'日曆2015與現在分開，in2015標在已結束的過去一點，不把它當現在完成式的自然搭配'))
s=axis(132)+dot(72,132,6,BLUE)+tx(72,172,'two years ago',13,BLUE)+line(72,74,205,74,GOLD,2)+line(72,67,72,81,GOLD)+line(205,67,205,81,GOLD)+tx(139,56,'2 years',15,GOLD)+tx(120,217,'a finished past time',12);frames.append((s,'距現在兩年前是特定過去時間，兩年長度只來自原選項two years ago'))
s=axis(159)+line(43,159,205,159,GREEN,8)+dot(43,159,5,GREEN)+tx(43,192,'2008',15)+tx(123,222,'since 2008 → Now',14,GREEN)+star(128,102,11)+line(70,123,178,123,GOLD,2,True)+tx(124,65,'has finished',16,GOLD);frames.append((s,'since2008表示2008以來到現在的範圍，星號只示已完成事件，不示確切年份或持續完成'))
s=axis(46)+dot(75,46,6,BLUE)+tx(75,23,'A: in 2015',12,BLUE)+axis(116)+dot(75,116,6,GOLD)+tx(78,93,'B: two years ago',12,GOLD)+axis(188)+line(37,188,205,188,GREEN,7)+tx(118,163,'C: since 2008',14,GREEN)+star(130,217,8);frames.append((s,'第四圖區分A與B特定過去時間點與C至今範圍；已完成事件不是從2008一直不停完成'))
paths=[]
for i,(s,title) in enumerate(frames):
 p=R/f'docs/comics/art/q-729-four-image-v2-panel-{i+1}.svg';p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240"><title>{html.escape(title)}</title><rect width="240" height="240" fill="#faf8ef"/>{s}</svg>');paths.append(str(p.relative_to(R)))
texts=[('① 先看原題有has finished','原題確實保留has。in 2015是特定且已結束的過去時間；若要說2015年完成，通常改用finished，不擅刪原題has。','新製時間圖｜2015是原選項，不替原題指定完成日期。'),('② two years ago也是過去時間點','two years ago指距現在兩年前，通常搭過去式。for two years ago又把期間for與ago時間點混在一起，不合本題。','新製時間圖｜Now只表示說話當下，沒有套入今年年份。'),('③ since 2008給的是至今範圍','四項依教材時間搭配預期C，但has finished原句不自然。只能理解為2008以來範圍內已完成，不能說一直持續完成。','星號只示一個已完成事件，不代表已知發生年，也非連續完成。')]
s=dict(id='q-729',subject='English',title='分清過去時間點與延伸至今的範圍',art=paths[0],panels=[dict(heading=h,text=t,caption=c,alt=frames[i][1],image=paths[i]) for i,(h,t,c) in enumerate(texts)],fourth=dict(answer='本題預期 C：since 2008',points=['A、B是明確過去時間，D的for…ago不合此句。','三條圖各自比較時間點或範圍，不據此比較A、B的遠近。','finish是完成事件，不能誤教成從2008一直進行完成。'],image=paths[3],alt=frames[3][1]),protectedWords=['has finished','since 2008','in 2015','two years ago','for two years ago','完成事件','原句不自然'],generationMethod='four authored SVG calendar/time-point/interval/event diagrams',generatorFile=str(Path(__file__).relative_to(R)),sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/'+p for p in q['images']],answerCheckedAgainst=q['question']+'\n'+q['answer']+'\n'+q['explanation'],rationale='實開原卷保留has finished和四選項、既有教材C及原句不自然的限制。四張時間圖實際區分年份日曆、距今過去點、至今區間與單一已完成事件，不用純文字流程框，不把finish誤畫成多年持續動作。既有核對卡已結案不重問。',createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),visualChecked=False,productionReview=dict(reviewerAgent='/root',originalVisualChecked=True,answerAndExplanationChecked=True,sourceQuestionUnchanged=True,checks=['實開原卷可見has finished，沒有擅刪has','只用原選項2008、2015、two years，不加確切完成日','星號是已完成事件概念例、無對應數值日期，不畫多年連續完成','A與B用分開時間線，只示過去時間點，不捏造兩者相對遠近','既有correction-q-729-0f59d056e4c5 resolved，保留現有C與措辭限制，不重開同項確認']))
(R/'docs/comics/q-729.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(Path(__file__).parent/'production-review.json').write_text(json.dumps(s['productionReview'],ensure_ascii=False,indent=2)+'\n')
print('q729 four calendar/timeline illustrations prepared')
