from pathlib import Path
import math,json,hashlib,datetime,itertools,sys
TARGETS=set(map(int,sys.argv[1:])) if len(sys.argv)>1 else set(range(1112,1121))
R=Path(__file__).resolve().parents[4];P=Path(__file__).parent;A=R/'docs/comics/art';A.mkdir(exist_ok=True)
C='#536b79';O='#d97866';H='#dbeaf1';CL='#82aa65';N='#6c91bc';gold='#d4a243';blue='#4c91aa';ink='#294e60'
def text(x,y,s,size=23,color=ink,anchor='middle'):
 from html import escape
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-family="Noto Sans CJK TC,sans-serif">{escape(s)}</text>'
def line(x,y,X,Y,color=ink,w=4,dash=''):return f'<path d="M{x} {y}L{X} {Y}" fill="none" stroke="{color}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def path(d,color=ink,w=4,fill='none'):return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}"/>'
def circle(x,y,r,fill,stroke='#fff',w=2):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def rect(x,y,w,h,fill='#fff',stroke=ink,rx=5):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
def arrow(x,y,X,Y,color=gold,w=5):
 a=math.atan2(Y-y,X-x);l=12;return line(x,y,X,Y,color,w)+path(f'M{X-l*math.cos(a-.5)} {Y-l*math.sin(a-.5)}L{X} {Y}L{X-l*math.cos(a+.5)} {Y-l*math.sin(a+.5)}',color,w)
def atom(x,y,e,r=21):return circle(x,y,r,{'C':C,'O':O,'H':H,'Cl':CL,'N':N}.get(e,'#ddd'),ink,2)+text(x,y+7,e,21,'#fff' if e in ['C','N'] else ink)
def mol(nodes,bonds):
 s=''
 for a,b,*rest in bonds:
  x,y=nodes[a][:2];X,Y=nodes[b][:2];s+=line(x,y,X,Y,ink,5)
  if rest and rest[0]==2:s+=line(x,y+8,X,Y+8,ink,3)
 for x,y,e,*rr in nodes:s+=atom(x,y,e,rr[0] if rr else 21)
 return s
def water(x,y,k=1):return f'<g transform="translate({x} {y}) scale({k})">'+mol([(0,0,'O'),(-32,32,'H'),(32,32,'H')],[(0,1),(0,2)])+'</g>'
def co2(x,y,k=1):return f'<g transform="translate({x} {y}) scale({k})">'+mol([(-50,0,'O'),(0,0,'C'),(50,0,'O')],[(0,1,2),(1,2,2)])+'</g>'
def beaker(x,y,w=100,h=140,fill='#d9ecf3'):
 return f'<g><path d="M{x} {y}V{y+h}Q{x} {y+h+8} {x+9} {y+h+8}H{x+w-9}Q{x+w} {y+h+8} {x+w} {y+h}V{y}" fill="{fill}" fill-opacity=".7" stroke="{ink}" stroke-width="4"/>'+line(x,y+35,x+w,y+35,blue,3)+'</g>'
def wave(x,y,X,Y,color=gold):
 dx,dy=X-x,Y-y;L=math.hypot(dx,dy);a=math.atan2(dy,dx);pts=[]
 for k in range(41):
  t=k/40;z=5*math.sin(t*math.pi*8);pts.append((x+dx*t-z*math.sin(a),y+dy*t+z*math.cos(a)))
 return '<polyline points="'+' '.join(f'{u:.1f},{v:.1f}' for u,v in pts)+f'" fill="none" stroke="{color}" stroke-width="4"/>'+arrow(X-14*math.cos(a),Y-14*math.sin(a),X,Y,color,3)
def save(n,j,s):
 if n not in TARGETS:return str(Path("docs/comics/art")/f"q-{n}-panel-{j}.svg")
 z=f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 360 360"><rect width="360" height="360" fill="#f4f8f8"/>{s}</svg>'
 f=A/f'q-{n}-panel-{j}.svg';f.write_text(z);return str(f.relative_to(R))
