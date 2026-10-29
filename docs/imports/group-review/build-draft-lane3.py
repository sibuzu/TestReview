"""Build one claimed, verified group without writing the published question bank."""
import argparse
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/jack/git/TestReview')


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def unique(values):
    result = []
    seen = set()
    for value in values:
        key = canonical(value)
        if key not in seen:
            result.append(copy.deepcopy(value))
            seen.add(key)
    return result


def build(group_id, title):
    queue = json.loads((ROOT / 'docs/imports/group-review/queue.json').read_text())
    job = next(g for g in queue['groups'] if g['id'] == group_id)
    assert job['owner'] == '/root/comic_lane_3' and job['state'] == 'merging'
    review_path = ROOT / job['reviewReport']
    assert hashlib.sha256(review_path.read_bytes()).hexdigest() == job['reviewSHA256']
    review = json.loads(review_path.read_text())
    basis = next(g for g in review['confirmedGroups'] if set(g['questionIds']) == set(job['questionIds']))
    assert basis.get('groupType') != 'ai_extension_group'
    data_path = ROOT / 'site/dist/data.json'
    data = json.loads(data_path.read_text())
    by_id = {q['id']: q for q in data['questions']}
    sources = {s['id']: s for s in data['sources']}
    ids = job['questionIds']
    originals = {qid: by_id[qid] for qid in ids}
    assert all('來源AI延伸' not in q.get('sourceLabel', '') for q in originals.values())
    numbers = basis['originalQuestionNumbers']
    order = basis.get('printedQuestionOrder')
    if not order:
        def sort_number(qid):
            value = str(numbers.get(qid) or '')
            return (0, int(value)) if value.isdigit() else (1, ids.index(qid))
        order = sorted(ids, key=sort_number)
    assert len(order) == len(ids) and set(order) == set(ids)
    children = []
    for qid in order:
        child = copy.deepcopy(originals[qid])
        if numbers.get(qid) is not None:
            if 'originalQuestionNumber' in child:
                assert str(child['originalQuestionNumber']) == str(numbers[qid])
            child['originalQuestionNumber'] = str(numbers[qid])
        children.append(child)
    parent = copy.deepcopy(originals[job['retainId']])
    common = basis.get('commonMaterial', {})
    passage = common.get('passage', '')
    if passage:
        assert any(passage == q.get('passage', '') or passage in q.get('question', '') for q in originals.values()), 'Common passage needs an existing exact source'
    tables = common.get('tables', [])
    assert all(any(table in q.get('tables', []) for q in originals.values()) for table in tables)
    current_figures = [f for q in originals.values() for f in q.get('questionFigures', [])]
    figures = []
    for figure in common.get('questionFigures', []):
        match = next((f for f in current_figures if f.get('src') == figure.get('src')), None)
        if match is None:
            target_hash = hashlib.sha256((ROOT / 'site/dist' / figure['src']).read_bytes()).hexdigest()
            match = next(f for f in current_figures if hashlib.sha256((ROOT / 'site/dist' / f['src']).read_bytes()).hexdigest() == target_hash)
        figures.append(copy.deepcopy(match))
    date_child = min((q for q in originals.values() if q.get('date')), key=lambda q: (q['date'], int(q['id'][2:])))
    parent.update(title=title, subject=job['subject'], groupQuestions=children,
                  passage=passage, tables=copy.deepcopy(tables), questionFigures=figures,
                  date=date_child['date'], dateLabel=date_child.get('dateLabel', ''),
                  addedAt=min(q['addedAt'] for q in originals.values() if q.get('addedAt')),
                  images=unique([i for q in originals.values() for i in q.get('images', [])]),
                  explanationFigures=unique([f for q in originals.values() for f in q.get('explanationFigures', [])]),
                  optionAnalysis=[], correctOption='')
    if basis.get('commonOptionBank'):
        parent['commonOptionBank'] = copy.deepcopy(basis['commonOptionBank'])
    def section(qid):
        number = numbers.get(qid)
        unit = '項' if number and re.search(r'第\s*' + re.escape(str(number)) + r'\s*項', originals[qid]['title']) else '題'
        return f'【原第{number}{unit}｜{originals[qid]["title"]}】' if number else f'【{originals[qid]["title"]}】'
    for field in ['question', 'answer', 'explanation', 'studentAnswer', 'trap']:
        parent[field] = '\n\n'.join(section(qid) + '\n' + originals[qid][field] for qid in order if originals[qid].get(field))
    parent['tags'] = unique([tag for q in originals.values() for tag in q.get('tags', [])])
    checks = []
    snapshots = []
    for child in children:
        qid = child['id']
        original = originals[qid]
        preserved = all(child.get(key) == value for key, value in original.items())
        assert preserved and set(child) - set(original) <= {'originalQuestionNumber'}
        asset_paths = list(original.get('images', []))
        asset_paths += [f['src'] for f in original.get('questionFigures', []) + original.get('explanationFigures', [])]
        if original.get('teachingComic', {}).get('art'):
            asset_paths.append(original['teachingComic']['art'])
        for asset in asset_paths:
            assert (ROOT / 'site/dist' / asset).is_file(), f'Missing asset: {asset}'
        checks.append({'id': qid, 'fullObjectPreserved': preserved, 'originalQuestionPreserved': child['question'] == original['question'],
                       'allOptionsPreserved': child.get('optionAnalysis') == original.get('optionAnalysis') and child['question'] == original['question'],
                       'answerPreserved': child['answer'] == original['answer'] and child.get('correctOption') == original.get('correctOption'),
                       'explanationPreserved': child['explanation'] == original['explanation'],
                       'allFiguresAndTablesPreserved': all(child.get(k) == original.get(k) for k in ['passage', 'tables', 'questionFigures', 'images', 'explanationFigures']),
                       'ownComicPreserved': child.get('teachingComic') == original.get('teachingComic'),
                       'assetFilesChecked': len(asset_paths)})
        snapshots.append({'id': qid, 'sha256': sha(original), 'sourceId': original['sourceId'],
                          'sourceURL': sources[original['sourceId']]['url'], 'sourcePath': 'site/dist/data.json',
                          'fieldNames': sorted(original)})
    assert parent.get('teachingComic') == originals[job['retainId']].get('teachingComic')
    out = ROOT / 'docs/imports/group-review/drafts' / group_id
    out.mkdir(parents=True, exist_ok=True)
    draft_path = out / 'question.json'
    manifest_path = out / 'manifest.json'
    manifest = {'groupId': group_id, 'producerAgent': '/root/comic_lane_3', 'createdAt': datetime.now(timezone.utc).isoformat(),
                'questionIds': ids, 'retainId': job['retainId'], 'displayOrder': order,
                'draftPath': str(draft_path.relative_to(ROOT)), 'childCoverage': order,
                'reviewReport': job['reviewReport'], 'reviewSHA256': job['reviewSHA256'],
                'dataSnapshotSHA256': hashlib.sha256(data_path.read_bytes()).hexdigest(),
                'hashMethod': 'SHA256 of UTF-8 canonical JSON: ensure_ascii=False, sort_keys=True, separators=(comma,colon)',
                'childSnapshots': snapshots, 'checks': checks, 'representativeSubject': job['subject'],
                'representativeSubjectReason': basis.get('representativeSubjectReason'),
                'commonMaterialSource': 'Verified review and matching latest published child objects; no new text/answers/images',
                'sourceAIImagesAdded': False, 'newArtProduced': False,
                'notes': ['All child object fields remain unchanged except optional originalQuestionNumber addition.',
                          'Parent teachingComic only supports the old renderer; the grouped renderer must show each child comic once.',
                          'Draft only. No shared bank, aliases, flags or published assets were mutated.']}
    draft_path.write_text(json.dumps(parent, ensure_ascii=False, indent=2) + '\n')
    manifest['draftSHA256'] = hashlib.sha256(draft_path.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'group': group_id, 'order': order, 'title': title, 'checks': len(checks), 'manifest': str(manifest_path.relative_to(ROOT))}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('group')
    parser.add_argument('--title', required=True)
    args = parser.parse_args()
    build(args.group, args.title)
