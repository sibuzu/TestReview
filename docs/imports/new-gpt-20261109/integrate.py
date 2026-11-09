"""Publish frozen, original-checked drafts; illustration work stays independent.

Usage: python docs/imports/new-gpt-20261109/integrate.py source/manifest.json
The manifest items bind questionPath/questionSHA256 and reviewPath/reviewSHA256.
Only the single integration owner runs this command and curate.py afterwards.
"""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / 'site/scripts')]
from monitor.comic_pipeline import locked, save


def load(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def bound(path, expected):
    assert expected and sha(path) == expected, f'Frozen handoff changed: {path}'
    return load(path)


def publish_asset(path, qid=None):
    source = ROOT / path
    if str(path).startswith('assets/'):
        assert (ROOT / 'site/dist' / path).is_file()
        return path
    assert source.is_file() and str(path).startswith('docs/'), path
    folder = 'questions' if qid else 'originals'
    stem = f'{qid}-{source.stem}' if qid else source.stem
    target = f'assets/{folder}/{stem}-{sha(path)[:12]}{source.suffix}'
    dest = ROOT / 'site/dist' / target
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert dest.read_bytes() == source.read_bytes()
    else:
        dest.write_bytes(source.read_bytes())
    return target


def normalize(question):
    script = "import {validateQuestion} from './site/dist/core.js';let s='';for await(const b of process.stdin)s+=b;console.log(JSON.stringify(validateQuestion(JSON.parse(s))));"
    result = subprocess.run(['node', '--input-type=module', '-e', script], cwd=ROOT,
                            input=json.dumps(question), text=True,
                            capture_output=True, check=True)
    return json.loads(result.stdout)


def grouped(item, manifest_path):
    """Preserve original children and their routes beneath one shared reading."""
    question = bound(item['questionPath'], item['questionSHA256'])
    review = bound(item['reviewPath'], item['reviewSHA256'])
    children = question['groupQuestions']
    members = [q['id'] for q in children]
    assert len(members) >= 2 and len(set(members)) == len(members)
    assert review.get('childCoverage') == members
    assert question['id'] == min(members, key=lambda qid: int(qid[2:]))
    parent_id = question['id']
    directory = (ROOT / manifest_path).parent / 'group-intake'
    directory.mkdir(exist_ok=True)
    for child in children:
        assert child.get('contentStatus') == '完整原題'
        child_path = directory / (child['id'] + '.json')
        save(child_path, child)
        child_item = dict(item, id=child['id'], questionPath=str(child_path.relative_to(ROOT)),
                          questionSHA256=sha(child_path), inheritedGroupDraft=item['questionPath'])
        child_manifest = directory / (child['id'] + '-manifest.json')
        save(child_manifest, child_item)
        main(child_manifest)
    question['images'] = [publish_asset(p, parent_id) for p in question.get('images', [])]
    for figure in question.get('questionFigures', []):
        figure['src'] = publish_asset(figure['src'], parent_id)
    published_children = []
    for qid in members:
        latest = load(f'docs/complete-questions/{qid}.json')
        # An idempotent source-manifest retry reads the retained parent's
        # already-published group override; select its original atomic child.
        if latest.get('groupQuestions'):
            latest = next(c for c in latest['groupQuestions'] if c['id'] == qid)
        published_children.append(latest)
    question['groupQuestions'] = published_children
    question = normalize(question)
    question['addedAt'] = '2026-11-09'
    revision = hashlib.sha256(json.dumps(sorted(members), separators=(',', ':')).encode()).hexdigest()
    with locked(ROOT):
        groups = load('docs/question-groups.json')
        entry = dict(members=members, displayOrder=members, revision=revision)
        assert parent_id not in groups or groups[parent_id] == entry
        assert all(not (set(g['members']) & set(members)) for parent, g in groups.items() if parent != parent_id)
        save(ROOT / f'docs/complete-questions/{parent_id}.json', question)
        groups[parent_id] = entry
        save(ROOT / 'docs/question-groups.json', groups)
    print(json.dumps({'groupPublished': parent_id, 'originalQuestionIds': members}, ensure_ascii=False))


def main(manifest_path):
    manifest_path = manifest_path.resolve().relative_to(ROOT)
    manifest = load(manifest_path)
    plan_path = 'docs/imports/new-gpt-session-2026-11-09.json'
    plan = load(plan_path)
    reservations = load(plan['qidReservations'])['sources']
    imported = []
    for item in manifest.get('items', [manifest]):
        if item.get('status') != 'ready':
            continue
        question = bound(item['questionPath'], item['questionSHA256'])
        if question.get('groupQuestions'):
            grouped(item, manifest_path)
            continue
        review = bound(item['reviewPath'], item['reviewSHA256'])
        qid = question['id']
        assert review.get('originalVisualChecked') is True
        assert review.get('completeOriginalAndOptions') is True
        assert review.get('sourceGeneratedArtUsed') is False
        assert review.get('actualViewed') and all((ROOT / p).is_file() for p in review['actualViewed'])
        assert review.get('duplicateReview') and review.get('inclusionEvidence')
        assert question.get('contentStatus') == '完整原題'
        assert not question.get('explanationFigures'), 'Source AI illustrations are excluded.'
        source = next(s for s in plan['sources'] if s['sourceId'] == question['sourceId'])
        reservation = next(s for s in reservations if s['sourceId'] == question['sourceId'])
        assert reservation['firstId'] <= int(qid[2:]) <= reservation.get('lastId', int(qid[2:]))
        assert (int(qid[2:]) - reservation['firstId']) % reservation['step'] == 0
        acquisition = load(source['acquisitionRecord'])
        assert acquisition['downloadedImages'] and len(acquisition['downloadedImages']) == acquisition['imagesExpected']
        directory = ROOT / source['draftDirectory']
        receipt_path = directory / 'integrated.json'
        receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {'items': []}
        old = next((r for r in receipt['items'] if r['id'] == qid), None)
        if old:
            assert old['draftSHA256'] == item['questionSHA256'], 'Published draft revision needs explicit correction handling.'
            continue
        question['images'] = [publish_asset(p, qid) for p in question.get('images', [])]
        for figure in question.get('questionFigures', []):
            figure['src'] = publish_asset(figure['src'], qid)
        # Provenance remains in the frozen draft and source evidence archive.
        question = normalize(question)
        question['addedAt'] = '2026-11-09'
        assert question['id'] == qid and question['question']
        timestamp = datetime.now(timezone.utc).isoformat()
        with locked(ROOT):
            rows = load('docs/additional-questions.json')
            assert not any(q['id'] == qid for q in rows), 'qid already exists without this receipt.'
            compact = lambda t: ''.join(t.split())
            published_data = load('site/dist/data.json')
            published_originals = [c for q in published_data['questions'] for c in (q.get('groupQuestions') or [q])]
            comparable = {q['id']: q for q in published_originals + rows}
            text_matches = [q['id'] for q in comparable.values() if q.get('subject') == question['subject']
                            and compact(q.get('question', '')) == compact(question['question'])
                            and compact(q.get('passage', '')) == compact(question.get('passage', ''))
                            and q.get('tables', []) == question.get('tables', [])]
            assert not text_matches or review.get('sameTextDifferentFiguresExplained'), f'Exact-text candidate requires explicit figure comparison: {text_matches}'
            rows.append(question)
            save(ROOT / 'docs/additional-questions.json', rows)
            save(ROOT / f'docs/complete-questions/{qid}.json', question)
            sources = load('docs/additional-sources.json')
            row = next(s for s in sources if s['id'] == source['sourceId'])
            meta = load(source['draftDirectory'] + '/source.json')
            transcript = (ROOT / meta['transcriptPath']).read_text()
            target = 'sources/' + source['url'].rsplit('/', 1)[-1] + '.txt'
            (ROOT / 'site/dist' / target).write_text(transcript)
            row.update(status='pending', transcript=target, content=transcript[:100000],
                       images=list(dict.fromkeys(publish_asset(p['path']) for p in acquisition['downloadedImages'])),
                       note='原卷已實取；依製作代理逐題核對稿收入，來源AI圖片不採用，插畫另列待製。')
            save(ROOT / 'docs/additional-sources.json', sources)
            imports = load('docs/imports/more-gpt-progress.json')
            entry = next(s for s in imports['sources'] if s.get('sourceId') == source['sourceId'])
            entry['questionIds'] = list(dict.fromkeys(entry.get('questionIds', []) + [qid]))
            entry.update(state='partial', contentCurationComplete=False,
                         reason='完整原卷核對稿逐題收入；本批其他題目與跨來源查重仍在整理。')
            save(ROOT / 'docs/imports/more-gpt-progress.json', imports)
            progress = load('docs/comics/progress.json')
            assert not any(e['id'] == qid for e in progress['entries'])
            progress['entries'].append(dict(id=qid, subject=question['subject'], date=question['date'],
                title=question['title'], state='queued', questionPublished=True,
                sourceId=question['sourceId'], freshFourPanelRequired=True,
                reason='新來源原題已發布，教學插畫獨立待製；不阻擋完整題目閱讀。'))
            progress['updatedAt'] = timestamp
            save(ROOT / 'docs/comics/progress.json', progress)
            receipt['items'].append(dict(id=qid, draft=item['questionPath'], draftSHA256=item['questionSHA256'],
                producerReview=item['reviewPath'], producerReviewSHA256=item['reviewSHA256'],
                publishedAt=timestamp, teachingComicState='queued',
                publishedSHA256=hashlib.sha256(json.dumps(question, ensure_ascii=False, sort_keys=True).encode()).hexdigest()))
            save(receipt_path, receipt)
            current_plan = load(plan_path)
            current_plan['scopeQuestionIds'] = list(dict.fromkeys(current_plan.get('scopeQuestionIds', []) + [qid]))
            current_plan['updatedAt'] = timestamp
            save(ROOT / plan_path, current_plan)
        imported.append(qid)
    print(json.dumps({'published': imported, 'manifest': str(manifest_path)}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    main(parser.parse_args().manifest)
