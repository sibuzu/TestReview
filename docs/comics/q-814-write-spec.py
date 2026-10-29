from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-814.png');d={'id':'q-814','subject':'Chinese','title':'前文寫形態，後句接捕捉神韻姿態','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 莖葉布散：先看引文描寫什麼','text':'本文把蒝連到莖葉布散的樣子，重點是枝葉展開的形態。雖然前面提到香菜常被人和九層塔混淆，但接下來並沒有並列兩種植物的特徵，不能因此選 A 的差異分析。','alt':'全新內建自然系香菜枝葉向外舒展情境，無九層塔、原產地地圖或精確器官計數，不充當科學鑑定照。'},
{'heading':'② 莖柔葉細：文字描摹柔細樣貌','text':'莖柔、葉細，仍在描寫植物外形；這些短句讓讀者感受它的神韻姿態。本文引用李時珍的解釋，沒有另找證據查驗正誤，引用不等於查證，所以不是 B。','alt':'全新內建香菜細長柔曲葉柄與分裂小葉近景，輔助莖柔葉細的文學描寫，不把圖片當作查證本草綱目正誤的實驗。'},
{'heading':'③ 根多鬚：接續整體的姿態描寫','text':'根多鬚、綏綏然，繼續描摹根鬚與整體樣貌。因此寥寥數句、精確後，最順接捕捉了蒝荽的神韻姿態。這裡也沒有說明植物來自哪裡，不能接 D 的起源地。','alt':'全新內建香菜整株細中央根與多細側根情境，對應原文根多鬚；不畫成洋蔥球根、整把白粗鬚根或介紹原產地。'}],
'fourth':{'answer':'答案 C：捕捉了蒝荽的神韻姿態','points':['莖葉布散、莖柔葉細、根多鬚，都在寫形態。','A 差異比較、B 查證、D 起源，皆不是這段引文的作用。','字形依本文辨析蒝與芫；不擴大成否定所有現行芫荽寫法。']},
'protectedWords':['蒝荽','芫荽','九層塔','莖葉布散','莖柔葉細','莖柔','葉細','根多鬚','綏綏然','神韻姿態','李時珍','本草綱目','引用','查證','寥寥數句','起源地','差異分析','現行'],
'originalChecked':{'images':['site/dist/assets/questions/q-814-source-1.jpg'],'visualChecked':True,'answer':'C','notes':'親見21原全文四項/紅改C，蒝非芫、綏綏然原字核對，不採既有原AI菥蓂或綠綠然；原AI訂正卡已存在不重開。'},
'sourceUrl':'https://gemini.google.com/share/ec6c955b81b3','answerCheckedAgainst':'原卷引用描述莖/葉/根神態，C承接精確；MOE B03993蒝莖葉布散釋義及簡編香菜主文已讀。',
'references':[{'title':'教育部異體字字典B03993：蒝','url':'https://dict.variants.moe.edu.tw/dictView.jsp?ID=68892&powerMode=2&q=1','supports':'草木莖葉布散之形及本草綱目胡荽引文','access':'主文字義已讀，未要求學生用圖鑑鑑定植物'},{'title':'教育部簡編辭典：香菜','url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=27957&la=0&powerMode=0','supports':'分裂細葉形態和現行別名芫荽，避免把文章內字形主張擴張為普遍禁寫','access':'主文已讀，未引入高度、藥效、食用或原產地等旁題知識'}],
'rationale':'新三個植物自然近景對應莖葉布散/莖柔葉細/根多鬚；答案由前文功能而非拿AI圖做查證決定。限制字形說法在本文，既有C不重開。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-814-generation.json','promptFile':'docs/comics/q-814-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'C','comparisonWithBasilInvented':False,'quotationIsIndependentVerification':False,'originClaimed':False,'anatomicalExactnessClaimed':False,'allCurrent芫荽SpellingsCondemned':False,'medicalOrCookingAdviceAdded':False,'rareCharactersKept':['蒝荽','芫荽','綏綏然']},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-814.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
