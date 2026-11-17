"""Only source-local verified drafts; integration belongs to Agent1."""
from pathlib import Path
import json,hashlib,datetime
from questions import QUESTIONS,PASSAGES,TABLES
B=Path(__file__).parent
SOURCE='https://chatgpt.com/share/6afc7636-b8dc-83ec-a9de-c3ac330e5d27'
LAW='https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=C0010011'
ELECT='https://law.cec.gov.tw/LawContent.aspx?id=GL000292'
REFER='https://law.cec.gov.tw/LawContent.aspx?id=GL000290'
LOCAL='https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=A0040003'
EXPLAIN={
1133:'答案D。原卷公告明確指敦品中學，這所矯正學校收容執行感化教育處分的少年，以學校教育、生活輔導及技能學習協助少年。感化教育是少年保護處分，不能把它等同刑罰。\n\nC安置輔導也是保護處分，但由適當福利、教養、醫療等機構或處所執行，與本題敦品中學不同。A拘役、B有期徒刑屬刑罰；本題不是詢問這兩項。判斷須看具體學校及收容目的，不可誤推所有少年矯正學校都只執行感化教育；例如明陽中學另有執行少年徒刑的功能。\n\n查核：[敦品中學感化教育收容資料](https://www.tyr.moj.gov.tw/media/20726903/%E8%BF%91%E4%BA%94%E5%B9%B4%E6%84%9F%E5%8C%96%E6%95%99%E8%82%B2%E6%94%B6%E5%AE%B9%E6%83%85%E5%BD%A2-%E6%9C%88%E5%A0%B1-110-115.pdf?mediaDL=true)、[少年事件處理法]('+LAW+')。',
1134:'答案B。文中警方取締交通違規、行政機關依法裁處罰鍰，是執行法律的行政行為。罰鍰是行政罰，與刑罰中的罰金不同，故A不選。\n\n立法院三讀通過修正案是立法行為；不能因B正確就把立法院修法也說成行政行為。《道路交通管理處罰條例》雖名為條例，仍是立法院通過的法律，不是行政機關訂定的命令，C不選。修法重點為遏止違規、維護交通安全與公共利益；依法管制行為可能限制部分自由，但不能把目的簡化為限縮人民權利，D不適當。\n\n題目中的年份、統計數與新聞敘述照原卷保留，不另補未提供的罰鍰級距。',
1135:'原卷教材訂正為C，但本題的單選條件須保留疑義。未滿14歲的行為不罰；14歲以上未滿18歲並非沒有刑事責任，依法得減輕其刑，並非一律免刑或必減刑。\n\n依《少年事件處理法》第27條，少年觸犯最輕本刑5年以上有期徒刑之罪等情形，應裁定移送檢察官。持刀強迫他人交付財物，若符合強盜等重大犯罪的要件，最貼近教材想呈現的少年刑事案件，故原卷選C。但移送偵查不等於保證定罪或判有期徒刑。\n\nA的17歲少年偷錢也非絕不可能判刑。第27條第2項允許少年法院依重大情節等條件裁量移送；題幹只寫尚未成年而被判刑，沒有明示只問必須移送的重罪，因此若把題意理解為任何可能判刑的少年，A亦可能成立，不能僅憑年齡把A絕對排除。B的18歲已不屬現行少事法所稱少年；D未滿14歲不受刑罰，但仍可能有少年保護處遇。\n\n查核：[少年事件處理法第2、27條]('+LAW+')、[刑法第18條](https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=C0000001)。保留原卷C，不杜撰A的金額或情節來製造唯一答案。',
1136:'答案B。共同材料的甲先調查少年事件，再把符合刑事處理條件的案件移送地檢署，指少年法院（庭）；乙偵查終結並提起公訴，指檢察官。\n\n警方調查後移送少年法院（庭）；少年法院依少事法第27條判斷是否裁定移送檢察官。檢察官偵查後決定是否起訴；若起訴，仍由法院審理判決。因此法官不負責起訴，少輔會也不是本題裁定移送檢察官的司法機關。\n\n本題原卷已明示17歲、強盜最輕本刑5年以上，與單看未成年或行為名稱不同。偵查、起訴及審判是不同職權，起訴也不是定罪。查核：[少年事件處理法第27條]('+LAW+')。',
1151:'答案B。傳統農牧方式很受水分可利用程度影響：乾燥地區難以穩定種植，常以游牧因應；赤道附近較濕潤，雨林地區可見採集、漁獵及游耕；不同雨量帶形成不同生產型態。原圖也標有綠洲灌溉等方式，說明水資源是重要限制。\n\nA氣溫、C溫差也可能影響農業，但不是這張非洲整體分布圖最主要的分類線索。D降雨類型著重降雨形成機制，與B直接比較雨量的多寡不同；不能把地形雨、對流雨等名稱拿來取代水分供給。\n\n這是本題傳統生產型態的簡化比較，不表示非洲所有地區都只有原圖列出的生業，也不由圖虛構精確年雨量或作物產量。',
1152:'答案B：X是伊拉克，對應乙；Y是土耳其，對應丙。題文的兩河流域文明與北部石油線索，指向伊拉克；逃難者希望經鄰近歐洲的土耳其進入歐洲，因此次序為乙、丙。\n\n原圖甲是伊朗、乙是伊拉克、丙是土耳其、丁是沙烏地阿拉伯。A把X判作伊朗且Y判作伊拉克；C雖以土耳其作Y，但X仍錯；D的兩國皆不符題意。不可只看到國名以伊開頭就把伊朗與伊拉克混同。\n\n題幹用曾描述歷史上的占領及逃難背景；新製地圖只輔助辨識國家位置及題文方向，不冒充現行控制範圍、精確逃難路線或難民人數。',
1153:'原卷訂正A。依目前可讀的題幹與現行規定，受監護宣告者若已符合公職罷免投票的其他資格，不再僅因監護宣告而失去該投票權；《公民投票法》第7條則仍要求未受監護宣告，因此A能解釋兩種票的資格差異。\n\nB的18至未滿20歲，原則可符合公投年齡卻尚未達公職選罷投票年齡，與題述方向相反。褫奪公權不應與監護宣告混為一談；D的遷入未滿6個月，不能單憑此判斷：公職選罷須看原選舉區的居住條件，全國性公投看國內連續居住，並非跨縣市搬家就重新起算國內居住。\n\n但是分享照片未包含本組上方共同閱讀，無法完整核對此次投票的日期、種類與前文條件。上述為現有題幹及現行法規的條件說明，先保存原卷A，不把缺失前文猜寫成核三或特定罷免新聞。查核：[公職人員選舉罷免法第14、15條]('+ELECT+')、[公民投票法第7、8條]('+REFER+')。',
1154:'原卷訂正A。依目前可讀條件，中央民意代表指立法委員；區域立委可由符合資格的原選舉區選民依法提出罷免，符合題意。B全國不分區立委及D由政黨票選出的立委，不適用公職人員罷免規定；C直轄市議員屬地方民意代表，不符合中央一詞。\n\n分享照片未包含題幹上文所指的共同閱讀。現有條件與現行法規可支持教材A，但仍須補齊共同文才能完成原題核對；不依來源AI推寫該新聞。查核：[公職人員選舉罷免法第2、3、75條]('+ELECT+')。',
1155:'答案D。屏東市是屏東縣下的縣轄市，縣這一層的民意代表是縣議員，市這一層則是市民代表。縣市兩層可分別關心公園、道路與地方安全等事務，所以是縣議員、市民代表。\n\n屏東市不能因名稱有市就當成直轄市或省轄市；A、C所列市議員不合本題縣轄市層級。B的區域立委屬中央民意代表，雖可關心地方議題，仍不屬本題所問地方民意代表。也要分清民意機關與行政機關：縣議會不同於縣政府，市民代表會不同於市公所。查核：[地方制度法第5、14條]('+LOCAL+')。',
1156:'答案D，對照附表為丁。臺南市是直轄市，西港區是一般行政區；本次地方選舉可選直轄市長、直轄市議員與里長。一般區的區長不是由區民直接選出，也沒有一般區民代表會，故不能多領區長、區民代表票。\n\n甲是中央選舉的總統副總統、區域立委及政黨票，與本次地方選舉不同。乙多出區長及區民代表兩項；丙列縣（市）長與縣（市）議員，並非直轄市的組合。直轄市山地原住民區具有不同制度，但西港區不是這類自治區，不可套用其區長、區民代表選舉。\n\n原題首投族依可領取選票的資格解讀，未提供生日，不自行補年齡或日期。查核：[地方制度法]('+LOCAL+')、[公職人員選舉罷免法]('+ELECT+')。'
}
REASONS={
1133:['拘役是刑罰，不是本題敦品中學所執行的感化教育。','有期徒刑是刑罰；不能以其他矯正學校的徒刑功能取代本題學校。','安置輔導由適當機構或處所執行，與本題具體學校不同。','敦品中學執行感化教育；屬少年保護處分。'],
1134:['罰鍰屬行政罰，與刑罰中的罰金不同。','警方取締及行政機關裁罰屬行政行為。','條例由立法院通過，屬法律位階。','主要目的為交通安全與公共利益，並非單純限縮權利。'],
1135:['17歲具有刑事責任能力，重大情節等條件下也可能裁量移送；不能絕對排除。','18歲已不屬現行少事法所稱少年。','依教材意圖最符合重大犯罪情境，但是否定罪判刑仍須依法審理。','未滿14歲不受刑罰，仍可能有保護處遇。'],
1136:['甲正確；起訴不是法官職權。','甲為少年法庭，乙為偵查並起訴的檢察官。','兩者均與題文職權不符。','檢察官正確，但甲不是少輔會。'],
1151:['本圖生活型態差異最主要受水分限制。','雨量多寡影響傳統農牧方式與分布。','溫差不是圖中整體分布的主要線索。','降雨形成的機制與雨量多寡不是同一概念。'],
1152:['甲是伊朗，乙是伊拉克，兩者次序不符。','乙伊拉克、丙土耳其，與兩河流域及赴歐方向符合。','丙正確，但X不是甲伊朗。','丁沙烏地阿拉伯與甲伊朗皆不符。'],
1153:['就現存題幹與現行法規，監護宣告造成兩項資格差異；共同閱讀仍待補。','年齡門檻方向相反：公投18歲，公職選罷20歲。','褫奪公權與監護宣告不同，不能直接套用。','須分清原選舉區與全國國內居住，不能只憑跨市遷入未滿6個月判斷。'],
1154:['中央民意代表且可依法罷免，符合現有條件；共同閱讀仍待補。','全國不分區立委依法不適用罷免。','屬地方民意代表，不是中央。','指政黨名單立委，與B同類。'],
1155:['市議員的層級不符，且區域立委屬中央。','區域立委是中央民意代表。','縣轄市設市民代表會，不設市議會。','屏東縣縣議員與屏東市市民代表，均為地方民意代表。'],
1156:['甲屬中央選舉票。','乙多出一般區不由民選的區長、區民代表。','丙是縣（市）層級，不是直轄市。','丁為直轄市長、市議員、里長，符合西港區。']}

