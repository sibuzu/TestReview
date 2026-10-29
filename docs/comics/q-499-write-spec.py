from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-499.png');d={'id':'q-499','subject':'Chinese','title':'得下之情：先察知人民需求與實情','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 得下之情，是掌握百姓的實情','text':'上指在上位的為政者，下指百姓，情是實際情況。得下之情，就是了解民情；不是要百姓取得官員的好感。用現代例子想：先聽居民反映困難，才能知道他們需要什麼。','alt':'全新內建一般社區工作者在樹蔭長椅聽成年長者反映需求，現代類比例子非古文實際人物或事件。'},
{'heading':'② 原句強調：了解民情有助於治理','text':'原句用得民情則治、不得民情則亂的對比，凸顯掌握實情的重要。查看居民說的狀況、釐清問題，正是在「察」；重點不是一開始就禁止或處罰民眾。','alt':'全新內建同一現代工作者與成人居民安全查看一般步道不平或積水，記錄實際問題，無法令情節或災難傷害。'},
{'heading':'③ B的察，最直接對應了解民情','text':'民之所欲，為官必察，意思是百姓的需求，為官者必須察知。A強調禁，C強調罰，D強調謀，都不如B的察直接呼應原句。插畫是輔助理解的現代例子，不是原文記載。','alt':'全新內建一般公共服務工作者與成人同事整理空白資料、比較需求，沒有政治人物國旗選舉或保證成效的文字。'}],
'fourth':{'answer':'答案 B：民之所欲，為官必察','points':['情是民情與實情，不是討取上位者好感。','得下之情，對應察知百姓需求。','比較禁、察、罰、謀，選最接近原句的核心動作。']},
'protectedWords':['得下之情','民情','實情','為政者','得民情則治','不得民情則亂','民之所欲','為官必察','察知','百姓需求'],
'originalChecked':{'images':['site/dist/assets/questions/q-499-source-c64663f64f.jpg'],'visualChecked':True,'answer':'B','notes':'親見原16完整引句及四項樂禁/欲察/惡罰/為謀，學生B與原答一致；四選核心動作獨立對比，無原文修改。'},
'sourceUrl':'https://share.gemini.google/1P48K0fgDy6p','answerCheckedAgainst':'原引句得下之情/不得下之情對治亂，四項B民欲必察最直接同義；不新增未提供作者與實際政策條文。',
'rationale':'用聆聽、查看、整理實情三個一般現代類比讓察知民情具體化，避免把情誤作好感，或將原句當作對任何人民欲望立即照單全收；不杜撰古代事件。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-499-generation.json','promptFile':'docs/comics/q-499-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'B','modernExamplesNotOriginalEvents':True,'specificLawAdded':False,'realPoliticianDepicted':False,'guaranteedPolicyOutcome':False,'emotionMeansOfficialFavor':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-499.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
