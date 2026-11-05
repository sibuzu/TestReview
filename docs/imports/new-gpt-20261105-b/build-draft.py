from pathlib import Path
import json,hashlib,datetime,copy
from zoneinfo import ZoneInfo
D=Path(__file__).resolve().parent;R=Path.cwd();URL='https://chatgpt.com/share/6aec9480-acd4-83ec-93b8-0728550cb2a2';SID='src-more-059'
a=json.loads((R/'docs/sources/6aec9480-acd4-83ec-93b8-0728550cb2a2.json').read_text());items=[]
def asset(k):return str((D/'originals'/f'{k}.png').relative_to(R))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def evidence(page,crops,mark):
 m=a['messages'][1];p=f'docs/source-pages/chatgpt-6aec9480-{page}.jpg';att=next(v for v in m['content']['parts'] if isinstance(v,dict) and v.get('size_bytes')==(R/p).stat().st_size)
 return dict(url=URL,messageIndex=1,messageId=m['id'],firstQuestionTimestamp=m['create_time'],firstQuestionDateTime=datetime.datetime.fromtimestamp(m['create_time'],ZoneInfo('Asia/Taipei')).isoformat(),originals=[dict(path=p,sha256=sha(p),bytes=(R/p).stat().st_size,fileId=att['asset_pointer'].split('?')[0])],attachmentMatchedBy='archive size_bytes/fileId',cropHashes={asset(k):sha(asset(k)) for k in crops},inclusionEvidence=mark)
def q(no,title,stem,opts,answer,explanation,analyses,student,images,page,mark,figures=None):
 key=f'gpt059-math-{no}';x=dict(id=key,sourceId=SID,subject='Math',title=title,chapter='綜合',volume='綜合',date='2026-11-05',dateLabel='首次出題日期',question=stem+'\n'+'\n'.join(f'({c}) {o}' for c,o in zip('ABCD',opts)),answer=f'({answer}) {opts["ABCD".index(answer)]}',explanation=explanation,trap='',verification='原卷逐題核對',verificationNote='已實開真正上傳的兩頁原卷及裁圖，逐題核對條件、圖形與全部選項。日期為首次原卷核對訊息的台灣日，實際考試日期未提供。未確認冊次或教材章節，歸綜合。',diagram='',tags=[title.split('｜')[-1],'函數'],images=[asset(k) for k in images],sourceLabel=f'分享原卷｜第{no}題',studentAnswer=student,contentStatus='完整原題',correctOption=answer,passage='',optionAnalysis=[dict(label=c,text=o,wordClass='應選' if c==answer else '不選',meaning='',explanation=t) for c,o,t in zip('ABCD',opts,analyses)],tables=[],questionFigures=figures or [],explanationFigures=[],originalQuestionNumber=str(no),sourceEvidence=evidence(page,images,mark))
 items.append(dict(draftId=key,originalQuestionNumber=str(no),date=x['date'],answerCanBeDetermined=True,correctOption=answer,sourceEvidence=x['sourceEvidence']));return x
def fig(k,alt,caption):return dict(src=asset(k),alt=alt,caption=caption)
q7=q(7,'數學第7題｜函數計算流程','下圖為某函數的計算流程，若輸入一個x值，輸出的值為y，則此函數可表示為下列何者？',['y＝x－2²×5－13','y＝5（x－2²）－13','y＝5x²－20x＋7','y＝5x²－4x－9'],'C',
'''依流程保留每一步運算的對象
輸入x→減2得x－2→平方得（x－2）²→乘以5得5（x－2）²→減13。
所以y＝5（x－2）²－13＝5（x²－4x＋4）－13＝5x²－20x＋7，選C。

平方的是減2後的整個結果，不是只把2平方。A、B中的2²都只對2平方，沒有依流程把x－2當作整體平方。D也不等於展開式：中間項須是5×（－4x）＝－20x，常數項是20－13＝7。

可用x＝2回代驗算：流程結果是－13；C代入得20－40＋7＝－13。B則為5（2－4）－13＝－23，不符合。
原AI答案表將學生B判成正確，與原卷流程、選項不符；獨立驗算後訂正C，不因原AI稱答對就漏收此錯題。''',
 ['先依通常運算順序只把2平方，沒有將減2後的整體平方。','2²位於括號內，但不是（x－2）²，平方對象錯誤。','正確流程5（x－2）²－13展開即得此式。','展開時中間項與常數項皆不符正確式。'],'B；原卷未見紅筆訂正。',['page1-q7'],1,'user訊息1要求核對整份原卷；第7原作答B經流程獨立驗算應C，來源AI誤判B正確，仍屬真錯題。',[fig('page1-q7-flow','輸入x→減2→平方→乘以5→減13→輸出y','原卷計算流程；運算順序另以文字完整保留。')])
