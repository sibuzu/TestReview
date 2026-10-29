from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-492-v2.png');d={'id':'q-492','subject':'Chinese','title':'語境、關聯詞與意外語氣，合看選D','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 老店談口味，應說光顧或消費','text':'A前面談飲食老店的獨特口味，後面卻用諮商，和情境不合。諮商通常用在心理輔導或專業諮詢；這裡的客人是來吃東西或消費，改成光顧更合適。原題仍保留諮商供辨讀。','alt':'全新內建一般老店成人客人用餐、店家端食物，沒有把店家畫成心理諮詢室或把原題錯詞合入圖片。'},
{'heading':'② 勸大家再給機會，用不妨較自然','text':'C是在勸大家考慮再給一次機會，用不妨更自然。不吝常見於不吝指教、不吝賜教等客套說法，和此處勸人採取做法的語氣不同。依本題比較不選C，保留原題不吝，不擅改字。','alt':'全新內建兩位成人朋友在公園誠懇道歉、考慮和解的一般語境，不吝與不妨的精確比較由HTML列，不重開使用者已確認D。'},
{'heading':'③ 竟然寫出乎意料，放在D語意通順','text':'放棄令人稱羨的高薪工作去遊學，可能使旁人意外，因此竟然能表達這個語氣。毅然強調決斷，竟然強調意外；本句不必硬把竟然改成毅然，選D。','alt':'全新內建成年上班族在家收拾書與行李準備遊學，成人友人微驚而支持，呈現旁人意外語氣，不給薪資數字或真實目的國。'}],
'fourth':{'answer':'答案 D：竟然放棄高薪工作去遊學','points':['A諮商不合老店用餐情境，光顧較合適。','B雖然應接轉折，固然不能在此代替但是。','C不妨較自然；D竟然能表達出乎意料。']},
'protectedWords':['諮商','心理輔導','專業諮詢','光顧','不妨','不吝','不吝指教','不吝賜教','竟然','毅然','出乎意料','高薪工作','遊學','固然','但是'],
'originalChecked':{'images':['site/dist/assets/questions/q-492-source-5d6d00e0ff.jpg'],'visualChecked':True,'answer':'D','notes':'親見2題最通順正確及全部四句，原卷C為不吝、D為竟然。遵使用者明確D與C不吝/不妨語氣解釋、D不必改毅然，不重開既有結案。'},
'sourceUrl':'https://share.gemini.google/4TSQakuIUwvo','answerCheckedAgainst':'使用者已確認D與逐項解說；原圖四句逐字比對，原字不吝及竟然保留。',
'rationale':'以老店用餐、給機會、意外遊學三情境對照詞語使用條件，第四格補B關聯詞，保留原題與使用者已定答案和解說，不將語氣比較升格成所有用法一律不合法。',
'sourceAIUsed':False,'generationCalls':2,'generationMetadata':'docs/comics/q-492-generation.json','promptFile':'docs/comics/q-492-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'D','userConfirmedAnswerReopened':False,'originalCChangedToBufang':False,'jingranForcedToYiran':False,'allBulinUsesDeclaredInvalid':False,'realPersonOrSalaryInvented':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-492.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
