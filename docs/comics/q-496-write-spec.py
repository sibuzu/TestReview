from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-496.png');d={'id':'q-496','subject':'Chinese','title':'只求自保、占位不任事，才是本文無功的問題','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 官員自稱清廉，還不等於已盡職責','text':'官員以只喝一杯水自稱清廉，卻沒有說自己辦成哪些應辦事務。本文並未否定不收錢的重要，而是追問設官治理百姓，應盡的責任是否有履行。清廉與盡責，要分開檢查。','alt':'全新內建夢中寓言場景，官員持單一清水杯自誇、端正而不恐怖的閻羅王聆聽，無刑罰血腥或真實歷史肖像。'},
{'heading':'② 避嫌疑不言、畏煩重不辦，都是只求自全','text':'怕惹嫌疑就不肯說，怕事情繁重就不肯做，才是文中無功的具體表現。官員只求自己安全，沒有承擔應有職責，對應本題明哲保身、尸位素餐，而非單純沒有獲得重大勳功。','alt':'全新內建寓言官員避開無字案件文書、成人百姓等待的概念回想，沒有收賄、濫殺或新增個案傷亡情節。'},
{'heading':'③ 木偶比喻：不收錢，仍不等於好官','text':'閻羅王用木偶連水都不喝作譏諷：若只以不收錢判好官，木偶豈不更好？圖是這個假設比喻，並非真的放木偶任官。無功指不盡責作為，不能和不收錢畫上等號。','alt':'全新內建穿簡單衣袍的靜止木偶與反思官員，明示為文本假設比較，不是實際木偶被任命或魔法懲罰。'}],
'fourth':{'answer':'答案 C：明哲保身，尸位素餐','points':['本題的自保：怕嫌疑、怕繁重而不任事。','尸位素餐：占著職位，卻未盡應有職責。','本文無功不是不收錢，也未寫官員濫殺人命。']},
'protectedWords':['清廉','盡責','職責','一杯水','避嫌疑','畏煩重','只求自全','無功','明哲保身','尸位素餐','閻羅王','不收錢','重大勳功','畫上等號'],
'originalChecked':{'images':['site/dist/assets/questions/q-496-reading-source-623fb37cd3.jpg','site/dist/assets/questions/q-496-source-a4d1aa7319.jpg'],'visualChecked':True,'answer':'C','notes':'親見閱微原全段與40四項，避嫌疑不言/畏煩重不舉/木偶連水不飲為譏諷，原C判讀沿用；不把自稱清廉當盡責證據、不增實際懲罰。'},
'sourceUrl':'https://share.gemini.google/4TSQakuIUwvo','answerCheckedAgainst':'原文具體不言不舉與一身求自全對應C兩成語；MOE尸位素餐占職受俸不做事全文核。',
'references':[{'title':'教育部簡編辭典：尸位素餐','url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=33119&la=0&powerMode=0','supports':'占職受俸而不做事，對應本題不任事','access':'主文已讀，不引申為現行法律責任或所有無重大功績均有罪'}],
'rationale':'自稱不收錢、實際避責與木偶假設三景，將文中無功的語境與清廉區分；不把陰間寓言變成法律教學、實錄刑罰或沒有勳功皆定罪。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-496-generation.json','promptFile':'docs/comics/q-496-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'C','inactionEqualsNotTakingMoney':False,'allLackOfGreatAchievementsMeansGuilt':False,'dummyIsHypotheticalComparison':True,'currentLegalConclusion':False,'homicideOrBriberyAdded':False,'punishmentInvented':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-496.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
