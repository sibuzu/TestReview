import json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3]
qs={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']}
now=datetime.now(timezone.utc).isoformat()
data={
'q-752':{
 'title':'last night問過去，Did後接原形go',
 'panels':[
 ['① 問的是昨晚','last night表示昨晚，是過去的時間。本句是在問Jenny有沒有一起去看電影，還沒有告訴我們她到底去了沒有。','想像昨晚的可能情境，不能當成已確認到場。','兩人討論昨晚可能的電影行程，上方想像泡泡是電影院，不代表肯定去過。'],
 ['② 人名不是選be的理由','Jenny雖是單數，仍要看句中動詞。本句主要動詞是原形go，不是形容詞或名詞，不能直接把Is放在前面。','先辨認Jenny，再看她後面的原形動詞go。','Jenny拿著手提包思考，泡泡中是空電影院座位；沒有票或肯定到場的結果。'],
 ['③ Did帶過去，go不變','一般動作的過去疑問句用Did＋主詞＋原形動詞。因此填Did，go維持原形，不用改成went。','討論仍是問句，沒有新增Jenny去了或沒去的答案。','問話者與對方討論，空白行事曆和帶問號的影院想像畫面提示未定的過去疑問。']
 ],
 'answer':'答案 B：Did',
 'points':['Did Jenny go to a movie with you last night?','Does是現在式，不合last night。','Is或Are不能在本句直接帶原形go；Are也不合Jenny單數。'],
 'fourthAlt':'對話者詢問昨晚的電影行程，上方Jenny站在影院外的畫面是可能情境，並未揭露肯定或否定簡答。',
 'protected':['last night','Did','Does','Jenny','go'],
 'checks':['實開原卷核對原B與四選項，保留學生A作答證據於原題收合區','未猜補Jenny實際去或沒去，所有影院畫面明示可能情境','Did承擔過去，go維持原形','不因Jenny是人或單數就用be；一般動作與時間線索共同判斷']},
'q-758':{
 'title':'回看當時，was searching表正在搜尋',
 'panels':[
 ['① 聚焦正在做的動作','本題把At that time理解為回看過去某個時刻，丈夫正在上網找資料。was searching把動作呈現為當時進行中。','正在操作電腦的片刻，不代表已經找到結果。','丈夫操作筆電查找資料，妻子在旁作輔助情境；畫面沒有指定搜尋主題或時間。'],
 ['② was＋V-ing','her husband是第三人稱單數。過去進行式用was＋searching，表達他當時正在搜尋；不是用現在的is searching。','近看操作中的電腦與雙手，強調搜尋尚在進行。','越肩近看丈夫鍵盤與觸控板操作，螢幕只有空白搜尋框與無字資料區塊，沒有假造查得結果。'],
 ['③ 當時不是死背口訣','At that time提供時間背景，並非一出現就只能用進行式。若只敘述過去發生的搜尋事件，searched也可成句。','回憶畫面區分過去與現在，不替原題指定時刻。','妻子在現在場景回想丈夫使用筆電，丈夫只在回憶泡泡中，沒有新增確切時刻。']
 ],
 'answer':'教材預期 B：was searching',
 'points':['At that time, her husband was searching for some information on the Internet.','本卷預期把過去某時的動作視為正在進行。','C searched另有可成立語境；不說At that time永遠排除一般過去式。'],
 'fourthAlt':'柔邊回憶中的書房，丈夫仍專注操作筆電查資料，總結過去當時正在搜尋，不呈現搜尋已完成。',
 'protected':['At that time','was searching','is searching','searched'],
 'checks':['實開原卷核對教材B與全部四選項','保留C searched可成句的語境限制，不把At that time誤教成強制口訣','was配合her husband單數，searching形態正確','四圖無精確鐘點/日期/搜尋主題/成功結果；妻子僅情境配角不當原題已給動作']}}
for qid,c in data.items():
 d=R/'docs/comics/biology-rework-20261112'/qid
 p=[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.png') for i,v in enumerate(c['panels'],1)]
 review={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[str(d.relative_to(R)/'contact.png')],'checks':c['checks']}
 spec={'id':qid,'subject':'English','title':c['title'],'art':p[0]['image'],'panels':p,'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.png','alt':c['fourthAlt']},'protectedWords':c['protected'],'generationMethod':'built-in image_gen: four independent detailed colour anime teaching scenes','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in qs[qid]['images']],'answerCheckedAgainst':qs[qid]['question']+'\n'+qs[qid]['answer']+'\n'+qs[qid]['explanation'],'rationale':'實開原卷核對完整題目，維持教材預期與已說明的語境限制。四張不同情境圖用來辨識主詞、動作與時間，不增加原題條件。','createdAt':now,'visualChecked':True,'productionReview':review}
 (R/f'docs/comics/{qid}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
