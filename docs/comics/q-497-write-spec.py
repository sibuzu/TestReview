from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-497.png');d={'id':'q-497','subject':'Chinese','title':'兩空一起讀：層巒聳翠，矗立高峰','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 層巒：層層重疊的山峰','text':'第一空接著「聳翠接天宮」，要寫層層山峰高聳青翠的景象。層巒直接點出重疊山峰，搭配最自然；繁複只說繁多複雜，沒有把眼前的山巒景象寫清楚。','alt':'全新內建青綠山巒前後重疊的文學山景，非玉山測繪或真實照片，沒有把天宮畫成空中宮殿。'},
{'heading':'② 矗立：高聳直立的樣子','text':'後兩句由雲湧、風濤急，寫到山峰仍高聳直立，用矗立最貼切。鼎立著重三方如鼎足般並立，不是單純寫一座主峰高聳；不要和鼎力、畢力或助力混成同一個詞。','alt':'全新內建一座主要高峰聳於雲間，其他較低山脊在下，不畫三座等大主峰或實際地理最高排名。'},
{'heading':'③ 兩個詞都放回原詩，選整組最貼切','text':'佇立可以寫人停留站立，山峰也能擬人，但D的繁複仍不如層巒貼合前句。不能只挑一個看起來可用的詞；兩空一起看，A的層巒／矗立最能連貫原詩山景。','alt':'全新內建成人師生在有護欄安全觀景臺對讀空白紙並指山景，圖作詞義教學情境，文字與各選項精確比較由HTML列出。'}],
'fourth':{'answer':'答案 A：層巒／矗立','points':['層巒：重疊山峰，接聳翠的景象。','矗立：高聳直立，寫山峰的形勢。','兩空都須合詩意，不用原AI改寫詩句來驗證格律。']},
'protectedWords':['層巒','矗立','聳翠接天宮','任憑雲湧風濤急','高聳直立','鼎立','鼎力','畢力','助力','佇立','繁複','山巒'],
'originalChecked':{'images':['site/dist/assets/questions/q-497-source-372531008a.jpg'],'visualChecked':True,'answer':'A','notes':'親見四句兩空及四組詞；原卷聳翠接天宮、任憑雲湧風濤急，C壁立、D佇立，紅A；不採原AI另改詩句平仄說。'},
'sourceUrl':'https://share.gemini.google/1P48K0fgDy6p','answerCheckedAgainst':'原卷紅A、兩空詞義分別回詩核對；教育部層巒疊嶂/矗立/鼎立詞義佐證。',
'references':[{'title':'教育部簡編辭典：層巒疊嶂','url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=38241&la=0&powerMode=0','supports':'層疊山峰的概念，非單一層巒詞條','access':'主文已讀'}, {'title':'教育部重編辭典：矗立','url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=125485&la=0&powerMode=0','supports':'高聳直立','access':'主文已讀'}, {'title':'教育部重編辭典：鼎立','url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=46994&la=0&powerMode=0','supports':'三方如鼎足般對立','access':'主文已讀'}],
'rationale':'用重疊山巒和單一主要高峰概念景分辨兩詞，第三格提醒整組搭配，不讓影像決定精確玉山山形、全球高度排名或原詩平仄。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-497-generation.json','promptFile':'docs/comics/q-497-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'A','bothBlanksChecked':True,'sourcePoemRewritten':False,'metricBasedOnInventedPoem':False,'yushanSurveyOrPhoto':False,'heightRankingClaim':False,'literalSkyPalace':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-497.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
