from pathlib import Path
import json,math
P=Path('docs/imports/new-gpt-20261031-a/agent3-math');URL=json.loads((P/'source.json').read_text())['url']
INK='#35594f';BLUE='#639abc';GREEN='#8db787';ORANGE='#d7a85c';RED='#cb8791'
def rect(x,y,w,h,c='#e6efe4',stroke=INK,r=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" stroke="{stroke}" stroke-width="1.6"/>'
def line(x1,y1,x2,y2,c=INK,w=2,more=''):return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none" {more}/>'
def circle(x,y,r=4,c=BLUE,stroke=INK):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{stroke}" stroke-width="1.5"/>'
def arrow(x1,y1,x2,y2,c=BLUE):return line(x1,y1,x2,y2,c,3,'marker-end="url(#a)"')
def axis(x1=15,y=115,x2=165):return line(x1,y,x2,y)+''.join(line(x,y-4,x,y+4) for x in range(x1,x2+1,15))
def path(d,c=BLUE,w=3):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"/>'
def dots(n,x,y,dx=10,c=GREEN):return ''.join(circle(x+i*dx,y,3,c) for i in range(n))
def bracket(x1,x2,y,c=INK):return line(x1,y,x2,y,c)+line(x1,y,x1,y+5,c)+line(x2,y,x2,y+5,c)
arts={}
# q890 allowable a-domain uses exact endpoint sqrt(40), closed since equality admits a repeated root.
p1=axis()+line(90,37,90,145,'#b1bfb8')+rect(35,45,110,30,'#f0dfb8')
x=lambda a:90+7*a
p2=axis()+line(15,115,x(-math.sqrt(40)),115,GREEN,6)+line(x(math.sqrt(40)),115,165,115,GREEN,6)+circle(x(-math.sqrt(40)),115,4,GREEN)+circle(x(math.sqrt(40)),115,4,GREEN)+circle(x(6),115,4,RED)+line(x(6),65,x(6),108,RED,2)
xx=lambda t:22+32*t;yy=lambda v:142-15*v
curve='M'+'L'.join(f'{xx(t):.2f} {yy(2*t*t-6*t+5):.2f}' for t in [i/30*3 for i in range(31)])
p3=line(17,142,160,142)+line(22,15,22,148)+path(curve)+circle(xx(1.5),yy(.5),4,RED)
arts[890]=[p1,p2,p3]
# q892 signed integer counters do not represent negative physical lengths.
def signed(a,b):return dots(a,22,58,11,GREEN)+dots(b,22,101,11,RED)+arrow(37,120,139,120)+dots(abs(a-b),22,148,11,GREEN if a>b else RED)
arts[892]=[signed(12,1),signed(6,2),signed(3,4)]
# q894 exact numerical axes, important values stay in HTML text.
def rootline(vals,highlight=None):
 f=lambda t:90+12*t;s=axis(15,92,165)
 for t in vals:s+=circle(f(t),92,5,BLUE if t!=highlight else ORANGE)
 return s
arts[894]=[rootline([-2,3])+bracket(66,126,60,BLUE),rootline([4,-5])+bracket(30,138,60,GREEN),rootline([-6,1])+arrow(18,59,102,59,ORANGE)]
# q896 exact outer15/inner14 sample x=3; 29-unit L is an equal-area rearrangement, not the literal hole position.
arts[896]=[rect(22,22,135,135,'#c9dbc1')+rect(26.5,26.5,126,126,'#f9faf3'),rect(18,18,142.1,142.1,GREEN)+rect(27.47,27.47,132.63,132.63,'#fafbf6')+''.join(line(18+i*9.473,18,18+i*9.473,27.47,'#fff') for i in range(1,15))+''.join(line(18,27.47+i*9.473,27.47,27.47+i*9.473,'#fff') for i in range(1,14)),''.join(rect(14+i*5.25,76,5.25,23,GREEN,'#fff') for i in range(29))+bracket(14,166.25,118)]
# q898 truthful geometric sample x4 -> height13, widths3+10. All lengths positive.
def joined(high=0):
 s=rect(25,25,30,130,'#cbddea')+rect(55,25,100,130,'#dce8ca')+line(55,25,55,155,ORANGE,4)
 if high==1:s+=line(20,25,20,155,BLUE,4)
 if high==2:s+=line(25,19,155,19,ORANGE,4)+line(25,161,155,161,ORANGE,4)
 return s
arts[898]=[joined(),joined(1),joined(2)]
# q900 exact midpoint number lines.
def midline(a,b,m):
 f=lambda t:18+(t-a)/(b-a)*144;s=line(15,100,165,100)+''.join(circle(f(t),100,5,ORANGE if t==m else BLUE) for t in [a,m,b]);return s+bracket(f(a),f(m),64,BLUE)+bracket(f(m),f(b),64,BLUE)
arts[900]=[midline(-2,12,5),midline(10,26,18),midline(-2,12,5)+arrow(18,132,162,132,ORANGE)]
# q902 two ratio steps; number-line keeps both +3 and -3; parallel scaled chains show equal ratios.
arts[902]=[line(27,90,153,90)+''.join(circle(t,90,7,BLUE) for t in [27,90,153])+path('M27 63Q58 25 90 63')+path('M90 63Q121 25 153 63')+bracket(27,153,125),axis()+circle(45,115,6,ORANGE)+circle(135,115,6,ORANGE)+line(90,55,90,143,'#bcc8bf'),line(25,55,155,55)+line(25,125,155,125)+''.join(circle(t,y,5,BLUE if y==55 else GREEN) for t in [25,90,155] for y in [55,125])+''.join(arrow(t,68,t,111) for t in [25,90,155])]
# q904 six terms create five gaps; third point highlighted in position3 of6.
arts[904]=[line(15,90,165,90)+''.join(circle(15+30*i,90,6,ORANGE if i in [0,5] else '#e6efe4') for i in range(6)),''.join(rect(15+i*30,72,30,35,GREEN,'#fff') for i in range(5))+bracket(15,165,122),line(15,135,165,35,BLUE,3)+''.join(circle(15+30*i,135-20*i,5,ORANGE if i==2 else BLUE) for i in range(6))+line(75,95,75,150,ORANGE,2)]
# q906 eight inserted points plus two endpoints, paired four times;96 unit grid is12x8.
arts[906]=[line(15,110,165,110)+''.join(circle(15+i*150/9,110,5,BLUE if i in [0,9] else GREEN) for i in range(10)),''.join(circle(20+i*20,128,4,GREEN) for i in range(8))+''.join(path(f'M{20+i*20} 115Q90 {8+i*17} {160-i*20} 115',BLUE,2) for i in range(4)),''.join(rect(28+c*10,47+r*10,10,10,GREEN,'#fff') for c in range(12) for r in range(8))]
# q908 exact 7x4 topology; intersection is vertical index2, horizontal index4.
col=''.join(rect(70,15+i*38,38,38,ORANGE if i==1 else '#e6efe4') for i in range(4))
row=''.join(rect(6+i*24,80,24,24,ORANGE if i==3 else '#e6efe4') for i in range(7))
pair=''.join(rect(6+i*24,95,24,24,ORANGE if i==3 else '#e6efe4') for i in range(7))+path('M18 84Q90 15 162 84',BLUE,2)+path('M42 84Q90 42 138 84',BLUE,2)+path('M66 84Q90 65 114 84',BLUE,2)+line(90,124,90,153,ORANGE,3)
arts[908]=[col,row,pair]
copies={
890:('有實數解，先看平方是否非負',[('① 將條件化成a²≥40','判別式為a²−40。有實數解就須非負，等價於a²≥40。','平方條件與實數門檻的概念圖，精確式子在HTML。'),('② 數線兩側才符合','允許範圍為a≤−√40或a≥√40，端點可取；整數就是a≤−7或a≥7。','以精確±√40為閉端點的數線，6位於不合條件的中央區間。'),('③ 代入6，曲線沒有碰到x軸','a＝6時Δ＝−4。圖畫2x²−6x＋5，其最低值0.5仍高於x軸，沒有實根。','精確拋物線2x²−6x＋5在x軸上方，最低點(1.5,0.5)。')],'答案 D：6',['整數條件：a≤−7或a≥7。','−9、−7、8均可；6不行。','有解指本題國中範圍的實數解。']),
892:('先配乘積−12，再核對和',[('① 12與−1，和為11','用整數配對，乘積須為−12。綠點代表正1、紅點代表負1，這組留下11。','12個綠色正單位與1個紅色負單位相消，剩11正單位。'),('② 6與−2，和為4','(x＋6)(x−2)＝x²＋4x−12，所以4能作k；符號反過來也可得−4。','6個正單位與2個負單位相消，剩4正單位。'),('③ 3與−4，和為−1','全部整數配對的和是±11、±4、±1，沒有−7。這是整係數分解的範圍。','3個正單位與4個負單位相消，剩1負單位；不是負的幾何長度。')],'答案 B：−7',['兩常數乘積要等於−12。','兩常數相加才是k。','依國中整係數分解的作答慣例判斷。']),
894:('把讀對的係數各留一項',[('① 甲留下正確常數b','甲只看錯x項係數。由根−2、3重建(x＋2)(x−3)，可知b＝−6。','數線標出甲算出的兩根−2與3，非原方程式的正確根。'),('② 乙留下正確一次項a','乙只看錯常數。根4、−5之和是−1，因此原一次項係數a＝1。','數線標出乙算出的兩根−5與4，非原方程式的正確根。'),('③ 回到原題要求a−b','a＝1、b＝−6，故a−b＝1−(−6)＝7。數線由−6到1相差7。','同尺度數線從−6到1的向右差距7。')],'答案 A：7',['甲：根的乘積保住b。','乙：根的和保住a。','不要採用各人看錯的那一項。']),
896:('平方差拆成正整數乘積',[('① 外面積減裡面積','P＝(4x＋3)²−(3x＋5)²＝(x−2)(7x＋8)。圖先用最後x＝3的15與14回查。','外邊15、內邊14的精確同心正方形，是x＝3回查示例。'),('② 質數要讓小因數等於1','x＞2，兩因數都為正；7x＋8＞1，所以x−2只能是1，得到x＝3。','15×15減14×14的等面積L形重排，保留29個單位格。'),('③ 回代後得到29','x＝3時，225−196＝29＝1×29。細長條正好29格，不把負式值當邊長。','29個等寬單位格組成1×29的長條。')],'答案 C：29',['先用外邊大於內邊，得x＞2。','兩因數為正整數才用質數條件。','x＝3時，外邊15、內邊14。']),
898:('共邊找因式，總長取兩倍',[('① 兩塊共用同一條高','面積分別為(3x＋1)(2x−5)、(3x＋1)(4x−6)，共邊CD＝3x＋1。','左右兩塊共用橘色直邊；本圖以x＝4的13高、3與10寬按比例示意。'),('② 沿水平方向加兩段寬','AD＝2x−5、DE＝4x−6，所以AE＝6x−11。圖用x＝4驗算，兩寬是3及10。','共高13、左右寬3與10的精確x＝4示例，非假定一般x固定為4。'),('③ 上下兩條大邊相等','BF＝AE，因此AE＋BF＝2(6x−11)＝12x−22。只算題目問的第(2)小題。','以橘色標出大長方形上下兩條等長邊。')],'AE＋BF＝12x−22',['先分解兩塊面積，找出共邊。','AE＝AD＋DE，BF＝AE。','所有邊須為正；幾何範圍x＞5/2。']),
900:('等差中項就是兩端的平均',[('① 第一組：a＋b＝10','兩端平均5，所以兩端和為10。圖用算出的b＝−2、a＝12驗算，中點正好5。','同尺度數線−2到12，中點5，兩半長度相等。'),('② 第二組：3a＝36','(a＋b)＋(2a−b)＝36，b相消，得a＝12；回查10與26的中點是18。','數線10到26，中點18，左右各距8。'),('③ 求的是差，不是和','a＝12、b＝−2，a−b＝14。減負數要加回，數線距離也正好14。','從−2到12的正向差距14。')],'答案 C：14',['a＋b＝10。','3a＝36，得a＝12。','b＝−2，故a−b＝14。']),
902:('隔兩項看平方，整列倍乘不改公比',[('① 第2到第4項走兩步','−315÷(−35)＝9＝r²；中間還隔著第3項，不能當成只乘一次r。','第2、3、4項的三節點與兩段相同公比弧線。'),('② r的正負都可能','r²＝9，所以r＝3或−3。只給這兩個偶數項，無法排除其中一種符號。','數線上的−3與3兩個對稱可行值，標籤由HTML說明。'),('③ 每項乘−5會約掉','新相鄰項比值為[(−5)aₙ₊₁]/[(−5)aₙ]，倍率約掉，仍為原公比r。','上下兩條等比節點鏈逐項同倍率對應，連結步數相同。')],'答案 A：±3',['隔兩項，所以得到r²。','r＝3與r＝−3都符合。','非零倍乘改項值，不改相鄰項比。']),
904:('等差看差值，不看指數表面',[('① 先算第6項等於1','(−1)⁶＝1，但題目仍是等差數列；不能把每項當成(−1)ⁿ。','六個等間隔項次點，兩端標色，非交錯±1序列。'),('② 六項之間只有五段','首項−1到第6項1，合計增加2，平均分成5個公差，d＝0.4。','五個等寬區間代表第1至第6項的五次公差。'),('③ 第3項只走兩步','a₃＝−1＋2×0.4＝−0.2。圖中第3點是橘點；六項依序穩定遞增。','六項數值−1、−0.6、−0.2、0.2、0.6、1的精確等差折線，第三點高亮。')],'答案 B：−0.2',['第6項給定值是1。','d＝[1−(−1)]÷5＝0.4。','第3項＝首項＋2d。']),
906:('插入項總和，要扣掉兩端',[('① n項之外還有兩個端點','全列共n＋2項，首末平均12。圖用最後n＝8的10項回查，兩端另著色。','10個等間隔節點，8個插入項與2個端點分色。'),('② 插入項也兩兩平均12','全部和12(n＋2)，扣掉兩端和24，剩下12n；相對的插入項每對和24。','8個插入節點形成4組對稱配對，不包括外側兩端。'),('③ 96除以12得到項數','12n＝96，得n＝8；圖有8排，每排12個單位格，共96。','精確12欄8列、96個單位格的乘積圖。')],'答案 A：8',['96只算插入的n項。','全列n＋2項，兩端和24。','插入項平均12，所以n＝96÷12。']),
908:('先解直行，再用橫列對稱',[('① 直行四格有三段','頂−10、底2，公差為12÷3＝4；交叉格是第2格，值為−6。','四格直行，橘色交叉格在由上第2格。'),('② 橫列七格，中間是第4格','交叉格同時是橫列正中央。等差數列左右對稱的兩項，其和等於2倍中項。','七格橫列，正中央第4格以橘色標示。'),('③ 不用求橫列公差','最左x與最右y對稱，x＋y＝2×(−6)＝−12；其他兩對也有相同和。','七格中的三組左右對稱配對，皆圍繞橘色中格。')],'答案 A：−12',['直行公差4，交叉格−6。','橫列7格的第4格為中項。','兩端和＝2倍中項。'])}
for n,ps in arts.items():
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="a" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0 0L4 2L0 4Z" fill="#639abc"/></marker></defs>'
 for i,g in enumerate(ps):svg+=f'<g transform="translate({i*180} 0)"><rect width="180" height="180" fill="{["#f8f4e9","#eef4ec","#eef3f7"][i]}"/>'+g+'</g>'
 svg+='</svg>';ap=Path(f'docs/comics/art/q-{n}.svg');ap.write_text(svg);title,pan,ans,pts=copies[n];spec={'id':f'q-{n}','subject':'Math','title':title,'art':str(ap),'layoutVersion':'native-fluid-v6','panels':[{'heading':a,'text':b,'alt':c} for a,b,c in pan],'fourth':{'answer':ans,'points':pts},'protectedWords':['等差數列','等比數列','判別式','因式分解','整係數','告訴乃論'][:5],'sourceUrl':URL,'originalMaterialsChecked':True,'sourceGeneratedArtUsed':False,'generationMethod':'new exact native SVG algebra/geometry/number-line diagram, precise labels and formulas remain HTML','rationale':'原卷與全部選項親見，獨立代數重算；圖逐題繪出平方實根範圍／整數配對／保留係數／平方差／共邊／中點／倍率／間隔／配對或十字拓樸，不使用無關人物圖。'};Path(f'docs/comics/q-{n}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print('10 exact native math specs')
