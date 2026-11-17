from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).parent;D=json.load(open('site/dist/data.json'))['questions'];C={int(x['candidateId'].rsplit('-',1)[1]):x for x in json.load(open(P/'crop-records.json'))};now=datetime.datetime.now(datetime.timezone.utc).isoformat()
oldurl='https://chatgpt.com/share/6ae2305b-4b44-83ee-997b-6938a4f8d7e4';dups={9:'q-795',11:'q-798',15:'q-804'}
common={'source':'原始24 User附件，已排除來源AI圖與同頁非指定題','indexCandidates':'docs/imports/new-gpt-20261117-72/lane3/duplicate-candidates.json','phraseSearch':'docs/imports/new-gpt-20261117-72/lane3/duplicate-phrase-search.json','method':'META candidates + distinctive full-bank phrase search + full question/options/materials + original-image visual comparison; URL/hash/title alone not identity'}
S={
5:[{'title':'檔案管理局：西北剿共部署（含1931瑞金與軍事圍剿）','url':'https://art.archives.gov.tw/tw/art/1940.html','supports':'瑞金蘇維埃政權與國民政府軍事圍剿關係；不沿用網頁對人物政治評價。'}],
6:[{'title':'國寶指定公告：訓政時期約法原件','url':'https://gazette.nat.gov.tw/EG_FileManager/eguploadpub/eg022077/ch05/type3/gov46/num17/OEg.pdf','supports':'1931-05-12制定，1931-06-01公布施行。'}],
7:[{'title':'美國國務院：The Mukden Incident of 1931','url':'https://history.state.gov/milestones/1921-1936/mukden-incident','supports':'1931-09-18瀋陽鐵路事件及日本占領滿洲的時間地點。'},{'title':'FRUS：1931-09-19當時電報','url':'https://history.state.gov/historicaldocuments/frus1931-41v01/d1','supports':'9月18夜瀋陽附近攻擊的 contemporaneous 史料；不以任一方敘事取代全部責任判斷。'}],
8:[{'title':'國史館館刊46：國民政府遷都重慶史料研究','url':'https://www.drnh.gov.tw/var/file/3/1003/img/10/163456254.pdf','supports':'1937-11-20公布遷都重慶、持久抗戰背景。'}],
9:[{'title':'全國法規資料庫：1943中英新約換文','url':'https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=Y0030029','supports':'1943-01-11簽換、05-20生效；原段三項放棄條約特權及官方租界用字。'}],
10:[{'title':'中華郵政：陸海軍大元帥就任紀念郵票史料','url':'https://www.post.gov.tw/post/internet/W_stamphouse/index_en.jsp?ID=2807&file_name=B007&keyword=%25&stamp_cat_standard=%25&stamp_subcat_name=%25&stamp_year=%25&type=2808','supports':'1928年6月北伐軍逼近北京、張作霖撤返途中皇姑屯遭炸的同一時期背景。'}],
11:[{'title':'檔案管理局：金圓券沿革','url':'https://aa.archives.gov.tw/ELK/NAAMaterialDetail?DID=2155','supports':'1948年8月幣制改革及通膨危機未解決。'},{'title':'檔案管理局：中央銀行史料','url':'https://www.archives.gov.tw/wSite/public/Attachment/0/f1717662462440.pdf','supports':'37年8月國共戰爭緊張引發通膨及發行金圓券。'}],
12:[{'title':'Truman Library：Marshall Mission to China 1945-1947（檔案選編）','url':'https://www.trumanlibrary.gov/library/online-collections/marshall-china','supports':'調停階段與原始外交檔案。'},{'title':'FRUS 1946v10：調停、初步協議與停戰失敗原始文件集','url':'https://history.state.gov/historicaldocuments/frus1946v10/comp1','supports':'曾有協商與停戰但後續失敗，不把A誤教成從未有任何協議。'}],
13:[{'title':'國史館臺灣文獻館：滿洲國存續年代註解','url':'https://www.th.gov.tw/Epaper_Content/241/8823/','supports':'1932-03-01至1945-08-18存在的日本傀儡政權。'}],
14:[{'title':'廣州市規劃和自然資源局：東較場沿革','url':'https://ghzyj.gz.gov.cn/xwzx/gzdt/content/post_9948111.html','supports':'東較場在廣州、1926北伐誓師；本題8月預祝會日期取原卷公報，不以7月誓師會替換。'}],
15:[{'title':'全國法規資料庫：中英關稅條約','url':'https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=Y0040049','supports':'1928-12-20簽約、1929-01-10生效；精確拆開簽訂/易幟/生效。'}],
16:[{'title':'檔案管理局：西北剿共部署與西安事變','url':'https://art.archives.gov.tw/tw/art/1940.html','supports':'1936-12-12西安事變及1937改變攘外必先安內政策。'}],
17:[{'title':'國史館：1912臨時約法與1914新約法沿革','url':'https://ahdas.drnh.gov.tw/docs/zong/024.pdf','supports':'1912-03-11臨時約法與責任內閣制度年代。'},{'title':'訓政約法原件國寶指定公告','url':'https://gazette.nat.gov.tw/EG_FileManager/eguploadpub/eg022077/ch05/type3/gov46/num17/OEg.pdf','supports':'1931訓政約法。'},{'title':'總統府：憲法本文','url':'https://www.president.gov.tw/Page/94','supports':'1946-12-25制定、1947-01-01公布、1947-12-25施行。'}],
18:[{'title':'FRUS：1969-07-25關島尼克森主義說明','url':'https://history.state.gov/historicaldocuments/frus1969-76v01/d29','supports':'關島談話日期與政策內容。'},{'title':'美國陸軍：Nixon Doctrine and Vietnamization','url':'https://www.army.mil/article-amp/3867/nixon_doctrine_and_vietnamization','supports':'越戰中南越更多承擔地面軍力、美軍撤減與訓練援助。'}]
}
items=[]
for i in range(5,19):
 q=json.load(open(P/f's72-history-{i:02}.json'));qid=f'q-{1132+i}';q.update(id=qid,candidateId=qid,localCandidateId=f's72-history-{i:02}',images=[C[i]['path']],supportingSources=S[i]);q['inclusionEvidence']['cropSourceImageIndex']=C[i]['sourceImageIndex'];q['inclusionEvidence']['cropPath']=C[i]['path'];q['inclusionEvidence']['cropSHA256']=C[i]['sha256']
 if i==9:q['questionFigures']=[{'src':'site/dist/assets/questions/q-795-figure-original.png','alt':'跨來源已實比相同的三段原卷官方文件節錄（原印公共租借），非AI圖。','caption':'兩份原卷材料相同；本批原件亦見核對原圖。'}]
 dup={**common,'decision':'new','basis':'無META exact/similar候選；獨特片語與完整全庫比對未見同題。'}
 if i in dups:
  existing=next(x for x in D if x['id']==dups[i]);dup.update(decision='duplicate',existingId=dups[i],earliestDate=existing['date'],newSource=q['sourceUrl'],oldSource=oldurl)
  if i==9:dup.update(basis='題幹、四選項集合與三段條約材料相同；只有B/C調序，人工對照保留原題q795的C，不新增。',fullComparison=str(P/'q-795-option-permutation-review.json'),newToExistingOptionMapping={'A':'A','B':'C','C':'B','D':'D'},oldOriginals=['site/dist/assets/questions/q-795-original.png','site/dist/assets/questions/q-795-figure-original.png'])
  elif i==11:dup.update(basis='題幹與四選項相同；1937/1948-6/1948-8各米麵油九格值與單位均同；已實看兩原卷。',oldOriginals=['site/dist/assets/questions/q-798-source.jpg'])
  else:dup.update(basis='完整值百抽五/各國均霑引文與四選項相同，僅標點斷行；已實看兩原卷。',oldOriginals=['site/dist/assets/questions/q-804-source.jpg'])
  q['existingQuestionId']=dups[i];q['disposition']='duplicate'
  q['preserveExistingQuestionAndDate']=True
 else:q['disposition']='new'
 q['duplicateReview']=dup
 if i==13:q['materialCompletenessReview']='Original photo right edge cuts non-text figure content; all choices and core 满洲国/国境 cues readable, pending root essential-material decision; never fabricated missing edge.'
 out=P/f'{qid}.json';out.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 actual=[q['inclusionEvidence']['originalPath'],C[i]['path']]
 if i==11:actual.insert(1,'docs/source-pages/chatgpt-6afc7636-12.jpg')
 if i in dups:actual+=dup['oldOriginals']
 review={'id':qid,'candidateId':qid,'originalVisualChecked':True,'completeOriginalAndOptions':i!=13,'essentialMaterialReadable':True,'sourceGeneratedArtUsed':False,'actualViewed':actual,'inclusionEvidence':q['inclusionEvidence'],'duplicateReview':dup,'cropping':'Native rectangular crop only; red/blue handwriting retained; tiny adjoining lines may remain due oblique source, and never become extra questions. No de-red, inpainting or reconstruction.','cropSHA256':C[i]['sha256'],'scientificHistoricalReview':q['explanation'],'supportingSources':S[i],'materialNote':q.get('materialNote',''),'passed':i!=13,'checkedAt':now}
 rp=P/f'{qid}-review.json';rp.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 items.append({'candidateId':qid,'originalImageIndices':[i]+q.get('supplementaryOriginalImageIndices',[]),'disposition':q['disposition'],'existingQuestionId':q.get('existingQuestionId'),'draftPath':str(out),'draftSHA256':hashlib.sha256(out.read_bytes()).hexdigest(),'reviewPath':str(rp),'specPath':None,'status':'material_review' if i==13 else 'ready_for_intake','illustrationStatus':'not_started_pending_root_dedupe_freeze'})
(P/'manifest.json').write_text(json.dumps({'sourceId':'src-more-072','sourceUrl':'https://chatgpt.com/share/6afc7636-b8dc-83ec-a9de-c3ac330e5d27','phase':'complete-original-intake-and-deduplication-only','items':items,'summary':{'candidates':14,'duplicate':3,'new':11,'newMaterialReview':1,'readyNew':10,'illustrationsStarted':0},'checkedAt':now},ensure_ascii=False,indent=2)+'\n')
(P/'research.json').write_text(json.dumps(S,ensure_ascii=False,indent=2)+'\n')
(P/'duplicate-decisions.json').write_text(json.dumps([json.load(open(P/f'q-{1132+i}.json'))['duplicateReview']|{'candidateId':f'q-{1132+i}'} for i in range(5,19)],ensure_ascii=False,indent=2)+'\n')
(P/'reviews.json').write_text('[]\n')
print('14 reserved drafts/reviews and manifest saved; 3 duplicate + 10 ready new + 1 essential-material decision')
