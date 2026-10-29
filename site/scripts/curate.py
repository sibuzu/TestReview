"""Rebuild the reviewed, versioned browser dataset from archived source evidence."""
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from review_requests import apply_review_requests
from pending_sources import apply_pending_sources
BASE = Path(__file__).resolve().parents[1]
ROOT = BASE if (BASE / 'docs/sources').exists() else BASE.parent
DEST = BASE / 'dist'
subjects = [
 ('Chinese','國文','南一','文'),('English','英文','翰林','Aa'),('Math','數學','康軒','π'),
 ('Biology','生物','翰林','生'),('Physics-Chemistry','理化','翰林','理'),('Earth','地科','翰林','地'),
 ('History','歷史','康軒','史'),('Geography','地理','康軒','圖'),('Civics','公民','康軒','民')]
sources=[]
(DEST/'sources').mkdir(exist_ok=True)
files=['6ae04cde-c9c8-83ee-a7da-581604501e2b','6ae04d90-c71c-83ee-9e37-548bbbcaa04c','6ae04e07-ac08-83e8-a547-b5a07976b7d8','6ae04e1a-cca0-83e8-9529-2f4efc7a0673','6ae04e56-3000-83ee-8868-eabc56516027','6ae04e77-8d18-83e8-b44b-5e20e25e3b37','gemini-english','gemini-chinese','gemini-science']
images=json.loads((ROOT/'docs/sources/image-downloads.json').read_text())
for i,key in enumerate(files):
 d=json.loads((ROOT/f'docs/sources/{key}.json').read_text())
 if 'messages' in d:
  ms=[m for m in d['messages'] if m['author']['role'] in ['user','assistant'] and m['content'].get('parts')]
  text='\n\n'.join(m['author']['role']+'\n'+'\n'.join(p if isinstance(p,str) else '[原卷附圖：請依本來源的圖片保存狀態核對]' for p in m['content']['parts']) for m in ms)
  date=datetime.datetime.fromtimestamp(ms[0]['create_time'],datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()
  title=d['title'];missing=any(isinstance(p,dict) and p.get('content_type')=='image_asset_pointer' for m in ms for p in m['content']['parts'])
 else:
  text=d['text']
  created=re.search(r'Created with[^\n]*?([A-Z][a-z]+ \d{1,2}, \d{4}) at',text)
  if not created:raise ValueError(f'{key}: missing Gemini Created date; do not substitute publication or import date')
  date=datetime.datetime.strptime(created.group(1),'%B %d, %Y').date().isoformat()
  title={'gemini-english':'英語考古題對答案與解析','gemini-chinese':'國文錯題分析與複習計畫','gemini-science':'自然考題錯題分析與複習'}[key];missing=False
 (DEST/f'sources/{key}.txt').write_text(text)
 sources.append(dict(id=f'src-{i+1}',url=d['url'],title=title,platform='ChatGPT' if i<6 else 'Gemini',status='read',content='',date=date,addedAt='2026-10-27',transcript=f'sources/{key}.txt',images=[x['path'] for x in images if x['source']==key and 'path' in x],note=('對話文字及原始附圖已透過已登入的分享頁保存。' if any(x['source']==key and 'path' in x for x in images) else '對話文字已讀取；原始附圖尚待補齊。') if missing else '已保存對話文字。'+('原卷照片已下載；為分享頁預覽解析度。' if i>=6 else '')))
extra_sources=ROOT/'docs/additional-sources.json'
if extra_sources.exists():sources.extend(json.loads(extra_sources.read_text()))
records=[]
def add(src,subject,title,chapter,question,answer,explanation,trap,tags,verification='整理',volume='綜合',note='',diagram=''):
 records.append(dict(id=f'q-{len(records)+1:03}',sourceId=f'src-{src}',subject=subject,title=title,chapter=chapter,volume=volume,date=sources[src-1]['date'],dateLabel='首次出題日期',addedAt='2026-10-27',question=question,answer=answer,explanation=explanation,trap=trap,tags=tags.split('、'),verification=verification,verificationNote=note,diagram=diagram,images=[],status='todo',starred=False,notes=''))
add(1,'Chinese','張釋之：依法斷案與人物判讀','文言閱讀','閱讀《史記・張釋之馮唐列傳》改寫段落，判讀張釋之的執法原則、人物語氣與文帝的態度。','依法審理、不畏權勢；文帝最終接受合理諫言。','原始輸入含「道高廟」「下庭畏」等疑似語音辨識錯字。先核對原文，再分辨盜取宗廟器物的實際案件，與「假令愚民取長陵一抔土」的假設論證。對話中的逐句翻譯與選項文字不可直接作為定稿。','不要把假設當成已發生的事；不要把「廷尉」誤解成庭院中的職位。','文言文、人物形象、審題','待核對',note='原文有多處辨識錯字；需提供原始題本或清楚文字。冊次無可靠依據，歸綜合。')
add(2,'English','Amber 的考前一晚：作文訂正','寫作與時態','訂正：Amber played video game too late, so she didn’t prepare her exam. She regret about it. She swear that she never do again.','played video games until very late; prepare for her exam; regretted it; swore she would never do it again.','敘述過去事件時維持過去式。prepare for 表示「為……做準備」；regret 可直接接受詞，不加 about；swear 的過去式為 swore，轉述未來承諾可用 would。\n參考改寫：Amber played video games until very late, so she didn’t prepare for her exam. She regretted it and swore she would never do it again.','too late 本身不是一律錯誤，要依情境判斷；這裡用 until very late 精準描述玩到很晚。','過去式、動詞搭配、寫作')
add(3,'Math','第 17 題｜正方形外的 AE','四邊形與座標','正方形 ABCD 邊長 1，AE ∥ BD，BE = BD，求 AE（依對話中 E 向外延伸的位置）。','AE = (√6 − √2) / 2','取 B=(0,0)、A=(0,1)、D=(1,1)，設 AE=t，則 E=(t/√2,1+t/√2)。由 BE²=2 得 t²+√2t−1=0，取正根即得答案。','設參數時確認它是線段長，還是方向向量的倍數；兩者差 √2。','座標法、畢氏定理','待核對',note='計算已按對話文字重算；原圖無法下載，E 的實際位置仍待核對。')
add(3,'Math','第 19 題｜矩形的角度分配','四邊形與角度','矩形中 AE ⟂ BD，∠DAE = 3∠BAE，求 ∠EAC。','依對話位置條件：45°','設 ∠BAE=x，直角可分為 x+3x=90°，得 x=22.5°。後續須結合矩形對角線的角度及 E 的位置，對話給出 ∠EAC=45°。','圖中射線位置會影響角度相加或相減。','角度、矩形','待核對',note='缺原圖，保留來源推論，待核對射線位置。')
add(3,'Math','第 20 題｜等面積與黃金比例','四邊形與面積','矩形中 [△APQ]=[△BCP]=[△CDQ]，求 AQ:QD（依對話中的 P、Q 位置）。','AQ:QD = (1+√5)/2 : 1','設矩形寬 w、高 h，AQ=q、AP=p。等面積可化為 pq=w(h−p)=h(w−q)。令 p/h=q/w=r，得 r²=1−r，r=(√5−1)/2。故 q/(w−q)=(1+√5)/2。','比較面積前要先找對每個三角形的底與高。','等面積、黃金比例','待核對',note='代數已重算，P、Q 的原始圖示尚待補齊。')
add(3,'Math','第 21 題｜AI 解答矛盾：面積真的是 8？','四邊形與座標','正方形內點 P，PA=1、PB=3、PD=√7，求正方形面積。','依這組條件，面積應為 8 + √14；原對話後續的「8」推導錯誤。','設 A=(0,0)、B=(s,0)、D=(0,s)、P=(x,y)，令 u=s²。由三個距離平方得 x=(u−8)/(2s)、y=(u−6)/(2s)。代入 x²+y²=1，得 (u−8)²+(u−6)²=4u，即 u²−16u+50=0。\nu=8±√14；P 在正方形內要求 x、y>0，所以取 u=8+√14。\n英國旗定理只保證 PA²+PC²=PB²+PD²，並不保證這個和等於 2s²。','原 AI 把任意內點套入「對角頂點距離平方和=2s²」，這個等式不成立。','AI解答核對、座標法、畢氏定理','已更正',note='已依對話文字獨立重算並指出錯誤等式；原題附圖仍需補存。',diagram='square')
add(3,'Math','第 16、18 題｜證明與作圖待補','四邊形與作圖','第16題涉及 AE ⟂ DF、BF=CE 的證明；第18題要求只畫一條直線將圖形面積二等分。','原題條件不足，暫不提供答案。','原分享只列出第16題結論，未載完整條件；第18題也缺少圖形。需要原題圖後才能進行證明或作圖。','只有結論而沒有已知條件，不能反推出一份可靠證明。','證明、作圖','待補原題',note='兩題暫合為待補資料提醒，取得原圖後拆分。')
add(4,'Math','第 6 題｜四邊長 1、2、3、4 的梯形','梯形與面積','已知非退化梯形四邊長為 1、2、3、4，求面積。','10√2 / 3','檢查兩底與兩腰的組合，非退化配置為兩底 1、4，兩腰 2、3。平移短腰得到邊長 2、3、3 的三角形。設底邊方向投影為 x、3−x，則 x²+h²=4、(3−x)²+h²=9，得 x=2/3、h=4√2/3。面積=(1+4)h/2=10√2/3。','先確認哪些邊互相平行；不能只憑長短猜底邊。','梯形、輔助線、畢氏定理','整理',diagram='trapezoid')
add(4,'Math','第 7 題｜梯形高與點到直線距離','梯形與面積','依對話：直角梯形 AB ∥ CD、AB=4、CD=3、BC=7，O 為 AD 中點。求 O 到 BC 的距離。','2√3','先由 BC²=(4−3)²+AD² 得 AD=4√3。用座標或拆分面積可得 △BCO 面積=7√3。再以 BC=7 為底，距離 d=2×7√3/7=2√3。','梯形的高 AD 與 O 到斜邊 BC 的距離是不同線段。','點到直線距離、面積','待核對',note='計算已重算；缺原圖，保留對話描述的位置條件。')
add(5,'Math','第 15 題｜梯形條件衝突，先停下來','梯形與面積','原 AI 將題目辨讀為：AB ∥ CD，AB=8、AD=3、CD=6，且 ∠B+∠C=90°，求面積。','暫不採用原 AI 的 42√5/5。請先核對原圖。','若 A、B、C、D 為梯形依序頂點，AB ∥ CD 代表同側內角 ∠B+∠C=180°，與 90° 矛盾。原解答又把 CD 同時當作底邊與腰使用，因此後續三角比計算沒有可靠依據。','先檢查題目是否自洽，再計算。AI 辨圖錯誤可能把標記或角名抄錯。','AI解答核對、平行線、條件辨識','待補原題',note='來源有兩張附圖，但下載需授權；需補第15題清楚原圖。')
add(6,'Math','第 1 題｜垂直且等長，就一定是正方形？','四邊形判別','下列何者錯誤？「對角線互相垂直且等長的四邊形一定是正方形」。','此敘述錯誤，原題選 B。','反例：A=(0,3)、B=(2,0)、C=(0,−1)、D=(−2,0)。AC=BD=4 且互相垂直，但 AC 被交點分成 3 與 1，未互相平分，因此不是正方形。\n若另加對角線互相平分，才能配合等長、垂直判定正方形。','正向命題成立，不代表反向命題一定成立。','反例、正方形、充分條件','整理',diagram='diagonals')
add(7,'English','Anything：喝什麼都可以','代名詞與語意',"Noah: I’ve had too many cookies. My throat is so dry. Quinn: What would you like to drink then? Noah: _____ you can get. Just get it now!\n(A) Something (B) Nothing (C) Everything (D) Anything",'(D) Anything','Anything you can get 表示「你拿得到的任何東西都可以」，符合口渴且急迫、沒有特別偏好的語境。Something you can get 在其他語境可以合乎文法；這題重點是選出最符合語境的一項。','不要把「本題不最佳」記成「這種文法絕對不成立」。','不定代名詞、上下文')
add(7,'English','No one else：其他人要放在哪裡？','代名詞與語意',"Gary is the best teacher I’ve ever known. No one _____ teaches so well.\n(A) all (B) another (C) else (D) other",'(C) else','else 放在 no one、someone、anyone 等不定代名詞之後。若用 other，需改寫為 No other teacher teaches so well.','記住 no one else 與 no other + 名詞，是兩種不同結構。','else、other、不定代名詞')
add(7,'English','Traffic lights：跨句的因果線索','字彙與閱讀','Most of the _____ along this road were knocked down during the typhoon. So make sure no cars are coming when you cross the street.\n(A) bus stops (B) motorcycles (C) public phones (D) traffic lights','(D) traffic lights','後句提醒過馬路時確認來車，前句應是交通號誌損壞，影響路口通行。把兩句讀成一個因果關係，再選出 traffic lights。','只看「颱風把東西吹倒」會誤選 motorcycles；要讀完後句。','生活字彙、因果推論')
chinese=[
('初出茅廬：用字義辨字形','字音字形','初出茅「ㄌㄨˊ」應寫哪個字？','廬','「廬」指簡陋房屋，如草廬；「盧」多用作姓氏等，不能寫成初出茅盧。','不能只靠同音字直覺作答。'),
('瑣碎：玉字旁與金字旁','字音字形','「絮絮叨叨」解釋中的「ㄙㄨㄛˇ碎」應如何寫？','瑣碎','「瑣」有細小、零碎之義；「鎖」是鎖具。用字義辨別部首。','寫得快時仍要檢查部首。'),
('穠纖合度：成語的對應關係','字音字形','「穠纖合度」中的「纖」可以換成身軀的「軀」嗎？','不能；應為「纖」。','「穠」與「纖」分別對應豐腴與纖細，合度意為恰到好處。','不要把成語拆成日常口語重新拼湊。'),
('手無縛雞之力：形近字辨析','字音字形','「手無縳雞之力」中的錯字如何改正？','縳 → 縛','「縛」表示綑綁；「手無縛雞之力」比喻力氣弱小。','改錯時逐字核對，不要只找一個不熟的字。'),
('汗流浹背：形近字與選項','字音字形','「汗流夾背」是否正確？','應寫「汗流浹背」。','「浹」有浸透之意，用水部表示汗水濕透背部。','選字形正確項時，要逐一檢查常見成語。'),
('秋天的況味：由中年步入晚年','秋天的況味','「想著人生由［　］步入晚年時是否也該有生命的壯麗演出？」應填什麼？','中年','後文已寫「步入晚年」，前文應描述進入晚年之前的階段；秋天的成熟意象也呼應中年。','填入後把整句重讀一次，檢查是否變成「由晚年步入晚年」。'),
('天狗食日：活動表格閱讀','閱讀與圖表','活動包含日食講座、直播與戶外觀測，從表格可讀出什麼？','整場活動包含室內與戶外兩部分（來源選 A）。','對照時間欄與活動欄。來源所述時間為 14:00–17:30，全部在下午；不可推成中午結束。','表格的時間、地點、活動性質要分別核對。'),
('湖濱散記：第三張椅子的象徵','閱讀與推論','梭羅的第三張椅子是為了社交，大量訪客只能坐第三張椅子，意涵為何？','這些訪客往往不是摯友（來源選 C）。','第一張椅子象徵獨處，第二張代表友誼，第三張代表社交。由象徵層次推論訪客關係。','不要把「社交訪客」推成「不請自來」，那是原文未提供的資訊。'),
('陋室銘：唐人的書房會有宋人的書嗎？','陋室銘','劉禹錫的書房中，不可能出現《說文解字》還是《歐陽文忠公全集》？','《歐陽文忠公全集》','劉禹錫為唐代，歐陽修為宋代，宋在唐之後。東漢許慎的《說文解字》則早於唐代。','把作者與朝代連起來，排除未來才出現的作品。'),
('陋室銘：「何陋之有」的之','陋室銘','「何陋之有」與「學而時習之」中的「之」，用法是否相同？','不同：前者為助詞，後者為代詞。','「何陋之有」可理解為「有何陋」，之為賓語前置的結構標誌；「學而時習之」的之指所學的內容。','不能看到同一字就認定詞性相同。'),
('深藍的憂鬱：「彷彿」不等於已發生','深藍的憂鬱','題目問何者錯誤：「彷彿看到下一次比賽後的勝利歡呼」能解讀成棋王已經大獲全勝嗎？','不能；「已經大獲全勝」是錯誤敘述。','「彷彿」與「下一次」表達想像與未來，不能當成已發生的勝利。','圈出「何者錯誤」，避免反向選錯。'),
('鳥：譬喻與誇飾的判讀','鳥','「我想牠的苦悶，大概是僅次於粘在膠紙上的蒼蠅……」應如何判斷修辭？','依來源選項：誇飾、譬喻（B）。','把籠中鳥的苦悶與黏在膠紙上的蒼蠅比較，形成譬喻，並強化苦悶的感受。仍應結合原段落與選項判讀。','有無設問要依是否提出問題判斷；不能只憑情緒猜修辭。'),
('孟、仲、季：初秋是哪一個？','秋天的況味','「我所愛的不是晚秋，是初秋」的初秋又稱什麼？','孟秋','每季依序為孟（初）、仲（中）、季（末）。孟秋為農曆七月、仲秋八月、季秋九月。','不要把初秋與中秋的仲秋混為一談。')]
for title,chapter,q,a,e,t in chinese:add(8,'Chinese',title,chapter,q,a,e,t,'審題、'+chapter,note='課名依來源整理；原卷編排與使用者指定南一版尚未完成對照，冊次歸綜合。')
add(8,'Chinese','「蹔」的讀音：先核對原字','字音字形','來源報告記錄了「蹔」的注音訂正，應如何複習？','先核對原卷字形，再查標準字典。','來源的字形與讀音說明需要再次確認，現階段不直接收作定論，避免把辨識錯字背下來。','生僻字若照片不清楚，先確認是否為同一個字。','字音、原字核對','待核對',note='原圖為低解析度預覽，無法可靠確認這個字，故保留為待核對。')
science=[
('有機物判定：有碳不一定是有機物','有機化合物','葡萄糖與碳酸氫鈉都含碳、氫、氧，是否都是有機物？','不是；國中分類中葡萄糖屬有機物，碳酸氫鈉屬無機物。','國中常見無機碳化合物包含 CO、CO₂、碳酸鹽與碳酸氫鹽。\n若燃燒產物有 CO₂ 和水，可以推知原物質含碳、氫；若反應有外界氧氣參與，不能單憑產物證明原物質含氧。來源「必含 C、H、O」需依實驗條件確認。','檢出產物中的氧，不代表氧一定全來自原物質。','元素判定、有機物'),
('有機物種類多：碳原子的連結方式','有機化合物','為何有機化合物種類繁多？','碳原子可互相連結成鏈、成環，並有不同結構。','多樣的碳骨架與不同原子的連結方式，帶來大量不同化合物；不能只用「碳活性很大」來解釋。','分辨結構多樣性與化學活性。','碳骨架、結構'),
('酯化反應：酸與醇生成什麼？','有機化合物','有機酸與醇的酯化反應，除酯以外還會生成什麼？','水','在適當條件下，有機酸與醇可反應生成酯和水。複習時同時辨認羧基與醇類的羥基。','別把反應產物與原物質的分類混在一起。','酯化、反應式'),
('靜摩擦力：方向要抵抗運動趨勢','6-2 摩擦力','物體在水平面靜止，左側拉力 2 kgw、右側拉力 5 kgw，摩擦力為何？','向左，3 kgw','不計摩擦力時，合力為向右 5−2=3 kgw。物體靜止表示總合力為零，因此摩擦力為向左 3 kgw。','摩擦力抵抗相對運動趨勢，不是跟著較大的拉力。','受力平衡、摩擦力'),
('接觸面積變大，最大摩擦力也變大？','6-2 摩擦力','同樣木塊從疊放改為並排，總重與接觸材料不變，原先需 20 gw 克服最大靜摩擦力，現在呢？','在國中理想乾摩擦模型下，仍為 20 gw。','最大靜摩擦力近似為 μsN。材料與總正向力不變，最大靜摩擦力不因表觀接觸面積改變。','此結論有模型條件，不能延伸成所有材料、所有情況都與面積無關。','乾摩擦模型、正向力'),
('壓在牆上的木塊：推力與摩擦力不同方向','6-2 摩擦力','木塊被水平推向垂直牆面而保持靜止，向上的摩擦力如何決定？','若垂直方向只有重力與摩擦力，摩擦力等於物重。','水平推力改變正向力 N，進而改變最大靜摩擦力 μsN；實際靜摩擦力只需補足垂直平衡。當 μsN 小於物重，木塊無法保持靜止。','原分享的數值敘述混合了不同題況，沒有 μs 或臨界條件時不能算出最小推力。','受力圖、最大靜摩擦力'),
('彈簧混聯：先找誰在承重','力與彈簧','兩根上方彈簧共同支撐下方一根彈簧與負載，在忽略彈簧重量時，拉力關係為何？','F₁+F₂=F₃；若上方兩彈簧相同且對稱，F₁=F₂=F₃/2。','把連接處隔離，靜止代表上下力平衡。並聯分擔負載；只有相同勁度、相同伸長量的彈簧才等分拉力。','並聯不一定各分一半，要先確認彈簧與幾何條件。','彈簧、並聯'),
('彈簧圖表：總長不等於伸長量','力與彈簧','彈簧無負載時長 12 cm，掛重後長 17 cm，虎克定律中的伸長量為何？','5 cm','伸長量 Δx=17−12=5 cm。彈性限度內 F=kΔx，應代入伸長量，而非總長。','先從圖表讀出零負載時的原長。','虎克定律、圖表'),
('磅秤與彈簧：向上的力有兩個','力與彈簧','物體靜置磅秤上，另受向上彈簧拉力 500 gw；若物重 800 gw，磅秤讀數為何？','300 gw','受力平衡：彈簧拉力 T + 磅秤支撐力 N = 物重 W。所以 N=800−500=300 gw。若 T 達到 W，物體可能離開秤面，不能出現負的支撐力。','原分享前段有方向筆誤，應以 T+N=W 為準。','正向力、受力平衡'),
('帕斯卡原理：半徑比要先平方','6-3 壓力','液壓機大、小活塞半徑比為 3:1，小活塞施力 30 kgw，大活塞理想支撐力為何？','270 kgw','同一高度、忽略損失與活塞自重時，F小/A小=F大/A大。面積比為 3²:1²=9:1，因此 F大=30×9=270 kgw。','題目給半徑比或直徑比，要先轉成面積比。','帕斯卡原理、平方比'),
('托里切利實驗：把管頂氣壓加回來','6-3 壓力','外界 76 cmHg，管內水銀柱比槽面高 38 cm，求管內液面下 10 cm 處總壓。','48 cmHg，約 652.8 gw/cm²','管頂氣壓=76−38=38 cmHg。從管內頂部液面向下 10 cm，壓力再增加 10 cmHg，所以總壓 48 cmHg。若題目指槽面下10 cm，則應為86 cmHg，要先辨明參考液面。','深度相對哪個液面，是計算前最重要的條件。','大氣壓、液體壓力'),
('冰塊融化：純水與鹽水的差別','6-4 浮力','漂浮的純水冰塊分別放在純水與鹽水中，融化後液面如何變化？','理想條件下：純水液面不變，鹽水液面上升。','冰塊漂浮時，排開液體的重量等於冰塊重量。同質量下，鹽水密度較大、排開體積較小；融化形成純水的體積較大，因此鹽水杯液面上升。忽略溫度、混合體積等效應。','比較的是融化後水的體積與原來排開液體的體積。','浮力、密度'),
('鐵球與鋁球：浮力的反作用力','6-4 浮力','同質量鐵球與鋁球由外部支架懸吊，完全浸入兩杯等量水且不碰杯底，哪杯增加的秤重較多？','鋁球那杯','同質量下，鋁密度較小、體積較大，排水體積較大，受到浮力較大，對水施加的向下反作用力也較大。若球落在杯底，或懸吊架也放在同一秤上，則整體受力需重新分析。','先確認支架放在哪裡、球是否接觸杯底。','反作用力、系統邊界'),
('同體積物體：比較排水體積','6-4 浮力','同一液體中，等體積物體有的漂浮、有的完全浸沒，如何比較浮力？','在液體可接觸各表面的通常條件下，排水體積越大，浮力越大。','B=ρ液gV排。完全浸沒的等體積物體，排水體積相等，浮力相等；漂浮且露出水面的物體，排水體積較小。接觸容器底部且液體無法進入底面時，要另作受力分析。','不是「沉得越深，浮力一定越大」。','排水體積、阿基米德原理'),
('先判浮沉，再算浮力','6-4 浮力','甲 40g/50cm³、乙 30g/60cm³、丙 60g/30cm³，放入水中，求靜止時浮力（一般浸潤條件）。','甲 40 gw，乙 30 gw，丙 30 gw；甲 > 乙 = 丙。','先算密度：甲0.8、乙0.5、丙2 g/cm³。甲乙漂浮，浮力等於物重；丙完全浸沒，排水30cm³，受浮力30gw。','g 是質量，gw 是重量單位；以 N 計算時需乘重力加速度。','密度、浮沉判斷')]
for title,chapter,q,a,e,t,tags in science:add(9,'Physics-Chemistry',title,chapter,q,a,e,t,tags,volume='第四冊',note='來源自然試卷標示（四）；部分題目依對話條件改寫為觀念複習，非逐字完整原題。')
# User explicitly retains English composition as English / comprehensive.
for q in records:
 if q['sourceId']=='src-2':
  q['chapter']='綜合'
  q['tags'].append('寫作補充')
  q['verificationNote']='依使用者指定保留為英文綜合的寫作補充練習。'
extra_questions=ROOT/'docs/additional-questions.json'
if extra_questions.exists():records.extend(json.loads(extra_questions.read_text()))
# Keep stable question IDs while excluding entries removed by the user.
excluded_path = ROOT / 'docs/excluded-questions.json'
excluded_ids = set(json.loads(excluded_path.read_text())) if excluded_path.exists() else set()
for question_id in excluded_ids:
 if re.fullmatch(r'q-\d+', question_id):
  (DEST / (question_id + '.html')).unlink(missing_ok=True)
aliases_path = ROOT / 'docs/question-aliases.json'
question_aliases = json.loads(aliases_path.read_text()) if aliases_path.exists() else {}
excluded_ids.update(question_aliases)
records = [q for q in records if q['id'] not in excluded_ids]
if any(target not in {q['id'] for q in records} for target in question_aliases.values()):
 raise ValueError('Question aliases must point to an existing canonical question')
(DEST/'question-alias-data.js').write_text('// Generated by curate.py from docs/question-aliases.json.\nexport const QUESTION_ALIASES = '+json.dumps(question_aliases,ensure_ascii=False,separators=(',',':'))+';\n')
# Full-question overrides are transcribed and checked against the exact source page.
# Only explicitly completed questions are changed; other notes await user review.
for q in records:
 override = ROOT / 'docs/complete-questions' / (q['id'] + '.json')
 if override.exists():
  q.update(json.loads(override.read_text()))
  q['contentStatus'] = q.get('contentStatus', '完整原題')
 else:
  q['contentStatus'] = q.get('contentStatus', '待更新')
 if q['sourceId'] in ['src-7','src-8','src-9']:
  q['date']=next(s['date'] for s in sources if s['id']==q['sourceId'])
  q['dateLabel']='對話建立日期（Created）'
apply_review_requests(records, ROOT)
apply_pending_sources(sources, ROOT)
# Curated diagrams are accessible, code-native SVGs, independent of missing source photos.
revision='2026-10-27.'+hashlib.sha256(json.dumps([sources, records],ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:12]
payload=dict(schemaVersion=1,revision=revision,subjects=[dict(id=i,name=n,publisher=p,icon=ic) for i,n,p,ic in subjects],sources=sources,questions=records)
from optimized_assets import optimize_payload, prune_unreferenced
payload=optimize_payload(payload)
payload['revision']='2026-10-27.'+hashlib.sha256(json.dumps([payload['sources'],payload['questions']],ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:12]
(DEST/'data.json.tmp').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(DEST/'data.json.tmp').replace(DEST/'data.json')
print(f'{len(sources)} sources, {len(records)} questions, {sum(len(s["images"]) for s in sources)} original images')

subprocess.run([sys.executable, str(BASE / 'scripts/build_review_page.py')], check=True)

prune_unreferenced(DEST, payload)
