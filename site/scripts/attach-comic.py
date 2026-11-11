"""Attach reviewed comic specs as native HTML data; does not mark visual review complete."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from optimized_assets import optimize_payload

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from monitor.comic_execution import assert_work_allowed

def retained_figures(qid, override, baseline):
    """A new comic must not erase official reference material in the base row."""
    figures = override.get('explanationFigures', baseline)
    return [figure for figure in figures if figure['src'] != f'assets/comics/{qid}.png']

def attach(qid):
    assert_work_allowed(ROOT, qid)
    spec_path = ROOT / 'docs/comics' / (qid + '.json')
    spec = json.loads(spec_path.read_text())
    assert spec['id'] == qid and len(spec['panels']) == 3
    published = {}
    def publish_image(relative, label):
        if relative in published:
            return published[relative]
        art_path = ROOT / relative
        art = art_path.read_bytes()
        suffix = art_path.suffix.lower()
        assert suffix in ('.png', '.svg', '.webp', '.jpg', '.jpeg'), 'Use a raster illustration or an authored SVG diagram.'
        asset = f'assets/comics/{qid}-{label}-{hashlib.sha256(art).hexdigest()[:10]}{suffix}'
        (ROOT / 'site/dist' / asset).write_bytes(art)
        published[relative] = optimize_payload({'art': asset})['art']
        return published[relative]
    asset = publish_image(spec['art'], 'art')
    panels = []
    for index, panel in enumerate(spec['panels'], 1):
        item = {k: panel[k] for k in ('heading', 'text', 'alt', 'caption', 'diagram') if k in panel}
        if panel.get('image'):
            item['image'] = publish_image(panel['image'], f'panel-{index}-art')
        panels.append(item)
    fourth = {k: spec['fourth'][k] for k in ('answer', 'points')}
    if spec['fourth'].get('image'):
        fourth.update(image=publish_image(spec['fourth']['image'], 'panel-4-art'),
                      alt=spec['fourth'].get('alt', '本題結論圖解'))
    comic = {'title': spec['title'], 'art': asset, 'panels': panels, 'fourth': fourth}
    # Match the browser import schema: a single character cannot wrap inside.
    words = list(dict.fromkeys(word.strip() for word in spec.get('protectedWords', [])
        if isinstance(word, str) and len(word.strip()) >= 2 and len(word) <= 40
        and not re.search(r'[\x00-\x1f]', word)))[:50]
    if words:
        comic['protectedWords'] = words
    override_path = ROOT / 'docs/complete-questions' / (qid + '.json')
    override = json.loads(override_path.read_text()) if override_path.exists() else {}
    # A question without an override can still have official explanation figures.
    baseline = []
    if 'explanationFigures' not in override:
        data = json.loads((ROOT/'site/dist/data.json').read_text())
        baseline = next((q.get('explanationFigures', []) or []
                         for q in data['questions'] if q['id'] == qid), [])
    override['explanationFigures'] = retained_figures(qid, override, baseline)
    if override.get('groupQuestions'):
        child = next(child for child in override['groupQuestions'] if child['id'] == qid)
        child['teachingComic'] = comic
        # A group renders one lesson per original, never another parent lesson.
        override['teachingComic'] = None
    else:
        override['teachingComic'] = comic
    override_path.write_text(json.dumps(override, ensure_ascii=False, indent=2) + '\n')
    groups_path = ROOT/'docs/question-groups.json'
    groups = json.loads(groups_path.read_text()) if groups_path.exists() else {}
    parent_id = next((parent for parent, group in groups.items()
                      if parent != qid and qid in group['members']), None)
    if parent_id:
        parent_path = ROOT/'docs/complete-questions'/(parent_id+'.json')
        parent = json.loads(parent_path.read_text())
        child = next(child for child in parent['groupQuestions'] if child['id'] == qid)
        child['teachingComic'] = comic
        parent['teachingComic'] = None
        parent_path.write_text(json.dumps(parent, ensure_ascii=False, indent=2) + '\n')
    spec.update(nativeArt=asset, layoutVersion='native-four-images-v7' if all(p.get('image') for p in panels) and fourth.get('image') else 'native-fluid-v6',
                nativeLayout={'width': '100%', 'height': 'auto', 'artWidth': 180,
                              'fontSize': 14, 'equalColumnWidths': True, 'equalHeightWithinRow': True,
                              'independentRowHeights': True, 'singleColumnNaturalHeight': True,
                              'narrowSingleColumn': True})
    for key in ('displayMaxWidth', 'displayMaxHeight'):
        spec.pop(key, None)
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
    print(qid, asset)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ids', nargs='+')
    for qid in parser.parse_args().ids:
        if not qid.startswith('q-') or not qid[2:].isdigit():
            parser.error('Use stable q-NNN identifiers.')
        attach(qid)
