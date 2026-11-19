import json,hashlib,html
from pathlib import Path
from datetime import datetime,timezone
R=Path.cwd();B=R/'docs/imports/new-gpt-20261119-73/lane3';REL=str(B.relative_to(R));URL='https://chatgpt.com/share/6aff02c8-3e8c-83ec-ba50-ab1ab4a030a5'
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def t(x,y,s,size=18,color='#17334b',anchor='middle'):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{html.escape(str(s))}</text>'
def line(x,y,X,Y,color='#334155',w=3,dash=''):return f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{color}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def arr(x,y,X,Y,color='#2563eb',w=4):
 import math
 a=__import__('math').atan2(Y-y,X-x);l=11;d=0.5;p=[(X,Y),(X-l*math.cos(a-d),Y-l*math.sin(a-d)),(X-l*math.cos(a+d),Y-l*math.sin(a+d))]
 return line(x,y,X,Y,color,w)+f'<polygon points="'+ ' '.join(f'{a},{b}' for a,b in p)+f'" fill="{color}"/>'
def rect(x,y,w,h,color='#bfdbfe',stroke='#334155',rx=5):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{color}" stroke="{stroke}" stroke-width="2"/>'
def circle(x,y,r,c='#cbd5e1'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="#334155" stroke-width="2"/>'
def svg(q,p,body,title):
 path=B/f'art/{q}-panel-{p}.svg';path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400" role="img"><title>'+html.escape(title)+'</title><rect width="400" height="400" rx="18" fill="#f8fafc"/><g font-family="Noto Sans CJK TC, Noto Sans TC, sans-serif">'+body+'</g></svg>');return str(path.relative_to(R))
def axis(x=65,y=310,w=270,h=240,ylab='a',xlab='m'):
 return arr(x,y,x+w,y,'#475569',2)+arr(x,y,x,y-h,'#475569',2)+t(x-15,y+25,'0',15)+t(x+w+10,y+25,xlab,20)+t(x-15,y-h-10,ylab,20)
def curve(points,color='#2563eb',w=4):return '<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"/>'
def bookcase(x,y,full=True,scale=1):
 s=rect(x,y,100*scale,155*scale,'#c99469','#765637')
 for j in range(3):
  s+=line(x+8*scale,y+(48+j*48)*scale,x+92*scale,y+(48+j*48)*scale,'#765637',3)
  if full:
   for i,c in enumerate(['#60a5fa','#fca5a5','#86efac','#fde68a']):s+=rect(x+(12+20*i)*scale,y+(12+48*j)*scale,15*scale,32*scale,c,'#79583c',1)
 return s
# Actual question texts and teaching copies, independently checked from uploaded originals.
data=[
(1163,7,'18','固定合力下的質量與加速度關係','若實驗中施加固定的外力於不同質量的物體上，則物體獲得的加速度（a）與質量（m）的關係圖，最可能為下列何者？\n(A) 見原卷選項圖 A\n(B) 見原卷選項圖 B\n(C) 見原卷選項圖 C\n(D) 見原卷選項圖 D','A','(A) 原圖 A 的反比曲線','外力固定時，牛頓第二運動定律 F＝ma 可改寫為 a＝F／m，因此 m 增加，a 會減小，且兩者的乘積 ma 維持 F。這是反比關係，圖形在第一象限向右下彎曲，所以選 A。\n\n例如質量變成2倍，加速度變成原來的1／2；質量變成3倍，加速度變成原來的1／3。反比曲線不會在某個有限正質量處降為0。B隨質量增加而上升；C雖下降但為直線；D為正比上升直線，三者均不符。',['反比曲線，m增加時a下降且ma固定。','上彎遞增曲線，m增加時a反而增加。','向右下的直線，並非反比曲線。','通過原點的上升直線，表示正比。'],[('① 固定的是合力','同樣的合力 F 作用在不同質量上。先抓住 F 固定，再看 a 如何隨 m 改變。'),('② 質量加倍，加速度減半','由 a＝F／m 可知，質量為 m、2m、4m 時，加速度依序為 a、a／2、a／4。'),('③ 反比曲線向右下彎','質量越大，加速度越小，但不是等斜率的下降直線；每一點的 ma 都相同。')],['原圖 A 符合 a＝F／m。','下降直線 C 不能代替反比曲線。','比較前先確認題目的合力固定。']),
(1164,8,'21','書櫃推不動與最大靜摩擦力','阿忠與小志想要移動地上的書櫃，發現書櫃裝滿書時，他們無法推動書櫃，因此將裡面的書先拿下，之後就可以輕鬆推動書櫃。兩人對此現象的解釋如下：\n阿忠：由牛頓第二運動定律 F＝ma 可知，書櫃裝滿書時，質量 m 較大，因此推動書櫃所需的力 F 也較大，而造成我們推不動書櫃。\n小志：書櫃裝滿書時，書櫃垂直作用於地面的力較大，因此書櫃與地面間的最大靜摩擦力較大，而造成我們推不動書櫃。\n關於兩人的解釋是否合理？\n(A) 兩人均合理\n(B) 兩人均不合理\n(C) 只有阿忠合理\n(D) 只有小志合理','D','(D) 只有小志合理','答案D。題目比較的是書櫃能否由靜止開始滑動。裝滿書時重量較大，對地面的正向作用力較大，在相同接觸面條件下，最大靜摩擦力也較大。當推力還沒有超過這個上限，實際靜摩擦力就與推力大小相等、方向相反，書櫃維持靜止；拿下書後，上限降低，同樣的推力較容易使書櫃開始滑動，因此小志的解釋合理。\n\n阿忠把 F＝ma 的 F 直接當成推力，忽略書櫃同時受到地面摩擦力。F＝ma 中的 F 應是合力；靜止時 a＝0、合力為0，不代表推力為0。較大的質量確實會讓相同合力產生較小加速度，但這不能單獨說明為何推不動，所以阿忠的解釋不合理。',['阿忠未把推力與合力分清，不能判兩人都合理。','小志的最大靜摩擦力解釋合理，故非兩人都不合理。','阿忠忽略摩擦力，推力不等於合力。','只有小志合理，重點是開始滑動的門檻。'],[('① 同樣推力，結果不同','裝滿書時推不動，拿下書後能推動。題目在問「能否開始移動」，先比較靜摩擦的上限。'),('② 書越多，地面承受越大','滿載時重量與正向作用力較大，相同接觸面下的最大靜摩擦力也較大。'),('③ 推力未過門檻，仍靜止','靜止時推力與實際靜摩擦力平衡。不是任何推力都會產生加速度，也不是摩擦力永遠取最大值。')],['選 D：只有小志合理。','F＝ma 的 F 代表合力。','推力超過最大靜摩擦力才開始滑動。']),
(1165,9,'6','懸吊木塊的反作用力與平衡力','如右圖，天花板下方的細繩懸吊著木塊，地球吸引木塊的力為 F₁，細繩拉木塊的力為 F₂，木塊拉細繩的力為 F₃，細繩拉天花板的力為 F₄，天花板拉細繩的力為 F₅，細繩質量可忽略，試回答下列(1)～(4)題：\n(1) F₂ 的反作用力為＿＿＿＿。\n(2) F₄ 的反作用力為＿＿＿＿。\n(3) 使木塊靜止不動的兩力為＿＿＿＿。\n(4) 使細繩靜止不動的兩力為＿＿＿＿。','','(1) F₃；(2) F₅；(3) F₁、F₂；(4) F₃、F₅','(1) F₂ 是「細繩拉木塊」，把施力與受力物體互換，反作用力就是「木塊拉細繩」F₃。\n\n(2) F₄ 是「細繩拉天花板」，其反作用力為「天花板拉細繩」F₅。\n\n(3) 木塊受地球向下的引力 F₁、細繩向上的拉力 F₂；兩力作用在同一木塊上，大小相等、方向相反，使木塊靜止。它們是平衡力，不是作用力與反作用力。F₁ 的反作用力是木塊吸引地球的力，本題未另編號。\n\n(4) 把細繩單獨當受力物體，木塊在下端向下拉繩的 F₃，與天花板在上端向上拉繩的 F₅，使可忽略質量的細繩靜止。F₄ 作用在天花板上，不能放入細繩的受力平衡。\n\n辨別原則：作用力與反作用力分別作用在不同物體；要判斷平衡，則只列同一物體受到的力。',[],[('① 交換施力者與受力者','F₂ 是繩拉木塊，F₃ 是木塊拉繩，兩力分別作用在木塊與細繩上，所以是一對反作用力。'),('② 天花板與細繩也成一對','F₄ 是繩拉天花板，F₅ 是天花板拉繩。互換施力與受力物體，就找到另一力。'),('③ 木塊的平衡只看木塊','木塊受到向下 F₁ 與向上 F₂，大小相等、合力為0。這兩力不是第三定律的一對。')],['(1) F₃；(2) F₅。','(3) 木塊：F₁、F₂。','(4) 細繩：F₃、F₅；F₄不作用在繩上。']),
(1166,10,'7','兩木塊加速時的作用力大小','甲、乙兩物體在光滑水平面上，受到 F₁ 和 F₂ 的水平推力，如右圖所示，同時向右做等加速度運動，假設甲對乙的作用力為 F₃，乙對甲的作用力為 F₄，試回答下列(1)、(2)題：（圖中的力大小未依實際比例繪製）\n(1) F₁、F₂、F₃、F₄ 中，哪些力互為作用力和反作用力？\n(2) 比較 F₁、F₂、F₃、F₄ 四個力的大小關係。','','(1) F₃、F₄；(2) F₁＞F₄＝F₃＞F₂','(1) F₃ 是甲推乙，F₄ 是乙推甲；施力與受力物體互換，兩者是作用力與反作用力，因此 F₃＝F₄，但方向相反、作用在不同物體。F₁ 與 F₂ 是外界分別施加在甲、乙上的力，不能因方向相反就把它們配為第三定律的一對。\n\n(2) 向右為正。甲受到向右 F₁、向左 F₄，因甲向右加速，所以 F₁－F₄＝m甲a＞0，得 F₁＞F₄。乙受到向右 F₃、向左 F₂，因乙也向右加速，所以 F₃－F₂＝m乙a＞0，得 F₃＞F₂。再用 F₃＝F₄，合併得 F₁＞F₄＝F₃＞F₂。\n\n甲、乙的接觸力雖然相等，仍不妨礙各自受合力而向右加速；同時也不能只依原圖箭頭長短判斷，因原題已註明未按力的實際比例畫。',[],[('① 接觸處的一對力','甲推乙的 F₃ 向右，乙推甲的 F₄ 向左；兩力大小相等、作用在不同物體。'),('② 單看甲：右推大於左推','甲向右加速，水平合力必須向右，所以 F₁－F₄＞0，得到 F₁＞F₄。'),('③ 單看乙：接觸力勝過外推','乙同樣向右加速，F₃－F₂＞0，因此 F₃＞F₂。不能把等大反作用力當成合力為0。')],['一對反作用力為 F₃、F₄。','甲：F₁＞F₄；乙：F₃＞F₂。','合併 F₁＞F₄＝F₃＞F₂。']),
(1167,11,'8','太空中的火箭如何推進','太空中火箭能夠向前推進，主要的原因為何？\n(A) 噴出氣體施力於空氣，空氣給火箭反作用力\n(B) 高速氣流會減少空氣的阻力使火箭向前推進\n(C) 因為火箭受空氣的浮力作用而產生向上推力\n(D) 燃燒燃料噴出的氣體給火箭反作用力使火箭向前推進','D','(D) 燃燒燃料噴出的氣體給火箭反作用力使火箭向前推進','答案D。火箭把燃燒產生的氣體向後噴出；火箭對氣體施加向後的力，氣體同時對火箭施加大小相等、方向相反的力，使火箭向前推進。這一對力分別作用在氣體與火箭上，不會在火箭的受力圖中彼此抵銷。\n\nA把火箭推進誤認成需要推外界空氣；太空中缺乏空氣，火箭仍可靠噴出自身攜帶的推進物質獲得推力。B只談減少空氣阻力，不能說明火箭主動獲得推力。C所述空氣浮力不符合太空情境，也不是火箭的推進原理。\n\n概念查核：[NASA 牛頓第三運動定律與作用反作用力](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/newtons-third-law-action-reaction/)。',['火箭推進不需要外界空氣。','減少阻力不是產生推進力的原因。','太空中的火箭推進並非空氣浮力。','氣體對火箭的反作用力提供推力。'],[('① 火箭向後噴出氣體','噴嘴把氣體向後加速。題目說太空中，別先假設有外界空氣可推。'),('② 氣體同時向前推火箭','火箭推氣體向後，氣體推火箭向前；施力與受力物體互換，方向相反、大小相等。'),('③ 兩力不作用在同一物體','火箭的受力圖只放「氣體推火箭」；氣體受到的反向力另畫在氣體上，不拿來互抵。')],['選 D：噴出氣體給火箭反作用力。','氣體向後，火箭向前。','不靠外界空氣，也不靠浮力。']),
(1168,12,'10','推牆後的加速度與慣性','小寶穿著溜冰鞋推牆壁，如右圖所示，若小寶對著牆壁施加向左 50 kgw 的力，下列敘述何者錯誤？\n(A) 牆反推小寶 50 kgw 之力\n(B) 與牆接觸期間，小寶有一向右的加速度\n(C) 小寶的體重愈輕，產生的加速度愈大\n(D) 手離開牆後，若不計地板摩擦力，則小寶的速度愈來愈大','D','(D) 錯誤；離牆後應維持等速度','答案D。原圖中牆在小寶左側，小寶向左推牆50 kgw，牆便同時向右推小寶50 kgw，故A正確。依本題溜冰鞋、忽略水平阻力的模型，與牆接觸並持續推牆時，小寶受到向右的合力，產生向右加速度，B正確。\n\nC是在相同推牆力、相同重力加速度下比較：體重較輕表示質量較小，依 a＝F／m 得加速度較大。作用力與反作用力仍然等大，不能說較輕者受到的反作用力較大。\n\n手離開牆壁後，牆不再對小寶施加接觸推力；若不計地板摩擦力及其他水平阻力，水平合力為0、加速度為0，小寶以離牆瞬間已有的速度作等速度直線運動，不會越來越快，所以D錯誤。\n\n本題以kgw表示力，不是質量單位；不必把50 kgw誤當50 kg才能判斷。原AI解說圖曾把牆畫在右側卻標示向左推牆，與原卷左右關係矛盾，本題依真正原卷重製示意。',['第三定律：牆反推小寶的力與50 kgw推牆力等大。','接觸推牆時，牆向右的反作用力使小寶向右加速。','相同合力下質量愈小，加速度愈大。','離牆後忽略水平阻力，保持等速度，不會一直加速。'],[('① 牆在左，小寶向左推','按真正原卷定位：牆在左側，小寶站右側向左推牆，推力50 kgw。'),('② 牆反推小寶向右','接觸時，牆給小寶向右50 kgw的力，使他向右加速；反作用力仍與推牆力等大。'),('③ 離牆後，接觸推力消失','手離牆後，忽略水平阻力，水平合力為0。圖中等時間的位置間距相等，表示等速度。')],['選 D：不會速度愈來愈大。','接觸時向右加速，離牆後等速度。','原卷牆在左；新圖依此修正原AI左右錯置。'])
]
art={}
# 1163 fixed F carts / bar chart / inverse graph / compare curve and straight line
q='q-1163';body=t(200,38,'相同合力 F',24)
for j,(label,w) in enumerate([('m',65),('2m',130)]):
 y=105+j*130;body+=rect(70,y,w,55)+t(70+w/2,y+35,label,23)+circle(85,y+65,9)+circle(70+w-15,y+65,9)+arr(70+w,y+28,170+w,y+28)+t(120+w,y+13,'F',23)+line(45,y+77,355,y+77)
art[q]=[svg(q,1,body,'同樣合力推兩種質量的物體')]
body=t(200,38,'F 固定：質量增、加速度減',20)
for j,(m,a) in enumerate([('m',1),('2m',.5),('4m',.25)]):
 y=95+j*90;body+=t(50,y+20,m,20)+rect(90,y,210*a,38,'#93c5fd')+t(100+210*a,y+27,['a','a/2','a/4'][j],19,anchor='start')
body+=t(200,365,'m × a = 固定的 F',23);art[q].append(svg(q,2,body,'質量與加速度的數量比較長條圖'))
body=t(200,35,'a = F / m',25)+axis();pts=[(65+x,310-3900/x) for x in range(18,265)];body+=curve(pts)
for x in [35,70,140]:body+=circle(65+x,310-3900/x,5,'#fb923c')+line(65+x,310,65+x,310-3900/x,'#cbd5e1',1,'4 4')
art[q].append(svg(q,3,body,'正質量下的反比加速度曲線'))
body=t(200,35,'A：曲線，非下降直線',22)+axis()+curve(pts)+line(90,90,315,310,'#dc2626',3,'8 6')+t(255,88,'C：不符合',18,'#b91c1c')+t(205,360,'越靠右，下降越平緩',20)
art[q].append(svg(q,4,body,'正確反比曲線與錯誤直線的比較'))
# 1164 physics diagram bookcase full/empty, normal forces, friction threshold, push comparison
q='q-1164';body=t(200,35,'先拿下書，較容易開始滑動',21)+bookcase(45,100,True)+bookcase(250,100,False)+t(95,290,'滿載',23)+t(300,290,'空櫃',23)+arr(10,170,42,170,'#2563eb')+arr(215,170,247,170,'#2563eb')+line(20,260,380,260)+t(95,330,'推不動',20)+t(300,330,'可以推動',20)
art[q]=[svg(q,1,body,'滿載與空櫃的移動門檻比較')]
body=t(200,35,'滿載：正向力與摩擦上限較大',20)
for x,full,L in [(55,True,85),(250,False,48)]:
 body+=bookcase(x,105,full,.8)+line(x-20,233,x+100,233)+arr(x+40,215,x+40,215-L,'#16a34a')+arr(x+55,240,x+55,240+L,'#dc2626')+t(x+40,95,'N',21)+t(x+82,300 if full else 285,'W',21)
body+=t(200,375,'相同地面：最大靜摩擦力隨 N 增大',17)
art[q].append(svg(q,2,body,'滿載與空櫃的正向力和重量比較'))
body=t(200,35,'尚未滑動：兩個水平力平衡',21)+bookcase(145,92,True,1.1)+line(40,270,365,270)+arr(50,185,140,185,'#2563eb')+arr(145,244,55,244,'#ea580c')+t(65,160,'推力',20)+t(78,225,'靜摩擦力',18)+t(200,320,'推力 = 實際靜摩擦力',21)+t(200,355,'合力為 0，a = 0',22)
art[q].append(svg(q,3,body,'靜止書櫃的推力與實際靜摩擦力'))
body=t(200,35,'同樣推力能否超過門檻？',22)
for y,label,limit in [(110,'滿載',275),(245,'空櫃',150)]:
 body+=t(45,y,label,18)+line(85,y+35,345,y+35,'#cbd5e1',12)+line(85,y+35,limit,y+35,'#fb923c',12)+line(limit,y+15,limit,y+55,'#b45309',3)+arr(85,y+5,230,y+5)+t(310,y+5,'推力',17)+t((85+limit)/2,y+80,'靜摩擦上限',17,'#9a3412')
art[q].append(svg(q,4,body,'同樣推力與兩種最大靜摩擦門檻'))
# 1165 force models
q='q-1165'
def ceiling():return line(60,90,340,90,'#475569',8)+''.join(line(x,90,x+20,65,'#94a3b8',2) for x in range(65,330,25))
body=t(200,35,'繩與木塊：一對反作用力',21)+ceiling()+line(200,95,200,220,'#64748b',5)+rect(145,220,110,65)+t(200,260,'木塊',20)+arr(173,235,173,150,'#16a34a')+t(125,175,'F₂',24)+arr(225,205,225,290,'#ea580c')+t(280,205,'F₃',24)+t(200,335,'F₂：繩 → 木塊',20)+t(200,368,'F₃：木塊 → 繩',20)
art[q]=[svg(q,1,body,'細繩拉木塊與木塊拉細繩作用在不同物體')]
body=t(200,35,'天花板與繩：另一對',21)+ceiling()+line(200,95,200,270,'#64748b',5)+arr(175,95,175,175,'#ea580c')+t(125,135,'F₄',24)+arr(225,175,225,95,'#16a34a')+t(280,155,'F₅',24)+t(200,320,'F₄：繩 → 天花板',20)+t(200,355,'F₅：天花板 → 繩',20)
art[q].append(svg(q,2,body,'細繩拉天花板與天花板拉細繩'))
body=t(200,35,'只看木塊的受力',24)+rect(140,170,120,75)+t(200,215,'木塊',22)+arr(200,170,200,65,'#16a34a')+arr(200,245,200,350,'#dc2626')+t(255,110,'F₂',25)+t(255,310,'F₁',25)+t(90,375,'F₂ = F₁',23,anchor='start')
art[q].append(svg(q,3,body,'木塊向上拉力與向下引力平衡'))
body=t(200,35,'只看細繩的受力',24)+line(200,135,200,275,'#64748b',7)+arr(200,135,200,55,'#16a34a')+arr(200,275,200,355,'#ea580c')+t(265,100,'F₅',25)+t(265,325,'F₃',25)+t(100,210,'細繩',22)+t(200,385,'F₅ = F₃；不包含 F₄',20)
art[q].append(svg(q,4,body,'細繩受到天花板向上和木塊向下的拉力平衡'))
# 1166 contact blocks
q='q-1166';body=t(200,35,'接觸力：F₃ 與 F₄',24)+rect(105,160,95,80,'#fde68a')+rect(200,160,95,80)+t(150,210,'甲',25)+t(245,210,'乙',25)+line(50,245,350,245)+arr(205,130,290,130,'#2563eb')+t(255,110,'F₃',25)+arr(195,275,110,275,'#ea580c')+t(145,315,'F₄',25)+t(200,365,'大小相等，受力物體不同',20)
art[q]=[svg(q,1,body,'兩木塊相互接觸力是反作用力對')]
body=t(200,35,'甲：F₁ − F₄ > 0',25)+rect(140,150,120,90,'#fde68a')+t(200,205,'甲',28)+arr(30,180,135,180)+t(70,150,'F₁',25)+arr(260,220,185,220,'#ea580c')+t(305,225,'F₄',25)+arr(185,95,270,95,'#16a34a')+t(310,100,'a',25)+t(200,325,'甲向右加速',22)+t(200,365,'F₁ > F₄',28)
art[q].append(svg(q,2,body,'甲物體水平受力及右向加速度'))
body=t(200,35,'乙：F₃ − F₂ > 0',25)+rect(140,150,120,90)+t(200,205,'乙',28)+arr(40,180,135,180)+t(75,150,'F₃',25)+arr(340,220,265,220,'#dc2626')+t(315,255,'F₂',25)+arr(185,95,270,95,'#16a34a')+t(310,100,'a',25)+t(200,325,'乙也向右加速',22)+t(200,365,'F₃ > F₂',28)
art[q].append(svg(q,3,body,'乙物體的接觸推力大於向左外力'))
body=t(200,35,'比較大小，不表示方向',23)
for j,(lab,L,c) in enumerate([('F₁',245,'#2563eb'),('F₄',165,'#ea580c'),('F₃',165,'#16a34a'),('F₂',85,'#dc2626')]):
 y=95+j*65;body+=t(45,y+15,lab,24)+rect(85,y-3,L,22,c,c,2)
body+=t(200,370,'F₁ > F₄ = F₃ > F₂',26)
art[q].append(svg(q,4,body,'示意長條比較四個力的大小，數值非原題給定'))
# 1167 rocket mechanics; no external air
q='q-1167'
def rocket(x=210,y=160,scale=1):
 return f'<g transform="translate({x},{y}) scale({scale})">'+rect(-60,-40,120,80,'#e2e8f0')+'<path d="M60 -40 L110 0 L60 40Z" fill="#60a5fa" stroke="#334155" stroke-width="2"/><path d="M-60 -40 L-80 -65 L-30 -40M-60 40L-80 65L-30 40" fill="#93c5fd" stroke="#334155" stroke-width="2"/>'+rect(-72,-26,12,52,'#475569')+circle(35,0,18,'#dbeafe')+'</g>'
body=t(200,35,'噴出自身攜帶的氣體',23)+rocket(230,180,.95)
for j in range(4):body+=circle(125-j*25,180+(-1)**j*15,7,'#fdba74')
body+=arr(125,260,45,260,'#ea580c')+t(120,303,'氣體向後',22)+arr(270,95,360,95,'#2563eb')+t(300,70,'火箭向前',21)
art[q]=[svg(q,1,body,'火箭向後噴氣、向前推進的方向')]
body=t(200,35,'兩物體互相推',25)+rocket(255,155,.65)+circle(85,155,25,'#fdba74')+t(85,205,'噴出氣體',19)+arr(115,95,35,95,'#ea580c')+t(90,70,'火箭推氣體',18)+arr(220,250,300,250)+t(260,290,'氣體推火箭',18)+t(200,355,'力等大、方向相反',24)
art[q].append(svg(q,2,body,'氣體與火箭各自承受等大反向的力'))
body=t(200,35,'只畫火箭的受力',25)+rocket(190,190,.85)+arr(220,110,345,110)+t(265,85,'氣體給火箭的推力',18)+t(200,335,'另一個力在氣體上',22)+t(200,370,'不能在火箭上彼此抵銷',21)
art[q].append(svg(q,3,body,'火箭受力圖只列氣體作用在火箭的力'))
body=t(200,35,'太空中仍可推進',25)+rocket(245,205,.8)
for x,y,r in [(40,75,2),(130,110,3),(335,70,2),(65,300,3),(340,320,2)]:body+=circle(x,y,r,'#64748b')
for j in range(4):body+=arr(140-j*18,170+j*20,70-j*10,170+j*20,'#ea580c',3)
body+=arr(255,105,350,105)+t(200,340,'不需要外界空氣',23)+t(200,375,'D：氣體的反作用力',24)
art[q].append(svg(q,4,body,'真空背景下火箭靠自身噴氣推進'))
# 1168 exact left-wall mechanical diagram, body icon rather than narrative illustration
q='q-1168'
def wall():return rect(35,85,22,215,'#cbd5e1')+''.join(line(35,y,57,y-18,'#94a3b8',2) for y in range(105,300,22))
def skater(x=155,y=175):
 return circle(x,y-48,17,'#fed7aa')+rect(x-15,y-27,30,62,'#93c5fd')+line(x-15,y-16,x-65,y-6,'#475569',8)+line(x-7,y+35,x-20,y+78,'#475569',8)+line(x+10,y+35,x+35,y+72,'#475569',8)+line(x-28,y+80,x-2,y+80,'#334155',5)+line(x+23,y+75,x+48,y+75,'#334155',5)+circle(x-23,y+87,5,'#475569')+circle(x-8,y+87,5,'#475569')+circle(x+28,y+82,5,'#475569')+circle(x+43,y+82,5,'#475569')
body=t(200,35,'原卷：牆在左，人站右側',22)+wall()+skater(130,185)+line(35,300,365,300)+arr(122,140,58,140,'#ea580c')+t(220,120,'向左推牆',20)+t(230,152,'50 kgw',24)+t(200,355,'這個力作用在牆上',21)
art[q]=[svg(q,1,body,'小寶在牆右側向左推牆50kgw')]
body=t(200,35,'接觸時：牆向右推小寶',22)+wall()+skater(135,190)+line(35,300,365,300)+arr(150,150,290,150)+t(260,122,'50 kgw',24)+arr(240,240,335,240,'#16a34a')+t(325,215,'a',25)+t(200,355,'小寶獲得向右的加速度',21)
art[q].append(svg(q,2,body,'牆對小寶的右向反作用力及右向加速度'))
body=t(200,35,'手離牆後：等速度',24)+wall()+line(35,300,370,300)
for i,x in enumerate([145,225,305]):
 body+=circle(x,210,13,'#dbeafe')+rect(x-9,226,18,35,'#bfdbfe')+circle(x-7,283,5)+circle(x+8,283,5)+t(x,335,f't{i}',18)
body+=arr(140,170,195,170,'#2563eb',3)+arr(220,170,275,170,'#2563eb',3)+arr(300,170,355,170,'#2563eb',3)+t(200,375,'等時間的位置間距相等',21)
art[q].append(svg(q,3,body,'離牆後忽略阻力，等時間前進相同距離'))
body=t(200,35,'接觸加速 → 離牆等速',23)+axis(60,310,275,230,'v','t')+line(60,310,185,150,'#2563eb',4)+line(185,150,330,150,'#16a34a',4)+line(185,310,185,130,'#94a3b8',2,'5 5')+t(185,340,'離牆',19)+t(120,80,'有向右推力',17)+t(272,120,'水平合力為0',17)+t(200,380,'D 錯：離牆後不再變快',22)
art[q].append(svg(q,4,body,'速度時間圖顯示推牆時加速、離牆後等速，示意未按數值'))
acq=json.loads((R/'docs/imports/new-gpt-20261119-73/acquisition.json').read_text())
for number,index,onum,title,question,correct,answer,explanation,analyses,panels,points in data:
 q=f'q-{number}';original=f'{REL}/crops/{q}-original.png';figs=[]
 if q in ['q-1163','q-1165','q-1166','q-1168']:
  fig=f'{REL}/crops/{q}-figure.png';figs=[dict(src=fig,alt={'q-1163':'原卷A、B、C、D四個質量與加速度關係圖','q-1165':'原卷細繩懸吊木塊圖，保留手寫標記','q-1166':'原卷甲乙木塊受F₁與F₂推力、向右加速圖','q-1168':'原卷小寶在左側牆壁右方推牆圖'}[q],caption=('原卷四個選項分區裁切後依A～D順序並排，未重繪或改動曲線。' if number==1163 else '原卷必要附圖裁切，非AI重製。'))]
 row=acq['downloadedImages'][index-1]
 draft=dict(id=q,sourceId='src-more-073',subject='Physics-Chemistry',title=f'理化第{onum}題｜{title}',chapter='綜合',volume='綜合',date='2026-11-19',dateLabel='首次出題日期',addedAt='2026-11-19',question=question,answer=answer,explanation=explanation,trap='',verification='原卷逐題核對',verificationNote='已實開真正User原卷、完整題幹與全部選項或填答、必要原圖。日期取首次原提問台灣日，非考試日期；冊章無證據歸綜合。',diagram='',notes='',status='todo',starred=False,tags=['牛頓運動定律'],images=[original],sourceLabel=f'分享原卷｜第{onum}題',studentAnswer=row['userText'],contentStatus='完整原題',correctOption=correct,passage='',originalQuestionNumber=onum,optionAnalysis=[dict(label=chr(65+i),text=(question.split(f'({chr(65+i)}) ')[1].split('\n')[0] if f'({chr(65+i)}) ' in question else ''),wordClass='應選' if chr(65+i)==correct else '不選',meaning='',explanation=an) for i,an in enumerate(analyses)],tables=[],questionFigures=figs,explanationFigures=[])
 save(B/f'questions/{q}.json',draft)
 spec=dict(id=q,subject='Physics-Chemistry',title=title,art=art[q][0],panels=[dict(heading=h,text=tx,image=art[q][i],caption='新製精確力學教學示意，非原卷；原生SVG標示可核對。',alt=h+'：'+tx) for i,(h,tx) in enumerate(panels)],fourth=dict(answer=('選 D：離牆後應維持等速度' if number==1168 else answer),points=points,image=art[q][3],alt=f'第4張新製圖：{title}的整合判斷'),sourceUrl=URL,sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=[original]+[f['src'] for f in figs],answerCheckedAgainst=explanation,rationale='逐題依原卷核對受力物體、方向、圖形關係與全部選項，四張各自新製圖分別讀條件、辨關係、推導和整合，不使用原AI圖。',generationMethod='four independently authored native SVG force/graph diagrams',producerAgent='/root/comic_lane_3',visualChecked=False,layoutVersion='native-four-images-v7',createdAt=datetime.now(timezone.utc).isoformat(),protectedWords=['作用力','反作用力','靜摩擦力','牛頓第二運動定律','牛頓第三運動定律','天花板','等速度','加速度'],artSHA256=hashlib.sha256((R/art[q][0]).read_bytes()).hexdigest())
 save(B/f'specs/{q}.json',spec)
print('6 full drafts, 6 specs, 24 unique SVG diagrams written')
