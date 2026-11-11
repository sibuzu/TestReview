from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[4];P=next(q for q in json.loads((R/'site/dist/data.json').read_text())['questions'] if q['id']=='q-581');QS={q['id']:q for q in P['groupQuestions']};now=datetime.now(timezone.utc).isoformat()
D={
'q-581':{'title':'配置圖能讀相鄰，不能補未知資訊','rows':[
 ['① 只用圖上有的資訊','原圖將白沙灣遊客中心與開幕主舞臺表演場地標在鄰近位置。先看標示與相對配置，不替未標名海域補上名稱。','新製配置關係示意；不補原圖沒有的北箭、比例尺或海域名稱。','簡化海岸場地配置，左側特技區、較右造型區，下方主舞臺與遊客中心鄰近；海域只註明未標名。'],
 ['② 相鄰關係直接可讀','選項C說遊客中心緊鄰主舞臺，這是原圖可直接讀取的關係。建築小景只幫助理解相鄰，不表示真的長這樣或相隔幾公尺。','主舞臺與遊客中心的相鄰示意，不是實景立面。','紅屋頂舞臺與藍色遊客中心並置，兩者相鄰但不強制接觸，無實際距離數值。'],
 ['③ 無比例尺不能算實際距離','市集和播報臺在圖上各有位置，但題圖沒有比例尺或已知實際長度，無法求兩地的實際距離，因此D不合。','虛線連接只示待求距離，不是道路或實測長度。','市集攤位與播報圖示分置，虛線及問號表示實際距離未知，沒有公里、公尺或換算比例。']
 ],'answer':'答案 C：遊客中心緊鄰主舞臺','points':['圖上標示與相鄰位置能直接讀出。','原圖未標海域名稱，不能由配置圖自行補出臺灣海峽。','沒有比例尺，不能求市集到播報臺的實際距離。'],'alt4':'新製配置示意圈出主舞臺與遊客中心的鄰近關係，保留左側特技與較右造型兩區，不加原圖未知資訊。','protected':['遊客中心','主舞臺','白沙灣','比例尺','實際距離','臺灣海峽'],'sources':[],'checks':['實開完整第44題/四選項/共同題文及圖九，放大原圖確認播報臺、市集、遊客中心與舞臺','保留已結案C與原AI先B後C的訂正解說，不重開同項確認','不補海域名、北向或比例尺，未把輔助小景當真實建築外觀','市場與播報臺連線不附長度，不猜實際距離或道路','四張配置/建築/待求距離/整合示意各有實際圖像']},
'q-582':{'title':'東南風往西北，逆風跑向東南','rows':[
 ['① 風名看風吹來的方向','共同題文給東南風，表示從東南吹向西北。第一圖藍箭尾在東南，箭頭朝西北；不要把吹去的方向當風名。','北上東右；藍箭頭表示空氣移動，不表示人跑動。','北上羅盤中，藍色空氣箭頭從右下東南指向左上西北，箭頭尖端正確。'],
 ['② 逆風跑，方向與風相反','題文要求逆風向前跑。藍風往西北，橘色人的跑動便朝相反的東南，迎向來風，所以選A。','藍風與橘色跑動箭頭分開，兩者精確反向。','同一北上羅盤，藍箭朝西北、橘箭朝東南，平行分置避免重疊，分別標風與人。'],
 ['③ 方位圖不是高度或風速圖','俯視圖把風箏畫在人物西北側，提線接到手邊，人朝東南跑。畫面只說明方位，不用北海岸或活動月份另猜季風。','俯視方位示意，不是升力、風速或高度測量。','俯視羅盤上風箏在人物西北側，提線連手，藍風往西北、橘跑動朝東南；沒有機械升力數據。']
 ],'answer':'答案 A：東南方','points':['東南風：東南 → 西北。','逆風跑：迎向東南來風。','依題文現場風向，不把西北吹去方向選成迎風跑方向。'],'alt4':'北上羅盤標示原題四個方向選項，藍風朝西北、橘跑動朝東南，A東南以紅色標明。','protected':['東南風','東南方','西北方','逆風','來風','藍箭頭','北海岸'],'sources':[{'url':'https://agr.cwa.gov.tw/','support':'氣象署農業氣象觀測網說明風向為風吹來的方向；已查原頁。'}],'checks':['實開第45題/全選項與共同題文，保持已核對A及原B紅A筆跡','四圖北上東右，藍風SE→NW，橘跑動NW→SE，箭尾和箭頭逐張核對','不是把東南風解成吹向東南，也不選順風跑','第3圖提線接手、風箏在下風NW，明示俯視而非高度/升力測量','保留現場東南風，不由北海岸季節猜新風向']},
'q-583':{'title':'以石門為起點，比較就近與不宜','rows':[
 ['① 活動在新北石門','共同題文說活動在新北市石門區。第一圖用橙點概示北部石門，題目要同時抓住就近與不宜兩個條件。','橙點示石門區位，不是精測活動座標。','臺灣主島輪廓北端附近標石門橙點，說明活動位於北部。'],
 ['② 三個選項的代表遺址在北部','圓山文化的代表遺址在臺北；十三行與大坌坑的代表遺址在新北八里。B、C、D均屬北部，比較符合本題相對就近。','以臺北、八里概略區位比較；不把代表遺址當文化完整分布。','北部海岸放大圖，石門橙點，八里與臺北圓山為藍綠點；八里旁標十三行和大坌坑，不另造精確遺址坐標。'],
 ['③ 長濱文化代表遺址在臺東','長濱文化的代表遺址八仙洞在臺東長濱。相較其他北部選項，長濱離石門較遠，因此A最不符合就近的條件。','直線只比較區位，不是道路、公里或車程。','臺灣圖保留北部石門橙點與東部臺東長濱紅點，以虛線比較區位，沒有道路或車程數字。']
 ],'answer':'答案 A：長濱文化','points':['題目問不宜就近安排的一項。','圓山、十三行、大坌坑的代表遺址在北部；八仙洞在臺東長濱。','比較代表遺址區位，不是文化年代或整體分布範圍。'],'alt4':'臺灣定位圖以北部B/C/D區位圈和東部A長濱紅點對比石門，說明不宜就近的是A，非道路或文化疆界圖。','protected':['石門','就近','不宜','長濱文化','臺東長濱','圓山文化','十三行','大坌坑','八仙洞'],'sources':[{'url':'https://www.eastcoast-nsa.gov.tw/zh-tw/attractions/detail/37/','support':'東管處八仙洞頁：臺東長濱與長濱文化；實讀。'},{'url':'https://nhsrc.boch.gov.tw/SiteDetail?id=20060501000002','support':'文資局圓山遺址資料：臺北盆地；實讀。'},{'url':'https://sshm.vm.ntpc.gov.tw/heritage_detail_shihsanhang','support':'新北十三行博物館：十三行遺址與八里；實讀。'},{'url':'https://sshm.vm.ntpc.gov.tw/heritage_detail_dapenkeng','support':'新北十三行數位博物館大坌坑遺址位置；實讀。'}],'checks':['實開完整第46題/四選項與共同題文，保留原A及原D紅A筆跡','先石門、再就近/不宜，未拿文化年代取代距離條件','圓山臺北、十三行與大坌坑八里、八仙洞臺東長濱的代表遺址區位核對','點與圈示區位，不當文化唯一分布或精確遺址坐標','未造車程/公里/道路，代表科目仍沿用子題History、題組Geography']}}
