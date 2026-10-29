"""Apply the user's current policy to explanation artwork, never exam figures."""
import json


def is_source_ai_figure(figure):
    description = figure.get('caption', '') + figure.get('alt', '')
    return ('來源AI' in description or '來源 AI' in description or
            'source-ai' in figure.get('src', '').lower())


def apply_comic_policy(questions, root):
    path = root / 'docs/comics/policy.json'
    if not path.exists() or json.loads(path.read_text()).get('reuseSourceAI', True):
        return
    for question in questions:
        if 'explanationFigures' in question:
            question['explanationFigures'] = [f for f in question['explanationFigures']
                                              if not is_source_ai_figure(f)]