q10=q(10,'數學第10題｜水桶注水關係式','有一容量為9公升的水桶，內部已裝有1.5公升的水，已知有一水管每秒的流量為300毫升，若用此水管開始注水x秒後，水桶的容量剩下y公升，則x與y的關係式為何？',['y＝0.3x＋1.5','y＝7.5－300x','y＝－0.3x＋9','y＝－0.3x＋7.5'],'D',
'''先辨清楚y代表的是哪個量
原卷題幹寫「水桶的容量剩下y公升」，是尚可容納水的剩餘容量，不是已裝的水量。
原有水1.5公升、總容量9公升，因此剛開始的剩餘容量為9－1.5＝7.5公升。每秒流入300毫升＝0.3公升，剩餘容量每秒減少0.3公升。
所以y＝7.5－0.3x＝－0.3x＋7.5，選D。實際注水至滿的時間為7.5÷0.3＝25秒，這個容量模型適用0≤x≤25。

A是桶中已裝水量的式子，沒有對應本題問的「容量剩下」。B初值7.5雖對，卻把毫升數300直接與公升相減，單位不一致。C使用總容量9當初值，漏扣原本已裝的1.5公升。
原AI把y解讀成桶內水量而改選A；原卷清楚問剩餘容量，原作答D正確。此題是原AI誤改，保留使用者原問核對範圍與明確原題作為更正證據。''',
 ['這是已裝水量，不是本題尚可容納的剩餘容量。','300的單位是毫升，須改成0.3公升才可運算。','初值應扣掉已裝1.5公升，為7.5，不是9。','剩餘容量初值7.5公升，每秒減少0.3公升，符合題意。'],'D；原卷未見紅筆訂正。',['page1-q10'],1,'user訊息1要求核對整份原卷；原AI稱第10學生D錯而改A，但原卷問容量剩下，D其實正確；此為來源AI實質誤改，保留更正原題，不稱學生錯題。')
q16=q(16,'數學第16題｜兩直線的函數值比較','如右圖，坐標平面上，直線L₁為一次函數y＝ax＋b的圖形，直線L₂為y＝cx＋d的圖形。若L₁與L₂相交於點P（2，－3），則下列敘述何者錯誤？',['2a＋b＝2c＋d','3a＋b＜3c＋d','b＜d','－a＋b＜－c＋d'],'B',
'''先把代數式看成同一個x對應的高度
L₁的函數值為ax＋b，L₂的函數值為cx＋d。比較兩式時，是在相同x的垂直位置比較哪一條線較高。
交點P（2，－3）表示x＝2時，兩條線的y值同為－3，所以2a＋b＝2c＋d，A正確。
圖中L₂向右下降比L₁更快；交點右側x＞2，L₁在L₂上方。x＝3時應是3a＋b＞3c＋d，B印成小於，因此題目問錯誤敘述時選B。

交點左側x＜2，L₁在L₂下方。x＝0時比較y截距，b＜d，C正確；x＝－1時得到－a＋b＜－c＋d，D也正確。

也可令兩線差值為（ax＋b）－（cx＋d）＝（a－c）（x－2）。原圖L₁的斜率較大、a－c＞0，因此x－2的正負決定哪條線較高；不須猜出原圖沒有提供的個別斜率數值。''',
 ['交點的x為2，兩線函數值相等，敘述正確。','x＝3在交點右側，L₁較高，應為大於；此敘述錯誤，符合題目所問。','x＝0在交點左側，L₁較低，b＜d正確。','x＝－1在交點左側，L₁較低，敘述正確。'],'A；原卷未見紅筆訂正。',['page2-q16'],2,'user訊息20明示第16、17、18題@錯題；第16原作答A，獨立比圖與代數驗答B。',[fig('page2-q16-graph','兩條下降直線L₁與L₂交於P（2，－3）；L₂較陡，交點右側L₁較高、左側L₁較低。','原卷直線圖；僅提供交點與相對位置，不杜撰個別斜率。')])
