from native import *
# q1144: a literal three-seat table geometry, then proportional historical dates.
b=label(320,53,'戰後國共和談的三方',42)
b+='<ellipse cx="320" cy="340" rx="190" ry="120" fill="#b58f66" stroke="#816144" stroke-width="8"/><ellipse cx="320" cy="330" rx="182" ry="108" fill="#dfc39c"/>'
for x,y,t,c in [(320,150,'美國',GOLD),(120,490,'國民政府',BLUE),(520,490,'中共',RED)]:
 b+=f'<rect x="{x-42}" y="{y-25}" width="84" height="60" rx="16" fill="{c}"/><rect x="{x-52}" y="{y-50}" width="104" height="20" rx="9" fill="{c}"/>'+label(x,y+96,t,36,c)
b+=label(320,622,'席位為關係示意，非歷史座次',27,'#657e7f');save('q-1144',2,b)
save('q-1144',3,timeline([(1924,['聯俄容共'],-1),(1936,['西安事變'],1),(1945,['美國開始','來華調停'],-1),(1947,['調停失敗'],1)],1922,1949,'三個階段別混淆'))
# q1145: actual modern locator geometry and historical existence interval, not fabricated historical border.
b=label(320,54,'滿洲國存在的時間區間',39)+line(90,290,560,290,INK,5)
lo,hi=1915,1950;xx=lambda y:90+(y-lo)/(hi-lo)*470
b+=f'<rect x="{xx(1932)}" y="255" width="{xx(1945)-xx(1932)}" height="70" rx="8" fill="{GOLD}"/>'
for y in [1919,1928,1932,1945,1949]:
 x=xx(y);b+=line(x,245,x,340,INK,3)
 # stagger labels where years are close.
 yy=389 if y in [1919,1932,1949] else 445
 b+=label(x,yy,str(y),36,RED if y in [1932,1945] else INK)
b+=label(320,190,'1932–1945',54,RED)+label(320,523,'早於1932：尚未成立',38)+label(320,580,'晚於1945：已終結',38);save('q-1145',1,b)
b,xy=mapview((108,34,134,50));b+=label(320,49,'瀋陽位於中國東北',43)+city(xy,'Shenyeng','瀋陽',20,55,c=RED)+city(xy,'Beijing','北京',-15,58,c=BLUE)+label(455,185,'東北',46,TEAL)+label(320,626,'現代底圖僅供地點定位',29,'#657e7f');save('q-1145',2,b,SEA)
b=label(320,53,'四選項的時間，放同一刻度',36)+line(100,110,100,535,INK,4)
start,end=1917,1949
for y in [1917,1928,1932,1945,1949]:
 yy=115+(y-start)/(end-start)*420;b+=line(90,yy,110,yy,INK,3)+label(80,yy+10,str(y),26,INK,'end')
for x,a,z,t,c in [(190,1917,1919,'A',BLUE),(300,1919,1928,'B',BLUE),(410,1932,1945,'C',RED),(520,1945,1949,'D',BLUE)]:
 y=115+(a-start)/(end-start)*420;h=(z-a)/(end-start)*420;b+=f'<rect x="{x-23}" y="{y}" width="46" height="{max(10,h)}" fill="{c}" rx="7"/>'+label(x,y-18,t,46,c)
