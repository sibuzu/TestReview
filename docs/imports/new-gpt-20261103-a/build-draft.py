from pathlib import Path
import json,hashlib,datetime,zoneinfo,copy
R=Path('/home/jack/git/TestReview');D=R/'docs/imports/new-gpt-20261103-a';D.mkdir(exist_ok=True)
archive=json.loads((R/'docs/sources/6ae8b58d-7da4-83ee-a45e-4046864af26f.json').read_text())
url=archive['url'];sid='src-more-053'
def save(name,data):
 p=D/name;p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def digest(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def asset(name):return 'docs/imports/new-gpt-20261103-a/originals/'+name

def base(n,title,stem,options,correct,exp,analysis,tags,images,student,mi):
 m=archive['messages'][mi];ts=m['create_time']; dt=datetime.datetime.fromtimestamp(ts,zoneinfo.ZoneInfo('Asia/Taipei'))
 return dict(id=f'gpt053-original-{n}',sourceId=sid,subject='English',title=title,chapter='綜合',volume='綜合',date=dt.date().isoformat(),dateLabel='首次出題日期',question=stem+'\n'+'\n'.join(f'({k}) {t}' for k,t in zip('ABCD',options)),answer=f'({correct}) {options["ABCD".index(correct)]}',explanation=exp,trap='',verification='原卷逐題核對',verificationNote='已實看真正使用者上傳的原卷及裁切成品，核對完整題幹、四個選項與必要閱讀文；冊次及教材章節無證據，歸綜合。日期取首次提問訊息的台灣日期，非實際考試日期。',diagram='',tags=tags,images=images,sourceLabel=f'分享原卷｜第{n}題',studentAnswer=student,contentStatus='完整原題',correctOption=correct,passage='',optionAnalysis=[dict(label=k,text=t,wordClass='應選' if k==correct else '不選',meaning='',explanation=a) for k,t,a in zip('ABCD',options,analysis)],tables=[],questionFigures=[],explanationFigures=[],originalQuestionNumber=str(n),sourceEvidence=dict(url=url,messageIndex=mi,messageId=m.get('id'),firstQuestionTimestamp=ts,firstQuestionDateTime=dt.isoformat(),originalCropPaths=images,originalImageHashes={p:digest(p) for p in images},inclusionEvidence=f'使用者訊息指定「{next((p for p in m["content"]["parts"] if isinstance(p,str)),"")}」，且原卷題號{n}旁有紅筆訂正；已實際核看。'))

q6=base(6,'英文第6題｜Never開頭的禁止句',
'Never _____ to Mr. Robinson like that again, or you might lose your job. You have to keep that in mind.',
['to talk','talk','talking','not talk'],'B',
'本句是在提醒對方「絕對不要再那樣跟羅賓森先生說話，否則你可能會丟掉工作；你必須記住這件事」。省略主詞you的祈使句以動詞原形開頭；本題用Never加強禁止語氣，因此結構是Never＋原形動詞talk，選B。\n\nNever已表達「絕對不」，本句不再加not；to talk與talking也不符合這裡的祈使句結構。or在此接續「否則」的後果，不會使前面的命令改成to V或V-ing。\n\n判讀時先辨認這是對人的命令或勸告，再套用Never＋原形動詞。不是所有含never的英文句子都固定接原形，例如She never talks like that是有主詞的一般現在式敘述句。',
['to talk是不定詞；本題禁止祈使句需要直接使用動詞原形。','talk是動詞原形，符合Never＋原形動詞的禁止祈使句。','talking是V-ing形式，不符合本句的祈使句結構。','本句以Never表達禁止，直接接talk即可；再加not不符合預期的禁止意思。'],
['祈使句','Never','動詞原形'],[asset('original-6.png')],'原卷紅筆訂正B；藍筆原選遭覆寫，未據此猜定。',1)

q12=base(12,'英文第12題｜花費動詞的主詞與受詞',
'It only _____ me 20 dollars to buy those plates. They were not as expensive as our old ones.',
['cost','took','spent','paid'],'A',
'句意是「買那些盤子只花了我20元。它們沒有我們舊的盤子那麼貴」。本句用It作形式主詞，真正的事情是後面的to buy those plates；中間依序接人me與金額20 dollars，符合It cost＋人＋金錢＋to V，因此選A。\n\n後句were表示談過去的情況。cost的原形、過去式、過去分詞同形，這裡的cost是過去式，不能因為結尾沒有-ed就排除。\n\n比較國中常用句型：物／It＋cost＋人＋錢；It＋take＋人＋時間＋to V；人＋spend＋錢／時間＋on名詞或V-ing；人＋pay＋錢＋for物。這一題不是只看「花錢」的中文，而是同時看主詞It、受詞me和金額的排列。\n\n後句not as expensive as意為「不如……昂貴」；our old ones中的ones代替前面複數的plates，指我們原來的那些盤子。',
['cost可用物或It作主詞，後接人與金額；cost過去式同形，符合本句。','國中常見It took＋人＋時間＋to V表示做事花多少時間；本題20 dollars是金額，不符合此句型。','spend通常以人作主詞；要改成I spent 20 dollars on those plates或I spent 20 dollars buying those plates。','pay通常以人作主詞；可說I paid 20 dollars for those plates，不能直接放入本題It＋空格＋me＋金額結構。'],
['花費動詞','cost','take','spend','pay','代名詞ones'],[asset('original-12.png')],'D（原卷藍筆），紅筆訂正A。',15)

q31=base(31,'英文第31題｜店家回覆的主要目的',
'What is the reply from the owner of Lily Pie mainly for?',
['To ask Zack W to say sorry.','To show their thanks to Zack W.','To invite Zack W to try their pie again.','To give the full picture of that day.'],'D',
'題目問「Lily Pie店主的回覆主要是為了什麼」。要看整段回覆的主要作用，不能只以第一句thank you判斷。\n\nZack的評論說店家一小時才接電話、四點就接近打烊，而且派又乾又硬，懷疑不是當天做的。店主逐項補充：第一次來電就有接聽，但Zack沒說話就掛斷；當天因朋友婚禮而四點關門，已在一週前公告並在電話中告知；派雖可能不合顧客喜好，卻都是當天早上現烤。這些內容的共同作用是補充事件另一方的經過，讓讀者了解當天完整情況，因此選D。\n\nA把道歉的方向看反了：We are sorry是店家向Zack表達歉意，不是要求Zack道歉。B雖抓到開頭道謝，卻無法涵蓋後面大量解釋。C所說邀請Zack再試派，文中沒有出現。the full picture在此是「事情的全貌、完整情況」，不是一張完整照片。\n\n閱讀評論與回覆時，也要分清兩方說法：評論中的「一小時才接」與店主回覆的「第一次就接了」是各自的陳述；本題考回覆目的，不要求替兩方裁定事實。',
['要求Zack道歉；回覆中的We are sorry是店家自己致歉，沒有要求Zack道歉。','向Zack致謝；開頭確實道謝，但主要篇幅是解釋電話、營業時間和派的新鮮程度，這不是最完整的主旨。','邀請Zack再次品嚐派；文中沒有提出此邀請。','說明當天完整情況；回覆逐項補充評論未呈現的經過，最能涵蓋整段目的。'],
['閱讀理解','寫作目的','評論與回覆','the full picture'],[asset('original-31-passage.png'),asset('original-31-question.png')],'A（原卷藍筆），紅筆訂正D。',23)
q31['passage']='''Lily Pie
About　Opening Hours　Menu　Review　Photos

Zack W
5 Reviews
★　2 days ago

I don't even want to give Lily Pie one star. I'm simply doing this to let everyone know about my terrible experience. That day, I didn't want to wait, so I called to place my order. It took them one hour to pick up the phone! Then, they told me to go there directly because there was no one waiting in line. I went there at around 4, but they were almost closed. There were only the last two pieces of pie in the shop. Well, if you close at 4, you should write 4, not 5:30, on your notice of opening hours! I still bought the two pieces, and that was a big mistake. They didn't taste fresh at all. They were dry and hard. They probably didn't bake them that day. I'll never buy anything from Lily Pie again.

Lily Pie (Owner)
1 day ago

Dear Zack, thank you for your review. We are sorry for your bad experience. We did pick up when you first called, but you hung up without saying anything. We closed at four because it was the wedding day of one of our good friends. We posted the time change a week ago, and we also told you about that on the phone. As for the pies, we baked each of them that morning. They might be too hard or dry for you, but they were 100% fresh.

原卷字詞提示：review 評論；directly 直接地；owner 業主；wedding 婚禮；reply 回覆。'''

q42=base(42,'英文第42題｜寄卡片習慣的由來','42. _____',
['I can learn to paint like the artists','I started doing this',"I wouldn't know about the artists","I don't have enough money to buy cards"],'B',
'第42空接在Thanks to my parents之後。前兩句先說作者每年寄出數百張口足畫家卡片，最後一段再交代原因：作者原本購買許多協會商品，因東西太占空間而與父母爭執，最後讓步，改成只買卡片並全部寄出去。父母促使作者開始「買卡片並寄出」的做法，因此選B：I started doing this。\n\nthis指向前文寄卡片的習慣，並由最後一段的decided to buy cards only and send all of them out補足背景。Thanks to my parents在這裡承接這件事的由來，不是說父母教作者畫畫，也不是說作者沒有買卡片的錢。\n\nC的wouldn\'t know表示「就不會知道」，既不符合全文已認識畫家的事實，也無法接出父母促成寄卡片習慣的因果。D的沒錢沒有文章證據。',
['作者沒有說學習口足繪畫；前後文談的是購買與寄送卡片。','表示「我開始做這件事」；this指購買並寄送卡片，對應最後一段父母促成的改變。','表示「我就不會知道這些藝術家」；和文章已知畫家、父母促成新做法的脈絡不合。','表示「我沒有足夠的錢買卡片」；文章沒有缺錢線索，反而說作者每年寄出數百張卡片。'],
['篇章填空','因果關係','指代','thanks to'],[asset('original-42-43.png')],'A（原卷藍筆），紅筆訂正B。',30)
q43=base(43,'英文第43題｜支持藝術家的方式','43. _____',
['but there was no way to do this',"but I didn't have much money",'so I sent money to them every month','so I could meet them in person'],'A',
'第43空前說作者長大後試著捐款感謝藝術家，空格後卻說只能透過口足畫家協會幫助他們。後面進一步解釋協會不接受捐款，而是將作品製成商品販售，讓藝術家靠銷售賺錢。作者想直接捐款卻做不到，前後是轉折，所以選A：but there was no way to do this。\n\n這裡的this指前面的make donations（捐款），和第42題this所指的寄卡片做法不同。作者後來改用購買商品支持藝術家，不是完全沒有任何支持方式；「沒有辦法」限於此處想直接捐款的做法。\n\nB雖也用but，卻把原因換成缺錢，文章沒有這個訊息。C說每月寄錢，與不接受捐款的說明不合。D說親自見藝術家，文中未提到這個目的。',
['「但是沒有辦法這麼做」的this指直接捐款，符合協會不收捐款及後文購買商品的限制。','「但是我沒有很多錢」；文章沒有說作者缺錢，限制在協會不收捐款。','「所以我每月寄錢給他們」；和協會不接受捐款的說明不合，也沒有每月寄錢的資訊。','「所以我可以親自見到他們」；文章沒有提到見面的目的，無法連接後文的購物支持。'],
['篇章填空','轉折','上下文線索','捐款與購買'],[asset('original-42-43.png')],'B（原卷藍筆），紅筆訂正A。',30)
passage='''I send hundreds of cards every year, even to friends of friends. The cards are all from mouth and foot painting artists. Thanks to my parents, __42__.

I first learned about mouth and foot painting artists when I was only 9. Their paintings were so beautiful, and it was hard to believe the artists painted them only with their mouths or feet. Their stories touched me and gave me the power to get through many difficult times.

I tried to make donations to thank these great artists after I grew up, __43__. I could only help them through the Association of Mouth and Foot Painting Artists. The association helps put the artists' works on different items for sale. People can buy things like bags, cups, and so on. The association doesn't take any donations because it means a lot to the artists to be able to sell these items to make money.

I used to buy different things from the association until they took up too much space in my house. After a big fight with my parents over that, I gave in and decided to buy cards only and send all of them out. To my surprise, it turned out to be an even better idea!

原卷字詞提示：painting 繪畫；artist 藝術家；donation 捐款；association 協會。'''
group=copy.deepcopy(q42)
group.update(title='英文題組｜口足畫家的卡片與支持方式（第42、43題）',question='【第42題】\n'+q42['question']+'\n\n【第43題】\n'+q43['question'],answer='【第42題】'+q42['answer']+'\n【第43題】'+q43['answer'],explanation='【第42題】\n'+q42['explanation']+'\n\n【第43題】\n'+q43['explanation'],studentAnswer='【第42題】'+q42['studentAnswer']+'\n【第43題】'+q43['studentAnswer'],originalQuestionNumber='42、43',correctOption='',optionAnalysis=[],passage=passage,tags=list(dict.fromkeys(q42['tags']+q43['tags'])),groupQuestions=[q42,q43],groupMetadata=dict(kind='original_paper',printedRange='原卷同一篇口足畫家卡片文章，第42、43空',draftMembers=[q42['id'],q43['id']],representativeSubjectReason='兩小題皆為同一英文文章的篇章填空，各自保留完整選項與答案。'))
group['sourceEvidence']['inclusionEvidence']='使用者訊息明確指定「42、43@錯題」；原卷第42紅筆B、第43紅筆A，共同文章及兩題四個選項均已實看核對。'
qs=[q6,q12,q31,group];save('questions.json',qs)
save('source.json',dict(id=sid,order=53,url=url,title=archive['title'],date='2026-11-02',dateLabel='首次出題日期',dateBasis='使用者首問create_time 1793628943.76839轉Asia/Taipei為2026-11-02T22:15:43.768390+08:00；不是實際考試日期。',transcriptPath='docs/imports/new-gpt-20261103-a/transcript.txt',archivePath='docs/sources/6ae8b58d-7da4-83ee-a45e-4046864af26f.json',state='ready',scope='只收入使用者指定且原卷有紅筆訂正的6、12、31、42、43；42/43合組，未問原卷題及AI延伸不收。'))
transcript='\n\n'.join(m['author']['role']+'\n'+'\n'.join(p if isinstance(p,str) else '[使用者原卷附圖]' for p in m.get('content',{}).get('parts',[])) for m in archive['messages'] if m['author']['role'] in ['user','assistant'])
(D/'transcript.txt').write_text(transcript+'\n')
manifest=dict(sourceId=sid,url=url,status='ready',producer='/root/comic_lane_2',questionPath='docs/imports/new-gpt-20261103-a/questions.json',questionSHA256=digest('docs/imports/new-gpt-20261103-a/questions.json'),originalQuestionCount=5,questionPageCount=4,originalQuestionNumbers=[6,12,31,42,43],sourceAIImagesAdopted=False,teachingComicState='queued_after_intake',pendingReviews=[],skips=[dict(kind='unasked_printed_question',numbers=[4,5,7,8,9,10,11,29,30],reason='同張原卷包含其他題，但使用者未問；不因同卷或有紅字就擴張本次範圍。'),dict(kind='ai_generated_extension',reason='來源中的cost小測驗及兩題考前自測為AI另編，非原卷錯題，排除。')],visualReview=dict(originalsViewed=[f'docs/source-pages/chatgpt-6ae8b58d-{n}.jpg' for n in range(1,5)],cropsViewed=[asset(n) for n in ['original-6.png','original-12.png','original-31-passage.png','original-31-question.png','original-42-43.png']],allOriginalsReadable=True,allCropsComplete=True,checkedOriginalText=True,checkedAllOptions=True,checkedNecessaryMaterials=True,checkedAnswers=True,notes='第6藍筆原選遭覆寫，不猜原作答；紅筆B清楚，題幹與四選項完整。第31完整保留評論與店主回覆，未只摘取AI引用段落。'),dedupe=dict(keywords=['Mr. Robinson','those plates','Lily Pie','mouth and foot'],indexSearchResults='all empty at initial exact distinctive keyword queries; further candidates report stored separately',exactContentChecked=True))
save('manifest.json',manifest)
print('ready',len(qs),'pages',5,'original questions')
