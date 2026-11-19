import json,sys,html,base64,mimetypes
from pathlib import Path
sys.path.insert(0,'site/scripts')
from teaching_comic import render_comic,inline_comic_support
R=Path.cwd();B=R/'docs/imports/new-gpt-20261119-73/lane3'
def image_url(p):
 f=R/p
 return 'data:'+str(mimetypes.guess_type(f.name)[0])+';base64,'+base64.b64encode(f.read_bytes()).decode()
for n in range(1163,1169):
 q=f'q-{n}';d=json.loads((B/f'questions/{q}.json').read_text());s=json.loads((B/f'specs/{q}.json').read_text())
 question='<h1>'+html.escape(d['title'])+'</h1><p>首次出題日期 2026-11-19</p><div class="question">'+html.escape(d['question']).replace('\n','<br>')+'</div>'+''.join('<img class="original-figure" src="'+image_url(f['src'])+'" alt="'+f['alt']+'">' for f in d['questionFigures'])
 details='<details><summary>答案、詳細解說與原圖</summary><h2>'+html.escape(d['answer'])+'</h2><div class="explanation">'+html.escape(d['explanation']).replace('\n','<br>')+'</div>'+render_comic(s,image_url)+'<img class="original" src="'+image_url(d['images'][0])+'" alt="本題原卷核對裁切"></details>'
 out='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box}body{margin:0;background:#f7f8f4;font-family:"Noto Sans CJK TC",sans-serif;color:#1e293b}main{width:min(calc(100% - 40px),1070px);margin:20px auto}h1{font-size:25px;line-height:1.4}.question,.explanation{font-size:17px;line-height:1.8;margin:20px 0}summary{padding:15px;cursor:pointer;background:white}.original,.original-figure{display:block;max-width:100%;height:auto;margin:16px auto}.art-gallery{display:grid;grid-template-columns:repeat(2,400px);gap:10px}.art-gallery img{width:400px;height:400px}</style><main>'+question+details+'</main>'+inline_comic_support(R/'site/dist')
 (B/f'qa/{q}-preview.html').write_text(out)
 gallery='<meta charset="utf-8"><style>body{margin:0;background:white}.gallery{display:grid;grid-template-columns:repeat(2,400px);gap:5px}.gallery img{width:400px;height:400px}</style><div class="gallery">'+''.join('<img src="'+image_url(i)+'">' for i in [p['image'] for p in s['panels']]+[s['fourth']['image']])+'</div>'
 (B/f'qa/{q}-art.html').write_text(gallery)
