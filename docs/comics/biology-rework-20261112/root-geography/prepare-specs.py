from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[4]
qs={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']};now=datetime.now(timezone.utc).isoformat()
D={
'q-096':{
 'title':'找出西安，再判斷西部經濟帶',
 'rows':[
 ['① 先找陸上經濟帶起點','先區分陸上的一帶與海上的一路。本題問陸上經濟帶起點，原圖甲對應西安；新圖箭頭只示陸上向西的方向，不畫完整路線。','新製定位圖：箭頭表示陸上方向，不是完整路線或行程。','歐亞大陸地圖標出內陸西安，紅箭頭向西延伸在陸地上，下方另標海洋。'],
 ['② 西安位在陝西','把範圍縮到中國，金色區域是陝西，紅點是西安。依本題經濟區域分類，陝西屬西部地區，因此起點城市符合B。','金色只標陝西，不把它誤當成整個西部地區。','中國及周邊定位圖中標示陝西輪廓與西安位置，沒有塗出未核對的完整經濟帶邊界。'],
 ['③ 內陸城市，不是沿海港口','第三圖分開西安、北京與上海的位置。西安在內陸；首都北京與沿海的上海不是同一座城市，不能把其他城市的特色移到西安。','比較城市位置，不推論港口最新排名。','地圖以紅點西安、綠點北京與藍點上海表示相對位置，西安在內陸而上海臨海。']
 ],
 'answer':'答案 B：位於西部經濟帶',
 'points':['西安在陝西，陝西歸西部地區。','北京是首都；西安是內陸城市，不是沿海港口，也不在熱帶。','原卷閱讀材料的合作情形照留，本題依起點城市與位置判斷。'],
 'fourthAlt':'放大陝西輪廓，西安紅點位於其中，總結西安隸屬陝西並屬西部地區，不把陝西當成整個西部。',
 'sources':[{'url':'https://www.stats.gov.cn/hd/lyzx/zxgk/202405/t20240524_1953711.html','support':'官方統計區域分類將陝西列為西部地區；全文實讀。'}],
 'checks':['實開完整題幹/四選項、閱讀裁圖與原附圖，原B保持','第一圖陸上箭頭只表示概略向西，不另造完整絲路或海路端點','陝西實際輪廓與西安/北京/上海點位使用固定版本Natural Earth資料，來源及SHA保存','只標陝西，未將陝西當作全西部邊界；未推論港口最新排名','保持原卷合作情形的歷史時點，不改正式題幹/答案/閱讀材料']},
'q-143':{
 'title':'本州中部日本海側，定位石川縣',
 'rows':[
 ['① 先找本州','題幹指定本州島。第一圖將本州以金色標出，與北海道、四國和九州分開，所以九州附近的甲不合。','本州用金色，其他島嶼保留淡色，先縮小大範圍。','日本主要島嶼輪廓圖，本州金色，北海道、四國與九州各有位置標示。'],
 ['② 再分日本海與太平洋側','日本海位在日本列島面向亞洲大陸的一側。本題說臨日本海，應找本州日本海側，不能只看同在本州就選太平洋側的丁。','先辨海域兩側；圈只指向後續討論地區。','日本海在本州面向亞洲大陸一側，太平洋在另一側，圈出本州中部日本海側。'],
 ['③ 放大石川縣與能登半島','石川縣位於本州中部日本海沿岸，能登半島向日本海突出。把題幹三個定位線索合起來，可對照原圖丙。','圈是能登地區定位，不是精測震央；石川縣以引線指向沿岸。','能登半島海岸線放大圖，能登地區用圓圈定位，石川縣文字以引線連到沿岸，非完整縣界或震央測量圖。']
 ],
 'answer':'答案 C：丙',
 'points':['本州中部＋日本海側＋石川縣，對應丙。','甲在九州附近，乙不在題述石川縣能登位置，丁在太平洋側。','四點依原圖作相對位置示意；年份與規模依原題保留，不新增精測震央座標。'],
 'fourthAlt':'日本地圖四點甲乙丙丁的相對位置比較，丙以紅點和圈標在本州中部日本海側；四點不是精測震央座標。',
 'sources':[{'url':'https://www.jma.go.jp/jma/kishou/books/hakusho/2024/index2.html','support':'日本氣象廳記載2024年能登地區M7.6事件與日本海側海嘯；全文實讀。'},{'url':'https://www.jishin.go.jp/main/chousa/24feb_noto/index-e.htm','support':'地震本部公開能登石川地區地震評估，未採為新圖精確震央點位。'}],
 'checks':['實開完整原卷與日本四點附圖，保留已核對C、原學生D與全選項','金色本州實際幾何與北海道/四國/九州區分正確','日本海朝向亞洲大陸，太平洋在另一側，未畫成東西倒置','能登海岸10m底圖實看；石川縣標籤補引線，避免看成鄰縣或精確縣界','四點是原圖相對位置的概略比照，乙修至本州西部附近，不作精測震央','原題芮氏用語/2024/7.6照留，本次純圖解美術升級不重開同一答案']}}
for qid,c in D.items():
 q=qs[qid];d=R/'docs/comics/biology-rework-20261112'/qid;p=R/f'docs/comics/{qid}.json'
 if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
 r={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{qid}/panel-{i}.png' for i in range(1,5)],'checks':c['checks']}
 s={'id':qid,'subject':'Geography','title':c['title'],'art':f'docs/comics/art/{qid}-four-image-v2-panel-1.svg','panels':[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.svg') for i,v in enumerate(c['rows'],1)],'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.svg','alt':c['fourthAlt']},'protectedWords':['西部經濟帶','西安','陝西','日本海','太平洋','本州中部','能登半島','石川縣'],'generationMethod':'four authored native SVG locator maps based on pinned Natural Earth data','generatorFile':'docs/comics/biology-rework-20261112/root-geography/generate.py','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']]+['site/dist/'+x['src'] for x in q['questionFigures']],'answerCheckedAgainst':q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'四張實際地圖從廣域、海陸/省份、區域到答案定位分步呈現。原題與必要原地圖保留，新增圖明示輔助，不讓imagegen猜海岸/路線/城市位置。','sources':c['sources']+[{'url':'https://www.naturalearthdata.com/about/terms-of-use/','support':'公開領域底圖，固定版本資料與SHA見map-data-provenance.json。'}],'mapDataProvenance':'docs/comics/biology-rework-20261112/root-geography/map-data-provenance.json','createdAt':now,'visualChecked':True,'productionReview':r}
 p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(d/'sources.json').write_text(json.dumps(s['sources'],ensure_ascii=False,indent=2)+'\n')
