from native import *
# q1139: real city locator, physical track/cause illustration, dated event axis.
b,xy=mapview((118,37,128,45));b+=label(320,49,'柳條湖在瀋陽附近',42)+city(xy,'Shenyeng','瀋陽',0,65)+label(150,210,'東北',48)+label(320,626,'區域定位，非鐵路路線圖',29,'#657e7f');save('q-1139',2,b,SEA)
b=label(320,56,'鐵路事件 → 侵占東北',40)
# Rails and sleepers are actual geometric objects; not text-only flow boxes.
for y in range(130,370,35):b+=f'<path d="M170 {y}L470 {y}" stroke="#9c7650" stroke-width="18"/>'
b+=line(230,112,230,375,'#647176',10)+line(410,112,410,215,'#647176',10)+line(426,247,448,375,'#647176',10)
b+=f'<path d="M383 220L401 193L411 223L440 214L420 241L446 260L416 261L406 289L395 260L369 268L385 242L364 226Z" fill="#edb75d" stroke="{RED}" stroke-width="4"/>'
b+=label(320,423,'製造事件作藉口',42)+arrow(320,450,320,495,RED)+label(320,554,'進攻瀋陽、東北',45,RED)+label(320,612,'構圖示意，不重建現場',29,'#657e7f');save('q-1139',3,b)
save('q-1139',4,timeline([(1931.71,['九一八'], -1),(1932.17,['滿洲國'],1),(1937.52,['七七事變'],-1),(1941.93,['珍珠港'],1)],1930,1943,'四事件按年份定位'))
# Replace decimal year glyphs with familiar year labels without moving true chronological positions.
p=OUT/'q-1139-source72-4.svg';s=p.read_text()
for a,c in [('1931.71','1931'),('1932.17','1932'),('1937.52','1937'),('1941.93','1941')]:s=s.replace('>'+a+'<','>'+c+'<')
p.write_text(s)
# q1140 locator comparisons; arrows show displacement direction, not asserted historic travel tracks.
b,xy=mapview((116,29,123,34));b+=label(320,49,'日軍由上海進逼南京',40)
x,y=xy(*CITY['Shanghai']);u,v=xy(*CITY['Nanjing']);b+=arrow(x-12,y-14,u+12,v+14,RED)+city(xy,'Shanghai','上海',-45,58,c=TEAL)+city(xy,'Nanjing','南京',-25,-24,c=RED)+label(320,626,'區域方向示意，非作戰路線',28,'#657e7f');save('q-1140',1,b,SEA)
b,xy=mapview((102,24,124,36));b+=label(320,49,'移駐重慶，繼續抗戰',42)
x,y=xy(*CITY['Nanjing']);u,v=xy(*CITY['Chongqing']);b+=arrow(x-20,y+30,u+20,v+10,RED)+city(xy,'Nanjing','南京',0,-25,c=BLUE)+city(xy,'Chongqing','重慶',-15,58,c=RED)+label(320,565,'向內陸移駐',41,TEAL)+label(320,626,'只示方向，非精確遷移路徑',28,'#657e7f');save('q-1140',3,b,SEA)
# q1142: spatial contrast, within-year date order, broad period location.
b,xy=mapview((113,37,126,44));b+=label(320,49,'北京撤返東北途中',42)
x,y=xy(*CITY['Beijing']);u,v=xy(*CITY['Shenyeng']);b+=arrow(x+20,y-15,u-20,v-20,RED)+city(xy,'Beijing','北京',0,60,c=BLUE)+city(xy,'Shenyeng','瀋陽',-8,65,c=RED)+label(320,570,'皇姑屯在瀋陽附近',40)+label(320,626,'方向定位，非實際鐵路圖',28,'#657e7f');save('q-1142',2,b,SEA)
b=label(320,54,'同是1928，仍要分先後',40)+line(320,130,320,520,INK,5)+dot(320,155,RED,10)+dot(320,490,TEAL,10)+lines(280,145,['6月4日','皇姑屯事件'],40,RED,'end',gap=52)+lines(360,480,['12月29日','東北易幟'],36,TEAL,'start',gap=50)+label(320,610,'前者發生於北伐末期',39,RED);save('q-1142',3,b)
b=label(320,55,'事件落在北伐階段',43)
x0,x1=80,570;start,end=1926,1950
xx=lambda yr:x0+(yr-start)/(end-start)*(x1-x0)
for y,a,z,t,c in [(160,1926,1928.5,'北伐',RED),(295,1937,1945,'八年抗戰',TEAL),(430,1946,1949,'戰後內戰',BLUE)]:
 b+=line(x0,y,x1,y,'#becac1',3)+f'<rect x="{xx(a)}" y="{y-14}" width="{xx(z)-xx(a)}" height="28" rx="5" fill="{c}"/>'+label(80,y-38,t,39,c,'start')+label(320,y+59,f'{int(a)}–{int(z)}',33,c)
b+=dot(xx(1928.426),160,RED,11)+line(xx(1928.426),150,xx(1928.426),99,RED,3)+label(370,107,'1928皇姑屯',39,RED)+label(320,610,'各條使用相同年份刻度',30,'#657e7f');save('q-1142',4,b)
print('8 B-series SVGs saved')
