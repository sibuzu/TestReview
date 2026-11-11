"""Recheck the user's missing-only finish without resuming paused reworks."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from monitor.comic_pipeline import now,save
from monitor.comic_publish import missing_scope_finished,pending_batch
D=Path(__file__).resolve().parent
plan=json.loads((D/'plan.json').read_text());control=plan['executionControl'];ids=set(control['activeOriginalQuestionIds'])
assert plan['state']=='paused' and plan['goalActive'] is False
assert control['missingIllustration']=='completed' and control['biologyQualityUpgrade']=='paused' and control['textOnlyReplacement']=='paused'
assert len(ids)==22 and (plan['questionPageCount'],plan['originalQuestionCount'],plan['requiredImageCount'])==(130,140,560)
complete=[e for e in plan['entries'] if e['state']=='complete'];paused=[e for e in plan['entries'] if e['state']=='paused']
assert (len(complete),sum(len(e['originalQuestionIds']) for e in complete),plan['completedImages'])==(62,65,260)
assert len(paused)==68 and sum(len(e['originalQuestionIds']) for e in paused)==75
initial=json.loads((D/'scope-change-completion-snapshot.json').read_text());initial_ids={qid for e in initial['entries'] for qid in e['originalQuestionIds']};complete_ids={qid for e in complete for qid in e['originalQuestionIds']};assert complete_ids-initial_ids==ids
payload=json.loads((ROOT/'site/dist/data.json').read_text());by={q['id']:q for q in payload['questions']};atomic={q['id']:q for parent in payload['questions'] for q in parent.get('groupQuestions') or [parent]}
baseline=json.loads((D/'original-content-baseline.json').read_text())
def core(value):
 if isinstance(value,dict):return {k:core(v) for k,v in value.items() if k not in ['teachingComic','explanationFigures']}
 if isinstance(value,list):return [core(v) for v in value]
 return value
assert all(core(q)==core(by[q['id']]) for q in baseline),'Original content changed'
base={q['id']:q for q in baseline}
for e in paused:
 old=base[e['id']].get('groupQuestions') or [base[e['id']]];new=by[e['id']].get('groupQuestions') or [by[e['id']]]
 assert [q.get('teachingComic') for q in old]==[q.get('teachingComic') for q in new],e['id']
for qid in sorted(ids):
 spec=json.loads((ROOT/f'docs/comics/{qid}.json').read_text());review=spec['rootReview'];assert all(review.get(k) for k in ['visualChecked','originalVisualChecked','answerAndExplanationChecked','fourActualIndependentImages'])
 comic=atomic[qid]['teachingComic'];images=[p['image'] for p in comic['panels']]+[comic['fourth']['image']];assert len(set(images))==4 and all((ROOT/'site/dist'/p).is_file() for p in images)
 assert len(json.loads((ROOT/f'docs/comics/{qid}-validation.json').read_text())['results'])==6
 assert len(json.loads((ROOT/f'docs/comics/{qid}-preview-validation.json').read_text())['results'])==3
refs=set()
def walk(value):
 if isinstance(value,dict):
  for v in value.values():walk(v)
 elif isinstance(value,list):
  for v in value:walk(v)
 elif isinstance(value,str):
  if value.startswith('assets/') and '\n' not in value:refs.add(value)
  refs.update(re.findall(r'''(?:src|href)=["'](assets/[^"']+)''',value))
walk(payload);missing=[path for path in refs if not (ROOT/'site/dist'/path).is_file()];assert not missing
quality=json.loads((ROOT/'site/dist/biology-illustration-status.json').read_text());assert sum(x['state']=='fine' for x in quality.values())==17 and sum(x['state']=='legacy' for x in quality.values())==29
log=(ROOT/'.cache/root-missing-only-final-tests.log').read_text();assert re.search(r'# pass 123\b',log) and re.search(r'# fail 0\b',log)
_,_,_,jobs=pending_batch()
assert not jobs or missing_scope_finished(ROOT,jobs)
report=dict(checkedAt=now(),activeMissingOriginalIds=sorted(ids),activeMissingQuestionPages=20,activeMissingOriginals=22,activeMissingImages=88,formalLayouts=132,isolatedLayouts=66,finalBatchFormalLayouts=30,finalBatchOriginalIds=['q-774','q-608','q-612','q-762','q-763'],actualVisualReview='唯一整合者逐題實開原卷及必要圖、四張新圖、正式app/單頁1440與390；1120另自動排版驗證。',historicalScope=dict(questionPages=130,originalQuestions=140,requiredImages=560),historicalAccepted=dict(questionPages=62,originalQuestions=65,images=260),paused=dict(questionPages=68,originalQuestions=75,artworkMatchesOriginalBaseline=True),originalContentAndAnswersUnchanged=True,referencedAssets=len(refs),missingAssets=missing,biologyFine=17,biologyLegacy=29,siteTests=dict(actualCommand='npm test --prefix site',passed=123,failed=0,evidence='.cache/root-missing-only-final-tests.log',independentReviewer='/root'),rootIndependentSpotCheck=['q612-app-390','q774-standalone-1440'],partialPublicationGate='only explicit final flag, completed active missing scope, jobs inside active IDs, both rework categories paused',usageTokens=None,usageNote='內建imagegen未提供usage；不估算、不填0。',status='missing-only completed; broader rework paused',worknerdTaskId='t_a87b51180cc247a88d16')
save(D/'missing-only-completion-validation.json',report)
print(json.dumps(dict(result='PASS',missingOnly='22/22',historical='65/140',paused='75',referencedAssets=len(refs),missingAssets=missing),ensure_ascii=False))
