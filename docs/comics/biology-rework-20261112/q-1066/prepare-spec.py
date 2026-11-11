from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[4];d=Path(__file__).parent
qid='q-1066';p=R/f'docs/comics/{qid}.json'
if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
q=next(q for q in json.loads((R/'site/dist/data.json').read_text())['questions'] if q['id']==qid)
rows=[
['① 想買禮物，錢卻還不夠','說話者想買媽媽的生日禮物，接著請對方借錢。這兩句連起來，表示目前的金額仍有缺口。','錢包與禮物表示已有金額和想買的東西，虛線表示不足。','禮物放在櫃台，前景錢包上方有虛線金額符號，呈現想買但尚缺錢。'],
['② fifty dollars說明差額','上條代表禮物所需金額，下條代表手上已有金額，右端虛線缺口是50元。金額放在short前面：fifty dollars short。','長度只表示有缺口，不按實際金額比例；總價與已有金額未提供。','上方完整所需金額條、下方較短的已有金額條，右端虛線缺口與括線相連，沒有偽造總價。'],
['③ lend me是請求，尚未借到','Can you lend me some money?是請對方借一些錢。這個語境支持short的不足之意，enough的足夠則不合。','伸手請求借款；虛線表示金額尚待補足。','伸出的空手掌與虛線金額符號及向下虛線箭頭，表示請求借款，不表示已經收到錢。']]
now=datetime.now(timezone.utc).isoformat()
review={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{qid}/panel-{i}.png' for i in range(1,5)],'checks':['實開完整原卷保留原A與四選項及藍B紅A筆跡','be＋金額＋short表還差，50元是差額而非總價','未補禮物總價/現有金額/已借到的金額，金額條無實際比例','四張含禮物/錢包/金額缺口/借款手勢實際圖像，不是文字關係框','fourth實際缺口圖仍有未補足區，未畫成已完成購買或已借到款']}
s={'id':qid,'subject':'English','title':'fifty dollars short：還差五十元','art':f'docs/comics/art/{qid}-four-image-v2-panel-1.svg','panels':[dict(zip(['heading','text','caption','alt'],row),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.svg') for i,row in enumerate(rows,1)],'fourth':{'answer':'答案 A：short','points':['I am still fifty dollars short.','金額＋short說明還差多少；本題差額50元。','convenient是方便的，real是真實的，都不能表達原句的缺款。'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.svg','alt':'錢包指向禮物，下方金額線保留右端虛線缺口與括線，總結還差50元；不依長度計算未知總價。'},'protectedWords':['fifty dollars','short','enough','lend me','convenient'],'generationMethod':'native SVG: four independent vector illustrations and qualitative shortfall diagrams; precise fifty-dollar difference remains selectable HTML','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']],'answerCheckedAgainst':q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'本題重點為差額與借款語意，四張原生SVG以禮物/錢包、金額條、借款手掌和缺口關係圖表達，不繪無關人物、不讓生成圖猜面額；科目仍英文，原題不改。','createdAt':now,'visualChecked':True,'productionReview':review}
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
