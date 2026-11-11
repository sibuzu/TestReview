import json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3]
qs={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']}
now=datetime.now(timezone.utc).isoformat()
data={
'q-744':{
 'title':'Joe和Sue用they，will問句保留will',
 'panels':[
 ['① 先看未來的邀約','Ellen問Joe和Sue會不會來potluck。Will開頭詢問未來，後句It\'ll也延續尚未發生的聚會情境。','想像中的聚會是未來計畫，並非客人已經到場。','Ellen和Brian拿空白邀請卡討論，想像泡泡中出現未來聚會的Joe與Sue。'],
 ['② 兩人合稱they','Joe and Sue是兩個人，簡答用複數代名詞they代替，不用重複兩個名字。圖中的備餐只幫助認出這一對人物。','Joe與Sue一起準備餐點；兩人合稱they。','戴眼鏡穿鏽紅衣的Joe與穿紫衣的Sue一起準備分享餐點，和對話者明確區分。'],
 ['③ Yes後仍保留will','問句是Will Joe and Sue come...?，肯定簡答保留助動詞will：Yes, they will. 不能任意換成are、do或can。','Brian肯定回應未來計畫；現場只有兩名對話者。','Brian對Ellen比出肯定手勢，指向空白邀請卡；背景沒有Joe或Sue。']
 ],
 'answer':'答案 D：they will',
 'points':['Joe and Sue → they；Will問句 → 保留will。','Yes, they will. 表示他們會來。','can會改成能力或可能性的語意，無法直接保留原問句的will。'],
 'fourthAlt':'Ellen和Brian討論未來邀約，上方想像泡泡呈現四人在未來聚會相見，不是已發生事件。',
 'protected':['Joe and Sue','they will','It\'ll','potluck'],
 'checks':['完整保留原題D及四選項','will未來與It\'ll一致；they指兩人','第3圖首稿多出客人已移除，實看修訂圖恰兩位對話者','第4圖是明顯未來想像；備餐與場景為教學情境，非新增原題條件']},
'q-748':{
 'title':'昨晚的動作，read過去式拼法不變',
 'panels':[
 ['① last night定位在過去','Wendy問What did your brother do last night?，是詢問哥哥昨晚做了什麼。did與last night一起提示過去時間。','對話中的回想畫面指昨晚，沒有指定幾點。','Wendy詢問Bobby，回想泡泡呈現哥哥夜間看漫畫；不畫精確鐘點。'],
 ['② 回答做了什麼','He read some comic books. 用一般過去式直接敘述昨晚的動作，符合本題中性的問答。','哥哥在夜間閱讀漫畫，呈現過去做過的動作。','戴眼鏡穿深藍衣的哥哥在夜間燈下看漫畫，窗外是夜色。'],
 ['③ read拼法一樣，讀音不同','read的原形與過去式都寫read；過去式讀音像red。reads是現在式第三人稱單數，不能配合本題last night。','閱讀畫面相同，時態仍須靠句中時間與動詞形式判斷。','近看哥哥翻閱的漫畫與手部，圖中無可讀書名或自行指定的時刻。']
 ],
 'answer':'教材預期 A：read',
 'points':['He read some comic books.','did read可表強調或反駁，並非所有語境都不合法；此處不需特別強調。','was reading強調當時正在看；本題中性詢問做了什麼，預期用A直接回答。'],
 'fourthAlt':'Bobby回答Wendy，上方回想泡泡呈現哥哥昨晚看漫畫，總結教材預期一般過去式read。',
 'protected':['last night','did read','was reading','read','reads'],
 'checks':['保留原題教材預期A與全部選項','不將did read說成文法一律不合法','保留was reading的進行語意，不宣稱所有語境皆錯','哥哥與Bobby形象分開；昨晚只用夜色，不新增精確鐘點']}}
for qid,c in data.items():
 d=R/'docs/comics/biology-rework-20261112'/qid
 p=[]
 for i,v in enumerate(c['panels'],1):
  p.append(dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.png'))
 review={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[str(d.relative_to(R)/'contact.png')]+([f'docs/comics/art/{qid}-four-image-v2-panel-3.png'] if qid=='q-744' else []),'checks':c['checks']}
 spec={'id':qid,'subject':'English','title':c['title'],'art':p[0]['image'],'panels':p,'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.png','alt':c['fourthAlt']},'protectedWords':c['protected'],'generationMethod':'built-in image_gen: four independent detailed colour anime teaching scenes','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in qs[qid]['images']],'answerCheckedAgainst':qs[qid]['question']+'\n'+qs[qid]['answer']+'\n'+qs[qid]['explanation'],'rationale':'實開原卷核對完整題目，維持教材預期與已說明的語境限制。四張不同情境圖用來辨識主詞、動作與時間，不增加原題條件。','createdAt':now,'visualChecked':True,'productionReview':review}
 (R/f'docs/comics/{qid}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
 (d/'production-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