b+=label(320,605,'C：1932–1945，瀋陽',39,RED);save('q-1145',4,b)
# q1146: four different spatial scales/questions, no guessed historical frontiers or exact march routes.
b,xy=mapview((100,18,129,44));b+=label(320,49,'先對照原卷四點',44)
for name,t,dx,dy,c in [('Beijing','乙',-30,-20,BLUE),('Shanghai','甲',35,-12,BLUE),('Wuhan','丁',-40,35,BLUE),('Guangzhou','丙',0,58,RED)]:b+=city(xy,name,t,dx,dy,c)
b+=label(320,626,'依原卷相對區位，不表歷史疆界',25,'#657e7f');save('q-1146',1,b,SEA)
b,xy=mapview((109,20,118,27));b+=label(320,49,'廣東的廣州在珠江口附近',38)+city(xy,'Guangzhou','廣州',-40,-30,c=RED)+label(320,180,'廣東',47,TEAL)+label(450,536,'南海',42,BLUE)+label(320,626,'城市定位，非會場精測點',28,'#657e7f');save('q-1146',2,b,SEA)
b,xy=mapview((106,20,122,34));b+=label(320,49,'北伐由廣東向北推進',40)
x,y=xy(*CITY['Guangzhou']);u,v=xy(*CITY['Wuhan']);b+=arrow(x,y-20,u,v+20,RED)+city(xy,'Guangzhou','廣州',15,60,c=RED)+city(xy,'Wuhan','湖北一帶',-20,-25,c=TEAL)+label(220,370,'湖南',42)+label(320,626,'概括方向，不作單一路線宣稱',27,'#657e7f');save('q-1146',3,b,SEA)
b=label(320,50,'大會地點不是北伐終點',41)+'<ellipse cx="165" cy="275" rx="112" ry="72" fill="#c8a57b"/><ellipse cx="165" cy="275" rx="83" ry="47" fill="#9fba80"/><path d="M82 275H248" stroke="#fffaf0" stroke-width="3"/><rect x="130" y="184" width="70" height="18" fill="#8b6647"/>'+label(165,383,'東較場',47,TEAL)+label(165,443,'廣州',48,RED)+arrow(290,285,460,150,RED)+label(470,105,'向北推進',36,RED)
# Geographic inset is a true coastline around southern China with Guangzhou marker.
a,xy=mapview((108,20,120,29));# reuse actual geometry in small inset by transform.
a+=city(xy,'Guangzhou','丙',0,52,c=RED)
b+='<g transform="translate(300 310) scale(.48)">'+a+'</g>'+label(320,600,'廣東各界、東較場 → 丙',37,RED);save('q-1146',4,b)
# q1148: Xian locator, dated historical context, and distinct dated policy comparison table with physical paper/ink illustration.
b,xy=mapview((101,29,120,41));b+=label(320,49,'西安事變的地理位置',43)+city(xy,'Xian','西安',0,60,c=RED)+city(xy,'Nanjing','南京',15,60,c=BLUE)+label(320,626,'1936年事件定位，非勢力範圍',26,'#657e7f');save('q-1148',1,b,SEA)
b=label(320,53,'同在1936年的不同主張',41)+book(65,150,180,235,BLUE)+book(395,150,180,235,TEAL)+lines(160,450,['國民政府','先安內再攘外'],36,BLUE,gap=48)+lines(480,450,['事變要求','停止內戰抗日'],35,TEAL,gap=48)+line(320,150,320,550,'#c8d1ca',3)+label(320,610,'不能把兩方主張對調',40,RED);save('q-1148',2,b)
save('q-1148',4,timeline([(1927,['清黨'],-1),(1931,['九一八'],1),(1936,['西安事變'],-1),(1937,['七七事變'],1)],1925,1939,'不能把政策移錯年代'))
print('12 C-series SVGs saved')
# q1148 panel2 revised as geographic policy targets, rather than two labeled books.
b,xy=mapview((100,24,139,44));b+=label(320,49,'分清安內與攘外的對象',41)
x,y=xy(*CITY['Nanjing']);u,v=xy(109,36.5);j,k=xy(130,35)
b+=dot(x,y,BLUE,10)+arrow(x-20,y,u+18,v+16,BLUE)+arrow(x+18,y-20,j-15,k+20,RED)
b+=label(190,210,'內部衝突',42,BLUE)+label(480,330,'對日抵抗',41,RED)+label(x,y+60,'南京',39,TEAL)+label(320,566,'先安內 ≠ 停止內戰',39)+label(320,626,'政策對象示意，非部隊行軍路線',26,'#657e7f');save('q-1148',2,b,SEA)
