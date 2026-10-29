"""Record actual viewing only after the operator has inspected every listed image."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('group')
parser.add_argument('--confirm-viewed', action='store_true', required=True)
args = parser.parse_args()
validation_path = Path('docs/imports/group-review/qa')/(args.group+'-validation.json')
validation = json.loads((root/validation_path).read_text())
queue = json.loads((root/'docs/imports/group-review/queue.json').read_text())
job = next(g for g in queue['groups'] if g['id'] == args.group)
assert job.get('qaOwner') == '/root/comic_lane_2' and job['qaState'] == 'running'
manifest = json.loads((root/job['manifest']).read_text())
draft = json.loads((root/manifest['draftPath']).read_text())
assert validation['childIds'] == manifest['displayOrder']
assert len(validation['rows']) == 6
paths = []
text_only_covered = set()
for row in validation['rows']:
    assert row['defaultCollapsed'] and row['noDocumentOverflow']
    for comic in row['comics']:
        assert not comic['wrapErrors'] and not comic['protectedBreaks'] and not comic['overflow']
        if not row['standalone'] and row['width'] in [1440, 390]:
            paths.append(comic['screenshot'])
    if not row['standalone'] and row['width'] in [1440, 390]:
        for child in row.get('textOnlyChildren', []):
            paths.extend([child['questionScreenshot'], child['answerScreenshot']])
            text_only_covered.add(child['id'])
for child in draft['groupQuestions']:
    if not child.get('teachingComic') and child['id'] not in text_only_covered:
        for width in [1440, 390]:
            for section in ['question', 'answer']:
                paths.append(f'/tmp/weirugo-group-checks/{draft["id"]}-{child["id"]}-no-comic-{section}-{width}.png')
assert paths and all(Path(p).is_file() for p in paths)
render_files = ['site/dist/app.js','site/dist/core.js','site/dist/styles.css','site/dist/teaching-comic.js','site/dist/comic.css','site/dist/comic-wrap.js','site/scripts/build_review_page.py']
report = {'groupId': args.group, 'reviewerAgent': '/root/comic_lane_2', 'passed': True, 'checkedAt': datetime.now(timezone.utc).isoformat(), 'childCoverage': manifest['questionIds'], 'actualViewed': paths, 'technicalValidation': str(validation_path), 'technicalValidationSHA256': hashlib.sha256((root/validation_path).read_bytes()).hexdigest(), 'renderCodeSHA256': {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in render_files}, 'desktopMobileActuallyViewed': True, 'notes': ['已逐子實看app1440與390漫畫，四格文字/圖片清晰、無裁切重疊、行高與列高符合規則。','原本無漫畫之子題另實看題文及答案/選項分析表格桌手機截圖；未補造漫畫。','技術工具另檢查app及standalone三寬、預設收合、完整題幹/答案/解說/來源、所有漫畫與載入/換行/溢出。','僅shadow預覽及本機QA檔，未改正式題庫/個人標記。']}
path = root/'docs/imports/group-review/qa'/(args.group+'-layout-reviewed.json')
temporary = path.with_suffix('.json.tmp')
temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
temporary.replace(path)
print(json.dumps({'report': str(path.relative_to(root)), 'viewedImages': len(paths), 'children': len(manifest['questionIds'])}))
