"""Root-only publication of a checked priority-source transcription draft."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from monitor.comic_pipeline import locked, load, save, update_display


def publish(qid):
    plan = load(ROOT/'docs/comics/priority-source-6ae2305b.json')
    row = next(q for q in plan['questions'] if q['id']==qid)
    question = load(ROOT/row['draftPath'])
    # Acquisition provenance stays in the frozen draft and source plan; the
    # public question schema contains only fields supported by the reader.
    for key in ('originalMaterials', 'sourceMessageIndex'):
        question.pop(key, None)
    assert question['id']==qid and question['sourceId']==plan['sourceId']
    assert question['subject']==row['subject'] and question['date']==row['date']
    for key in ('question', 'answer', 'explanation', 'title', 'contentStatus'):
        assert question.get(key), f'Missing {key}'
    assert question['contentStatus']=='完整原題'
    assert not question.get('explanationFigures'), 'Source AI figures are excluded for this priority source.'
    assets = question.get('images', []) + [f['src'] for f in question.get('questionFigures', [])]
    assert assets and all((ROOT/'site/dist'/asset).is_file() for asset in assets)
    with locked(ROOT):
        path = ROOT/'docs/additional-questions.json'
        questions = load(path)
        existing = next((q for q in questions if q['id']==qid), None)
        if existing:
            # Surface substantive draft changes instead of silently replacing published text.
            keys = ('question','answer','explanation','passage','tables','correctOption')
            assert all(existing.get(k)==question.get(k) for k in keys), 'Published transcription changed; inspect before replacing.'
        else:
            questions.append(question)
            save(path, questions)
        path = ROOT/'docs/comics/progress.json'
        progress = load(path)
        entry = next(e for e in progress['entries'] if e['id']==qid)
        entry['title'] = question['title']
        entry['questionPublished'] = True
        save(path, progress)
        path = ROOT/'docs/comics/pipeline.json'
        pipeline = load(path)
        for job in pipeline['jobs']:
            if job['id']==qid:
                job['title'] = question['title']
        save(path, pipeline)
        update_display(ROOT, pipeline)
        path = ROOT/'docs/imports/more-gpt-progress.json'
        imports = load(path)
        source = next(s for s in imports['sources'] if s['url']==plan['url'])
        source['questionIds'] = [r['id'] for r in plan['questions'] if any(q['id']==r['id'] for q in questions)]
        save(path, imports)
    print(qid, question['title'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ids', nargs='+')
    for qid in parser.parse_args().ids:
        publish(qid)
