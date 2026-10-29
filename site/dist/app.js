import {renderTeachingComic,layoutTeachingComics} from './teaching-comic.js';
import {escapeHTML as e,safeAsset,selectQuestions,needsReview} from './core.js';
import {FAVORITES_KEY,favoriteIDs,loadFavorites} from './favorites.js';
import {parseRoute,questionHash,listHash} from './routes.js';
import {DOUBTS_KEY,loadDoubts,ANSWERED_KEY,loadAnswered,persistMarks} from './marks.js';
import {MarkSync} from './mark-sync.js';
import {hasQuestionMark,toggleQuestionMark} from './question-identity.js';
const $=id=>document.getElementById(id);
let data,filters={subject:'',search:'',volume:'',chapter:'',status:'',answered:'',sort:'newest',starred:false,issue:false,doubt:false},page='questions',layout='list',activeId='',toastTimer,favorites=new Set(),doubts=new Set(),answered=new Set();
let markSync;
// Keep this visit's rows visible so an accidental unstar can be undone in place.
// Actual marks still save and sync immediately; this set is never persisted.
let favoriteVisitIds=null;
function syncStatus(state){
 const labels={syncing:'標記同步中…',synced:'標記已同步雲端',pending:'本機已存，待同步',local:'標記存在此瀏覽器'};
 const button=$('sync-status');button.textContent=labels[state]||labels.local;button.dataset.state=state;
 button.title=state==='local'?'本機模式；部署Netlify Functions後可同步。點擊可重試。':state==='pending'?'標記已暫存，連線恢復後自動重試；點擊也可重試。':'單一使用者，共用同一份收藏、疑義與已作標記。點擊可立即同步。';
 document.querySelector('.storage-dot').dataset.state=state;
}
function applySyncedMarks(incoming){
 incoming.answered??=[];
 if(JSON.stringify([...favorites].sort())===JSON.stringify(incoming.favorites)&&JSON.stringify([...doubts].sort())===JSON.stringify(incoming.doubts)&&JSON.stringify([...answered].sort())===JSON.stringify(incoming.answered))return;
 try{persistMarks(localStorage,incoming.favorites,incoming.doubts,incoming.answered);}catch{}
 favorites=new Set(incoming.favorites);doubts=new Set(incoming.doubts);answered=new Set(incoming.answered);
 for(const q of data.questions){q.starred=hasQuestionMark(favorites,q.id);q.doubted=hasQuestionMark(doubts,q.id);q.answered=hasQuestionMark(answered,q.id);}
 render();
 // Change the three icons only; keep the answer panel, scroll and reading position.
 if(activeId){const q=data.questions.find(q=>q.id===activeId),actions=document.querySelector('#detail .detail-actions');if(q&&actions)actions.outerHTML=markButtons(q,true);}
}
function syncImportedMarks(beforeFavorites,beforeDoubts,beforeAnswered=answered){
 if(!markSync)return;const operations=[];
 for(const [kind,before,after] of [['favorite',beforeFavorites,favorites],['doubt',beforeDoubts,doubts],['answered',beforeAnswered,answered]])for(const id of new Set([...before,...after]))if(before.has(id)!==after.has(id))operations.push({kind,id,on:after.has(id)});
 if(operations.length)markSync.queueAll(operations);
}
const icon={all:'▦',star:'☆',source:'↙',issue:'◷'};
function toast(message){$('toast').textContent=message;$('toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('show'),3500);}
function saveFavorites(ids){try{const checked=favoriteIDs([...ids]);localStorage.setItem(FAVORITES_KEY,JSON.stringify(checked));favorites=new Set(checked);for(const q of data.questions)q.starred=hasQuestionMark(favorites,q.id);return true;}catch{toast('瀏覽器無法儲存收藏，請檢查儲存空間或瀏覽器設定。');return false;}}
function toggleFavorite(id){const before=new Set(favorites),next=toggleQuestionMark(favorites,id);if(!saveFavorites(next))return;syncImportedMarks(before,doubts);render();if(activeId){const b=document.querySelector('[data-detail-star]'),selected=hasQuestionMark(favorites,activeId);b.classList.toggle('selected',selected);b.textContent=selected?'★':'☆';b.title=selected?'取消收藏':'加入收藏';b.setAttribute('aria-pressed',selected);b.setAttribute('aria-label',selected?'取消收藏':'加入收藏');}}


function saveDoubts(ids){try{const checked=favoriteIDs([...ids]);localStorage.setItem(DOUBTS_KEY,JSON.stringify(checked));doubts=new Set(checked);for(const q of data.questions)q.doubted=hasQuestionMark(doubts,q.id);return true;}catch{toast('瀏覽器無法儲存疑義標記，請檢查瀏覽器設定。');return false;}}
function toggleDoubt(id){const before=new Set(doubts),next=toggleQuestionMark(doubts,id);if(!saveDoubts(next))return;syncImportedMarks(favorites,before);render();if(activeId){const b=document.querySelector('#detail [data-doubt]'),selected=hasQuestionMark(doubts,activeId);b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',selected);b.setAttribute('aria-label',selected?'取消疑義標記':'標記疑義，待老師確認');b.title=selected?'已標記疑義，點擊取消':'標記疑義，待老師確認';}}
function saveAnswered(ids){try{const checked=favoriteIDs([...ids]);localStorage.setItem(ANSWERED_KEY,JSON.stringify(checked));answered=new Set(checked);for(const q of data.questions)q.answered=hasQuestionMark(answered,q.id);return true;}catch{toast('瀏覽器無法儲存已作標記，請檢查儲存空間或瀏覽器設定。');return false;}}
function toggleAnswered(id){const before=new Set(answered),next=toggleQuestionMark(answered,id);if(!saveAnswered(next))return;syncImportedMarks(favorites,doubts,before);render();if(activeId){const q=data.questions.find(q=>q.id===activeId),actions=document.querySelector('#detail .detail-actions');if(q&&actions)actions.outerHTML=markButtons(q,true);}}
const answeredIcon="<svg class=\"tasklist-icon\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path class=\"tasklist-check\" d=\"M17.28 9.28a.75.75 0 00-1.06-1.06l-5.97 5.97-2.47-2.47a.75.75 0 00-1.06 1.06l3 3a.75.75 0 001.06 0l6.5-6.5z\"/><path fill-rule=\"evenodd\" d=\"M3.75 2A1.75 1.75 0 002 3.75v16.5c0 .966.784 1.75 1.75 1.75h16.5A1.75 1.75 0 0022 20.25V3.75A1.75 1.75 0 0020.25 2H3.75zM3.5 3.75a.25.25 0 01.25-.25h16.5a.25.25 0 01.25.25v16.5a.25.25 0 01-.25.25H3.75a.25.25 0 01-.25-.25V3.75z\"/></svg>";
const doubtIcon="<svg class=\"question-mark-icon\" viewBox=\"230 65 560 900\" aria-hidden=\"true\" focusable=\"false\"><path class=\"question-shape\" d=\"M715.720415 207.522102C675.902539 136.26685 603.803606 95.397443 518.015326 95.397443c-129.594189 0-205.287984 72.306782-238.682003 195.401348-20.885213 76.845665 110.976883 131.618411 140.38594 27.173916 15.792407-56.028029 37.099461-79.499576 98.296063-79.499576 33.883437 0 58.475115 13.134401 72.864799 38.912762 15.649063 28.014526 14.18286 62.384309 3.633769 79.571248-17.119363 27.874254-35.489913 44.013758-56.72939 62.663829-44.432528 39.05201-99.619947 88.864031-99.619946 221.809398 0 70.489385 71.537844 71.537844 71.537843 71.537844 39.470779 0 71.537844-32.067064 71.537844-71.537844 0-69.581199 14.880125-82.643928 50.856384-114.224647 25.013518-21.933671 55.960452-49.11066 84.325148-95.35956 39.677604-64.691123 39.399107-152.714544-0.701362-224.324059z\"/><path class=\"question-highlight\" d=\"M670.72987 403.764058c-24.240485 39.399107-50.648535 62.595229-73.980834 83.134369-40.172141 35.210392-69.16243 60.710256-69.16243 154.531941 0 9.850801-7.965828 17.884205-17.884205 17.884205-9.850801 0-17.884205-8.033404-17.884205-17.884205 0-110.031836 39.470779-144.68114 81.316973-181.430432 22.494761-19.769178 45.759483-40.168045 67.066536-74.960692 22.355512-36.326427 21.307054-91.374598-2.514662-133.850481-23.893388-42.758475-66.436847-66.369271-119.671717-66.369271-86.768138 0-134.762763 39.12061-150.969843 123.022894-1.884973 9.711552-11.213592 16.070904-20.925144 14.182859-9.711552-1.884973-16.067832-11.245333-14.181836-20.956885 19.493753-100.879326 82.05417-152.017278 186.076823-152.017278 66.78804 0 120.368983 30.11042 150.898172 84.672245 30.32134 54.071384 31.018606 122.393204 1.816372 170.040731z\"/><path class=\"question-shape\" d=\"M513.19385 757.121218c-47.433535 0-85.859952 38.423345-85.859951 85.859952 0 47.433535 38.426416 85.859952 85.859951 85.859952 47.364935 0 85.791351-38.426416 85.791352-85.859952 0-47.436607-38.426416-85.859952-85.791352-85.859952z\"/><path class=\"question-highlight\" d=\"M513.19385 875.187483c-17.812533 0-32.206313-14.39378-32.206313-32.206313 0-17.744957 14.39378-32.206313 32.206313-32.206313 17.744957 0 32.138736 14.461356 32.138737 32.206313-0.001024 17.812533-14.39378 32.206313-32.138737 32.206313z\"/></svg>";
function markButtons(q,detail=false){const doubt=hasQuestionMark(doubts,q.id),done=hasQuestionMark(answered,q.id),task=`<button class="answered-button ${done?'selected':''}" data-answered="${q.id}" aria-pressed="${done}" aria-label="${done?'已作，點擊標為未作':'未作，點擊標為已作'}" title="${done?'已作，點擊標為未作':'未作，點擊標為已作'}">${answeredIcon}</button>`,star=`<button class="${detail?'favorite-button':'star'} ${q.starred?'selected':''}" ${detail?'data-detail-star':'data-star'}="${q.id}" aria-pressed="${q.starred}" aria-label="${q.starred?'取消收藏':'加入收藏'}" title="${q.starred?'取消收藏':'加入收藏'}">${q.starred?'★':'☆'}</button>`;if(!detail)return star;return `<div class="question-actions detail-actions">${task}${star}<button class="doubt-button ${doubt?'selected':''}" data-doubt="${q.id}" aria-pressed="${doubt}" aria-label="${doubt?'取消疑義標記':'標記疑義，待老師確認'}" title="${doubt?'已標記疑義，點擊取消':'標記疑義，待老師確認'}">${doubtIcon}</button></div>`;}


function displayTitle(q){return q.title+(q.contentStatus==='待更新'?'（待更新）':'');}
function subject(id){return data.subjects.find(s=>s.id===id)||{id,name:'未分類',publisher:'',icon:'?'};}
function badge(id){const s=subject(id);return `<span class="subject-badge ${e(id)}"><span>${e(s.icon)}</span> ${e(s.name)}</span>`;}
function navButton(action,label,symbol,count,active){return `<button class="nav-item ${active?'active':''}" data-nav="${action}" ${active?'aria-current="page"':''}><span class="nav-symbol">${symbol}</span>${label}<span class="count">${count}</span></button>`;}
function updateNav(){const pending=data.sources.filter(s=>s.status==='pending').length,issues=data.questions.filter(needsReview).length,doubtCount=data.questions.filter(q=>hasQuestionMark(doubts,q.id)).length;
 $('main-nav').innerHTML=navButton('all','全部錯題',icon.all,data.questions.length,page==='questions'&&!filters.starred&&!filters.subject&&!filters.issue&&!filters.doubt)+navButton('star','重點收藏',icon.star,data.questions.filter(q=>q.starred).length,filters.starred)+(doubtCount?navButton('doubt','有疑義的題目','?',doubtCount,filters.doubt):'')+(pending?navButton('source','匯入紀錄',icon.source,pending,page==='sources'):'')+(issues?navButton('issue','待核對原題',icon.issue,issues,filters.issue):'');
 const route=parseRoute(location.hash),current=route.kind==='question'?data.questions.find(q=>q.id===route.id):null,nav=$('subjects');
 document.querySelector('.sidebar').classList.toggle('reading-question',!!current);
 nav.classList.toggle('question-nav',!!current);
 if(current){
  const saved=history.state?.returnTo?.filters;
  let qs=selectQuestions(data.questions,{...(saved||{sort:'newest'}),subject:current.subject});
  if(!qs.some(q=>q.id===current.id))qs=selectQuestions(data.questions,{subject:current.subject,sort:saved?.sort||'newest'});
  $('subject-heading').innerHTML=`${e(subject(current.subject).name)} <span>${qs.length}</span>`;
  nav.setAttribute('aria-label',subject(current.subject).name+'題目導覽');
  nav.innerHTML=qs.map(q=>`<a class="nav-item question-nav-link ${q.id===current.id?'active':''}" href="${questionHash(q.id)}" data-question-nav="${q.id}" ${q.id===current.id?'aria-current="page"':''}>${e(displayTitle(q))}</a>`).join('');
 }else{
  $('subject-heading').innerHTML=`依科目瀏覽 <span>${data.subjects.length}</span>`;
  nav.setAttribute('aria-label','科目分類');
  nav.innerHTML=data.subjects.map(s=>`<button class="nav-item ${filters.subject===s.id?'active':''}" data-subject="${s.id}" ${filters.subject===s.id?'aria-current="page"':''}><span class="subject-icon">${e(s.icon)}</span><span class="subject-name">${e(s.name)}<small>${e(s.id==='Physics-Chemistry'?'Physics':s.id)}</small></span><span class="count">${data.questions.filter(q=>q.subject===s.id).length}</span></button>`).join('');
 }
 const label=page==='sources'?'匯入紀錄':filters.subject?subject(filters.subject).name:filters.starred?'重點收藏':filters.doubt?'有疑義的題目':filters.issue?'待核對原題':'全部錯題';$('breadcrumb').innerHTML=`<a href="#questions">我的學習空間</a><span>/</span><strong aria-current="page">${e(label)}</strong>`;
}
function diagram(type){const wrap=body=>`<div class="card-art" aria-label="輔助示意圖，非原始題圖"><svg viewBox="0 0 300 160" role="img" aria-label="${type==='square'?'正方形與內點示意':type==='trapezoid'?'梯形高與底邊示意':'垂直等長但不互相平分的對角線反例'}"><g fill="none" stroke="#91a785" stroke-width="1.5">${body}</g></svg></div>`;
 if(type==='square')return wrap('<path d="M90 20h120v120H90z" fill="#edf2e9"/><path d="m90 20 32 28 88-28M122 48 88 92" stroke-dasharray="4 4"/><circle cx="122" cy="48" r="3" fill="#718b63"/><g fill="#7d9270" stroke="none" font-size="12" font-family="Georgia"><text x="77" y="17">A</text><text x="215" y="20">B</text><text x="215" y="150">C</text><text x="77" y="151">D</text><text x="125" y="43">P</text><text x="95" y="36">1</text><text x="163" y="26">3</text><text x="82" y="83">√7</text></g>');
 if(type==='trapezoid')return wrap('<path d="m70 130 45-100h42l93 100z" fill="#edf2e9"/><path d="M115 30v100" stroke-dasharray="4 4"/><path d="M115 120h10v10"/><g fill="#7d9270" stroke="none" font-size="12" font-family="Georgia"><text x="132" y="23">1</text><text x="151" y="148">4</text><text x="80" y="78">2</text><text x="209" y="78">3</text><text x="119" y="85">h</text></g>');
 if(type==='diagonals')return wrap('<path d="m150 12 74 108-74 35-74-35z" fill="#edf2e9"/><path d="M150 12v143M76 120h148" stroke-dasharray="4 4"/><path d="M150 111h9v9"/><g fill="#7d9270" stroke="none" font-size="12" font-family="Georgia"><text x="146" y="10">A</text><text x="230" y="124">B</text><text x="145" y="158">C</text><text x="63" y="124">D</text><text x="155" y="71">3</text><text x="155" y="141">1</text><text x="183" y="115">2</text><text x="110" y="115">2</text></g>');return '';}
function updateSelects(){$('answered-filter').value=filters.answered||'';const scoped=data.questions.filter(q=>!filters.subject||q.subject===filters.subject);const volumes=[...new Set(scoped.map(q=>q.volume))].sort();if(!volumes.includes(filters.volume))filters.volume='';$('volume-filter').innerHTML='<option value="">所有冊次</option>'+volumes.map(v=>`<option ${filters.volume===v?'selected':''}>${e(v)}</option>`).join('');
 const chapters=[...new Set(scoped.filter(q=>!filters.volume||q.volume===filters.volume).map(q=>q.chapter))].sort((a,b)=>a.localeCompare(b,'zh-Hant'));if(!chapters.includes(filters.chapter))filters.chapter='';$('chapter-filter').innerHTML='<option value="">所有章節</option>'+chapters.map(v=>`<option ${filters.chapter===v?'selected':''}>${e(v)}</option>`).join('');}
function render(){updateNav();if(activeId){updateQuestionBreadcrumb();return;}const sources=page==='sources';$('question-tools').hidden=sources;$('grid-view').parentElement.hidden=sources;
 $('page-title').textContent=sources?'匯入紀錄':filters.starred?'重點收藏':filters.doubt?'有疑義的題目':filters.issue?'待核對原題':filters.subject?subject(filters.subject).name:'全部錯題';
 if(sources){renderSources();return;}
 updateSelects();
 let candidates=data.questions,selection=filters;
 if(filters.starred){
  favoriteVisitIds??=new Set();
  for(const q of candidates)if(q.starred)favoriteVisitIds.add(q.id);
  candidates=candidates.filter(q=>favoriteVisitIds.has(q.id));
  selection={...filters,starred:false};
 }
 const qs=selectQuestions(candidates,selection);

 $('results').className=layout==='grid'?'question-grid':'question-list';
 $('results').innerHTML=qs.length?qs.map(q=>`<article class="question-card"><div class="card-main" role="link" tabindex="0" data-open="${q.id}" aria-label="閱讀 ${e(displayTitle(q))}"><div class="card-top">${badge(q.subject)}${markButtons(q)}</div><div class="card-location">${e(q.volume)} <span>/</span> ${e(q.chapter)}</div><h3><a href="${questionHash(q.id)}">${e(displayTitle(q))}</a></h3>${diagram(q.diagram)}<p class="question-preview">${e(q.question)}</p><div class="tags">${q.tags.slice(0,3).map(t=>`<span class="tag"># ${e(t)}</span>`).join('')}</div>${needsReview(q)?`<div class="issue-label">◌ ${e(q.contentStatus==='待更新'?'待更新':q.verification)}</div>`:q.verification==='已更正'?'<div class="issue-label" style="color:#7a9566">✓ 已更正原 AI 解答</div>':''}</div><div class="card-foot"><span class="card-date" title="${e(q.dateLabel||'首次出題日期')}：依目前來源最早可確認日期">◷ ${q.date.replaceAll('-','.')} </span><span aria-hidden="true">↗</span></div></article>`).join(''):`<div class="empty" style="grid-column:1/-1"><div class="empty-mark">a fresh page.</div><h3>${filters.subject&&!data.questions.some(q=>q.subject===filters.subject)?'這個科目的錯題本，等你開始。':'目前沒有符合條件的題目'}</h3><p>${filters.subject?'可以調整搜尋與篩選條件。':'試試其他關鍵字，或清除篩選條件。'}</p><button class="button clear-button" id="clear-filters">清除篩選</button></div>`;
 $('grid-view').classList.toggle('active',layout==='grid');$('list-view').classList.toggle('active',layout==='list');$('grid-view').setAttribute('aria-pressed',layout==='grid');$('list-view').setAttribute('aria-pressed',layout==='list');
}
function renderSources(){const pending=data.sources.filter(s=>s.status==='pending');$('results').className='source-list';$('results').innerHTML=(pending.length?`<div class="source-banner">${pending.length} 個來源尚未整理完成。</div>`:'<div class="empty-state">目前沒有待整理來源。</div>')+pending.map(s=>`<article class="source-card"><div class="source-platform">${s.platform==='Gemini'?'✧':'◎'}</div><div class="source-info"><h3>${e(s.title||'等待整理的學習討論')} <span class="tag">待整理</span></h3><a class="source-url" href="${e(s.url)}" target="_blank" rel="noopener noreferrer">${e(s.url)} ↗</a><p>${e(s.note||'尚未完成原題與圖片核對。')}</p><p>${e(s.date?'最早對話 '+s.date:'加入日期 '+s.addedAt)} · ${data.questions.filter(q=>q.sourceId===s.id).length} 題已列入題庫</p></div><div class="source-actions">${s.transcript||s.content?`<button class="button" data-source-detail="${s.id}">檢視內容</button>`:''}</div></article>`).join('');}
function photoHTML(images){return images.length?'<div class="photo-grid">'+images.map((src,i)=>`<a href="${e(safeAsset(src))}" target="_blank" rel="noopener noreferrer" aria-label="開啟原卷第 ${i+1} 張"><img src="${e(safeAsset(src))}" alt="原卷預覽第 ${i+1} 張" loading="lazy"><span>${i+1} ↗</span></a>`).join('')+'</div>':'';}
function fullOptionAnalysis(q){
 if(!q.optionAnalysis?.length)return '';
 const correct=q.correctOption||q.answer.match(/^正確答案：([A-D])/)?.[1];
 return `<section class="option-analysis" aria-label="逐項解析"><h3>逐項解析</h3><div class="option-table-wrap"><table><thead><tr><th scope="col">選項與原句</th><th scope="col">判讀</th><th scope="col">句意與判斷理由</th></tr></thead><tbody>${q.optionAnalysis.map(o=>`<tr class="${correct===o.label?'correct-option':''}"><th scope="row"><span class="choice-letter">${e(o.label)}</span>${e(o.text)}</th><td><strong>${e(o.wordClass)}</strong></td><td>${o.meaning?`<p>${e(o.meaning)}</p>`:''}<p>${e(o.explanation)}</p></td></tr>`).join('')}</tbody></table></div></section>`;
}
function questionMaterials(q){return `${q.passage?`<section class="reading-passage"><h3>作答所需文章／材料</h3><p>${e(q.passage)}</p></section>`:''}${(q.tables||[]).map(t=>`<div class="question-table"><table>${t.caption?`<caption>${e(t.caption)}</caption>`:''}<thead><tr>${t.headers.map(h=>`<th scope="col">${e(h)}</th>`).join('')}</tr></thead><tbody>${t.rows.map(row=>`<tr>${row.map(cell=>`<td>${e(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`).join('')}${(q.questionFigures||[]).map(f=>`<figure class="question-figure"><img src="${e(safeAsset(f.src))}" alt="${e(f.alt)}">${f.caption?`<figcaption>${e(f.caption)}</figcaption>`:''}</figure>`).join('')}`;}
function explanationFigures(q){return (q.explanationFigures||[]).map(f=>`<figure class="question-figure explanation-figure${f.src.startsWith('assets/comics/')?' teaching-comic':''}"><a href="${e(safeAsset(f.src))}" target="_blank" rel="noopener noreferrer"><img src="${e(safeAsset(f.src))}" alt="${e(f.alt)}" loading="lazy"></a>${f.caption?`<figcaption>${e(f.caption)}</figcaption>`:''}</figure>`).join('');}
function sourceEvidence(q){return `<section class="modal-source-images"><h3>原圖（僅本題）</h3>${q.images.length?q.images.map(path=>`<a class="question-evidence" href="${e(safeAsset(path))}" target="_blank" rel="noopener noreferrer"><img src="${e(safeAsset(path))}" alt="${e(q.sourceLabel||q.title)}原卷截圖" loading="lazy"></a>`).join(''):q.contentStatus==='完整原題'?'<p class="muted">'+(q.questionFigures?.length?'作答附圖已列在題目中，重繪圖已註明；此處尚無另存的原卷截圖。':'本題為文字來源，沒有原始附圖。')+'</p>':'<p class="muted">尚未取得可核對的原圖。此題保留待更新，未以推測補齊。</p>'}</section>`;}
function reviewRequests(q,s){
 if(!q.reviewQuestions?.length)return '';
 const previous=q.reviewPreviousId?`<a href="${questionHash(q.reviewPreviousId)}" data-question-nav="${e(q.reviewPreviousId)}">← 上一個待核對題目</a>`:'',next=q.reviewNextId?`<a href="${questionHash(q.reviewNextId)}" data-question-nav="${e(q.reviewNextId)}">下一個待核對題目 →</a>`:'';
 return `<section class="review-request" aria-labelledby="review-request-title"><div class="review-request-heading"><h2 id="review-request-title">請協助核對</h2><span>${e(q.reviewLabel)}</span></div><ol>${q.reviewQuestions.map(text=>`<li>${e(text)}</li>`).join('')}</ol>${q.reviewExcerpt?`<h3>目前保存的原始輸入（未訂正）</h3><div class="review-excerpt">${e(q.reviewExcerpt)}</div>`:''}${s?`<a class="review-source-link" href="${e(s.url)}" target="_blank" rel="noopener noreferrer">開啟原始對話 ↗</a>`:''}<nav class="review-queue-links" aria-label="優先核對題目">${previous}${next}</nav></section>`;
}
function renderDetail(id){const q=data.questions.find(q=>q.id===id);if(!q)return;activeId=id;const s=data.sources.find(s=>s.id===q.sourceId),complete=q.contentStatus==='完整原題';
 $('detail').innerHTML=`<header class="detail-header">${markButtons(q,true)}<div class="detail-subject">${badge(q.subject)}</div><h1>${e(displayTitle(q))}</h1><div class="detail-meta"><span>${e(q.volume)} / ${e(q.chapter)}</span><span>${e(q.dateLabel||'首次出題日期')} ${q.date}</span><span>加入 ${e(q.addedAt||'未記錄')}</span></div></header><div class="detail-content">${reviewRequests(q,s)}${!complete?'<div class="verification-note">待更新：尚未按完整原題標準核對。下方保留舊資料，不代表已驗證答案。</div>':''}${questionMaterials(q)}<p class="detail-question">${e(q.question)}</p><button class="answer-toggle" id="answer-toggle" aria-expanded="false" data-complete="true">先想一想，再查看答案、解說與原圖 <span>＋</span></button><div class="answer-panel" id="answer-panel" hidden>${q.studentAnswer?`<p class="original-response">原卷作答：<strong>${e(q.studentAnswer)}</strong></p>`:''}<h3>${e(q.answer||'尚未補上答案')}</h3>${fullOptionAnalysis(q)}<div class="explanation">${e(q.explanation)}</div>${renderTeachingComic(q.teachingComic)}${explanationFigures(q)}${q.trap?`<div class="trap"><strong>容易卡住的地方</strong><br>${e(q.trap)}</div>`:''}${q.verificationNote?`<p class="muted">核對註記：${e(q.verificationNote)}</p>`:''}${sourceEvidence(q)}</div><div class="source-bottom"><div>${complete?`<a class="source-link" href="${e(q.id)}.html" target="_blank" rel="noopener noreferrer">開啟本題單頁閱讀版 ↗</a>`:s?`<a class="source-link" href="${e(s.url)}" target="_blank" rel="noopener noreferrer">開啟 ${e(s.platform)} 原始討論 ↗</a>`:'<span class="muted">手動建立的題目</span>'}</div></div></div>`;
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
 const route=parseRoute(location.hash),q=route.kind==='question'?data.questions.find(q=>q.id===route.id):null;
 if(route.kind!=='starred')favoriteVisitIds=null;
 activeId='';
 $('list-page').hidden=route.kind==='question';$('question-page').hidden=route.kind!=='question';
 $('content').classList.toggle('reading-question',route.kind==='question');
 if(route.kind==='question'){
  page='questions';filters.subject=q?.subject||'';filters.starred=false;filters.issue=false;filters.doubt=false;updateNav();
  if(q){renderDetail(q.id);document.title=displayTitle(q)+'｜WeiRuGo';}
  else{$('detail').innerHTML='<div class="empty"><h1>找不到這道題目</h1><p>請回錯題本，確認題目是否仍在目前的題庫中。</p></div>';document.title='找不到題目｜WeiRuGo';}
  window.scrollTo(0,0);$('detail').focus({preventScroll:true});return;
 }
 const saved=history.state?.listSnapshot;
 if(saved&&saved.hash===(location.hash||'#questions')){filters={...saved.filters};page=saved.page;layout=saved.layout;}
 else {page=route.kind==='sources'?'sources':'questions';filters={...filters,subject:route.subject||'',starred:route.kind==='starred',issue:route.kind==='issues',doubt:route.kind==='doubts',status:'',answered:'',volume:'',chapter:'',search:''};}
 $('search').value=filters.search;$('sort').value=filters.sort;render();document.title='WeiRuGo';
 requestAnimationFrame(()=>window.scrollTo(0,saved?.hash===(location.hash||'#questions')?saved.scroll:0));
}
function changePage(action,subjectId=''){
 const hash=action==='source'?'#sources':action==='star'?'#starred':action==='issue'?'#issues':action==='doubt'?'#doubts':listHash({subject:subjectId});
 navigateRoute(hash);
}
document.querySelector('.skip').addEventListener('click',ev=>{ev.preventDefault();$('content').focus();$('content').scrollIntoView();});
document.addEventListener('click',ev=>{const link=ev.target.closest('[data-question-return]');if(!link||ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;if(history.state?.returnTo){ev.preventDefault();navigateRoute(link.hash,{listSnapshot:history.state.returnTo});}});

document.addEventListener('click',ev=>{const link=ev.target.closest('[data-question-nav]');if(link){if(ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;ev.preventDefault();showDetail(link.dataset.questionNav);return;}const b=ev.target.closest('button,[data-open]');if(!b)return;
 if(b.hasAttribute('data-close')){b.closest('dialog').close();return;}
 if(b.dataset.nav){changePage(b.dataset.nav);return;}if(b.dataset.subject){changePage('all',b.dataset.subject);return;}
 if(b.hasAttribute('data-answered')){ev.stopPropagation();toggleAnswered(b.dataset.answered);return;}
 if(b.hasAttribute('data-doubt')){ev.stopPropagation();toggleDoubt(b.dataset.doubt);return;}
 if(b.hasAttribute('data-star')){ev.stopPropagation();toggleFavorite(b.dataset.star);return;}
 if(b.dataset.detailStar){toggleFavorite(b.dataset.detailStar);return;}
 if(b.dataset.open){if(ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;ev.preventDefault();showDetail(b.dataset.open);return;}

 if(b.dataset.sourceDetail){showSource(b.dataset.sourceDetail);return;}if(b.dataset.transcript){showTranscript(b.dataset.transcript);return;}
 if(b.id==='clear-filters'){filters={...filters,search:'',status:'',answered:'',volume:'',chapter:''};$('search').value='';render();}
});
document.addEventListener('keydown',ev=>{if((ev.key==='Enter'||ev.key===' ')&&ev.target.matches('[data-open]')){ev.preventDefault();showDetail(ev.target.dataset.open);}});
$('detail').addEventListener('click',ev=>{if(ev.target.closest('#answer-toggle')){const show=$('answer-panel').hidden;$('answer-panel').hidden=!show;$('answer-toggle').setAttribute('aria-expanded',show);const complete=$('answer-toggle').dataset.complete==='true';$('answer-toggle').innerHTML=complete?(show?'收起答案、解說與原圖 <span>−</span>':'先想一想，再查看答案、解說與原圖 <span>＋</span>'):(show?'收起解題筆記 <span>−</span>':'先想一想，再看解題筆記 <span>＋</span>');}});
$('search').addEventListener('input',ev=>{filters.search=ev.target.value;render();});for(const [id,key] of [['answered-filter','answered'],['volume-filter','volume'],['chapter-filter','chapter'],['sort','sort']])$(id).onchange=ev=>{filters[key]=ev.target.value;if(key==='volume')filters.chapter='';render();};
$('grid-view').onclick=()=>{layout='grid';render();};$('list-view').onclick=()=>{layout='list';render();};

for(const d of document.querySelectorAll('dialog'))d.addEventListener('click',ev=>{if(ev.target===d){const r=d.getBoundingClientRect();if(ev.clientX<r.left||ev.clientX>r.right||ev.clientY<r.top||ev.clientY>r.bottom)d.close();}});
window.addEventListener('hashchange',()=>{if(data)applyRoute();});
if('scrollRestoration' in history)history.scrollRestoration='manual';
async function start(){try{const response=await fetch('data.json');if(!response.ok)throw Error('題庫讀取失敗');data=await response.json();
 try{favorites=new Set(loadFavorites(localStorage));}catch{toast('無法讀取本機收藏；題目仍可正常閱讀。');}
 try{doubts=new Set(loadDoubts(localStorage));}catch{toast('無法讀取本機疑義標記；題目仍可正常閱讀。');}
 try{answered=new Set(loadAnswered(localStorage));}catch{toast('無法讀取本機已作標記；題目仍可正常閱讀。');}
 for(const q of data.questions){q.starred=hasQuestionMark(favorites,q.id);q.doubted=hasQuestionMark(doubts,q.id);q.answered=hasQuestionMark(answered,q.id);}
 applyRoute();
 markSync=new MarkSync({storage:localStorage,getLocal:()=>({favorites:[...favorites],doubts:[...doubts],answered:[...answered]}),apply:applySyncedMarks,status:syncStatus});
 const refresh=()=>{if(document.visibilityState!=='hidden'&&markSync.available!==false)void markSync.refresh();};
 $('sync-status').onclick=()=>{markSync.available=null;void markSync.refresh();};
 window.addEventListener('focus',refresh);window.addEventListener('online',()=>{markSync.available=null;refresh();});document.addEventListener('visibilitychange',refresh);window.addEventListener('storage',event=>{if([FAVORITES_KEY,DOUBTS_KEY,ANSWERED_KEY].includes(event.key))refresh();});setInterval(refresh,60000);refresh();
 }catch(error){$('results').innerHTML='<div class="empty"><h3>暫時無法開啟錯題本</h3><p>請重新整理頁面，或確認網站資料檔案是否完整。</p></div>';console.error(error);}}
start();
