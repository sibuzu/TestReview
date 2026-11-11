from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];Q={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']};now=datetime.now(timezone.utc).isoformat()
D={
'q-437':{'title':'先批評、再肯定、又批評：抑揚抑','rows':[
 ['① 智短勇不足是抑','惟智短而勇不足，指出才智與勇氣的不足，是蘇轍在題文中的批評，所以第一空填抑。','猶疑的領袖情境只聯想評語，不是某場戰役史實或真實肖像。','成年古代領袖在空白規劃圖前思索，未畫實際戰役、勝敗或地名。'],
 ['② 近似高祖是揚','近似於高祖，以及三國之君獨有劉備近之，是以肯定為主的比較。未至仍保留限制，但第二空整體是揚。','比較情境不表示才智完全相等；近之而未至的限制照留。','匿名讀者比較兩份空白卷軸，上方兩個不同領袖形象表示比較，不是有數值的能力量尺。'],
 ['③ 翹然自喜又轉為抑','翹然自喜之心是在批評自負、自滿，不是單純稱讚開心，所以第三空回到抑。','自滿神態是文意聯想，不補出原文未提的史事或人物衝突。','古代領袖微仰頭、抱臂而略自滿，旁有閉合卷軸，沒有新增臣子被迫害或特定戰役。']
 ],'answer':'答案 A：抑、揚、抑','points':['智短勇不足 → 批評 → 抑。','近似高祖、獨有劉備近之 → 肯定 → 揚。','翹然自喜 → 批評自滿 → 抑，按原選項對應A。'],'alt4':'匿名古文讀者在桌上按順序比對三張空白紙，連結逐段評價與選項，不是劉備或蘇轍的寫實肖像。','protected':['智短勇不足','近似於高祖','翹然自喜','抑、揚、抑','近之而未至'],'checks':['實開原卷全文/全部選項，蘇轍及呂祖謙原材料不改，A與原學生C紅A保持','逐段判抑/揚/抑，再對原選項A，未照抄原AI錯誤字母C','第二段未至限制保留，不畫成完全等同高祖','插畫是匿名文意聯想，不新增戰役、年表或真實人物肖像','第四圖仍為獨立新圖，三紙順序不替代可核對的精確原文']},
'q-601':{'title':'抓深於與非一端，讀出作者的比較','rows':[
 ['① 深於是比它更深','其源深於女禍也，於在這裡引出比較。題文比較兩種危害，重點是作者認為宦官亂國之害更深，而非兩者只是並列。','匿名讀者比較文意，不是對所有人物群體下概括評價。','古文讀者在空白書頁兩欄之間思考，沒有新增宮廷事件或人物因果。'],
 ['② 非一端是不只一面','女，色而已；宦者之害，非一端也。後句再次強調宦官之害不只一個方面，呼應前面的深於比較。','器物只聯想一端與多端，不是危害數量、程度或價值的測量。','單一花飾盒與多份卷宗、印章分開擺置，作一面/多面之比喻，未標示數量比或新增害處類型。'],
 ['③ 原文沒說宦官引誘君主','B自行補出宦官設計使君主沉迷女色的因果，原文沒有這樣說；A也沒抓到比較高下，D則把比較方向倒過來。','宮廷職務情境不補原文未列的陰謀或具體史事。','匿名成年宮廷侍從站在卷宗架與關閉宮門旁，沒有女性誘惑、行賄、操控君主或其他新增情節。']
 ],'answer':'答案 C：宦官亂國之害更深','points':['深於：比它更深；非一端：不只一方面。','兩句共同突出作者對宦官亂國危害的比較論點。','依節錄文字作答，不補未節錄的歷史事例或選項B的因果。'],'alt4':'匿名讀者核對比較稿與兩冊書，分開的花飾盒和卷宗只幫助概念聯想，最後結論以本文比較句為準。','protected':['深於','非一端','宦官亂國','比較','女禍'],'checks':['實開原卷短文及全部四選項，歐陽脩原文保持，C與原學生B紅C保留','深於作比較、非一端作多面，沒有把原文讀成並列或反向比較','圖與文均不造宦官導致君主沉迷女色的B因果','不新增具體亂政史事，不把作者本段論點當現代族群/性別通則','四圖是獨立閱讀/物件比喻/宮廷角色/整合聯想，精確論點用文字']}}
for qid,c in D.items():
 q=Q[qid];d=R/'docs/comics/biology-rework-20261112'/qid;p=R/f'docs/comics/{qid}.json'
 if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
 rev={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{qid}/contact.png'],'checks':c['checks']}
 spec={'id':qid,'subject':'Chinese','title':c['title'],'art':f'docs/comics/art/{qid}-four-image-v2-panel-1.png','panels':[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.png') for i,v in enumerate(c['rows'],1)],'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.png','alt':c['alt4']},'protectedWords':c['protected'],'generationMethod':'built-in image_gen: four independent detailed literary teaching illustrations; exact source evaluation remains selectable text','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']],'answerCheckedAgainst':q['passage']+'\n'+q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'使用者核准missing_illustration補作；僅按完整原卷的抑揚/比較判讀，四張新圖不冒充歷史肖像或增加原文未列的史事。','createdAt':now,'visualChecked':True,'productionReview':rev}
 p.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(rev,ensure_ascii=False,indent=2)+'\n')
