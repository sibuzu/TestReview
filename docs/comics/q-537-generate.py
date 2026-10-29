import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#bd8b69"/></marker></defs>']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def rail(o,y):
 s.append(f'<path d="M{o+20} {y}H{o+180}M{o+20} {y-5}V{y+5}M{o+180} {y-5}V{y+5}" fill="none" stroke="#799690" stroke-width="2"/>')
def dot(o,k,y,name,c):
 x=o+20+k*80;s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>');t(x,y-17,name,16,c)
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'(a) 先只有 Tom',18);rail(0,105);dot(0,1,105,'Tom','#ac7958');t(60,128,'1 km',16);t(140,128,'1 km',16);t(100,168,'2公里海灘的中央',16)
t(300,22,'(c) 兩人各半中央',17);rail(200,105);dot(200,.5,105,'Tom','#ac7958');dot(200,1.5,105,'Sam','#67849b')
s.append('<path d="M300 49V149" stroke="#b6c7bc" stroke-dasharray="4 4"/>');t(240,129,'0.5',14);t(300,129,'1 km',16);t(360,129,'0.5',14);t(300,168,'攤位在0.5、1.5公里',15)
t(500,20,'(d) Tom先靠中央',16);rail(400,75);dot(400,1,75,'Tom','#ac7958');dot(400,1.5,75,'Sam','#67849b')
s.append('<path d="M460 95Q475 110 496 96" fill="none" stroke="#bd8b69" stroke-width="2" marker-end="url(#a)"/>')
t(500,121,'(b) Sam再跟上',16);rail(400,177)
s.append('<path d="M493 147L500 177L507 147" fill="none" stroke="#608a72" stroke-width="2"/>');t(468,145,'Tom',14,c='#ac7958');t(533,145,'Sam',14,c='#67849b');s.append('<circle cx="500" cy="177" r="5" fill="#608a72"/>')
s.append('</svg>');Path('docs/comics/art/q-537.svg').write_text(''.join(s))
x={'id':'q-537','subject':'English','title':'各半中央之後，Tom先移，Sam才跟上','art':'docs/comics/art/q-537.svg','protectedWords':['Tom','Sam','0.5公里','1.5公里','各半中央','圖序','相鄰','(a)','(c)','(d)','(b)'],'panels':[{'heading':'① (a)：先只有Tom，在整條海灘中央','text':'故事先說Tom一人來到2公里海灘，把攤位設在中央，兩側各1公里。先找只有一個攤位的(a)，不能一開始就放兩人相鄰的結局。','alt':'長2公里位置線的中央1公里處只有Tom，左右各1公里，未加入Sam或虛構顧客密度。'},{'heading':'② (c)：Sam加入，各在自己一半的中央','text':'兩人先商量把海灘分兩半，再各自站到那一半的中央。攤位位置是0.5與1.5公里，中間隔1公里，對應(c)，不是已經靠在一起。','alt':'同一比例位置線上Tom在0.5公里、Sam在1.5公里，中央虛線分兩半，兩端到攤位各0.5公里，中間1公里。'},{'heading':'③ (d)先Tom移，(b)才兩人相鄰','text':'接著Tom先靠近海灘中央，Sam還沒移，是(d)。Sam發現生意變少後才跟上，最後兩攤相鄰，才是(b)。要保留誰先移、誰後移的先後。','alt':'上方(d)用中央位置示意Tom先移、Sam仍在原半中央；下方(b)兩人標籤連到同一中央標點，表示最後相鄰，不虛構精確攤位寬度或間距。'}],'fourth':{'answer':'答案 B：(a)→(c)→(d)→(b)','points':['一人中央，再兩人各半中央。','Tom先靠中央，Sam之後才跟著移。','兩攤相鄰是最後結果，不是第二步。']},'rationale':'實看完整38–40文章及38四選項，另逐張看(a)(b)(c)(d)原卷位置圖，讀來源395–456行。新原生SVG同尺度區分四步，第三格上下呈d/b而不忽略第四狀態；d中央附近以中央點作示意，不新增精確停點條件。已resolved correction-q-537-4cfc15cdd15a距離措辭不重開，不把less than說成端點也嚴格小於。B答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-537-reading-source-4e5503d424.jpg','site/dist/assets/questions/q-537-source-b510c53f19.jpg','site/dist/assets/questions/q-537-option-a-1f4fdc909d.jpg','site/dist/assets/questions/q-537-option-b-f978969c94.jpg','site/dist/assets/questions/q-537-option-c-20202437ee.jpg','site/dist/assets/questions/q-537-option-d-79a35ecedc.jpg','site/dist/sources/gemini-niuTSqX6ssM7.txt lines 395–456'],'sourceUrl':'https://share.gemini.google/niuTSqX6ssM7','priorConfirmation':'correction-q-537-4cfc15cdd15a','generationMethod':'precise native SVG common-scale beach-location sequence with four story states across three diagrams','answerCheckedAgainst':'a一攤中央→c兩半中央→d僅Tom移中央附近→bSam跟移兩攤相鄰，B。c端點最遠0.5不誤作嚴格小於；已確認。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-537.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert [1-0,2-1]==[1,1]
assert [.5-0,1.5-.5,2-1.5]==[.5,1,.5]
Path('docs/comics/q-537-location-validation.json').write_text(json.dumps({'id':'q-537','scale':'80 SVG units per km in every rail','a':{'Tom':1,'Sam':None,'edgeDistances':[1,1]},'c':{'Tom':.5,'Sam':1.5,'segmentLengths':[.5,1,.5],'maximumNearestStandWalk':.5},'d':{'Tom':'central schematic point, not new measured condition','Sam':1.5,'onlyTomMoved':True},'b':{'TomAndSam':'same central marker, label leaders only offset','bothMoved':True},'sourceDiagramOrder':['a','c','d','b'],'answer':'B'},ensure_ascii=False,indent=2)+'\n')