common='如圖（一），在同一直線上，甲自A點開始追趕等速率前進的乙車，且圖（二）表示兩車距離與所經時間的線型關係圖。若乙車的速率為每秒2公尺。'
q17=q(17,'數學第17題｜兩車距離與時間','若經過x秒，甲、乙兩車的距離為y公尺，請問x與y的關係式為何？',['y＝（1/5）x＋10','y＝－（1/5）x＋10','y＝（1/5）x－10','y＝－（1/5）x－10'],'B',
'''由圖讀出起點與追上時間
圖（二）在x＝0時，兩車相距10公尺；50秒時相距0公尺，所以線段經過（0，10）與（50，0）。
距離每秒的改變量＝（0－10）÷（50－0）＝－1/5公尺／秒。初始距離是10，故y＝－（1/5）x＋10，選B。

A、C斜率為正，表示距離隨時間增加，與圖不符。C、D的截距是－10，等於說剛開始的兩車距離為負數，也與10公尺不符。可再用x＝50檢驗B：y＝－10＋10＝0，正好對應追上。

y是兩車之間的距離，不是甲或乙各自移動的路程。乙速率每秒2公尺不是此距離函數的斜率；－1/5表示兩車間距每秒縮短0.2公尺。圖示只描繪追上前0≤x≤50，不能將負距離當作追上後的實際間距。''',
 ['斜率正表示間距增加，與圖中下降不符。','起始10公尺，50秒降至0，斜率－1/5且截距10，正確。','斜率方向與初始值都不符。','雖為負斜率，但初始距離誤為－10公尺。'],'C；原卷未見紅筆訂正。',['page2-q17'],2,'user訊息20明示第16、17、18題@錯題；第17原作答C，依完整共圖獨立驗答B。')
q18=q(18,'數學第18題｜甲車移動的路程','經過30秒時，甲車自A點移動多少公尺？',['63','64','65','66'],'D',
'''先求每秒縮短多少距離
由共圖可知，甲原本落後乙10公尺，50秒後追上，因此每秒縮短的間距為10÷50＝0.2公尺。這是甲比乙快的相對速率，不是甲的速率。
乙每秒走2公尺，所以甲的速率為2＋0.2＝2.2公尺／秒。30秒時甲自A點移動2.2×30＝66公尺，選D。

另一解法：30秒後乙移動2×30＝60公尺，位置在距A點10＋60＝70公尺處。此時兩車距離由第17題的式子得10－0.2×30＝4公尺，所以甲的位置是70－4＝66公尺。

若直接算乙的2×30＝60，或只算間距減少0.2×30＝6，都不是本題問的甲車路程。A、B、C都不符合上述兩種互相驗證的計算。''',
 ['由追及速率2.2公尺／秒計算，30秒應為66，不是63。','2.2×30＝66，不是64。','2.2×30＝66，不是65。','甲速率2＋10/50＝2.2，乘30秒得66公尺。'],'C；原卷未見紅筆訂正。',['page2-q18'],2,'user訊息20明示第16、17、18題@錯題；第18原作答C，依共文乙速率與追上時間獨立驗答D。')
g=copy.deepcopy(q17);g.update(title='數學題組｜兩車追及（第17、18題）',question='請閱讀共用敘述及圖（一）、圖（二），回答第17、18題。',passage=common,groupQuestions=[q17,q18],correctOption='',optionAnalysis=[],originalQuestionNumber='17、18',questionFigures=[fig('page2-q17-18-diagrams','圖（一）甲在A點，乙在前方10公尺；圖（二）間距從0秒10公尺線性降至50秒0公尺。橫軸時間（秒）、縱軸兩車距離（公尺）。','原卷共同圖（一）、圖（二）；起點相距10公尺，50秒追上。')],images=[asset(k) for k in ['page2-q17-18-common','page2-q17','page2-q18']],answer='【第17題】'+q17['answer']+'\n【第18題】'+q18['answer'],explanation='【第17題】\n'+q17['explanation']+'\n\n【第18題】\n'+q18['explanation'],studentAnswer='【第17題】C\n【第18題】C',groupMetadata=dict(originalQuestionNumbers=['17','18'],displayOrder=[q17['id'],q18['id']],sourceGroupVerified=True,sharedPassageOnce=True,sourceSharedReadingOnly=True))
g['sourceEvidence']=evidence(2,['page2-q17-18-common','page2-q17','page2-q18'],'user訊息20明示17、18皆@錯題；共用敘述與兩圖只顯示一次，各子完整四選項與詳解保留。')
# q10 confirmed correct student's answer but retained as source-AI correction, not represented as student mistake.
parents=[q7,q16,g]
(D/'questions.json').write_text(json.dumps(parents,ensure_ascii=False,indent=2)+'\n')
for x in [q7,q16,q17,q18]:
 y=copy.deepcopy(x)
 if x in [q17,q18]:y['passage']=common;y['questionFigures']=g['questionFigures']
 (D/(x['id']+'.json')).write_text(json.dumps(y,ensure_ascii=False,indent=2)+'\n')
