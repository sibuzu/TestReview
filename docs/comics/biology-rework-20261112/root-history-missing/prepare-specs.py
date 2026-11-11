from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[4];D=Path(__file__).parent;Q={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']};now=datetime.now(timezone.utc).isoformat()
config={
'q-774':{'subject':'Chinese','ext':'png','title':'核對合音字，保留原卷單選疑義','rows':[
 ['① 啥：什麼','A的啥有甚麼之義，也有合音分析依據。不能為了配合單選預期C，就把啥與什麼的對應直接判錯。','詢問情境只聯想字義，不新增對話條件。','兩位成年人在書房交談，其中一人以疑問神情與開放手勢詢問，沒有文字或答案字母。'],
 ['② 甭是不用；叵是不可','B把甭寫成不可，D把叵寫成不用，兩項把不用與不可混用了。甭提了是不用提；居心叵測中的叵是不可。','已有雨傘而不需第二把，只比喻不用，不表示禁止帶傘。','門口一位已有雨傘的成年人友善婉拒另一把雨傘，對應不需要而不是法律禁止。'],
 ['③ 何消吩咐：何須再吩咐','消在本句是需要；教育部只消條也將消釋為需要的合音。何消吩咐就是哪裡需要再吩咐，對應原卷預期C。','工作情境只協助理解不需再吩咐，不補原題人物或情節。','成年人已開始整理空白文件，另一人準備說明但看見工作已理解；不表示拒絕工作。']
 ],'answer':'原卷預期 C；A亦有依據','points':['C：消 → 需要，符合原卷預期。','B甭 → 不用；D叵 → 不可，不能互換。','A啥 → 什麼亦有字義與合音依據，保留已確認的單選疑義，不強判A錯。'],'alt4':'讀者同時核對字典與兩張未刪去的空白字卡，表示依據需要保留，未把A強行刪成錯項。','protected':['需要','不用','不可'],'checks':['實開原卷題幹及四選項，保留啥/消與原卷預期C','保留既有已確認的A成立依據與單選疑義，不新建確認、不改核心答案','不用與不可不混用，雨傘比喻只表不需要','四幅新情境圖無錯誤中文或答案符號，第四幅實際字典/雙字卡圖仍保留雙依據'],'sources':[{'url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=113846&q=1&word=%E6%B6%88','support':'實讀只消條：消為需要的合音。'},{'url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=33869&la=0&powerMode=0','support':'實讀啥條：甚麼。合音研究依據沿用已核對原詳解及resolved確認，不新造排除理由。'}]},
'q-608':{'subject':'History','ext':'svg','title':'從清代賦稅分類，接到日治高砂族','rows':[
 ['① 由內附、輸餉判清代','地方志用是否歸附、繳納賦稅來分類；這是清代統治者的政治分類。先抓時代，不把舊稱當作族群文化高低。','新製文書聯想，不是原始地方志或身分資料。','開啟的帳冊、印章與毛筆，以內附輸餉文字連結清代賦稅線索。'],
 ['② 接續清代是日治','題目問接續的政權，因此把清代接到日治。圖中兩冊書表示時序，臺灣輪廓只協助定位，不表示歷史實際管轄範圍。','今海岸定位，不是番界、歷史疆界或族群分布。','臺灣定位輪廓與清代、日治兩冊書，上下箭頭表示前後時期。'],
 ['③ 1935是戶籍欄的更名','日治初期仍有生蕃、熟蕃用語。1935年修改戶口調查規程，在戶籍欄以高砂族取代生蕃；不是斷言此詞在1935年才首次出現。','日曆、帳冊與印章均為新製圖，不仿造原始戶籍文件。','1935日曆連到開啟的戶籍聯想帳冊，旁標高砂族與戶籍用語。']
 ],'answer':'答案 C：高砂族','points':['清代賦稅分類 → 接續的日治政權。','高砂族是本題對應的日治歷史用詞。','戰後又有山地同胞等舊稱；這些名稱不等於今日身分或文化分類。'],'alt4':'臺灣定位圖旁有日治時期書冊及高砂族字樣，以歷史舊稱不等於今日身分收束，不畫族群分布或文化高低。','protected':['高砂族','內附','輸餉','清代','日治','1935'],'checks':['實開原卷完整題幹與四選項，C與原有日期答案保持','實讀檔案管理局：1935是法律戶籍更名，不是首次造詞','歷史殖民分類與今日身分分開，不畫文化階序或刻板民族服裝','現代海岸只作位置參考，未暗示全島統治邊界或族群分布','四張獨立SVG含帳冊/日曆/地圖等真正圖像，第四非純文字框'],'sources':[{'url':'https://art.archives.gov.tw/tw/art/2092.html','support':'實讀主文，清代稅賦政治分類、日治沿用舊字及1935法定戶籍欄名稱。'}]},
'q-612':{'subject':'History','ext':'svg','title':'臺南首府從鄭氏開始，不把清代延續當起點','rows':[
 ['① 一府指臺南府城','俗諺中的一府是臺南，二鹿是鹿港，三艋舺是臺北艋舺。三個位置幫助讀懂背景，不是現今城市排名。','今海岸輔助定位；點位不表示歷史行政邊界或距離。','臺灣輪廓上分別標臺南、鹿港與艋舺，艋舺位於北部，臺南位於西南。'],
 ['② 鄭氏以臺南為統治中心','鄭成功在今臺南一帶設承天府。本題問漢人政權的首府起點，因此應先想到鄭氏，後來清代仍延續臺南的重要性。','通用官署圖只聯想行政中心，不是承天府建築復原。','臺南點位連到通用行政建築，精確標出鄭氏、承天府與今臺南。'],
 ['③ 1661進攻，1662投降','原詳解區分1661年鄭成功來臺進攻與1662年荷蘭人投降；不能把兩年事件混作同時。這不影響本題選鄭氏時期。','日曆與書冊只表示年代/事件，不是戰役或投降實錄。','左右兩張獨立日曆1661與1662，分別連到來臺進攻及荷蘭投降，箭頭表示先後。']
 ],'answer':'答案 B：鄭氏時期','points':['關鍵是從何時開始：鄭氏以臺南為統治中心。','清代政治重要性是延續，不能取代最早起點。','一府是臺南；不因府字就直接選清帝國。'],'alt4':'臺灣西南臺南點被圈出，旁有通用行政建築及首府起點文字，標示B鄭氏時期，今海岸不作鄭氏統治範圍。','protected':['一府','二鹿','三艋舺','承天府','鄭氏','1661','1662'],'checks':['實開原卷完整題幹四選項，B與最早起點保持','三城市依現代經緯度定位，未臆造古海岸/領域或距離','1661/1662分年，官署是通用教學圖不仿承天府史實外觀','清代是延續而不是起點，四幅各有地圖/年代日曆/建築圖像','原題及已有勘誤說明不變，不重開相同歷史確認'],'sources':[{'url':'https://thcts.sinica.edu.tw/themes/rb02.php','support':'實讀中研院明鄭行政疆域說明，今臺南承天府及後續清代沿用。'},{'url':'https://historic.tainan.gov.tw/index.php?belongid=45&id=89&index=1&lang=cht&option=module&task=pageinfo','support':'實讀延平郡王祠歷史年表，1662荷蘭人投降離臺；與1661來臺區分。'}]}}
for qid,c in config.items():
 q=Q[qid];p=R/f'docs/comics/{qid}.json';d=D.parent/qid;d.mkdir(exist_ok=True)
 if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
 rev={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[str((d/'contact.png').relative_to(R))],'checks':c['checks']}
 spec={'id':qid,'subject':c['subject'],'title':c['title'],'art':f"docs/comics/art/{qid}-four-image-v2-panel-1.{c['ext']}",'panels':[dict(zip(['heading','text','caption','alt'],row),image=f"docs/comics/art/{qid}-four-image-v2-panel-{i}.{c['ext']}") for i,row in enumerate(c['rows'],1)],'fourth':{'answer':c['answer'],'points':c['points'],'image':f"docs/comics/art/{qid}-four-image-v2-panel-4.{c['ext']}",'alt':c['alt4']},'protectedWords':c['protected'],'generationMethod':('built-in image_gen, four independent detailed word-meaning illustrations' if c['ext']=='png' else 'four independent authored native SVG locator and archival teaching illustrations'),'sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']],'answerCheckedAgainst':q.get('passage','')+'\n'+q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'只對原本完全缺圖題補四圖；核心原題與已確認答案/限制保留，不擴大到暫停重製範圍。','sources':c['sources'],'createdAt':now,'visualChecked':True,'productionReview':rev}
 if c['ext']=='svg':spec.update(generatorFile=str((D/'generate.py').relative_to(R)),mapDataProvenance=str((D/'provenance.json').relative_to(R)))
 p.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(rev,ensure_ascii=False,indent=2)+'\n')
print('Prepared3specs')
