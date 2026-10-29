import test from 'node:test';
import assert from 'node:assert/strict';
import {parseRoute,questionHash,listHash} from '../dist/routes.js';
test('every saved question can be linked directly',()=>{
 for(const id of ['q-016','q-024','9c5977bc-b636-49e5-903b-3cb3be8ce7aa'])assert.deepEqual(parseRoute(questionHash(id)),{kind:'question',id});
});
test('subject and utility links remain valid alongside question links',()=>{
 assert.deepEqual(parseRoute(listHash({subject:'Physics-Chemistry'})),{kind:'questions',subject:'Physics-Chemistry'});
 for(const kind of ['sources','starred','issues','doubts'])assert.deepEqual(parseRoute('#'+kind),{kind});
 assert.equal(listHash(), '#questions');
});
test('invalid or missing hashes fall back to the notebook',()=>{
 for(const hash of ['',undefined,'#content','#%E0%A4%A'])assert.deepEqual(parseRoute(hash),{kind:'questions'});
 assert.deepEqual(parseRoute('#question/missing'),{kind:'question',id:'missing'});
});
