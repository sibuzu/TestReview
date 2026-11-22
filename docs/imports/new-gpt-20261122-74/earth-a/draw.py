from pathlib import Path
import json,html
B=Path('docs/imports/new-gpt-20261122-74/earth-a');INK='#28465a';BLUE='#287aa3';RED='#ce704a';GREEN='#37816c';GOLD='#c5914c'
def tx(x,y,t,s=22,c=INK,a='middle'):return f'<text x="{x}" y="{y}" text-anchor="{a}" fill="{c}" font-size="{s}" font-family="sans-serif">{html.escape(t)}</text>'
def path(d,fill,stroke=INK,w=2):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'
def rect(x,y,w,h,c):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
def arr(x,y,z,w,c=BLUE):return f'<path d="M{x} {y}L{z} {w}" stroke="{c}" stroke-width="5" marker-end="url(#arrow)"/>'
def svg(body,title):return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="720" viewBox="0 0 360 360"><title>{html.escape(title)}</title><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker><pattern id="rock" width="17" height="17" patternUnits="userSpaceOnUse"><path d="M3 5l4 3m3 4l3-4" stroke="#706a68" stroke-width="1" opacity=".3"/></pattern><linearGradient id="mantle" x2="0" y2="1"><stop stop-color="#f2d3aa"/><stop offset="1" stop-color="#e2ac78"/></linearGradient></defs><rect width="360" height="360" rx="16" fill="#f4f8f5"/>{body}</svg>'''
def sub(scene='sub',labels=True):
 o=rect(20,90,320,215,'url(#mantle)')+rect(20,90,320,56,'#c9e5ef')
 if scene=='sub':
  o+=path('M20 145H174L214 180L300 278L282 292L198 194L162 165H20Z','#748f9c')
  o+=path('M197 145L216 161L233 141H266L287 105L307 141H340V202H245L220 176Z','#c8ac87')
  o+=path('M20 145H174L214 180L300 278L282 292L198 194L162 165H20Z','url(#rock)',stroke='none')
  o+=arr(53,115,141,115)+arr(322,89,250,89)+arr(221,206,264,255)
  if labels:o+=tx(202,65,'海溝',23)+path('M202 73V137','none',INK,1.5)+tx(79,193,'海洋板塊',20)+tx(284,227,'大陸板塊',20)+tx(105,280,'向下隱沒',21,BLUE)
 else:
  o+=path('M20 160H102L133 132L149 148L176 95L199 126L215 105L240 157H340V210H234L210 242L185 251L155 234L125 210H20Z','#c9b08b')
  o+=path('M20 160H102L133 132L149 148L176 95L199 126L215 105L240 157H340V210H234L210 242L185 251L155 234L125 210H20Z','url(#rock)',stroke='none')
  o+=arr(40,112,112,112)+arr(321,112,249,112)+arr(179,182,179,137,GREEN)
  if labels:o+=tx(83,285,'大陸板塊',20)+tx(279,285,'大陸板塊',20)+tx(180,72,'碰撞成山',24,GREEN)+tx(180,330,'聚合也可能沒有海溝',22)
 return o

def ridge(with_trench=False,age=False):
 o=rect(20,95,320,205,'url(#mantle)')+rect(20,95,320,65,'#cae5ef')
 if with_trench:
  o+=path('M20 166H73L99 144L125 166H237L270 196L319 263L303 278L252 210L228 185H125L99 165L73 185H20Z','#7d98a4')
  o+=path('M264 166L278 178L290 154H340V219H311L288 197Z','#bda984')
  o+=arr(131,122,220,122)+arr(80,122,32,122)+arr(252,218,281,254)
  o+=tx(99,65,'中洋脊',23)+tx(277,87,'海溝',22)+path('M99 72V135M277 94V162','none',INK,1.5)
  o+=path('M100 284Q87 243 99 173','none',RED,7)+arr(100,231,99,175,RED)
 else:
  o+=path('M20 176H127L180 139L232 176H340V207H233L180 166L127 207H20Z','#7c97a2')
  if age:
   for x,col in [(30,'#557ba7'),(75,'#829ec0'),(120,'#b9c8c1'),(165,'#e8c27d'),(210,'#b9c8c1'),(255,'#829ec0'),(300,'#557ba7')]:o+=rect(x,182,30,20,col)
  o+=arr(148,112,55,112)+arr(212,112,305,112)
  o+=path('M180 292Q161 252 179 176','none',RED,9)+arr(180,242,180,178,RED)
  o+=tx(180,68,'中洋脊',25)+path('M180 75V131','none',INK,1.5)+tx(180,283,'岩漿上升',22,RED)
 return o

panels={}
panels[1172]=[
 (sub(), '海洋板塊隱沒','海洋板塊在聚合邊界向下隱沒時，常形成海溝；這只是聚合邊界的一種情況。'),
 (sub('collision'),'大陸碰撞也是聚合','兩個大陸板塊互相靠近，地殼擠壓隆起成高山；沒有海溝仍可屬聚合邊界。'),
 (tx(180,36,'板塊就是岩石圈區塊',23)+rect(25,95,310,38,'#c5ac85')+rect(25,134,310,95,'#8b9c9e')+rect(25,230,310,84,'url(#mantle)')+path('M166 95V229','none',INK,5)+tx(95,121,'地殼',22)+tx(180,187,'上部地函堅硬層',22)+tx(180,280,'軟流圈',24,RED)+path('M18 95H9V229H18M340 95H350V229H340','none',GREEN,4)+tx(95,72,'板塊甲',22,GREEN)+tx(255,72,'板塊乙',22,GREEN)+tx(180,342,'同處厚度：板塊＝岩石圈',21),'岩石圈與板塊的厚度','板塊是岩石圈的一個區塊；同一位置的厚度相同，不表示所有不同板塊都一樣厚。'),
 ('<g transform="translate(0 20) scale(1 .42)">'+sub(labels=False)+'</g><g transform="translate(0 168) scale(1 .42)">'+sub('collision',False)+'</g>'+tx(180,30,'聚合：靠近，不保證海溝',22)+tx(180,164,'海洋板塊隱沒：常有海溝',20)+tx(180,330,'大陸碰撞：成山，不一定有海溝',19),'用反例排除絕對敘述','只要有大陸碰撞成山的反例，就不能說聚合邊界「就有海溝」。本題B錯誤，應選B。')]
panels[1173]=[
 (ridge()+tx(180,332,'新海洋地殼形成',24,GREEN),'中洋脊產生新地殼','岩漿在中洋脊附近上升並冷卻，形成新海洋地殼；這裡對應「形成」，不是舊地殼隱沒。'),
 (ridge(age=True)+tx(70,331,'較老',23,BLUE)+tx(180,331,'新',23,GOLD)+tx(291,331,'較老',23,BLUE),'地殼往兩側移動','新生地殼隨板塊向中洋脊兩側移動；同側距離中洋脊愈遠，通常形成愈早。色帶只示意相對年齡。'),
 (sub()+tx(180,332,'海溝：舊地殼向下隱沒',23,GREEN),'海溝附近向下隱沒','較老的海洋板塊可在聚合邊界隱沒。海溝是典型隱沒地形，符合題目的「沒入地函」。'),
 (ridge(True)+tx(180,333,'中洋脊生新，海溝隱沒舊',22,GREEN),'對照形成與隱沒位置','題目問舊地殼的去處，答案A海溝；D中洋脊則是新地殼的產生處。')]

def positions(bands=False):
 o=rect(25,110,310,55,'#c9e5ef')+rect(25,198,310,95,'url(#mantle)')+path('M25 178L58 150L91 178H272L307 219L296 232L265 198H91L58 173L25 198Z','#849da6')+path('M296 172L310 183L323 169H335V223H321L307 205Z','#bea87f')
 if bands:
  for x,col in [(95,'#e7c883'),(145,'#9fbab9'),(195,'#7e9eae'),(245,'#587d9e')]:o+=rect(x,180,40,16,col)
 o+=tx(58,66,'中洋脊',21)+tx(310,94,'海溝',21)+path('M58 73V142M310 100V167','none',INK,1.4)+arr(109,127,258,127)
 for x,t in [(112,'甲'),(181,'乙'),(251,'丙')]:o+=tx(x,236,t,25)+path(f'M{x} 210V200','none',INK,1.5)
 return o
snap=''
for j in range(3):
 y=76+j*86;snap+=tx(30,y+26,['早','中','晚'][j],22)+rect(57,y,270,34,'#f0d3a9')+rect(57,y,40,34,'#c9e5ef')+path(f'M57 {y+34}L77 {y+10}L97 {y+34}','#879ea6')
 for k,t in enumerate(['丙','乙','甲'][:j+1]):
  x=112+(j-k)*70;snap+=rect(x,y+3,49,27,['#65849d','#95b0b6','#e0bf7a'][k])+tx(x+24,y+25,t,21)
 snap+=arr(280,y-9,319,y-9)

panels[1174]=[
 (tx(180,30,'先找中洋脊，再找甲乙丙',22)+positions()+tx(180,334,'同側位置：甲 → 乙 → 丙',22),'核對原圖相對位置','原卷中洋脊在左，甲最近、乙居中、丙最遠且靠近右側海溝；先看清楚三者的位置。'),
 (tx(180,30,'靠近中洋脊，地殼較年輕',22)+positions(True)+tx(110,281,'新',23,GOLD)+tx(181,281,'較老',22)+tx(252,281,'最老',22,BLUE)+tx(180,334,'色帶只示意相對年齡',20),'由距離推相對年齡','中洋脊持續形成新地殼；向外移動愈遠，通常形成得愈早。因此年齡是丙＞乙＞甲。'),
 (tx(180,32,'依序形成，舊地殼向外移',22)+snap+tx(180,350,'三個時刻示意；未指定年數',20),'比較先後三個時刻','先形成的丙已移到較遠處，再形成乙，最後形成最靠近中洋脊的甲。圖示不是三者同時形成。'),
 (tx(180,30,'形成先後：丙 → 乙 → 甲',23)+positions(True)+tx(112,276,'最後',22,GOLD)+tx(181,276,'次之',22)+tx(251,276,'最早',22,BLUE)+tx(180,333,'D：丙最早，乙次之，甲最晚',20,GREEN),'把年齡轉成形成先後','最老等於最早形成，最年輕等於最晚形成。答案D；沒有距離與速率，不推算實際年數。')]
for n,ps in panels.items():
 qid=f'q-{n}';q=json.loads((B/'questions'/f'{qid}.json').read_text());paths=[]
 for i,(body,head,txt) in enumerate(ps,1):
  p=B/'art'/f'{qid}-panel-{i}.svg';p.write_text(svg(body,head));paths.append(str(p))
 spec=dict(id=qid,subject='Earth',title=q['title'].split('｜')[1],art=paths[0],panels=[dict(heading=f'{["①","②","③"][i]} {p[1]}',text=p[2],image=paths[i],alt='新製地質概念圖：'+p[1],caption='新製地科輔助示意，非原卷；相對位置依題意，非實際比例。')for i,p in enumerate(ps[:3])],fourth=dict(answer='答案 '+q['correctOption'],points=[ps[3][2]],image=paths[3],alt='新製整合圖：'+ps[3][1]),sourceUrl='https://chatgpt.com/share/6b01da76-e42c-83ec-921a-80ff392862c1',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=q['images'],answerCheckedAgainst=q['explanation'],rationale='依原卷條件新製四張地質剖面及相對年齡圖；精確箭頭、地殼與地函關係逐張核對，四張各有教學目的。',generationMethod='four newly authored exact native SVG geological diagrams',producerAgent='/root/source74_earth_a',layoutVersion='native-four-images-v7',protectedWords=['中洋脊','海洋地殼','大陸板塊','海洋板塊','岩石圈','軟流圈','海底擴張','甲乙丙'])
 (B/'specs'/f'{qid}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print('12 new geological SVGs and 3 specs written')
