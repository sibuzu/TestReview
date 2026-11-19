"""Apply previously resolved user decisions without regenerating illustrations."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent;sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import load,save,locked,now,begin,update_display
from monitor.comic_execution import assert_work_allowed
qid=sys.argv[1];D=BASE/qid;scope=load(D/'execution-scope.json');assert_work_allowed(ROOT,qid);q=load(ROOT/f'docs/complete-questions/{qid}.json');spec=load(ROOT/f'docs/comics/{qid}.json');record=load(D/'confirmation-snapshot.json')
save(D/'handled-confirmation-evidence.json',dict(requestId=record['id'],resolvedAt=record['resolvedAt'],source='monitor/confirmations.json resolved',snapshot=str((D/'confirmation-snapshot.json').relative_to(ROOT)),userComments=record.get('userComments',[])))
if qid=='q-1122':
 assert any('答案改為 D' in c.get('text','') for c in record.get('userComments',[]))
 q.update(correctOption='D',answer='(D) 巴拿馬運河（依大型礦砂船的運輸情境）',verification='使用者已確認',verificationNote='依使用者於2026-11-17T03:28:16.884450+00:00在monitor「q-1122」確認卡的明確留言，改採D。原卷紅筆B可能誤改，保留原筆跡與原標準答案需核對的證據；題幹未限定船型的條件限制仍說明，不再重問使用者D。原題、來源及首次日期不變。')
 q['explanation']='依使用者已明確指定的大型／超大型礦砂船運輸情境，答案採D（巴拿馬運河）。原卷藍筆D、紅筆B都保留；紅筆B可能是誤改，原標準答案仍需另外查核，不能把紅筆直接當作不可質疑的定論。\n\n先定位巴西在南美洲東部，出口港面向大西洋，中國位於東亞。巴西往中國的大型礦砂船可繞非洲南端好望角，進入印度洋，再往東亞；因此不能把B印度洋教成不可能經過。\n\nA大西洋：巴西面向大西洋，符合出發海域。B印度洋：好望角航路會經過，不能因此排除。C太平洋：中國位於太平洋西側，與往東亞的運輸海域相符。D巴拿馬運河：對船長、船寬或吃水超出運河限制的大型礦砂船，例如本題採用的超大型礦砂船情境，不能走巴拿馬通道，故選D。\n\n這項判斷有條件：原題沒有寫出船型、出發港或唯一航線，因此不能推成所有礦砂船都無法通過巴拿馬運河。通航能力要核對實際尺寸、吃水與運河規範，不能只用單一載重噸數把所有船型一刀切。原文「中國是該國最大的鐵礦出口國」照留，依上下文理解為中國是出口目的地，不擅改原題。\n\n查核：[Vale官方物流資料](https://www.vale.com/en/logistics)與[IMO第三次溫室氣體研究報告](https://ghgsmart.imo.org/wp-content/uploads/2023/05/third-imo-ghg-study-2014-executive-summary-and-final-report.pdf)（2014年報告，PDF第305頁對擴建後巴拿馬運河與散裝船船型的分析）。引用其船型／尺寸限制的原理，不把歷史船隊數當成目前現況。'
 spec['fourth'].update(answer='答案 D：巴拿馬運河（大型礦砂船情境）',points=['使用者已指定採D；原紅筆B可能誤改，保留原卷證據。','好望角航路會進入印度洋，不把B排除。','原題未限定船型；並非所有礦砂船都不能走運河。'])
 art=ROOT/spec['fourth']['image'];s=art.read_text();assert '保留原卷B；航路答案待核' in s;art.write_text(s.replace('保留原卷B；航路答案待核','大型礦砂船情境：選 D'))
 spec.setdefault('supportingSources',[]).append(dict(url='https://ghgsmart.imo.org/wp-content/uploads/2023/05/third-imo-ghg-study-2014-executive-summary-and-final-report.pdf',finding='2014研究PDF第305頁：擴建通航仍受不同船型尺寸/吃水限制；不引用歷史船隊數為現況。'))
elif qid=='q-1135':
 q.update(correctOption='C',answer='(C) 14歲胖虎持刀強迫同學上繳財物',verification='使用者已確認')
 q['explanation']=q['explanation'].replace('原卷教材訂正為C，但本題的單選條件須保留疑義。','依使用者已確認的教材意圖，答案為C；仍保留本題單選條件的限制。')
 q['verificationNote']=q['verificationNote'].replace('本題單選條件待確認，原題文字完整。','使用者已確認教材C及A在重大情節下仍可能裁量移送的條件限制；原題文字完整，不再重問。')
 for option in q['optionAnalysis']:option['wordClass']='應選（依教材意圖）' if option['label']=='C' else '不選'
 spec['title']='依教材選C，保留少年刑責的條件限制';spec['panels'][2]['text']=spec['panels'][2]['text'].replace('故保留單選疑義','解說保留此條件限制');spec['fourth']['answer']='答案 C（依教材意圖，保留條件限制）'
elif qid=='q-1168':
 assert q['correctOption']=='D';q['verification']='使用者已確認';q['verificationNote']+=' 使用者已在monitor確認原AI左右錯圖的排除與新圖處理，答案D維持；不重問同項。'
else:raise ValueError(qid)
for field in ['reviewQuestions','reviewExcerpt','reviewLabel','reviewPreviousId','reviewNextId']:q.pop(field,None)
spec['answerCheckedAgainst']=q['explanation'];spec['confirmationSync']=dict(scope=str((D/'execution-scope.json').relative_to(ROOT)),requestId=record['id'],resolvedAt=record['resolvedAt'],checkedAt=now(),existingFourImagesRetained=True)
save(ROOT/f'docs/complete-questions/{qid}.json',q);save(ROOT/f'docs/comics/{qid}.json',spec)
with locked(ROOT):
 requests=load(ROOT/'docs/review-requests.json');requests.pop(qid,None);save(ROOT/'docs/review-requests.json',requests)
 pipeline=load(ROOT/'docs/comics/pipeline.json');job=next(j for j in reversed(pipeline['jobs']) if j['id']==qid);assert job['state']=='blocked' and 'integrationEventId' not in job
 timing={k:job[k] for k in ['integrationStartedAt','integrationMonotonicStartNs','integrationTimingHost','integrationTimingScope'] if k in job}
 if timing:
  job['previousBlockedArtQATiming']=timing
  for key in timing:job.pop(key,None)
 job.update(state='ready',decision='complete',reason='同步monitor已明確確認的答案／處理，原題與既有四圖保留；僅必要文字／狀態修正。',confirmationUpdateScope=str((D/'execution-scope.json').relative_to(ROOT)),artQAOnly=False);save(ROOT/'docs/comics/pipeline.json',pipeline);update_display(ROOT,pipeline)
begin(ROOT,qid)
print(json.dumps(dict(updated=qid,sourceId=q['sourceId'],correctOption=q['correctOption'],existingImagesRetained=True),ensure_ascii=False))
