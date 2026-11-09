from pathlib import Path
import json,hashlib,datetime,subprocess
D=Path(__file__).resolve().parent;R=D.parents[3]
def rel(p):return str(p.relative_to(R))
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
viewed={1041:[7,8],1042:[9],1043:[10],1044:[11],1045:[12]}
details={
1041:'正式索引對特殊動物零候選；全庫題幹相似最高q-354是勸諫、q-289是崔延伯，文章與選項皆不同。本題兩張原卷一張甲乙全文、一張第36題，只有第36題是本次使用者提問；第35題未加。',
1042:'正式索引鋼絲絨無命中；碳酸鈉命中q-112鉻酸鉀平衡與q-556化學式慣例，皆非本題開放系統的兩反應質量選擇。全題幹比對無相同條件及四選項。',
1043:'碘關鍵詞q-279為蘋果汁氧化還原，與本題鹼性碘反應不同；題幹近似q-114為鉻酸根與二氧化碳，q-460為其他反應加入NaOH的時點，反應物、方程式、題幹及四選項均不同。',
1044:'豚鼠候選q-104為黑白毛、兩黑毛親代1黑3白與長期曲線；本題是長短毛8短2長、四種親代基因型，完整條件與選項不同，不合併。',
1045:'雙氧水與過氧化氫索引均無既有命中；全庫題幹與圖表核對未見本題30/10、20/20、10/30混合及四個散點圖。第22題雖同頁卻是獨立遺傳題，無共同材料，不合組。'}
items=[]
for number in range(1041,1046):
 qid=f'q-{number}';qp=D/(qid+'.json');q=json.loads(qp.read_text())
 choices=q['question'].split('\n(A) ',1)[1];parts=['A) '+choices]
 import re
 values=re.findall(r'\(([ABCD])\) ([^\n]+)',q['question'])
 q['optionAnalysis']=[dict(label=label,text=text,wordClass='應選' if label==q['correctOption'] else '不選',meaning='',explanation={'q-1041':{'A':'兩文並未支持所有店家都有專業人員盡責照顧；乙文有反例。','B':'好奇心未成為甲、乙共同明確支持的興趣來源。','C':'甲文談互動壓力，乙文談不當飼養，均指出動物福利可能受忽略。','D':'兩文未說所有動物都接受社會化訓練。'},'q-1042':{'A':'甲有外界氧氣進入並與鐵結合，量得質量增加。','B':'乙只形成留在容器中的沉澱，在排除蒸發等損失時總質量不變。','C':'甲不符合，不能兩者都選。','D':'乙在開放環境仍可測得前後總質量相同。'},'q-1043':{'A':'酸會消耗OH⁻，依題示反應傾向逆反應，與顏色變淡不合。','B':'加鹼增加OH⁻，促使正反應消耗紅褐色I₂。','C':'加酸可傾向逆反應，但I₂增加會使顏色加深，不合題幹。','D':'加鹼傾向正反應，不能配逆反應。'},'q-1044':{'A':'全部子代Ss、短毛，無法產生長毛。','B':'子代SS或Ss，全部短毛。','C':'可產生Ss短毛與ss長毛，符合觀察到兩種毛長。','D':'全部子代ss、長毛，無法產生短毛。'},'q-1045':{'A':'濃度編號由左至右I、II、III不符濃度由低到高。','B':'濃度與速率都按III、II、I遞增。','C':'濃度編號由左至右I、II、III先排錯。','D':'濃度編號正確，但將濃度增加畫成速率下降。'}}[qid][label]) for label,text in values]
 assert len(values)==4
 save(qp,q)
 av=[f'docs/source-pages/chatgpt-6af1d6de-{i}.jpg' for i in viewed[number]]+q['images']+[f['src'] for f in q.get('questionFigures',[])]
 review=dict(id=qid,reviewerAgent='/root/comic_lane_3',originalVisualChecked=True,completeOriginalAndOptions=True,sourceGeneratedArtUsed=False,actualViewed=list(dict.fromkeys(av)),duplicateReview=dict(exactOriginalQuestionMatch=False,candidates=[],checkedAgainst=details[number]),inclusionEvidence=q['studentAnswer'],checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),sourceUrl='https://chatgpt.com/share/6af1d6de-09f8-83ee-bb43-0897e3964704',answerIndependentlyChecked=True,explanationChecked=True,passed=True,originalQuestionNumber=q['originalQuestionNumber'],teachingComicState='queued',cropReview='實際開啟所有列於actualViewed的原卷及裁切成品；完整題幹、全部四選項、必要甲乙閱讀文／表格／四圖均保留。只旋轉與裁切，未去除或重製筆跡。')
 rp=D/(qid+'-review.json');save(rp,review)
 items.append(dict(id=qid,status='ready',questionPath=rel(qp),questionSHA256=sha(qp),reviewPath=rel(rp),reviewSHA256=sha(rp)))
save(D/'manifest.json',dict(sourceId='src-more-065',producerAgent='/root/comic_lane_3',status='ready',items=items,originalQuestionCount=5,questionPageCount=5,teachingComics='queued_separately',notes='後五原問均可完整核對；未加入同頁其他未提問題，亦不採來源AI延伸或插畫。'))
save(D/'reviews.json',dict(items=[],reason='本路五題均維持使用者指定與原AI相同答案（C/B/B/C/B），未發現需另請使用者確認的實質答案或條件錯誤。q-1041依原卷校正原AI轉錄中的繁養為豢養；q-1045保留原表空白，解說採濃度排序與1/時間，不填入原題未給的時間或速率。'))
print('ready',len(items))
