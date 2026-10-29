"""Mechanically add one frozen, producer-reviewed item from the two GPT sources.

The producer owns transcription, answers and visual QA. This command verifies
handoff hashes, publishes identical asset bytes, and preserves the review record.
It never substitutes an independent content or layout review.
"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from monitor.comic_pipeline import locked, load, save, now, ensure_job_identity, update_display, integrated


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(path, expected=None):
    path = ROOT / path
    assert path.is_file(), f'Missing handed-off file: {path}'
    if expected:
        assert digest(path) == expected, f'Frozen handoff changed: {path}'
    return path


def normalize(question):
    script = "import {validateQuestion} from './site/dist/core.js';let s='';for await(const b of process.stdin)s+=b;console.log(JSON.stringify(validateQuestion(JSON.parse(s))));"
    return json.loads(subprocess.run(['node', '--input-type=module', '-e', script],
                      cwd=ROOT, input=json.dumps(question), text=True,
                      capture_output=True, check=True).stdout)


def rewrite(value, mappings):
    if isinstance(value, str):
        return mappings.get(value, value)
    if isinstance(value, list):
        return [rewrite(v, mappings) for v in value]
    if isinstance(value, dict):
        return {k: rewrite(v, mappings) for k, v in value.items()}
    return value


def publish_bytes(path, target):
    sha = digest(path)
    old = Path(target)
    target = old.with_name(f'{old.stem}-{sha[:12]}{old.suffix}').as_posix()
    assert target.startswith(('assets/', 'sources/')) and '..' not in Path(target).parts
    dest = ROOT/'site/dist'/target
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert digest(dest) == sha, f'Immutable asset collision: {target}'
    else:
        dest.write_bytes(path.read_bytes())
    return target


def load_item(manifest_path, item_id=None):
    document = load(manifest_path)
    if 'items' not in document:
        return document
    if item_id:
        return next(item for item in document['items'] if item['id'] == item_id)
    assert len(document['items']) == 1, 'Choose --id for a multi-item source manifest'
    return document['items'][0]


def source_directory(manifest):
    order = {'src-more-049': 49, 'src-more-050': 50}[manifest['sourceId']]
    source = next(s for s in load(ROOT/'docs/imports/more-gpt-progress.json')['sources']
                  if s['order'] == order)
    return ROOT/source['draftDirectory']


def main(manifest_path, item_id=None):
    manifest = load_item(manifest_path, item_id)
    assert manifest['status'] == 'ready'
    directory = source_directory(manifest)
    receipt_path = directory/'integrated.json'
    receipt = load(receipt_path) if receipt_path.exists() else {'items': []}
    existing = next((r for r in receipt['items'] if r['id'] == manifest['id']), None)
    if existing:
        assert existing['questionSHA256'] == manifest['questionSHA256']
        print(json.dumps(existing, ensure_ascii=False))
        return
    qpath = checked(manifest['questionPath'], manifest['questionSHA256'])
    spec_path = checked(manifest['specPath'], manifest['specSHA256'])
    review_path = checked(manifest['qaReport'], manifest['qaReportSHA256'])
    question, spec, review = load(qpath), load(spec_path), load(review_path)
    assert question['id'] == spec['id'] == manifest['id'] == review['id']
    assert question['sourceId'] == manifest['sourceId'] in ('src-more-049', 'src-more-050')
    number = int(question['id'].removeprefix('q-'))
    assert number >= 850 and number % 2 == (question['sourceId'] == 'src-more-050'), 'Reserved permanent qid sequence mismatch'
    assert review['passed'] and review['actualViewed']
    assert review['completeOriginalAndOptions'] and not review['sourceGeneratedArtUsed']
    for path in review['actualViewed']:
        checked(path)
    validation_path = checked(review['automatedValidation'], review.get('automatedValidationSHA256'))
    assert not question.get('groupQuestions'), 'Pass grouped items through the catalog branch, preserving all child specs.'
    data = load(ROOT/'site/dist/data.json')
    raw = [c for q in data['questions'] for c in (q.get('groupQuestions') or [q])]
    assert not any(q['id'] == question['id'] for q in raw), 'qid already published without receipt'
    compact = lambda text: re.sub(r'\s+', '', text)
    handed_assets = {a['targetPath']: a['sha256'] for a in manifest['assets']}
    def figure_hashes(q, incoming=False):
        return [handed_assets[f['src']] if incoming else digest(ROOT/'site/dist'/f['src'])
                for f in q.get('questionFigures', [])]
    duplicates = [q['id'] for q in raw if q['subject'] == question['subject']
                  and compact(q['question']) == compact(question['question'])
                  and compact(q.get('passage', '')) == compact(question.get('passage', ''))
                  and q.get('tables', []) == question.get('tables', [])
                  and figure_hashes(q) == figure_hashes(question, True)]
    assert not duplicates, f'Exact original-text duplicate requires producer disposition: {duplicates}'
    mappings = {}
    for asset in manifest['assets']:
        source = checked(asset['sourcePath'], asset['sha256'])
        mappings[asset['targetPath']] = publish_bytes(source, asset['targetPath'])
    source_asset_mappings = dict(mappings)
    for original, common in manifest.get('renderAssetAliases', {}).items():
        assert original in mappings and common in mappings
        mappings[original] = mappings[common]
    question = normalize(rewrite(question, mappings))
    # This is publication metadata; the producer's original question date stays.
    published_added_at = datetime.now(ZoneInfo('Asia/Taipei')).date().isoformat()
    question['addedAt'] = published_added_at
    metadata_overrides = {'addedAt': published_added_at}
    for key in ('originalQuestionNumber',):
        if key in manifest.get('questionMetadataOverrides', {}):
            question[key] = manifest['questionMetadataOverrides'][key]
            metadata_overrides[key] = question[key]
    assert question.get('teachingComic') and not question.get('explanationFigures')
    for asset in question['images'] + [f['src'] for f in question.get('questionFigures', [])] + [question['teachingComic']['art']]:
        checked('site/dist/' + asset)
    source = load(directory/'source.json')
    transcript_path = checked(source['transcriptPath'])
    transcript = publish_bytes(transcript_path, f'sources/{source["id"]}.txt')
    source_id = source['id']
    order = 49 if source_id == 'src-more-049' else 50
    lane = int(review['reviewerAgent'].rsplit('_', 1)[-1])
    assert lane in (2, 3), 'Record the actual producer, independently of source ownership'
    timestamp = now()
    with locked(ROOT):
        additional = load(ROOT/'docs/additional-questions.json')
        assert not any(q['id'] == question['id'] for q in additional)
        additional.append(question)
        save(ROOT/'docs/additional-questions.json', additional)
        save(ROOT/'docs/complete-questions'/f'{question["id"]}.json', question)
        sources = load(ROOT/'docs/additional-sources.json')
        row = next(s for s in sources if s['id'] == source_id)
        row.update(title=source['title'], date=source['date'], platform='ChatGPT',
                   status='pending', transcript=transcript,
                   content=transcript_path.read_text()[:100000],
                   note='原卷與題目由指定製作代理核對，逐筆收入；僅採原卷錯題及自製四格。')
        row['images'] = list(dict.fromkeys(row.get('images', []) + question['images']))
        save(ROOT/'docs/additional-sources.json', sources)
        imports = load(ROOT/'docs/imports/more-gpt-progress.json')
        imported = next(s for s in imports['sources'] if s['order'] == order and s['url'] == source['url'])
        acquisition = load(ROOT/imported['acquisitionRecord'])
        imported.update(title=source['title'], state='partial', sourceCurationComplete=False,
                        downloadedImages=acquisition.get('downloadedImages', acquisition.get('originalImages', [])),
                        reason='原圖已取回；已完成稿逐筆收入，其餘由指定代理繼續核對與製圖。')
        imported['questionIds'] = list(dict.fromkeys(imported.get('questionIds', []) + [question['id']]))
        imports['updatedAt'] = timestamp
        save(ROOT/'docs/imports/more-gpt-progress.json', imports)
        progress = load(ROOT/'docs/comics/progress.json')
        assert not any(e['id'] == question['id'] for e in progress['entries'])
        progress['entries'].append(dict(id=question['id'], title=question['title'],
            subject=question['subject'], date=question['date'], state='queued',
            questionPublished=True, sourceId=source_id))
        progress.update(updatedAt=timestamp, workflowState='active')
        save(ROOT/'docs/comics/progress.json', progress)
        pipeline = load(ROOT/'docs/comics/pipeline.json')
        job = dict(id=question['id'], title=question['title'], subject=question['subject'],
                   lane=lane, state='ready', startedAt=manifest['readyAt'], readyAt=manifest['readyAt'],
                   decision='complete', reason='新來源原卷與全新四格；指定製作代理完成原題核對與自身完整版面QA，整合者僅技術加入。',
                   evidence=[manifest['questionPath'], manifest['specPath'], manifest['qaReport']],
                   producerManifest=str(manifest_path.relative_to(ROOT)))
        ensure_job_identity(job)
        pipeline['jobs'].append(job)
        save(ROOT/'docs/comics/pipeline.json', pipeline)
        update_display(ROOT, pipeline)
    validation = load(validation_path)
    validation.update(inheritedProducerReview=manifest['qaReport'],
                      inheritedWithoutRepeatedVisualReview=True,
                      technicalIntegrator='/root/comic_lane_1')
    save(ROOT/'docs/comics'/f'{question["id"]}-validation.json', validation)
    spec.update(nativeArt=question['teachingComic']['art'], layoutVersion='native-fluid-v6',
        rootReview=dict(visualChecked=True, reviewerAgent=review['reviewerAgent'],
            inheritedProducerQA=manifest['qaReport'], mechanicalIntegrator='/root/comic_lane_1',
            actualViewed=review['actualViewed'], checkedAt=review['checkedAt']))
    save(spec_path, spec)
    result = dict(id=question['id'], sourceId=source_id, questionSHA256=manifest['questionSHA256'],
                  producerManifest=str(manifest_path.relative_to(ROOT)),
                  producerReview=manifest['qaReport'], assetMappings=mappings,
                  sourceAssetMappings=source_asset_mappings,
                  renderAssetAliases=manifest.get('renderAssetAliases', {}),
                  metadataOverrides=metadata_overrides,
                  jobId=job['jobId'], addedAt=timestamp, state='added_pending_curate_and_integrated')
    receipt['items'].append(result)
    save(receipt_path, receipt)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def finish(manifest_path, item_id=None):
    manifest = load_item(manifest_path, item_id)
    directory = source_directory(manifest)
    receipt_path = directory/'integrated.json'
    receipt = load(receipt_path)
    row = next(r for r in receipt['items'] if r['id'] == manifest['id'])
    if row['state'] == 'integrated':
        print(manifest['id'], 'already integrated; no new event')
        return
    expected = normalize(rewrite(load(ROOT/manifest['questionPath']), row['assetMappings']))
    expected.update(row.get('metadataOverrides', {}))
    data = load(ROOT/'site/dist/data.json')
    actual = next(child for q in data['questions'] for child in (q.get('groupQuestions') or [q])
                  if child['id'] == manifest['id'])
    assert actual == expected, 'Curator output differs from the frozen producer item beyond documented asset paths/defaults'
    for path in actual['images'] + [f['src'] for f in actual.get('questionFigures', [])] + [actual['teachingComic']['art']]:
        checked('site/dist/' + path)
    url = f'http://127.0.0.1:8765/site/{manifest["id"]}.html'
    response = urllib.request.urlopen(url)
    assert response.status == 200
    validation = directory/'qa'/f'{manifest["id"]}-intake-validation.json'
    save(validation, dict(id=manifest['id'], passed=True, kind='mechanical-intake',
        producerReview=manifest['qaReport'], noRepeatedContentOrVisualReview=True,
        fullProducerQuestionPreserved=True, immutableAssetMappings=row['assetMappings'],
        standaloneURL=url, httpStatus=response.status, questionEntries=len(data['questions'])))
    integrated(ROOT, manifest['id'])
    with locked(ROOT):
        receipt = load(receipt_path)
        row = next(r for r in receipt['items'] if r['id'] == manifest['id'])
        row.update(state='integrated', integratedAt=now(), intakeValidation=str(validation.relative_to(ROOT)))
        save(receipt_path, receipt)
    print(manifest['id'], 'integrated; frozen content preserved, producer QA inherited')


def grouped(manifest_path, item_id=None, finalize=False):
    """Adapt an already-reviewed parent into the existing per-original ledger."""
    manifest = load_item(manifest_path, item_id)
    directory = source_directory(manifest)
    intake = directory/'intake'
    intake.mkdir(exist_ok=True)
    if finalize:
        expected = load(intake/f'{manifest["id"]}-published-parent.json')
        actual = next(q for q in load(ROOT/'site/dist/data.json')['questions'] if q['id'] == manifest['id'])
        assert actual == expected, 'Curated parent lost producer fields or a child comic'
        for child in manifest['childSpecs']:
            finish(intake/f'{child["id"]}-manifest.json')
        with locked(ROOT):
            receipt = load(directory/'integrated.json')
            row = next(r for r in receipt['groups'] if r['id'] == manifest['id'])
            row.update(state='integrated', integratedAt=now())
            save(directory/'integrated.json', receipt)
        return
    receipt_path = directory/'integrated.json'
    prior = load(receipt_path) if receipt_path.exists() else {}
    previous = next((r for r in prior.get('groups', []) if r['id'] == manifest['id']), None)
    if previous:
        assert previous['questionSHA256'] == manifest['questionSHA256']
        print(manifest['id'], previous['state'], '; no duplicate group or illustration event')
        return
    checked(manifest['questionPath'], manifest['questionSHA256'])
    checked(manifest['qaReport'], manifest['qaReportSHA256'])
    parent, review = load(ROOT/manifest['questionPath']), load(ROOT/manifest['qaReport'])
    members = [c['id'] for c in parent['groupQuestions']]
    assert members == manifest['questionIds'] == review['childCoverage']
    assert set(members) == {c['id'] for c in manifest['childSpecs']}
    assert parent['id'] == min(members, key=lambda s:int(s[2:]))
    # The producer explicitly verified these two views as the same material.
    # Keep both original photos/crops as evidence, but display its common crop.
    aliases = {r['src']: r['commonSrc'] for r in parent.get('groupMetadata', {}).get('commonFigureEquivalentSources', [])}
    for binding in manifest['childSpecs']:
        checked(binding['questionPath'], binding['questionSHA256'])
        if not any(r['id'] == binding['id'] for r in prior.get('items', [])):
            checked(binding['specPath'], binding['specSHA256'])
        derived_review = dict(review, id=binding['id'], questionPath=binding['questionPath'],
            questionSHA256=binding['questionSHA256'], inheritedGroupReview=manifest['qaReport'],
            inheritedGroupReviewSHA256=manifest['qaReportSHA256'], derivedReviewOnly=True)
        review_path = intake/f'{binding["id"]}-inherited-review.json'
        save(review_path, derived_review)
        child_manifest = dict(binding, sourceId=manifest['sourceId'],
            qaReport=str(review_path.relative_to(ROOT)), qaReportSHA256=digest(review_path),
            status='ready', assets=manifest['assets'], readyAt=manifest['readyAt'],
            renderAssetAliases=aliases, inheritedGroupManifest=str(manifest_path.relative_to(ROOT)))
        original_child = next(c for c in parent['groupQuestions'] if c['id'] == binding['id'])
        child_manifest['questionMetadataOverrides'] = {
            key: original_child[key] for key in ('originalQuestionNumber',) if key in original_child}
        child_path = intake/f'{binding["id"]}-manifest.json'
        save(child_path, child_manifest)
        main(child_path)
    receipt = load(directory/'integrated.json')
    rows = {r['id']: r for r in receipt['items'] if r['id'] in members}
    mappings = rows[members[0]]['assetMappings']
    parent = normalize(rewrite(parent, mappings))
    parent['addedAt'] = rows[members[0]]['metadataOverrides']['addedAt']
    parent['groupQuestions'] = [load(ROOT/'docs/complete-questions'/f'{qid}.json') for qid in members]
    revision = hashlib.sha256(json.dumps(sorted(members), separators=(',', ':')).encode()).hexdigest()
    with locked(ROOT):
        save(ROOT/'docs/complete-questions'/f'{parent["id"]}.json', parent)
        groups = load(ROOT/'docs/question-groups.json')
        assert parent['id'] not in groups, 'Do not silently replace an existing group'
        groups[parent['id']] = dict(members=members, displayOrder=members, revision=revision)
        save(ROOT/'docs/question-groups.json', groups)
        receipt = load(directory/'integrated.json')
        receipt.setdefault('groups', []).append(dict(id=parent['id'], originalQuestionIds=members,
            questionSHA256=manifest['questionSHA256'], producerManifest=str(manifest_path.relative_to(ROOT)),
            membershipRevision=revision, state='added_pending_curate_and_integrated',
            renderAssetAliases=aliases, originalEvidencePreserved=True))
        save(directory/'integrated.json', receipt)
    save(intake/f'{manifest["id"]}-published-parent.json', parent)
    print(parent['id'], 'group catalog added; complete original children and both comics retained')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--id', help='Select a ready item from a source-level manifest.')
    parser.add_argument('--finalize', action='store_true', help='After the batch curator build, record basic technical checks and the integration event.')
    args = parser.parse_args()
    path = args.manifest.resolve()
    if load_item(path, args.id).get('childSpecs'):
        grouped(path, args.id, args.finalize)
    else:
        (finish if args.finalize else main)(path, args.id)
