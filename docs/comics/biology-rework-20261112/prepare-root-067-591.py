from pathlib import Path
import json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];Q={q['id']:q for q in json.loads((R/'site/dist/data.json').read_text())['questions']};now=datetime.now(timezone.utc).isoformat()
D={
'q-067':{
 'title':'同音還要辨字形，只有C兩字相同',
 'rows':[
 ['① A：簿和部不同','對簿公堂的簿與案卷文書有關；按部就班的部是按一定次序進行。兩個都讀ㄅㄨˋ，字形仍不同。','案卷提醒簿；階梯只提示依次，按部就班仍寫部。','左側案卷和公堂，右側人物依序上階梯，作字義聯想，不把按部就班寫成步。'],
 ['② B：投和頭不同','走投無路是找不到可以投奔的出路，寫投；抱頭鼠竄的動作是護著頭逃跑，寫頭。同讀ㄊㄡˊ，不代表同一字。','左側無路可投，右側抱頭逃跑；不是把鼠竄當真人變成老鼠。','左側旅行者遇到阻路石牆，右側不同人物抱著頭快步逃走，沒有攻擊或受傷。'],
 ['③ C：兩個都寫唾','唾手可得形容很容易得到；唾面自乾含受辱而忍讓之意。兩個成語中的ㄊㄨㄛˋ都寫唾，符合前後相同。','左為容易取得，右為忍讓情境；國字由文字明確標示。','左側輕易取到低枝水果，右側成年學者沉著忍讓的情境，非特定史實人物或原卷照片。']
 ],'answer':'答案 C：唾／唾','points':['A：簿／部；B：投／頭。','C：唾手可得／唾面自乾，都寫唾。','D：脣槍舌劍／一箭之地，兵器的劍和弓箭的箭不同。'],'alt4':'桌上清楚區分直身雙刃劍與弓箭，箭有細長箭桿和羽毛；用來排除同音卻異字的D。','protected':['對簿公堂','按部就班','走投無路','抱頭鼠竄','唾手可得','唾面自乾','ㄅㄨˋ','ㄊㄡˊ','ㄊㄨㄛˋ'],'sources':[{'url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=11685&la=0&powerMode=0','support':'教育部簡編本唾手可得字形、讀音與容易得到之意；原頁實讀。'},{'url':'https://dict.idioms.moe.edu.tw/idiomView.jsp?ID=5235&la=0&webMd=1','support':'教育部成語典唾面自乾字形、讀音與忍讓義；原頁實讀。'}],'checks':['完整原題、四選項、原學生D及教材C保持','A明示部不是步，階梯僅作次序聯想，不讓視覺導致錯字','B投/頭分清；C唾/唾相同，不因同音混字','第四張清楚劍/箭兩種物件，沒有把箭畫成劍或錯造距離數值','四張無生成字，精確字形/注音全用可校對文字；示意不冒充原題附圖']},
'q-591':{
 'title':'逐字核對注音，公帑的帑讀ㄊㄤˇ',
 'rows':[
 ['① 轉捩點：ㄌㄧㄝˋ','捩讀ㄌㄧㄝˋ。原題A印ㄌㄟˋ，少了介音ㄧ，所以不選；轉捩點指足以影響事情發展的關鍵。','跑道轉彎只是轉折聯想，不新增原題比賽項目或結果。','跑者接近彎道與新的視野，空白路牌沒有文字或勝負資訊；不是原題人物實況。'],
 ['② 追溯：ㄙㄨˋ','溯讀ㄙㄨˋ，不是原題的ㄙㄨㄛˋ。追溯是回頭探查來源或過去，圖以查閱古蹟資料幫助聯想。','新製查史情境，不指定真實古蹟或證明其建造年代。','研究者比對無字舊照片與空白卷軸，背景為泛指的傳統院落，沒有真實古蹟名與年份。'],
 ['③ 粗獷：ㄍㄨㄤˇ','獷讀ㄍㄨㄤˇ；原題C的ㄎㄨㄤˋ，聲母和聲調都錯。嗓音粗獷是字義情境，不能把錯音當可接受的讀法。','唱歌情境連結聲音特色，正音由文字明列。','成年歌手有力唱歌，手持麥克風，沒有可讀歌詞、音量數據或文字音波標記。']
 ],'answer':'答案 D：帑讀ㄊㄤˇ','points':['公帑指公款，帑讀ㄊㄤˇ，與原題一致。','A捩＝ㄌㄧㄝˋ；B溯＝ㄙㄨˋ；C獷＝ㄍㄨㄤˇ。','原AI把錯音C當正確的處理不採用，逐項核對只有D符合。'],'alt4':'公共工程審查者核對空白帳簿，背景橋梁工地與無面額硬幣盒象徵公款，沒有虛構預算或私下交款。','protected':['轉捩點','追溯','粗獷','公帑','ㄌㄧㄝˋ','ㄌㄟˋ','ㄙㄨˋ','ㄙㄨㄛˋ','ㄍㄨㄤˇ','ㄎㄨㄤˋ','ㄊㄤˇ'],'sources':[{'url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=30965&la=0&powerMode=0','support':'教育部轉捩點：捩ㄌㄧㄝˋ；原頁實讀。'},{'url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=30869','support':'教育部追溯：溯ㄙㄨˋ；原頁實讀。'},{'url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=38255&la=0&powerMode=0','support':'教育部粗獷：獷ㄍㄨㄤˇ；原頁實讀。'},{'url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=17705&la=0&powerMode=0','support':'教育部公帑：帑ㄊㄤˇ；原頁實讀。'}],'checks':['原卷注音逐字實看，Aㄌㄟˋ/Bㄙㄨㄛˋ/Cㄎㄨㄤˋ/Dㄊㄤˇ照留，答案D不變','四個正音逐項教育部簡編本核對，未生成注音或國字','跑者/查史/歌手/公款四圖各連結字義，不把情境當比賽結果/古蹟年代/音量/預算事實','不重問已處理的原AI錯判C，同一訂正不新增確認卡','public funds以泛指工程監督示意，沒有行賄或具名機關/人物']}}
