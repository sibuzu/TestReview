"""Self-contained native HTML/CSS counterpart to teaching-comic.js."""
from html import escape
import json

def render_comic(c, image_url):
    if not c:
        return ''
    e = lambda text: escape(str(text))
    cells = []
    for i, p in enumerate(c['panels']):
        cells.append(f'<section class="comic-cell"><div class="comic-art"><img src="{image_url(c["art"])}" alt="{e(p["alt"])}" style="--panel:{i}" loading="lazy"></div><div class="comic-copy"><h4 class="comic-text">{e(p["heading"])}</h4><p class="comic-text">{e(p["text"])}</p></div></section>')
    points = ''.join(f'<li class="comic-text">{e(t)}</li>' for t in c['fourth']['points'])
    cells.append(f'<section class="comic-cell comic-recap"><h4 class="comic-text">④ {e(c["title"])}</h4><p class="comic-answer comic-text">{e(c["fourth"]["answer"])}</p><ul>{points}</ul></section>')
    words = c.get('protectedWords', [])
    words = words if isinstance(words, list) else []
    return f'<section class="native-comic" aria-label="{e(c["title"])}" data-protected-words="{e(json.dumps(words, ensure_ascii=False))}"><div class="comic-grid">'+''.join(cells)+'</div></section>'

def inline_comic_support(dest):
    # Reuse the actual browser layout code so standalone and app wrap identically.
    wrap = (dest/'comic-wrap.js').read_text().replace('export function ', 'function ')
    layout = (dest/'teaching-comic.js').read_text().split('let comicObserver;', 1)[1]
    layout = ('let comicObserver;'+layout).replace('export function ', 'function ')
    escape_js = "const e=v=>String(v??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));"
    return '<style>'+(dest/'comic.css').read_text()+'</style><script>'+escape_js+wrap+layout+'\nlayoutTeachingComics();</script>'
