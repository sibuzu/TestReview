from pathlib import Path
import json,sys,base64,mimetypes
R=Path.cwd();sys.path.insert(0,str(R/'site/scripts'))
from teaching_comic import render_comic,inline_comic_support
B=R/'docs/imports/new-gpt-20261119-73/lane2'
for p in sorted((B/'specs').glob('*.json')):
 s=json.loads(p.read_text());id=s['id']
 def url(rel):
  path=R/rel
  return 'data:'+mimetypes.guess_type(path.name)[0]+';base64,'+base64.b64encode(path.read_bytes()).decode()
 html='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box}body{margin:0;background:#f7f8f4;font-family:sans-serif}main{width:min(calc(100% - 80px),1070px);margin:auto}@media(min-width:761px) and (max-width:1200px){main{width:814px}}details>summary{padding:10px}</style><main><details><summary>答案、解說與原圖</summary>'+render_comic(s,url)+'</details></main>'+inline_comic_support(R/'site/dist')
 (B/'qa'/f'{id}-preview.html').write_text(html)
 print(id)
