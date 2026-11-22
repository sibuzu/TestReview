"""Producer-owned drafts and new scientific SVGs; never edits the shared bank."""
import json, hashlib, sys, html
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image

ROOT=Path(__file__).resolve().parents[4]
B=Path(__file__).resolve().parent
REL=B.relative_to(ROOT).as_posix()
SID='6b01da76-e42c-83ec-921a-80ff392862c1'
URL='https://chatgpt.com/share/'+SID
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for d in ['questions','reviews','crops','specs','art','qa']: (B/d).mkdir(exist_ok=True)
rects={1175:(7,(30,270,705,565)),1176:(8,(15,465,1079,705)),1177:(9,(25,458,1078,785)),1178:(10,(23,260,1078,836))}
for n,(image,r) in rects.items():Image.open(ROOT/f'docs/source-pages/chatgpt-6b01da76-{image}.jpg').crop(r).save(B/f'crops/q-{n}-original.png')
for n,im,r,name in [(1175,7,(707,332,1079,562),'map'),(1176,8,(710,447,1079,703),'earthquakes'),(1176,8,(28,545,704,681),'options'),(1178,10,(514,297,1077,480),'materials')]:
 Image.open(ROOT/f'docs/source-pages/chatgpt-6b01da76-{im}.jpg').crop(r).save(B/f'crops/q-{n}-{name}.png')
