import json
from pathlib import Path
from datetime import datetime,timezone
R=Path('/home/jack/codex-git/TestReview');O=Path('/tmp/weirugo-ready-760-912');O.mkdir(exist_ok=True)
qs={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']};now=datetime.now(timezone.utc).isoformat()
data={
'q-760':{
 'title':'Who詢問身分，不由複數回答倒推問句',
 'panels':[
 ['① Who問正在跑的是誰','Who在本題作主詞，詢問那邊正在跑的是誰。一般不預設人數時，可用Who is running over there?，不先因後來的回答改判它錯。','先問身分，再辨認人物；插畫不是額外的人數條件。','Alex與Bruce看向遠處跑步者，詢問人物身分；沒有賽事或成績。'],
 ['② 回答可以列出多人','Ben and his friends是複數主詞，所以回答用are。Ben and his friends are.省略了前文已提過的running。','Ben與朋友們正在跑；朋友的實際人數不由插畫指定。','Ben穿綠色跑步衣與朋友慢跑，僅呈現被辨認者，沒有問話者在此近景。'],
 ['③ 問句和簡答分別判斷','問句的主詞是Who；簡答的主詞是Ben and his friends。不能只看到簡答are，就說原問句一定要用are或把is判錯。','近看兩人的問答，被辨認者在畫面之外。','Alex提出問題、Bruce指向畫面外回答，背景空步道，和跑者近景分開。']
 ],
 'answer':'教材預期 A：is running',
 'points':['Who is running over there? → Ben and his friends are.','若事先已知要問的是多人，Who are running...?也可能成立。','不把Who一概教成只能單數，也不把問句強制改成跟回答人數一致。'],
 'fourthAlt':'Bruce向Alex指出正在跑步的Ben與朋友們，總結一般Who問句可以得到複數人物回答。',
 'protected':['is running','are running','Who','running'],
 'checks':['實開原卷核對教材預期A及全部四選項','保持已知複數時C可成立的限制，不重開相同原AI訂正','不因Ben and his friends are回答複數就倒推A不合法','插畫朋友數僅示意，不增添原題人數；第2與3圖已imagegen修訂成跑者與對話者獨立近景並實看']},
'q-912':{
 'title':'It作主詞，cost接人與金額',
 'panels':[
 ['① 先看It、me與金額','It作形式主詞，真正的事情是後面的to buy those plates。中間接me與20 dollars，符合It cost＋人＋金錢＋to V。','買盤子的事情花了多少錢，不是只看中文「花費」。','盤子近景與購買情境，價籤空白，沒有偽造面額或價格。'],
 ['② 換成人，要改整句','可以說I spent 20 dollars on those plates，或I paid 20 dollars for those plates。這些是人作主詞的改寫，不能只把spent或paid塞回原句。','付款者可用I作主詞，spent搭on、paid搭for。','購買者把無面額的紙鈔交給店員，盤子在櫃台上，未把圖中紙鈔當金額證據。'],
 ['③ 分清金錢與時間','國中常見It took＋人＋時間＋to V用來問花多久。本題給20 dollars，是金額；保留It、me與原句排列，選cost。','沙漏表示時間，錢包表示金錢，不表示特定時長或面額。','獨立桌面靜物，左方沙漏、右方錢包和無字金屬圓幣，清楚區分時間與金錢。']
 ],
 'answer':'答案 A：cost',
 'points':['It only cost me 20 dollars to buy those plates.','後句were提示過去；cost過去式和原形拼法相同。','our old ones的ones代替複數plates；新盤子較不昂貴，舊盤子的實際價格未給。'],
 'fourthAlt':'上方購買盤子、下方回家拆包並與原有盤子對照；新舊價格差只按原句理解，不新增舊盤子金額。',
 'protected':['20 dollars','those plates','cost','spent','paid','took','ones'],
 'checks':['實開原卷核對A cost、It/me/20 dollars排列、were與原卷藍D紅A作答證據保持','不把花費動詞都當可直接代換，spend/pay人主詞與on/for核對','took以國中常見時間句型比較，不宣稱任何語境絕不能接金錢','精確20 dollars在文字，畫中無數字價籤/可讀面額/虛構舊價；沙漏不指定時長','第3首稿混入購買場景已imagegen重製成獨立靜物且實看']}}
for q,c in data.items():
 p=[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{q}-four-image-v2-panel-{i}.png') for i,v in enumerate(c['panels'],1)]
 r={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{q}/contact.png'],'checks':c['checks']}
 s={'id':q,'subject':'English','title':c['title'],'art':p[0]['image'],'panels':p,'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{q}-four-image-v2-panel-4.png','alt':c['fourthAlt']},'protectedWords':c['protected'],'generationMethod':'built-in image_gen: four independent detailed colour anime teaching scenes','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in qs[q]['images']],'answerCheckedAgainst':qs[q]['question']+'\n'+qs[q]['answer']+'\n'+qs[q]['explanation'],'rationale':'實開完整原卷並維持已確認教材答案與其他語境限制。四幅獨立圖分開呈現人物/事物/動作，精確句型與數量用可核對文字。','createdAt':now,'visualChecked':True,'productionReview':r}
 (O/(q+'.json')).write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print('Prepared unpublished specs outside Git while integration publication snapshot runs.')
