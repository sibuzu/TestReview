import json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3]
qs={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']}
now=datetime.now(timezone.utc).isoformat()
data={
'q-750':{
 'title':'過去問句用did，後面do維持原形',
 'panels':[
 ['① 問的是上週六','last Saturday表示上週六，Jessie詢問Gloria那時做了什麼，不是現在習慣或此刻正在做的事。','Jessie與Adam回想Gloria上週六的活動。','Jessie詢問Adam，上方回憶泡泡呈現不同人物Gloria游泳。'],
 ['② went也指向過去','Adam回答She went swimming.，went是go的過去式，和last Saturday的過去時間一致。','游泳動作是回想中的過去活動，不是未來安排。','Gloria獨自在泳池泳道游泳，與對話場景分開呈現，沒有比賽或時刻。'],
 ['③ did後用原形do','過去式的一般動作問句用did＋主詞＋原形動詞。題幹已有do，所以空格填did，不能用was直接接do。','空白行事曆幫助回想過去，沒有新增實際日期。','Adam指向空白行事曆回答，回憶中Gloria在泳池旁拿毛巾；只有兩名對話者在現場。']
 ],
 'answer':'答案 C：did',
 'points':['What did Gloria do last Saturday?','She went swimming.','問句did承擔過去式；後面的do保留原形。does表現在，is或was不能直接構成本題do問句。'],
 'fourthAlt':'回想中的Gloria拿著毛巾離開泳池畔，總結上週六去游泳的活動；不新增時間或地點條件。',
 'protected':['last Saturday','went swimming','did','do'],
 'checks':['實開原卷核對C did與全部四選項','last Saturday與回答went雙重過去線索保持','不將did後do改成過去式','第2圖首稿過度重複對話拼圖，已重製成單獨游泳場景並實看','泳池環境與毛巾為輔助情境，不推論精確日曆日期或比賽']},
'q-751':{
 'title':'sang已是過去，配今天早上已發生的活動',
 'panels':[
 ['① sang是sing的過去式','Henry sang some English songs in class. 已把唱歌動作用過去式敘述，選項的時間要配合這個語意。','教室唱歌是輔助情境，沒有新增歌曲名稱。','Henry在教室前唱歌，同學坐著聆聽，書本沒有可讀歌詞。'],
 ['② 今天早上也可以是過去','this morning可指今天早上已經發生的事。例如稍晚回想早上的課堂，就能用sang描述。稍晚是理解用的例子，不是原題額外條件。','同一天稍晚回想早上，是說明用的可能情境。','Henry坐在教室座位回想早上唱歌，同一人物只在回憶泡泡中再次出現，非兩名Henry。'],
 ['③ 比較其他時間詞','now通常指現在，next Monday指未來；都不合本題已發生的sang情境。every weekend可配過去習慣，但本題沒有另給那種背景。','唱歌後的教室情境；不把週末習慣說成只能用現在式。','課堂唱歌後同學交談，前景空白活動卡和麥克風，無日期或鐘點。']
 ],
 'answer':'教材預期 C：this morning',
 'points':['Henry sang some English songs in class this morning.','sang與已經過去的今天早上相配。','若另有過去習慣背景，every weekend也能搭過去式；保留這項限制，不說D永遠不合法。'],
 'fourthAlt':'Henry和同學交談，上方泡泡回想今天早上的課堂唱歌，用同日稍晚作理解範例，不新增原題事實。',
 'protected':['this morning','every weekend','next Monday','sang','sing'],
 'checks':['實開原卷核對教材預期C與四選項','sang與sing不規則變化核對','稍晚回想是示例，不把原題未明時間新增成題幹事實','保留every weekend可搭過去習慣，不誤教一律現在式','四圖不同構圖，沒有虛構歌曲名/確切鐘點']}}
for qid,c in data.items():
 d=R/'docs/comics/biology-rework-20261112'/qid
 p=[]
 for i,v in enumerate(c['panels'],1):
  p.append(dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.png'))
 review={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[str(d.relative_to(R)/'contact.png')]+([f'docs/comics/art/{qid}-four-image-v2-panel-2.png'] if qid=='q-750' else []),'checks':c['checks']}
 spec={'id':qid,'subject':'English','title':c['title'],'art':p[0]['image'],'panels':p,'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.png','alt':c['fourthAlt']},'protectedWords':c['protected'],'generationMethod':'built-in image_gen: four independent detailed colour anime teaching scenes','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in qs[qid]['images']],'answerCheckedAgainst':qs[qid]['question']+'\n'+qs[qid]['answer']+'\n'+qs[qid]['explanation'],'rationale':'實開原卷核對完整題目，維持教材預期與已說明的語境限制。四張不同情境圖用來辨識主詞、動作與時間，不增加原題條件。','createdAt':now,'visualChecked':True,'productionReview':review}
 (R/f'docs/comics/{qid}.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
 (d/'production-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
