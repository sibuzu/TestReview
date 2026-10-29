#!/usr/bin/env python3
"""Rebuildable local search metadata. Never writes the published question bank."""
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
VERSION = 2


def normalized(text):
    # Preserve case, punctuation, powers and subscripts: they can change a problem.
    text = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', str(text or ''))).strip()
    return re.sub(r'(?<=[\u3400-\u9fff]) (?=[\u3400-\u9fff])', '', text)


def digest(text):
    return hashlib.sha256(normalized(text).encode()).hexdigest()


def json_text(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def stem_text(question):
    text = question.get('question', '')
    choices = [{'label': o.get('label', ''), 'text': o.get('text', '')}
               for o in question.get('optionAnalysis', [])]
    # Most records already print all choices in question. Do not make the
    # existence of an optional explanatory table change their identity.
    if choices and not all(normalized(o['text']) in normalized(text) for o in choices):
        text += '\n'+json_text(choices)
    return text


def input_paths(root):
    required = [root/'site/dist/data.json']
    patterns = ['docs/imports/*-progress.json', 'docs/acquisition/*.json',
                'docs/sources/*.json', 'docs/imports/new-gemini/*/manifest.json',
                'docs/imports/new-gemini/*/integrated.json',
                'docs/imports/new-gemini/*/group*.json',
                'docs/imports/new-gemini/*/questions/*.json',
                'docs/question-aliases.json', 'docs/question-groups.json', 'docs/comics/progress.json',
                'monitor/confirmations.json', 'monitor/import-control.json']
    return sorted(set(required + [p for pattern in patterns for p in root.glob(pattern)]))


def fingerprint(root):
    return [[str(p.relative_to(root)), p.stat().st_size, p.stat().st_mtime_ns]
            for p in input_paths(root)]


def canonical(qid, aliases):
    seen = set()
    while qid in aliases:
        if qid in seen:
            raise ValueError('Question alias cycle: '+qid)
        seen.add(qid)
        qid = aliases[qid]
    return qid


SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE sources(id TEXT PRIMARY KEY, title TEXT, url TEXT, platform TEXT,
 batch TEXT, source_order INTEGER, state TEXT, created_date TEXT, archive_path TEXT,
 transcript TEXT);
CREATE TABLE source_urls(source_id TEXT REFERENCES sources(id), url TEXT,
 PRIMARY KEY(source_id,url));
CREATE INDEX source_url_lookup ON source_urls(url);
CREATE TABLE passages(hash TEXT PRIMARY KEY, text TEXT NOT NULL);
CREATE TABLE records(key TEXT PRIMARY KEY, kind TEXT, id TEXT, published_id TEXT,
 title TEXT, subject TEXT, volume TEXT, chapter TEXT, date TEXT, state TEXT,
 comic_state TEXT, source_id TEXT REFERENCES sources(id), passage_hash TEXT REFERENCES passages(hash),
 question TEXT, answer TEXT, explanation TEXT, stem_hash TEXT, options_json TEXT,
 figures_json TEXT, images_json TEXT, file_path TEXT);
CREATE INDEX stem_lookup ON records(stem_hash);
CREATE INDEX material_lookup ON records(passage_hash);
CREATE INDEX record_ids ON records(id);
CREATE TABLE record_sources(record_key TEXT REFERENCES records(key),
 source_id TEXT REFERENCES sources(id), relation TEXT, PRIMARY KEY(record_key,source_id));
CREATE TABLE aliases(alias TEXT PRIMARY KEY, question_id TEXT NOT NULL);
CREATE TABLE question_groups(key TEXT PRIMARY KEY, title TEXT, published_id TEXT,
 passage_hash TEXT REFERENCES passages(hash), file_path TEXT);
CREATE TABLE group_members(group_key TEXT REFERENCES question_groups(key),
 record_key TEXT REFERENCES records(key), original_number TEXT,
 PRIMARY KEY(group_key,record_key));
CREATE TABLE confirmations(id TEXT PRIMARY KEY, state TEXT, title TEXT,
 question_id TEXT, source_key TEXT, question_url TEXT, source_url TEXT, detail_json TEXT);
CREATE VIRTUAL TABLE record_fts USING fts5(key UNINDEXED,title,question,passage,explanation, tokenize='trigram');
CREATE VIRTUAL TABLE source_fts USING fts5(id UNINDEXED,title,transcript, tokenize='trigram');
"""


def populate(db, files):
    data = files['site/dist/data.json']
    aliases = dict(files.get('docs/question-aliases.json', {}))
    for parent,group in files.get('docs/question-groups.json',{}).items():
        for member in group['members']:
            if member!=parent:aliases[member]=parent
    published = {q['id']: q for q in data['questions']}
    comics = {e['id']: e['state'] for e in files.get('docs/comics/progress.json', {}).get('entries', [])}
    source_map = {s['id']: dict(s) for s in data.get('sources', [])}
    progress_links = []
    for batch, path, prefix in [('todo', 'todo-progress.json', 'src-'),
                                ('gpt', 'more-gpt-progress.json', 'src-more-'),
                                ('gemini', 'more-gemini-progress.json', 'src-gemini-more-')]:
        for s in files.get('docs/imports/'+path, {}).get('sources', []):
            sid = s.get('id') or prefix + (str(s['order']) if batch == 'todo' else f'{s["order"]:03d}')
            source_map.setdefault(sid, {})
            source_map[sid].update(s, batch=batch, source_order=s['order'])
            for qid in s.get('questionIds', s.get('completeQuestionIds', [])):
                progress_links.append((canonical(qid, aliases), sid))
    receipts = {}
    import_control = files.get('monitor/import-control.json', {})

    def cancelled_source(key):
        match = re.fullmatch(r'gemini(\d+)', key or '')
        return bool(match and import_control.get('lastAllowedSourceOrder') is not None and
                    int(match[1]) > import_control['lastAllowedSourceOrder'])
    for path, receipt in files.items():
        if path.startswith('docs/imports/new-gemini/') and path.endswith('/integrated.json'):
            for mapping in receipt.get('mappings', []):
                qid = canonical(mapping.get('questionId'), aliases)
                if qid in published:
                    receipts[mapping['candidateId']] = qid
    skipped_drafts = set()
    for path, obj in files.items():
        if not path.startswith('docs/imports/new-gemini/') or not isinstance(obj, dict):
            continue
        if path.endswith('/manifest.json'):
            for original in obj.get('userSkippedOriginalKeys', []):
                skipped_drafts.add((obj.get('sourceKey'), str(original)))
            for skipped in obj.get('skippedThisBatch', []):
                skipped_drafts.add((obj.get('sourceKey'), str(skipped.get('originalQuestionKey'))))
        if obj.get('type') == 'shared_passage_question_group' and obj.get('groupKey') in receipts:
            for member in obj.get('subQuestions', []):
                receipts[member['candidateId']] = receipts[obj['groupKey']]
    for sid, s in source_map.items():
        if s.get('batch') == 'gemini':
            order = s['source_order']
            for p in (f'docs/acquisition/gemini-{order:03d}.json', f'docs/acquisition/new-gemini{order:03d}.json'):
                if p in files:
                    report = files[p]
                    for key in ('title', 'createdDate', 'archive'):
                        if report.get(key):
                            s[key] = report[key]
                    s['aliases'] = sorted(set(s.get('aliases', []) + report.get('aliases', [])))
        token = s.get('url', '').rstrip('/').rsplit('/', 1)[-1]
        candidates = [s.get('archive'), f'docs/sources/gemini-{token}.json',
                      f'docs/sources/{token}-rendered.json', f'docs/sources/{token}.json']
        archive = next((p for p in candidates if p and p in files), '')
        archived = files.get(archive, {})
        transcript = (archived.get('text') if isinstance(archived, dict) else '') or s.get('transcript') or s.get('content') or ''
        if not isinstance(transcript, str):
            transcript = json_text(transcript)
        db.execute('INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?)',
                   (sid, s.get('title', ''), s.get('url', ''), s.get('platform', ''),
                    s.get('batch', ''), s.get('source_order'), s.get('state', s.get('status', '')),
                    s.get('createdDate', s.get('date', '')), archive, transcript))
        for url in set([s.get('url', '')] + s.get('aliases', [])) - {''}:
            db.execute('INSERT OR IGNORE INTO source_urls VALUES (?,?)', (sid, url.rstrip('/')))
        db.execute('INSERT INTO source_fts VALUES (?,?,?)', (sid, s.get('title', ''), transcript))

    def passage(text):
        key = digest(text)
        db.execute('INSERT OR IGNORE INTO passages VALUES (?,?)', (key, text or ''))
        return key

    def add_record(q, kind, path, sid=None, published_parent=None):
        qid = q['id'] if kind in {'published','group_child'} else q['candidateId']
        key = kind+':'+qid
        target = qid if kind == 'published' else published_parent if kind=='group_child' else receipts.get(qid)
        sid = sid or q.get('sourceId')
        if sid not in source_map:
            sid = None
        options = [{'label': o.get('label', ''), 'text': o.get('text', '')} for o in q.get('optionAnalysis', [])]
        stem_hash = digest(stem_text(q))
        state = ('published' if target else 'draft_ready')
        if str(q.get('verification', '')).startswith('待') or q.get('contentStatus') == '待更新':
            state = 'awaiting_confirmation'
        material = q.get('passage', '')
        db.execute('INSERT INTO records VALUES ('+','.join('?' for _ in range(21))+')',
                   (key, kind, qid, target, q.get('title', ''), q.get('subject', ''),
                    q.get('volume', ''), q.get('chapter', ''), q.get('date', ''), state,
                    comics.get(qid if kind=='group_child' else target, 'not_published'), sid, passage(material), q.get('question', ''),
                    q.get('answer', ''), q.get('explanation', ''), stem_hash, json_text(options),
                    json_text({'figures': q.get('questionFigures', []), 'tables': q.get('tables', [])}),
                    json_text(q.get('images', [])), path))
        if sid:
            db.execute('INSERT OR IGNORE INTO record_sources VALUES (?,?,?)', (key, sid, 'primary'))
        db.execute('INSERT INTO record_fts VALUES (?,?,?,?,?)',
                   (key, q.get('title', ''), q.get('question', ''), material,
                    q.get('answer', '')+'\n'+q.get('explanation', '')))
        return key

    for q in published.values():
        add_record(q, 'published', 'site/dist/data.json')
        if q.get('groupQuestions'):
            group_key='published-group:'+q['id']
            db.execute('INSERT INTO question_groups VALUES (?,?,?,?,?)',
                (group_key,q['title'],q['id'],passage(q.get('passage','')),'site/dist/data.json'))
            for child in q['groupQuestions']:
                key=add_record(child,'group_child','site/dist/data.json',published_parent=q['id'])
                db.execute('INSERT INTO group_members VALUES (?,?,?)',
                    (group_key,key,child.get('originalQuestionNumber','')))
                if child.get('sourceId') in source_map:
                    db.execute('INSERT OR IGNORE INTO record_sources VALUES (?,?,?)',
                        ('published:'+q['id'],child['sourceId'],'group_child'))
    for path, q in files.items():
        if '/questions/' in path and path.startswith('docs/imports/new-gemini/') and q.get('candidateId'):
            if cancelled_source(q.get('sourceKey')):
                continue
            if (q.get('sourceKey'), str(q.get('originalQuestionNumber'))) in skipped_drafts:
                continue
            sid = 'src-gemini-more-'+q.get('sourceKey', '').removeprefix('gemini')
            add_record(q, 'draft', path, sid)
            if q.get('sourceUrl') and sid in source_map:
                for url in [q['sourceUrl']] + q.get('sourceAliases', []):
                    db.execute('INSERT OR IGNORE INTO source_urls VALUES (?,?)', (sid, url.rstrip('/')))
    for qid, sid in progress_links:
        if qid in published:
            db.execute('INSERT OR IGNORE INTO record_sources VALUES (?,?,?)', ('published:'+qid, sid, 'curation'))
    for path, manifest in files.items():
        if not (path.startswith('docs/imports/new-gemini/') and path.endswith('/manifest.json')):
            continue
        sid = 'src-gemini-more-'+manifest.get('sourceKey', '').removeprefix('gemini')
        if sid not in source_map:
            continue
        for reused in manifest.get('duplicates', []):
            qid = canonical(reused.get('existingQuestionId'), aliases)
            if qid in published:
                db.execute('INSERT OR IGNORE INTO record_sources VALUES (?,?,?)', ('published:'+qid, sid, 'confirmed_reuse'))
    for path, obj in files.items():
        if not isinstance(obj, dict) or obj.get('type') != 'shared_passage_question_group' or not obj.get('subQuestions'):
            continue
        if cancelled_source(obj.get('sourceKey')):
            continue
        members = obj['subQuestions']
        group_key = obj.get('groupKey') or path
        targets = {receipts.get(q['candidateId']) for q in members}
        target = next(iter(targets)) if len(targets) == 1 and None not in targets else None
        db.execute('INSERT INTO question_groups VALUES (?,?,?,?,?)',
                   (group_key, obj.get('title', group_key), target, passage(obj.get('commonPassage', '')), path))
        for q in members:
            key = 'draft:'+q['candidateId']
            if db.execute('SELECT 1 FROM records WHERE key=?', (key,)).fetchone():
                db.execute('INSERT INTO group_members VALUES (?,?,?)', (group_key, key, q.get('originalQuestionNumber', '')))
    for old in aliases:
        db.execute('INSERT INTO aliases VALUES (?,?)', (old, canonical(old, aliases)))
    confirmation_data = files.get('monitor/confirmations.json', {})
    # Most recent resolved version, then active version wins for the same card ID.
    cards = {c['id']: dict(c, state='resolved') for c in confirmation_data.get('resolved', [])}
    cards.update({c['id']: c for c in confirmation_data.get('requests', [])})
    for c in cards.values():
        db.execute('INSERT INTO confirmations VALUES (?,?,?,?,?,?,?,?)',
                   (c['id'], c.get('state', 'pending'), c.get('title', ''), c.get('questionId'),
                    c.get('sourceKey'), c.get('questionUrl', c.get('url', '')), c.get('sourceUrl', ''), json_text(c)))
    db.execute('INSERT INTO meta VALUES (?,?)', ('revision', str(data.get('revision', ''))))
    db.execute('INSERT INTO meta VALUES (?,?)', ('importState', import_control.get('state', 'active')))


def build(root=ROOT, db_path=None):
    root = Path(root).resolve()
    db_path = Path(db_path or root/'.cache/question-index.sqlite3').resolve()
    if db_path.is_relative_to(root/'site/dist'):
        raise ValueError('Local metadata must stay outside site/dist.')
    before = fingerprint(root)
    files = {p: json.loads((root/p).read_text()) for p, _, _ in before}
    db_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='question-index-', suffix='.sqlite3', dir=db_path.parent)
    os.close(fd)
    try:
        with sqlite3.connect(temporary) as db:
            db.executescript(SCHEMA)
            populate(db, files)
            for key, value in {'version': VERSION, 'inputs': before,
                               'builtAt': datetime.now(timezone.utc).isoformat()}.items():
                db.execute('INSERT INTO meta VALUES (?,?)', (key, json_text(value)))
            db.commit()
            if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('SQLite integrity check failed')
            if db.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Metadata relation check failed')
        if fingerprint(root) != before:
            raise RuntimeError('Inputs changed during indexing; prior index preserved. Retry after the current write.')
        os.replace(temporary, db_path)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return db_path


def connect(path):
    db = sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    return db


def is_stale(db, root):
    metadata = dict(db.execute('SELECT key,value FROM meta'))
    return (json.loads(metadata.get('version', '0')) != VERSION or
            json.loads(metadata.get('inputs', '[]')) != fingerprint(Path(root).resolve()))


def stats(db):
    return {'published': db.execute("SELECT count(*) FROM records WHERE kind='published'").fetchone()[0],
            'drafts': db.execute("SELECT count(*) FROM records WHERE kind='draft'").fetchone()[0],
            'unpublishedDrafts': db.execute("SELECT count(*) FROM records WHERE kind='draft' AND published_id IS NULL").fetchone()[0],
            'sources': db.execute('SELECT count(*) FROM sources').fetchone()[0],
            'groups': db.execute('SELECT count(*) FROM question_groups').fetchone()[0],
            'aliases': db.execute('SELECT count(*) FROM aliases').fetchone()[0],
            'importState': db.execute("SELECT value FROM meta WHERE key='importState'").fetchone()[0],
            'revision': db.execute("SELECT value FROM meta WHERE key='revision'").fetchone()[0]}


def search(db, query, kind='published', subject=None, limit=20):
    terms = query.split()
    if not terms:
        return []
    where, args = [], []
    if kind != 'all':
        where.append('r.kind=?'); args.append(kind)
    if subject:
        where.append('r.subject=?'); args.append(subject)
    if re.fullmatch(r'q-\d+', query):
        alias = db.execute('SELECT question_id FROM aliases WHERE alias=?', (query,)).fetchone()
        where.append('r.id=?'); args.append(alias[0] if alias else query)
    elif query.startswith(('https://', 'http://')):
        where.append('r.key IN (SELECT rs.record_key FROM record_sources rs JOIN source_urls su ON su.source_id=rs.source_id WHERE su.url=?)')
        args.append(query.rstrip('/'))
    elif all(len(t) >= 3 for t in terms):
        where.append('r.key IN (SELECT key FROM record_fts WHERE record_fts MATCH ?)')
        args.append(' AND '.join('"'+t.replace('"', '""')+'"' for t in terms))
    else:
        for term in terms:
            where.append("(r.title||char(10)||r.question||char(10)||p.text||char(10)||r.answer||char(10)||r.explanation) LIKE ? ESCAPE '\\'")
            args.append('%'+term.replace('\\','\\\\').replace('%','\\%').replace('_','\\_')+'%')
    return [dict(r) for r in db.execute(
        'SELECT r.key,r.id,r.published_id,r.kind,r.title,r.subject,r.state,r.comic_state,r.date,r.file_path '
        'FROM records r JOIN passages p ON p.hash=r.passage_hash WHERE '+' AND '.join(where)+
        ' ORDER BY r.date DESC,r.id LIMIT ?', [*args, limit])]


def duplicate_candidates(db, question, limit=10):
    stem = digest(stem_text(question))
    material = digest(question.get('passage', ''))
    exact = []
    for row in db.execute("SELECT id,title,kind,published_id,passage_hash,figures_json FROM records WHERE stem_hash=?", (stem,)):
        exact.append({**dict(row), 'relation': 'same_text_review_images' if row['passage_hash'] == material else 'same_stem_different_material'})
    shared = []
    if normalized(question.get('passage', '')):
        shared = [dict(r) for r in db.execute(
            "SELECT id,title,kind,published_id FROM records WHERE passage_hash=? AND stem_hash<>? LIMIT ?", (material, stem, limit))]
    target = normalized(question.get('question', ''))
    fuzzy = []
    for row in db.execute("SELECT id,title,question,published_id FROM records WHERE kind IN ('published','group_child') AND stem_hash<>?", (stem,)):
        score = difflib.SequenceMatcher(None, target, normalized(row['question']), autojunk=False).ratio()
        if score >= .6:
            fuzzy.append({'id': row['id'], 'title': row['title'], 'published_id':row['published_id'], 'score': round(score, 4)})
    return {'exactTextCandidates': exact[:limit], 'similarStems': sorted(fuzzy, key=lambda r:r['score'], reverse=True)[:limit],
            'sharedMaterialNotDuplicate': shared,
            'policy': 'Candidates only. Compare complete stem, choices, material and diagrams. Shared passage alone is not a duplicate; a real group keeps every subquestion.'}


def search_sources(db, query, limit=20):
    term = '%'+query.replace('\\','\\\\').replace('%','\\%').replace('_','\\_')+'%'
    where = "s.title LIKE ? ESCAPE '\\' OR s.id=? OR u.url LIKE ? ESCAPE '\\'"
    args = [term, query, term]
    terms = query.split()
    if terms and all(len(t) >= 3 for t in terms):
        where += ' OR s.id IN (SELECT id FROM source_fts WHERE source_fts MATCH ?)'
        args.append(' AND '.join('"'+t.replace('"','""')+'"' for t in terms))
    else:
        where += " OR s.transcript LIKE ? ESCAPE '\\'"
        args.append(term)
    return [dict(r) for r in db.execute(
        'SELECT DISTINCT s.id,s.title,s.url,s.state,s.archive_path FROM sources s '
        'LEFT JOIN source_urls u ON u.source_id=s.id WHERE '+where+' ORDER BY s.id LIMIT ?', [*args, limit])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--db', type=Path)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build'); sub.add_parser('status')
    q = sub.add_parser('search'); q.add_argument('query'); q.add_argument('--kind', choices=['published','draft','all'], default='published'); q.add_argument('--subject'); q.add_argument('--limit', type=int, default=20)
    q = sub.add_parser('show'); q.add_argument('id')
    q = sub.add_parser('candidates'); q.add_argument('file', type=Path)
    q = sub.add_parser('source'); q.add_argument('query'); q.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()
    path = args.db or args.root/'.cache/question-index.sqlite3'
    needs_build = not path.exists() or args.command == 'build'
    if not needs_build:
        with connect(path) as db:
            needs_build = is_stale(db, args.root)
    if needs_build:
        build(args.root, path)
    with connect(path) as db:
        if args.command in ('build', 'status'):
            result = {**stats(db), 'path': str(path), 'bytes': path.stat().st_size, 'stale': is_stale(db, args.root)}
        elif args.command == 'search':
            result = search(db, args.query, args.kind, args.subject, args.limit)
        elif args.command == 'candidates':
            candidate = json.loads(args.file.read_text())
            if candidate.get('subQuestions'):
                result = [{'candidateId': q.get('candidateId'), **duplicate_candidates(db, dict(
                    q, passage=q.get('passage') or candidate.get('commonPassage', '')))}
                    for q in candidate['subQuestions']]
            else:
                result = duplicate_candidates(db, candidate)
        elif args.command == 'source':
            result = search_sources(db, args.query, args.limit)
        else:
            alias = db.execute('SELECT question_id FROM aliases WHERE alias=?', (args.id,)).fetchone()
            qid = alias[0] if alias else args.id
            result = []
            for r in db.execute('SELECT r.*,p.text AS passage FROM records r JOIN passages p ON p.hash=r.passage_hash WHERE r.id=?', (qid,)):
                item = dict(r)
                item['sources'] = [dict(s) for s in db.execute('SELECT s.id,s.title,u.url FROM record_sources rs JOIN sources s ON s.id=rs.source_id JOIN source_urls u ON u.source_id=s.id WHERE rs.record_key=?', (r['key'],))]
                item['groups'] = [dict(g) for g in db.execute('SELECT * FROM question_groups WHERE published_id=?', (r['published_id'],))]
                result.append(item)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
