import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {canonicalURL,safeAsset,validateQuestion,mergeData,selectQuestions,escapeHTML,validDate} from '../dist/core.js';
const seed=JSON.parse(readFileSync(new URL('../dist/data.json',import.meta.url)));
const blank=()=>({...seed,questions:[],sources:[]});
test('dataset retains the original subjects and archives alongside new questions',()=>{assert.equal(seed.subjects.length,9);assert.ok(seed.sources.length>=9);assert.ok(seed.questions.length>=43);assert.equal(new Set(seed.questions.map(q=>q.id)).size,seed.questions.length);for(const q of seed.questions){assert.deepEqual(validateQuestion(q),q);assert.ok(seed.sources.some(s=>s.id===q.sourceId));}});
test('all source transcripts and locally saved images exist',()=>{for(const s of seed.sources){assert.ok(existsSync(new URL('../dist/'+s.transcript,import.meta.url)));for(const path of s.images)assert.ok(existsSync(new URL('../dist/'+path,import.meta.url)));}assert.ok(seed.sources.reduce((n,s)=>n+s.images.length,0)>=31);});
test('English composition remains in English comprehensive as requested',()=>{const q=seed.questions.find(q=>q.sourceId==='src-2');assert.equal(q.subject,'English');assert.equal(q.volume,'綜合');assert.equal(q.chapter,'綜合');});
test('date is original question appearance, not import date',()=>{const q=seed.questions.find(q=>q.sourceId==='src-2');assert.equal(q.date,'2025-08-05');assert.equal(q.addedAt,'2026-10-27');assert.equal(q.dateLabel,'首次出題日期');});
test('cross-subject natural-science material has exactly one primary subject',()=>{assert.deepEqual([...new Set(seed.questions.filter(q=>q.sourceId==='src-9').map(q=>q.subject))],['Physics-Chemistry']);});
test('URL canonicalization prevents link variants from making duplicates',()=>{assert.equal(canonicalURL(seed.sources[0].url+'/?utm_source=test#part'),seed.sources[0].url);for(const url of ['javascript:alert(1)','http://chatgpt.com/share/test','https://chatgpt.com.evil.test/share/test','https://example.com/share/id','https://chatgpt.com/share/id/extra'])assert.equal(canonicalURL(url),'');});
test('assets cannot escape their known local directories',()=>{for(const path of ['javascript:alert(1)','https://evil.test/a.jpg','assets/../secrets','/etc/passwd'])assert.equal(safeAsset(path),'');assert.equal(safeAsset('assets/originals/a.jpg'),'assets/originals/a.jpg');});
test('import round-trips every question and source',()=>{const {data}=mergeData(blank(),seed,'update');assert.deepEqual(data.questions,seed.questions);assert.deepEqual(data.sources,seed.sources);});
test('repeat import skips duplicates without losing progress',()=>{const current=structuredClone(seed);current.questions[0].status='mastered';const result=mergeData(current,seed);assert.equal(result.added,0);assert.equal(result.skipped,seed.questions.length);assert.equal(result.data.questions[0].status,'mastered');});
test('update duplicate changes content and keeps first appearance date',()=>{const incoming=structuredClone(seed);incoming.questions=[{...seed.questions[0],date:'2026-10-27',answer:'updated'}];const result=mergeData(seed,incoming,'update');assert.equal(result.updated,1);assert.equal(result.data.questions[0].answer,'updated');assert.equal(result.data.questions[0].date,seed.questions[0].date);});
test('same question with a new ID deduplicates by normalized content',()=>{const incoming={...seed,questions:[{...seed.questions[0],id:'new-id'}]};const result=mergeData(seed,incoming);assert.equal(result.skipped,1);assert.equal(result.data.questions.length,seed.questions.length);});
test('separate questions from the same source are preserved',()=>{assert.ok(seed.questions.filter(q=>q.sourceId==='src-9').length>10);assert.equal(mergeData(blank(),seed).data.questions.length,seed.questions.length);});
test('invalid imports are rejected atomically',()=>{const invalid=structuredClone(seed);invalid.questions[1].subject='Unknown';assert.throws(()=>mergeData(seed,invalid));assert.ok(seed.questions.length>=43);const missing={...seed,questions:[{...seed.questions[0],sourceId:'missing'}],sources:[]};assert.throws(()=>mergeData(blank(),missing));assert.throws(()=>mergeData(seed,{questions:[],sources:[]}));});
test('untrusted text is escaped and unknown fields are dropped',()=>{assert.equal(escapeHTML('<img src=x onerror="alert(1)">'),'&lt;img src=x onerror=&quot;alert(1)&quot;&gt;');assert.equal(validateQuestion({...seed.questions[0],onload:'evil'}).onload,undefined);});
test('filters combine subject, search, chapter, status and dates',()=>{
 const base={...seed.questions.find(q=>q.id==='q-042'),chapter:'浮力',question:'比較密度與浮力',status:'todo',date:'2026-05-01'};
 const fixtures=[{...base,id:'later',date:'2026-06-01'},{...base,id:'earlier'},{...base,id:'other-subject',subject:'Biology'},{...base,id:'other-chapter',chapter:'壓力'},{...base,id:'other-volume',volume:'第三冊'},{...base,id:'other-status',status:'mastered'}];
 const list=selectQuestions(fixtures,{subject:'Physics-Chemistry',volume:base.volume,chapter:'浮力',search:'密度',status:'todo',sort:'oldest'});
 assert.deepEqual(list.map(q=>q.id),['earlier','later']);
 assert.equal(selectQuestions(fixtures,{search:'__no_matching_question__'}).length,0);
 const sorted=selectQuestions(seed.questions,{sort:'oldest'});assert.ok(sorted[0].date<=sorted.at(-1).date);
});
test('dates reject impossible calendar dates',()=>{assert.equal(validDate('2026-02-30'),false);assert.equal(validDate('2024-02-29'),true);});
test('corrected square area satisfies independent coordinate distances',()=>{const u=8+Math.sqrt(14),s=Math.sqrt(u),x=(u-8)/(2*s),y=(u-6)/(2*s);assert.ok(x>0&&y>0&&x<s&&y<s);for(const [actual,target] of [[x*x+y*y,1],[(x-s)**2+y*y,9],[x*x+(y-s)**2,7]])assert.ok(Math.abs(actual-target)<1e-10);});
test('reviewed example restores original question and all four choices',()=>{const q=seed.questions.find(q=>q.id==='q-024');assert.equal(q.verification,'原題已核對');assert.equal(q.date,'2026-06-24');assert.equal(q.optionAnalysis.length,4);assert.ok(q.question.includes('(C) 蓮「之」愛，同予者何人'));assert.ok(!q.question.includes('牡丹'));assert.equal(q.studentAnswer,'C');assert.deepEqual(q.optionAnalysis.map(o=>o.wordClass),['助詞','助詞','助詞','代詞']);assert.ok(q.explanation.includes('詞性不同'));assert.equal(q.images.length,1);assert.ok(existsSync(new URL('../dist/'+q.images[0],import.meta.url)));});
test('complete example survives a version update with personal progress',()=>{const current=structuredClone(seed),q=current.questions.find(q=>q.id==='q-024');q.status='mastered';q.notes='我的筆記';const exported=mergeData(blank(),current,'update').data;const saved=exported.questions.find(q=>q.id==='q-024');assert.equal(saved.optionAnalysis[2].text,'蓮「之」愛，同予者何人');assert.equal(saved.status,'mastered');assert.equal(saved.notes,'我的筆記');assert.ok(saved.sourceLabel.includes('第 5 張'));});
test('standalone example keeps all explanations and shares local evidence assets',()=>{const page=readFileSync(new URL('../dist/q-024.html',import.meta.url),'utf8');for(const phrase of ['完整原題','逐項解析','無案牘','同予者何人','詳細說明與解題步驟','代詞'])assert.ok(page.includes(phrase));assert.ok(!page.includes('data:image/'));for(const [,src] of page.matchAll(/<img[^>]+src="([^"]+)"/g)){assert.ok(src.startsWith('assets/'));assert.ok(existsSync(new URL('../dist/'+src,import.meta.url)));}assert.ok(!page.includes('<script'));assert.ok(!page.includes('<link'));});

test('full reading passages survive import without truncation',()=>{const text='完整文章。'.repeat(400);const q=validateQuestion({...seed.questions[0],passage:text});assert.equal(q.passage,text);});
test('explanation figures survive validation and reject external asset paths',()=>{
 const figure={src:'assets/questions/q-006-explanation.png',alt:'旋轉與作高',caption:'解說示意'};
 const q=validateQuestion({...seed.questions[0],explanationFigures:[figure,{...figure,src:'https://example.com/tracking.png'},{...figure,src:'assets/../secrets'}]});
 assert.deepEqual(q.explanationFigures,[figure]);
});
test('the review queue includes every incomplete question',()=>{
 const pending=seed.questions.filter(q=>q.contentStatus==='待更新');
 const issues=selectQuestions(seed.questions,{issue:true});
 for(const q of pending){assert.ok(issues.some(item=>item.id===q.id));assert.ok(q.reviewQuestions.length>0);}
});
test('new biology questions include all choices, reviewed source crops and necessary figures',()=>{for(const q of seed.questions.filter(q=>q.sourceId==='src-more-002')){assert.equal(q.contentStatus,'完整原題');assert.equal(q.optionAnalysis.length,4);assert.ok(q.images.length);for(const image of [...q.images,...q.questionFigures.map(f=>f.src)])assert.ok(existsSync(new URL('../dist/'+image,import.meta.url)));}const q=seed.questions.find(q=>q.id==='q-047');assert.ok(q.title.includes('44'));assert.equal(q.correctOption,'D');});


test('answered filtering combines with subject/search/favorite and treats unset flags as not done',()=>{
 const base={...seed.questions[0],subject:'English',title:'English sample',question:'grammar',tags:[]};
 const questions=[{...base,id:'q-001',answered:true,starred:true},{...base,id:'q-002',answered:false,starred:true},{...base,id:'q-003',starred:false},{...base,id:'q-004',answered:true,subject:'Math',starred:true}];
 assert.deepEqual(selectQuestions(questions,{subject:'English',answered:'done',starred:true,search:'grammar'}).map(q=>q.id),['q-001']);
 assert.deepEqual(selectQuestions(questions,{subject:'English',answered:'not-done'}).map(q=>q.id),['q-002','q-003']);
 assert.equal(selectQuestions(questions,{answered:''}).length,4);
});
