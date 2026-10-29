import {renderTeachingComic,layoutTeachingComics} from './teaching-comic.js';
import {escapeHTML as e,renderText,safeAsset,selectQuestions,needsReview} from './core.js';
import {parseRoute,questionHash,listHash} from './routes.js';
import {DOUBTS_KEY,loadDoubts} from './marks.js';
import {FlagSync,FLAG_OUTBOX_KEY} from './flag-sync.js';
import {hasQuestionMark,toggleQuestionMark,canonicalQuestionId} from './question-identity.js';
import {FLAGS_KEY,PRACTICE_KEY,FLAG_OPTIONS,DEFAULT_FLAG,checkedFlags,checkedPractice,changedFlag,persistFlagState,discardLegacyMarks,flagIcon,practiceDay,dailyCounts} from './article-flags.js';
import {formatDataUpdatedAt} from './data-updated.js';
import {SESSION_KEY,readSession,restoreSession,signIn,signOut,accountStorage} from './auth.js';
const $=id=>document.getElementById(id);
let data,filters={subject:'',issue:false,doubt:false},page='questions',layout='list',activeId='',toastTimer,doubts=new Set(),flags={},practice=[];
let selectedFlags=new Set([3,4,5]),markSync,session,userStorage;
const flagFor=id=>flags[canonicalQuestionId(id)]??DEFAULT_FLAG;
const scopedQuestions=(questions,selection={})=>selectQuestions(questions.filter(q=>selectedFlags.has(flagFor(q.id))),{subject:selection.subject||'',doubt:!!selection.doubt,issue:!!selection.issue,sort:'newest'});
const icon={all:'▦',source:'↙',issue:'◷',progress:'▤'};
function toast(message){$('toast').textContent=message;$('toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('show'),3500);}
function syncStatus(state){
 const labels={syncing:'標記同步中…',synced:'標記已同步雲端',pending:'本機已存，待同步',local:'本機已存，待連線'};
 const button=$('sync-status');button.textContent=labels[state]||labels.pending;button.dataset.state=state;button.disabled=false;
 button.title='所有入口同步目前帳號的FLAG與進度；疑義共用。點擊立即同步。';document.querySelector('.storage-dot').dataset.state=state;
}
function refreshMarkButtons(){
 if(!activeId)return;const detail=$('detail'),value=flagFor(activeId),focused=document.activeElement?.closest('[data-article-flag]')?.closest('.flag-options');
 for(const button of detail.querySelectorAll('[data-article-flag]')){const selected=Number(button.dataset.articleFlag)===value;button.setAttribute('aria-checked',selected);button.tabIndex=selected?0:-1;}
 if(focused)focused.querySelector('[data-article-flag="'+value+'"]')?.focus({preventScroll:true});
 const button=detail.querySelector('[data-doubt]'),doubt=hasQuestionMark(doubts,activeId);
 if(button){button.classList.toggle('selected',doubt);button.setAttribute('aria-pressed',doubt);button.setAttribute('aria-label',doubt?'取消疑義標記':'標記疑義，待老師確認');button.title=doubt?'已標記疑義，點擊取消':'標記疑義，待老師確認';}
}
function applySyncedMarks(incoming){
 const nextFlags=checkedFlags(incoming.flags||{}),nextPractice=checkedPractice(incoming.practice||[]),nextDoubts=[...incoming.doubts].sort();
 if(JSON.stringify(flags)===JSON.stringify(nextFlags)&&JSON.stringify(practice)===JSON.stringify(nextPractice)&&JSON.stringify([...doubts].sort())===JSON.stringify(nextDoubts))return;
 try{persistFlagState(userStorage,nextFlags,nextPractice,nextDoubts);}catch{toast('瀏覽器無法儲存標記，請檢查儲存空間。');}
 flags=nextFlags;practice=nextPractice;doubts=new Set(nextDoubts);for(const q of data.questions)q.doubted=hasQuestionMark(doubts,q.id);
 render();refreshMarkButtons();
}
function setArticleFlag(id,value){
 const key=canonicalQuestionId(id);if(flagFor(key)===value)return;
 const oldEvents=new Set(practice.map(event=>event.eventId));let next;
 try{next=changedFlag(flags,practice,key,value);persistFlagState(userStorage,next.flags,next.practice,[...doubts]);}
 catch{toast('瀏覽器無法儲存FLAG，請檢查儲存空間。');return;}
 flags=next.flags;practice=next.practice;
 markSync?.queueAll([{kind:'flag',id:key,value},...practice.filter(event=>!oldEvents.has(event.eventId)).map(event=>({kind:'practice',...event}))]);
 render();refreshMarkButtons();toast('已設定為「'+value+' '+FLAG_OPTIONS[value-1].label+'」');
}
function toggleDoubt(id){
 const next=toggleQuestionMark(doubts,id),on=hasQuestionMark(next,id);
 try{persistFlagState(userStorage,flags,practice,[...next]);}catch{toast('瀏覽器無法儲存疑義標記。');return;}
 doubts=next;for(const q of data.questions)q.doubted=hasQuestionMark(doubts,q.id);
 markSync?.queueAll([{kind:'doubt',id:canonicalQuestionId(id),on}]);render();refreshMarkButtons();
}
const doubtIcon="<svg class=\"question-mark-icon\" viewBox=\"230 65 560 900\" aria-hidden=\"true\" focusable=\"false\"><path class=\"question-shape\" d=\"M715.720415 207.522102C675.902539 136.26685 603.803606 95.397443 518.015326 95.397443c-129.594189 0-205.287984 72.306782-238.682003 195.401348-20.885213 76.845665 110.976883 131.618411 140.38594 27.173916 15.792407-56.028029 37.099461-79.499576 98.296063-79.499576 33.883437 0 58.475115 13.134401 72.864799 38.912762 15.649063 28.014526 14.18286 62.384309 3.633769 79.571248-17.119363 27.874254-35.489913 44.013758-56.72939 62.663829-44.432528 39.05201-99.619947 88.864031-99.619946 221.809398 0 70.489385 71.537844 71.537844 71.537843 71.537844 39.470779 0 71.537844-32.067064 71.537844-71.537844 0-69.581199 14.880125-82.643928 50.856384-114.224647 25.013518-21.933671 55.960452-49.11066 84.325148-95.35956 39.677604-64.691123 39.399107-152.714544-0.701362-224.324059z\"/><path class=\"question-highlight\" d=\"M670.72987 403.764058c-24.240485 39.399107-50.648535 62.595229-73.980834 83.134369-40.172141 35.210392-69.16243 60.710256-69.16243 154.531941 0 9.850801-7.965828 17.884205-17.884205 17.884205-9.850801 0-17.884205-8.033404-17.884205-17.884205 0-110.031836 39.470779-144.68114 81.316973-181.430432 22.494761-19.769178 45.759483-40.168045 67.066536-74.960692 22.355512-36.326427 21.307054-91.374598-2.514662-133.850481-23.893388-42.758475-66.436847-66.369271-119.671717-66.369271-86.768138 0-134.762763 39.12061-150.969843 123.022894-1.884973 9.711552-11.213592 16.070904-20.925144 14.182859-9.711552-1.884973-16.067832-11.245333-14.181836-20.956885 19.493753-100.879326 82.05417-152.017278 186.076823-152.017278 66.78804 0 120.368983 30.11042 150.898172 84.672245 30.32134 54.071384 31.018606 122.393204 1.816372 170.040731z\"/><path class=\"question-shape\" d=\"M513.19385 757.121218c-47.433535 0-85.859952 38.423345-85.859951 85.859952 0 47.433535 38.426416 85.859952 85.859951 85.859952 47.364935 0 85.791351-38.426416 85.791352-85.859952 0-47.436607-38.426416-85.859952-85.791352-85.859952z\"/><path class=\"question-highlight\" d=\"M513.19385 875.187483c-17.812533 0-32.206313-14.39378-32.206313-32.206313 0-17.744957 14.39378-32.206313 32.206313-32.206313 17.744957 0 32.138736 14.461356 32.138737 32.206313-0.001024 17.812533-14.39378 32.206313-32.138737 32.206313z\"/></svg>";
function flagControls(q,position='header'){
 const value=flagFor(q.id);return `<div class="flag-options" role="radiogroup" data-flag-position="${position}" aria-label="題目FLAG（${position==='header'?'上方':'下方'}），快捷鍵1至5">${FLAG_OPTIONS.map(o=>`<button type="button" role="radio" class="flag-option" data-article-flag="${o.value}" aria-checked="${o.value===value}" tabindex="${o.value===value?0:-1}" aria-label="${o.value} ${o.label}" aria-keyshortcuts="${o.value}" title="${o.value} ${o.label}（快捷鍵 ${o.value}）" style="--flag-color:${o.color}"><span class="flag-key">${o.value}</span>${flagIcon(o.value)}</button>`).join('')}</div>`;
}
function markButtons(q,detail=false){
 const value=flagFor(q.id),option=FLAG_OPTIONS[value-1],doubt=hasQuestionMark(doubts,q.id);
 if(!detail)return `<span class="flag-indicator" role="img" style="color:${option.color}" aria-label="${value} ${option.label}" title="${value} ${option.label}">${flagIcon(value)}</span>`;
 return `<div class="question-actions detail-actions">${flagControls(q,'header')}<button class="doubt-button ${doubt?'selected':''}" data-doubt="${q.id}" aria-pressed="${doubt}" aria-label="${doubt?'取消疑義標記':'標記疑義，待老師確認'}" title="${doubt?'已標記疑義，點擊取消':'標記疑義，待老師確認'}">${doubtIcon}</button></div>`;
}
function displayTitle(q){return q.title+(q.contentStatus==='待更新'?'（待更新）':'');}
function subject(id){return data.subjects.find(s=>s.id===id)||{id,name:'未分類',publisher:'',icon:'?'};}
function badge(id){const s=subject(id);return `<span class="subject-badge ${e(id)}"><span>${e(s.icon)}</span> ${e(s.name)}</span>`;}
function navButton(action,label,symbol,count,active){return `<button class="nav-item ${active?'active':''}" data-nav="${action}" ${active?'aria-current="page"':''}><span class="nav-symbol">${symbol}</span>${label}<span class="count">${count}</span></button>`;}
function updateNav(){
 const scoped=scopedQuestions(data.questions),pending=data.sources.filter(s=>s.status==='pending').length,issues=scoped.filter(needsReview).length,doubtCount=scoped.filter(q=>hasQuestionMark(doubts,q.id)).length;
 const allActive=page==='questions'&&!filters.subject&&!filters.issue&&!filters.doubt;
 const today=dailyCounts(practice).find(row=>row.day===practiceDay())?.count||0;
 $('main-nav').innerHTML=navButton('all','全部錯題',icon.all,scoped.length+'/'+data.questions.length,allActive)+navButton('progress','我的進度',icon.progress,today,page==='progress')+(doubtCount?navButton('doubt','有疑義的題目','?',doubtCount,filters.doubt):'')+(pending?navButton('source','匯入紀錄',icon.source,pending,page==='sources'):'')+(issues?navButton('issue','待核對原題',icon.issue,issues,filters.issue):'');
 const route=parseRoute(location.hash),current=route.kind==='question'?data.questions.find(q=>q.id===route.id):null,nav=$('subjects');
 document.querySelector('.sidebar').classList.toggle('reading-question',!!current);nav.classList.toggle('question-nav',!!current);
 if(current){
  const qs=scopedQuestions(data.questions,{...(history.state?.returnTo?.filters||{}),subject:current.subject});
  $('subject-heading').innerHTML=`${e(subject(current.subject).name)} <span>${qs.length}</span>`;
  nav.setAttribute('aria-label',subject(current.subject).name+'題目導覽');
  nav.innerHTML=qs.map(q=>`<a class="nav-item question-nav-link ${q.id===current.id?'active':''}" href="${questionHash(q.id)}" data-question-nav="${q.id}" ${q.id===current.id?'aria-current="page"':''}>${e(displayTitle(q))}</a>`).join('');
 }else{
  $('subject-heading').innerHTML=`依科目瀏覽 <span>${data.subjects.length}</span>`;nav.setAttribute('aria-label','科目分類');
  nav.innerHTML=data.subjects.map(s=>`<button class="nav-item ${filters.subject===s.id?'active':''}" data-subject="${s.id}" ${filters.subject===s.id?'aria-current="page"':''}><span class="subject-icon">${e(s.icon)}</span><span class="subject-name">${e(s.name)}<small>${e(s.id==='Physics-Chemistry'?'Physics':s.id)}</small></span><span class="count">${scoped.filter(q=>q.subject===s.id).length}</span></button>`).join('');
 }
 const label=page==='sources'?'匯入紀錄':page==='progress'?'我的進度':filters.subject?subject(filters.subject).name:filters.doubt?'有疑義的題目':filters.issue?'待核對原題':'全部錯題';
 $('breadcrumb').innerHTML=`<a href="#questions">我的學習空間</a><span>/</span><strong aria-current="page">${e(label)}</strong>`;
}
function renderFlagFilters(){
 const counts=Object.fromEntries(FLAG_OPTIONS.map(o=>[o.value,0]));for(const q of data.questions)counts[flagFor(q.id)]++;
 $('question-tools').innerHTML=`<table class="flag-filter-table" aria-label="全域FLAG篩選"><thead><tr><th scope="col">FLAG</th><th scope="col">題數</th><th scope="col">顯示</th></tr></thead><tbody>${FLAG_OPTIONS.map(o=>`<tr><th scope="row"><label for="flag-filter-${o.value}"><span class="flag-row-icon" style="color:${o.color}">${flagIcon(o.value)}</span><span>${o.value} ${o.label}</span></label></th><td data-flag-count="${o.value}">${counts[o.value]}</td><td><input id="flag-filter-${o.value}" type="checkbox" data-flag-filter="${o.value}" ${selectedFlags.has(o.value)?'checked':''} aria-label="顯示${o.value} ${o.label}"></td></tr>`).join('')}</tbody></table>`;
}
function renderProgress(){
 const rows=dailyCounts(practice),today=rows.find(row=>row.day===practiceDay())?.count||0,total=rows.reduce((sum,row)=>sum+row.count,0);
 $('results').className='practice-progress';
 $('results').innerHTML=`<div class="practice-summary"><span>今天 <strong>${today}</strong> 題</span><span>累計淨題數 <strong>${total}</strong> 題</span></div><p class="practice-rule">一般改為其他狀態＋1，其他狀態改回一般－1，依每日淨變動統計。</p>${rows.length?`<table class="practice-table"><thead><tr><th scope="col">日期</th><th scope="col">作題淨數</th></tr></thead><tbody>${rows.map(row=>`<tr><th scope="row">${e(row.day.replaceAll('-','/'))}</th><td class="${row.count<0?'negative':''}">${row.count>0?'+':''}${row.count}</td></tr>`).join('')}</tbody></table>`:'<p class="empty-progress">尚無作題紀錄。</p>'}`;
}
function diagram(type){const wrap=body=>`<div class="card-art" aria-label="輔助示意圖，非原始題圖"><svg viewBox="0 0 300 160" role="img" aria-label="${type==='square'?'正方形與內點示意':type==='trapezoid'?'梯形高與底邊示意':'垂直等長但不互相平分的對角線反例'}"><g fill="none" stroke="#91a785" stroke-width="1.5">${body}</g></svg></div>`;
 if(type==='square')return wrap('<path d="M90 20h120v120H90z" fill="#edf2e9"/><path d="m90 20 32 28 88-28M122 48 88 92" stroke-dasharray="4 4"/><circle cx="122" cy="48" r="3" fill="#718b63"/><g fill="#7d9270" stroke="none" font-size="12" font-family="Georgia"><text x="77" y="17">A</text><text x="215" y="20">B</text><text x="215" y="150">C</text><text x="77" y="151">D</text><text x="125" y="43">P</text><text x="95" y="36">1</text><text x="163" y="26">3</text><text x="82" y="83">√7</text></g>');
 if(type==='trapezoid')return wrap('<path d="m70 130 45-100h42l93 100z" fill="#edf2e9"/><path d="M115 30v100" stroke-dasharray="4 4"/><path d="M115 120h10v10"/><g fill="#7d9270" stroke="none" font-size="12" font-family="Georgia"><text x="132" y="23">1</text><text x="151" y="148">4</text><text x="80" y="78">2</text><text x="209" y="78">3</text><text x="119" y="85">h</text></g>');
 if(type==='diagonals')return wrap('<path d="m150 12 74 108-74 35-74-35z" fill="#edf2e9"/><path d="M150 12v143M76 120h148" stroke-dasharray="4 4"/><path d="M150 111h9v9"/><g fill="#7d9270" stroke="none" font-size="12" font-family="Georgia"><text x="146" y="10">A</text><text x="230" y="124">B</text><text x="145" y="158">C</text><text x="63" y="124">D</text><text x="155" y="71">3</text><text x="155" y="141">1</text><text x="183" y="115">2</text><text x="110" y="115">2</text></g>');return '';}
function render(){
 updateNav();if(activeId){updateQuestionBreadcrumb();return;}
 const sources=page==='sources',progress=page==='progress';$('question-tools').hidden=sources||progress;$('grid-view').parentElement.hidden=sources||progress;
 $('page-title').textContent=sources?'匯入紀錄':progress?'我的進度':filters.doubt?'有疑義的題目':filters.issue?'待核對原題':filters.subject?subject(filters.subject).name:'全部錯題';
 if(sources){renderSources();return;}if(progress){renderProgress();return;}
 renderFlagFilters();const qs=scopedQuestions(data.questions,filters);
 $('results').className=layout==='grid'?'question-grid':'question-list';
 $('results').innerHTML=qs.length?qs.map(q=>`<article class="question-card"><div class="card-main" role="link" tabindex="0" data-open="${q.id}" aria-label="閱讀 ${e(displayTitle(q))}"><div class="card-top">${badge(q.subject)}${markButtons(q)}</div><div class="card-location">${e(q.volume)} <span>/</span> ${e(q.chapter)}</div><h3><a href="${questionHash(q.id)}">${e(displayTitle(q))}</a></h3>${diagram(q.diagram)}<p class="question-preview">${renderText(q.question)}</p><div class="tags">${q.tags.slice(0,3).map(t=>`<span class="tag"># ${e(t)}</span>`).join('')}</div>${needsReview(q)?`<div class="issue-label">◌ ${e(q.contentStatus==='待更新'?'待更新':q.verification)}</div>`:q.verification==='已更正'?'<div class="issue-label" style="color:#7a9566">✓ 已更正原 AI 解答</div>':''}</div><div class="card-foot"><span class="card-date" title="${e(q.dateLabel||'首次出題日期')}：依目前來源最早可確認日期">◷ ${q.date.replaceAll('-','.')} </span><span aria-hidden="true">↗</span></div></article>`).join(''):`<div class="empty" style="grid-column:1/-1"><div class="empty-mark">a fresh page.</div><h3>${filters.subject&&!data.questions.some(q=>q.subject===filters.subject)?'這個科目的錯題本，等你開始。':'目前沒有符合條件的題目'}</h3><p>可在上方勾選要顯示的FLAG。</p><button class="button clear-button" id="clear-filters">顯示一般、重要與很重要</button></div>`;
 $('grid-view').classList.toggle('active',layout==='grid');$('list-view').classList.toggle('active',layout==='list');$('grid-view').setAttribute('aria-pressed',layout==='grid');$('list-view').setAttribute('aria-pressed',layout==='list');
}
function renderSources(){const pending=data.sources.filter(s=>s.status==='pending');$('results').className='source-list';$('results').innerHTML=(pending.length?`<div class="source-banner">${pending.length} 個來源尚未整理完成。</div>`:'<div class="empty-state">目前沒有待整理來源。</div>')+pending.map(s=>`<article class="source-card"><div class="source-platform">${s.platform==='Gemini'?'✧':'◎'}</div><div class="source-info"><h3>${e(s.title||'等待整理的學習討論')} <span class="tag">待整理</span></h3><a class="source-url" href="${e(s.url)}" target="_blank" rel="noopener noreferrer">${e(s.url)} ↗</a><p>${e(s.note||'尚未完成原題與圖片核對。')}</p><p>${e(s.date?'最早對話 '+s.date:'加入日期 '+s.addedAt)} · ${data.questions.filter(q=>q.sourceId===s.id).length} 題已列入題庫</p></div><div class="source-actions">${s.transcript||s.content?`<button class="button" data-source-detail="${s.id}">檢視內容</button>`:''}</div></article>`).join('');}
function photoHTML(images){return images.length?'<div class="photo-grid">'+images.map((src,i)=>`<a href="${e(safeAsset(src))}" target="_blank" rel="noopener noreferrer" aria-label="開啟原卷第 ${i+1} 張"><img src="${e(safeAsset(src))}" alt="原卷預覽第 ${i+1} 張" loading="lazy"><span>${i+1} ↗</span></a>`).join('')+'</div>':'';}
function fullOptionAnalysis(q){
 if(!q.optionAnalysis?.length)return '';
 const correct=q.correctOption||q.answer.match(/^正確答案：([A-D])/)?.[1];
 return `<section class="option-analysis" aria-label="逐項解析"><h3>逐項解析</h3><div class="option-table-wrap"><table><thead><tr><th scope="col">選項與原句</th><th scope="col">判讀</th><th scope="col">句意與判斷理由</th></tr></thead><tbody>${q.optionAnalysis.map(o=>`<tr class="${correct===o.label?'correct-option':''}"><th scope="row"><span class="choice-letter">${e(o.label)}</span>${renderText(o.text)}</th><td><strong>${e(o.wordClass)}</strong></td><td>${o.meaning?`<p>${renderText(o.meaning)}</p>`:''}<p>${renderText(o.explanation)}</p></td></tr>`).join('')}</tbody></table></div></section>`;
}
function questionMaterials(q){return `${q.passage?`<section class="reading-passage"><h3>作答所需文章／材料</h3><p>${renderText(q.passage)}</p></section>`:''}${(q.tables||[]).map(t=>`<div class="question-table"><table>${t.caption?`<caption>${e(t.caption)}</caption>`:''}<thead><tr>${t.headers.map(h=>`<th scope="col">${e(h)}</th>`).join('')}</tr></thead><tbody>${t.rows.map(row=>`<tr>${row.map(cell=>`<td>${renderText(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`).join('')}${(q.questionFigures||[]).map(f=>`<figure class="question-figure"><img src="${e(safeAsset(f.src))}" alt="${e(f.alt)}">${f.caption?`<figcaption>${e(f.caption)}</figcaption>`:''}</figure>`).join('')}`;}
function explanationFigures(q){return (q.explanationFigures||[]).map(f=>`<figure class="question-figure explanation-figure${f.src.startsWith('assets/comics/')?' teaching-comic':''}"><a href="${e(safeAsset(f.src))}" target="_blank" rel="noopener noreferrer"><img src="${e(safeAsset(f.src))}" alt="${e(f.alt)}" loading="lazy"></a>${f.caption?`<figcaption>${e(f.caption)}</figcaption>`:''}</figure>`).join('');}
function sourceEvidence(q){return `<section class="modal-source-images"><h3>原圖（僅本題）</h3>${q.images.length?q.images.map(path=>`<a class="question-evidence" href="${e(safeAsset(path))}" target="_blank" rel="noopener noreferrer"><img src="${e(safeAsset(path))}" alt="${e(q.sourceLabel||q.title)}原卷截圖" loading="lazy"></a>`).join(''):q.contentStatus==='完整原題'?'<p class="muted">'+(q.questionFigures?.length?'作答附圖已列在題目中，重繪圖已註明；此處尚無另存的原卷截圖。':'本題為文字來源，沒有原始附圖。')+'</p>':'<p class="muted">尚未取得可核對的原圖。此題保留待更新，未以推測補齊。</p>'}</section>`;}
function reviewRequests(q,s){
 if(!q.reviewQuestions?.length)return '';
 const previous=q.reviewPreviousId?`<a href="${questionHash(q.reviewPreviousId)}" data-question-nav="${e(q.reviewPreviousId)}">← 上一個待核對題目</a>`:'',next=q.reviewNextId?`<a href="${questionHash(q.reviewNextId)}" data-question-nav="${e(q.reviewNextId)}">下一個待核對題目 →</a>`:'';
 return `<section class="review-request" aria-labelledby="review-request-title"><div class="review-request-heading"><h2 id="review-request-title">請協助核對</h2><span>${e(q.reviewLabel)}</span></div><ol>${q.reviewQuestions.map(text=>`<li>${e(text)}</li>`).join('')}</ol>${q.reviewExcerpt?`<h3>目前保存的原始輸入（未訂正）</h3><div class="review-excerpt">${e(q.reviewExcerpt)}</div>`:''}${s?`<a class="review-source-link" href="${e(s.url)}" target="_blank" rel="noopener noreferrer">開啟原始對話 ↗</a>`:''}<nav class="review-queue-links" aria-label="優先核對題目">${previous}${next}</nav></section>`;
}
function renderDetail(id){const q=data.questions.find(q=>q.id===id);if(!q)return;activeId=id;const s=data.sources.find(s=>s.id===q.sourceId),complete=q.contentStatus==='完整原題';
 $('detail').innerHTML=`<header class="detail-header">${markButtons(q,true)}<div class="detail-subject">${badge(q.subject)}</div><h1>${e(displayTitle(q))}</h1><div class="detail-meta"><span>${e(q.volume)} / ${e(q.chapter)}</span><span>${e(q.dateLabel||'首次出題日期')} ${q.date}</span><span>加入 ${e(q.addedAt||'未記錄')}</span></div></header><div class="detail-content">${reviewRequests(q,s)}${!complete?'<div class="verification-note">待更新：尚未按完整原題標準核對。下方保留舊資料，不代表已驗證答案。</div>':''}${questionMaterials(q)}<p class="detail-question">${renderText(q.question)}</p><button class="answer-toggle" id="answer-toggle" aria-expanded="false" data-complete="true">先想一想，再查看答案、解說與原圖 <span>＋</span></button><div class="answer-panel" id="answer-panel" hidden>${q.studentAnswer?`<p class="original-response">原卷作答：<strong>${e(q.studentAnswer)}</strong></p>`:''}<h3>${renderText(q.answer||'尚未補上答案')}</h3>${fullOptionAnalysis(q)}<div class="explanation">${renderText(q.explanation)}</div>${renderTeachingComic(q.teachingComic)}${explanationFigures(q)}${q.trap?`<div class="trap"><strong>容易卡住的地方</strong><br>${renderText(q.trap)}</div>`:''}${q.verificationNote?`<p class="muted">核對註記：${e(q.verificationNote)}</p>`:''}${sourceEvidence(q)}</div><div class="question-footer-flags">${flagControls(q,'footer')}</div>${!complete&&s?`<div class="source-bottom"><a class="source-link" href="${e(s.url)}" target="_blank" rel="noopener noreferrer">開啟 ${e(s.platform)} 原始討論 ↗</a></div>`:''}</div>`;
 layoutTeachingComics($('detail'));
 updateQuestionBreadcrumb();
}
async function showTranscript(id){const s=data.sources.find(s=>s.id===id);const pre=$('transcript');if(!s||!pre)return;pre.hidden=false;pre.textContent='讀取中…';try{if(s.content)pre.textContent=s.content;else {const response=await fetch(safeAsset(s.transcript));if(!response.ok)throw Error('無法讀取');pre.textContent=await response.text();}}catch{pre.textContent='暫時無法讀取保存的對話。可開啟原始討論。';}}
function showSource(id){const s=data.sources.find(s=>s.id===id);if(!s)return;activeId='';$('source-detail').innerHTML=`<header class="detail-header"><div class="dialog-heading"><span class="eyebrow">LEARNING SOURCE</span><button class="icon-button" data-close aria-label="關閉來源">×</button></div><h2>${e(s.title)}</h2><a class="source-link" href="${e(s.url)}" target="_blank" rel="noopener noreferrer">開啟原始分享 ↗</a></header><div class="detail-content"><p class="muted">${e(s.note)}</p>${photoHTML(s.images)}<pre class="transcript" id="transcript"></pre></div>`;$('detail-dialog').showModal();showTranscript(id);}
function updateQuestionBreadcrumb(){
 const q=data.questions.find(q=>q.id===activeId);if(!q)return;
 const returnHash=history.state?.returnTo?.hash||listHash({subject:q.subject});
 $('breadcrumb').innerHTML=`<a href="#questions">我的學習空間</a><span>/</span><a href="${e(returnHash)}" data-question-return>${e(subject(q.subject).name)}</a><span>/</span><strong aria-current="page">${e(displayTitle(q))}</strong>`;
}
function listSnapshot(){return {hash:location.hash||'#questions',filters:{...filters},page,layout,scroll:window.scrollY};}
function navigateRoute(hash,state={}){history.pushState(state,'',hash);applyRoute();}
function showDetail(id){
 if(!data.questions.some(q=>q.id===id))return;
 if(activeId===id){renderDetail(id);return;}
 const returnTo=activeId?history.state?.returnTo:listSnapshot();
 if(!activeId)history.replaceState({listSnapshot:returnTo},'',location.href);
 navigateRoute(questionHash(id),{returnTo,fromList:!activeId||!!history.state?.fromList});
}
function applyRoute(){
 if(activeId&&$('toast').textContent.startsWith('已設定為')){clearTimeout(toastTimer);$('toast').classList.remove('show');$('toast').textContent='';}
 const route=parseRoute(location.hash),q=route.kind==='question'?data.questions.find(q=>q.id===route.id):null;activeId='';
 $('list-page').hidden=route.kind==='question';$('question-page').hidden=route.kind!=='question';$('content').classList.toggle('reading-question',route.kind==='question');
 if(route.kind==='question'){
  page='questions';filters={subject:q?.subject||'',issue:false,doubt:false};updateNav();
  if(q){renderDetail(q.id);document.title=displayTitle(q)+'｜WeiRuGo';}else{$('detail').innerHTML='<div class="empty"><h1>找不到這道題目</h1><p>請回錯題本確認題目網址。</p></div>';document.title='找不到題目｜WeiRuGo';}
  window.scrollTo(0,0);$('detail').focus({preventScroll:true});return;
 }
 const saved=history.state?.listSnapshot;
 if(saved&&saved.hash===(location.hash||'#questions')){filters={subject:saved.filters.subject||'',issue:!!saved.filters.issue,doubt:!!saved.filters.doubt};page=saved.page;layout=saved.layout;}
 else{page=route.kind==='sources'?'sources':route.kind==='progress'?'progress':'questions';filters={subject:route.subject||'',issue:route.kind==='issues',doubt:route.kind==='doubts'};}
 render();document.title='WeiRuGo';requestAnimationFrame(()=>window.scrollTo(0,saved?.hash===(location.hash||'#questions')?saved.scroll:0));
}
function changePage(action,subjectId=''){
 const hash=action==='source'?'#sources':action==='progress'?'#progress':action==='issue'?'#issues':action==='doubt'?'#doubts':listHash({subject:subjectId});navigateRoute(hash);
}
document.querySelector('.skip').addEventListener('click',ev=>{ev.preventDefault();$('content').focus();$('content').scrollIntoView();});
document.addEventListener('click',ev=>{const link=ev.target.closest('[data-question-return]');if(!link||ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;if(history.state?.returnTo){ev.preventDefault();navigateRoute(link.hash,{listSnapshot:history.state.returnTo});}});
document.addEventListener('click',ev=>{
 const link=ev.target.closest('[data-question-nav]');if(link){if(ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;ev.preventDefault();showDetail(link.dataset.questionNav);return;}
 const b=ev.target.closest('button,[data-open]');if(!b)return;
 if(b.hasAttribute('data-close')){b.closest('dialog').close();return;}
 if(b.dataset.nav){changePage(b.dataset.nav);return;}if(b.dataset.subject){changePage('all',b.dataset.subject);return;}
 if(b.hasAttribute('data-article-flag')){setArticleFlag(activeId,Number(b.dataset.articleFlag));return;}
 if(b.hasAttribute('data-doubt')){toggleDoubt(b.dataset.doubt);return;}
 if(b.dataset.open){if(ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;ev.preventDefault();showDetail(b.dataset.open);return;}
 if(b.dataset.sourceDetail){showSource(b.dataset.sourceDetail);return;}if(b.dataset.transcript){showTranscript(b.dataset.transcript);return;}
 if(b.id==='clear-filters'){selectedFlags=new Set([3,4,5]);render();}
});
document.addEventListener('change',ev=>{if(ev.target.matches('[data-flag-filter]')){const value=Number(ev.target.dataset.flagFilter);if(ev.target.checked)selectedFlags.add(value);else selectedFlags.delete(value);render();document.querySelector('[data-flag-filter="'+value+'"]')?.focus({preventScroll:true});}});
document.addEventListener('keydown',ev=>{if((ev.key==='Enter'||ev.key===' ')&&ev.target.matches('[data-open]')){ev.preventDefault();showDetail(ev.target.dataset.open);}});
document.addEventListener('keydown',ev=>{
 if(!activeId||ev.repeat||ev.isComposing||ev.ctrlKey||ev.metaKey||ev.altKey)return;
 if(ev.target instanceof Element&&ev.target.closest('input,textarea,select,[contenteditable]:not([contenteditable="false"]),[role="textbox"],dialog[open]'))return;
 if(/^[1-5]$/.test(ev.key)){ev.preventDefault();setArticleFlag(activeId,Number(ev.key));return;}
 if(ev.target.closest?.('[data-article-flag]')&&['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(ev.key)){
  ev.preventDefault();const current=flagFor(activeId),next=ev.key==='Home'?1:ev.key==='End'?5:(current-1+(['ArrowLeft','ArrowUp'].includes(ev.key)?4:1))%5+1;setArticleFlag(activeId,next);
 }
});
$('detail').addEventListener('click',ev=>{if(ev.target.closest('#answer-toggle')){const show=$('answer-panel').hidden;$('answer-panel').hidden=!show;$('answer-toggle').setAttribute('aria-expanded',show);const complete=$('answer-toggle').dataset.complete==='true';$('answer-toggle').innerHTML=complete?(show?'收起答案、解說與原圖 <span>−</span>':'先想一想，再查看答案、解說與原圖 <span>＋</span>'):(show?'收起解題筆記 <span>−</span>':'先想一想，再看解題筆記 <span>＋</span>');}});
$('grid-view').onclick=()=>{layout='grid';render();};$('list-view').onclick=()=>{layout='list';render();};
for(const d of document.querySelectorAll('dialog'))d.addEventListener('click',ev=>{if(ev.target===d){const r=d.getBoundingClientRect();if(ev.clientX<r.left||ev.clientX>r.right||ev.clientY<r.top||ev.clientY>r.bottom)d.close();}});
window.addEventListener('hashchange',()=>{if(data)applyRoute();});if('scrollRestoration' in history)history.scrollRestoration='manual';
async function start(){try{
 const response=await fetch('data.json');if(!response.ok)throw Error('題庫讀取失敗');data=await response.json();
 const updated=formatDataUpdatedAt(data.dataUpdatedAt);if(updated){$('data-updated-time').textContent=updated;$('data-updated-time').dateTime=data.dataUpdatedAt;$('data-updated').hidden=false;}
 let legacyDoubts=[];try{legacyDoubts=discardLegacyMarks(localStorage);}catch{toast('瀏覽器無法清除舊標記。');}
 try{flags=checkedFlags(JSON.parse(userStorage.getItem(FLAGS_KEY)||'{}'));practice=checkedPractice(JSON.parse(userStorage.getItem(PRACTICE_KEY)||'[]'));doubts=new Set(loadDoubts(userStorage));}catch{toast('無法讀取本機標記；題目仍可正常閱讀。');}
 for(const q of data.questions)q.doubted=hasQuestionMark(doubts,q.id);applyRoute();
 markSync=new FlagSync({storage:userStorage,getToken:()=>session.token,getLocal:()=>({flags,practice,doubts:[...doubts]}),apply:applySyncedMarks,status:syncStatus});
 if(markSync.localOnly)syncStatus('local');if(legacyDoubts.length)markSync.queueAll(legacyDoubts);
 const refresh=()=>{if(document.visibilityState!=='hidden'&&markSync.available!==false)void markSync.refresh();};
 $('sync-status').onclick=()=>{markSync.available=null;void markSync.refresh();};window.addEventListener('focus',refresh);window.addEventListener('online',()=>{markSync.available=null;refresh();});document.addEventListener('visibilitychange',refresh);
 window.addEventListener('storage',event=>{if(userStorage.ownsKey(event.key)){try{applySyncedMarks({flags:JSON.parse(userStorage.getItem(FLAGS_KEY)||'{}'),practice:JSON.parse(userStorage.getItem(PRACTICE_KEY)||'[]'),doubts:loadDoubts(userStorage)});}catch{}refresh();}});
 setInterval(refresh,60000);refresh();
 }catch(error){$('results').innerHTML='<div class="empty"><h3>暫時無法開啟錯題本</h3><p>請重新整理頁面，或確認網站資料檔案是否完整。</p></div>';console.error(error);}}
async function bootAuth(){
 session=await restoreSession(localStorage);
 if(!session){$('signin-screen').hidden=false;$('app-shell').hidden=true;document.body.classList.remove('auth-pending');return;}
 userStorage=accountStorage(localStorage,session.user);$('account-name').textContent=session.user;
 $('signin-screen').hidden=true;$('app-shell').hidden=false;document.body.classList.remove('auth-pending');await start();
}
$('signin-form').addEventListener('submit',async event=>{
 event.preventDefault();const button=$('signin-submit');button.disabled=true;button.textContent='Signing in…';$('signin-error').textContent='';
 try{await signIn(localStorage,$('signin-user').value,$('signin-password').value);$('signin-password').value='';location.reload();}
 catch(error){$('signin-error').textContent=error.message||'暫時無法Sign In。';}finally{button.disabled=false;button.textContent='Sign In';}
});
$('sign-out').addEventListener('click',async()=>{$('app-shell').hidden=true;$('signin-screen').hidden=false;for(const id of ['signin-user','signin-password','signin-submit'])$(id).disabled=true;$('signin-submit').textContent='Signing out…';await signOut(localStorage,session);history.replaceState({},'','#questions');location.reload();});
window.addEventListener('storage',event=>{if(event.key===SESSION_KEY)location.reload();});
bootAuth();
