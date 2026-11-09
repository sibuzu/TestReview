"""Audit the complete 47-original goal against published content and evidence.

Read-only except for this goal's audit report. A passing report requires actual
published comics, both QA stages and stable original content; queued work fails.
Run: python3 docs/comics/remaining-20261109/audit.py [--partial]
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[3]
DIRECTORY = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def existing(path):
    target = ROOT / path
    return target.is_file()


def audit():
    plan = read(DIRECTORY / 'plan.json')
    baseline = read(DIRECTORY / 'original-content-baseline.json')
    expected_answers = read(DIRECTORY / 'expected-answers.json')['records']
    outside_document = read(DIRECTORY / 'outside-scope-baseline.json')
    outside_baseline = outside_document['records']
    data = read(ROOT / 'site/dist/data.json')
    asset_map = read(ROOT / 'site/asset-map.json')
    def referenced_assets(value):
        if isinstance(value, str) and value.startswith('assets/'):
            yield value
        elif isinstance(value, dict):
            for child in value.values():
                yield from referenced_assets(child)
        elif isinstance(value, list):
            for child in value:
                yield from referenced_assets(child)
    data_assets = set(referenced_assets(data))
    missing_assets = sorted(p for p in data_assets if not existing('site/dist/' + p))
    all_originals = [c for q in data['questions'] for c in (q.get('groupQuestions') or [q])]
    originals = {c['id']: c for c in all_originals}
    canonical_hash = lambda value: hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    derived = set(outside_document.get('excludedDerivedFields', []))
    outside_changes = [qid for qid, digest in outside_baseline.items()
                       if qid not in originals
                       or canonical_hash({k: v for k, v in originals[qid].items()
                                          if k not in derived}) != digest]
    derived_only_changes = [qid for qid, digest in outside_document['fullRecordHashes'].items()
                            if qid in originals and qid not in outside_changes
                            and canonical_hash(originals[qid]) != digest]
    group_coverage = {c['id']: [member['id'] for member in q['groupQuestions']
                              if member['id'] in plan['questionIds']]
                      for q in data['questions'] if q.get('groupQuestions')
                      for c in q['groupQuestions'] if c['id'] in plan['questionIds']}
    # A final sibling check can prove both comics are present in the shared
    # parent page. Each original must still have its own six layout results.
    group_reports = {}
    for qid in group_coverage:
        path = ROOT / 'docs/comics' / (qid + '-validation.json')
        if path.is_file():
            group_reports[qid] = (str(path.relative_to(ROOT)), read(path).get('results', []))
    entries = {e['id']: e for e in read(ROOT / 'docs/comics/progress.json')['entries']}
    jobs = read(ROOT / 'docs/comics/pipeline.json')['jobs']
    rows = []
    for qid in plan['questionIds']:
        errors = []
        group_evidence = set()
        def require(condition, reason):
            if not condition:
                errors.append(reason)
        question = originals.get(qid, {})
        require(bool(question), 'original missing from published bank')
        require(entries.get(qid, {}).get('state') == 'complete', 'comic not complete')
        for key, value in baseline['records'][qid].items():
            require(question.get(key) == value, 'original content changed: ' + key)
        for key, value in expected_answers[qid]['fields'].items():
            require(question.get(key) == value, 'verified answer/student record changed: ' + key)
        comic = question.get('teachingComic') or {}
        require(len(comic.get('panels', [])) == 3 and bool(comic.get('fourth')),
                'published four-panel comic missing')
        require(bool(comic.get('art')) and existing('site/dist/' + comic.get('art', '')),
                'published shared asset missing')
        require(str(comic.get('art', '')).startswith('assets/comics/')
                and Path(comic.get('art', '')).suffix.lower() in {'.webp', '.svg'},
                'shared WebP/SVG publication policy not satisfied')
        require(not question.get('explanationFigures'), 'source AI explanation figure remains')
        spec_path = ROOT / 'docs/comics' / (qid + '.json')
        spec = read(spec_path) if spec_path.is_file() else {}
        require(spec.get('id') == qid, 'editable spec missing')
        require(spec.get('sourceGeneratedArtUsed') is False, 'new art provenance unverified')
        require(spec.get('visualChecked') is True, 'producer visual review missing')
        require(spec.get('originalMaterialsChecked') is True, 'original material review missing')
        material_paths = list(spec.get('originalMaterials') or [])
        original_checked = spec.get('originalChecked') or {}
        material_paths.extend(original_checked.get('images') or [])
        if original_checked.get('path'):
            material_paths.append(original_checked['path'])
        require(bool(material_paths) and all(existing(p) for p in material_paths),
                'reviewed original material files missing')
        published_keys = ('heading', 'text', 'alt', 'caption', 'diagram')
        expected_panels = [{k: p[k] for k in published_keys if k in p}
                           for p in spec.get('panels', [])]
        require(comic.get('panels') == expected_panels,
                'published panel content differs from reviewed editable spec')
        require(comic.get('fourth') == {k: spec.get('fourth', {}).get(k)
                                       for k in ('answer', 'points')},
                'published conclusion differs from reviewed editable spec')
        selected = re.search(r'(?<![A-Za-z])([ABCD])(?![A-Za-z])',
                             comic.get('fourth', {}).get('answer', ''))
        if selected and question.get('correctOption') in {'A', 'B', 'C', 'D'}:
            require(selected.group(1) == question['correctOption'],
                    'comic conclusion choice contradicts the verified original answer')
        art = ROOT / spec.get('art', '__missing_art__')
        require(art.is_file(), 'editable artwork missing')
        if art.is_file() and spec.get('artSHA256'):
            require(hashlib.sha256(art.read_bytes()).hexdigest() == spec['artSHA256'],
                    'editable artwork changed after review')
        png_size = None
        if art.is_file() and art.suffix.lower() == '.png':
            raw = art.read_bytes()
            require(raw.startswith(b'\x89PNG\r\n\x1a\n'), 'raw raster format is not PNG')
            if raw.startswith(b'\x89PNG\r\n\x1a\n'):
                png_size = struct.unpack('>II', raw[16:24])
            provenance = next((r for r in asset_map.values()
                               if r.get('web') == comic.get('art')), {})
            require(provenance.get('originalSHA256') == hashlib.sha256(raw).hexdigest()
                    and provenance.get('mode') == 'quality88-original-dimensions',
                    'WebP provenance/quality policy does not match reviewed raw art')
            require(bool(provenance.get('originalArchive'))
                    and existing(provenance.get('originalArchive', '')),
                    'original raster archive missing')
        for field, stage in [('previewValidation', 'isolated'), ('validationFile', 'formal')]:
            evidence = ROOT / spec.get(field, '__missing_' + field + '__')
            require(evidence.is_file(), stage + ' QA evidence missing')
            if not evidence.is_file():
                continue
            checked = read(evidence).get('results', [])
            widths = {r.get('viewport', r.get('width')) for r in checked}
            require({1440, 1120, 390}.issubset(widths), stage + ' three-width coverage missing')
            if stage == 'formal':
                combinations = {(r.get('standalone'), r.get('viewport', r.get('width')))
                                for r in checked}
                require({(view, width) for view in (False, True)
                         for width in (1440, 1120, 390)}.issubset(combinations),
                        'app/standalone three-width coverage missing')
            for result in checked:
                if stage == 'formal' and png_size:
                    require(bool(result.get('artImages'))
                            and all((i.get('width'), i.get('height')) == png_size
                                    for i in result['artImages']),
                            'published raster dimensions differ from original')
                if stage == 'formal' and qid in group_coverage:
                    expected_group = set(group_coverage[qid])
                    covered = False
                    for member in group_coverage[qid]:
                        path, evidence_results = group_reports.get(member, ('', []))
                        if any(r.get('standalone') == result.get('standalone')
                               and r.get('viewport') == result.get('viewport')
                               and expected_group.issubset(r.get('groupComicIds') or [])
                               for r in evidence_results):
                            covered = True
                            group_evidence.add(path)
                    require(covered, 'complete group comic coverage not demonstrated in both views')
                require(not result.get('overflow') and not result.get('docOverflow')
                        and not result.get('wrapErrors') and not result.get('protectedBreaks'),
                        stage + ' layout failure recorded')
                require(bool(result.get('screenshot')) and existing(result.get('screenshot', '')),
                        stage + ' rendered screenshot missing locally')
        review = spec.get('rootReview') or {}
        require(review.get('visualChecked') is True
                and review.get('desktopMobileActuallyViewed') is True,
                'formal visual review missing')
        actual_viewed = review.get('screenshots') or review.get('actualViewed') or []
        require(len(set(actual_viewed)) >= 4 and all(existing(p) for p in actual_viewed),
                'formal desktop/mobile visual evidence missing locally')
        latest = next((j for j in reversed(jobs) if j['id'] == qid), {})
        require(latest.get('state') == 'integrated' and latest.get('decision') == 'complete',
                'verified integration event missing')
        require(bool(latest.get('integrationEventId')), 'stable integration event ID missing')
        rows.append(dict(id=qid, passed=not errors, errors=errors,
                         state=entries.get(qid, {}).get('state'),
                         integrationEventId=latest.get('integrationEventId'),
                         groupCoverageEvidence=sorted(group_evidence)))
    event_ids = [r['integrationEventId'] for r in rows if r['integrationEventId']]
    unique_scope = len(set(plan['questionIds'])) == 47
    unique_events = len(set(event_ids)) == len(event_ids)
    report = dict(checkedAt=datetime.now(timezone.utc).isoformat(),
                  passed=all(r['passed'] for r in rows) and len(rows) == 47
                         and unique_scope and unique_events,
                  scopeOriginals=len(rows), fullyVerified=sum(r['passed'] for r in rows),
                  uniqueScopeIds=unique_scope, uniqueIntegrationEvents=unique_events,
                  publishedPages=len(data['questions']), publishedOriginals=len(originals),
                  revision=data['revision'], results=rows)
    require_counts = (len(data['questions']) == baseline['totalPages']
                      and len(originals) == len(all_originals) == 925)
    report['originalCountsPreserved'] = require_counts
    report['outsideScopeRecordsPreserved'] = len(outside_baseline) - len(outside_changes)
    report['outsideScopeChanges'] = outside_changes
    report['outsideScopeDerivedNavigationChanges'] = derived_only_changes
    report['dataAssetReferences'] = len(data_assets)
    report['missingDataAssets'] = missing_assets
    report['passed'] = report['passed'] and require_counts and not outside_changes and not missing_assets
    (DIRECTORY / 'completion-audit.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--partial', action='store_true', help='Report incomplete work without failing.')
    args = parser.parse_args()
    report = audit()
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if args.partial or report['passed'] else 1)
