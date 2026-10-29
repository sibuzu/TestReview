export const STATUS = { todo: '待複習', learning: '加強中', mastered: '已掌握' };
export const SUBJECT_IDS = ['Chinese','English','Math','Biology','Physics-Chemistry','Earth','History','Geography','Civics'];
export function today() { return new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Taipei' }).format(new Date()); }
export function escapeHTML(v) { return String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
// Keep one printed pronunciation together without changing its characters.
// Use only for text content; attributes must continue to use escapeHTML.
export function renderText(value) {
  return escapeHTML(value).replace(/˙?[\u3105-\u312f]+[ˊˇˋ˙]?/gu,
    syllable => `<span class="phonetic">${syllable}</span>`);
}
export function canonicalURL(value) {
  try { const u=new URL(value.trim()); if(u.protocol!=='https:') return ''; const valid=(u.hostname==='chatgpt.com'&&/^\/share\/[a-zA-Z0-9-]+\/?$/.test(u.pathname))||(['share.gemini.google','gemini.google.com'].includes(u.hostname)&&/^\/(share\/)?[a-zA-Z0-9_-]+\/?$/.test(u.pathname)); return valid?u.origin+u.pathname.replace(/\/$/,''):''; } catch { return ''; }
}
export function safeAsset(value) { return typeof value==='string' && /^(assets|sources)\/[a-zA-Z0-9_./-]+$/.test(value) && !value.includes('..') ? value : ''; }
export function fingerprint(q) { return q.subject+':'+q.question.normalize('NFKC').replace(/[\s\p{P}\p{S}]/gu,'').toLowerCase(); }
export function validDate(value) { return typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)&&!Number.isNaN(Date.parse(value))&&new Date(value).toISOString().slice(0,10)===value; }
const stringFields=['id','sourceId','subject','title','chapter','volume','date','dateLabel','addedAt','question','answer','explanation','trap','verification','verificationNote','diagram','notes'];
export function validateQuestion(q) {
  if(!q || typeof q!=='object' || !SUBJECT_IDS.includes(q.subject) || typeof q.id!=='string' || !/^[\w-]{1,100}$/.test(q.id) || typeof q.title!=='string'||!q.title.trim()||typeof q.question!=='string'||!q.question.trim()||!validDate(q.date)) throw Error('題目需有有效的識別碼、科目、標題、日期與題目內容。');
  const out={}; for(const k of stringFields) out[k]=typeof q[k]==='string'?q[k].slice(0,50000):'';
  out.volume=out.volume||'綜合';out.chapter=out.chapter||'綜合';out.status=Object.hasOwn(STATUS,q.status)?q.status:'todo';out.starred=!!q.starred;
  out.tags=Array.isArray(q.tags)?q.tags.filter(x=>typeof x==='string').slice(0,20):[];
  out.images=Array.isArray(q.images)?q.images.filter(safeAsset).slice(0,50):[];
  for(const key of ['sourceLabel','studentAnswer','contentStatus','correctOption','passage','reviewExcerpt','reviewLabel','reviewPreviousId','reviewNextId','originalQuestionNumber']) if(typeof q[key]==='string') out[key]=q[key].slice(0,['passage','reviewExcerpt'].includes(key)?50000:1000);
  if(Array.isArray(q.reviewQuestions))out.reviewQuestions=q.reviewQuestions.filter(x=>typeof x==='string').slice(0,30).map(x=>x.slice(0,5000));
  if(Array.isArray(q.optionAnalysis)) out.optionAnalysis=q.optionAnalysis.slice(0,30).map(option=>Object.fromEntries(['label','text','wordClass','meaning','explanation'].map(key=>[key,typeof option?.[key]==='string'?option[key].slice(0,5000):''])));
  if(Array.isArray(q.tables)) out.tables=q.tables.slice(0,10).map(table=>({caption:String(table.caption||'').slice(0,1000),headers:(Array.isArray(table.headers)?table.headers:[]).map(x=>String(x).slice(0,1000)).slice(0,20),rows:(Array.isArray(table.rows)?table.rows:[]).slice(0,100).map(row=>(Array.isArray(row)?row:[]).map(x=>String(x).slice(0,5000)).slice(0,20))}));
  if(Array.isArray(q.questionFigures)) out.questionFigures=q.questionFigures.filter(f=>safeAsset(f?.src)).slice(0,15).map(f=>({src:safeAsset(f.src),alt:String(f.alt||'題目附圖').slice(0,1000),caption:String(f.caption||'').slice(0,1000)}));
  if(Array.isArray(q.explanationFigures)) out.explanationFigures=q.explanationFigures.filter(f=>safeAsset(f?.src)).slice(0,15).map(f=>({src:safeAsset(f.src),alt:String(f.alt||'解說示意圖').slice(0,1000),caption:String(f.caption||'').slice(0,1000)}));
  if(q.teachingComic && safeAsset(q.teachingComic.art) && Array.isArray(q.teachingComic.panels) && q.teachingComic.panels.length===3 && Array.isArray(q.teachingComic.fourth?.points)) {
    const c=q.teachingComic,clean=v=>typeof v==='string'?v.slice(0,5000):'';
    out.teachingComic={art:safeAsset(c.art),title:clean(c.title),panels:c.panels.map(p=>({heading:clean(p?.heading),text:clean(p?.text),alt:clean(p?.alt)})),fourth:{answer:clean(c.fourth.answer),points:c.fourth.points.slice(0,5).map(clean)}};
    const words=Array.isArray(c.protectedWords)?[...new Set(c.protectedWords.filter(w=>typeof w==='string'&&w.trim().length>=2&&w.length<=40&&!/[\u0000-\u001f]/u.test(w)).map(w=>w.trim()))].slice(0,50):[];
    if(words.length)out.teachingComic.protectedWords=words;
  }
  if(q.groupQuestions!==undefined){
    if(!Array.isArray(q.groupQuestions)||q.groupQuestions.length<2||q.groupQuestions.length>30||q.groupQuestions.some(child=>!child||child.groupQuestions!==undefined))throw Error('題組必須有2至30個完整子題，不可巢狀合併。');
    out.groupQuestions=q.groupQuestions.map(child=>validateQuestion(child));
    const ids=out.groupQuestions.map(child=>child.id);
    if(new Set(ids).size!==ids.length||!ids.includes(q.id))throw Error('題組子題識別碼重複或缺少保留題號。');
    if(q.groupMetadata&&typeof q.groupMetadata==='object'){
      const meta=q.groupMetadata;out.groupMetadata={};
      for(const key of ['groupId','kind','retainId','reviewReport','printedRange','representativeSubjectReason'])if(typeof meta[key]==='string')out.groupMetadata[key]=meta[key].slice(0,5000);
      for(const key of ['originalQuestionIds','displayOrder','aliasesProposed'])if(Array.isArray(meta[key]))out.groupMetadata[key]=meta[key].filter(id=>ids.includes(id));
      out.groupMetadata.commonFigureEquivalentSources=(Array.isArray(meta.commonFigureEquivalentSources)?meta.commonFigureEquivalentSources:[]).filter(row=>safeAsset(row?.src)&&safeAsset(row?.commonSrc)&&/^[a-f0-9]{64}$/.test(row?.sha256||'')).map(row=>({src:row.src,commonSrc:row.commonSrc,sha256:row.sha256}));
    }
  }
  return out;
}
export function validateSource(s) {
  if(!s||typeof s!=='object'||typeof s.id!=='string'||!/^[\w-]{1,100}$/.test(s.id)||!canonicalURL(s.url)) throw Error('來源必須是有效的 ChatGPT 或 Gemini 分享連結。');
  const out={id:s.id,url:canonicalURL(s.url),status:['read','excluded'].includes(s.status)?s.status:'pending'};
  for(const k of ['title','platform','date','addedAt','note','content']) out[k]=typeof s[k]==='string'?s[k].slice(0,100000):'';
  out.images=Array.isArray(s.images)?s.images.filter(safeAsset).slice(0,100):[];
  out.transcript=safeAsset(s.transcript);return out;
}
export function mergeData(current,incoming,mode='skip') {
  if(incoming.schemaVersion!==1||!Array.isArray(incoming.questions)||!Array.isArray(incoming.sources))throw Error('檔案格式不符，請匯入 WeiRuGo 匯出的 JSON。');
  if(incoming.questions.length>10000||incoming.sources.length>10000)throw Error('檔案筆數過多。');
  const questions=incoming.questions.map(validateQuestion),sources=incoming.sources.map(validateSource);
  const result=structuredClone(current), sourceMap=new Map();let added=0,updated=0,skipped=0;
  for(const s of sources){const same=result.sources.find(x=>x.url===s.url);if(same){sourceMap.set(s.id,same.id);if(mode==='update')Object.assign(same,{...s,id:same.id});continue;}const id=result.sources.some(x=>x.id===s.id)?crypto.randomUUID():s.id;sourceMap.set(s.id,id);result.sources.push({...s,id});}
  for(const q of questions){ q.sourceId=sourceMap.get(q.sourceId)||q.sourceId; if(q.sourceId&&!result.sources.some(s=>s.id===q.sourceId))throw Error('題目所引用的來源不存在。');const same=result.questions.find(x=>x.id===q.id||fingerprint(x)===fingerprint(q));if(same){if(mode==='update'){Object.assign(same,{...q,id:same.id,date:same.date<q.date?same.date:q.date});updated++;}else skipped++;}else {result.questions.push(q);added++;}}
  return {data:result,added,updated,skipped};
}
export function needsReview(q){return q.contentStatus==='待更新'||['待核對','待補原題'].includes(q.verification);}
export function selectQuestions(questions,filters) {
  const text=(filters.search||'').trim().toLowerCase();
  const result=questions.filter(q=>(!filters.subject||q.subject===filters.subject)&&(!filters.volume||q.volume===filters.volume)&&(!filters.chapter||q.chapter===filters.chapter)&&(!filters.status||q.status===filters.status)&&(!filters.answered||(filters.answered==='done'?!!q.answered:!q.answered))&&(!filters.starred||q.starred)&&(!filters.doubt||q.doubted)&&(!filters.issue||needsReview(q))&&(!text||[q.title,q.question,q.answer,q.explanation,q.chapter,...q.tags].join(' ').toLowerCase().includes(text)));
  return result.sort((a,b)=>filters.sort==='title'?a.title.localeCompare(b.title,'zh-Hant',{numeric:true}):filters.sort==='oldest'?a.date.localeCompare(b.date)||a.id.localeCompare(b.id):b.date.localeCompare(a.date)||a.id.localeCompare(b.id));
}
