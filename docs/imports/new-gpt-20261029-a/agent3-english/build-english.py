import json
from pathlib import Path
P=Path('docs/imports/new-gpt-20261029-a/agent3-english')
source=json.loads(Path('docs/imports/new-gpt-20261029-a/source.json').read_text());(P/'source.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
market="""Do you shop for food at supermarkets or traditional markets? How often do you go there? Let us know your views.

Jenny
I like supermarkets better. I go there three or four times a week. Supermarkets are big and clean. Besides, they have air conditioning. I feel comfortable when shopping at supermarkets. I am always worried about the dirty floor at traditional markets. And the fish or meat there may not be as fresh as that at supermarkets. These are two of the drawbacks.

Tom
I cook every day. I enjoy shopping for meat, fish, and vegetables at a traditional market near my home every morning. At traditional markets, I can always buy the freshest food because some farmers sell the food from their own farms or gardens. It's also interesting to have a talk with the stand owners. Going shopping at supermarkets will not be so much fun. I go to the supermarket only twice a month.

Ben
I like supermarkets more. I usually shop at a supermarket twice a week. Everything has a price tag. That makes shopping easier.

Linda
Supermarkets run more than 8 hours a day. For office workers like me, going shopping at supermarkets is more convenient because many traditional markets are only open in the morning or between 2 p.m. and 6 p.m. I shop at a supermarket on Saturdays.

字詞：traditional 傳統的；view 觀點；air conditioning 空調設備；tag 標籤。"""
chat="""Happy Group (9)

Jim
Good news! Since this September, Sunshine Supermarket on Park Street has had a “quiet hour” between 10:30 and 11:30 on Wednesdays for people with autism. This is because they struggle with loud music and noise in a store. During this hour, the clerk will turn off TVs and music, so they will be able to shop more comfortably. What do you think of the news?

Lucy
Thank you, Jim. I avoid taking Mary to supermarkets because they are too noisy for her. I think the quiet hour in the supermarket is what we need. I'll take her there on a Wednesday morning.

Carrie
I don't think an hour is enough. What's more, 10:30–11:30 a.m. is an office hour. Though a “quiet hour” is what I've been waiting for years, how can I shop at Sunshine Supermarket at that time?

Mark
I don't agree with Carrie. The “quiet hour” is a good start to be friendly to those with autism. I hope more and more stores will care about people with special needs. I'll share the news with my boss. Maybe there will be a “quiet hour” in our bakery for people with autism.

Kent
Mark is right. People with autism and their family need support. We should all help them live a better life. I think Sunshine Supermarket is doing the right thing.

字詞：autism 自閉症；struggle 掙扎；support 支持。"""
rows=[(862,15,'代名詞與形容詞片語',"Jessie was so surprised when she entered her room. That was because _____ full of many beautiful roses.",['there was','they were','it was','there were'],'C','D','空格後是full of many beautiful roses，構成be full of「充滿」。所描述的是前句單數her room，因此用it指房間；前文為過去式was，接it was，選C。many roses雖為複數，卻在of後作片語的一部分，不是這一句要代替的主詞。there was／there were為存在句型，不能直接接這裡的full of片語取代it was；they were也沒有合適的複數先行詞。完整意思是：她驚訝，因為房間裡滿是美麗玫瑰。',['there was表示有某事物，後面需要合適名詞結構，不能直接代入本空。','房間是單數，不能被of後的roses誤導改用they。','it回指her room，was與前文過去敘事一致；be full of結構完整。','there were存在句型與複數形式都不合此處房間描述。']),
(864,16,'地點之間的問句',"Remy: _____ is it from your home to the post office?\nAngel: It's 5 minutes by bike.",['How long','How far','How soon','How often'],'B','A','How far is it from A to B?用來詢問兩地之間的距離，所以選B。回答用「騎車5分鐘」表達路程遠近，在這種問路情境很常見；不能只看到minutes就一律填How long。How long通常詢問一段時間，旅行時間常用How long does it take ...?；How soon問還要多久將發生，How often問頻率，都不合本題兩地之間的句型。',['常問持續多久，問交通時間常用How long does it take，不是本題的距離句型。','How far is it from A to B?與地點間距離吻合。','問多久以後發生，常用in加一段時間回答，不是本題。','問多常發生，應答為頻率，不是騎車路程。']),
(866,35,'購物偏好的人數',"How many of the four people like supermarkets more?",['One.','Two.','Three.','Four.'],'C','B','逐人判斷偏好，不只數直接出現more的人。Jenny說like supermarkets better；Ben說like supermarkets more；Linda說超市對自己較方便，並在週六去超市。三人偏好超市。Tom喜歡每天到傳統市場買菜、與攤商聊天，超市一個月才去兩次，因此不算在偏好超市的人中。共三人，選C。比較級better、more及more convenient都能提供偏好線索，不能把不同說法漏算。',['只算一人會漏掉其他等義偏好線索。','只算明說like的兩人，會漏掉Linda較方便的說明。','Jenny、Ben、Linda，共三人。','Tom偏好傳統市場，不能四人全算進去。']),
(868,36,'購物頻率與比較基準',"Who goes shopping at supermarkets less often than Ben?",['Jenny and Tom.','Only Tom.','Only Linda.','Linda and Tom.'],'D','B','比較基準是Ben：每週去超市兩次。Jenny每週三、四次，比Ben多；Linda固定週六去，一般每週一次，比Ben少；Tom每月僅兩次，也比Ben每週兩次少。所以Linda和Tom都符合，選D。每週兩次與每月兩次，數字同為two但期間不同，頻率不能視為相同；Linda的星期六也要轉成每週一次來比較。',['Jenny每週三、四次，比Ben多，所以此組錯。','Tom符合，但少算Linda。','Linda符合，但少算Tom。','Linda每週一次、Tom每月兩次，都比Ben每週兩次少。']),
(870,41,'avoid的上下文語意',"What does avoid mean?",['To keep away from.','To enjoy.','To begin.','To remember.'],'A','C','Lucy說I avoid taking Mary to supermarkets because they are too noisy for her，意思是因為超市對Mary太吵，會避免帶她去。後文安靜時段符合需要，便打算帶她前往，也支持avoid是「避免、避開」，選A To keep away from。原句avoid後接taking這個V-ing形式。B享受、C開始、D記得都不符合因為太吵而暫時避開的語境。她避免的是帶Mary到嘈雜的環境，不是在避免或排斥Mary本人。',['avoid有避免、避開之意，符合因太吵而暫不前往。','enjoy是享受，與避開噪音語境不合。','begin是開始，不能表達本句因太吵而不去。','remember是記得，與上下文行為原因不同。'])]
for n,num,title,stem,opts,ans,student,exp,reasons in rows:
 q={'id':f'q-{n}','sourceId':'src-more-049','subject':'English','title':f'英文第{num}題｜{title}','volume':'綜合','chapter':'綜合','date':'2026-10-29','dateLabel':'首次出題日期','addedAt':'2026-10-29','question':stem+'\n'+'\n'.join(f'({chr(65+i)}) {v}' for i,v in enumerate(opts)),'answer':f'({ans}) {opts[ord(ans)-65]}','explanation':exp,'optionAnalysis':[{'label':chr(65+i),'text':v,'wordClass':'應選' if chr(65+i)==ans else '不選','meaning':'','explanation':reasons[i]} for i,v in enumerate(opts)],'correctOption':ans,'studentAnswer':student,'passage':market if n in [866,868] else chat if n==870 else '', 'tables':[],'questionFigures':[],'images':[],'explanationFigures':[],'contentStatus':'完整原題','verification':'原卷逐題核對','verificationNote':'已實看原卷本題、完整四選項及閱讀材料；原問以外的小題不收入。','sourceLabel':f'分享原卷｜第{num}題','trap':'依完整句型或上下文核對，不只抓一個單字或數字。','tags':['英語閱讀' if n>=866 else '英語文法'],'status':'todo','starred':False,'notes':'','diagram':''}
 (P/'questions'/f'q-{n}.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
print('5 English drafts; no shared edits')
