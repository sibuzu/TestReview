from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
D=Path(__file__).parent;R=D.parents[2]
a=json.loads((R/'docs/sources/6aea1969-2bc0-83ec-8b0d-f21da9cfed80.json').read_text());url=a['url'];questions=[];items=[]
def img(k):return str((D/'originals'/f'{k}.png').relative_to(R))
def add(key,no,title,stem,options,correct,explanation,analyses,index,student='',passage='',images=(),tables=None,figures=None,mark=''):
 q=dict(id=key,sourceId='src-more-056',subject='English',title=title,chapter='綜合',volume='綜合',date='2026-11-03',dateLabel='首次出題日期',question=stem+'\n'+'\n'.join(f'({c}) {o}' for c,o in zip('ABCD',options)),answer=f'({correct}) {options["ABCD".index(correct)]}',explanation=explanation,trap='',verification='原卷逐題核對',verificationNote='已實看原始上傳題本及裁圖，核對題幹、四選項、必要文章/圖表；依使用者在原對話明示的錯題與訂正收錄，不將題本印刷答案冒充學生筆跡。日期採原始出題訊息的台灣日期，未提供實際考試日。',diagram='',notes='',status='todo',starred=False,tags=[title.split('｜')[-1]],images=[img(k) for k in images],sourceLabel=f'分享原題｜第{no}題',studentAnswer=student,contentStatus='完整原題',correctOption=correct,passage=passage,optionAnalysis=[dict(label=c,text=o,wordClass='應選' if c==correct else '不選',meaning='',explanation=e) for c,o,e in zip('ABCD',options,analyses)],tables=tables or [],questionFigures=figures or [],explanationFigures=[],originalQuestionNumber=str(no))
 questions.append(q);m=a['messages'][index];attach=next(x for x in m['content']['parts'] if isinstance(x,dict) and x.get('content_type')=='image_asset_pointer');raw=next(p for p in (R/'docs/source-pages').glob('chatgpt-6aea1969-*.png') if p.stat().st_size==attach['size_bytes'])
 ims=[img(k) for k in images]+[f['src'] for f in figures or []]
 items.append(dict(key=key,originalQuestionNumber=str(no),messageIndex=index,messageId=m['id'],messageCreatedAt=datetime.fromtimestamp(m['create_time'],ZoneInfo('Asia/Taipei')).isoformat(),sourceOriginal=str(raw.relative_to(R)),sourceOriginalSHA256=hashlib.sha256(raw.read_bytes()).hexdigest(),attachment=attach['asset_pointer'].split('?')[0],inclusionEvidence=mark,crops=[dict(path=f,sha256=hashlib.sha256((R/f).read_bytes()).hexdigest(),visuallyChecked=True) for f in ims],answerVerified=True,duplicateDecision='new',originalAIError=False))
