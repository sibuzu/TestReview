import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {QUESTION_ALIASES} from '../dist/question-alias-data.js';
import {hasQuestionMark,toggleQuestionMark} from '../dist/question-identity.js';
import {parseRoute,questionHash} from '../dist/routes.js';

test('a deduplicated question bookmark resolves to the retained question',()=>{
 assert.deepEqual(QUESTION_ALIASES,JSON.parse(fs.readFileSync(new URL('../../docs/question-aliases.json',import.meta.url),'utf8')));
 assert.deepEqual(parseRoute('#question/q-217'),{kind:'question',id:'q-212'});
 assert.equal(questionHash('q-217'),'#question/q-212');
});
test('marks on either original ID remain visible and can be switched off together',()=>{
 for(const selected of [['q-217'],['q-212'],['q-212','q-217']]){
  const ids=new Set([...selected,'q-163']);
  assert.equal(hasQuestionMark(ids,'q-212'),true);
  assert.equal(hasQuestionMark(ids,'q-217'),true);
  assert.deepEqual([...toggleQuestionMark(ids,'q-212')],['q-163']);
 }
 assert.deepEqual([...toggleQuestionMark(new Set(['q-163']),'q-217')],['q-163','q-212']);
});
