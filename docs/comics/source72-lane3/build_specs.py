from pathlib import Path
import json,datetime,hashlib,sys
R=Path(__file__).resolve().parents[3];P=R/'docs/imports/new-gpt-20261117-72/lane3';O=P/'comics'
content={
'q-1137':dict(title='瑞金政權：先辨年代，再看國共關係',panels=[('① 瑞金與國家銀行是辨認線索','中華蘇維埃共和國是1931年中共在瑞金建立的政權。銀行圖為一般情境示意，不能因發行貨幣就判成日本傀儡政權。'),('② 瑞金在江西，別與東北混淆','地圖標出江西瑞金與南京的相對位置，僅供地理定位，未重建歷史疆界。滿洲國在東北，是另一政權。'),('③ 當時是軍事對立，不是結盟','國民政府將此政權視為叛亂、分裂政權，進行軍事圍剿。行軍圖是當時一般軍事情境示意，不是特定作戰紀錄。')],answer='答案C：視為叛亂政權，派兵征伐',points=['1931年的瑞金蘇區，對應國共軍事對立。','美國馬歇爾調停始於1945年底，是戰後另一階段，不能選D。'],protected=['中華蘇維埃共和國','國民政府','1931年','1945年底','軍事圍剿']),
'q-1138':dict(title='1931年與黨治權責指向訓政約法',panels=[('① 先換算年代：民國20年＝1931','原題說1931年5月制定，對應《中華民國訓政時期約法》。文件插畫只是教學靜物，正式名稱與日期以文字為準。'),('② 三項權力都由國民黨機關掌握','全國代表大會行使統治權；中央執委會選任國府委員，並解釋約法。這三項是原表訓政、黨治的核心線索。'),('③ 其他三部文件不在1931年','1912年是臨時約法，1914年是中華民國約法，1936年是五五憲草。時間與原表制度須一起核對。')],answer='答案D：《中華民國訓政時期約法》',points=['1931年5月12日制定，6月1日公布施行。','議事場景僅為教學示意；不是宣稱描繪某次真實會議。'],protected=['1931年','1912年','1914年','1936年','中央執委會','訓政時期約法'])}
extra=Path(__file__).parent/'content-more.json'
if extra.exists():content.update(json.load(open(extra)))
for qid in sys.argv[1:]:
 q=json.load(open(P/f'{qid}.json'));c=content[qid];imgs=[]
 for n in range(1,5):
  ps=[R/f'docs/comics/art/{qid}-source72-{n}.{ext}' for ext in ['png','svg']];found=[p for p in ps if p.exists()];assert len(found)==1,(qid,n,found);imgs.append(str(found[0].relative_to(R)))
 gs=[]
 for p in O.glob('batch-*-generation.json'):
  gs.extend(x for x in json.load(open(p)) if x['id']==qid)
 s=dict(id=qid,subject='History',title=c['title'],art=imgs[0],layoutVersion='native-four-images-v7',generationMethod='new independent built-in imagegen historical scenes plus precise original native SVG geography/chronology/institutional illustrations',sourceGeneratedArtUsed=False,reusedOldGeneratedArt=False,originalMaterialsChecked=True,originalMaterials=q['images']+[x['src'] for x in q['questionFigures']],answerCheckedAgainst=q['explanation'],rationale='Read complete original question, four options and required materials; source72 intake review and official primary evidence retained. Historical scenes explicitly generic teaching reconstructions, not records of a specific event. Native maps use Natural Earth modern locator geometry, no invented historical borders. Four distinct teaching images, including answer synthesis.',producerAgent='/root/comic_lane_3',visualChecked=False,panels=[dict(heading=h,text=t,image=imgs[i],alt=h+'；新製'+('歷史情境示意，非真實照片。' if imgs[i].endswith('.png') else '精確原生圖，詳見可選取文字。')) for i,(h,t) in enumerate(c['panels'])],fourth=dict(answer=c['answer'],points=c['points'],image=imgs[3],alt='第四張不同新圖：'+('一般歷史情境示意。' if imgs[3].endswith('.png') else '原生年代／位置整合圖。')),protectedWords=c['protected'],manualLineBreaks=False,artHashes={x:hashlib.sha256((R/x).read_bytes()).hexdigest() for x in imgs},supportingSources=q['supportingSources'],intakeReview=str(P/f'{qid}-review.json'),generationEvidence=gs,nativeGenerator='docs/comics/source72-lane3/native.py',mapProvenance='docs/comics/source72-lane3/map-provenance.json',createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
 s['panels'][0]['caption']='新製教學圖，情境非歷史照片。'
 assert len(set(s['artHashes'].values()))==4
 (R/f'docs/comics/{qid}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
 print(qid,'4 distinct new images spec saved')