def spec(n,title,panels,fourth,alts,rationale,protected=[],sources=[]):
 if n not in TARGETS:return
 q=json.load(open(P/f'q-{n}.json'));im=[str(Path('docs/comics/art')/f'q-{n}-panel-{j}.svg') for j in range(1,5)]
 d=dict(id=f'q-{n}',subject='Physics-Chemistry',title=title,art=im[0],layoutVersion='native-four-images-v7',generationMethod='four new independent native SVG scientific structure/apparatus/relationship diagrams',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=q['images']+[x['src'] for x in q['questionFigures']],answerCheckedAgainst=q['explanation'],rationale=rationale,producerAgent='/root/comic_lane_3',visualChecked=False,panels=[dict(heading=h,text=t,image=im[i],alt=alts[i]) for i,(h,t) in enumerate(panels)],fourth=dict(answer=fourth[0],points=fourth[1],image=im[3],alt=alts[3]),protectedWords=protected,manualLineBreaks=False,createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),artHashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in im},supportingSources=sources)
 (R/f'docs/comics/q-{n}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# Exact truncated icosahedral C60 graph: 60 vertices,90 edges,degree3.
ph=(1+math.sqrt(5))/2;v=[]
for s,t in itertools.product([-1,1],repeat=2):v.extend([(0,s,t*ph),(s,t*ph,0),(s*ph,0,t)])
dist=lambda a,b:sum((x-y)**2 for x,y in zip(a,b))
e=[(i,j) for i in range(12) for j in range(i) if abs(dist(v[i],v[j])-4)<1e-7];vv=[]
for i,j in e:
 vv.extend([tuple((2*v[i][k]+v[j][k])/3 for k in range(3)),tuple((v[i][k]+2*v[j][k])/3 for k in range(3))])
ee=[(i,j) for i in range(60) for j in range(i) if abs(dist(vv[i],vv[j])-4/9)<1e-7]
assert len(vv)==60 and len(ee)==90 and all(sum(i in e for e in ee)==3 for i in range(60))
def cage(x,y,scale=1):
 a=.45;b=.35;v3=[]
 for X,Y,Z in vv:
  u=X*math.cos(a)+Z*math.sin(a);z=-X*math.sin(a)+Z*math.cos(a);v3.append((u,Y*math.cos(b)-z*math.sin(b),Y*math.sin(b)+z*math.cos(b)))
 s=''
 for i,j in sorted(ee,key=lambda z:sum(v3[k][2] for k in z)):
  X,Y,Z=v3[i];U,V,W=v3[j];s+=line(x+X*65*scale,y+Y*65*scale,x+U*65*scale,y+V*65*scale,'#b3c1c7' if Z+W<0 else C,3*scale)
 for i in sorted(range(60),key=lambda i:v3[i][2]):
  X,Y,Z=v3[i];s+=circle(x+X*65*scale,y+Y*65*scale,4*scale,'#bdcbd1' if Z<0 else C,'#eaf0f1',.7)
 return s
# q1112.
s=cage(180,174,1.32)+text(180,31,'C₆₀：60個碳原子',24)+text(180,333,'封閉籠狀分子',22);save(1112,1,s)
pts=[(180+72*math.cos(i*math.pi/3),175+72*math.sin(i*math.pi/3),'C') for i in range(6)]
s=mol(pts,[(i,(i+1)%6) for i in range(6)])
for i,(x,y,e0) in enumerate(pts):s+=line(x,y,180+(x-180)*1.5,175+(y-175)*1.5,C,4)
s+=text(180,35,'只看元素種類',26)+text(180,321,'局部片段：每個頂點都是C',20);save(1112,2,s)
s=water(180,161,1.8)+text(180,40,'水 H₂O：含H與O',25)+text(180,322,'兩種元素→化合物',24);save(1112,3,s)
s=text(180,30,'結構不同，同為碳',25)
# Graphite local three connected hexagons.
for cx,cy in [(103,120),(174,161),(103,202)]:
 p=[(cx+47*math.cos(k*math.pi/3),cy+47*math.sin(k*math.pi/3)) for k in range(6)]
 for k in range(6):s+=line(*p[k],*p[(k+1)%6],C,3)
 for x,y in p:s+=circle(x,y,6,C)
s+=text(109,288,'石墨局部',20)
for x,y in [(275,94),(237,163),(315,165),(277,232)]:s+=line(275,165,x,y,C,5)+atom(x,y,'C',17)
s+=atom(275,165,'C',22)+text(275,288,'鑽石局部',20)+text(180,337,'分類看組成，不看外形',22);save(1112,4,s)
spec(1112,'60個原子，仍只有一種元素',[('① 先看C₆₀的籠狀結構','一個分子含60個碳原子，但每個頂點都是碳。圖依截斷二十面體精確構成60頂點、90邊，不是把原子數當元素種類。'),('② 多個原子，不等於多種元素','局部放大仍全是C。依國中物質分類，單一元素組成的純物質屬元素物質；不能因分子很大就改判化合物或聚合物。'),('③ 用水分子對照化合物','水H₂O同時含氫、氧兩種元素，才是化合物。C₆₀沒有第二種元素，也沒有不同物質混合的條件。')],('答案A：元素',['富勒烯、石墨與鑽石結構不同，仍都只含碳；不要按外形或原子多寡分類。']),['新製精確C60閉籠，60碳頂點90鍵邊；線只表連接未指定鍵級。','新製C60局部六環及第三連接短線，只顯示部分結構，C標籤明示全碳。','新製水的一氧二氫彎曲分子，用元素種類差異作比較，非原卷。','新製石墨相連六環局部與鑽石四配位局部，皆標C，整合單一元素概念。'],'四張分別是精確C60閉籠、局部同元素、水分子比較、碳同素異形結構；均為真正分子/晶格幾何，不以文字框分類湊四圖。',['C₆₀','60個碳原子','化合物'],[{'url':'https://iupac.qmul.ac.uk/fullerene/','finding':'C60為閉籠全碳三配位結構。'},{'url':'https://edu.rsc.org/feature/symmetry-of-buckminsterfullerene/2020237.article','finding':'截斷二十面體60頂點、12五邊形、20六邊形。'}])
# q1113: real transfer geometries, no people placeholders.
s=rect(50,64,95,226,'#dfb8a7',C,35)+rect(35,50,125,254,'none',blue,42)+text(99,183,'熱源',24)
for y in [102,180,258]:s+=wave(165,y,315,y)
s+=text(249,49,'外部真空',24)+text(241,329,'紅外線向外傳',23);save(1113,1,s)
s=text(180,34,'傳導需要物質連接',24)+rect(34,97,292,49,'#bdd0da',C)
for x in range(60,310,39):s+=circle(x,121,10,O)+arrow(x-8,170,x+21,170,gold,3)
s+=text(180,208,'粒子間傳遞',22)+rect(34,243,106,38,'#bdd0da',C)+rect(221,243,105,38,'#bdd0da',C)+line(143,229,218,297,O,6)+line(143,297,218,229,O,6)+text(180,331,'真空間隙沒有傳導介質',20);save(1113,2,s)
s=text(180,31,'對流靠流體整體流動',23)+beaker(55,70,250,220)
s+=path('M110 249Q75 190 108 121',O,5)+arrow(106,139,108,121,O)+path('M248 122Q285 190 249 250',blue,5)+arrow(250,234,249,250,blue)+arrow(126,101,232,101,O)+arrow(234,266,126,266,blue)
s+=text(180,184,'氣體／液體',23)+text(180,332,'外部真空沒有這種流動',20);save(1113,3,s)
s=text(180,30,'多層隔熱，減少輻射交換',22)+rect(30,80,70,205,'#dfb8a7',C,20)
for x in [125,155,185,215]:s+=rect(x,70,10,224,'#c6d9e1',C,2)
s+=wave(102,135,122,135)+wave(229,160,324,160)+wave(324,222,229,222,blue)+text(280,120,'向外',21)+text(280,267,'也會吸收',18)+text(67,324,'熱源',20)+text(174,324,'隔熱層',20);save(1113,4,s)
spec(1113,'對外部真空，熱仍能以輻射傳播',[('① 沒有空氣，仍會發出紅外線','熱輻射以電磁波傳播，不需物質媒介。太空艙外近似真空，人體與太空衣仍可向外發出輻射。'),('② 傳導要有物質作媒介','固體粒子可逐步傳熱，但真空間隙沒有這種連續媒介。與工具接觸處仍可能傳導，不能說整套太空衣完全沒有傳導。'),('③ 對流要有流體移動','對流是氣體或液體的整體流動；周圍真空無空氣對流。因此A、C、D不是題目對外散熱的主要途徑。')],('答案B：輻射',['隔熱層減少輻射交換；太空衣也要防過熱並調節人體產熱，不是只防冷。']),['新製熱源/太空衣截面與向外紅外線箭頭，外側標真空。','新製固體粒子連接與真空間隙對比，真空處打叉只指缺乏傳導介質。','新製液體容器中暖升冷降循環，箭頭表示流體而非輻射。','新製多層隔熱剖面，向外發射與向內吸收波箭頭分別標示。'],'四張以輻射、粒子傳導、流體對流、多層隔熱的真實機制幾何比較，避免人體漫畫代替物理條件。',['熱輻射','太空衣','真空'],[{'url':'https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/','finding':'真空無對流；接觸物體可傳導，輻射仍可傳播。'}])
# q1114: ethanol correct valence.
def ethanol(x,y,k=1,hydrogens=False):
 nodes=[(-55,0,'C'),(0,0,'C'),(55,0,'O'),(93,30,'H')];b=[(0,1),(1,2),(2,3)]
 if hydrogens:
  nodes += [(-91,34,'H'),(-55,-52,'H'),(-55,52,'H'),(0,-52,'H'),(0,52,'H')];b += [(0,4),(0,5),(0,6),(1,7),(1,8)]
 return f'<g transform="translate({x} {y}) scale({k})">'+mol(nodes,b)+'</g>'
s=text(180,30,'乙醇：CH₃－CH₂－OH',23)+ethanol(160,175,1.15,True)+path('M205 132Q297 119 303 202Q274 258 215 214',gold,4)+text(262,291,'羥基－OH',23);save(1114,1,s)
s=text(180,30,'－OH ≠ OH⁻',29)+ethanol(113,107,.62,True)+text(180,173,'乙醇：共價連接',22)+beaker(68,200,220,100)
s+=text(120,253,'Na⁺',27)+text(236,253,'OH⁻',27)+text(180,334,'對照：NaOH水中有游離離子',18);save(1114,2,s)
s=text(180,28,'溶質與溶劑，要看情境',23)+beaker(31,100,118,175)+beaker(211,100,118,175)
for x,y in [(58,170),(90,220),(123,160)]:s+=circle(x,y,9,'#9561b6')
for x,y in [(232,185),(271,240),(304,170)]:s+=ethanol(x,y,.18,True)
s+=text(89,66,'碘溶於乙醇',19)+text(271,66,'乙醇加入大量水',17)+text(89,311,'乙醇＝溶劑',20)+text(271,311,'乙醇可作溶質',18);save(1114,3,s)
s=text(180,28,'A看分子，B看酸鹼性',23)+ethanol(159,118,1,True)
s+=rect(46,262,268,25,'#d8e8d5',C,3)+line(180,248,180,300,gold,6)+text(180,230,'近中性',24)+text(180,335,'含羥基，不表示呈鹼性',22);save(1114,4,s)
spec(1114,'乙醇含羥基，不等於溶液呈鹼性',[('① 從結構找共價羥基','乙醇可寫成CH₃－CH₂－OH，確實含－OH原子團，所以A成立。圖逐一核對2碳、6氫、1氧的連接。'),('② 羥基不是游離氫氧根','乙醇分子的－OH以共價鍵連接；不同於NaOH水中的OH⁻。不能只因化學式有OH，就把乙醇水溶液判成鹼性。'),('③ 常用來溶解別物時，是溶劑','C原印「溶質」照留。碘溶於乙醇時，乙醇是溶劑；加入大量水時乙醇可作溶質。D也錯，酒精殺菌並非濃度愈高必愈好。')],('答案A：含有－OH原子團',['乙醇水溶液依教材近中性；自製防蚊液的背景不等同效力驗證。']),['新製乙醇完整球棍結構，2C6H1O、C均四價，羥基圈示。','新製乙醇共價羥基與NaOH水中Na+及OH-比較，未混為同一分子。','新製兩個溶液情境：碘/乙醇與乙醇/大量水，瓶內僅概念分布不是濃度測量。','新製乙醇結構加近中性的定性位置圖，整合羥基與酸鹼性不同。'],'精確分子與溶液角色圖優於人物操作圖；四圖獨立描繪結構、離子差異、溶液情境、結構與性質整合，不提供防蚊配方效力背書。',['NaOH','－OH','OH⁻','乙醇','溶劑','溶質','CH₃－CH₂－OH','2碳','6氫','1氧'],[{'url':'https://www.cdc.gov/infection-control/hcp/disinfection-sterilization/chemical-disinfectants.html','finding':'一般酒精殺菌以適當含水濃度有效，無水乙醇不必然較佳；不延伸成所有消毒用途。'}])
# q1115: balanced species and safe distinction of chlorine/chloramine.
s=text(180,28,'Cl₂＋H₂O ⇌ HCl＋HClO',21)+mol([(70,110,'Cl'),(123,110,'Cl')],[(0,1)])+water(260,94,.85)
s+=text(180,116,'＋',26)+arrow(161,176,161,208,blue,3)+arrow(198,208,198,176,blue,3)+mol([(61,263,'H'),(112,263,'Cl')],[(0,1)])+mol([(223,263,'H'),(266,263,'O'),(310,263,'Cl')],[(0,1),(1,2)])+text(175,271,'＋',25)+text(180,335,'分子示意：原子數守恆',21);save(1115,1,s)
s=text(180,29,'鹽酸提供H⁺與Cl⁻',25)+mol([(57,105,'H'),(104,105,'O'),(151,105,'Cl')],[(0,1),(1,2)])+text(241,88,'H⁺',27)+text(288,137,'Cl⁻',27)+arrow(180,169,180,208,gold)
s+=mol([(68,262,'Cl'),(124,262,'Cl')],[(0,1)])+water(268,247,.9)+text(180,270,'＋',25)+text(180,334,'促進左移→形成Cl₂',23);save(1115,2,s)
s=text(180,30,'氯氣與氯胺，皆有風險',23)+mol([(80,108,'Cl'),(144,108,'Cl')],[(0,1)])+text(253,112,'Cl₂',27)+mol([(92,253,'N'),(55,215,'H'),(55,292,'H'),(153,253,'Cl')],[(0,1),(0,2),(0,3)])+text(255,246,'NH₂Cl',25)+text(255,280,'氯胺之一',19)+text(180,336,'氨水也不可與含氯劑混用',20);save(1115,3,s)
def bottle(x,label,col):return rect(x+16,75,44,33,col,C,3)+rect(x,108,76,166,'#fff',C,13)+rect(x+5,186,66,80,col,'none',5)+text(x+38,174,label,20)
s=text(180,29,'保留原印，不當作無條件安全',19)+bottle(24,'HClO','#d6e9cd')+bottle(141,'HCl','#f1d7cd')+bottle(258,'NH₃','#d2e4f0')+line(113,131,133,162,O,5)+line(113,162,133,131,O,5)+line(229,131,250,162,O,5)+line(229,162,250,131,O,5)+text(180,320,'依標示使用，不自行混合',22);save(1115,4,s)
spec(1115,'指定產物是Cl₂，酸化平衡選鹽酸',[('① 用原反應辨認左右兩側','Cl₂與水形成HCl及HClO，是可逆平衡。圖只用分子表達原子守恆；不要把反應式當成混合清潔劑的操作指示。'),('② 鹽酸促進氯氣形成','鹽酸提供H⁺及Cl⁻，可促進HClO＋H⁺＋Cl⁻形成Cl₂與水，對應原反應往左，故選B。'),('③ 氨水的風險，不能忽略','D也不能混用，可能產生氯胺。氯氣與氯胺是不同物質；題目指定Cl₂，並不表示其他選項可安全混合。')],('答案B：鹽酸',['原印「且無毒」照留，解說不作任意濃度或接觸皆安全的保證；依產品標示，不自行混用。']),['新製Cl2及水與HCl及HOCl的可逆分子示意，各側2H2Cl1O守恆。','新製HOCl、H+、Cl-與產物Cl2水的粒子示意，酸化方向明確，不含操作濃度。','新製Cl2雙原子分子與NH2Cl氯胺分子，N三鍵連兩H一Cl。','新製三瓶分開直立的含氯劑/鹽酸/氨水及不混合符號，為使用風險整合圖。'],'四張為守恆分子、平衡促進、氯氣/氯胺結構、分開儲用容器，非純文字框。原題無毒語句限制及原AI未釐清處另review交root。',['HClO','Cl₂','H⁺','Cl⁻','氯胺'],[{'url':'https://doh.wa.gov/community-and-environment/contaminants/bleach-mixing-dangers','finding':'含氯漂白劑與酸產氯氣，與氨可產氯胺，兩者都不可混用。'},{'url':'https://www.cdc.gov/niosh/ershdb/emergencyresponsecard_29750024.html','finding':'氯氣在水中形成鹽酸及次氯酸並有危害。'}])
# q1116: real solutions, ester structure, ionic lattice, qualitative acid/base scale.
s=text(180,27,'按題目主要成分比較',24)
for x,lab in [(15,'NaCl'),(132,'C₂H₅OH'),(249,'CH₃COOH')]:s+=beaker(x,91,96,165)+text(x+48,71,lab,18)
for x,y,lab in [(39,151,'＋'),(87,184,'－'),(46,222,'－'),(88,234,'＋')]:s+=circle(x,y,15,'#a5cad4')+text(x,y+6,lab,18)
s+=ethanol(171,171,.28,True)+ethanol(181,227,.28,True)+text(297,155,'HA',22)+text(279,207,'H⁺',18)+text(317,232,'A⁻',18)
s+=text(63,297,'近中性',20)+text(180,297,'近中性',20)+text(297,297,'酸性',20)+text(180,336,'HA代表乙酸；不是實測pH',17);save(1116,1,s)
s=text(180,25,'生成乙酸乙酯，不是乙醇乙酯',19)
s+=text(35,125,'CH₃',22)+text(103,125,'C',25)+text(103,69,'O',25)+text(157,125,'OH',22)+line(59,118,89,118)+line(119,118,138,118)+line(99,78,99,104)+line(108,78,108,104)
s+=text(203,125,'＋',24)+text(282,125,'HO－C₂H₅',21)+arrow(180,165,180,194,gold)+text(180,153,'酸催化等條件',16)
s+=text(31,284,'CH₃',21)+text(94,284,'C',24)+text(94,231,'O',24)+line(56,277,80,277)+line(90,239,90,262)+line(99,239,99,262)+text(148,284,'O',24)+line(109,277,132,277)+text(224,284,'C₂H₅',24)+line(164,277,190,277)+text(288,284,'＋H₂O',21)+text(180,332,'乙酸＋乙醇 ⇌ 酯＋水',22);save(1116,2,s)
s=text(180,28,'NaCl離子晶體：熔點較高',22)
for i,j in itertools.product(range(4),repeat=2):
 x=62+i*42;y=77+j*42;sg='＋' if (i+j)%2==0 else '－';s+=circle(x,y,18,'#a8cbd8' if sg=='＋' else '#d8e8bb',C,1)+text(x,y+6,sg,19)
s+=text(132,280,'離子間強作用力',20)+path('M260 92V235Q239 265 260 282Q282 295 293 276Q313 250 290 235V92Z',C,4,'#f1d9ba')+rect(265,141,20,110,O,'none',2)+text(278,326,'相對較高',18);save(1116,3,s)
s=text(180,29,'主要成分的定性酸鹼圖',22)+rect(24,195,108,30,'#f1d6ba','none',0)+rect(132,195,96,30,'#d6e8c8','none',0)+rect(228,195,108,30,'#d3e3ef','none',0)
s+=text(70,265,'酸性',23)+text(180,265,'中性附近',21)+text(288,265,'鹼性',23)+arrow(74,135,74,190,O)+arrow(180,104,180,190,blue)+text(74,109,'乙酸',23)+text(180,80,'NaCl／乙醇',22)+text(180,328,'依題目簡化，不保證酒類pH＝7',18);save(1116,4,s)
spec(1116,'先按主要成分判酸鹼，再逐字看酯名',[('① 主要成分的三種水溶液','依題目簡化，NaCl與乙醇水溶液近中性，乙酸水溶液呈酸性，所以預期C。實際酒類另有成分，不能保證所有米酒的pH恰為7。'),('② A的反應物對，產物名稱錯','乙酸與乙醇可在適當條件下酯化，生成乙酸乙酯及水。原選項「乙醇乙酯」照留，不能因前半句合理就忽略錯名。'),('③ NaCl熔點高，也有大量可移動離子','B誤說NaCl熔點最低。NaCl水中充分解離，常見同濃度下導電性優於部分解離的乙酸，D說食醋最佳也不合。')],('答案C：前兩者近中性，乙酸酸性',['按所列主要成分判讀；酯化產物要逐字看，不能把乙酸乙酯寫成乙醇乙酯。']),['新製三個溶液容器，NaCl離子、乙醇分子、乙酸HA及少量離子示意，不畫成實測濃度。','新製酯化結構式，乙酸羰基保留，乙氧基連到酸側形成乙酸乙酯及水。','新製NaCl正負離子晶體與相對高熔點溫度計，未杜撰數值。','新製定性酸中鹼位置圖，乙酸在酸性、NaCl及乙醇在近中性，非實測市售米酒pH。'],'四張分別描繪溶液粒子、酯化分子結構、離子晶體、定性酸鹼關係，不以文字框替代物質。',['NaCl','C₂H₅OH','CH₃COOH','乙酸乙酯','乙醇乙酯'])
# q1117: technical ear-thermometer device and energy path, not a medical/anatomy chart.
def device(x,y,k=1):
 return f'<g transform="translate({x} {y}) scale({k})">'+path('M0 30L35 0H78L98 33L128 115Q134 138 116 148H83L54 80H23Z',C,4,'#d5e2e7')+rect(68,55,37,45,'#a9c9b4',C,4)+rect(7,14,28,26,'#eef3f4',C,2)+circle(102,121,9,'#d79a75',C,1)+'</g>'
s=text(180,29,'耳溫槍：接收紅外線',23)+device(105,85,1.2)+arrow(40,133,110,112,gold)+text(58,176,'探測端',21)+line(205,189,294,189,blue,3)+text(286,225,'顯示端',21)+text(180,332,'不是向耳膜發射測溫光束',20);save(1117,1,s)
s=text(180,28,'耳道剖面與輻射方向',24)
s+=path('M45 94Q128 54 233 85L289 123L275 255Q215 282 160 251Q102 221 48 249L48 208Q96 184 153 208Q210 232 245 220L255 147Q206 109 145 119Q91 128 45 145Z','#ad8c7f',4,'#e9c9b4')
s+=line(255,147,245,220,O,8)+rect(25,150,75,45,'#d4e3e9',C,8)+rect(91,156,13,33,'#f4eee2',C,2)
for y in [155,180,204]:s+=wave(237,y,111,177,gold)
s+=text(287,106,'耳膜',21)+text(63,283,'探頭',22)+text(180,327,'探頭在入口，與耳膜不接觸',19);save(1117,2,s)
s=text(180,28,'輻射→感測元件→電訊號',22)+rect(150,87,76,104,'#a9c6d2',C,7)
for x in [160,181,202,219]:s+=line(x,194,x,222,C,4)
for y in [105,139,173]:s+=wave(35,y,143,y,gold)
s+=text(84,65,'紅外線',21)+text(189,65,'感測器',21)+line(181,221,181,261,blue,4)+line(181,261,270,261,blue,4)+rect(252,237,77,53,'#c3d6c1',C,5)+text(291,272,'讀值',21)+text(180,328,'功能示意，非實際電路設計',18);save(1117,3,s)
s=text(180,29,'B的能量路徑最符合',24)+path('M36 104Q57 71 93 104Q106 137 91 170Q61 193 39 163Z','#b48777',4,'#e5c3b1')+text(64,213,'耳部',22)+device(226,102,.7)
for y in [111,140,167]:s+=wave(108,y,227,y,gold)
s+=text(170,244,'熱輻射跨越間隙',22)+text(180,330,'發出：耳部｜接收：耳溫槍',20);save(1117,4,s)
spec(1117,'耳膜發出紅外線，耳溫槍接收',[('① 先認探測端的紅外線元件','耳溫槍用紅外線感測器讀取耳部熱輻射；不是把測溫光束打到耳膜，再等待反射回來。'),('② 看清能量由哪裡傳向哪裡','耳膜與耳道組織發出紅外線，傳至探頭。示意探頭位於耳道入口附近，與耳膜有間距，不畫成接觸耳膜。'),('③ 感測訊號換算成溫度','主要依接收到的紅外線產生訊號，再換算讀值。A、D的空氣對流及C的空氣傳導，不是題目這種元件的主要原理。')],('答案B：耳膜以輻射傳給耳溫槍',['辨認發出端、接收端與紅外線線索；不需等空氣傳熱到探頭。']),['新製通用耳溫槍裝置，探頭/感測端與顯示端分明，沒有虛構溫度讀數。','新製局部耳道剖面，耳膜斜面深處、探頭在入口且不相觸，波箭頭由耳膜往探頭。','新製紅外線到感測晶片封裝再經導線到讀值顯示的功能示意，未冒充真實電路。','新製耳部放射與外側接收裝置間的電磁波能量路徑整合，箭頭由耳部出發。'],'此題教學重點為測溫裝置與能量路徑，採精確裝置/局部剖面/感測器功能/完整方向四張原生圖；非生物解剖鑑別題，不用人物漫畫或醫療操作深度數值。',['耳溫槍','紅外線','熱輻射','感測器'],[{'url':'https://www.accessdata.fda.gov/cdrh_docs/pdf18/K180387.pdf','finding':'耳溫槍讀取耳膜組織發出的紅外線，感測器接收後電路換算讀值。'}])
# q1118: two separate bodies, latent heat and qualitative temperature curves.
s=text(83,29,'乙：0°C',22)+text(275,29,'甲：25°C',21)
s+=rect(37,100,287,214,'#e2e6e7',C,5)+rect(51,164,259,137,'#b4dbe9','none',0)
s+=path('M140 69V264Q140 284 175 284Q210 284 210 264V69',C,4,'#edf6fa')
for x,y in [(157,226),(186,235),(166,258)]:s+=f'<rect x="{x-9}" y="{y-9}" width="18" height="18" transform="rotate(17 {x} {y})" fill="#fff" stroke="{blue}" stroke-width="2"/>'
for x,Y in [(175,230),(271,259)]:s+=line(x,49,x,Y,O,5)+circle(x,Y,7,O,C,1)
s+=line(109,37,175,51,blue,2)+line(276,37,271,49,blue,2)+arrow(91,213,133,213,gold,4)+arrow(255,213,217,213,gold,4)+text(180,343,'隔著試管壁傳熱，不直接混合',19);save(1118,1,s)
s=text(180,28,'吸熱先改變狀態',25)+rect(24,82,137,195,'#daeaf2',blue,13)+beaker(201,82,137,195)
for x,y in [(64,126),(118,126),(64,204),(118,204)]:s+=water(x,y,.42)
for x,y in [(240,150),(294,195),(240,235),(302,123)]:s+=water(x,y,.42)
s+=arrow(168,178,194,178,gold,4)+text(90,311,'冰熔化：0°C',20)+text(269,311,'熔化後的水',20)+text(180,343,'熔化期間吸熱，溫度不先上升',18);save(1118,2,s)
def axes(x,y,w,h):return arrow(x,y,x+w,y,ink,3)+arrow(x,y,x,y-h,ink,3)
s=text(180,28,'C：先恆溫，後升溫同溫',22)+axes(45,281,279,216)+text(22,89,'25',20)+text(23,288,'0',20)+text(36,51,'°C',19)+text(211,332,'時間（未標數值）',19)
s+=path('M45 80Q88 174 209 183Q270 185 320 185',O,5)+path('M45 281H157Q204 281 236 235Q274 185 320 185',blue,5)+line(157,281,157,109,C,2,'5 6')+text(142,310,'熔完',18)+text(260,160,'甲',22,O)+text(239,270,'乙',22,blue)+text(312,217,'同溫',18)+text(180,355,'定性示意，未補造終溫或秒數',16);save(1118,3,s)
s=text(180,28,'B與C都同溫，差在初期',22)
for x,kind in [(24,'B'),(204,'C')]:
 s+=axes(x,258,137,155)+text(x+67,76,kind,28)+path(f'M{x} 111Q{x+28} 175 {x+128} 181',O,4)
 if kind=='B':s+=path(f'M{x} 258Q{x+40} 181 {x+128} 181',blue,4)
 else:s+=path(f'M{x} 258H{x+50}Q{x+90} 255 {x+102} 209Q{x+116} 183 {x+128} 181',blue,4)+path(f'M{x} 275H{x+50}',gold,7)
 s+=text(x+67,303,'立即升溫' if kind=='B' else '先有0°C平台',19)
s+=text(180,343,'C需按冰能全熔的命題情境判讀',17);save(1118,4,s)
spec(1118,'先恆溫熔化，再升溫至熱平衡',[('① 甲測杯水，乙測試管中的冰','甲原為25°C、乙原為0°C，兩者隔試管壁交換熱。熱由溫水傳向冰，不能把裝置誤畫成冰與杯水混在一起。'),('② 冰熔化時吸熱，仍約0°C','相變化需要吸熱，但不是立刻升溫。冰全熔成水後，再吸熱才升溫；圖為狀態比較，非分子數或時間比例。'),('③ 甲降溫，乙先平台再升溫','原卷C有熔化恆溫段，最後兩條線同溫。未給水冰質量，所以圖只表趨勢，不補造終溫、秒數，也不能保證任意冰量都全熔。')],('依原卷預期C：先熔化恆溫，最後同溫',['B其實也是最後同溫，錯在乙立即升溫；不是原AI說的乙恆0或末段異溫。C按可全熔的命題情境判讀。']),['新製絕熱杯與獨立試管，甲在杯水、乙在管內碎冰，熱箭頭經壁朝內。','新製四個水分子群的固/液狀態比較，熔化吸熱不先升溫，非精確晶格或比例。','新製C定性溫度時間曲線，甲25降、乙0平台後升，同溫未標虛構終溫秒數。','新製B/C對比兩張縮圖，兩者終點同溫但B立即上升、C有0平台；更正原AI誤讀。'],'四圖為實驗裝置、狀態粒子、C曲線、B/C起始差異，均真正物理圖。原AIA/B曲線誤讀與缺質量限制已交reviews，未改原題選項。',['25°C','0°C','試管壁','熱平衡','甲','乙'])
# q1119: actual atom counts and carbon conservation.
def propene(x,y,k=1):
 ns=[(-80,0,'C'),(0,0,'C'),(80,0,'C'),(-80,-65,'H'),(-80,65,'H'),(-135,0,'H'),(0,-65,'H'),(80,-65,'H'),(135,0,'H')];bb=[(0,1),(1,2,2),(0,3),(0,4),(0,5),(1,6),(2,7),(2,8)]
 return f'<g transform="translate({x} {y}) scale({k})">'+mol(ns,bb)+'</g>'
def ethane(x,y,k=1):
 ns=[(-31,0,'C'),(31,0,'C'),(-31,-55,'H'),(-31,55,'H'),(-86,0,'H'),(31,-55,'H'),(31,55,'H'),(86,0,'H')];bb=[(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,7)]
 return f'<g transform="translate({x} {y}) scale({k})">'+mol(ns,bb)+'</g>'
s=text(180,28,'丙烯：CH₃－CH＝CH₂',23)+propene(180,182,1)+text(180,324,'3個碳、6個氫；有C＝C',22);save(1119,1,s)
s=text(180,27,'烴只含碳與氫',26)+propene(180,113,.65)+text(180,185,'丙烯：烴',23)+ethanol(163,267,.8,True)+text(180,341,'乙醇另含氧，不是烴',21);save(1119,2,s)
s=text(180,28,'完全燃燒的產物種類相同',22)+text(89,86,'C₃H₆',25)+text(265,86,'CH₃COOH',23)+arrow(88,110,88,157,gold)+arrow(268,110,268,157,gold)+text(180,187,'氧充足、完全燃燒',20)
s+=co2(104,253,.8)+water(267,237,.8)+text(102,315,'CO₂',25)+text(267,315,'H₂O',25)+text(180,348,'相同種類 ≠ 相同產量',20);save(1119,3,s)
s=text(180,27,'只追蹤碳：每1mol反應物',21)+propene(54,113,.26)+text(54,157,'C₃H₆',20)+arrow(102,113,130,113,gold,4)
for x in [160,233,306]:s+=co2(x,113,.45)
s+=text(232,162,'3mol CO₂',21)+ethane(53,239,.33)+text(53,281,'C₂H₆',20)+arrow(102,239,130,239,gold,4)
for x in [179,279]:s+=co2(x,239,.55)
s+=text(231,286,'2mol CO₂',21)+text(180,333,'同種CO₂質量比＝3：2',23)+text(180,356,'只數CO₂；O₂與H₂O省略',15);save(1119,4,s)
spec(1119,'先看組成，再分清產物種類與數量',[('① 丙烯只含碳氫，具有雙鍵','C₃H₆可寫成CH₃－CH＝CH₂。圖逐一核對3碳6氫、碳四價；丙烯是烴類，但不是所有有機物都是烴。'),('② A把乙醇也當烴，錯在有氧','乙醇含O，不能列入只含C、H的烴類。B也錯：丙烯與甲烷在水中溶解度低，不能說易溶。'),('③ 完全燃燒，產物都是CO₂和水','丙烯及乙酸在氧充足、完全燃燒下，產物種類都為CO₂與H₂O，因此C成立。產物種類相同，不等於產物數量相同。')],('答案C；D的CO₂質量比應為3：2',['每1mol丙烯、乙烷各含3mol與2mol碳，形成同種CO₂的量比及質量比均3：2，不是1：1。']),['新製丙烯完整3C6H結構，單雙鍵及每個H均可核。','新製丙烯與乙醇兩種分子作組成比較，紅氧原子明確表示乙醇非烴。','新製兩原料完全燃燒通往CO2與水分子，只比較產物種類，未把種類當產量。','新製每1mol丙烯3molCO2、每1mol乙烷2molCO2的碳追蹤分子圖，明示省略O2/H2O非完整反應式。'],'四張分別是丙烯結構、烴/非烴比較、產物分子、碳數追蹤；化學式與莫耳比逐一核對，不用純文字反應框代替圖像。',['3mol','2mol','3碳','6氫','CH₃COOH','C₃H₆','CH₃－CH＝CH₂','C₂H₆','CO₂','H₂O','1mol','3：2'],[{'url':'https://pubchem.ncbi.nlm.nih.gov/compound/Propylene','finding':'丙烯為H2C=CHCH3，水中溶解度低。'}])
# q1120: true70:30 composition, PP repeat unit, heat-softening rod, material-to-product integration.
def husk(x,y,k=1):return f'<g transform="translate({x} {y}) scale({k})">'+path('M0 -25Q30 -10 0 28Q-30 9 0 -25Z','#a2824f',2,'#dcc28b')+path('M0 -21Q7 0 0 24','#a2824f',2)+'</g>'
a=-math.pi/2+2*math.pi*.7;X,Y=180+107*math.cos(a),180+107*math.sin(a)
s=text(180,28,'依文章：70%稻殼＋30%PP',22)+circle(180,181,107,'#a8c5d5',C,3)+path(f'M180 181L180 74A107 107 0 1 1 {X:.2f} {Y+1:.2f}Z',C,2,'#ddc18b')+text(213,216,'70%',31)+text(127,133,'30%',27)
s+=husk(82,312,.65)+text(150,323,'稻殼',21)+circle(252,311,13,'#a8c5d5',C,2)+text(302,323,'PP',22);save(1120,1,s)
s=text(180,28,'聚丙烯：重複單元連長鏈',22)+text(106,152,'CH₂',33)+text(229,152,'CH',33)+line(27,143,68,143)+line(145,143,199,143)+line(262,143,326,143)+line(230,169,230,216)+text(230,249,'CH₃',33)+path('M61 91H47V276H61',blue,4)+path('M292 91H306V276H292',blue,4)+text(324,288,'n',25)+text(112,232,'甲基側基',20)+arrow(147,234,189,234,gold,3)+text(180,333,'主鏈延伸，側基不是網狀交聯',19);save(1120,2,s)
s=text(180,29,'熱塑性：受熱可能軟化變形',21)+path('M42 87H317V111H42Z',C,3,'#adc3ce')+text(180,153,'原形狀',23)+arrow(180,176,180,207,gold)+path('M42 245Q120 235 174 257Q220 280 312 273V296Q214 303 166 279Q117 259 42 269Z',C,3,'#adc3ce')+text(180,335,'高溫使用須依製品耐熱標示',20);save(1120,3,s)
s=text(180,28,'農業副產物＋塑膠→複合筷',21)
for x,y,k in [(53,88,.65),(90,103,.7),(67,137,.65)]:s+=husk(x,y,k)
for x,y in [(255,92),(286,126),(311,88)]:s+=circle(x,y,13,'#a8c5d5',C,2)
s+=text(71,180,'稻殼70%',20)+text(285,180,'PP30%',20)+arrow(92,192,147,225,gold,4)+arrow(263,192,215,225,gold,4)
s+=path('M125 245L137 245L234 315L226 324Z',C,3,'#baa789')+path('M150 236L162 236L255 307L248 317Z',C,3,'#baa789')+text(180,350,'含PP，不等於整支可完全分解',18);save(1120,4,s)
spec(1120,'主要原料看70%，聚合物看長鏈',[('① 稻殼才是文章的主要原料','稻殼占70%，食品級聚丙烯PP占30%。A把主要原料說成生物完全無法分解，忽略稻殼的植物來源有機成分。'),('② PP的重複單元接成主鏈','PP可表示為［－CH₂－CH（CH₃）－］ₙ。CH₃是甲基側基，主鏈仍延伸，屬鏈狀聚合物，選B；有側基不等於網狀交聯。'),('③ 熱塑性不等於任意高溫可用','PP受熱可能軟化變形，C不能不看製品耐熱規格就說可直接高溫使用。D也不合原文：取得稻殼不需為此砍伐樹木。')],('答案B：聚丙烯屬鏈狀聚合物',['稻殼可再利用，但含PP的整支複合筷，不等於可以快速完全生物分解；實際回收亦須看製品條件。']),['新製70:30精確圓餅面積圖，配稻殼形狀及PP顆粒圖例，數值完全來自原文。','新製PP單一重複單元結構及n括號，CH2/CH主鏈、CH3側基鍵數正確。','新製同一塑膠棒受熱前直形、受熱後彎形的裝置材料比較，未杜撰耐熱數值。','新製稻殼與PP顆粒結合為兩支複合筷的物質來源整合，不宣稱整支可完全分解。'],'四張以精確組成圖、化學重複結構、受熱形變、原料到實物筷子整合教學；不是四個文字流程框，也不延伸為產品安全或回收承諾。',['PP','CH（CH₃）','70%','30%','聚丙烯','CH₃','CH₂','甲基側基','鏈狀聚合物'])
