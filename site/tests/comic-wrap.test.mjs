import test from 'node:test';
import assert from 'node:assert/strict';
import {wrapComicText} from '../dist/comic-wrap.js';
import {renderTeachingComic} from '../dist/teaching-comic.js';
import {validateQuestion} from '../dist/core.js';
import {readFileSync} from 'node:fs';

test('Chinese comic wrapping preserves words, punctuation and all original content',()=>{
 const paragraphs=['「家務、育兒本來就是女性的工作」','父親在育兒工作中形同缺席；','母親獨自承擔所有照顧責任。'];
 for(const text of paragraphs)for(const width of [10,12,14,16]){
  const lines=wrapComicText(text,width+.6,s=>[...s].length);
  assert.equal(lines.join(''),text);
  assert.ok(lines.every(l=>l.length<=width));
  assert.ok(lines.every(l=>!/^作|^[，。；」]|[「]$/u.test(l)));
  assert.ok(lines.every(l=>l.replace(/\p{P}/gu,'').length>1));
  for(const word of ['工作','缺席','責任'])if(text.includes(word))assert.ok(lines.some(l=>l.includes(word)));
 }
});

test('native comic supports safe imported data and escapes display text',()=>{
 const data=JSON.parse(readFileSync(new URL('../dist/data.json',import.meta.url)));
 const q=data.questions.find(q=>q.id==='q-271');
 assert.deepEqual(validateQuestion(q).teachingComic,q.teachingComic);
 assert.equal(validateQuestion({...q,teachingComic:{...q.teachingComic,art:'https://evil.test/a.png'}}).teachingComic,undefined);
 const c=structuredClone(q.teachingComic);c.panels[0].text='<script>alert(1)</script>';
 const html=renderTeachingComic(c);
 assert.ok(html.includes('&lt;script&gt;'));
 assert.ok(!html.includes('<script>'));
 assert.equal((html.match(/class="comic-cell/g)||[]).length,4);
});

test('geometry wrapping keeps triangle names and segment labels intact',()=>{
 const text='△BCE與△BCA共底BC，CE：CA＝3：5。';
 for(const width of [7,9,12]){
  const lines=wrapComicText(text,width+.6,s=>[...s].length);
  assert.equal(lines.join(''),text);
  for(const name of ['△BCE','△BCA','BC','CE','CA'])assert.ok(lines.some(line=>line.includes(name)));
 }
});

test('ratio and percentage wrapping keeps each value together',()=>{
 const text='東協10／10，APEC為12／21，要比較3：5與100%的比例。';
 const lines=wrapComicText(text,9.6,s=>[...s].length);
 assert.equal(lines.join(''),text);
 for(const ratio of ['10／10','12／21','3：5','100%'])assert.ok(lines.some(line=>line.includes(ratio)));
});

test('English contractions remain whole during mixed-language wrapping',()=>{
 const text="選 we can’t call it our neighbor，don't 拆開縮寫。";
 const lines=wrapComicText(text,12.6,s=>[...s].length);
 assert.equal(lines.join('').replaceAll(' ',''),text.replaceAll(' ',''));
 for(const word of ['can’t',"don't"])assert.ok(lines.some(line=>line.includes(word)));
});

test('short algebraic fractions stay with their denominators',()=>{
 const text='EO／BC＝a／(a＋b)，EF＝2ab／(a＋b)。';
 const lines=wrapComicText(text,13.6,s=>[...s].length);
 assert.equal(lines.join(''),text);
 for(const fraction of ['EO／BC','a／(a＋b)','2ab／(a＋b)'])assert.ok(lines.some(line=>line.includes(fraction)));
});

test('algebraic factors and squared groups do not split at internal signs',()=>{
 const text='整理為(2r－1)(r－2)＝0，另有(r＋1)²與a／(a＋b)、ab／(a＋b)²。';
 const lines=wrapComicText(text,13.6,s=>[...s].length);
 assert.equal(lines.join(''),text);
 for(const factor of ['(2r－1)','(r－2)','(r＋1)²','a／(a＋b)','ab／(a＋b)²'])assert.ok(lines.some(line=>line.includes(factor)));
});

test('scientific quantities keep their cubic units and volume units together',()=>{
 const text='甲30cm³與乙25cm³，液體各20mL，質量10kg。';
 const lines=wrapComicText(text,10.6,s=>[...s].length);
 assert.equal(lines.join(''),text);
 for(const quantity of ['30cm³','25cm³','20mL','10kg'])assert.ok(lines.some(line=>line.includes(quantity)));
});

test('negative numbers stay with their minus sign in narrow math explanations',()=>{
 const text='代入後a的值是−18，不能取−19，並比較−6x與−11／6。';
 for(const width of [7,9,12]){
  const lines=wrapComicText(text,width+.6,s=>[...s].length);
  assert.equal(lines.join(''),text);
  for(const value of ['−18','−19','−6x','−11／6'])assert.ok(lines.some(line=>line.includes(value)));
  assert.ok(lines.every(line=>!/[−－-]$/.test(line)));
 }
});

test('classical passage names remain intact when explaining who did what',()=>{
 const text='陳靈公不聽泄冶之諫，曹羈三諫曹君不聽而去。';
 for(const width of [7,9,12]){
  const lines=wrapComicText(text,width+.6,s=>[...s].length);
  assert.equal(lines.join(''),text);
  for(const name of ['陳靈公','泄冶','曹羈','曹君'])assert.ok(lines.some(line=>line.includes(name)));
 }
});

test('per-comic vocabulary survives validation and protects every name without changing copy',()=>{
 const data=JSON.parse(readFileSync(new URL('../dist/data.json',import.meta.url)));
 const q=structuredClone(data.questions.find(q=>q.id==='q-271'));
 q.teachingComic.protectedWords=['蘭蘭','阿科','小克','蘭蘭',null,42,'','x','x'.repeat(41)];
 const words=validateQuestion(q).teachingComic.protectedWords;
 assert.deepEqual(words,['蘭蘭','阿科','小克']);
 const text='阿科109秒，小克135秒，都比108秒久；蘭蘭103秒，比108秒短。';
 for(const width of [7,9,12]){
  const lines=wrapComicText(text,width+.6,s=>[...s].length,words);
  assert.equal(lines.join(''),text);
  for(const word of words)assert.ok(lines.some(line=>line.includes(word)));
 }
 q.teachingComic.protectedWords=['"><img src=x onerror=alert(1)>'];
 const html=renderTeachingComic(validateQuestion(q).teachingComic);
 assert.ok(html.includes('data-protected-words='));
 assert.ok(!html.includes('<img src=x'));
 assert.ok(html.includes('&lt;img'));
});
