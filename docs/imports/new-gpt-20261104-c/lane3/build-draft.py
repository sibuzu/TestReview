from pathlib import Path
import json,hashlib,datetime,copy
from zoneinfo import ZoneInfo
D=Path(__file__).parent;R=D.parents[3];URL='https://chatgpt.com/share/6aeb402e-c158-83ee-b603-6444a590bf27';SID='src-more-057'
a=json.loads((R/'docs/sources/6aeb402e-c158-83ee-b603-6444a590bf27.json').read_text());items=[]
def asset(k):return str((D/'originals'/f'{k}.png').relative_to(R))
def evidence(index,files,crops,mark):
 m=a['messages'][index];att=[x for x in m['content']['parts'] if isinstance(x,dict) and x.get('content_type')=='image_asset_pointer'];rows=[]
 for n in files:
  p=R/f'docs/source-pages/chatgpt-6aeb402e-{n}.jpg';match=next(x for x in att if x['size_bytes']==p.stat().st_size)
  rows.append(dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,fileId=match['asset_pointer'].split('?')[0]))
 return dict(url=URL,messageIndex=index,messageId=m['id'],firstQuestionTimestamp=m['create_time'],firstQuestionDateTime=datetime.datetime.fromtimestamp(m['create_time'],ZoneInfo('Asia/Taipei')).isoformat(),originals=rows,attachmentMatchedBy='archive size_bytes/fileId, not DOM filename order',cropHashes={asset(k):hashlib.sha256((R/asset(k)).read_bytes()).hexdigest() for k in crops},inclusionEvidence=mark)
def q(key,no,title,stem,opts,answer,explanation,analyses,student,images,index,files,mark):
 x=dict(id=key,sourceId=SID,subject='Chinese',title=title,chapter='綜合',volume='綜合',date='2026-11-04',dateLabel='首次出題日期',question=stem+'\n'+'\n'.join(f'({c}) {o}' for c,o in zip('ABCD',opts)),answer=f'({answer}) {opts["ABCD".index(answer)]}',explanation=explanation,trap='',verification='原卷逐題核對',verificationNote='已實看真正上傳原卷與裁圖，核對完整題幹、全部四選項及共用閱讀；日期為原始提問訊息的台灣日期，未提供實際考試日。未確認對應冊次、章節，歸綜合。',diagram='',tags=[title.split('｜')[-1]],images=[asset(k) for k in images],sourceLabel=f'分享原卷｜第{no}題',studentAnswer=student,contentStatus='完整原題',correctOption=answer,passage='',optionAnalysis=[dict(label=c,text=o,wordClass='應選' if c==answer else '不選',meaning='',explanation=t) for c,o,t in zip('ABCD',opts,analyses)],tables=[],questionFigures=[],explanationFigures=[],originalQuestionNumber=str(no),sourceEvidence=evidence(index,files,images,mark))
 items.append(dict(draftId=key,messageIndex=index,originalQuestionNumber=str(no),date='2026-11-04',answerCanBeDetermined=True,correctOption=answer,sourceEvidence=x['sourceEvidence']))
 return x