reviews=[dict(draftId=q7['id'],kind='原AI錯誤判答',before='原AI選擇題表將第7學生B列為正確B。',after='原卷B是5（x－2²）－13，只平方2；依流程應平方整個x－2，展開5x²－20x＋7，正解C，學生B需訂正。',reason='原AI答案表與原卷平方範圍不符，因而漏列真正錯題。',expectedAnswer='C',sourceUrl=URL,questionText=q7['question'],evidence=q7['images']),dict(originalQuestionNumber='10',kind='來源AI誤改已正確題（不新增錯題）',before='原AI稱第10正解A，將學生D判錯，解讀y為桶內水量。',after='原卷問水桶容量剩下y公升，剩餘容量7.5－0.3x，正解D；學生D原本正確。',reason='將剩餘容量與已裝水量混淆，原題不得改寫成桶內水量。',expectedAnswer='D',sourceUrl=URL,questionText=q10['question'],evidence=q10['images']),dict(kind='來源AI誤改已正確題（不新增錯題）',originalQuestionNumber='5',before='原AI把常數函數y=a誤讀成y=ax，算出h+k=6而改B，判學生D錯。',after='原卷常數函數y=a通過（2，6），故a=h=k=6，h+k=12選D；學生D原本正確，不新增為學生錯題。',reason='原AI擅改函數類型造成錯誤訂正。',expectedAnswer='D',sourceUrl=URL,questionText='若（－5，h）、（2，6）、（7，k）三點都在常數函數y＝a的圖形上，則h＋k之值為何？\n(A) 2\n(B) 6\n(C) 10\n(D) 12',evidence=[asset('q5-detail')]),dict(kind='來源AI誤改已正確題（不新增錯題）',originalQuestionNumber='非選2(1)',before='原AI稱126只是半成品而不是乙產出，將本小題改115，判學生126錯。',after='原問正是送入乙機器的半成品；y＝(2/3)×180＋6＝126公斤，學生原答正確。115是乙後續產品z，非第(1)小題所問。第(2)小題原答441亦正確。',reason='原AI錯認題目要求的生產階段。',expectedAnswer='126公斤',sourceUrl=URL,questionText='有甲、乙兩部機器在生產線上連在一起，若x表示原料重量，甲機器的半成品重量y＝(2/3)x＋6；y表示送進乙機器的半成品重量，而乙機器的產品重量為z＝(5/6)y＋10。試回答下列問題：\n(1) 若將180公斤的原料送進甲機器，則有幾公斤的半成品會進入乙機器？（2分）\n(2) 若最後想要由乙機器得到260公斤的成品，則須送多少原料進甲機器？（4分）',evidence=[asset('nonchoice2-detail')])]
(D/'transcript.txt').write_text(json.loads((R/'docs/sources/6aec9480-acd4-83ec-93b8-0728550cb2a2-rendered.json').read_text())['text']+'\n')
manifest=dict(sourceId=SID,url=URL,status='ready',producer='/root/comic_lane_3',questionPath=str((D/'questions.json').relative_to(R)),questionSHA256=sha(str((D/'questions.json').relative_to(R))),originalQuestionCount=4,questionPageCount=3,actualStudentMistakeCount=4,sourceAICorrectionQuestionCount=0,archivePath='docs/sources/6aec9480-acd4-83ec-93b8-0728550cb2a2.json',transcriptPath=str((D/'transcript.txt').relative_to(R)),sourceAIImagesAdopted=False,teachingComicState='queued_after_intake',pendingQuestionConditions=[],items=[v for v in items if v['originalQuestionNumber']!='10'],reviews=reviews,sharedMaterials='第17、18題共用敘述及圖（一）（二）僅parent顯示一次，各子四選項/解析完整。',skips=[dict(kind='student_original_correct',questionNumbers=['1','2','3','4','5','6','8','9','10','11','12','13','14','15','19','20','非選1','非選2'],reason='已核對全部20選擇＋2非選，未另問且原本答對的同卷題暫跳過、不永久排除。第5、第10與非選2(1)AI誤判另保留來源級完整review證據，不虛設qid。'),dict(kind='source_ai_generated',reason='來源AI分數面板、延伸互動與生成圖不當新原題。')],visualReview=dict(originalsViewed=[f'docs/source-pages/chatgpt-6aec9480-{n}.jpg' for n in [1,2]],allOriginalsReadable=True,cropsViewed=[str(f.relative_to(R)) for f in sorted((D/'originals').glob('*.png'))],allCropsComplete=True,checkedNecessaryMaterials=True,notes='已實看全部原圖及裁圖；第10必保留「容量剩下」原字，非桶內水量。'),titleReview='自訂標題中性，不透露正解。',contentFrozen=True,readyAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('ready',len(parents),'pages',4,'originals; source-level corrections=3')
