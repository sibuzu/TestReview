"""Selectable Chinese labels for deterministic teaching diagram blocks."""
from html import escape
import math


def render_diagram(d):
    if not isinstance(d, dict) or d.get('kind') not in ('nested', 'flow', 'bars', 'sum', 'change', 'paths'):
        return ''
    items = d.get('items', [])
    if not isinstance(items, list) or not 1 <= len(items) <= 8 or any(not isinstance(i, dict) or not isinstance(i.get('label'), str) or not i['label'] for i in items):
        return ''
    kind = d['kind']
    if kind == 'nested' and len(items) != 2:
        return ''
    if kind in ('bars', 'sum') and (any(type(i.get('value')) not in (int, float) or not math.isfinite(i['value']) or not 0 <= i['value'] <= 1e9 for i in items) or not any(i['value'] > 0 for i in items)):
        return ''
    if kind == 'paths' and not d.get('target'):
        return ''
    e = lambda s: escape(str(s)[:500])
    tone = lambda i: i.get('tone') if i.get('tone') in ('blue', 'green', 'gold', 'purple') else 'blue'
    def text(s, tag='span', cls=''):
        return f'<{tag} class="comic-text {cls}">{e(s)}</{tag}>'
    def node(i):
        detail = text(i['detail'], 'span', 'diagram-detail') if i.get('detail') else ''
        return f'<div class="diagram-node tone-{tone(i)}">{text(i["label"], "strong")}{detail}</div>'
    content = ''
    if kind == 'nested':
        content = f'<div class="diagram-set tone-{tone(items[0])}">{text(items[0]["label"], "strong")}<div class="diagram-set tone-{tone(items[1])}">{text(items[1]["label"], "strong")}</div></div>'
    elif kind == 'flow':
        content = ''.join((text('↓ '+d.get('arrow', '下一步'), 'p', 'diagram-arrow') if n else '')+node(i) for n, i in enumerate(items))
    elif kind == 'paths':
        content = '<div class="diagram-inputs">'+''.join(node(i) for i in items)+'</div>'+text('↓ '+d.get('arrow', '送交'), 'p', 'diagram-arrow')+node({'label': d['target'], 'tone': 'blue'})
    elif kind == 'bars':
        maximum = max(i['value'] for i in items)
        content = ''.join('<div class="diagram-bar-row">'+text(f'{i["label"]}：{i["value"]:g} 件', 'strong')+f'<div class="diagram-track"><div class="diagram-fill tone-{tone(i)}" style="width:{100*i["value"]/maximum}%"></div></div></div>' for i in items)
    elif kind == 'sum':
        total = sum(i['value'] for i in items)
        content = '<div class="diagram-sum-segments">'+''.join(f'<div class="diagram-summand tone-{tone(i)}" style="flex:{i["value"]}">'+text(i.get('shortLabel', i['label']), 'strong')+text(f'{i["value"]:g} 件', 'span')+'</div>' for i in items)+'</div><div class="diagram-legend">'+''.join(node(dict(i, detail=f'{i["value"]:g} 件')) for i in items)+'</div>'+text(' ＋ '.join(f'{i["value"]:g}' for i in items)+f' ＝ {total:g} 件', 'p', 'diagram-equation')
    elif kind == 'change':
        content = ''.join(f'<div class="diagram-change tone-{tone(i)}">'+text(i['label'], 'strong')+'<div class="diagram-change-lines">'+text('原本位置（虛線）', 'span', 'diagram-before')+text('↓ 件數減少，線段下移', 'p', 'diagram-arrow')+text('減少後位置（實線）', 'span', 'diagram-after')+'</div></div>' for i in items)
    note = text(d['note'], 'p', 'diagram-note') if d.get('note') else ''
    return f'<section class="comic-diagram diagram-{kind}" aria-label="{e(d.get("title", ""))}">'+text(d.get('title', ''), 'p', 'diagram-title')+content+note+'</section>'