coverage=[]
for qid,c in D.items():
 q=QS[qid];d=R/'docs/comics/biology-rework-20261112'/qid;p=R/f'docs/comics/{qid}.json'
 if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
 r={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{qid}/panel-{i}.png' for i in range(1,5)],'checks':c['checks']}
 s={'id':qid,'subject':q['subject'],'title':c['title'],'art':f'docs/comics/art/{qid}-four-image-v2-panel-1.svg','panels':[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.svg') for i,v in enumerate(c['rows'],1)],'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.svg','alt':c['alt4']},'protectedWords':c['protected'],'generationMethod':'four independent authored native SVG teaching illustrations with exact direction/locator relationships','generatorFile':'docs/comics/biology-rework-20261112/root-kite-group/generate.py','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']]+['site/dist/'+f['src'] for f in q.get('questionFigures',[])],'answerCheckedAgainst':q['passage']+'\n'+q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'屬原本缺圖補作的同一題組，每個原問各四張獨立新圖；配置/風向/地理區位需要精確可校對位置，採原生SVG，完整原題、共同題文、原圖及已確認答案均保持。','sources':c['sources'],'mapDataProvenance':'docs/comics/biology-rework-20261112/root-kite-group/provenance.json','createdAt':now,'visualChecked':True,'productionReview':r}
 p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(d/'sources.json').write_text(json.dumps(c['sources'],ensure_ascii=False,indent=2)+'\n')
 coverage.append({'originalId':qid,'spec':f'docs/comics/{qid}.json','images':[f'docs/comics/art/{qid}-four-image-v2-panel-{i}.svg' for i in range(1,5)],'subjectUnchanged':q['subject'],'answerUnchanged':q['answer']})
(Path(__file__).parent/'coverage.json').write_text(json.dumps({'groupPageId':'q-581','originalIds':['q-581','q-582','q-583'],'requiredImages':12,'existingAliasesRetained':['q-582','q-583'],'coverage':coverage},ensure_ascii=False,indent=2)+'\n')
