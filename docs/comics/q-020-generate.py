"""A reading-context diagram; no life-stage ages or historical reconstruction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import socket
import time

started = datetime.now(timezone.utc).isoformat()
mono = time.monotonic_ns()
art = Path('docs/comics/art/q-020-context.svg')
p = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-label="原句起終點、四個選項階段、完整代入比較"><rect width="900" height="300" fill="#faf7ed"/><style>text{font-family:"Noto Sans CJK TC",sans-serif;text-anchor:middle;fill:#294b48}.h{font-size:24px;font-weight:700}.w{font-size:25px}.s{font-size:20px}.good{fill:#3c7659}.bad{fill:#a65746}</style><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#7d9680"/></marker></defs>']

def text(x, y, words, cls='w'):
    return f'<text x="{x}" y="{y}" class="{cls}">{words}</text>'

def card(x, y, words, fill='#e6eddf', cls='w'):
    return f'<rect x="{x}" y="{y}" width="250" height="52" rx="12" fill="{fill}"/>' + text(x+125, y+35, words, cls)

p += ['<g id="context">', text(150, 32, '原句的起點與終點', 'h'),
      text(150, 67, '人生由', 's'), card(25, 84, '［　］：起點', '#eadfc5'),
      '<path d="M150 146V185" fill="none" stroke="#7d9680" stroke-width="3" marker-end="url(#arrow)"/>',
      card(25, 200, '步入晚年：終點'), text(150, 281, '空格不是再填終點', 's'), '</g>']
p += ['<g id="options" transform="translate(300 0)">', text(150, 32, '對照本題四個選項', 'h')]
for label, y, fill in [('A 幼年', 49, '#ebe9e1'), ('B 青年', 105, '#ebe9e1'), ('C 中年', 161, '#d9e8d4'), ('D 晚年', 217, '#e5eee2')]:
    p.append(card(25, y, label, fill))
    if y < 217:
        p.append(f'<path d="M150 {y+53}V{y+56}" stroke="#7d9680" stroke-width="2" marker-end="url(#arrow)"/>')
p += ['</g><g id="substitution" transform="translate(600 0)">', text(150, 32, '填回完整句子比較', 'h'),
      text(150, 73, 'D 代入', 's bad'), card(25, 87, '由晚年步入晚年', '#f0e1db', 'w bad'),
      text(150, 168, '缺少階段的轉換', 's bad'), text(150, 209, 'C 代入', 's good'),
      card(25, 222, '由中年步入晚年', '#dcebd6', 'w good'), '</g></svg>']
art.write_text(''.join(p))

spec = {
 'id': 'q-020', 'subject': 'Chinese', 'title': '先讀起終點，再把選項填回上下文',
 'art': str(art), 'artMode': 'deterministic-svg', 'generatorFile': 'docs/comics/q-020-generate.py',
 'layoutVersion': 'native-fluid-v6', 'producerAgent': '/root/comic_lane_1',
 'panels': [
  {'heading': '① 晚年已寫出，空格要填轉入前的階段',
   'text': '原句是「人生由［　］步入晚年」。「由」指出起點，「步入」指出接下來的階段；後面已經是晚年，空格應和它形成有意義的轉換，不能只看見晚年就照抄。',
   'alt': '新原生句子結構圖，空格標起點、步入晚年標終點，箭頭只示意原句轉換，不是固定年齡公式。'},
  {'heading': '② 深秋紅葉的意象，呼應成熟的人生',
   'text': '前文寫深秋紅葉耀眼、天地宣告落幕，接著聯想生命也可有壯麗演出。在四個選項中，中年最能銜接走向晚年的成熟階段，比幼年、青年更符合這段上下文。',
   'alt': '新原生圖列本題A幼年、B青年、C中年、D晚年，突出中年接向晚年；只比較題中四項，不指定歲數或宣稱完整人生分期。'},
  {'heading': '③ 把C與D填回去，檢查整句是否通順',
   'text': 'C填入後是由中年步入晚年，保留階段轉換；D則成了由晚年步入晚年，不合此處轉入另一人生階段的語意。閱讀填空要看整句，不只抓一個關鍵詞。',
   'alt': '新原生完整代入比較：D由晚年步入晚年，C由中年步入晚年，顏色對比語境是否有階段轉換，未更改原題選項。'}],
 'fourth': {'answer': '答案 C：中年', 'points': [
    '空格寫起點，後文晚年寫轉入的階段。',
    '深秋與成熟的意象，支持中年走向晚年。',
    'D填回後重複同一階段，不合本文轉換的意思。']},
 'protectedWords': ['人生階段','中年','晚年','幼年','青年','深秋','紅葉','上下文','起點','終點','步入晚年','由中年步入晚年','由晚年步入晚年','階段轉換','壯麗演出','關鍵詞'],
 'originalChecked': {'images': ['site/dist/assets/questions/q-020-source-1-bac65e151a.jpg','site/dist/assets/questions/q-020-source-2-dccf834f4c.jpg'], 'visualChecked': True, 'answer': 'C', 'notes': '親見東福寺楓火遊記完整必要段、人生由空格步入晚年句與25四項、原D作答；不再以秋天的況味當課名，不補原文未指定年齡或生理條件。'},
 'answerCheckedAgainst': '原卷步入晚年在空格後，成熟深秋意象與四選項代入檢查；維持既有C，不將原AI作唯一答案依據。',
 'rationale': '本題難點在空格前後句法、成熟意象與填回比較，精確原生結構圖較泛用年齡人物更直接。不需生成東福寺外觀或虛構作者人物，也不把中年定義成固定年齡。',
 'generationCalls': 0, 'sourceAIUsed': False, 'manualLineBreaks': False,
 'diagramChecks': {'answer': 'C','optionOrder': ['幼年','青年','中年','晚年'], 'originalEndpoint': '晚年','correctSubstitution': '由中年步入晚年','dSubstitution': '由晚年步入晚年','fixedAgesClaimed': False,'fullLifeStageTaxonomyClaimed': False,'exactTempleOrAuthorReconstructed': False},
 'artSHA256': hashlib.sha256(art.read_bytes()).hexdigest(), 'timingEvidence': 'docs/comics/q-020-timing.json'
}
Path('docs/comics/q-020.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
Path('docs/comics/q-020-timing.json').write_text(json.dumps({'id':'q-020','startedAt':started,'monotonicStartNs':mono,'timingHost':socket.gethostname(),'scope':'same-host native SVG composition and preview QA; no imagegen call','generationCalls':0},ensure_ascii=False,indent=2)+'\n')
