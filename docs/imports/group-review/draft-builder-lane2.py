"""Prepare only the currently claimed group's complete, lossless local handoff."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
AGENT = '/root/comic_lane_2'


def read(path):
    return json.loads((ROOT/path).read_text())


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def write(path, value):
    target = ROOT/path
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix+'.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(target)


def union(values):
    output, seen = [], set()
    for value in values:
        key = canonical(value)
        if key not in seen:
            output.append(deepcopy(value))
            seen.add(key)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('group')
    parser.add_argument('--title', required=True)
    args = parser.parse_args()
    queue = read(Path('docs/imports/group-review/queue.json'))
    job = next(g for g in queue['groups'] if g['id'] == args.group)
    assert job['state'] == 'merging' and job['owner'] == AGENT, 'Only build own current claim.'
    report = read(Path(job['reviewReport']))
    reviewed = next(g for g in report['confirmedGroups'] if set(g['questionIds']) == set(job['questionIds']))
    assert reviewed.get('groupType', 'original_paper') in {'original_paper', 'original_paper_group'}
    data_path = ROOT/'site/dist/data.json'
    data_bytes = data_path.read_bytes()
    data = json.loads(data_bytes)
    lookup = {q['id']: q for q in data['questions']}
    raw = {qid: deepcopy(lookup[qid]) for qid in job['questionIds']}
    assert not any(re.search('AI.*(?:延伸|模擬|自編)', q.get('sourceLabel', '')) for q in raw.values())
    numbers = reviewed['originalQuestionNumbers']
    order = reviewed.get('displayQuestionOrder', reviewed.get('displayOrder'))
    if not order:
        order = sorted(raw, key=lambda qid: (int(re.search(r'\d+', str(numbers[qid])).group()), int(qid[2:])))
    assert len(order) == len(raw) and set(order) == set(raw)
    assert job['retainId'] == min(raw, key=lambda qid: int(qid[2:]))

    # Use latest published text, not an earlier audit snapshot, when it matches the common text.
    material = deepcopy(reviewed.get('commonMaterial', {}))
    wanted_passage = material.get('passage', '')
    passage_source = None
    if wanted_passage:
        exact = [qid for qid in order if raw[qid].get('passage', '') == wanted_passage]
        if exact:
            passage_source = exact[0]
        else:
            ranked = sorted(order, key=lambda qid: SequenceMatcher(None, wanted_passage, raw[qid].get('passage', '')).ratio(), reverse=True)
            passage_source = ranked[0]
            assert SequenceMatcher(None, wanted_passage, raw[passage_source].get('passage', '')).ratio() > .9, 'Common passage changed materially; ask root.'
        material['passage'] = raw[passage_source]['passage']
    else:
        material['passage'] = ''
    current_tables = [t for q in raw.values() for t in q.get('tables', [])]
    for table in material.get('tables', []):
        assert table in current_tables, 'Reviewed common table differs from latest; ask root.'
    current_figures = [f for q in raw.values() for f in q.get('questionFigures', [])]
    figures = []
    for reviewed_figure in material.get('questionFigures', []):
        src = reviewed_figure['src']
        latest = next((f for f in current_figures if f.get('src') == src), None)
        figure = deepcopy(latest) if latest else {'src': src, 'alt': '題組共同原卷附圖', 'caption': '共同原卷附圖'}
        for key, value in reviewed_figure.items():
            figure.setdefault(key, deepcopy(value))
        figures.append(figure)
    for ref in material.get('requiredFigureRefs', []):
        src = ref if isinstance(ref, str) else ref['src']
        existing = next((f for f in current_figures if f.get('src') == src), None)
        figures.append(deepcopy(existing) if existing else {'src': src, 'alt': '題組共同原卷材料與必要附圖', 'caption': '共同原卷材料與必要附圖'})
    figures = union(figures)

    parent = deepcopy(raw[job['retainId']])
    children = []
    snapshots = []
    checks = []
    directory = Path('docs/imports/group-review/drafts')/job['id']
    for qid in order:
        original = raw[qid]
        child = deepcopy(original)
        if 'originalQuestionNumber' in child:
            assert str(child['originalQuestionNumber']) == str(numbers[qid])
        child['originalQuestionNumber'] = numbers[qid]
        children.append(child)
        snapshot_path = directory/'children'/(qid+'.json')
        write(snapshot_path, original)
        assert read(snapshot_path) == original
        assert all(child[key] == value for key, value in original.items())
        snapshots.append({'questionId': qid, 'path': str(snapshot_path), 'sha256': sha((ROOT/snapshot_path).read_bytes()), 'canonicalSHA256': sha(canonical(original)), 'sourceId': original['sourceId'], 'sourceLabel': original.get('sourceLabel', ''), 'date': original['date'], 'addedAt': original['addedAt']})
        checks.append({'questionId': qid, 'allOriginalFieldsUnchanged': True, 'fullQuestionAndOptionsPreserved': child.get('question') == original.get('question'), 'answerAndCorrectOptionPreserved': all(child.get(k) == original.get(k) for k in ['answer', 'correctOption']), 'explanationAndOptionAnalysisPreserved': all(child.get(k) == original.get(k) for k in ['explanation', 'optionAnalysis']), 'allFiguresAndOriginalsPreserved': all(child.get(k) == original.get(k) for k in ['images', 'questionFigures', 'explanationFigures', 'tables', 'passage']), 'fullTeachingComicPreserved': child.get('teachingComic') == original.get('teachingComic'), 'teacherConfirmedMetadataPreserved': all(child.get(k) == original.get(k) for k in ['studentAnswer', 'verificationNote', 'protectedWords']), 'teachingComicPresent': bool(original.get('teachingComic'))})

    def heading(qid):
        name = raw[qid]['title'].split('｜', 1)[-1].strip()
        return '【第'+str(numbers[qid])+'題｜'+name+'】'

    parent.update(title=args.title, subject=job['subject'], passage=material['passage'], tables=deepcopy(material.get('tables', [])), questionFigures=figures, groupQuestions=children)
    for field in ['question', 'answer', 'explanation']:
        parent[field] = '\n\n'.join(heading(qid)+'\n'+raw[qid].get(field, '') for qid in order)
    parent['correctOption'] = ''
    parent['optionAnalysis'] = []
    parent['studentAnswer'] = '\n'.join(heading(qid)+' '+raw[qid].get('studentAnswer', '') for qid in order)
    parent['images'] = union([item for qid in order for item in raw[qid].get('images', [])])
    parent['explanationFigures'] = union([item for qid in order for item in raw[qid].get('explanationFigures', [])])
    parent['tags'] = union([tag for qid in order for tag in raw[qid].get('tags', [])])
    earliest = min(raw.values(), key=lambda q: (q['date'], int(q['id'][2:])))
    parent['date'] = earliest['date']
    parent['dateLabel'] = earliest.get('dateLabel', '')
    parent['addedAt'] = min(q['addedAt'] for q in raw.values())
    parent['groupMetadata'] = {'groupId': job['id'], 'kind': 'original_paper', 'originalQuestionIds': job['questionIds'], 'displayOrder': order, 'retainId': job['retainId'], 'aliasesProposed': [qid for qid in raw if qid != job['retainId']], 'reviewReport': job['reviewReport'], 'printedRange': reviewed['printedRange'], 'representativeSubjectReason': reviewed.get('representativeSubjectReason', '依已核原卷題組代表科目。')}
    equivalent_figures = []
    for common in figures:
        common_src = common['src']
        common_hash = sha((ROOT/'site/dist'/common_src).read_bytes())
        for child_figure in current_figures:
            src = child_figure['src']
            if src != common_src and sha((ROOT/'site/dist'/src).read_bytes()) == common_hash:
                equivalent_figures.append({'src': src, 'commonSrc': common_src, 'sha256': common_hash})
    parent['groupMetadata']['commonFigureEquivalentSources'] = union(equivalent_figures)
    assert parent.get('teachingComic') == raw[job['retainId']].get('teachingComic')
    assert [child['id'] for child in children] == order
    for qid in order:
        for field in ['question', 'answer', 'explanation']:
            assert raw[qid].get(field, '') in parent[field]
    assets = set()
    def collect(value):
        if isinstance(value, dict):
            for item in value.values(): collect(item)
        elif isinstance(value, list):
            for item in value: collect(item)
        elif isinstance(value, str) and value.startswith('assets/'):
            assets.add(value)
    collect(parent)
    for asset in assets:
        assert (ROOT/'site/dist'/asset).is_file(), 'Missing asset: '+asset
    write(directory/'question.json', parent)
    manifest = {'schemaVersion': 1, 'groupId': job['id'], 'preparedBy': AGENT, 'preparedAt': datetime.now(timezone.utc).isoformat(), 'questionIds': job['questionIds'], 'retainId': job['retainId'], 'displayOrder': order, 'draftPath': str(directory/'question.json'), 'childCoverage': job['questionIds'], 'reviewReport': job['reviewReport'], 'childSnapshots': snapshots, 'checks': {'allChildrenFullObjects': True, 'noAnswerOrExplanationChanged': True, 'noChildComicDeduplication': True, 'parentCorrectOptionEmpty': True, 'commonPassageSourceQuestionId': passage_source, 'reviewedCommonMaterialRetained': True, 'allReferencedAssetsExist': True, 'assetCount': len(assets), 'perChild': checks}, 'inputPublishedData': {'path': 'site/dist/data.json', 'sha256': sha(data_bytes), 'questions': len(data['questions'])}, 'notes': ['僅獨立合稿，未改題庫/別名/雲端標記/來源進度，未重新製圖。', '各子完整原物件另有快照；groupQuestions只增原卷題號，其餘欄位逐項完全一致。', 'parent保留canonical既有漫畫僅作舊版相容；正式新renderer必須逐子呈現全部漫畫一次。']}
    write(directory/'manifest.json', manifest)
    print(json.dumps({'groupId': job['id'], 'title': parent['title'], 'order': order, 'answers': {qid: raw[qid].get('correctOption') for qid in order}, 'commonPassageChars': len(parent['passage']), 'tables': len(parent['tables']), 'commonFigures': len(figures), 'childComicCount': sum(bool(q.get('teachingComic')) for q in raw.values()), 'assets': len(assets), 'manifest': str(directory/'manifest.json')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
