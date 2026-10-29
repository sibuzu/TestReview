from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-819.png');d={'id':'q-819','subject':'Chinese','title':'白龍的處境，對應吳王想微服涉險','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 白龍原本尊貴，卻自己化成魚','text':'白龍原是天帝貴畜，卻下到水中化為魚。比喻的關鍵不是誰地位最高，而是尊貴者改換身分，讓自己處在可能受傷害的情境；這條處境線索才對應吳王。','alt':'全新內建傳統白色中國龍在清澈池畔的寓言場景，非真實動物照、無西方翼龍或傷人，不另加天帝出場。'},
{'heading':'② 化魚遭射，說明改換身分的風險','text':'故事中白龍以魚形被射中眼睛，上訴時天帝反問豫且何罪。漁者是造成傷害的角色，天帝是聽訴判斷的角色；兩者都不是被拿來對應吳王處境的主角。','alt':'全新內建白色普通魚在水中的化魚示意，遭射眼睛僅由HTML忠實交代，不畫血傷、射擊動作、網捕或處刑。'},
{'heading':'③ 吳王欲棄尊位，伍子胥用白龍勸止','text':'吳王原有萬乘之位，卻打算與布衣飲酒，伍子胥擔心他遇到如豫且般的傷害者。尊貴、改換身分、可能涉險，與白龍一線相應。原文王乃止，是聽諫停止，並非已飲酒遇害。','alt':'全新內建陸上宮室中成人吳王聽年長伍子胥勸諫的情境，無平民飲酒會、實際微服受傷或天庭神判。'}],
'fourth':{'answer':'答案 A：白龍比喻吳王','points':['對比的是處境：尊貴者降低身分而可能涉險。','天帝雖地位高，敘事功能仍不是吳王的喻體。','布衣是吳王想與之飲酒的平民，不是吳王的喻體。']},
'protectedWords':['白龍','吳王','伍子胥','天帝','貴畜','豫且','漁者','布衣','萬乘之位','身分','處境','比喻','喻體','王乃止','改換身分','可能涉險','上訴','眼睛','飲酒遇害'],
'originalChecked':{'images':['site/dist/assets/questions/q-819-source-1.jpg','site/dist/assets/questions/q-819-source-2.jpg'],'visualChecked':True,'answer':'A','notes':'親見共同全文與41四項、紅改A。白龍化魚遇射→吳王棄尊位飲酒可能有患，王乃止不作已飲酒傷亡；天帝角色功能不同，A沿用。'},
'sourceUrl':'https://gemini.google.com/share/ec6c955b81b3','answerCheckedAgainst':'原卷夫白龍天帝貴畜/今棄萬乘之位而從布衣飲酒及王乃止，相同處境對應白龍與王，非僅身份排名；A不變。',
'rationale':'白龍、魚形與吳王聽諫三情境構成比喻線；不以最高位天帝硬配君王，不把尚未實行的飲酒與警告變成已遇害，也不添加血傷。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-819-generation.json','promptFile':'docs/comics/q-819-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'A','whiteDragonMapsToKing':True,'heavenlyEmperorMapsToKing':False,'fisherMapsToKing':False,'kingActuallyWentDrinkingOrWasHurt':False,'dragonAndFishAreSeparateFightingAnimals':False,'modernLegalConclusionAdded':False,'visibleEyeInjuryShown':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-819.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
