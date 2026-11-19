"""Read-only checks of this intake; writes only this lane's final evidence file."""
import datetime
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parents[1]
read = lambda p: json.loads(p.read_text())
plan = read(BASE/'plan.json')
assert plan['productionStopped'] and plan['validatedIllustrationCount'] == 84
assert plan['illustrationsOutstanding'] == 0
ids = set(plan['newQuestionIds'])
assert len(ids) == 21
old = {q['id']: q for q in read(ROOT/'.cache/intake-20261117-72/baseline-data.json')['questions']}
new = {q['id']: q for q in read(ROOT/'site/dist/data.json')['questions']}
assert len(old) == 936 and len(new) == 957 and set(new)-set(old) == ids
navigation = {'reviewLabel', 'reviewPreviousId', 'reviewNextId'}
normalize = lambda q: {k:v for k,v in q.items() if k not in navigation}
assert all(normalize(q) == normalize(new[i]) for i,q in old.items())
assert all(new[i]['date'] == '2026-11-17' for i in ids)
assert all(new[i]['date'] == '2026-10-29' for i in plan['duplicateQuestionIds'])
assets = []
for qid in sorted(ids):
    q = new[qid]
    c = q['teachingComic']
    spec = read(ROOT/f'docs/comics/{qid}.json')
    paths = [p['image'] for p in c['panels']] + [c['fourth']['image']]
    sources = [p['image'] for p in spec['panels']] + [spec['fourth']['image']]
    assert len(paths) == len(set(paths)) == 4
    for relative, source in zip(paths, sources):
        path = ROOT/'site/dist'/relative
        raw = path.read_bytes()
        if path.suffix != '.svg':
            with Image.open(path) as im:
                im.load()
                assert min(im.size) > 0
                with Image.open(ROOT/source) as original:
                    assert im.size == original.size
        else:
            # The price bar chart legitimately uses rect/line primitives.
            assert b'<svg' in raw and any(s in raw for s in [b'<path', b'<circle', b'<polygon', b'<rect', b'<line'])
        assets.append({'id':qid, 'path':relative, 'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()})
    assert spec['sourceGeneratedArtUsed'] is False
    if spec.get('producerAgent') == '/root':
        assert spec['producerReview']['desktopMobileActuallyViewed']
    else:
        producer = read(BASE/'lane3/comics/generation-audit.json')
        assert spec['producerVisualChecked'] and producer['actuallyViewedEveryFullSizeImage']
        assert producer['actuallyViewedEveryThreeWidthPreview']
    assert spec['rootReview']['reviewerAgent'] == '/root/comic_lane_1'
    assert spec['rootReview']['fourActualIndependentImages']
    validation = read(ROOT/f'docs/comics/{qid}-validation.json')
    assert len(validation['results']) == 6
    assert all(not r['docOverflow'] and not r['overflow'] and len(r['artImages']) == 4
               and all(im['loaded'] for im in r['artImages']) for r in validation['results'])
assert len(assets) == len({a['path'] for a in assets}) == len({a['sha256'] for a in assets}) == 84
originals = read(BASE/'acquisition.json')['downloadedImages']
assert len(originals) == 24
for row in originals:
    p = ROOT/row['path']
    b = p.read_bytes()
    assert len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256']
    with Image.open(p) as im:
        im.load()
        assert im.size == (row['width'], row['height']) == (1080, 1440)
progress = read(BASE/'execution-progress.json')
awaiting = {'q-1135', 'q-1153', 'q-1154'}
assert set(progress['awaitingConfirmationQuestionIds']) == awaiting
assert len(progress['completedQuestionIds']) == 18
events = plan['integrationEvents']
assert len(events) == len({e['integrationEventId'] for e in events}) == 18
assert not awaiting.intersection(e['id'] for e in events)
ledger = read(ROOT/'docs/comics/publication-ledger.json')
published_events = {event for batch in ledger['publishedBatches'] for event in batch['eventIds']}
assert set(read(BASE/'publication-baseline.json')['baselineEventIds']) <= published_events
pending_events = {e['integrationEventId'] for e in events} - published_events
assert len(pending_events) == 8
for qid in awaiting:
    assert new[qid]['verification'] == '待核對' and new[qid]['correctOption'] == ''
for qid in ['q-1153','q-1154']:
    assert new[qid]['contentStatus'] == '待更新'
assert read(ROOT/'monitor/new-source-authorization.json')['state'] == 'closed'
assert read(ROOT/'docs/comics/pipeline.json')['claimsPaused']
report = {'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'passed':True, 'oldQuestionsPreserved':936, 'newQuestions':21, 'duplicateOriginals':3,
          'originalsReDecodedAndHashed':24, 'publishedIndependentIllustrations':84,
          'formalLayoutsVerified':126, 'completeIntegrationEvents':18,
          'pendingPublicationEvents':len(pending_events),
          'awaitingConfirmationQuestionIds':sorted(awaiting), 'executionClosed':True,
          'assets':assets}
(Path(__file__).parent/'final-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k != 'assets'},ensure_ascii=False))
