"""Read-only status of the paused illustration work, independent of new imports."""
import json
from collections import Counter

PLAN = 'docs/comics/biology-rework-20261112/plan.json'
SUBJECTS = {'Biology': '生物', 'Chinese': '國文', 'English': '英文', 'Math': '數學',
            'Physics-Chemistry': '理化', 'Earth': '地科', 'Geography': '地理',
            'History': '歷史', 'Civics': '公民'}


def four_images(question):
    comic = question.get('teachingComic') or {}
    images = [p.get('image') for p in comic.get('panels', [])]
    images.append(comic.get('fourth', {}).get('image'))
    return len(images) == 4 and all(images) and len(set(images)) == 4


def build_rework_status(root, data, progress):
    path = root / PLAN
    if not path.is_file():
        return None
    plan = json.loads(path.read_text(encoding='utf-8'))
    questions, parents = {}, {}
    for page in data.get('questions', []):
        for question in page.get('groupQuestions') or [page]:
            questions[question['id']] = question
            parents[question['id']] = page['id']
    counts, items, seen = {}, [], set()
    for entry in plan.get('entries', []):
        completed_ids = entry.get('completedOriginalIds', entry.get('originalQuestionIds', [entry['id']]))
        for qid in entry.get('originalQuestionIds', [entry['id']]):
            if qid in seen:
                continue
            seen.add(qid)
            question = questions.get(qid, {})
            subject = question.get('subject', entry.get('subject', ''))
            row = counts.setdefault(subject, Counter(completed=0, pending=0, reassess=0))
            complete = entry.get('state') == 'complete' and qid in completed_ids and four_images(question)
            row['completed' if complete else 'pending'] += 1
            items.append(dict(id=qid, title=question.get('title', entry.get('title', qid)),
                              subject=subject, subjectName=SUBJECTS.get(subject, subject),
                              state='complete' if complete else 'paused',
                              url='/site/index.html#question/' + parents.get(qid, entry['id'])))
    reassess = []
    for entry in progress.get('entries', []):
        qid = entry['id']
        if entry.get('state') != 'not_suitable' or qid in seen or qid not in questions or four_images(questions[qid]):
            continue
        seen.add(qid)
        subject = questions[qid].get('subject', entry.get('subject', ''))
        counts.setdefault(subject, Counter(completed=0, pending=0, reassess=0))['reassess'] += 1
        reassess.append(dict(id=qid, title=questions[qid].get('title', entry.get('title', qid)),
                             subject=subject, reason=entry.get('reason', ''),
                             url='/site/index.html#question/' + parents[qid]))
    rows = [dict(subject=subject, name=SUBJECTS.get(subject, subject), **row)
            for subject, row in counts.items()]
    rows.sort(key=lambda r: (r['subject'] != 'Biology', -r['pending'], r['name']))
    completed = sum(r['completed'] for r in rows)
    pending = sum(r['pending'] for r in rows)
    biology = next((r for r in rows if r['subject'] == 'Biology'), {'pending': 0})
    return dict(title='圖解重製與待補清單', state=plan.get('state', 'paused'),
                completed=completed, pending=pending, reassess=len(reassess),
                total=completed + pending, unit='原問', subjects=rows,
                biologyPending=biology['pending'], otherPending=pending - biology['pending'],
                biologyResumeCommand=plan.get('executionControl', {}).get('biologyResumePhrase')
                    or '將生物的舊解說圖改為精美解說圖',
                otherResumeCommand='繼續非生物圖解重製，只處理監看頁的待重製清單',
                reassessCommand='重新檢視並補製 ' + '、'.join(r['id'] for r in reassess) + ' 的四張圖解',
                items=items, reassessItems=reassess, plan=PLAN,
                note='按原問計數，題組內每一小題各算一題；草稿與待驗收圖不計已完成。新來源製圖另列，不會恢復這份暫停清單。')
