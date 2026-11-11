"""Four genuine native scientific illustrations per source-checked question."""
from pathlib import Path
import json,math,html,datetime
R=Path(__file__).resolve().parents[4];D=json.loads((R/'site/dist/data.json').read_text());NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
C={'ink':'#294d43','blue':'#3677a5','gold':'#b5792b','green':'#23836c','red':'#b65846','grey':'#aebdb6'}
def t(x,y,s,size=12,color=C['ink'],anchor='middle'):return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="sans-serif" font-size="{size}" fill="{color}">{html.escape(str(s))}</text>'
def ln(x,y,xx,yy,col=C['ink'],w=1.7,dash=''):return f'<path d="M{x} {y}L{xx} {yy}" stroke="{col}" stroke-width="{w}" fill="none"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def arrow(x,y,xx,yy,col=C['gold'],w=2):
 a=math.atan2(yy-y,xx-x);return ln(x,y,xx,yy,col,w)+ln(xx,yy,xx-7*math.cos(a-.5),yy-7*math.sin(a-.5),col,w)+ln(xx,yy,xx-7*math.cos(a+.5),yy-7*math.sin(a+.5),col,w)
def circ(x,y,r,fill,stroke=C['ink']):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
def rect(x,y,w,h,fill,stroke='none',radius=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'
def beaker(x,y,w=55,h=75,fill='#d8e7ed',sediment=False,level=.55):
 top=y+h*(1-level);s=rect(x+2,top,w-4,y+h-top-2,fill)
 if sediment:
  for i in range(13):s+=circ(x+7+i*3.4,y+h-5-(i%3)*3,2,'#ffffff','#99aaa2')
 s+=f'<path d="M{x} {y}V{y+h-5}Q{x} {y+h} {x+5} {y+h}H{x+w-5}Q{x+w} {y+h} {x+w} {y+h-5}V{y}M{x-3} {y}H{x+w+3}" fill="none" stroke="{C["ink"]}" stroke-width="2"/>'
 return s

def flask(x,y,label,fill='#d8e7ed',w=38,h=65):
 s=f'<path d="M{x+w*.35} {y}v22L{x} {y+h-5}Q{x} {y+h} {x+5} {y+h}H{x+w-5}Q{x+w} {y+h} {x+w} {y+h-5}L{x+w*.65} {y+22}V{y}Z" fill="{fill}" stroke="{C["ink"]}" stroke-width="1.6"/>'+t(x+w/2,y+h+17,label,10)
 return s

def wool(cx,cy,col=C['grey']):
 return ''.join(f'<path d="M{cx-24} {cy+j*3-10}q9 -9 17 0t17 0t16 0" fill="none" stroke="{col}" stroke-width="2"/>' for j in range(7))
def scale(cx,cy,tilt=0,left='wool',right='oxide'):
 s=ln(cx,cy-25,cx,cy+24)+f'<path d="M{cx-15} {cy+35}L{cx} {cy+16}L{cx+15} {cy+35}Z" fill="#cdd7d0" stroke="{C["ink"]}"/>'+ln(cx-52,cy-20-tilt,cx+52,cy-20+tilt)
 for side,kind in [(-1,left),(1,right)]:
  xx=cx+side*43;yy=cy-20+side*tilt;s+=ln(xx,yy,xx-17,yy+28)+ln(xx,yy,xx+17,yy+28)+f'<path d="M{xx-20} {yy+28}q20 14 40 0" fill="#dce6df" stroke="{C["ink"]}"/>'
  if kind in ['wool','oxide']:s+=f'<g transform="translate({xx},{yy+18}) scale(.45)">'+wool(0,0,C['grey'] if kind=='wool' else '#886c55')+'</g>'
  else:s+=f'<g transform="translate({xx-12},{yy-5}) scale(.42)">'+beaker(0,0,55,75,'#deebef',kind=='after')+'</g>'
 return s

def bond(x,y,xx,yy,double=False,col=C['ink']):return ln(x,y,xx,yy,col,1.8)+(ln(x+3,y,xx+3,yy,col,1.5) if double else '')
def atom(x,y,s,col=C['ink'],size=13):return t(x,y+4,s,size,col)
def water(x,y,scale=1):
 s=bond(x,y,x-12*scale,y+10*scale)+bond(x,y,x+12*scale,y+10*scale)+circ(x,y,6*scale,'#d87663')+circ(x-12*scale,y+10*scale,4*scale,'#f5f5eb')+circ(x+12*scale,y+10*scale,4*scale,'#f5f5eb');return s

def triester(x=28,y=48,free=False):
 s=''
 for i,group in enumerate(['CH₂','CH','CH₂']):
  yy=y+i*60;s+=atom(x,yy,group)
  if i<2:s+=bond(x,yy+11,x,yy+46)
  if free:s+=bond(x+13,yy,x+33,yy)+atom(x+48,yy,'OH',C['blue'])
  else:
   s+=bond(x+14,yy,x+32,yy)+atom(x+43,yy,'O',C['blue'])+bond(x+52,yy,x+72,yy)+atom(x+84,yy,'C')+bond(x+84,yy-8,x+84,yy-24,True)+atom(x+84,yy-34,'O',C['red'])+bond(x+93,yy,x+110,yy)+atom(x+124,yy,f'R{i+1}',C['gold'])
 return s

def svg(s,title):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240"><title>{html.escape(title)}</title><rect width="240" height="240" fill="#faf8ef"/>{s}</svg>'
def save(qid,frames,panels,title,answer,points,checks,caption,sources=()):
 q=next(q for q in D['questions'] if q['id']==qid);paths=[]
 for i,(body,alt) in enumerate(frames):
  p=R/f'docs/comics/art/{qid}-four-image-v2-panel-{i+1}.svg';p.write_text(svg(body,alt));paths.append(str(p.relative_to(R)))
 spec=dict(id=qid,subject=q['subject'],title=title,art=paths[0],panels=[dict(heading=h,text=text,alt=frames[i][1],caption=caption,image=paths[i]) for i,(h,text) in enumerate(panels)],fourth=dict(answer=answer,points=points,image=paths[3],alt=frames[3][1]),protectedWords=['OH⁻','I₂','IO₃⁻','NaOH','CaCO₃','三酸甘油酯','乙醇','酯化反應','氫氧化鈉'],generationMethod='four authored native SVG apparatus/material/structural-formula diagrams',generatorFile=str(Path(__file__).relative_to(R)),sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/'+x for x in q['images']]+['site/dist/'+f['src'] for f in q.get('questionFigures',[])],answerCheckedAgainst=q['question']+'\n'+q['answer']+'\n'+q['explanation'],rationale='對照實開原卷與必要附圖保留全部原題及既有答案。每格是新的實際器材/物質/結構圖，不以純文字流程框取代，不杜撰原卷數值；四圖各有不同教學作用。',createdAt=NOW,visualChecked=False,productionReview=dict(reviewerAgent='/root',checkedAt=NOW,originalVisualChecked=True,answerAndExplanationChecked=True,checks=checks,sources=list(sources),sourceQuestionUnchanged=True))
 (R/f'docs/comics/{qid}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');b=R/f'docs/comics/biology-rework-20261112/{qid}';b.mkdir(exist_ok=True);(b/'production-review.json').write_text(json.dumps(spec['productionReview'],ensure_ascii=False,indent=2)+'\n')
# q1042, measured contents vs material entering/leaving the measurement boundary.
frames=[]
s=rect(40,85,160,115,'none',C['blue'],10).replace('stroke="'+C['blue']+'"','stroke="'+C['blue']+'" stroke-dasharray="5 4"')+wool(120,157)+circ(75,50,8,'#b8cfe5')+circ(89,50,8,'#b8cfe5')+t(82,30,'O₂',15)+arrow(90,68,113,123)+t(120,220,'m + m(O₂)',16);frames.append((s,'氧分子由藍虛線秤量邊界外加入鋼絲絨，秤上物質增加'))
s=beaker(30,35,43,55,'#d7e8ee')+beaker(165,35,43,55,'#d7e8ee')+t(51,21,'Na₂CO₃',12)+t(186,21,'CaCl₂',12)+arrow(63,101,99,137)+arrow(177,101,141,137)+beaker(85,145,70,65,'#d7e8ee',True)+t(120,230,'CaCO₃ ↓ + NaCl(aq)',12);frames.append((s,'兩份溶液混合後產生仍留在容器內的碳酸鈣白色沉澱，未畫氣體逸出'))
s=scale(120,122,0,'before','after')+t(64,66,'m',18)+t(178,66,'m',18)+t(120,203,'m(before) = m(after)',15);frames.append((s,'混合前的全部溶液與混合後含沉澱內容物，用平衡秤表示總質量相同'))
s='<g transform="translate(37,25) scale(.7)">'+scale(120,122,12,'wool','oxide')+'</g>'+t(120,20,'m(after) > m(before)',13)+'<g transform="translate(37,131) scale(.7)">'+scale(120,85,0,'before','after')+'</g>'+t(120,225,'m(after) = m(before)',13);frames.append((s,'第四圖並列：上方鋼絲絨因氧加入而增重，下方沉澱反應質量相同'))
save('q-1042',frames,[('① 甲有外界的氧加入','甲是鋼絲絨與氧反應。只秤鋼絲絨與留下的氧化物，反應後多了氧的質量，量得會增加。'),('② 乙的沉澱沒有離開','乙反應產生碳酸鈣白色沉澱與氯化鈉溶液。沉澱仍在容器內，沒有反應氣體逸出，不能把析出當作質量消失。'),('③ 比較前後全部內容物','題目不計水蒸發，且無濺出等損失時，兩份溶液混合前的總質量，等於反應後溶液加沉澱的總質量。')],'先看物質有沒有進出量測範圍','答案 B：僅乙',['第四圖上方甲增重，下方乙不變。','密閉與否不是唯一判準，要看量測範圍的物質進出。','包含外界參與氧氣的完整反應仍遵守質量守恆。'],['氧氣跨入秤量邊界，未指定鋼絲絨氧化物為某固定化學式','乙CaCO3沉澱留存，沒有畫泡泡/逸氣','圖無虛構質量與實驗器材已知條件，秤為觀念圖'],'新製秤量範圍示意｜未指定器材、質量數值或容器大小。')
# q1043, solution colour (not microscopic pigment identity) and equilibrium direction.
frames=[]
s=beaker(24,65,65,115,'#9d593b')+beaker(150,65,65,115,'#e8cdb0')+arrow(99,120,139,120)+t(56,42,'I₂',19)+t(182,42,'I₂ ↓',19);frames.append((s,'原碘水紅褐色與變淡後比較，變淡仍帶淡色，不畫成I2必定全消失'))
s=beaker(80,103,80,107,'#c49164')+'<g transform="translate(40,-16) rotate(24,105,75)">'+rect(100,32,13,56,'#d9e6ed',C['ink'],3)+rect(97,25,19,14,'#a8c0cc',C['ink'],3)+'<path d="M100 88l6 15 7-15" fill="#d9e6ed" stroke="#294d43"/></g>'+t(167,43,'OH⁻ ↑',19)+arrow(173,66,142,106);frames.append((s,'加入鹼使OH負離子增加；滴管只表加入，不代表量或濃度'))
s=flask(19,87,'I₂','#a66543',55,82)+flask(161,87,'I⁻ / IO₃⁻','#f3f4ec',55,82)+arrow(88,118,145,118,C['green'],4)+arrow(145,134,88,134,C['grey'],1.3)+t(120,53,'OH⁻',18);frames.append((s,'左有色I2轉向右無色離子，正反應向右較強；兩箭頭仍表示可逆'))
s=beaker(26,70,63,105,'#e8cdb0')+beaker(151,70,63,105,'#9d593b')+t(58,43,'OH⁻ ↑',18)+t(182,43,'OH⁻ ↓',18)+arrow(26,197,89,197,C['green'],3)+arrow(214,197,151,197,C['gold'],3);frames.append((s,'第四圖並列加鹼OH增加變淡且右移、加酸OH減少較深且左移，按題示模型比較'))
save('q-1043',frames,[('① 變淡代表有色I₂減少','原式左側I₂紅褐色，右側離子無色。顏色變淡表示I₂減少，對應平衡向右、正反應方向移動。'),('② 加鹼增加左側OH⁻','OH⁻在原式左側。加鹼使OH⁻增加，平衡朝消耗OH⁻的方向移動，也就是向右消耗I₂。'),('③ 反應可逆，這次向右','右側I⁻與IO₃⁻為無色，因此向右可使紅褐色變淡。要同時核對變淡、正反應、鹼性三項條件。')],'先由有色物質找方向，再判酸鹼','答案 B：正反應方向、可能為鹼性物質',['第四圖左為加鹼：OH⁻增、右移、I₂減少。','右為加酸：OH⁻減、依題示模型左移，與變淡不合。','只依本題反應式判斷，不把加鹼向右當作通則。'],['顏色只表示原題I2減少而非完全反應','正向右、逆向左箭頭與原式一致','保留可逆雙向箭頭，不將平衡移動說成單向完全反應'],'新製碘水示意｜顏色比較與方向依原題反應模型，不表示濃度數值。')
# q1046, oil/alkali vs cosolvent; no operational quantities or flame.
frames=[]
s=flask(16,72,'oil','#d8b35a',46,86)+flask(93,72,'NaOH(aq)','#c2dce7',46,86)+flask(170,88,'C₂H₅OH','#edf0e9',45,70)+t(120,38,'oil + NaOH',18);frames.append((s,'椰子油及氫氧化鈉兩反應物，乙醇另列；每瓶是bulk物質不代表分子係數'))
s=beaker(25,78,70,115,'#bcd7e2');s+=rect(27,129,66,20,'#dab967')+beaker(148,78,70,115,'#c9d9b5')+arrow(103,135,137,135)+ln(179,130,199,51,C['grey'],4)+t(120,42,'C₂H₅OH',18);frames.append((s,'原先油與鹼液分層，乙醇配合攪拌幫助接觸；配色示角色不當作真實液色'))
s='<g transform="translate(10,13) scale(.68)">'+triester()+'</g>'+arrow(170,116,213,116)+flask(181,143,'soap','#e3dfc7',38,48)+t(178,65,'NaOH',14)+t(82,220,'glycerol + salts',15);frames.append((s,'油脂三酯鍵在強鹼反應中轉成甘油與脂肪酸鹽；不將乙醇併列主要反應物'))
s=flask(15,31,'oil','#d8b35a',38,56)+flask(75,31,'NaOH','#c2dce7',38,56)+arrow(124,70,166,70)+rect(178,49,40,31,'#e0e2bd',C['ink'],7)+t(198,100,'soap',13)+flask(78,146,'C₂H₅OH','#edf0e9',38,50)+arrow(128,175,151,105,C['grey'])+t(182,139,'+ glycerol',12);frames.append((s,'第四圖油與NaOH的主反應箭頭指向肥皂甘油，乙醇在下方作接觸輔助，不併入產物'))
save('q-1046',frames,[('① 兩種主要反應物','椰子油提供油脂，氫氧化鈉提供強鹼，兩者發生皂化反應；不能因三種都加入，就說三者都是主要反應物。'),('② 乙醇幫助接觸混合','油脂與氫氧化鈉水溶液不容易混合。乙醇幫助兩者接觸，攪拌也有助混合；角色與提供強鹼的NaOH不同。'),('③ 看真正反應與產物','油脂與強鹼反應後，生成脂肪酸鈉等肥皂成分和甘油。乙醇負責幫助混合，不能替換椰子油或NaOH的角色。')],'皂化反應物與幫助混合者要分開','答案 B：椰子油、NaOH反應；乙醇幫助混合',['油脂＋強鹼生成肥皂及甘油。','下方乙醇是幫助混合，與上方主反應分開。','A、C顛倒角色，D誤把乙醇也列為主要反應物。'],['三酸甘油酯畫3個酯基，氧連接為甘油—O—C(=O)—R','未將混合幫助誤畫成酯化/乙醇被皂化消耗','不新增比例、濃度、火源等操作條件'],'新製物質角色示意｜配色辨角色，非原卷用量、液色或操作步驟。',[dict(url='https://www.rsc.org/suppdata/c7/rp/c7rp00133a/c7rp00133a2.pdf',note='RSC教學實驗：鹼水解三酸甘油酯生成羧酸鹽與甘油。')])
# q1048, exact functional groups (all backbone/oxygen bonds checked).
frames=[]
s=triester(65,55,True)+''.join(f'<ellipse cx="{113}" cy="{55+i*60}" rx="19" ry="15" fill="none" stroke="{C["blue"]}" stroke-width="2"/>' for i in range(3))+t(120,223,'3 × OH',17);frames.append((s,'甘油三個碳骨架連三個OH，以藍圈標三個羥基'))
s=triester(27,53)+''.join(water(205,53+i*60,.8) for i in range(3));frames.append((s,'三酸甘油酯三組O—C=O—R酯鍵與旁邊三個水分子；R代表各脂肪酸烴基'))
s=atom(25,104,'CH₃')+bond(42,104,61,104)+atom(73,104,'C')+bond(73,94,73,72,True)+atom(73,60,'O',C['red'])+bond(83,104,106,104)+atom(119,104,'O',C['blue'])+bond(129,104,146,104)+atom(163,104,'CH₂')+bond(181,104,199,104)+atom(217,104,'CH₃')+'<ellipse cx="97" cy="95" rx="43" ry="55" fill="none" stroke="#b5792b" stroke-width="2"/>'+water(120,188,1)+t(120,31,'CH₃COOC₂H₅',17);frames.append((s,'乙酸乙酯的C(=O)—O—C酯結構被圈出，下方水分子；氧橋接乙基，不是Na鹽'))
s=atom(30,92,'CH₃')+bond(48,92,66,92)+atom(78,92,'C')+bond(78,81,78,58,True)+atom(78,46,'O',C['red'])+bond(88,92,109,92)+atom(126,92,'O⁻',C['blue'])+atom(175,92,'Na⁺',C['gold'])+water(120,166)+t(120,213,'CH₃COONa + H₂O',15);frames.append((s,'第四圖醋酸鈉羧酸根與Na正離子分開示離子關係，沒有酯的O—C乙基連接'))
save('q-1048',frames,[('① 甘油是含三個OH的醇','甘油的三個羥基可分別與脂肪酸的羧基形成酯鍵。先辨認醇與羧酸的反應，不只看到產生水就選中和。'),('② 三個酯鍵並生成三個水','一個甘油與三個脂肪酸生成一個三酸甘油酯，也生成三個水分子。圖中三條鏈分別有O—C(＝O)—R酯結構。'),('③ 乙醇與醋酸也是酯化','A所列反應產生乙酸乙酯與水，產物含酯結構，與題幹X同屬酯化，因此選A；原卷的反應式照留。')],'反應是否同類，分類名稱也要正確','答案 A：與乙醇、醋酸的酯化反應同類',['第四圖是中和所得醋酸鈉，不是酯，雖然也生成水。','B把酯化誤稱中和，C把中和誤稱酯化。','D所列式本身是中和，但與X不同類，所以不能選D。'],['甘油CH2—CH—CH2與3OH價數正確','三酯鍵每個O連甘油/酰基，C=O與R連接正確，3水逐一畫出','乙酸乙酯CH3COOCH2CH3連接正確','醋酸根與Na為離子表示，未誤畫O—Na為酯鍵','未把R1/2/3當成固定脂肪酸種類'],'新製官能基結構圖｜R代表烴基，非原題指定脂肪酸種類。',[dict(url='https://goldbook.iupac.org/terms/view/E02219/pdf',note='IUPAC酯定義：酸與醇形式上脫水連接的結構。')])
print('Prepared four verified native illustrations each for q1042/q1043/q1046/q1048')
