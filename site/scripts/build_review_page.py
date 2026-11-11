"""Build reading pages using shared image assets, without duplicating image bytes."""
from teaching_comic import render_comic, inline_comic_support
from group_review_html import render_group_page
import os
import html
import json
import re
from pathlib import Path
from illustration_quality import biology_quality
BASE=Path(__file__).resolve().parents[1]
DEST=Path(os.environ.get('WEIRUGO_DIST', BASE/'dist'))
CSS=(BASE/'scripts/review-page.css').read_text()
quality=biology_quality(BASE.parent)
e=lambda value:html.escape(str(value or ''))
def text_html(value):
 return re.sub(r'˙?[\u3105-\u312f]+[ˊˇˋ˙]?', lambda match: '<span class="phonetic">'+match[0]+'</span>', e(value))
def image_url(path):
 if not re.fullmatch(r'assets/[a-zA-Z0-9_./-]+', path) or '..' in path:
  raise ValueError('Invalid local asset path: '+path)
 if not (DEST/path).is_file():raise FileNotFoundError(DEST/path)
 return path
def table_html(t):
 return '<div class="data-table"><table><caption>'+e(t.get('caption',''))+'</caption><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+text_html(c)+'</td>' for c in row)+'</tr>' for row in t['rows'])+'</tbody></table></div>'
payload=json.loads((DEST/'data.json').read_text());subjects={s['id']:s['name'] for s in payload['subjects']};count=0
for q in payload['questions']:
 if q.get('contentStatus')!='完整原題':continue
 if os.environ.get('WEIRUGO_BIOLOGY_LABELS_ONLY') and q.get('subject')!='Biology':continue
 quality_item=quality.get(q['id'])
 quality_badge=('<span class="illustration-quality '+quality_item['state']+'" title="'+e(quality_item['note'])+'">'+e(quality_item['label'])+'</span>') if quality_item else ''
 if q.get('groupQuestions'):
  page=render_group_page(q,subjects,{s['id']:s for s in payload['sources']},CSS,text_html,image_url,table_html,lambda:inline_comic_support(DEST),DEST)
  if quality_badge:page=page.replace('<h1>',quality_badge+'<h1>',1)
  (DEST/(q['id']+'.html')).write_text(page);count+=1
  continue
 rows=''.join(f'<tr class="{"correct" if o["label"]==q.get("correctOption", "D" if q["id"]=="q-024" else "") else ""}"><th scope="row"><b>({e(o["label"])})</b><br>{text_html(o["text"])}</th><td>{e(o["wordClass"])}</td><td><p>{text_html(o["meaning"])}</p><p>{text_html(o["explanation"])}</p></td></tr>' for o in q.get('optionAnalysis',[]))
 options=('<h2>逐項解析</h2><div class="table-wrap"><table><thead><tr><th scope="col">選項與原句</th><th scope="col">判讀</th><th scope="col">句意與判斷理由</th></tr></thead><tbody>'+rows+'</tbody></table></div>') if rows else ''
 materials=('<section class="reading-passage"><h3>作答所需文章／材料</h3>'+text_html(q.get('passage'))+'</section>') if q.get('passage') else ''
 materials+=''.join(table_html(t) for t in q.get('tables',[]))
 materials+=''.join('<figure class="question-figure"><img src="'+image_url(f['src'])+'" alt="'+e(f['alt'])+'"><figcaption>'+e(f.get('caption',''))+'</figcaption></figure>' for f in q.get('questionFigures',[]))
 explanation='<p>'+text_html(q['explanation']).replace('\n','<br>')+'</p>'
 explanation+=render_comic(q.get('teachingComic'),image_url)
 explanation+=''.join('<figure class="question-figure'+(' teaching-comic' if f['src'].startswith('assets/comics/') else '')+'"><img src="'+image_url(f['src'])+'" alt="'+e(f['alt'])+'"><figcaption>'+e(f.get('caption',''))+'</figcaption></figure>' for f in q.get('explanationFigures',[]))
 evidence=''.join('<img src="'+image_url(path)+'" alt="本題原卷截圖" loading="lazy">' for path in q['images'])
 response=('<div class="response">原卷作答：<b>'+e(q['studentAnswer'])+'</b></div>') if q.get('studentAnswer') else ''
 reference='<a href="https://dict.revised.moe.edu.tw/dictView.jsp?ID=7481&amp;la=0&amp;powerMode=0">教育部辭典「之」</a>' if q['id']=='q-024' else '題幹與附圖依提供的原卷核對。'
 review_request=''
 if q.get('reviewQuestions'):
  source=next((s for s in payload['sources'] if s['id']==q['sourceId']),{})
  review_request='<section class="trap review-request" aria-labelledby="review-request-title"><h2 id="review-request-title">請協助核對</h2><p class="small">'+e(q.get('reviewLabel',''))+'</p><ol>'+''.join('<li>'+text_html(item)+'</li>' for item in q['reviewQuestions'])+'</ol>'
  if q.get('reviewExcerpt'):
   review_request+='<h3>目前保存的原始輸入（未訂正）</h3><div class="reading-passage review-excerpt">'+text_html(q['reviewExcerpt'])+'</div>'
  if source.get('url'):
   review_request+='<a href="'+e(source['url'])+'" target="_blank" rel="noopener noreferrer">開啟原始對話 ↗</a>'
  review_request+='</section>'
 page=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(q['title'])}｜完整原題與詳解｜WeiRuGo</title><style>{CSS}</style></head><body><main><header><div class="eyebrow">WeiRuGo · 完整原題</div><h1>{e(q['title'])}</h1><div class="meta">{e(subjects[q['subject']])} / {e(q['volume'])} / {e(q['chapter'])} · {e(q.get('dateLabel','首次出題日期'))}：{e(q['date'])}</div></header><div class="content"><p class="source">{e(q.get('sourceLabel',''))}</p>{review_request}<h2>完整原題</h2>{materials}<div class="question">{text_html(q['question'])}</div><details class="review"><summary>先想一想，再查看答案、解說與原圖</summary><div class="review-content">{response}<div class="answer">{text_html(q['answer']).replace(chr(10),'<br>')}</div>{options}<h2>詳細說明與解題步驟</h2>{explanation}<aside class="trap"><b>這題要記住</b><br>{text_html(q['trap'])}</aside>{'<p class="small">核對註記：'+e(q['verificationNote'])+'</p>' if q.get('verificationNote') else ''}<section class="evidence"><h2>原圖（僅本題）</h2>{evidence or ('<p>作答附圖已列在題目中，重繪圖已註明；此處尚無另存的原卷截圖。</p>' if q.get('questionFigures') else '<p>此題無附圖。</p>')}</section></div></details><footer>{reference}</footer></div></main>{inline_comic_support(DEST) if q.get('teachingComic') else ''}</body></html>'''
 if quality_badge:page=page.replace('<h1>',quality_badge+'<h1>',1)
 (DEST/(q['id']+'.html')).write_text(page);count+=1
print(f'Built {count} exercise pages with shared image assets.')