def main():
    acquisition=json.loads((B.parent/'acquisition.json').read_text())['downloadedImages']
    dup=json.loads((B/'duplicate-review.json').read_text())
    manifest={'sourceId':'src-more-072','producerAgent':'/root','items':[]}
    for n,(index,subject,num,title,stem,options,letter) in QUESTIONS.items():
        qid=f'q-{n}';missing=n in [1153,1154];uncertain=n==1135
        question=stem+'\n'+'\n'.join(f'({chr(65+i)}) {v}' for i,v in enumerate(options))
        image=str(B/'crops'/f'{qid}-original.png')
        images=[image];figures=[]
        if n==1136:images.insert(0,str(B/'crops'/f'{qid}-passage-original.png'))
        figure={1133:('announcement','原卷教師甄選簡章：敦品中學111學年度、111-07-08、5357及法務部矯正署'),1135:('court','原卷法官對話：雖然尚未成年，但為犯罪行為，因此處有期徒刑'),1151:('africa','原卷非洲傳統農牧業分布圖，含赤道、南北回歸線及不同生活型態'),1152:('map','原卷西亞甲乙丙丁圖，保留國界、土耳其及兩河流域相對位置')}.get(n)
        if figure:
            suffix,alt=figure;figures=[dict(src=str(B/'crops'/f'{qid}-{suffix}-original.png'),alt=alt,caption='原卷必要附圖裁切，非AI重製；以可讀原圖為準。')]
        q=dict(id=qid,sourceId='src-more-072',subject=subject,title=('地理' if subject=='Geography' else '公民')+f'第{num}題｜'+title,
            chapter='綜合',volume='綜合',date='2026-11-17',dateLabel='首次出題日期',addedAt='2026-11-18',question=question,
            answer=('原卷教材訂正：' if missing or uncertain else '')+f'({letter}) '+options[ord(letter)-65],correctOption='' if missing or uncertain else letter,
            explanation=EXPLAIN[n],passage=PASSAGES.get(n,''),tables=TABLES.get(n,[]),images=images,questionFigures=figures,explanationFigures=[],
            verification='待核對原題' if missing or uncertain else '原卷逐題核對',verificationNote='已實開本題真正User原卷及必要附圖，保留完整可讀題幹與ABCD；日期取首次原提問台灣日，非實際考試日期。冊次章節無證據，歸綜合。'+('本組必要共同閱讀未包含於分享附件，不猜補。' if missing else '本題單選條件待確認，原題文字完整。' if uncertain else ''),
            contentStatus='待更新' if missing else '完整原題',originalQuestionNumber=num,sourceLabel='分享原卷｜第'+num+'題',
            studentAnswer=acquisition[index-1]['userText'],tags=['法律與生活'] if subject=='Civics' else ['自然環境與人文生活'],
            optionAnalysis=[dict(label=chr(65+i),text=o,wordClass='條件待核' if missing or uncertain else '應選' if i==ord(letter)-65 else '不選',meaning='',explanation=REASONS[n][i]) for i,o in enumerate(options)],
            trap='',diagram='',notes='',status='todo',starred=False)
        if missing or uncertain:
            q.update(reviewLabel='共同閱讀前文待補' if missing else '單選條件：A也可能進入少年刑事程序',
                     reviewQuestions=['請補原卷第33～35題上方的完整共同閱讀文字或原圖，以核對此次投票的日期、種類及其他前文條件；目前保留原卷訂正A。'] if missing else ['原卷訂正C，但A的17歲竊盜亦可能依少事法第27條第2項裁量移送並判刑。題幹未限定只問最輕本刑5年以上的應移送案件；是否保留教材C並註明此單選條件限制？'],
                     reviewExcerpt=question+('\n\n【可讀原圖對話】'+PASSAGES[n] if n in PASSAGES else ''))
        path=B/f'{qid}.json';path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
        viewed=[acquisition[index-1]['path'],*images,*[f['src'] for f in figures]]
        review=dict(id=qid,originalVisualChecked=True,completeOriginalAndOptions=not missing,requiredMaterialMissing=missing,
            sourceGeneratedArtUsed=False,actualViewed=list(dict.fromkeys(viewed)),inclusionEvidence=f"來源72第{index}張User原圖，使用者明示{acquisition[index-1]['userText']}；只收入這一題，不收同頁鄰題。",
            duplicateReview=next(r for r in dup if r['id']==qid),correctOptionIndependentReview=letter,
            originalFirstUserMessageId=acquisition[index-1]['messageId'],firstQuestionTimestamp=acquisition[index-1]['firstQuestionTimestamp'],
            missingMaterial='第33～35題共同閱讀未在24附件中' if missing else None,answerConditionUncertain=uncertain)
        rp=B/f'{qid}-review.json';rp.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
        manifest['items'].append(dict(candidateId=qid,disposition='new',draftPath=str(path),draftSHA256=hashlib.sha256(path.read_bytes()).hexdigest(),reviewPath=str(rp),reviewSHA256=hashlib.sha256(rp.read_bytes()).hexdigest(),originalImageIndices=[index],specPath=None,previewValidation=None,comicStatus='awaiting_illustration',awaitingConfirmation=missing or uncertain))
    (B/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