qdata={
1175:dict(number='12',title='地科第12題｜P處火山與板塊隱沒',stem='某一座火山位於右圖中的P處，試問它應是由於下述哪一種板塊相對運動方式所造成？',options=['兩板塊相互擠壓，其中一板塊沒入另一板塊之下','因軟流圈熱對流，使兩側板塊受到張裂性力量驅動而向兩側分開','兩相鄰板塊近乎平行的錯移','兩板塊近乎垂直的上下錯移'],answer='A',student='12@錯題B → A',tags=['板塊隱沒','火山','聚合型板塊邊界'],explanation='答案A。先讀原題地圖：P位於日本附近、太平洋西側的聚合型板塊邊界。兩板塊靠近，其中海洋板塊向下隱沒，與上方的岩漿生成及火山活動有關，因此應選A。\n\nB描述張裂型板塊邊界，兩側向外分離，可在中洋脊產生新海洋地殼與火山活動；但本題須按P的位置判斷，不能只因張裂處也可能有火山就選B。C是板塊近乎平行的水平錯動，主要累積與釋放剪應力，不能用來解釋P處這類火山帶。D的近乎垂直上下錯移也不是本題地圖所示火山帶的形成方式。\n\n本題只需辨認日本附近的隱沒型聚合邊界；實際區域板塊構造較複雜，圖解不把整個太平洋西緣硬畫成只有兩塊板塊。',analysis=['原圖P在日本附近聚合邊界；一板塊向下隱沒，符合火山帶的形成機制。','張裂處也可能有火山，但與原圖P所在邊界的類型不同。','近乎平行錯移不是P處火山帶的主要成因。','原圖未表示以近乎垂直上下錯移形成此火山帶。'],figures=[('map','原題P位置與板塊邊界圖；圖例區分聚合型與張裂型。')]),
1176:dict(number='17',title='地科第17題｜地震深度與板塊交界形式',stem='右圖為南太平洋海域的地震分布狀態，下列何者最可能是圖中X方框處的板塊交界形式？',options=['如原圖A：兩板塊靠近，其中一板塊向下隱沒','如原圖B：兩板塊向兩側分離','如原圖C：兩板塊沿交界水平錯移','如原圖D：兩板塊沿交界水平錯移（方向配置見原圖）'],answer='A',student='17@錯題B → A',tags=['地震深度','隱沒帶','聚合型板塊邊界'],explanation='答案A。先對照原圖圖例：黑實心圓是深源地震，空心圓是中源地震，點線表示淺源地震。X框內的震源由東側較淺，向西側逐漸加深，表示板塊向西側下方隱沒；A的隱沒構造符合這種分布。\n\nB的表面箭頭是向兩側分離，表示張裂型板塊邊界，不是「聚合但沒有畫出隱沒」。C、D的板塊在交界兩側近乎平行水平錯移。張裂與水平錯動邊界主要發生淺源地震，不能用來解釋本題同時具有中源、深源地震的傾斜隱沒帶。\n\n關鍵是震源深度與空間排列，不能只看地震很多就認定某種板塊交界；也不能把「有深源地震」擴張成所有聚合邊界都必有深源地震。',analysis=['聚合與向下隱沒符合淺、中、深源地震向一側逐漸加深的排列。','原選項箭頭向外，表示張裂型；原AI將B稱為聚合型是讀圖錯誤。','此圖是水平錯動，不能對應向地函深處延伸的震源帶。','同為水平錯動的另一箭頭配置，也不能對應本題隱沒震源帶。'],figures=[('earthquakes','原題南太平洋地震分布與圖例，保留X方框及北向。'),('options','原題四個板塊交界圖示A～D，保留各圖北向與運動箭頭；選項以此原圖為準。')]),
1177:dict(number='22',title='地科第22題｜中洋脊與海溝的年齡、運動比較',stem='中洋脊與海溝各自代表兩種不同板塊邊界的地形特徵，將最靠近中洋脊以及最靠近海溝的海洋地殼年齡，以及各自的板塊運動情形整理如右表所示，則下列關於W、X、Y、Z所填入的組合，何者最合理？',options=['W填入較老，X填入張裂','W填入較年輕，X填入聚合','Y填入較老，Z填入聚合','Y填入較年輕，Z填入張裂'],answer='C',student='22@錯題B → C',tags=['中洋脊','海溝','海洋地殼年齡'],explanation='答案C。先分開判斷年齡與板塊運動。中洋脊是海底擴張、新海洋地殼形成的位置，兩側板塊彼此遠離，所以W＝較年輕，X＝張裂。海洋地殼離開中洋脊後逐漸變老，在海溝附近隨板塊隱沒，因此本題比較下Y＝較老，Z＝聚合。\n\nA的X正確，但W錯；B的W正確，但X錯；C的Y與Z都正確；D的年齡與運動類型都錯。一個選項包含兩個條件，必須兩項都對才能選。\n\n「較老、較年輕」是本題中洋脊與海溝的相對比較，不表示所有海溝旁的地殼都必須有同一個絕對年齡。',analysis=['中洋脊是張裂邊界，但附近的新地殼較年輕，W不能填較老。','W較年輕正確；X應填張裂，不能填聚合。','海溝附近地殼相對較老，且屬聚合隱沒邊界，兩項都正確。','海溝應為相對較老、聚合，兩項皆不符。'],figures=[],tables=[dict(caption='原題比較表',headers=['地形特徵','中洋脊','海溝'],rows=[['海洋地殼年齡比較','W','Y'],['板塊運動情形','X','Z']])]),
1178:dict(number='23',title='地科第23題｜中洋脊兩側的移動與地殼年齡',stem='老師在課堂上以一張海報來讓學生分組上臺說明某一類型板塊交界的各項特徵，如右圖（一）所示。右圖（二）為老師提供學生使用的貼紙，並告訴學生這些貼紙上的箭頭或文字的用途，是用來說明兩板塊相對運動方向與海洋地殼年齡的關係，若要正確呈現這類型板塊交界的特徵，下列哪一種黏貼方式最為合理？',options=['左側→、較新—較老；右側←、較老—較新','左側←、較新—較老；右側→、較老—較新','左側→、較老—較新；右側←、較新—較老','左側←、較老—較新；右側→、較新—較老'],answer='D',student='23 @錯題A → D',tags=['中洋脊','海底擴張','海洋地殼年齡'],explanation='答案D。圖（一）的板塊交界位於海底隆起處，對應中洋脊。新海洋地殼在交界處形成，兩側板塊向外分開，因此左側板塊向左←，右側板塊向右→。\n\n再讀年齡貼紙：各側文字都按圖中由左到右的方向讀。左半邊從遠離中洋脊處走向交界，是「較老—較新」；右半邊從交界走向外側，是「較新—較老」。兩邊共同原則都是靠近中洋脊較新、往外較老，符合D。\n\n逐項比較：A的箭頭向內聚合，而且年齡排列也反了；B箭頭向外正確，但年齡排列相反；C年齡排列正確，但箭頭向內；D方向與年齡兩項都正確。原AI說「A與D年齡排列完全相同、A只有方向錯」，不符合原卷；年齡相同的比較應是C與D。答案D仍維持，但選項解說已依原卷訂正。',analysis=['箭頭向內，且左新—老／右老—新的年齡排列也與中洋脊不符。','向外移動正確，但兩側年齡貼紙應反過來。','左老—新、右新—老的年齡排列正確，但箭頭向內錯誤。','向外張裂，靠近交界較新、遠離交界較老，兩項都正確。'],figures=[('materials','原題圖（一）海報剖面與圖（二）貼紙；海報下兩列留白供黏貼。')],tables=[dict(caption='四個原圖選項的貼紙內容（各側年齡文字均由左至右讀）',headers=['選項','左側箭頭','右側箭頭','左側年齡','右側年齡'],rows=[['A','→','←','較新—較老','較老—較新'],['B','←','→','較新—較老','較老—較新'],['C','→','←','較老—較新','較新—較老'],['D','←','→','較老—較新','較新—較老']])])}
now=datetime.now(timezone.utc).isoformat()
sources=[dict(title='USGS：地震深度與隱沒帶',url='https://www.usgs.gov/faqs/what-depth-do-earthquakes-occur-what-significance-depth'),dict(title='USGS：隱沒帶地震、海溝與火山',url='https://www.usgs.gov/special-topics/subduction-zone-science/science/introduction-subduction-zones-amazing-events'),dict(title='NOAA：海床年齡與張裂邊界',url='https://sos.noaa.gov/catalog/datasets/age-of-the-seafloor/')]
for n,d in qdata.items():
 qid=f'q-{n}';opts=d['options']
 if n==1175:d['title']='地科第12題｜P處火山與板塊相對運動'
 if n==1176:d['stem']+='\n（以下文字為圖示選項的輔助辨讀，選項以原卷附圖為準。）'
 q=dict(id=qid,sourceId='src-more-074',subject='Earth',title=d['title'],chapter='綜合',volume='第五冊',date='2026-11-22',dateLabel='首次出題日期',addedAt='2026-11-22',question=d['stem']+'\n'+'\n'.join(f'({chr(65+i)}) {o}'for i,o in enumerate(opts)),answer=f'({d["answer"]}) '+opts[ord(d['answer'])-65],correctOption=d['answer'],explanation=d['explanation'],trap='',verification='原卷逐題核對',verificationNote='已實開真正User原卷、完整題幹、四選項及必要圖表；日期取首次User提問台灣日，非實際考試日。原卷頁首明示國中自然科學（五），可確認第五冊；尚未核對正式章節映射，章節歸綜合。',diagram='',notes='',status='todo',starred=False,tags=d['tags'],images=[f'{REL}/crops/{qid}-original.png'],sourceLabel=f'分享原卷｜第{d["number"]}題',studentAnswer=d['student'],contentStatus='完整原題',passage='',originalQuestionNumber=d['number'],optionAnalysis=[dict(label=chr(65+i),text=o,wordClass='應選'if chr(65+i)==d['answer']else'不選',meaning='',explanation=d['analysis'][i])for i,o in enumerate(opts)],tables=d.get('tables',[]),questionFigures=[dict(src=f'{REL}/crops/{qid}-{name}.png',alt=cap,caption=cap)for name,cap in d['figures']],explanationFigures=[])
 if n==1175:q['images'].append(f'{REL}/crops/{qid}-map.png')
 save(B/f'questions/{qid}.json',q)
 review=dict(id=qid,originalVisualChecked=True,completeOriginalAndOptions=True,requiredMaterialMissing=False,sourceGeneratedArtUsed=False,actualViewed=[f'docs/source-pages/chatgpt-6b01da76-{rects[n][0]}.jpg',f'{REL}/crops/{qid}-original.png']+[f['src']for f in q['questionFigures']],inclusionEvidence=f'使用者指定{d["student"]}；只收入該題，未收入鄰題或AI延伸練習。',duplicateReview='已搜尋正式題與全部草稿META，逐項比對題幹、選項及必要圖形。未找到相同完整原題；同題材的海溝、中洋脊題條件和選項不同，不合併。',dateEvidence='對應原User訊息timestamp換算Asia/Taipei為2026-11-22，非匯入日或實際考試日。',sources=sources,reviewedAt=now)
 save(B/f'reviews/{qid}.json',review)
changes=[dict(questionId='q-1176',originalAIChatLink=URL,before='原AI將B稱為聚合型、未明確呈現隱沒，並把D稱為張裂型。',after='依原卷箭頭，B為張裂型，C與D均為水平錯動圖示；A為向下隱沒的聚合型，答案仍A。',reason='原AI沒有依原卷的實際箭頭辨認板塊相對運動。'),dict(questionId='q-1178',originalAIChatLink=URL,before='原AI稱A與D的年齡排列完全相同，A年齡正確但箭頭錯；表中也把A判為年齡對、C判為年齡錯。',after='A的方向與年齡都錯；B方向對但年齡錯；C年齡對但方向錯；D兩項都對。年齡排列相同的是C與D，答案仍D。',reason='逐讀原圖：A左較新—較老／右較老—較新，D左較老—較新／右較新—較老；原AI的比較與原卷相反。')]
save(B/'review-changes.json',changes)
print('Saved four complete original-question drafts and reviews.')
