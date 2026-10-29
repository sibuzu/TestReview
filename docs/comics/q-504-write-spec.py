from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-504.png');d={'id':'q-504','subject':'Chinese','title':'訪賢未遇、回望臥龍岡，對應三顧草廬','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 訪賢良，卻不遇空回','text':'冒著風雪拜訪有才德的人，卻沒有遇見，只能失望返回。先抓住「求賢」與「撲空」兩個動作，便能排除赴宴、戰事或弔喪的情節。三格是同次詩境，不各代表一次拜訪。','alt':'全新內建小說概念動漫成人古裝旅人騎馬到雪中草廬、無主人現身，非史實建築復原或三次拜訪次數圖。'},
{'heading':'② 梨花與柳絮，都是在比喻雪','text':'溪橋結凍、山石濕滑，寒氣侵入鞍馬，寫路途艱辛。接著用梨花、柳絮比喻紛飛的白雪，不是說當時春花盛開；讀景物要和整首的風雪寒意連在一起。','alt':'全新內建同一成人旅人騎馬行過冰雪石橋，白雪飛舞，沒有春日梨花柳樹、沒有馬車，不用花瓣取代雪。'},
{'heading':'③ 臥龍岡，指向延攬諸葛亮的故事','text':'停鞭回首，看見白雪堆滿臥龍岡，再和前面的訪賢未遇合看，指向劉備延攬諸葛亮。C的三顧草廬是整段求賢故事的名稱，不能因為詩中撲空，就說這一定是第三次。','alt':'全新內建同一小說旅人停馬回頭遙望覆雪山岡與遠處草廬，沒有與諸葛亮見面的畫面，也不把爛銀畫成金屬。'}],
'fourth':{'answer':'答案 C：司馬徽再薦名士　劉玄德三顧草廬','points':['訪賢良、不遇空回：求賢而撲空。','臥龍岡：連到劉備延攬諸葛亮的故事。','梨花與柳絮寫雪；不把三顧誤解成詩中一定第三訪。']},
'protectedWords':['訪賢良','求賢','撲空','不遇空回','臥龍岡','劉備','諸葛亮','司馬徽再薦名士','劉玄德三顧草廬','三顧草廬','梨花','柳絮'],
'originalChecked':{'images':['site/dist/assets/questions/q-504-source-1f48807f48.jpg'],'visualChecked':True,'answer':'C','notes':'親見完整八句詩及全部回目四項、原註凍合/爛銀；不遇非不過、鞍馬停鞭非馬車，原紅C。'},
'sourceUrl':'https://share.gemini.google/PayZ1lfF9trh','answerCheckedAgainst':'原紅C、詩中訪賢不遇與臥龍岡；另實讀Gutenberg原小說第三十七回詩前後及三十八回開首兩次不遇，以原題為準不改原詩。',
'references':[{'title':'Project Gutenberg：三國志演義','url':'https://www.gutenberg.org/cache/epub/23950/pg23950.html','supports':'第三十七回題名、風雪訪孔明詩與第三十八回兩次不遇的前後文','access':'web原典與Python官方電子書實讀完整詩前後及回目，古典公版文本'}],
'rationale':'以詩中同次騎馬風雪訪賢至回望的三個視角連結故事線索，不虛構孔明已見面、不把三張畫當三訪或誤畫春花馬車。原詩與註釋皆保留。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-504-generation.json','promptFile':'docs/comics/q-504-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'C','oneSnowyVisitAcrossScenes':True,'impliesThirdVisitInPoem':False,'literalPearBlossomsOrWillowCatkins':False,'horseNotCarriage':True,'hostPresent':False,'historicalDocumentaryPortrait':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-504.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
