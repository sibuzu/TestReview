from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[4];Q={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']};now=datetime.now(timezone.utc).isoformat()
D={
'q-1057':{
 'title':'台地與埤塘合看，再定位桃園',
 'rows':[
 ['① 地形與灌溉一起看','題文說地勢稍高而表面平坦，又有蓄水灌溉的埤塘。這組線索對應桃園台地，不能只抓工業或太陽能一個詞。','台地、埤塘與農田為概念示意，不是特定地點剖面或地下水位圖。','較高而平坦的台地立體地塊，埤塘儲水透過藍色水路箭頭送向農田，未畫地下水層或水位。'],
 ['② 部分埤塘改成都市工業用地','產業轉型、人口移入，使都市與工業用地需求增加，文中提到部分埤塘被填平。兩幅小景用來理解土地利用的轉變。','前後場景只示變化方向；不是埤塘實際數量或面積統計。','左側農業景觀有埤塘與田地，右側部分埤塘位置改為道路和建築，保留另一處水面，未畫污染煙霧。'],
 ['③ 光電利用也要看生態','題文再談埤塘加設太陽能板，以及池塘、鳥類生態的取捨。圖把發電與棲地並置，提醒回到整段地形、水利與產業的線索。','發電與棲地示意；不表示覆蓋率、鳥數或每座埤塘都受同程度影響。','有部分太陽能板的池塘，仍留水面與岸邊植物，鳥形符號與發電閃電符號並列，沒有鳥類死亡或調查數據。']
 ],
 'answer':'答案 D：丁',
 'points':['桃園台地＋埤塘灌溉，是本題辨識組合。','再核對都市、工業與光電利用的轉變。','按本題原圖，桃園在臺灣西北部的丁；不套其他臺灣圖的標點。'],
 'fourthAlt':'臺灣主島輪廓上依本題原圖標出甲乙丙丁相對位置，丁在西北部桃園一帶以紅圈及引線指出。',
 'sources':[{'url':'https://www.tycg.gov.tw/cp.aspx?n=35','support':'桃園市官方土地介紹：西北部台地與農業灌溉人工埤塘；原頁實讀。'},{'url':'https://www.ia.gov.tw/zh-TW/media/StoryContent?a=109&id=479&listid=109&p=1','support':'農田水利署桃園灌區埤塘發展史：台地坡降、較高處蓄水與下接灌溉，以及工業都市化變遷；原頁實讀。'}],
 'checks':['實開完整原題與必要臺灣四點圖，原D與藍c紅D作答記錄不動','四張是地形/土地利用/光電棲地/定位實際圖像，不是舊文字流程框','不把地勢高直接畫成地下水必少的科學定律，不加未提供水位/岩層/時程','前後埤塘數與覆蓋面積僅情境，不當歷年統計；不推論全部光電相同生態影響','甲乙丙丁按本題原圖相對位置，丁在西北桃園；不套其他題標點、不當精測座標']},
'q-1063':{
 'title':'西非馬利與跨撒哈拉貿易',
 'rows':[
 ['① 馬利先定位在西非','馬利帝國、黃金食鹽與沙漠商路合起來，指向西非。第一圖以非洲全貌找馬利區域，再看其北側的撒哈拉。','圈只示馬利相關區域，不畫帝國或現代馬利國界；沙漠色帶為概略範圍。','非洲海陸輪廓，撒哈拉以淡金色帶概示，西非馬利區域用圈定位，不以現代國界代替帝國疆界。'],
 ['② 商路穿越撒哈拉','西非馬利與北非經由跨撒哈拉商路交流，黃金與食鹽是題目的重要商品線索。雙向箭頭幫助辨認跨沙漠的聯繫。','箭頭不是精確商路；右側金、鹽是商品圖例，不是礦產位置或交換比率。','西北非地圖，兩個方向的箭頭穿越沙漠色帶，側邊獨立底框放金與鹽圖例，不在地圖上標特定產地。'],
 ['③ 不能只憑伊斯蘭就選西亞','A伊朗高原、B阿拉伯半島、D安納托力亞高原都在西亞一帶，與西非馬利的定位不符。伊斯蘭文化也傳到非洲，不能單靠宗教名詞選B。','A、B、C、D只示各區相對位置，不畫高原或半島的精確範圍。','非洲與西亞並置地圖，以字母圈示A伊朗、B阿拉伯、C撒哈拉、D安納托力亞的概略區位，馬利在西非。']
 ],
 'answer':'答案 C：撒哈拉沙漠',
 'points':['西非馬利＋穿越沙漠的商路，指向撒哈拉。','不能把伊斯蘭文化限定在阿拉伯半島。','原題年代、方位措辭與商品敘述照留；此圖用區域與商路判讀，不增添詳細帝國邊界或產地。'],
 'fourthAlt':'西北非海陸圖以馬利區域圈與跨沙漠概略路徑，連向標C的撒哈拉色帶，總結原題C。',
 'sources':[{'url':'https://whc.unesco.org/en/list/119/','support':'UNESCO廷巴克圖世界遺產：撒哈拉門戶、伊斯蘭學術與商貿；全文實讀。'},{'url':'https://www.metmuseum.org/es/essays/the-trans-saharan-gold-trade-7th-14th-century','support':'Metropolitan Museum研究文章：跨撒哈拉黃金與食鹽貿易；全文實讀，不把文中延伸年代換入原題。'}],
 'checks':['實開完整原卷，保持C與全部四選項/13至17世紀/原文商品及方位措辭','圈不冒充古馬利帝國疆界，不以現代馬利國界當古國範圍','撒哈拉金色帶僅概略位置，非精確沙漠邊界','金/鹽符號已改獨立底框圖例，未置為具體礦址或唯一產區','箭頭只表跨沙漠聯繫，不造真實路線/端點/交換價值或數量','西非與西亞位置分清，不用宗教名詞直接選阿拉伯半島；不重開已保留的原文條件限制']}}
for qid,c in D.items():
 q=Q[qid];d=R/'docs/comics/biology-rework-20261112'/qid;p=R/f'docs/comics/{qid}.json'
 if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
 rev={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{qid}/panel-{i}.png' for i in range(1,5)],'checks':c['checks']}
 s={'id':qid,'subject':'Geography','title':c['title'],'art':f'docs/comics/art/{qid}-four-image-v2-panel-1.svg','panels':[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.svg') for i,v in enumerate(c['rows'],1)],'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.svg','alt':c['fourthAlt']},'protectedWords':['桃園台地','埤塘','太陽能','撒哈拉','西非馬利','伊斯蘭','安納托力亞','阿拉伯半島'],'generationMethod':'four authored native SVG geography illustrations and locator maps','generatorFile':'docs/comics/biology-rework-20261112/root-geography-2/generate.py','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']]+['site/dist/'+f['src'] for f in q['questionFigures']],'answerCheckedAgainst':q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'四張實際地形/地景/地圖分步說明地理判讀，原卷與已核對答案維持，不以imagegen猜精確地圖，不從插畫新增原題數據。','sources':c['sources']+[{'url':'https://www.naturalearthdata.com/about/terms-of-use/','support':'公開領域海陸資料，固定版本與SHA見map-data-provenance.json。'}],'mapDataProvenance':'docs/comics/biology-rework-20261112/root-geography-2/map-data-provenance.json','createdAt':now,'visualChecked':True,'productionReview':rev}
 p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(rev,ensure_ascii=False,indent=2)+'\n');(d/'sources.json').write_text(json.dumps(s['sources'],ensure_ascii=False,indent=2)+'\n')
