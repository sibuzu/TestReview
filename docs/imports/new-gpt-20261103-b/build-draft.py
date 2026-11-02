from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
D=Path(__file__).parent;ROOT=D.parents[2]
archive=json.loads((ROOT/'docs/sources/6ae8b5b9-d8d8-83ee-991b-3fffcf6219e2.json').read_text())
source='https://chatgpt.com/share/6ae8b5b9-d8d8-83ee-991b-3fffcf6219e2'
questions=[];items=[]
def add(key,no,subject,title,stem,options,answer,explanation,analyses,passage='',student='',images=None,index=0,mark=''):
 ims=[str((D/'originals'/f'{x}.webp').relative_to(ROOT)) for x in images or []]
 q=dict(id=key,sourceId='src-more-054',subject=subject,title=title,chapter='綜合',volume='綜合',date='2026-11-02',dateLabel='首次出題日期',question=stem+'\n'+'\n'.join(f'({lab}) {text}' for lab,text in zip('ABCD',options)),answer=f'({answer}) {options["ABCD".index(answer)]}',explanation=explanation,trap='',verification='原卷逐題核對',verificationNote='已實看原卷及本題裁圖，核對完整題幹、四選項與必要文章；日期取原始使用者提問訊息的台灣日期，未提供實際考試日期。',diagram='',notes='',status='todo',starred=False,tags=[title.split('｜')[-1]],images=ims,sourceLabel=f'分享原卷｜第{no}題',studentAnswer=student,contentStatus='完整原題',correctOption=answer,passage=passage,optionAnalysis=[dict(label=lab,text=text,wordClass='應選' if lab==answer else '不選',meaning='',explanation=why) for lab,text,why in zip('ABCD',options,analyses)],tables=[],questionFigures=[],explanationFigures=[],originalQuestionNumber=str(no))
 questions.append(q)
 m=archive['messages'][index];p=next(x for x in m['content']['parts'] if isinstance(x,dict) and x.get('content_type')=='image_asset_pointer')
 raw=next(x for x in (ROOT/'docs/source-pages').glob('chatgpt-6ae8b5b9-*.jpg') if x.stat().st_size==p['size_bytes'])
 items.append(dict(key=key,originalQuestionNumber=str(no),messageIndex=index,messageId=m['id'],messageCreatedAt=datetime.fromtimestamp(m['create_time'],ZoneInfo('Asia/Taipei')).isoformat(),sourceOriginal=str(raw.relative_to(ROOT)),sourceOriginalSHA256=hashlib.sha256(raw.read_bytes()).hexdigest(),attachment=p['asset_pointer'].split('?')[0],inclusionEvidence=mark,crops=[dict(path=x,sha256=hashlib.sha256((ROOT/x).read_bytes()).hexdigest(),visuallyChecked=True) for x in ims],answerVerified=True,duplicateDecision='new',originalAIError=False))
