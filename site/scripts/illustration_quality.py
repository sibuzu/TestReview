"""Biology labels follow accepted work, never the mere presence of a comic."""
import json


def biology_quality(root):
    path = root/'docs/comics/biology-rework-20261112/plan.json'
    if not path.exists():
        return {}
    result = {}
    for entry in json.loads(path.read_text()).get('entries', []):
        if entry.get('subject') != 'Biology':
            continue
        accepted = entry.get('state') == 'complete'
        for qid in entry.get('originalQuestionIds', [entry['id']]):
            spec_path = root/f'docs/comics/{qid}.json'
            spec = json.loads(spec_path.read_text()) if spec_path.exists() else {}
            review = spec.get('rootReview', {})
            verified = (accepted and spec.get('visualChecked') and review.get('visualChecked')
                        and review.get('originalVisualChecked') and review.get('answerAndExplanationChecked')
                        and review.get('fourActualIndependentImages'))
            missing = 'missing_illustration' in entry.get('reasons', []) and not verified
            state = 'fine' if verified else 'missing' if missing else 'legacy'
            draft = bool(spec.get('fourth', {}).get('image')) and not verified
            result[qid] = dict(state=state, label={'fine':'精美解說圖','legacy':'舊版解說圖','missing':'解說圖待補'}[state],
                draftPendingReview=draft, note='新版草稿待驗收，尚未採用' if draft else '')
    return result


def write_quality(root):
    quality = biology_quality(root)
    dest = root/'site/dist'
    (dest/'biology-illustration-status.json').write_text(json.dumps(quality, ensure_ascii=False, indent=2)+'\n')
    (dest/'biology-illustration-status.js').write_text('// Generated from formally reviewed work; not comic existence.\nexport const BIOLOGY_ILLUSTRATION_STATUS = '+json.dumps(quality,ensure_ascii=False)+';\n')
    return quality


if __name__ == '__main__':
    from pathlib import Path
    from collections import Counter
    print(dict(Counter(item['state'] for item in write_quality(Path(__file__).resolve().parents[2]).values())))
