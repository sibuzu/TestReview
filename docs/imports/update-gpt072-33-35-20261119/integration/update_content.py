"""Apply the supplied common passage/photos to the two existing originals only."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,locked,now,begin,update_display
from monitor.comic_execution import assert_work_allowed
h=load(D/'root/content-handoff.json');assert h['sameConversationConfirmed'] and h['originalsActuallyViewed'] and h['dateUnchanged']=='2026-11-17'
ids=['q-1153','q-1154'];passage=(ROOT/h['passagePath']).read_text().strip();assert '8月23日' in passage and '434萬票' in passage
for row in h['crops']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'] and row['actuallyViewed']
def publish(path):
 raw=(ROOT/path).read_bytes();p=Path(path);target=f'assets/originals/gpt072-supplement-{p.stem}-{hashlib.sha256(raw).hexdigest()[:12]}{p.suffix}';dest=ROOT/'site/dist'/target;dest.write_bytes(raw);return target
reading=publish('docs/imports/update-gpt072-33-35-20261119/root/shared-reading.png')
explanations={
'q-1153': '答案A。共同閱讀已補齊，情境為2025年（民國114年）8月23日的全國性公民投票第21案與中央民意代表罷免案同日投票。依該次官方投票公報及法定資格，符合公職罷免其他資格的受監護宣告者，可以領取罷免票；但全國性公投的投票權仍要求未受監護宣告，因此A能解釋「有罷免票、沒有公投票」。這不表示受監護宣告者不必符合其他年齡、居住等資格。\n\nB：公投年齡是年滿18歲，公職選罷投票年齡是年滿20歲。18歲至未滿20歲者，是可能符合公投年齡卻尚未達罷免年齡，方向與題述相反。\n\nC：褫奪公權與監護宣告是不同制度，不能直接把褫奪公權當作此處公投法的監護資格限制。\n\nD：公職罷免須看原選舉區繼續居住4個月的條件；全國性公投看在中華民國繼續居住6個月。從高雄搬到新北，不會把原先在國內的居住期間歸零；而「遷入新北未滿6個月」也不等於「未滿4個月」。所以不能僅憑D推得能領罷免票卻不能領全國性公投票。\n\n查核：中央選舉委員會2025年8月23日[新北市罷免投票公報](https://web.cec.gov.tw/api/file/a6ae5405-f1be-40a2-b65e-f810d0a2cc04.pdf)、[公職人員選舉罷免法第14、15條](https://law.cec.gov.tw/LawContent.aspx?id=GL000292)及[公民投票法第7、8條](https://law.cec.gov.tw/LawContent.aspx?id=GL000290)。',
'q-1154': '答案A。共同閱讀指出114年8月23日同時舉行第11屆中央民意代表罷免投票，並提到7項罷免案均未通過。中央民意代表指立法委員，而區域立委可由符合資格的原選舉區選民依法提案罷免，符合「中央」與「可被罷免」兩個條件。\n\nA：區域立委是中央民意代表，適用依法罷免的規定。\nB：全國不分區及僑居國外國民立法委員不適用公職人員罷免規定。\nC：直轄市市議員是地方民意代表，不符合題目的中央一詞。\nD：經由政黨票產生的名單立委，與B所述屬同一類，不適用罷免。不能因為所有立委都是中央民代，就認為每一類立委都可用罷免方式解職。\n\n查核：[公職人員選舉罷免法第2、3、75條](https://law.cec.gov.tw/LawContent.aspx?id=GL000292)。'}
analyses={
'q-1153':['其他資格符合時，監護宣告不排除本次公職罷免投票資格；公投法仍要求未受監護宣告。','年齡方向相反：公投年滿18歲，公職罷免年滿20歲。','褫奪公權不同於監護宣告，不能直接套用公投法的監護資格限制。','原選區4個月與國內6個月是不同條件；跨市搬家不會使國內居住期間歸零，未滿6個月也不等於未滿4個月。'],
'q-1154':['區域立委是中央民意代表，可由原選舉區選民依法提案罷免。','全國不分區及僑居國外國民立委不適用罷免。','直轄市市議員屬地方民意代表，不符合中央。','政黨票選出的名單立委與B同類，不適用罷免。']}
for qid in ids:
 assert_work_allowed(ROOT,qid);q=load(ROOT/f'docs/complete-questions/{qid}.json');before=load(D/f'before/docs/complete-questions/{qid}.json')
 assert q['question']==before['question'] and q['sourceId']=='src-more-072' and q['date']=='2026-11-17'
 q.update(passage=passage,contentStatus='完整原題',verification='原卷逐題核對',correctOption='A',answer='(A) '+q['optionAnalysis'][0]['text'],explanation=explanations[qid],verificationNote='已實開使用者補充的完整共同閱讀與本題原卷，核對全文及四選項；照片只作可查核裁切／旋轉，不採AI重繪。題目日期沿用首次提問2026-11-17，非補圖或實際考試日期；共同閱讀情境為2025-08-23。冊次章節無證據，維持綜合。',images=[reading,publish(f'docs/imports/update-gpt072-33-35-20261119/root/{qid}-original.png')])
 for field in ('reviewQuestions','reviewExcerpt','reviewLabel','reviewPreviousId','reviewNextId'):q.pop(field,None)
 for i,option in enumerate(q['optionAnalysis']):option.update(wordClass='應選' if option['label']=='A' else '不選',explanation=analyses[qid][i])
 save(ROOT/f'docs/complete-questions/{qid}.json',q)
 spec=load(ROOT/f'docs/comics/{qid}.json');spec.update(title='同日投票的兩種資格差異' if qid=='q-1153' else '中央民代與依法罷免的兩項條件',answerCheckedAgainst=q['explanation'],supplementarySourceUrl=h['updatedShareUrl'],originalMaterials=[str((D/'root/shared-reading.png').relative_to(ROOT)),str((D/f'root/{qid}-original.png').relative_to(ROOT))],visualChecked=False)
 if qid=='q-1153':
  spec['panels'][0].update(heading='① 確認同日投票的兩種票',text='共同閱讀指出114年8月23日同時舉行罷免與全國性公投。本題能領罷免票、不能領公投票，須比較資格差異。')
  spec['panels'][2]['text']='此次公職罷免不會僅因監護宣告排除投票權，公投仍要求未受監護宣告；原選區4個月與國內6個月的居住條件要分開。'
  spec['fourth'].update(answer='答案 A：安安是受監護宣告者',points=['監護宣告是兩種投票資格的差異；其他資格仍須符合。','公投18歲、公職罷免20歲，B的方向相反。','跨市搬家不會使國內居住期間歸零；D不能直接解釋。'],alt='第4張既有圖解補文更新：監護宣告與兩種投票資格的差異')
 else:
  spec['fourth'].update(answer='答案 A：區域立委',points=['共同閱讀的中央民意代表為立法委員。','區域立委可依法罷免，名單立委不適用。','市議員屬地方，不能只看是否由人民選出。'],alt='第4張既有圖解補文更新：中央與可依法罷免的條件')
 spec['supplementReview']=dict(reviewerAgent='/root/comic_lane_1',sourceHandoff='docs/imports/update-gpt072-33-35-20261119/root/content-handoff.json',sharedReadingAndCropsActuallyViewed=True,existingEightDiagramsRetained=True,checkedAt=now())
 save(ROOT/f'docs/comics/{qid}.json',spec)
 image=ROOT/f'docs/comics/art/{qid}-panel-4.svg';art=image.read_text();art=art.replace('原卷A；共同閱讀待補','答案 A：監護資格的差異').replace('原卷A；共同閱讀仍待補','答案 A：區域立委');image.write_text(art)
with locked(ROOT):
 requests=load(ROOT/'docs/review-requests.json')
 for qid in ids:requests.pop(qid,None)
 save(ROOT/'docs/review-requests.json',requests)
 sources=load(ROOT/'docs/additional-sources.json');source=next(s for s in sources if s['id']=='src-more-072');new_originals=[publish(i['path']) for i in load(D/'acquisition.json')['downloadedImages']];source['images']=list(dict.fromkeys(source['images']+new_originals));supplements=source.setdefault('supplements',[])
 if not any(s.get('url')==h['updatedShareUrl'] for s in supplements):supplements.append(dict(url=h['updatedShareUrl'],questionIds=ids,acquisition=str((D/'acquisition.json').relative_to(ROOT)),note='同一對話的新分享；使用者補齊第33～35題共同閱讀，僅更新既有錯題33與35。'));source['note']='第72來源原24原問已整理；兩題共同閱讀已由同一對話新分享補齊，q-1153/q-1154維持原ID、首次日期與答案A；未指定正常作答34不新增。其餘既有個別待確認不變。';save(ROOT/'docs/additional-sources.json',sources)
 gp=load(ROOT/'docs/imports/more-gpt-progress.json');row=next(r for r in gp['sources'] if r.get('sourceId')=='src-more-072');row.setdefault('downloadedImages',load(ROOT/'docs/imports/new-gpt-20261117-72/acquisition.json')['downloadedImages']);existing={i['sha256'] for i in row['downloadedImages']}
 for im in load(D/'acquisition.json')['downloadedImages']:
  if im['sha256'] not in existing:row['downloadedImages'].append(dict(im,index=len(row['downloadedImages'])+1,supplementIndex=im['index'],supplementUrl=h['updatedShareUrl']))
 row.update(archiveImages=26,archiveMessages=299,supplementalAcquisition=str((D/'acquisition.json').relative_to(ROOT)),supplementalShareUrl=h['updatedShareUrl']);gp['updatedAt']=now();save(ROOT/'docs/imports/more-gpt-progress.json',gp)
 pipeline=load(ROOT/'docs/comics/pipeline.json')
 for qid in ids:
  job=next(j for j in reversed(pipeline['jobs']) if j['id']==qid);assert job['state']=='blocked' and 'integrationEventId' not in job
  job.update(state='ready',decision='complete',reason='使用者已補完整共同閱讀及本題原卷；維持原題/ID/日期與既有四圖，待本次正式驗版完成後解除缺文狀態。',materialUpdateScope=str((D/'execution-scope.json').relative_to(ROOT)),materialSupplementReceivedAt=now(),artQAOnly=False)
 save(ROOT/'docs/comics/pipeline.json',pipeline);update_display(ROOT,pipeline)
for qid in ids:begin(ROOT,qid)
print(json.dumps(dict(updatedQuestionIds=ids,sourceId='src-more-072',question34Added=False,existingEightIllustrationsRetained=True),ensure_ascii=False))
