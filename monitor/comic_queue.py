"""Choose comics by the smallest completed-count squared / subject total."""
from collections import Counter
from fractions import Fraction

SETTLED = {'complete', 'existing_ai', 'not_suitable'}
SUBJECT_ORDER = ['Chinese', 'English', 'Math', 'Biology', 'Physics-Chemistry', 'Earth', 'History', 'Geography', 'Civics']


def subject_stats(entries):
    totals = Counter(e['subject'] for e in entries)
    unfinished = Counter(e['subject'] for e in entries if e['state'] not in SETTLED)
    available = Counter(e['subject'] for e in entries if e['state'] == 'queued')
    return sorted(({'subject': subject, 'total': total,
                    'completed': total - unfinished[subject],
                    'remaining': unfinished[subject], 'available': available[subject],
                    'priorityScore': (total - unfinished[subject]) ** 2 / total,
                    'unfinishedPercent': round(100 * unfinished[subject] / total, 2)}
                   for subject, total in totals.items()),
                  key=lambda s: (Fraction(s['completed'] ** 2, s['total']), -s['remaining'], SUBJECT_ORDER.index(s['subject'])))


def next_entry(entries):
    """Do not mistake an unavailable confirmation item for actionable work."""
    subject = next((s['subject'] for s in subject_stats(entries) if s['available']), None)
    candidates = [e for e in entries if e['subject'] == subject and e['state'] == 'queued']
    return sorted(candidates, key=lambda e: (-int(e['date'].replace('-', '')), e['id']))[0] if candidates else None


if __name__ == '__main__':
    import argparse
    import json
    from datetime import datetime, timezone
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--claim', action='store_true', help='Reserve the next item for review.')
    args = parser.parse_args()
    path = Path(__file__).resolve().parents[1] / 'docs/comics/progress.json'
    progress = json.loads(path.read_text())
    selected = next_entry(progress['entries'])
    if args.claim and selected:
        selected['state'] = 'reviewing'
        selected['reviewStartedAt'] = datetime.now(timezone.utc).isoformat()
        progress['updatedAt'] = selected['reviewStartedAt']
        progress['nextSubject'] = selected['subject']
        path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'next': selected, 'subjects': subject_stats(progress['entries'])}, ensure_ascii=False, indent=2))
