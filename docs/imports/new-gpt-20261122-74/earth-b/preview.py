from pathlib import Path
import json,sys,base64,mimetypes,html
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
sys.path.insert(0,str(ROOT/'site/scripts'))
from teaching_comic import render_comic,inline_comic_support
out=ROOT/'.cache/source74-earthb-qa';out.mkdir(exist_ok=True)
def img(p):return 'data:'+mimetypes.guess_type(p)[0]+';base64,'+base64.b64encode((ROOT/p).read_bytes()).decode()
for n in range(1175,1179):
 s=json.loads((B/f'specs/q-{n}.json').read_text());q=json.loads((B/f'questions/q-{n}.json').read_text())
 body='<h1>'+html.escape(q['title'])+'</h1><div class="stem">'+html.escape(q['question']).replace('\n','<br>')+'</div>'
 for t in q['tables']:
  body+='<table><caption>'+html.escape(t['caption'])+'</caption><thead><tr>'+''.join('<th>'+html.escape(h)+'</th>'for h in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(c)+'</td>'for c in row)+'</tr>'for row in t['rows'])+'</tbody></table>'
 for f in q['questionFigures']:body+='<figure><img src="'+img(f['src'])+'"><figcaption>'+html.escape(f['caption'])+'</figcaption></figure>'
 body+='<details><summary>答案、解說與原圖</summary><p>'+html.escape(q['answer'])+'</p><p>'+html.escape(q['explanation']).replace('\n','<br>')+'</p>'+render_comic(s,img)+'<img class="original" src="'+img(q['images'][0])+'"></details>'
 css='*{box-sizing:border-box}body{margin:0;background:#f7f8f4;font-family:sans-serif;color:#243f50;line-height:1.6}main{width:min(calc(100% - 40px),1070px);margin:auto}h1{font-size:24px}table{border-collapse:collapse;margin:20px 0;width:100%;font-size:14px}td,th{border:1px solid #b6c6c9;padding:6px}img{max-width:100%;height:auto}figure{margin:16px 0}details>summary{font-family:sans-serif;padding:10px;cursor:pointer}.original{margin-top:20px}@media(min-width:761px) and (max-width:1200px){main{width:814px}}'
 (out/f'q-{n}.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>'+css+'</style><main>'+body+'</main>'+inline_comic_support(ROOT/'site/dist'))
print(out)
