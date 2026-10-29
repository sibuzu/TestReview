"""Reading-page rendering for groups, without changing any child snapshot."""
import hashlib
import html
import json
from urllib.parse import urlsplit
from teaching_comic import render_comic

GROUP_CSS='''
main{max-width:1200px}.group-question+.group-question,.group-answer+.group-answer{border-top:1px solid #dce5d5;padding-top:18px;margin-top:24px}
.group-question>h2,.group-answer>h2{font-size:19px;line-height:1.6}.group-child-source{font-size:12px;color:#6f8064;overflow-wrap:anywhere}
.group-specific-caption{font-size:13px;color:#6f8064}.group-answer .native-comic{margin:18px 0}.group-answer .explanation{white-space:normal}
'''


def ordered_children(question):
    children=question['groupQuestions']
    order=question.get('groupMetadata',{}).get('displayOrder',[])
    positions={qid:index for index,qid in enumerate(order)}
    return sorted(children,key=lambda child:positions.get(child['id'],len(order))) if order else children


def child_materials(child,parent,asset_root):
    """Only remove text actually present in the common material, not paraphrases."""
    passage=child.get('passage','');common=parent.get('passage','')
    if passage and passage in common:
        passage=''
    elif common and passage.startswith(common):
        passage=passage[len(common):].strip()
    tables=[table for table in child.get('tables',[]) if table not in parent.get('tables',[])]
    figures=[];captions=[];shared=parent.get('questionFigures',[])
    equivalent={row['src']:row for row in parent.get('groupMetadata',{}).get('commonFigureEquivalentSources',[])}
    for figure in child.get('questionFigures',[]):
        matches=[other for other in shared if other.get('src')==figure.get('src')]
        proof=equivalent.get(figure.get('src'))
        if not matches and proof:
            matches=[other for other in shared if other.get('src')==proof.get('commonSrc')]
            if matches:
                paths=[(asset_root/source).resolve() for source in (figure['src'],proof['commonSrc'])]
                valid=all(path.is_relative_to(asset_root.resolve()) and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==proof.get('sha256') for path in paths)
                if not valid:matches=[]
        if not matches:
            figures.append(figure)
        elif figure.get('caption') and all(figure['caption']!=other.get('caption') for other in matches):
            captions.append(figure['caption'])
    return dict(passage=passage,tables=tables,questionFigures=figures),captions


def source_link(child,sources):
    source=sources.get(child.get('sourceId'),{})
    url=source.get('url','');parts=urlsplit(url)
    if parts.scheme!='https' or parts.hostname not in {'chatgpt.com','share.gemini.google','gemini.google.com'}:
        return ''
    return '<a href="'+html.escape(url,quote=True)+'" target="_blank" rel="noopener noreferrer">原AI對話 ↗</a>'


def render_group_page(question,subjects,sources,css,text_html,image_url,table_html,comic_support,asset_root):
    e=lambda value:html.escape(str(value or ''))

    def materials(value):
        result=('<section class="reading-passage"><h3>作答所需文章／材料</h3>'+text_html(value['passage'])+'</section>') if value.get('passage') else ''
        result+=''.join(table_html(table) for table in value.get('tables',[]))
        result+=''.join('<figure class="question-figure"><img src="'+image_url(figure['src'])+'" alt="'+e(figure.get('alt'))+'"><figcaption>'+e(figure.get('caption'))+'</figcaption></figure>' for figure in value.get('questionFigures',[]))
        return result

    def answer(child):
        result=('<div class="response">原卷作答：<b>'+e(child['studentAnswer'])+'</b></div>') if child.get('studentAnswer') else ''
        result+='<div class="answer">'+text_html(child.get('answer','')).replace('\n','<br>')+'</div>'
        rows=''.join('<tr class="'+('correct' if option['label']==child.get('correctOption') else '')+'"><th scope="row"><b>('+e(option['label'])+')</b><br>'+text_html(option.get('text'))+'</th><td>'+e(option.get('wordClass'))+'</td><td><p>'+text_html(option.get('meaning'))+'</p><p>'+text_html(option.get('explanation'))+'</p></td></tr>' for option in child.get('optionAnalysis',[]))
        if rows:result+='<h3>逐項解析</h3><div class="table-wrap"><table><thead><tr><th scope="col">選項與原句</th><th scope="col">判讀</th><th scope="col">句意與判斷理由</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
        result+='<h3>詳細說明與解題步驟</h3><div class="explanation"><p>'+text_html(child.get('explanation','')).replace('\n','<br>')+'</p></div>'
        # The same art may illustrate different answers. Render each complete
        # child lesson; never deduplicate teaching comics by image hash or URL.
        result+=render_comic(child.get('teachingComic'),image_url)
        result+=''.join('<figure class="question-figure'+(' teaching-comic' if figure['src'].startswith('assets/comics/') else '')+'"><img src="'+image_url(figure['src'])+'" alt="'+e(figure.get('alt'))+'"><figcaption>'+e(figure.get('caption'))+'</figcaption></figure>' for figure in child.get('explanationFigures',[]))
        if child.get('trap'):result+='<aside class="trap"><b>這題要記住</b><br>'+text_html(child['trap'])+'</aside>'
        if child.get('verificationNote'):result+='<p class="small">核對註記：'+e(child['verificationNote'])+'</p>'
        evidence=''.join('<img src="'+image_url(path)+'" alt="本題原卷截圖" loading="lazy">' for path in child.get('images',[]))
        result+='<section class="evidence"><h3>原圖（僅本題）</h3>'+(evidence or '<p>此題沒有另存原卷截圖。</p>')+'</section>'
        return result

    questions=materials(question);answers='';children=ordered_children(question)
    for child in children:
        specific,captions=child_materials(child,question,asset_root)
        questions+='<section class="group-question" data-group-question="'+e(child['id'])+'"><h2>'+e(child['title'])+'</h2>'+materials(specific)+''.join('<p class="group-specific-caption">'+text_html(caption)+'</p>' for caption in captions)+'<div class="question">'+text_html(child['question'])+'</div></section>'
        link=source_link(child,sources)
        provenance=e(child.get('sourceLabel'))+' · '+e(child.get('dateLabel','首次出題日期'))+' '+e(child.get('date'))+(' · '+link if link else '')
        answers+='<section class="group-answer" data-group-answer="'+e(child['id'])+'"><h2>'+e(child['title'])+'</h2><p class="group-child-source">'+provenance+'</p>'+answer(child)+'</section>'
    support=comic_support() if any(child.get('teachingComic') for child in children) else ''
    return '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(question['title'])+'｜完整原題與詳解｜WeiRuGo</title><style>'+css+GROUP_CSS+'</style></head><body><main><header><div class="eyebrow">WeiRuGo · 完整原題</div><h1>'+e(question['title'])+'</h1><div class="meta">'+e(subjects[question['subject']])+' / '+e(question.get('volume','綜合'))+' / '+e(question.get('chapter','綜合'))+' · '+e(question.get('dateLabel','首次出題日期'))+'：'+e(question['date'])+'</div></header><div class="content"><h2>完整原題</h2>'+questions+'<details class="review"><summary>先想一想，再查看答案、解說與原圖</summary><div class="review-content">'+answers+'</div></details></div></main>'+support+'</body></html>'
