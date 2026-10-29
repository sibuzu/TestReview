from item_helpers import *
import sys
qid,nextId,nextNo=sys.argv[1:];mPath=P/'manifest.json';m=json.loads(mPath.read_text());assert qid not in [x['id'] for x in m['items']],'Frozen item already ready'
sp=R/'docs/comics'/f'{qid}.json';s=json.loads(sp.read_text());end=time.monotonic_ns();stamp=now();duration=(end-s['startedMonotonicNs'])/1e9
s.update(completedAt=stamp,endedMonotonicNs=end,durationSeconds=duration if duration>=0 else None,timingValid=duration>=0,monotonicClockHost='same-execution-host',excludeFromSpeedStatistics=True,speedStatisticsExclusionReason='原生SVG，非imagegen生成樣本',visualChecked=True);dump(sp,s)
qp=P/'questions'/f'{qid}.json';q=json.loads(qp.read_text());auto=P/'qa'/f'{qid}-validation.json';assert json.loads(auto.read_text())['passed']
viewed=[f'docs/imports/new-gpt-20261029-a/qa/{qid}-app-{kind}-{width}.png' for kind in ['question','comic'] for width in [1440,390]]+[f'.cache/new-gpt-20261029-a-publish/{qid}-original.webp']
review=dict(id=qid,passed=True,reviewerAgent='/root/comic_lane_2',checkedAt=stamp,questionPath=str(qp.relative_to(R)),questionSHA256=sha(qp),automatedValidation=str(auto.relative_to(R)),automatedValidationSHA256=sha(auto),comicPreviewValidation=f'docs/comics/{qid}-preview-validation.json',appAndStandaloneWidths=[1440,1120,390],actualViewed=viewed,actualViewScope='實看原卷裁圖、app完整題目及全部四格1440/390；app/standalone三寬皆程式核對，不冒稱standalone實看。',completeOriginalAndOptions=True,necessaryFiguresVisuallyChecked=True,newComicRawVisuallyChecked=True,answerDefaultCollapsed=True,noOverflow=True,personalCloudRequestsAborted=True,sourceGeneratedArtUsed=False,newSubstantiveIssues=[])
rp=P/'qa'/f'{qid}-reviewed.json';dump(rp,review)
allAssets=json.loads((P/'asset-map.json').read_text());targets=set(q['images']+[q['teachingComic']['art']]+[f['src'] for f in q.get('questionFigures',[])])
assets=[a for a in allAssets if a['targetPath'] in targets];assert len(assets)>=2
m['items'].append(dict(id=qid,sourceId='src-more-049',questionPath=str(qp.relative_to(R)),questionSHA256=sha(qp),specPath=str(sp.relative_to(R)),specSHA256=sha(sp),qaReport=str(rp.relative_to(R)),qaReportSHA256=sha(rp),contentReview=f'docs/imports/new-gpt-20261029-a/reviews/{qid}-content.json',status='ready',assets=assets,readyAt=stamp));dump(mPath,m)
aPath=R/'docs/acquisition/new-gpt-20261029-a.json';a=json.loads(aPath.read_text());a.update(checkedAt=stamp,readyQuestionCount=len(m['items']),completedOriginalQuestions=[json.loads((R/x['questionPath']).read_text())['originalQuestionNumber'] for x in m['items']],currentQuestionId=nextId,currentOriginalQuestionNumber=nextNo);dump(aPath,a)
print('READY',qid,len(m['items']))
