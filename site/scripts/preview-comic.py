"""Render one worker's isolated native comic without editing the shared site."""
import base64
import json
import mimetypes
from pathlib import Path
import re
import sys
from teaching_comic import inline_comic_support, render_comic

root = Path(__file__).resolve().parents[2]
qid = sys.argv[1]
assert re.fullmatch(r'q-\d+', qid)
spec = json.loads((root/'docs/comics'/f'{qid}.json').read_text())
def image_url(_):
    path = root/spec['art']
    return 'data:'+mimetypes.guess_type(path.name)[0]+';base64,'+base64.b64encode(path.read_bytes()).decode()
dest = Path('/tmp/weirugo-comic-previews')
dest.mkdir(exist_ok=True)
html = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box}body{margin:0;background:#f7f8f4}main{width:min(calc(100% - 80px),1070px);margin:auto}@media(min-width:761px) and (max-width:1200px){main{width:814px}}details>summary{font-family:sans-serif;padding:10px}</style><main><details><summary>答案、解說與原圖</summary>'+render_comic(spec,image_url)+'</details></main>'+inline_comic_support(root/'site/dist')
(dest/f'{qid}.html').write_text(html)
print(dest/f'{qid}.html')
