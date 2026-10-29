"""Publish shared WebP assets while retaining full-size originals outside Git."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = Path(os.environ.get('WEIRUGO_ORIGINAL_ARCHIVE',
                            str(Path.home() / 'backups/WeiRuGo-original-assets')))


def paths_in(value):
    if isinstance(value, str):
        if value.startswith('assets/'):
            yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from paths_in(child)
    elif isinstance(value, list):
        for child in value:
            yield from paths_in(child)


def remap(value, mapping):
    if isinstance(value, str):
        return mapping.get(value, {}).get('web', value)
    if isinstance(value, list):
        return [remap(child, mapping) for child in value]
    if isinstance(value, dict):
        return {key: remap(child, mapping) for key, child in value.items()}
    return value


def archive_file(path, relative):
    """Never overwrite an earlier original, even if a filename was reused."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    target = ARCHIVE / digest[:16] / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(path, target)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
    return str(target)


def convert(dist, relative):
    source = dist / relative
    if not source.is_file() or source.suffix.lower() != '.png':
        return None
    # Keep logos and original exam scans as supplied. Text-bearing older AI
    # diagrams use lossless WebP; only native wordless scene strips use lossy.
    if not relative.startswith(('assets/comics/', 'assets/explanations/')):
        return None
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    dest = source.with_name(source.stem + '-web.webp')
    temporary = dest.with_suffix('.tmp.webp')
    lossless = '-art-' not in source.name
    subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error',
                    '-y', '-i', str(source), '-c:v', 'libwebp',
                    '-lossless', '1' if lossless else '0', '-quality', '88',
                    '-compression_level', '6', '-threads', '1',
                    str(temporary)], check=True)
    if temporary.stat().st_size >= source.stat().st_size * .95:
        temporary.unlink()
        return None
    temporary.replace(dest)
    return dict(web=dest.relative_to(dist).as_posix(), originalSHA256=digest,
                originalBytes=source.stat().st_size, webBytes=dest.stat().st_size,
                mode='lossless' if lossless else 'quality88-original-dimensions',
                originalArchive=archive_file(source, relative))


def optimize_payload(payload, dist=None, manifest_path=None):
    dist = Path(dist or ROOT / 'site/dist')
    manifest_path = Path(manifest_path or ROOT / 'site/asset-map.json')
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    references = set(paths_in(payload))
    pending = []
    for relative in sorted(references):
        record = manifest.get(relative)
        if record and (dist / record['web']).exists():
            if not (dist / relative).exists() or hashlib.sha256((dist / relative).read_bytes()).hexdigest() == record['originalSHA256']:
                continue
        pending.append(relative)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for relative, record in zip(pending, pool.map(lambda p: convert(dist, p), pending)):
            if record:
                manifest[relative] = record
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = manifest_path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(manifest_path)
    return remap(payload, manifest)


def prune_unreferenced(dist, payload):
    """Archive unused published assets; keep every referenced file and logo."""
    import re
    referenced = set(paths_in(payload))
    # Also honor paths in scripts, styles, standalone pages and source pages.
    for path in dist.rglob('*'):
        if path.is_file() and path.suffix in ('.html', '.css', '.js', '.txt', '.svg'):
            referenced.update(re.findall(r'assets/[a-zA-Z0-9_./-]+', path.read_text(errors='replace')))
    referenced.add('assets/weirugo-logo.png')
    removed = []
    for path in sorted((dist / 'assets').rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(dist).as_posix()
        if relative in referenced:
            continue
        size = path.stat().st_size
        backup = archive_file(path, relative)
        path.unlink()
        removed.append(dict(path=relative, bytes=size, archive=backup))
    return removed


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist', type=Path, default=ROOT / 'site/dist')
    parser.add_argument('--manifest', type=Path, default=ROOT / 'site/asset-map.json')
    parser.add_argument('--prune', action='store_true')
    args = parser.parse_args()
    data = args.dist / 'data.json'
    payload = optimize_payload(json.loads(data.read_text()), args.dist, args.manifest)
    # Asset paths contribute to the data revision as well as question content.
    payload['revision'] = 'assets-' + hashlib.sha256(json.dumps(
        {k:v for k,v in payload.items() if k != 'revision'}, ensure_ascii=False,
        sort_keys=True).encode()).hexdigest()[:16]
    data.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    subprocess.run([os.sys.executable, str(ROOT / 'site/scripts/build_review_page.py')],
                   env={**os.environ, 'WEIRUGO_DIST': str(args.dist)}, check=True)
    removed = prune_unreferenced(args.dist, payload) if args.prune else []
    report = dict(at=datetime.now(timezone.utc).isoformat(), dist=str(args.dist),
                  questionCount=len(payload['questions']), removed=removed,
                  archivedBytes=sum(row['bytes'] for row in removed))
    (args.manifest.parent / 'asset-optimization-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'removed'}))
