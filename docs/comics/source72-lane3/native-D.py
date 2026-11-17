from native import *
# q1149: 1912 institutional clue, five powers in final constitution, real chronological axis.
b=label(320,54,'丙：臨時約法的制度線索',40)+hall(70,180,170,TEAL)+hall(400,180,170,BLUE)+label(155,369,'參議院',45,TEAL)+label(485,369,'內閣',45,BLUE)+arrow(395,250,265,250,RED)+label(320,453,'內閣向國會負責',43,RED)+book(250,500,130,90,GOLD)+label(320,150,'1912年',54,GOLD);save('q-1149',1,b)
b=label(320,54,'乙：憲法的五權體制',42)+label(320,113,'主權屬於國民全體',43,RED)
for x,y,t,c in [(130,205,'行政',TEAL),(320,205,'立法',BLUE),(510,205,'司法',GOLD),(220,400,'考試',BLUE),(420,400,'監察',TEAL)]:b+=hall(x-55,y,110,c)+label(x,y+174,t,42,c)
b+=label(320,622,'1946制定，1947施行',35,RED);save('q-1149',3,b)
save('q-1149',4,timeline([(1912,['丙：臨時約法'],-1),(1931,['甲：訓政約法'],1),(1947,['乙：憲法施行'],-1)],1909,1950,'先後：丙 → 甲 → 乙'))
# q1150: exact physical geography plus proportional event chronology.
b,xy=mapview((98,7,132,40));b+=label(320,49,'越南與朝鮮半島分開定位',38)+city(xy,'Hanoi','越南',-30,80,c=RED)+city(xy,'Seoul','韓國',-35,60,c=BLUE)+label(320,626,'現代底圖僅供區域位置判讀',27,'#657e7f');save('q-1150',1,b,SEA)
save('q-1150',4,timeline([(1948,['戰後國共內戰'],-1),(1951,['韓戰'],1),(1969,['尼克森主義'],-1),(1989,['六四事件'],1)],1945,1992,'1969的政策，對應越戰'))
print('5 D-series SVGs saved')