poem='（甲）採珠行　元稹\n\n海波無底珠沉海，採珠之人判死採。\n萬人判死一得珠，斛量買婢人何在。\n年年採珠珠避人，今年採珠由海神。\n海神採珠珠盡死，死盡明珠空海水。\n珠為海物海屬神，神今自採何況人。\n\n注：①採珠：到水裡採取珍珠。②判死：付出生命作為代價。'
translation='''全詩逐句白話
「海波無底珠沉海，採珠之人判死採」：海水深不可測，珍珠沉在海底；採珠的人冒著生命危險去採取。「判死」指拼死、冒死。
「萬人判死一得珠，斛量買婢人何在」：許多人冒死，才可能取得珍珠；那些以大量珍珠購買婢女的人，如今又在哪裡？「斛」是古代容量單位，以斛計珠顯出數量多，不是採珠工具。「萬人」與「一得」形成懸殊對比，不是提供可計算的統計採獲率。
「年年採珠珠避人，今年採珠由海神」：人們年年採珠，珍珠彷彿躲避人類；今年甚至由海神親自採珠。這是詩中的想像、諷喻，不是神明採珠的歷史紀錄。
「海神採珠珠盡死，死盡明珠空海水」：海神一採，珍珠便被取盡；珍珠消失，只剩空蕩的海水。藉誇張想像凸顯過度索取、資源耗竭。
「珠為海物海屬神，神今自採何況人」：珍珠本來是海中產物，海洋又屬海神；如今連海神都自行採取，何況是人類呢？以反問延伸對貪取的反思。'''
p1=q('gpt057-pearl-q1',1,'國文第1題｜〈採珠行〉的主旨判讀','有關本詩的主旨，下列敘述何者正確？',['譴責人們與神明爭採珍珠','呼籲重視海洋生態的平衡','呼籲從事捕獵應重視安全','撻伐買婢的行為忽視人權'],'B',translation+'''\n\n第1題詳解
全詩由冒死採珠寫到「珠盡死」「空海水」，呈現過度索取之下珍珠耗竭的景象。在本題四個選項中，B最能涵蓋詩末對海洋資源及人類行為的反思，依原卷紅筆維持B。
A把想像中的海神當成真有神、人爭奪的事件，偏離諷喻。C只抓住冒死採珠的危險，不能概括後半資源被採盡的內容。D只抓買婢，並非本詩整體論述。
本詩也同情冒死勞動者、反映富貴者奢侈與社會不公；選B不表示古詩只有現代環境保護一種意義。作答須比較四項何者最能涵蓋本題所引全詩，不把單一細節當全文主旨。

原AI作答紀錄更正：原AI曾寫本題藍筆選B且已正確；實看放大原卷，藍筆是A、紅筆訂正B。原題與答案B不變，原作答記錄依原圖更正。

原典核對：[《全唐詩》卷418〈採珠行〉](https://zh.wikisource.org/zh-hant/全唐詩/卷418)。詩文用字依原卷保留。''',
['海神為想像與諷喻，不是單純譴責人與神競爭。','珠盡死、空海水呈現資源被取盡，四項中最能概括本題全詩。','採珠危險是部分內容，不足概括後半的資源耗竭。','買婢是其中材料，不是全詩只談的人權主張。'],'A；原卷紅筆訂正B。',['pearl-poem','pearl-q1'],118,[3],'user訊息118明示1、2@錯題；第1題藍A覆紅B已放大實看，不採原AI誤讀成藍B。')
p2=q('gpt057-pearl-q2',2,'國文第2題｜「斛量買婢」的文意','從詩意推斷，「斛量買婢」指的是下列何現象？',['海邊萬人空巷，珍珠被一斛一斛採走','大家都跑去採珍珠，導致無人買賣婢女','富人揮霍珍珠後，只好賣掉婢女來償債','珍珠被採盡之前，富人揮霍珍珠的情景'],'D',
'''逐詞判讀
斛是古代容量單位；斛量表示珍珠多到以容量計量。買婢是購買婢女，動作是「買」，不是「賣」。合起來是在說富貴者以大量珍珠購買婢女、奢侈耗費珍珠的情景，因此選D。

C把買婢反過來說成賣婢，還額外加入償債情節，原詩沒有這個因果。A把斛量誤套為一斛一斛採珠，也添入萬人空巷；B把採珠與無人買賣婢女連成原詩未說的因果，均不合。

全詩逐句白話已列在本組第1題解說。此題把「萬人判死」的艱險取得，與「斛量買婢」的富人奢侈並置；把握動詞及前後對比，不因看到珍珠、婢女就拼出未出現的故事。這是對古代詩句的理解，不把買婢當成值得提倡的行為。''',
['斛量指以容量計量珍珠，不是詩中描述的採珠方式；萬人空巷亦非原意。','原詩沒說因採珠而無人買賣婢女。','買與賣方向相反，償債也是原文未有的情節。','符合富貴者以大量珍珠奢侈消費的情景。'],'C；原卷紅筆訂正D。',['pearl-q2'],118,[3],'user訊息118明示1、2@錯題；第2題藍C紅D，題幹四選項完整。')
whale='''（丙）解析魚類的情感　網路文章

海洋生物也有情感嗎？在動畫電影海底總動員中，海洋生物角色們各個活靈活現，充滿獨特個性，不僅能夠彼此交流，還能夠表達出和人類一樣的各種喜怒哀樂。根據一些科學研究以及生態觀察顯示，這些情感反應可能並非只存在人類的幻想裡頭，海洋生物不僅會有近似於害羞或焦慮的表現，甚至有可能具有像人類一般的同理心！

澳洲的行為生態學教授布朗在魚類生物學期刊中發表了一篇研究，其研究對象是十七隻來自澳洲東岸的澳洲虎鯊，布朗教授指出，不同的鯊魚即便遇到了相同的情境，仍會表現出不同的反應，顯示出鯊魚的性格存在著個體之間的差異——有些鯊魚遇到陌生環境中的障礙物時，只需短短二秒便能突破，有些卻必須花上長達二十分鐘，表現得比同類更加小心翼翼；而每隻鯊魚從突然離水到重新回到水中並平復下來所花費的時間也大不相同，說明了他們對於環境焦慮的抗壓性存在著差異。

除了鯊魚以外，另外一份關於座頭鯨的觀察報告則指出，座頭鯨會為了拯救其他非自己族類的動物和掠食者搏鬥。2008年時，海洋生物學者彼得曼及其研究團隊記錄下了二隻座頭鯨不斷拍動魚鰭並發出叫聲，只為了幫助海豹脫離殺人鯨捕食的影片，一週後，研究團隊又再度發現，類似的救援行動來自於完全不同的座頭鯨身上，這一次，他們除了奮力趕跑殺人鯨外，甚至還將跌下浮冰的海豹「抱」在自己的肚子上，帶往安全的地方。這些被拯救的生物當中，有高達90%都是非座頭鯨：海獅、海豹、翻車魚以及灰鯨等都包含在內。

目前，座頭鯨出現「利他行為」的原因還有待進一步研究，但彼得曼在文章中寫道：「人類保護其他動物，我們稱之為同理心，如果今天是發生在座頭鯨身上，我們會稱之為天性，但有時候，這兩者之間的界線是模糊的。」'''
w=q('gpt057-whale-q7',7,'國文第7題｜座頭鯨舉動與名句','文中座頭鯨的舉動，下列哪項人類的精神最接近？',['己所不欲，勿施於人','博施於民，而能濟眾','願無伐善，無施勞','以直報怨，以德報德'],'B',
'''先找文章中的具體行為
座頭鯨不只保護同類，也驅趕掠食者、救助海豹等其他動物。文中還寫將海豹抱在肚子上帶往安全處。這些證據的重點是主動、廣泛幫助其他生命，最接近B，故選B。

四句逐句白話與比較
A「己所不欲，勿施於人」：自己不願承受的事，不要強加別人；重點在不施加不願承受的事，沒有B直接表達主動救助眾者。
B「博施於民，而能濟眾」：廣泛施予恩惠，並能幫助眾人。博是廣泛，濟是救助，對應文章救助不同動物的行為。
C「願無伐善，無施勞」：願不誇耀自己的長處、不把勞苦事推給他人。「伐善」指自誇；教育部辭典在「施勞」第一義直接引本句，釋為把勞事加諸他人。此外「施勞」也有張揚功勞一義，原AI採不表彰功勞的說明屬此另一釋義。兩種解讀均不如B直接切合本題廣泛主動救助的證據，不靠把某一義說成唯一來選答。
D「以直報怨，以德報德」：以公正態度回應怨恨，以恩德回報恩德；重點在回應恩怨，本文沒有報恩、報怨關係。

閱讀限制
文章以同理心類比動物行為，但結尾明說利他原因仍待研究，不宜斷言座頭鯨具有和人類完全相同的道德意識。90%是文中這些救援紀錄所述比例，不擴成所有海洋生物、所有救援都必如此。虎鯊研究與座頭鯨救援是不同材料，不能混成同一研究對象。

字義核對：[教育部「博施濟眾」](https://dict.revised.moe.edu.tw/dictView.jsp?ID=13242&la=0&powerMode=0)、[「伐善」](https://dict.revised.moe.edu.tw/dictView.jsp?ID=33238&la=0&powerMode=0)、[「施勞」](https://dict.revised.moe.edu.tw/dictView.jsp?ID=127169&la=0&powerMode=0)。''',
['自己不想承受的事，不強加別人，未如B直接對應主動廣泛救助。','廣施恩惠、救助眾者，最切合救助不同動物的利他行為。','伐善為誇耀長處；施勞有加勞事於人及誇功兩義，此句不如B直接對應廣泛救助。','公正回應怨恨、以恩報恩，本文沒有恩怨回報關係。'],'A；原卷紅筆訂正B。',['whale-passage-1','whale-passage-2','whale-q7'],134,[4,5],'user訊息134明示7@錯題並附兩頁；只收第7，未問第6不擴收，整篇跨頁文章已核齊。')
w['passage']=whale
seafood='''從臺灣海鮮選擇指南看消費者行動（節錄）　廖運志

為達成永續漁業，鼓勵民眾藉由消費者的力量，來改變過漁（過度撈捕）與濫捕對漁業資源及海洋生態造成的嚴重影響，「臺灣海鮮選擇指南」手冊所提供的挑選原則與建議如下：
沙丁魚、竹筴魚及秋刀魚等，屬於體型小、生長速度快，野外數量尚豐富，因此建議食用；反觀過去曾因過度撈捕而禁捕的鯨鯊，以及最近才列入保育類的隆頭鸚哥魚及曲紋唇魚（俗稱蘇眉或龍王鯛）等，因體型大、成長慢，過度利用後資源不易恢復，易瀕危，應避免食用。
除了沙丁魚、竹筴魚及秋刀魚外，還包含鯖魚、白帶魚及飛魚等體色屬銀白色的中小型魚類，因這些棲息於中表水層之洄游魚類，目前因數量較多、撈捕的方法不會破壞海底環境，屬於建議食用種類；體色鮮豔珊瑚礁魚類如鸚哥魚、紅石斑等，則因為數量較少、定棲性魚類資源恢復較不易，屬於避免食用種類。
選擇以不易發生混獲的漁法所取得的魚類，如一支釣的鰹魚、鏢旗魚；或對環境干擾較少的漁法所捕撈的海鮮，例如櫻花蝦，因為捕撈櫻花蝦採用中層網，不會接觸到海底；避免選擇以底拖網等方法撈捕的野生海蝦。
過濾海水的文蛤、牡蠣等，或食藻類的鮑魚、九孔等螺貝類，或以浮游動物、小魚為食物的種類，這些屬於食物鏈底層的種類因食物來源豐富，數量也相對較多，建議食用。鯊魚、鮪魚等大型掠食性魚類，則因位於生態系食物金字塔的頂端，數量較少，許多種類已因過度捕撈大量減少，因此除了瀕危及保育物種已禁止捕撈外，都應盡量避免選擇。
當許多野生魚類因為過度捕撈、棲地破壞、汙染及外來種入侵等問題已紛紛從餐桌上消失，養殖魚類取而代之。我們又該如何選擇這些養殖魚類呢？
消費者可以選擇臺灣鯛（吳郭魚）、虱目魚等，因為他們的餌料屬於植物性來源；應避免食用動物性餌料的肉食性養殖魚類，如石斑、鮭魚及養殖蝦等，因為這些餌料的來源多是野生魚類（魚粉），甚至是由底拖網混獲的下雜魚所製成的。'''
s1=q('gpt057-seafood-q1',1,'國文第1題｜海鮮指南的編纂目的','依文意判斷，「臺灣海鮮選擇指南」手冊編纂的原因最有可能為下列何者？',['研究臺灣近海魚類的生態及其面臨的危機','探討臺灣魚類產業的經營方向與發展策略','建議民眾食用合宜的魚類以延續海洋資源','使民眾了解海洋知識以加速海洋生態研究'],'C',
'''找出編寫給誰、希望對方做什麼
開頭明說為達成永續漁業，鼓勵民眾藉消費者力量改變過漁、濫捕的影響，接著整篇提供挑選海鮮原則。因此手冊的直接目的是引導消費者選擇合宜食物，協助海洋資源延續，C最符合。

A的生態危機是相關背景與研究主題，不能直接代替面向消費者的手冊目的。B著重產業經營策略，文中未以業者為主要指導對象。D把目的變成加速科學研究，也不是文中消費者行動的方向。

文章推理是問題（過漁與濫捕損傷資源）→方法（提供選購指南、改變消費）→目的（永續利用海洋資源）。不要只因出現生態、海洋等相同字詞，就忽略誰採取何種行動。

本文的物種、保育現況語句及推薦名單依原卷保留，本題按文意判讀，不把節錄中的「目前」「最近」另當作現今資料更新日期。''',
['相關研究背景不是這份消費者指南的直接目的。','不是以漁業公司經營策略為重點。','對應引導消費選擇、減輕過漁影響、延續資源的目的。','不是要透過民眾加速科學研究。'],'A；原卷紅筆訂正C。',['seafood-passage-1','seafood-passage-2','seafood-q1'],138,[6,7],'user訊息138明示1、2@錯題；第1藍A紅C，兩頁共用文章完整、所需全文保留。')
s2=q('gpt057-seafood-q2',2,'國文第2題｜海鮮挑選原則的判讀','依據本文，有關海鮮挑選原則，下列敘述何者正確？',['體型小的魚，肉質鮮嫩且不易受重金屬汙染，宜多選購','珊瑚礁定棲魚類，體色鮮豔、數量較多，適合多加食用','避免食用以底拖漁網捕撈的野生海蝦，如：櫻花蝦','多選擇屬於食物鏈底層的海鮮，因其數量相對較多'],'D',
'''回到原文逐項核對
D直接對應「這些屬於食物鏈底層的種類因食物來源豐富，數量也相對較多，建議食用」，答案D。
A雖用體型小這個文章出現的特徵，卻加上肉質鮮嫩、不易受重金屬汙染等原文未提供的理由。文章推薦的原有條件還有生長速度快、野外數量等，不是單憑小就能推定選項全部成立。
B將原文珊瑚礁定棲魚數量較少、資源恢復不易，反說成數量較多、宜多吃，與本文相反。
C的避免底拖網野生海蝦原則與文章有關，但把櫻花蝦放進例子就錯了：原文明說櫻花蝦使用中層網，不接觸海底，不能直接當作底拖漁網案例。

選項要整句成立
讀到前半句相似，不代表後半理由或例子也正確。A是增加無據理由，C是把不同漁法的例子混在一起。D則從對象、數量理由到選擇方向都與原文一致。

這是依本文進行資訊一致性判讀；不從本題另外推論某種魚必然無污染、所有漁法在任何情況均有相同效果。''',
['肉質與重金屬理由未受本文支持，不能只因提到體型小就整句判對。','原文說數量較少、恢復不易，與選項相反。','櫻花蝦用中層網不接觸海底，不是此處底拖漁網的例子。','對應本文食物鏈底層、來源豐富、相對數量多的選擇原則。'],'C；原卷紅筆訂正D。',['seafood-q2'],138,[6,7],'user訊息138明示1、2@錯題；第2藍C紅D，四選項與跨頁共同文章完整。')
def group(children,title,passage,numbers):
 g=copy.deepcopy(children[0]);g['title']=title;g['passage']=passage;g['groupQuestions']=children;g['question']='請閱讀共用文章，回答第'+numbers+'題。';g['answer']='\n'.join('【第'+c['originalQuestionNumber']+'題】'+c['answer'] for c in children);g['explanation']='\n\n'.join('【第'+c['originalQuestionNumber']+'題】\n'+c['explanation'] for c in children);g['studentAnswer']='\n'.join('【第'+c['originalQuestionNumber']+'題】'+c['studentAnswer'] for c in children);g['correctOption']='';g['optionAnalysis']=[];g['originalQuestionNumber']=numbers;g['images']=list(dict.fromkeys(f for c in children for f in c['images']));g['groupMetadata']=dict(originalQuestionNumbers=[c['originalQuestionNumber'] for c in children],displayOrder=[c['id'] for c in children],sourceGroupVerified=True,sharedPassageOnce=True,sourceSharedReadingOnly=True);return g
