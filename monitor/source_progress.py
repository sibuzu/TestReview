"""Update one source by identity, never by list position or a reused loop value."""
from .comic_pipeline import load, save


def update_source(root, order, metadata, *, source_url, aliases=()):
    order = int(order)
    path = root / 'docs/imports/more-gemini-progress.json'
    data = load(path)
    matches = [row for row in data['sources'] if row.get('order') == order]
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one source at order {order}')
    row = matches[0]
    if row.get('url') not in {source_url, *aliases}:
        raise ValueError('Source URL does not match the selected order or aliases')
    expected_key = f'gemini{order:03}'
    if metadata.get('sourceKey', expected_key) != expected_key:
        raise ValueError('Source key and order disagree')
    if 'order' in metadata and metadata['order'] != order:
        raise ValueError('Cannot change a source order')
    if 'url' in metadata and metadata['url'] != row['url']:
        raise ValueError('Preserve the original source URL; store aliases separately')
    row.update(metadata)
    save(path, data)
    return row
