from pathlib import Path
import json,hashlib,datetime,time
from PIL import Image
R=Path('/home/jack/git/TestReview');P=R/'docs/imports/new-gpt-20261029-a';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for d in ['questions','qa','reviews']: (P/d).mkdir(exist_ok=True)
images=json.loads((P/'original-image-map.json').read_text())
for i,m in enumerate(images,1):
 rot=90 if i in [1,4,5,6,7] else 0
 m.update(visualChecked=True,visualReviewRecordedAt=now,rotationDegrees=rot,uprightPath=f'.cache/new-gpt-20261029-a-upright/user-{i:03}.png' if rot else m['path'])
 m.pop('uprightCandidatePath',None);m.pop('candidateRotationDegrees',None)
dump(P/'original-image-map.json',images)
acq=json.loads((R/'docs/acquisition/new-gpt-20261029-a.json').read_text());acq.update(state='transcribing',checkedAt=now,downloadedImages=images,downloadedImageCount=9,expectedImageCount=9,visualChecked=True,visuallyCheckedImageCount=9,candidateOriginalQuestionCount=11,candidateEntryCount=10,currentQuestionId='q-850',currentOriginalQuestionNumber=11,sourceTitle='錯題解析',noTranscriptionStarted=False,groupingEvidence='僅原35、36共用34～37原題組上文；15、16同頁但分立。41只收已問小題、保留完整共同材料。')
dump(R/'docs/acquisition/new-gpt-20261029-a.json',acq)
source=dict(id='src-more-049',url=acq['url'],title='錯題解析',date='2026-10-29',dateLabel='首次出題日期',dateBasis='原使用者題目訊息create_time轉Asia/Taipei；非分享網址建立日、非推定實際測驗日',transcriptPath=str((P/'transcript.txt').relative_to(R)),archivePath=str((P/'archive.json').relative_to(R)),images=['assets/originals/q-850-original.webp'],originalImageMapPath=str((P/'original-image-map.json').relative_to(R)),state='transcribing',questionIdReservation='偶數q850、852…依原題原子順序；真題組保留各子永久qid',excludedContent='不收入AI另編類似題、延伸練習或來源AI漫畫')
dump(P/'source.json',source)
cache=R/'.cache/new-gpt-20261029-a-publish';cache.mkdir(exist_ok=True)
original=cache/'q-850-original.webp';Image.open(R/images[0]['uprightPath']).crop((0,225,1420,715)).save(original,lossless=True,method=6)
art=R/'docs/comics/art/q-850.svg';art.parent.mkdir(exist_ok=True)
art.write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">
<rect width="540" height="180" fill="#f8fbf3"/>
<g font-family="Noto Sans CJK TC,sans-serif" text-anchor="middle" fill="#294d42">
<text x="90" y="19" font-size="12">題幹已說：髮菜是藍菌</text>
<rect x="36" y="29" width="108" height="28" rx="9" fill="#d9ead7"/><text x="90" y="49" font-size="14" font-weight="bold">原核生物</text>
<ellipse cx="90" cy="106" rx="56" ry="32" fill="#e9f2dc" stroke="#527b66" stroke-width="3"/>
<path d="M62 96C74 79 107 124 119 102C108 90 76 125 66 108C79 93 107 121 117 110" fill="none" stroke="#b57b45" stroke-width="3"/>
<g fill="#72977a"><circle cx="53" cy="103" r="2"/><circle cx="82" cy="123" r="2"/><circle cx="111" cy="87" r="2"/></g>
<text x="90" y="154" font-size="10.5">原核細胞示意：有DNA</text><text x="90" y="171" font-size="10.5">沒有核膜包住的細胞核</text>
<g transform="translate(180)"><rect x="8" y="28" width="164" height="135" rx="12" fill="#fff" stroke="#9db79d"/>
<rect x="27" y="44" width="126" height="29" rx="7" fill="#d9ead7"/><text x="90" y="64" font-size="13" font-weight="bold">原核生物界</text>
<path d="M90 74V94M47 94H133M47 94V111M133 94V111" fill="none" stroke="#648974" stroke-width="2"/>
<rect x="16" y="111" width="65" height="29" rx="7" fill="#edf4e5"/><text x="48.5" y="131" font-size="12">髮菜</text>
<rect x="94" y="111" width="70" height="29" rx="7" fill="#edf4e5"/><text x="129" y="131" font-size="12">念珠藻</text>
<text x="90" y="19" font-size="12">不必每個階層都相同</text><text x="90" y="155" font-size="10.5">共同的「界」就符合題意</text></g>
<g transform="translate(360)"><text x="90" y="19" font-size="12">四選項的細胞類型</text>
<rect x="9" y="29" width="162" height="132" rx="9" fill="#fff" stroke="#a6bca5"/>
<path d="M10 62H170M10 95H170M10 128H170" stroke="#e0e8db"/>
<rect x="11" y="96" width="158" height="31" fill="#d9ead7"/>
<g font-size="12" text-anchor="start"><text x="17" y="51">A 高麗菜</text><text x="17" y="84">B 石花菜</text><text x="17" y="117" font-weight="bold">C 念珠藻</text><text x="17" y="150">D 新月藻</text></g>
<g font-size="12" text-anchor="end"><text x="161" y="51">真核</text><text x="161" y="84">真核</text><text x="161" y="117" font-weight="bold">原核</text><text x="161" y="150">真核</text></g></g></g></svg>''')
spec=dict(id='q-850',subject='Biology',title='名字有菜或藻，分類仍要看生物特徵',art=str(art.relative_to(R)),layoutVersion='native-fluid-v6',panels=[dict(heading='① 題幹已指出：髮菜是藍菌',text='藍菌是原核生物，有DNA，卻沒有核膜包住的細胞核。食材俗名帶有「菜」，不表示它就是植物。',alt='原核細胞示意，DNA直接位在細胞內，未畫出核膜包住的細胞核。'),dict(heading='② 念珠藻也在原核生物界',text='依本題的國中五界分類，髮菜與念珠藻都在原核生物界。只要「界」這一個階層相同，就符合題目的「至少一個」。',alt='分類樹以原核生物界連接髮菜與念珠藻，未捏造同種或其他更小階層。'),dict(heading='③ 比細胞特徵，不比名字',text='高麗菜、石花菜、新月藻都是真核生物。念珠藻雖然名稱有「藻」，實際上是藍菌，因此這題應選C。',alt='逐項比較四選項細胞類型，A、B、D為真核，C念珠藻為原核。')],fourth=dict(heading='④ 至少一個相同階層即可',answer='答案 C：念珠藻',points=['髮菜與念珠藻都為藍菌。','兩者共同在原核生物界，已符合題意。','不需要證明所有分類階層都完全相同。']),protectedWords=['髮菜','藍菌','念珠藻','原核生物界','高麗菜','石花菜','新月藻','真核生物','DNA'],generationMethod='precise_native_svg',generationCalls=0,sourceGeneratedArtUsed=False,sourceOriginalImage=images[0]['path'],sourceOriginalSHA256=images[0]['sha256'],sourceQuestionNumber=11,startedAt=now,startedMonotonicNs=time.monotonic_ns(),timingScope='本題專屬原稿、原生SVG與隔離QA；不含先前來源取圖及整批原卷預讀',rationale='精確細胞示意、分類樹與四選項比較比人物圖更能直接釐清本題五界分類。原題、紅筆C與獨立核對一致；不使用來源AI圖。')
dump(R/'docs/comics/q-850.json',spec)
choices=[('A','至少有一個分類階層與高麗菜相同','高麗菜是植物，為真核生物；髮菜是藍菌，不是植物。'),('B','至少有一個分類階層與石花菜相同','石花菜為紅藻，是真核生物，不是原核的藍菌。'),('C','至少有一個分類階層與念珠藻相同','念珠藻與髮菜均為藍菌，在本題五界分類中同在原核生物界，至少界這一階層相同。'),('D','至少有一個分類階層與新月藻相同','新月藻為綠藻，是真核生物，不能因名稱帶藻就當成藍菌。')]
comic={k:spec[k] for k in ['title','panels','fourth','protectedWords']};comic['art']='assets/comics/q-850-new-art.svg'
q=dict(id='q-850',sourceId='src-more-049',subject='Biology',title='生物第11題｜髮菜與念珠藻的分類階層',chapter='綜合',volume='綜合',date='2026-10-29',dateLabel='首次出題日期',addedAt='2026-10-29',originalQuestionNumber=11,question='髮菜是一種藍菌，音似「發財」，故常被用於宴席食用。現今因過度採挖，已被禁止採集與銷售，下列關於「髮菜」的敘述，何者正確？\n'+'\n'.join(f'({l}) {t}' for l,t,e in choices),answer='(C) 至少有一個分類階層與念珠藻相同',explanation='題幹已指定髮菜是藍菌。依本題採用的國中五界分類，藍菌歸在原核生物界，念珠藻也是藍菌，因此髮菜與念珠藻至少在「界」這個分類階層相同，C正確。\n\n分類階層由大到小為界、門、綱、目、科、屬、種。題目說「至少有一個」，所以證明兩者同界已經足夠，不必把每個階層都列出來。高麗菜、石花菜、新月藻都是真核生物，不能因俗名有「菜」或「藻」就判定與髮菜同類。',trap='俗名有「菜」不等於植物；名字帶「藻」也不一定是原生生物。先抓題幹已指定的藍菌身分。',tags=['藍菌','原核生物','五界分類','分類階層'],verification='原卷逐題核對',verificationNote='已實看9張原卷，本題11題幹及全部四選項完整；紅筆C與獨立分類核對一致。原卷上相鄰第10、12題未被使用者詢問，本次不另收入。',images=['assets/originals/q-850-original.webp'],questionFigures=[],explanationFigures=[],tables=[],passage='',sourceLabel='分享原卷｜第11題',studentAnswer='B',correctOption='C',optionAnalysis=[dict(label=l,text=t,wordClass='應選' if l=='C' else '不選',meaning='',explanation=e) for l,t,e in choices],contentStatus='完整原題',status='todo',starred=False,notes='',teachingComic=comic)
dump(P/'questions/q-850.json',q)
assets=[dict(sourcePath=str(original.relative_to(R)),targetPath=q['images'][0],sha256=sha(original),lossless=True,kind='original_crop',cropBox=[0,225,1420,715],originalSHA256=images[0]['sha256']),dict(sourcePath=str(art.relative_to(R)),targetPath=comic['art'],sha256=sha(art),lossless=True,kind='new_native_art')]
dump(P/'asset-map.json',assets)
proof=dict(id='q-850',sourceQuestionNumber=11,originalPath=images[0]['path'],originalSHA256=images[0]['sha256'],actualViewed=images[0]['uprightPath'],fullStemAndFourChoicesChecked=True,originalHandwrittenAnswer='B',originalRedCorrection='C',independentAnswer='C',sourceAIAnswer='C',newSubstantiveDisagreement=False,necessaryQuestionFigure=False,sourceGeneratedArtUsed=False,dedup=dict(sqliteSearches=['髮菜','念珠藻'],strongDuplicateIds=[]),referenceSources=[dict(title='臺大科學Online〈髮菜〉，國中自然教師撰文、臺師大生科教師責編',url='https://case.ntu.edu.tw/highscope/%E9%AB%AE%E8%8F%9C%EF%BC%88bangia-atropurea%EF%BC%89/index.html',supports='正文另述的藍菌髮菜為念珠藻目的原核生物；題幹已明確指定藍菌，不和同俗名紅毛菜混用。',checkedAt=now)],dateBasis='原使用者訊息create_time，Asia/Taipei為2026-10-29')
dump(P/'reviews/q-850-content.json',proof)
qa_src=(R/'docs/imports/new-gpt-20261029-b/check-new-draft.cjs').read_text().replace('new-gpt-20261029-b','new-gpt-20261029-a').replace('weirugo-new-gpt-b-','weirugo-new-gpt-a-')
(P/'check-new-draft.cjs').write_text(qa_src)
print('q-850 draft / fresh SVG / source crop ready for isolated QA',sha(original),original.stat().st_size)