parents=[group([p1,p2],'國文題組｜〈採珠行〉閱讀（第1、2題）',poem,'1、2'),w,group([s1,s2],'國文題組｜海鮮指南閱讀（第1、2題）',seafood,'1、2')]
(D/'questions.json').write_text(json.dumps(parents,ensure_ascii=False,indent=2)+'\n')
for x in [p1,p2,w,s1,s2]:(D/(x['id']+'.json')).write_text(json.dumps(dict(x,passage=poem if x['id'].startswith('gpt057-pearl') else seafood if x['id'].startswith('gpt057-seafood') else whale),ensure_ascii=False,indent=2)+'\n')
reviews=[dict(draftId=p1['id'],kind='原AI原作答誤讀',answerCanBeDetermined=True,expectedAnswer='B',before='原AI訊息128/132稱第1題藍筆選B且已與詩意一致。',after='原卷放大可見藍筆A、紅筆訂正B，原作答記錄A→B；題幹、四選項與答案B不改。',reason='原AI將學生原選項誤讀，會造成錯題紀錄不準；不是答案未定。',sourceUrl=URL,questionText=poem+'\n\n'+p1['question'],evidence=[asset('pearl-q1'),asset('pearl-poem')]),dict(draftId=w['id'],kind='文言多義詞釐清',answerCanBeDetermined=True,expectedAnswer='B',before='原AI將C無施勞只釋不表彰功勞，並概括全句僅為謙虛不居功。',after='教育部施勞第一義直接引本句，為不將勞事推給他人；第二義另有張揚功勞。解說並列釐清，不把原AI所取第二義判作完全無此義，也不因此改B答案。',reason='避免將多義詞固定為唯一解；兩義均不如B直接對應廣泛主動救助，原題答案可核。',sourceUrl=URL,questionText=whale+'\n\n'+w['question'],primarySources=['https://dict.revised.moe.edu.tw/dictView.jsp?ID=127169&la=0&powerMode=0','https://dict.revised.moe.edu.tw/dictView.jsp?ID=33238&la=0&powerMode=0'],evidence=[asset('whale-q7')])]
manifest=dict(sourceId=SID,url=URL,part='reading5',producer='/root/comic_lane_3',status='ready',questionPath=str((D/'questions.json').relative_to(R)),questionSHA256=hashlib.sha256((D/'questions.json').read_bytes()).hexdigest(),originalQuestionCount=5,questionPageCount=3,wholeSource=dict(originalQuestionCount=15,questionPageCount=13),archivePath='docs/sources/6aeb402e-c158-83ee-b603-6444a590bf27.json',transcriptPath=str((D/'transcript.txt').relative_to(R)),sourceAIImagesAdopted=False,teachingComicState='queued_after_intake',pendingQuestionConditions=[],reviews=reviews,items=items,skips=[dict(kind='unasked_original_question',question='whale-q6',reason='user僅問第7，故第6虎鯊個性題不擴收；完整共用文章仍保留。'),dict(kind='source_ai_generated',reason='原AI會考互動延伸小測驗、AsyncImage/插圖/圖表不收入，不採原AI解說圖。')],visualReview=dict(originalsViewed=[f'docs/source-pages/chatgpt-6aeb402e-{n}.jpg' for n in range(3,8)],allOriginalsReadable=True,cropsViewed=[str(f.relative_to(R)) for f in sorted((D/'originals').glob('*.png'))],allCropsComplete=True,checkedNecessaryMaterials=True,notes='垂直排印按原卷轉錄為橫排文字；裁圖已逐張實開，第一次裁圖發現選項續欄需向左擴充後重看，現在詩題D與鯨魚/海鮮各四選項全部保留。海鮮末欄貼書脊且與鄰題相近，為保留必要全文留少量鄰題邊緣，未將鄰題收入。'),sharedMaterials='採珠兩子與海鮮兩子各共用原文一次，無共同選項；各子題不同四選項均保留。',titleReview='自訂標題中性，不透露正解。',contentFrozen=True,readyAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('ready',len(parents),'pages',sum(len(p.get('groupQuestions') or [p]) for p in parents),'originals')
