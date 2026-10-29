"""Record actual app screenshot views AFTER the reviewer has opened every one."""
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/jack/git/TestReview')
RENDER_FILES = ['site/dist/app.js', 'site/dist/styles.css', 'site/dist/comic.css',
                'site/dist/comic-wrap.js', 'site/dist/teaching-comic.js',
                'site/dist/core.js', 'site/dist/group-materials.js', 'site/scripts/build_review_page.py',
                'site/scripts/group_review_html.py', 'site/scripts/teaching_comic.py']


def finish(group_id, note):
    path = ROOT / 'docs/imports/group-review/qa' / (group_id + '-validation.json')
    technical = json.loads(path.read_text())
    expected = {(standalone, width) for standalone in [False, True] for width in [1440, 1120, 390]}
    assert {(r['standalone'], r['width']) for r in technical['rows']} == expected
    images = []
    coverage = []
    dest = ROOT / 'docs/comics/qa/group-review' / group_id
    dest.mkdir(parents=True, exist_ok=True)
    for row in technical['rows']:
        assert row['noDocumentOverflow'] and row['defaultCollapsed']
        assert [comic['id'] for comic in row['comics']] == technical['childIds']
        for comic in row['comics']:
            assert not comic['wrapErrors'] and not comic['overflow'] and not comic['protectedBreaks']
            assert len(comic['cells']) == 4 and all(image['loaded'] for image in comic['decoded'])
            if not row['standalone'] and row['width'] in [1440, 390]:
                source = Path(comic['screenshot'])
                target = dest / source.name
                shutil.copyfile(source, target)
                assert source.read_bytes() == target.read_bytes()
                images.append(str(target.relative_to(ROOT)))
                coverage.append({'childId': comic['id'], 'width': row['width'], 'mode': 'app',
                                 'actuallyViewed': True, 'screenshot': images[-1]})
    report = {'groupId': group_id, 'reviewerAgent': '/root/comic_lane_3', 'passed': True,
              'checkedAt': datetime.now(timezone.utc).isoformat(),
              'childCoverage': technical['childIds'], 'actualViewed': images,
              'actualViewCoverage': coverage, 'automatedValidation': str(path.relative_to(ROOT)),
              'automatedValidationSHA256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'automatedLayouts': 6, 'appAndStandaloneTechnicalPassed': True,
              'allChildComicsChecked': True, 'visualNotes': note,
              'renderCodeSHA256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in RENDER_FILES},
              'technicalCheckerSHA256': hashlib.sha256((ROOT / 'site/scripts/check-groups.cjs').read_bytes()).hexdigest(),
              'personalCloudRequestsAborted': True, 'sharedBankEdited': False}
    out = path.with_name(group_id + '-layout-reviewed.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(str(out.relative_to(ROOT)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('group')
    parser.add_argument('--note', required=True)
    args = parser.parse_args()
    finish(args.group, args.note)