add('gpt056-english-01',1,'英文第1題｜又來一通電話用another','Ms. Johnson has been taking phone calls since she entered the office this morning. Just when she thought she could finally leave work, ______ call came in.',['another','each','the next','the other'],'A',
'''逐句翻譯
Ms. Johnson has been taking phone calls since she entered the office this morning.：強森女士從今天早上進辦公室起，就一直在接電話。
Just when she thought she could finally leave work, another call came in.：正當她以為終於可以下班時，又有一通電話打進來。

詳解
前面已一直接電話，正想下班時又增加一通，最貼切的是another call（又一通電話），選A。空格後原本就有call，another直接修飾單數可數名詞call，沒有省略名詞。
each表示每一個，側重逐一看待，無法表達這裡又增加一通的敘事。the next表示接續的下一個，側重已建立的順序；本題的語氣重點是以為終於結束，卻又來一通。the other指特定的另一個，常用於兩者中的另一個或已知的另一對象；本文未作這種限定。

快速判斷：一直接電話→以為能下班→又來一通，another最符合語境。不能把another和the other都譯成另一個就忽略是否特定。原選項未提供，不能推定孩子原先選哪個或實際錯因。''',
['another call表示已有來電後又增加一通，最符合語氣。','each指每一個，不表此處又多一通。','the next側重順序；本題的又來一通以another最貼切。','the other需要特定的另一對象，本題未限定。'],0,student='未提供原選項；使用者以「1@錯題」明示本題。',images=['english-01'],mark='user訊息0明示1@錯題並附原題截圖；原圖A是題本印刷解答，不當學生作答。題幹與四選項完整可核。')
add('gpt056-english-04',4,'英文第4題｜旅行期間的住宿用stay','Carey: Where did you ______ during your trip in Europe?\nAlex: I was a couchsurfer, so I spent the nights on different couches.',['live','keep','land','stay'],'D',
'''逐句翻譯
Carey: Where did you stay during your trip in Europe?：Carey問，你在歐洲旅行期間住在哪裡？
Alex: I was a couchsurfer, so I spent the nights on different couches.：Alex回答，我是沙發客，所以晚上睡在不同的沙發上。
原卷字詞：couchsurfer＝沙發客，指旅行時借住他人住處的旅人。

詳解
during your trip in Europe限定旅行期間；spent the nights on different couches說明旅途中的過夜方式。問的是暫時住宿，stay最自然，答案D。
live常著重居住、日常生活的地點；本題不是單問日常住處。這是語境搭配的比較，不是說live永遠不能指短期居住。keep是保持、保留，本句不能直接表住宿；land是降落、登陸，與回答在哪裡過夜不符。

Where＋did＋主詞＋原形動詞是問句結構。live與stay形式上都能放在did後，不能只靠動詞原形選答，還要讀旅行與過夜的語境。

快速判斷：旅行期間＋過夜地點→stay。使用者記錄A→D，但未提供完整作答思路，不推定實際錯因。''',
['日常居住是常見重點，本題旅途住宿以stay較自然，並非live在任何短期情境都錯。','keep表示保持、保留，不合這裡問住宿。','land表示降落、登陸，不合沙發過夜回答。','stay表示停留、暫住，呼應旅遊期間與過夜方式。'],12,student='A；使用者更正為D。',images=['english-04'],mark='user訊息12明示4@錯題 a--d；題本D為印刷解答，非紅筆。完整對話與全部四選項可核。')
add('gpt056-english-05',5,'英文第5題｜派對上沒有玩得開心','Cathy: Jim didn’t appear to ______ at the party last night.\nSam: Well, he only knew few of your friends and was too shy to talk to strangers.',['enjoy himself','help himself','speak for himself','help him out'],'A',
'''逐句翻譯
Cathy: Jim didn’t appear to enjoy himself at the party last night.：Jim昨晚在派對上看起來玩得不開心。
Sam: Well, he only knew few of your friends and was too shy to talk to strangers.：嗯，他只認識你朋友中的少數幾人，又太害羞而不敢和陌生人說話。

詳解
Sam用認識的人少、太害羞不敢聊天，解釋Jim在派對上難以自在融入、看來沒有玩得開心。enjoy oneself意為過得愉快；主詞Jim是男性單數，所以用enjoy himself，答案A。
help himself可指自行取用食物等，常見help oneself to…，本題沒有取食物線索。speak for himself是替自己發言、表達自己的立場，不等於一般聊天。help him out是幫他解困，涉及幫助另一位男性，對話未提出要幫誰或何種困難。

appear to＋原形動詞在此是看起來……。要把didn’t一併代入：不是Jim玩得開心，而是看起來沒有玩得開心。himself指主詞本人；help him out的him則是所幫助的人，人物關係不同。

快速判斷：認識的人少＋太害羞→派對中的感受→didn’t enjoy himself。原題的few照留；本題按整段語境辨片語，不另編選項。''',
['enjoy himself指自己玩得開心，連同didn’t表沒有玩得開心，呼應下句。','自行取用或自助的情境並未出現。','替自己發言不等於在派對和別人聊天。','幫他解困需要另一位受助者及困難，此處未交代。'],21,student='D；使用者後續更正為A。',images=['english-05'],mark='user訊息21附第5題，訊息28明示d--a補充，確認第5題D→A；題本A為印刷解答。裁圖已保留最下方C/D全文。')
fringe='Are you interested in arts festivals? If yes, then don’t miss the Edinburgh Fringe Festival.\n\nWhat is the Edinburgh Fringe Festival?\nIt is the world’s largest arts festival, and it is held in Edinburgh for more than three weeks in August each year. During the festival, about 400,000 people from far and wide have a great time enjoying the performances.\n\nHow did the Edinburgh Fringe Festival start?\nThere is an interesting story behind it. In 1947, they held the first Edinburgh International Festival. However, only some theater groups were invited to perform. Not on the performing list, eight theater groups arrived in Edinburgh. They couldn’t perform at the festival. Not wanting to give up, they found other places in the city to put on their shows. Much to everyone’s surprise, their shows became a hit. That was how the Edinburgh Fringe Festival started. It has been held every year since then.\n\nWhat is in the Edinburgh Fringe Festival?\nThere are theaters, music, comedies, children’s shows and more. People of all ages can enjoy different performances at the festival.\n\nIs the Edinburgh Fringe Festival free?\nThough there are a lot of free shows at the festival, you still need to buy tickets to watch most of the shows. Some may cost about 35 pounds, but most of them are about ten pounds.\n\n原卷字詞：performance表演；international國際的；perform表演；comedy喜劇。'
add('gpt056-english-25',25,'英文第25題｜人數、票價不等於售出票數','What can we NOT know from the reading?',['Whether there are performances for children.','For how long the Edinburgh Fringe Festival is held each year.','How many tickets are sold at the Edinburgh Fringe Festival each year.','What happened to the eight theater groups after they arrived at the Edinburgh International Festival in 1947.'],'C',
'''全文逐句翻譯
你對藝術節有興趣嗎？如果有，就別錯過愛丁堡藝穗節。
「什麼是愛丁堡藝穗節？」它是世界上最大的藝術節，每年八月在愛丁堡舉辦，持續超過三週。藝術節期間，約四十萬名來自各地的人們愉快地欣賞表演。
「愛丁堡藝穗節如何開始？」它背後有個有趣的故事。1947年，第一屆愛丁堡國際藝術節舉行。然而，只有部分劇團受邀演出。八個不在演出名單上的劇團抵達愛丁堡。他們無法在該藝術節表演。他們不願放棄，在市內另找地方演出。令大家驚訝的是，他們的演出大受歡迎。愛丁堡藝穗節就是這樣開始的。自此以後，它每年舉辦。
「藝穗節有哪些內容？」有戲劇、音樂、喜劇、兒童表演等。各年齡層的人都能欣賞不同的表演。
「藝穗節免費嗎？」雖然有許多免費表演，但大多數表演仍須買票。有些票價約35英鎊，大部分約10英鎊。
附圖地圖標示愛丁堡位於英國蘇格蘭；2016年表演類型比例為喜劇34%、戲劇27%、音樂15%、兒童表演5%、其他19%。

詳解
題目問無法得知什麼，先圈NOT。文章沒有告訴我們每年賣出幾張票，所以選C。
A問是否有兒童表演，第三部分明列children’s shows，圖表也有5%，可知。B的For how long…each year問每年持續多久，第一部分明寫超過三週；不是從創辦至今共多少年。D問八劇團後續，第二部分交代未能在原藝術節演出，便另找場地並大受歡迎，也可知。

數字要連同單位與對象判讀。400,000是人數，不是票數；35與10是英鎊票價，不是張數；圖表是表演類型百分比，不是售票總量。文中還有免費表演，不能假設每人必買一張票。

快速判斷：問票數須找幾張；人數、金額、比例都不能直接代替。文章的歷史及數據按原卷保留，這是在依本文作答，不當作現今活動資訊。''',
['文章及圖表明示有兒童表演，能得知。','每年持續超過三週，第一段有明確答案；不問創辦至今年數。','全文無每年售票張數，人數/票價/表演比例不能推出票數。','第二部分交代八劇團另覓場地演出並大受歡迎，能得知。'],34,student='B；使用者更正為C。',passage=fringe,images=['english-25-passage','english-25-question'],tables=[dict(caption='Different types of Performances at the Edinburgh Fringe Festival in 2016（原卷圓餅圖資料）',headers=['表演類型','比例'],rows=[['comedy（喜劇）','34%'],['theater（戲劇）','27%'],['music（音樂）','15%'],['children’s shows（兒童表演）','5%'],['others（其他）','19%']])],figures=[dict(src=img('english-25-map'),alt='原卷英國地圖標示Edinburgh位於Scotland',caption='原卷附圖：Map of Edinburgh, Scotland, the UK。'),dict(src=img('english-25-chart'),alt='2016年表演類型圓餅圖，喜劇34%、戲劇27%、音樂15%、兒童5%、其他19%',caption='原卷圓餅圖；精確比例另以可讀表格保留。')],mark='user訊息34明示25@錯題 b--c；完整閱讀文章、地圖、圓餅圖與第25題四選項可核。原卷23/24未問，不擴收。')
rv='When you feel too tired from your work, camping, for sure, is as a great way to run away from it for some time. However, if you want to have a great time, you should get everything ready before going camping. This is the reason why many people turn to RVs for help. An RV is like a moving house and takes you to almost everywhere in the world.\n\nThe idea of RVs started very early. In 1915, the Conklin family in the USA spent many months staying inside the car and driving from one city to another. They decorated their car just like a home. Inside it were a full kitchen, sofas and a small garden. By the mid-1920s, the car companies saw the growing need and started to make different moving homes for people to choose from.\n\nUntil now, RVs are a sign of our times. Many people don’t want to lose their free life by buying a very expensive house. So they would like to buy an RV for themselves because RVs allow them to work on the road and live freely at the same time. All in all, RVs are more than just a kind of car for camping, but they are a good choice for outdoor living.\n\n原卷字詞：decorate裝飾；company公司；outdoor戶外的。'
add('gpt056-english-35',35,'英文第35題｜依原文找露營車受歡迎的原因','What is the reason why RVs are popular today?',['People want to be their own boss.','The house price is getting too high.','People don’t want to live inside the house.','They can save money by going to different places.'],'B',
'''全文逐句翻譯
當你因工作感到非常疲倦時，露營無疑是暫時遠離工作的一種好方法。然而，若想玩得愉快，應在去露營前做好一切準備。這就是許多人尋求露營車協助的原因。露營車像會移動的房子，可以帶你到世界上幾乎任何地方。
露營車的構想很早就出現。1915年，美國Conklin一家花好幾個月住在車內，開車從一座城市到另一座城市。他們把車布置得像家。車內有設備齊全的廚房、沙發與小花園。到1920年代中期，汽車公司看見需求增加，開始製造不同的移動住宅供人選擇。
直到今日，露營車已是這個時代的一種象徵。許多人不想因買昂貴房子而失去自由生活。因此，他們想為自己買露營車，因為車讓人能在路上工作並同時自由生活。總之，露營車不只是露營用汽車，也是戶外生活的好選擇。
原卷首句確實印is as a great way；原文照留，正常敘述此意應為is a great way，多出的as不照教成正確句型。

詳解
題目問今日受歡迎的原因，重點在第三段。very expensive house指房子非常昂貴，接續So說人們因而選擇露營車，保有自由。B最貼近這個原因，答案B。精確而言，本文說房屋昂貴，沒有另外呈現房價上漲過程；按四選項比較，B仍最合。
A把在路上工作擴成想當老闆，本文沒說創業。C把不想因購買昂貴房屋而失自由，改成不想住在房屋裡，改動原因。D把前往不同地方當作省錢方法，本文沒有建立這個因果關係。

free life在此是自由生活，不是免費生活。不能把文章曾出現的昂貴房屋與去不同地方，任意拼成去不同地方就能省錢。

快速判斷：回到第三段找very expensive house→So的因果，核對選項是否保留原文關係。首次圖漏D已由同串後續附件補齊，本題四選項完整。''',
['原文說可在路上工作，未說要當老闆或創業。','最貼近房子非常昂貴這個原因；文中未另證房價上升過程。','文章不是討厭房屋，而是不想為昂貴房屋失去自由。','文章未說移動到不同地方能使人省錢，因果無依據。'],44,student='D；使用者更正為B。',passage=rv,images=['english-35-passage','english-35-question'],mark='user訊息44明示35@錯題 d--b，後續訊息52上傳原題補足D。主圖原文及補圖四選項均已實看；題本B為印刷解答。')
letter='Ask Julie\nAll you need to know about living in Novara\n\nDear Julie,\nI’m a newcomer to this country. Every day I experience cultural shocks here.\nTake yesterday for example. I was fined $60 for not keeping my dog, Charlie, on a leash at a small park. I really don’t know why. Since we live in a small apartment, if he stays inside for too long, he starts barking. But believe me, he’s a sweet boy. When I take him for a walk at the park and let him run free there, he is happy and lovely.\nI just don’t understand why I should keep a friendly dog on a leash all the time.\nTroubled Jack\n\nDear Troubled Jack,\nWelcome to Novara.\nI’m sorry to hear that you have to pay a $60 fine for breaking the leash law. In this country, dogs must be kept on a leash in public places to keep everyone safe, and this rule must be followed by every owner.\nNow you know about the leash law. Please follow it.\nThere will be more to learn about living in a new country. Please feel free to ask.\nJulie\n\n原卷字詞：cultural shock文化衝擊；fine罰款；leash牽繩；bark吠叫；law法律。'
add('gpt056-english-38',38,'英文第38題｜受罰經歷是寫信起因','Why does Troubled Jack write this letter?',['He had an unhappy experience.','He is going to move to a new country.','He wants to know more about leash laws.','He wants to keep a dog in a small apartment.'],'A',
'''全文逐句翻譯
Ask Julie：請教Julie。副標為在Novara生活，你需要知道的事。
親愛的Julie：我是剛來這個國家的新居民。每天我都在這裡經歷文化衝擊。
就拿昨天為例。我在小公園未替我的狗Charlie繫牽繩，因此被罰60元。我真的不知道為什麼。因為我們住在小公寓，牠若在屋裡待太久，就會吠叫。但請相信我，牠是溫和可愛的狗。我帶牠到公園散步，讓牠在那裡自由奔跑時，牠很開心可愛。
我就是不明白，為何必須一直替友善的狗繫牽繩。——煩惱的Jack。
親愛的煩惱的Jack：歡迎來到Novara。
聽說你違反牽繩法而必須付60元罰款，我很遺憾。在這個國家，為了保障大家安全，狗在公共場所必須繫牽繩，每位飼主都應遵守。
現在你知道牽繩法了，請遵守。在新國家生活還有更多要學習的事，有問題請隨時提出。——Julie。
本文的國家、法規與罰款為閱讀情境，依文意作答，不當成現實地方法規資訊。

詳解
依使用者原對話的C→A訂正與題本答案，採A。他先說每天遭遇文化衝擊，再以昨天因沒繫牽繩被罰60元為例，反覆說I really don’t know why與I just don’t understand why，受罰且困擾的經歷是促使他寫信的起點。
B說即將搬家，但newcomer表示他已來到此國。D說想養狗，但文中已養狗、已住小公寓，只是背景，不是新需求。
C與信中為什麼友善的狗仍須繫牽繩的疑問確有關，不能教成Jack完全不想了解法規。本題按題本判讀，A更直接概括整封信的起因；C較聚焦信中涉及的法規話題。保留這項概括範圍的細緻比較，不宣稱C毫無文字依據。

快速判斷：先分促使寫信的事件（受罰、困擾）與信中問題的主題（牽繩規則），再比較哪項更直接概括全信。這是原對話已明示的A及A/C範圍說明，不重新要求確認相同訂正。''',
['被罰60元並反覆困惑，是促使寫信的不愉快經歷，符合題本採A的概括。','newcomer說他已搬來，不是將要搬來。','確與信中疑問有關；按題本判讀，A更概括寫信起因，不能說C完全無據。','他已經養狗並住小公寓，這只是背景。'],62,student='C；使用者更正為A。',passage=letter,images=['english-38-passage','english-38-question'],mark='user訊息62明示38@錯題C--A；原圖兩封信與第38題完整，保留原對話A/C範圍比較，不把原user已指定的A重開同項確認。')
(D/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2)+'\n')
manifest=dict(sourceId='src-more-056',order=56,url=url,title=a['title'],date='2026-11-03',dateBasis='原使用者各題create_time之Asia/Taipei日期，無實際考試日',archivePath='docs/sources/6aea1969-2bc0-83ec-8b0d-f21da9cfed80.json',transcriptPath=str((D/'transcript.txt').relative_to(R)),questionPath=str((D/'questions.json').relative_to(R)),questionSHA256=hashlib.sha256((D/'questions.json').read_bytes()).hexdigest(),questionCount=6,originalQuestionCount=6,groupCount=0,allOriginalsVisuallyChecked=True,originalsAvailable=7,originalsExpected=7,items=items,skips=[dict(kind='source_unasked_originals',reason='藝穗節第23/24題及Jack第39題未由user指定，不擴收。'),dict(kind='supplement_attachment_not_new_question',reason='第7張上傳附件依bytes為原圖chatgpt-6aea1969-3.png，補原第35題D選項，不另算一題。'),dict(kind='source_ai_generated',reason='來源AI圖及最後將內容優化為資訊圖表的操作不另建錯題；未採任何來源AI解說圖。')],reviews=[],notes=['本批依user明示@錯題/錯選→訂正收題；藍色印刷解答不是學生紅筆。','q35原印is as a great way保留，解說釐清；q38既有A/C語意範圍說明保留，未新增或改答。','原AI第1題早先誤說省略call，已在同串訊息8自行更正；採原題完整another call，不把已撤回說法當現行答案。'],state='ready',producer='/root/comic_lane_3',readyAt=datetime.now(timezone.utc).isoformat())
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('ready',len(questions))
