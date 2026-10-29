from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-025.png');d={'id':'q-025','subject':'Chinese','title':'已恢復信心，不等於已贏下比賽','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 聽到點子，先發生的是心情轉變','text':'科學家朋友提出方法後，棋王露出難得的微笑、陰霾消散。文中先交代他恢復信心，認為有機會帶來轉機；並沒有在這裡交代一場比賽已經結束或已經贏了。','alt':'全新內建匿名成年棋手聽成年科學家朋友建議的情境，棋盤只是模糊背景、不構造合法棋局，不造作弊器材或未述技術方法。'},
{'heading':'② 微笑、陰霾消散，是現在的心理感受','text':'陰霾消散形容心中的憂慮減輕，不是指已收到勝利成績。微笑與希望可在比賽前出現，不能把有信心獲勝，直接換成已經大獲全勝。','alt':'全新內建同一棋手小幅放鬆微笑的內心轉變，無勝負告示、獎盃、實際頒獎或室內天氣雲霾。'},
{'heading':'③ 彷彿、下一次：勝利仍在想像裡','text':'彷彿看到下一次比賽後的歡呼，標示想像中的未來情景。D 說棋王想像勝利，符合文意；A 卻把它改成已經獲勝。題目問何者錯誤，所以要選 A，不能因 D 描述得對就選 D。','alt':'全新內建明顯淡色羽化夢境中棋手想像群眾鼓掌的未來場景；僅想像、非史實勝利照片或全人類已實際鼓掌，未畫獎盃或比分。'}],
'fourth':{'answer':'答案 A：已經大獲全勝，超出文意','points':['已發生：聽點子、微笑、恢復信心。','想像中：下一次比賽獲勝後的歡呼。','審題是何者錯誤，D 正確就不是本題答案。']},
'protectedWords':['棋王','科學家','恢復信心','微笑','陰霾消散','彷彿','下一次','比賽','已經','大獲全勝','獲勝','何者錯誤','想像','心理感受','文意','未來情景','勝利成績','轉機'],
'originalChecked':{'images':['site/dist/assets/questions/q-025-source-1-ff8d8c892d.jpg'],'visualChecked':True,'answer':'A','notes':'親見11題引文、何者錯誤、四項與學生D/紅改A。彷彿/下一次是未來想像，微笑不是已完成勝利；不以原小說之外的棋賽史補題。'},
'sourceUrl':'https://share.gemini.google/P5nF20mjzum8','answerCheckedAgainst':'原卷時態彷彿/下一次與A已經衝突，D正確不應選；B僅按文意恢復信心的轉機，不把實際勝率或比賽結果當已證實。',
'rationale':'聽點子→心理鬆動→未來想像三景，第三景羽化成夢境讓想像不冒充已發生。人物匿名，不宣稱是真實棋王比賽或可靠棋局教學；精確判讀放HTML。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-025-generation.json','promptFile':'docs/comics/q-025-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'A','asksForIncorrectStatement':True,'smileAlreadyHappened':True,'victoryAlreadyHappened':False,'applauseIsImaginedFuture':True,'DIsCorrectButNotChosen':True,'realMatchIdentityClaimed':False,'legalChessPositionClaimed':False,'scientificMethodOrCheatingInvented':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-025.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
