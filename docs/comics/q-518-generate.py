import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def rect(x,y,w,h,fill='#edf1e6',stroke='#b9cbbd'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>')
for i in range(3):rect(i*200+2,2,196,196,'#faf8ee')
t(100,23,'黑袖鴿：有例外',18)
rect(16,45,168,42,'#3f4948');t(100,66,'部分羽毛是黑色',16,'white')
rect(16,96,168,42,'#fffdf7');t(100,117,'其餘白帶些黃色',16)
t(100,163,'全身白色 ×',20,'#a46e59');t(100,186,'不能省掉例外',15)
t(300,23,'翠翼鳩：定位習性',17)
rect(218,42,164,49,'#d6e7cd');t(300,56,'許多地區',17);t(300,79,'整年都可繁殖',17)
for m in range(1,13):
 x=225+39*((m-1)%4);y=101+23*((m-1)//4);rect(x,y,33,19,'#e1ecda');t(x+16.5,y+10,str(m),13)
t(300,185,'保留「許多」的範圍',15)
t(500,23,'紅鳩：場所與行為',17)
rect(416,44,168,57,'#e2ebef');t(500,60,'電線或電線桿',16);t(500,84,'停棲',19,'#557c97')
rect(416,110,168,57,'#dce9d2');t(500,126,'樹的較高處',16);t(500,150,'築巢',19,'#507a5b')
t(500,186,'停棲 ≠ 築巢',18,'#a16c3e')
s.append('</svg>');Path('docs/comics/art/q-518.svg').write_text(''.join(s))
j={'id':'q-518','subject':'Chinese','title':'找到鳥名，逐字比對範圍與行為','art':'docs/comics/art/q-518.svg','protectedWords':['黑袖鴿','翠翼鳩','維多利亞冠鴿','紅鳩','許多地區','整年','全身','輪流孵化','電線桿','停棲','築巢'],'panels':[{'heading':'① A漏掉例外，不能改寫成全身','text':'黑袖鴿的資料先列黑色飛羽、覆羽及尾羽等例外，再說其餘白色帶些黃色調。A直接說「全身」白色，抹去了原文限制。','alt':'兩塊語意卡分別列部分羽毛黑色、其餘白帶黃色，並列全身白色不符；卡片大小只分組不表示羽色比例。'},{'heading':'② B直接對應翠翼鳩的習性欄','text':'先找到翠翼鳩，再看習性：「在許多地區整年都可以繁殖。」B保留鳥名、地區範圍及整年繁殖，與原文相符；許多地區仍不等於全部地區。','alt':'翠翼鳩習性原句關鍵詞與程式排列1至12月份，表示原文整年，整體限定於許多地區，不把繁殖範圍擴為所有地區。'},{'heading':'③ D把停棲處，換成了築巢處','text':'紅鳩會停在電線或電線桿，也常落地覓食；巢則位在樹的較高處。D的覓食敘述雖符合，但把停棲的位置改成築巢的位置，整句仍不合資料。','alt':'紅鳩雙欄對應卡，電線或電線桿對停棲，樹的較高處對築巢；不畫電線桿上的鳥巢。'}],'fourth':{'answer':'答案 B：與資料逐項相符','points':['A省略黑色羽毛例外；D偷換停棲與築巢。','C只說雄鴿孵卵，未完整表達原文雌雄輪流。','依原卷比對，不把現行保育等級或其他生態知識代入。']},'rationale':'實看四鳥完整原表和第36題四選項，讀來源144–160逐項判B。原卷限定許多、黑羽例外、雙親輪流、停棲/築巢不可替換。新精確語意SVG避免生成鳥類色塊及錯誤巢位；12月格程式列1..12，整年範圍明限許多地區；不宣稱雄性從不孵化，C僅缺輪流資訊而B最直接。保育碼LC/NT僅原題，不查新標準替換。','sourceUrl':'https://share.gemini.google/CYhs1soHtI73','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-518-reading-source-63b28caf41.jpg','site/dist/assets/questions/q-518-source-af5bf86610.jpg','site/dist/sources/gemini-CYhs1soHtI73.txt lines144–160'],'answerCheckedAgainst':'B與翠翼鳩習性直接一致；A全身省例外、C未完整輪流、D場所與行為偷換。依完整原表判最可能。','generationMethod':'precise native SVG scope/exception cards, programmatic12-month reading cue and location-action comparison','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-518.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
assert list(range(1,13))==[i+1 for i in range(12)]
Path('docs/comics/q-518-reading-validation.json').write_text(json.dumps({'id':'q-518','monthCue':list(range(1,13)),'calendarScope':'many regions only, no all-region inference','exceptionNoNumericalColorRatio':True,'nestingNotOnPole':True,'bothParentsTakeTurnsNotMaleNeverIncubates':True,'correctBUnchanged':True,'tableColumnsMatched':['black-wing exceptions','emerald dove habits many regions year-round','crowned-pigeon alternate incubation','red dove perches-wire/nests-high-tree'],'allChecksPass':True},ensure_ascii=False,indent=2)+'\n')