add('gpt054-chinese-02',2,'Chinese','國文第2題｜樹木榮衰與國運','根據上文，下列關於先民對樹木認知的敘述何者最恰當？',['實用的效益攸關生計','榮衰與時局安危有關','變異緣於主政者失德','榮枯取決於栽植技巧'],'B',
'''解題關鍵是「特定樹木的枯疏與否，則與當朝國運密切相關」。B以「榮衰」對應樹木的狀態，以「時局安危」對應國運，最符合原文。

A談木材、果實等實用價值及民生，但文章沒有討論這些用途。C把「徵兆、象徵」改成「主政者失德造成變異」，增加了文中沒有的因果關係，而且連理木反而象徵君王有德，不能把所有變異都說成失德。D談種植技巧，也不是本文所述先民的信仰解讀。

快速判斷：找到「國運密切相關」，再比對同義的「時局安危有關」。本文在說明古人的觀念，作答依文章內容，不自行加入現代植物學解釋。''',
['文章未談樹木的實用價值及生計。','樹木榮衰對應枯疏狀態，時局安危對應當朝國運。','原文說象徵及相關，未說失德造成變異；連理木還象徵有德。','原文未討論栽植方法。'],
'「先民認為上天藉自然現象，傳達與人事相應的啟示。樹木天然的變異現象，遂成了政治上的吉祥徵兆。例如異根連枝的『連理木』，象徵君王有德，獲得上天肯定。而特定樹木的枯疏與否，則與當朝國運密切相關。」\n（節錄改寫自國立故宮博物院南部院區〈「樹：從信仰到抒情」展覽簡介〉）',student='原選項筆跡重疊，不強判；紅筆訂正B。',images=['chinese-02'],index=0,mark='使用者明確輸入2@錯題；原卷第2題左側紅B覆於藍筆答案上，紅筆B清楚。')
poem='嗟君此別意如何，駐馬銜杯問謫居。\n巫峽啼猿數行淚，衡陽歸雁幾封書。\n青楓江上秋帆遠，白帝城邊古木疏。\n聖代即今多雨露，暫時分手莫躊躇。\n——高適〈送李少府貶峽中王少府貶長沙〉'
add('gpt054-chinese-23',23,'Chinese','國文第23題｜送別詩中的想像景物','有關上述詩歌的內容，下列說明何者最恰當？',['送別的對象只有一人','作者在巫峽送別友人前往衡陽','詩中描寫了友人貶謫之地的景觀','作者有預感這次分別後將永不再相見'],'C',
'''逐句白話
「嗟君此別意如何」：唉，朋友這次即將遠別，心中有何感受？「君」是對友人的稱呼，不能只據此認定只有一人。
「駐馬銜杯問謫居」：停馬舉杯，關心朋友遭貶後將去的地方。「謫」指降職或被貶。
「巫峽啼猿數行淚」：想到峽中淒切的猿聲，彷彿令人流下數行眼淚。
「衡陽歸雁幾封書」：想到衡陽的歸雁，又能帶回朋友幾封書信？以雁寄託通信的盼望。
「青楓江上秋帆遠」：想像青楓江上，秋日船帆漸行漸遠。
「白帝城邊古木疏」：想像白帝城旁，古老樹木稀疏，景象清冷。
「聖代即今多雨露」：如今聖明時代多有恩澤；雨露比喻朝廷恩惠，含有勸慰、盼友人再受起用之意。
「暫時分手莫躊躇」：我們只是暫時分別，別為此徘徊不前、憂傷遲疑。

詳解
詩題寫明李少府貶往峽中、王少府貶往長沙，是送別兩位友人。巫峽、衡陽、青楓江、白帝城及猿聲、歸雁、秋帆、古木，是對友人貶謫之地及遠行景象的描寫、想像，故C最合適。

A忽略詩題中的兩個人。B把詩中出現的地名直接當成詩人送別地與友人的目的地，原詩沒有說作者在巫峽送人去衡陽。D與「暫時分手」及結尾勸慰的語氣不符，沒有永不相見的預言。

快速判斷：先拆詩題的兩人、兩個貶謫去處，再分清眼前送別與想像遠方。''',
['詩題有李少府、王少府兩位友人。','詩句地名不能直接當作作者所在地與友人路線。','猿、雁、秋帆、古木等描寫或想像貶謫之地景觀。','暫時分手及莫躊躇是在勸慰，並非預言永別。'],poem,student='B；紅筆訂正C。',images=['chinese-23'],index=34,mark='使用者輸入23@錯題；原卷第23題詩框左側紅C覆藍B，全部詩文及四選項可讀。')
li='李姬者名香，母曰貞麗。貞麗有俠氣，嘗一夜博，輸千金立盡。所交接皆當世豪傑，尤與陽羨陳貞慧善也。姬為其養女，亦俠而慧，略知書，能辨別士大夫賢否，張學士溥、夏吏部允彝亟稱之。少，風調皎爽不群；十三歲，從吳人周如松受歌玉茗堂《四傳奇》，皆能盡其音節。尤工〈琵琶詞〉，然不輕發也。\n——節錄自侯方域〈李姬傳〉\n\n注釋：①亟：時常、屢次。②皎爽：高潔爽朗。'
add('gpt054-chinese-39',39,'Chinese','國文第39題｜李姬傳的文言字義','根據本文，下列文句的解說何者最恰當？',['嘗一夜博——嘗試和別人在晚上賭博','所交接皆當世豪傑——承繼家業的人都是當地出名的人物','亦俠而慧，略知書——性格也仗義又聰明伶俐，還稍微讀了些書','尤工〈琵琶詞〉，然不輕發——特別會寫〈琵琶詞〉，但不輕易發表'],'C',
'''逐句白話
「李姬者名香，母曰貞麗」：李姬名叫香，母親叫貞麗。
「貞麗有俠氣，嘗一夜博，輸千金立盡」：貞麗有豪俠氣概，曾有一晚賭博，千金立刻輸光。「嘗」是曾經。
「所交接皆當世豪傑，尤與陽羨陳貞慧善也」：她交往的都是當時的豪傑，尤其和陽羨的陳貞慧交好。「善」是交好。
「姬為其養女，亦俠而慧，略知書，能辨別士大夫賢否」：李姬是貞麗的養女，也仗義聰明，稍通文墨，能分辨士大夫是否賢能。
「張學士溥、夏吏部允彝亟稱之」：張溥學士和任吏部官的夏允彝經常稱讚她。「之」指李姬。
「少，風調皎爽不群」：她年少時，風度氣質高潔爽朗，與眾不同。
「十三歲，從吳人周如松受歌玉茗堂《四傳奇》，皆能盡其音節」：十三歲時，向吳地人周如松學唱玉茗堂《四傳奇》，都能充分掌握曲調節奏。「受歌」是學唱。
「尤工〈琵琶詞〉，然不輕發也」：尤其擅長演唱〈琵琶詞〉，卻不隨便開口唱。「尤」是尤其，「工」是擅長，「發」依演唱語境解為發聲演唱。

詳解
C逐字符合「俠＝仗義、慧＝聰明、略知書＝稍通文墨」，答案C。
A把曾經誤作嘗試。B把交往誤作承繼，把當時世上誤作當地。D雖讀來通順，卻把前文受歌、音節建立的演唱情境改成寫作、發表。

快速判斷：文言字義須前後對照；受歌→音節→尤工→不輕發，是學唱到演唱的線索。不能把所有文章中的「發」都固定解成發表，也不能一律解成唱歌。''',
['嘗是曾經，不是嘗試。','交接是交往，當世是當時世上，均非選項所說。','俠、慧、略知書的解釋均符合文意。','受歌、音節說明工是擅長演唱，不輕發是不隨便開口唱。'],li,student='D；紅筆訂正C。',images=['chinese-39'],index=57,mark='使用者輸入39@錯題；原卷第39題左側紅C覆藍D，全篇文章、注釋及四選項可讀。')
pearl='凡珠在蚌，如玉在璞。初不識其貴賤，剖取而識之。自五分至一寸五分徑者為大品。小，平似覆釜，一邊光彩微似鍍金者，此名璫珠，其值一顆千金矣。古來「明月」、「夜光」，即此便是。白晝晴明，簷下看有光一線閃爍不定，「夜光」乃其美號，非真有昏夜放光之珠也。次則走珠，置平底盤中，圓轉無定歇，價亦與璫珠相仿（化者之身受含一粒，則不復朽壞，故帝王之家重價購此）。次則滑珠，色光而形不甚圓。次則螺蚵珠，次官雨珠，次稅珠，次蔥符珠。幼珠如粱粟，常珠如豌豆。卑而碎者曰璣。自夜光至于碎璣，譬均一人身，而王公至于氓隸也。\n——節錄改寫自《天工開物》\n\n注釋：①小：略。②釜：鍋子。③化者：死去者。④氓隸：百姓。'
add('gpt054-chinese-42',42,'Chinese','國文第42題｜夜光珠的美稱與實際特性','曉明是古代珍珠特展的策展人員，他發現簡介的標牌有一張錯誤，必須撤換。請問是下列哪一張？',['螺蚵珠：價值高於官雨珠與稅珠','滑珠：色澤光亮，但形體並不圓潤','走珠：能防腐，故帝王家多重金收購','夜光珠：以能在夜間發光而聞名於世'],'D',
'''逐句白話
「凡珠在蚌，如玉在璞」：珍珠藏在蚌中，就像玉藏在未經雕琢的玉石中。
「初不識其貴賤，剖取而識之」：起初不知道珍珠價值高低，要剖蚌取出才能知道。
「自五分至一寸五分徑者為大品」：直徑從五分到一寸五分的屬大顆上品。
「小，平似覆釜，一邊光彩微似鍍金者，此名璫珠，其值一顆千金矣」：略微扁平，像倒扣的鍋子，一側光澤稍像鍍金的叫璫珠，一顆價值千金。
「古來『明月』、『夜光』，即此便是」：古來稱為明月珠、夜光珠的，就是這類珍珠。
「白晝晴明，簷下看有光一線閃爍不定」：晴朗白天在屋簷下看，會有一線光澤不停閃爍。
「『夜光』乃其美號，非真有昏夜放光之珠也」：夜光只是美稱，並非真的有在黑夜發光的珍珠。
「次則走珠，置平底盤中，圓轉無定歇，價亦與璫珠相仿」：其次是走珠，放在平底盤中不停滾轉，價格和璫珠相近。
「化者之身受含一粒，則不復朽壞，故帝王之家重價購此」：文中認為死者含一顆走珠，遺體便不腐壞，所以帝王之家高價購買。這是古文的記載，本題不檢驗其防腐功效。
「次則滑珠，色光而形不甚圓」：再其次是滑珠，色澤光亮而形狀不太圓。
「次則螺蚵珠，次官雨珠，次稅珠，次蔥符珠」：等級再依序往下，為螺蚵珠、官雨珠、稅珠、蔥符珠。
「幼珠如粱粟，常珠如豌豆」：細小珍珠像穀粒，一般珍珠像豌豆。
「卑而碎者曰璣」：低等而細碎的珍珠叫璣。
「自夜光至于碎璣，譬均一人身，而王公至于氓隸也」：從夜光珠到碎璣，好比同樣是人，身分卻有從王公到百姓的差別，用來比喻珍珠等級不同。

詳解
題目要選錯誤、必須撤換的標牌。D把夜光這個美稱當成夜間自行發光的功能，與「非真有昏夜放光之珠也」相反，因此選D。
A依文中排列，螺蚵珠在官雨珠與稅珠之前，符合等級、價值較高。B的光亮是色澤、不圓是形狀，兩者可以同時成立，正對應「色光而形不甚圓」。C符合本文關於走珠、防腐及帝王高價購買的記載；這是在比對文章，不是主張現代科學已證實該效果。

快速判斷：先圈錯誤、必須撤換，再找非真有昏夜放光，便能排除按名稱猜功能的D。''',
['文中螺蚵珠列在官雨珠及稅珠之前，標牌符合本文等級順序。','色光而形不甚圓，同時描述光澤及形狀，標牌正確。','按文章記載，走珠與防腐、帝王高價購買相連，標牌符合本文。','夜光只是美稱，文中明確否定黑夜發光，因此本題應撤換D。'],pearl,student='B；紅筆訂正D，另於D旁有藍筆記號。',images=['chinese-42-passage','chinese-42-question'],index=136,mark='使用者輸入42@錯題；第42題左側紅D覆藍B，已放大核對，原AI答案D與原卷及原文相符。原卷第41題未被問且無紅訂正，不擴收。')
add('gpt054-english-04',4,'English','英文第4題｜用them指回原本的鑰匙',"I left my keys on the bus. It'll be hard to get ______ back.",['it','ones','them','the ones'],'C',
'''逐句翻譯
I left my keys on the bus.：我把鑰匙遺留在公車上。
It'll be hard to get them back.：要把那些鑰匙拿回來會很困難。

詳解
空格要指回前一句my keys，也就是原本遺留的那些鑰匙。keys是複數，位於get後面當受詞，所以用複數受格代名詞them，答案C。
A it指單數，與keys不合。B ones常代替複數名詞，用在同類事物的選擇或比較，本句要直接指回原本那些鑰匙。D the ones通常用於區分特定的一組，例如配合修飾語說明是哪一些；本句直接代回my keys，用them最自然。不是說the ones在所有句子都不能指鑰匙。

句首It'll be hard to…的It是虛主詞，真正談的是拿回鑰匙這件事；它不等於後面get的受詞，不能因前面有It就把空格也填it。

快速判斷：my keys＝複數、原本那一組→get後須受格→them。''',
['it是單數，不能代回複數keys。','本句不是選擇同類的其他事物，應直接指回原本的keys。','them為複數受格，直接指回my keys。','本句不須另作區分或加修飾，直接用them回指最合適。'],student='A；紅筆訂正C。',images=['english-04'],index=166,mark='使用者輸入4@錯題；旋轉90度後確認第4題左側紅C覆藍A，上方另有藍C屬第3題，不能錯位判讀。')
add('gpt054-english-11',11,'English','英文第11題｜to change表示去銀行的目的','John is going to take a trip to the USA. He has to go to the bank ______ some money.',['change','changing','to change','and changes'],'C',
'''逐句翻譯
John is going to take a trip to the USA.：約翰即將去美國旅行。
He has to go to the bank to change some money.：他必須去銀行換些錢。

詳解
先問去銀行做什麼：為了換錢。英文用to＋原形動詞表示目的，因此在go to the bank後接to change some money，答案C。
A直接接change，缺少引出目的的to。B changing不構成本句所需的目的用法，不能只看到go就選V-ing。D若共用has to，應並列為has to go…and change…，不能接第三人稱單數changes。

三個to分清楚
has to go：has to＋原形動詞，表示必須去。
to the bank：介系詞to＋地點名詞，交代目的地。
to change some money：不定詞to＋原形動詞，交代去銀行的目的。

原對話的to用法追問補充
to＋原形動詞也可出現在want to sleep（想睡覺）、happy to see you（很高興見到你）、homework to do（要做的作業），不全都翻成為了。介系詞to可表示方向、接收對象、範圍，例如go to school、give it to me、from Monday to Friday。固定搭配look forward to seeing you、be used to getting up early中的to是介系詞，後接動作時用V-ing；不可見到to就一律接原形。

快速判斷：go to the bank後問目的→為了換錢→to change。''',
['缺少引出目的的不定詞to。','changing不能直接構成本句所要的目的結構。','to＋原形動詞表示為了換錢。','共用has to時，並列動詞須是go…and change，不能用changes。'],student='B；紅筆訂正C。',images=['english-11'],index=186,mark='使用者輸入11@錯題；轉正原卷第11題左側藍B上覆紅C，第11題題號另有紅記號，四選項完整。')
(D/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2)+'\n')
manifest=dict(sourceId='src-more-054',order=54,url=source,title=archive['title'],date='2026-11-02',dateBasis='各原始使用者出題訊息create_time的Asia/Taipei日期；未提供考試日',archivePath='docs/sources/6ae8b5b9-d8d8-83ee-991b-3fffcf6219e2.json',transcriptPath=str((D/'transcript.txt').relative_to(ROOT)),questionPath=str((D/'questions.json').relative_to(ROOT)),questionSHA256=hashlib.sha256((D/'questions.json').read_bytes()).hexdigest(),questionCount=6,originalQuestionCount=6,groupCount=0,allOriginalsVisuallyChecked=True,originalsAvailable=6,originalsExpected=6,items=items,skips=[dict(kind='source_unasked_originals',reason='同張試卷上的未問或正常題不擴收，僅整理使用者實際指定6個原題。'),dict(kind='ai_outputs_and_operations',reason='6張來源AI解說圖、技能操作與自編例句不另建題；to追問作第11題必要補充保留。')],reviews=[],state='ready',producer='/root/comic_lane_3',readyAt=datetime.now(timezone.utc).isoformat())
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('questions',len(questions),'manifest ready')