for qid,c in D.items():
 q=Q[qid];d=R/'docs/comics/biology-rework-20261112'/qid;p=R/f'docs/comics/{qid}.json'
 if p.exists() and not (d/'previous-spec.json').exists():shutil.copyfile(p,d/'previous-spec.json')
 rev={'reviewerAgent':'/root','checkedAt':now,'originalVisualChecked':True,'fourGeneratedImagesVisualChecked':True,'answerAndExplanationChecked':True,'sourceQuestionUnchanged':True,'actualViewed':[f'docs/comics/biology-rework-20261112/{qid}/contact.png'],'checks':c['checks']}
 spec={'id':qid,'subject':'Chinese','title':c['title'],'art':f'docs/comics/art/{qid}-four-image-v2-panel-1.png','panels':[dict(zip(['heading','text','caption','alt'],v),image=f'docs/comics/art/{qid}-four-image-v2-panel-{i}.png') for i,v in enumerate(c['rows'],1)],'fourth':{'answer':c['answer'],'points':c['points'],'image':f'docs/comics/art/{qid}-four-image-v2-panel-4.png','alt':c['alt4']},'protectedWords':c['protected'],'generationMethod':'built-in image_gen: four independent richly detailed word-meaning illustrations; exact characters/phonetics remain selectable text','sourceGeneratedArtUsed':False,'originalMaterialsChecked':True,'originalMaterials':['site/dist/'+x for x in q['images']],'answerCheckedAgainst':q['question']+'\n'+q['answer']+'\n'+q['explanation'],'rationale':'只處理使用者核准的missing_illustration補作。四張詞義圖配合逐字核對，不讓生成圖決定國字/注音，不改原題與已確認答案。','sources':c['sources'],'createdAt':now,'visualChecked':True,'productionReview':rev}
 p.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');(d/'production-review.json').write_text(json.dumps(rev,ensure_ascii=False,indent=2)+'\n');(d/'sources.json').write_text(json.dumps(c['sources'],ensure_ascii=False,indent=2)+'\n')
