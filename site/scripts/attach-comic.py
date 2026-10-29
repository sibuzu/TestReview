"""Attach reviewed comic specs as native HTML data; does not mark visual review complete."""
import argparse
import hashlib
import json
from pathlib import Path
from optimized_assets import optimize_payload

ROOT = Path(__file__).resolve().parents[2]

def attach(qid):
    spec_path = ROOT / 'docs/comics' / (qid + '.json')
    spec = json.loads(spec_path.read_text())
    assert spec['id'] == qid and len(spec['panels']) == 3
    art_path = ROOT / spec['art']
    art = art_path.read_bytes()
    assert art_path.suffix.lower() in ('.png', '.svg'), 'Use a PNG illustration or an authored SVG diagram.'
    asset = f'assets/comics/{qid}-art-{hashlib.sha256(art).hexdigest()[:10]}{art_path.suffix.lower()}'
    (ROOT / 'site/dist' / asset).write_bytes(art)
    asset = optimize_payload({'art': asset})['art']
    comic = {
        'title': spec['title'], 'art': asset,
        'panels': [{k: p[k] for k in ('heading', 'text', 'alt')} for p in spec['panels']],
        'fourth': {k: spec['fourth'][k] for k in ('answer', 'points')},
    }
    if spec.get('protectedWords'):
        comic['protectedWords'] = spec['protectedWords']
    override_path = ROOT / 'docs/complete-questions' / (qid + '.json')
    override = json.loads(override_path.read_text()) if override_path.exists() else {}
    # Replace only our previous flattened comic; retain other explanation figures.
    override['explanationFigures'] = [f for f in override.get('explanationFigures', [])
                                     if f['src'] != f'assets/comics/{qid}.png']
    override['teachingComic'] = comic
    override_path.write_text(json.dumps(override, ensure_ascii=False, indent=2) + '\n')
    spec.update(nativeArt=asset, layoutVersion='native-fluid-v6',
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
