"""Source-bound transcription of the six original Chinese questions; no shared writes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SOURCE = 'https://chatgpt.com/share/6af1d6de-09f8-83ee-bb43-0897e3964704'


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def path(name):
    return str((OUT / name).relative_to(ROOT))


def digest(name):
    return hashlib.sha256((OUT / name).read_bytes()).hexdigest()


def base(qid, num, title, question, choices, answer, explanation, tags, passage=''):
    return dict(id=qid, sourceId='src-more-065', subject='Chinese',
                title=f'國文第{num}題｜{title}', chapter='綜合', volume='綜合',
                date='2026-11-09', dateLabel='首次出題日期', addedAt='2026-11-09',
                question=question + '\n' + '\n'.join(f'({k}) {v}' for k, v in zip('ABCD', choices)),
                answer=f'({answer}) {choices["ABCD".index(answer)]}', correctOption=answer,
                explanation=explanation, trap='', verification='原卷逐題核對',
                verificationNote='已實開真正上傳原卷及本題裁切成品，核對完整題幹、全部選項、必要材料與解說。未提供實際考試日期，日期取本題首次使用者訊息（台灣時間）；無冊次或課次證據，歸綜合。',
                diagram='', notes='', status='todo', starred=False, tags=tags,
                images=[path(f'{qid}-original.jpg')], sourceLabel=f'分享原卷｜第{num}題',
                contentStatus='完整原題', originalQuestionNumber=str(num), passage=passage,
                tables=[], questionFigures=[], explanationFigures=[])


questions = [
    base('q-1035', 6, '互文與頂真',
         '請問下列選項中，何者運用到互文修辭？',
         ['軍書十二卷，卷卷有爺名', '秦時明月漢時關', '丞相玄機，神鬼莫測', '策勳十二轉，賞賜百千強'], 'B',
         '互文是把原本完整的意思分置於前後文，閱讀時須相互補足。「秦時明月漢時關」應合起來理解為秦漢以來的明月與關塞，並不是秦朝只有明月、漢朝只有關塞，所以選B。\n\nA前句末尾的「卷」接到後句開頭的「卷」，以相同字詞銜接，重點是頂真。C「神鬼莫測」強調連神鬼也難以測度其玄機，帶有誇飾意味，不須把前後分置的內容交互補足。D以「十二轉」「百千強」強調記功、賞賜之多，含數量誇飾及對偶意味，不是互文。\n\n辨別時，先問是否須把前後文合起來補全語意；不要因為句子有重複字或排列整齊，就判為互文。',
         ['修辭', '互文', '頂真']),
    base('q-1036', 7, '女性長者的祝壽題辭',
         '金曉奶奶下週過七十大壽，鄰居云云想送花籃給金曉奶奶，請問下列哪一個題辭最適合寫在花籃的卡片上？',
         ['花好月圓', '松柏長青', '懿範長存', '壽考宜家'], 'D',
         '這題須同時判斷「祝壽」的場合與「奶奶」的身分。「壽考」指高壽，「壽考宜家」是祝賀女性壽誕的題辭，最切合女性長者七十大壽，選D。\n\nA「花好月圓」常用於婚嫁祝賀，不符合本題生日場合。B「松柏長青」比喻如松柏長久青翠，可用於一般祝壽，本身並不是錯誤的祝福；但題目問「最適合」，D明確對應女壽，因此較貼切。C「懿範長存」是追念女性美好德範的哀輓題辭，用於在世長輩的壽誕不合適。\n\n教育部《國語辭典簡編本》的常用題辭表把「松柏長青」列於一般祝壽，把「壽考宜家」列於女壽。因此不應把B誤教成不能祝壽。',
         ['應用文', '題辭', '祝壽']),
    base('q-1037', 21, '銘志與史書的異同',
         '關於本文的解讀，下列何者正確？',
         ['銘志與史傳內容完全相同而能流傳後世', '關於人的善惡都會被詳細記錄在碑銘中', '道德高尚者會藉由立碑來彰顯個人功績', '放置於廟中或墓穴裡的碑銘用意不同'], 'C',
         '本文先說銘志的意義與史書相近，接著指出兩者不同：史書「於善惡無所不書」，而銘志著重表彰人的功德、才能品行與志節義行，希望美好的事蹟不被後世遺忘，因此選C。\n\nC的「藉由立碑」是在說以碑銘彰顯值得傳世的德行功績，不必解讀為當事人一定親自替自己立碑。原文所說「懼後世之不知，則必銘而見之」，強調的是使後人知曉美行的功能。\n\nA把「義近於史」誤解成「內容完全相同」，忽略緊接的「亦有與史異者」。B把史書的「善惡無所不書」錯套到碑銘。D與「或納於廟，或存於墓，一也」相反：放置地點雖不同，表彰美德、使事蹟傳世的用意相同。',
         ['文言文', '比較閱讀', '銘志', '史書'],
         '曾鞏寄歐陽舍人書：「夫銘志之著於世，義近於史，而亦有與史異者。蓋史之於善惡無所不書，而銘者，蓋古之人有功德、材行、志義之美者，懼後世之不知，則必銘而見之。或納於廟，或存於墓，一也。」'),
    base('q-1038', 26, '微小差異的持續累積',
         '左圖為老師在黑板寫下的話，他想傳達什麼道理？',
         ['在壞習慣的惡性循環之下，即使有再好的資質也將毫無用處', '勤奮或懶惰只差一點，但持續下去，最終的成果將大大不同', '我為人人，人人為我，每個人都無法離群索居，要懂得相互關懷', '雖天生資質不同，但天生我材必有用，總會找到屬於自己的一片天'], 'B',
         '黑板把略大於1的1.1與略小於1的0.9反覆連乘作比較：起初數字相差不大，持續累積後卻一個增加、一個減少，成果逐漸拉開。B同時包含「只差一點」「持續下去」「成果大大不同」，最符合圖意。\n\nA只談壞習慣使好資質失去作用，沒有呈現勤奮與懶惰兩種方向的比較，且額外加入圖中未談的天生資質。C談人際互助，D談不同資質各有發展，均不對應反覆連乘的累積效果。\n\n數值核對：原卷黑板確實寫2.85與0.31，不是0.35。若從一個1.1開始再乘1.1十次，共有11個因數，1.1¹¹≈2.8531；同理0.9¹¹≈0.3138，正好分別約為2.85與0.31。若把「相乘十次」理解為10個相同因數，才會算得1.1¹⁰≈2.5937與0.9¹⁰≈0.3487。原卷的數值可按「做十次乘法」理解，不應直接判為計算錯誤。無論此語句的計次方式，圖所表達的小差異長期累積主旨皆指向B。',
         ['圖文閱讀', '主旨判斷', '累積效果'],
         '黑板文字（照原卷）：\n1.1×1.1……相乘十次約為2.85\n但0.9×0.9……相乘十次約為0.31'),
    base('q-1039', 27, '詩中的回望與情感整理',
         '關於這首詩的解讀，下列說明何者最恰當？',
         ['此詩藉物抒情，作者說明願保有內心的純真', '作者直言未經歲月洗鍊的記憶不值得回憶', '從詩中可知作者為背包客棧的經營者', '作者透過寫詩回望曾經歷過的人與事'], 'D',
         '詩中從喜歡出發、停留與歲月留下的色彩，寫到夜裡作詩、清晨逐行逐段檢視，再「慢慢刪去／每一個與你有著關聯的字」。寫下、檢視與刪去，都呈現作者回望並整理曾經歷過的人事與情感，因此D最恰當。刪去相關文字，仍表示她正在面對這段經驗，不等於從未回望。\n\nA的「願保有內心的純真」沒有足夠詩句支持，不能只因出現果樹、風雨等意象就加入這個結論。B把「喜歡歲月漂洗過後的顏色」過度推成未經歲月洗鍊的記憶都不值得回憶，原文沒有這樣否定。C把喜歡出發、離開、停留直接推為經營背包客棧的職業身分，缺乏依據。\n\n原卷只署名席慕蓉，未標詩篇名稱；保留原卷節錄，不加上未經原卷證實的篇名。末節是「逐行逐段地檢視」「慢慢刪去」，不能誤讀為「慢慢畫出」。',
         ['新詩', '閱讀理解', '席慕蓉'],
         '（一）\n我喜歡出發　喜歡離開／喜歡一生中都能有新的夢想／千山萬水　隨意行去／不管星辰指引的是什麼方向\n\n我喜歡停留　喜歡長久／喜歡在園裡種下千棵果樹／靜待冬雷夏雨　春華秋實／喜歡生命裡只有單純的盼望／只有一種安定和緩慢的成長\n\n我喜歡歲月漂洗過後的顏色／喜歡那沒有唱出來的歌\n\n我喜歡在夜裡寫一首長詩／然後再來在這清涼的早上／逐行逐段地檢視／慢慢刪去／每一個與你有著關聯的字\n（席慕蓉）'),
    base('q-1040', 31, '馬援資產變化的圖表判讀',
         '根據本文，關於馬援資產多寡的變化情況，依時間來看的話，下列圖表何者最貼切？',
         ['圖表A', '圖表B', '圖表C', '圖表D'], 'D',
         '依文章的時間順序，把「家用不足」→「後有畜數千頭，穀數萬斛」→「乃盡散於親舊」連起來：起初資產少，後來經營田牧累積大量財產，接著把財產分送親友故舊，所以資產應先增加、後減少，對應D。\n\n「凡殖財產，貴其能賑施也，否則守錢虜耳」是散財的原因：馬援認為增殖財產，貴在能用來救濟施助，否則只是守著錢的奴僕。資產的下降來自他主動散財，不宜誤說成經營失敗。\n\nA是一路增加，漏掉散財後的減少。B是一路減少，漏掉先累積財富。C是先減少再增加，順序與原文相反。D才能兼顧前後兩階段。圖是變化趨勢示意，文章未提供確切年齡、各時點金額，也不能由曲線自行推算。',
         ['文言文', '圖表判讀', '馬援'],
         '（三）馬援少時，以家用不足辭其兄況，欲就邊郡田牧。況曰：「汝大才當晚成，良工不示人以朴①，且從所好。」遂之北地田牧。常謂賓客曰：「丈夫為志，窮當益堅，老當益壯。」後有畜數千頭，穀數萬斛。既而嘆曰：「凡殖②財產，貴其能賑施也，否則守錢虜③耳！」乃盡散於親舊。聞隗囂好士，往從之。囂甚敬重，與決籌策。（節錄自資治通鑑）\n\n註①朴：樹木的外皮，此指未加工的木材。②殖：生財牟利。③虜：奴隸、僕人。')
]

students = ['原卷黑筆A，紅筆訂正B；原始提問記錄A→B。',
            '原卷黑筆B，紅筆訂正D；原始提問記錄B→D。',
            '原卷黑筆B，紅筆訂正C；原始提問記錄B→C。',
            '原卷黑筆A，紅筆訂正B；原始提問記錄A→B。',
            '原卷黑筆A，紅筆訂正D；原始提問記錄A→D。',
            '原卷黑筆A，紅筆訂正D；原始提問記錄A→D。']
for q, student in zip(questions, students):
    q['studentAnswer'] = student
questions[3]['questionFigures'] = [dict(src=path('q-1038-board.jpg'), caption='題目黑板原圖，文字與數值照原卷保留。')]
questions[5]['questionFigures'] = [dict(src=path('q-1040-options.jpg'), caption='原卷A～D四個圖表選項；縱軸為資產，橫軸為年齡。')]
questions[5]['answer'] = '(D) 圖表D（資產先增加、後減少）'

manifest = dict(sourceId='src-more-065', producer='/root/comic_lane_2', items=[])
acq = json.loads((ROOT / 'docs/acquisition/new-gpt-20261109-65.json').read_text())
for i, q in enumerate(questions, 1):
    qid = q['id']
    save(OUT / f'{qid}.json', q)
    review = dict(id=qid, sourceId='src-more-065', reviewerAgent='/root/comic_lane_2',
                  originalVisualChecked=True, completeOriginalAndOptions=True,
                  sourceGeneratedArtUsed=False, passed=True,
                  actualViewed=[f'docs/source-pages/chatgpt-6af1d6de-{i}.jpg', path(f'original-{i}-rotated.jpg'), path(f'{qid}-original.jpg')] + [f['src'] for f in q['questionFigures']],
                  actualViewedNote='原卷以90度旋轉成品實開，逐題裁切亦已實開；保留原筆跡。',
                  duplicateReview=dict(method='本機META索引關鍵詞＋正式題庫題幹選項候選比對', state='no_duplicate_found', evidenceFile=path('duplicate-check.json')),
                  inclusionEvidence=students[i-1],
                  sourceAttachment=dict(index=i, path=acq['downloadedImages'][i-1]['path'], sha256=acq['downloadedImages'][i-1]['sha256'], messageId=acq['downloadedImages'][i-1]['messageId'], firstQuestionTimestamp=acq['downloadedImages'][i-1]['firstQuestionTimestamp']),
                  dateRule='首次使用者原題訊息，Asia/Taipei轉換為2026-11-09；非考試日。',
                  teachingComicState='queued')
    save(OUT / f'{qid}-review.json', review)
    manifest['items'].append(dict(id=qid, status='ready', questionPath=path(f'{qid}.json'), questionSHA256=digest(f'{qid}.json'), reviewPath=path(f'{qid}-review.json'), reviewSHA256=digest(f'{qid}-review.json')))
save(OUT / 'manifest.json', manifest)

corrections = [
    dict(questionId='q-1035', reason='原AI誤抄C選項，須回復真正原卷文字。',
         before='原AI將C寫為「丞相之機，神鬼莫測」。',
         after='原卷C為「丞相玄機，神鬼莫測」，完整保留原選項；答案B不變。'),
    dict(questionId='q-1036', reason='原AI將題幹人名「金曉」誤抄成「金鷹」。',
         before='原AI題幹寫「金鷹奶奶」。',
         after='依原卷回復「金曉奶奶」；答案D不變。教育部題辭表支持松柏長青為一般祝壽、壽考宜家為女壽。'),
    dict(questionId='q-1037', reason='原AI把原文起首「夫銘志」誤抄為「太銘志」。',
         before='原AI引文起首為「太銘志之著於世」。',
         after='依原卷回復「夫銘志之著於世」，保留全文與選項；答案C不變。'),
    dict(questionId='q-1038', reason='原AI誤讀黑板0.31為0.35，並將可按十次乘法成立的2.85直接指為題目數值錯誤。',
         before='原AI寫「0.9×0.9……相乘十次約為0.35」，並以1.1^10≈2.59指稱原卷2.85不符、可能題目有誤。',
         after='原卷黑板保留2.85與0.31；解說指出11個因數做十次乘法時1.1^11≈2.8531、0.9^11≈0.3138，兩數一致。若數十個因數則為2.59與0.35，須區分因數個數和乘法次數。主旨與答案B不變。'),
    dict(questionId='q-1039', reason='原AI誤指詩名，且把末節「慢慢刪去」改成「慢慢畫出」，造成閱讀證據失真。',
         before='原AI稱本詩為席慕蓉〈一棵開花的樹〉，引文寫「慢慢畫出每一個與你有著關聯的字」，C解說也誤將經營者身分連到「你」。',
         after='原卷只署席慕蓉，未印篇名，故不附未證實篇名；全文照錄「逐行逐段地檢視／慢慢刪去／每一個與你有著關聯的字」。D以寫詩、檢視與刪去來回望、整理曾經的人事解釋；C指作者的職業，並非「你」。答案D不變。')
]
for row in corrections:
    row.update(sourceUrl=SOURCE, originalAiChatUrl=SOURCE, title=next(q['title'] for q in questions if q['id'] == row['questionId']), fullQuestion=next(q for q in questions if q['id'] == row['questionId']), evidence=path(row['questionId'] + '-original.jpg'))
save(OUT / 'reviews.json', corrections)
save(OUT / 'external-evidence.json', dict(sources=[dict(url='https://dict.concised.moe.edu.tw/appendix.jsp?ID=11&la=0&page=7&powerMode=0', title='教育部《國語辭典簡編本》常用題辭表', checkedFacts=['松柏長青列一般祝壽', '壽考宜家列女壽'])], note='僅支持題辭用法；原題文字以原卷為準，不由外站補題。'))
print(json.dumps(dict(items=[q['id'] for q in questions], manifest=path('manifest.json')), ensure_ascii=False))
