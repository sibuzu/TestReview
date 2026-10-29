import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'先找上方分布資料',16)
s.append('<path d="M21 113L65 57L100 103L132 49L181 113Z" fill="#c4d8bc" stroke="#608569" stroke-width="2"/>')
t(100,141,'mountains',20);t(100,173,'China and Taiwan',17)
t(300,22,'另外兩項不能亂換',16)
r(216,44,168,57,'#e6edf3');t(300,63,'small animals',18);t(300,85,'如 birds、frogs',16)
r(216,120,168,57,'#f1e5d6');t(300,140,'poisonous',20);t(300,162,'不是被咬也無妨',15)
t(500,22,'下方標為 A Story',16)
s.append('<path d="M419 52Q460 42 500 57Q540 42 581 52V158Q540 148 500 164Q460 148 419 158Z" fill="#efe6cf" stroke="#9b896d" stroke-width="2"/><path d="M500 57V163" stroke="#b8a88e" stroke-width="2"/>')
t(459,93,'蛇',27);t(541,93,'人',27);t(500,135,'故事中的變身',17)
t(500,184,'文化敘事 ≠ 動物能力',14,c='#966745')
s.append('</svg>');Path('docs/comics/art/q-534.svg').write_text(''.join(s))
x={'id':'q-534','subject':'English','title':'先辨資料與故事，再用明文選B','art':'docs/comics/art/q-534.svg','protectedWords':['百步蛇','mountains','China and Taiwan','small animals','birds','frogs','poisonous','A Story','文化敘事','動物能力','臺灣山區'],'panels':[{'heading':'① B對應上方動物資料的山區分布','text':'上方明寫大多在China and Taiwan的mountains。B說人們可能在臺灣山區看到，直接符合；may是可能，不是說每座山一定看得到。','alt':'非比例山形符號配原文mountains與China and Taiwan，僅標明分布線索，不虛構精確地圖、密度或必定目擊地點。'},{'heading':'② 食物與毒性，也要照原資料判讀','text':'資料寫small animals，例如birds或frogs，不能自行改成羊或山羊來支持A。又明寫poisonous，因此不能由本文得到C所說被咬也不會生病的結論。','alt':'上方食物資料與poisonous兩張原文線索卡，沒畫羊當獵物，也不畫危險咬傷或不當處置，不把有毒擴大為每次必然發病。'},{'heading':'③ A Story是傳說，不是生物能力說明','text':'下方漫畫另標A Story，蛇變成人是故事情節。傳說有文化意涵，但不能直接當成動物實際會變人的證據，因此D不合題意。','alt':'書本符號左右標蛇與人，明確寫故事中的變身；不生成真實蛇人變形、不仿造原住民族服飾或把文化故事當科學資料。'}],'fourth':{'answer':'答案 B：可能在臺灣山區看見百步蛇','points':['分布線索在上方動物資料區。','食物與poisonous按原文，不自行換條件。','A Story的傳說情節，不等於真實動物能力。']},'rationale':'實看完整百步蛇特徵/文化/四格故事及第34題四選項，讀來源278–344行。新精確SVG用山區線索、食性毒性明文、另標故事書三層，聚焦資料與文化敘事的閱讀界線；不重畫誤導蛇種外形、不虛構圖騰或山區保證目擊，不延伸醫療處置。B答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-534-reading-figure-94ba874172.jpg','site/dist/assets/questions/q-534-source-42a9e42d30.jpg','site/dist/sources/gemini-niuTSqX6ssM7.txt lines 278–344'],'sourceUrl':'https://share.gemini.google/niuTSqX6ssM7','generationMethod':'precise native SVG documentary evidence versus separately labelled cultural story comparison','answerCheckedAgainst':'上方Most...mountains in China and Taiwan直接支持B may，A替換食物、C與有毒資料不符、D將A Story變身當動物能力，B明確。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-534.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
