from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-817.svg');p=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-label="古籍解說錦瑟外觀與悲意，及本文全唐詩十一例李商隱四例口徑"><rect width="900" height="300" fill="#faf8ed"/><style>text{font-family:"Noto Sans CJK TC",sans-serif;text-anchor:middle;fill:#294c48}.h{font-size:24px;font-weight:700}.w{font-size:26px;font-weight:700}.s{font-size:20px}</style>']
for i,(title,quote,role,meaning) in enumerate([('《周禮樂器圖》','繪文如錦','外觀／構造','華美高貴'),('《史記封禪書》','瑟聲的悲意','援引傳說','悲哀象徵')]):
 p.append(f'<g id="book-{i}" transform="translate({i*300} 0)"><text x="150" y="34" class="h">{title}</text><path d="M28 64 Q90 51 150 68 Q210 51 272 64 V167 Q210 153 150 171 Q90 153 28 167 Z" fill="#eee4ce" stroke="#8e9379" stroke-width="3"/><path d="M150 69 V170" stroke="#8e9379" stroke-width="2"/><rect x="49" y="87" width="202" height="55" rx="9" fill="#fcfaf2"/><text x="150" y="123" class="w">{quote}</text><text x="150" y="215" class="s">{role}</text><rect x="36" y="235" width="228" height="48" rx="12" fill="#e2ebde"/><text x="150" y="267" class="w">{meaning}</text></g>')
p.append('<g id="statistics" transform="translate(600 0)"><text x="150" y="34" class="h">本文統計範圍</text><text x="150" y="75" class="w">《全唐詩》11 次</text>')
coords=[(45+42*k,119) for k in range(6)]+[(66+42*k,161) for k in range(5)]
for i,(x,y) in enumerate(coords):p.append(f'<circle class="occurrence" cx="{x}" cy="{y}" r="13" fill="{"#49755d" if i<4 else "#d5ddcb"}"/>')
p.append('<text x="150" y="211" class="w">李商隱 4 次</text><text x="150" y="246" class="s">引例要限定詩人</text><text x="150" y="279" class="s">非詩人創作獨白</text></g></svg>');a.write_text(''.join(p))
d={'id':'q-817','subject':'Chinese','title':'兩本古籍解說錦瑟特性，統計與引例要標清範圍','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-817-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 引《周禮樂器圖》，說外觀與構造','text':'本文先說美麗高貴，再引雅瑟、頌瑟與繪文如錦的說明。引文的作用，是解說錦瑟的外觀與構造，並非摘錄李商隱本人談創作背景的獨白。','alt':'全新精確SVG古籍書名、繪文如錦與外觀構造華美高貴的文字關係，未重畫瑟或臆造琴絃數與形制。'},
{'heading':'② 引《史記封禪書》，說悲哀意象','text':'本文又援引鼓瑟而悲的傳說，說明瑟的悲哀象徵；這和前面的華美特性，合成文章所說美麗與哀愁的共同結晶。前後兩處引古籍，都為了說明錦瑟的特性，正扣住 A。','alt':'全新精確SVG史記封禪書/瑟聲悲意/援引傳說/悲哀象徵關係，沒有神祇砸琴或弦數從五十到二十五的AI重製。'},
{'heading':'③ 有統計與引例，選項範圍仍須精準','text':'依本文統計，《全唐詩》出現十一次，李商隱用了四次，並列舉他的詩句。C 應明確限定《全唐詩》，D 應限定李商隱在《全唐詩》中的引例；不以未列完詩句判錯。','alt':'全新精確SVG依本文十一圓點、四點著色表示李商隱用例；標本文全唐詩口徑，不宣稱重查整部古典詩歌或讓圓點面積代表文本量。'}],
'fourth':{'answer':'答案 A：引用古籍說明錦瑟的特性','points':['兩處引古籍，分別解說華美與悲哀特性。','C 統計限《全唐詩》；D 引例限李商隱在其中的詩句。','引詩句，不等於引用詩人說明創作背景的獨白。']},
'protectedWords':['錦瑟','李商隱','全唐詩','周禮樂器圖','史記封禪書','繪文如錦','外觀','構造','悲哀意象','悲哀象徵','美麗高貴','華美','傳說','古籍','統計','引例','創作背景','獨白','十一次','四次','共同結晶','雅瑟','頌瑟'],
'originalChecked':{'images':['site/dist/assets/questions/q-817-source-1.jpg','site/dist/assets/questions/q-817-source-2.jpg'],'visualChecked':True,'answer':'A','notes':'親見共同長文、三引詩/兩古籍及29四項紅改A。沿用resolved correction-q-817-13b1f1004b24：C限定全唐詩統計、D限定李商隱用例；不重開、原四項不改、不擅加所有後判錯。'},
'sourceUrl':'https://gemini.google.com/share/ec6c955b81b3','answerCheckedAgainst':'原卷引用兩古籍各解華美與悲哀；使用者已確認A，C/D精確範圍沿既有結案，B詩句非詩人創作獨白。',
'rationale':'古籍→解說功能與明確統計口徑三圖，不重造器物絃數、不把神話當史實。四/十一僅視覺化本文口徑，未聲稱重新校勘全唐詩；已確認A不重開。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'A','statisticalCorpus':'依本文《全唐詩》','occurrences':11,'liShangyinOccurrences':4,'examplesScope':'李商隱在全唐詩中的用例','completenessArgumentUsedToRejectD':False,'allAddedToOriginalOptions':False,'mythTurnedIntoHistory':False,'instrumentAnatomyReconstructed':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-817.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
