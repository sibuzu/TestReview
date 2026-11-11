from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[4];d=Path(__file__).parent;qid='q-921';p=R/f'docs/comics/{qid}.json'
if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
q=next(q for q in json.loads((R/'site/dist/data.json').read_text())['questions'] if q['id']==qid)
rows=[
['① 未來旅行，需要先換錢','John即將去美國旅行。先看原句的目的鏈：為了準備旅行，他必須去銀行換些錢；旅行仍是計畫，不是已經完成。','在家準備行李是旅行計畫的輔助情境，沒有出發日期。','John在家看空白旅行資料與打開的行李箱，旁有地球儀和模型飛機，沒有已完成旅行或金額。'],
['② to the bank交代去哪裡','go to the bank表示去銀行。這個to是介系詞，後接地點名詞the bank，回答去哪裡，尚未交代去做什麼。','走向銀行的畫面對應目的地，不是換錢目的本身。','John沿人行道走向無字銀行建築，尚未到兌換櫃台，沒有地名或匯率。'],
['③ to change交代去的目的','去銀行做什麼？為了換錢，用to＋原形動詞：to change some money。原題bank後不能直接接change或changing來表這個目的。','換錢是去銀行的目的；紙鈔無面額，不表示實際換匯數字。','John與銀行服務人員討論換錢，兩色無字紙鈔分置櫃台兩側，無匯率或已完成交易數據。']]
now=datetime.now(timezone.utc).isoformat()
r={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{qid}/contact.png',f'docs/comics/art/{qid}-four-image-v2-panel-1.png'],'checks':['實開原卷核對原C to change及全部選項與藍B紅C筆跡','三個to分別has to go、to the bank、to change不混淆，不把to一律當目的','並列共用has to時用go...and change，非and changes','第一圖首稿冒出旅遊拼貼與具體美鈔面額，已imagegen移除整個泡泡並實看','不補出發日/換匯額/匯率/旅行城市；銀行情境解釋意圖，並非證明已完成交易']}
s={'id':qid,'subject':'English','title':'去哪裡，與為了做什麼','art':f'docs/comics/art/{qid}-four-image-v2-panel-1.png','panels':[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.png') for i,v in enumerate(rows,1)],'fourth':{'answer':'答案 C：to change','points':['He has to go to the bank to change some money.','to the bank是目的地；to change是為了換錢。','共用has to並列動作時，go與change都用原形，不能填and changes。'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.png','alt':'John拿錢包與銀行人員討論換匯，無字紙鈔與模型飛機鑰匙圈連結未來旅行計畫和換錢目的。'},'protectedWords':['to the bank','to change','some money','has to go','and changes','changing'],'generationMethod':'built-in image_gen: four independent detailed colour anime teaching illustrations','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']],'answerCheckedAgainst':q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'四張獨立情境圖依序分開未來旅行、銀行目的地、換錢目的及整句整合；精確句型用文字，不在插畫補金額或時程。保留原題與既有to追問完整解說。','createdAt':now,'visualChecked':True,'productionReview':r}
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
