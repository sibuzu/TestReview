from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).parent;src='https://chatgpt.com/share/6afb1a9c-4f5c-83e8-becb-a35cb4110073'
all=[]
for n in range(1112,1121):
 q=f'q-{n}';path=P/f'{q}.json';d=json.load(open(path));r=dict(candidateId=q,originalVisualChecked=True,completeOriginalAndOptions=True,sourceGeneratedArtUsed=False,actualViewed=[f'docs/source-pages/chatgpt-6afb1a9c-{n-1104}.jpg']+d['images']+[x['src'] for x in d['questionFigures']],inclusionEvidence=dict(userMessage=d['studentAnswer'],originalImageIndex=n-1104,redCorrectionRetained=True,adjacentQuestionsExcluded=True),duplicateReview=dict(candidateIndex='duplicate-candidates.json',keywordSearch='duplicate-search.json',result='new',compared=['q-1046：皂化反應角色，非本題乙醇四敘述；題幹、材料與四選項不同','q-279：蘋果汁/碘液氧化還原，非乙醇物性','q-112：鉻酸平衡，非次氯酸/酒精題'] if n==1114 else [],reason='索引無相同題幹/選項候選；九原題與條件互不重複，圖表/所有選項已逐題實核。'),dateEvidence='acquisition downloadedImages首次user訊息epoch轉Asia/Taipei；2026-11-16，非加入或分享建立日期',passed=True,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
 rp=P/f'{q}-review.json';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 all.append(dict(candidateId=q,disposition='new',draftPath=str(path),draftSHA256=hashlib.sha256(path.read_bytes()).hexdigest(),originalImageIndices=[n-1104],duplicateQuestionId=None,specPath=None,previewValidation=None,reviewPath=str(rp)))
(P/'manifest.json').write_text(json.dumps(dict(sourceId='src-more-071',sourceUrl=src,items=all),ensure_ascii=False,indent=2)+'\n')
rv=[]
for q,kind,reason,before,after in [('q-1118','原AI圖表判讀訂正','原AI把B圖乙線的立即升溫誤讀為持續0°C，並誤說末段不同溫；也把A的升溫線錯指甲。','原AI說B「甲逐漸下降，乙維持0°C，最後停在不同溫度」，A「甲下降後又上升，乙始終接近0°C」。','B乙原圖由0°C立即升溫，最後與甲同溫；缺少冰熔化的初期恆溫段。A甲降至近0°C而乙升至較高溫；不是甲回升。答案C維持。另保留原題未給質量、C依全熔命題預設的條件限制，不杜撰質量。'),('q-1115','原題語句限制','原題「且無毒」不能當無條件安全保證；原AI未釐清此句。保留印刷材料，詳解須限制濃度、途徑與混用風險。','原卷前言稱「次氯酸溶解於水中後，具有很強的消毒性能，且無毒」。','原印照留；詳解明示並非任意濃度/用途/接觸皆安全或當前產品防疫效力保證；按產品標示、不自行混用。答案B不變，氨水也不可混用。')]:
 d=json.load(open(P/f'{q}.json'));rv.append(dict(questionId=q,kind=kind,questionText=(d.get('passage','')+'\n'+d['question']).strip(),questionUrl=f'https://monitor-test.sibuzu.com/site/index.html#question/{q}',sourceUrl=src,reason=reason,before=before,after=after))
(P/'reviews.json').write_text(json.dumps(rv,ensure_ascii=False,indent=2)+'\n')
print('9 drafts and review manifest ready')
