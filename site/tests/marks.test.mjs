import test from 'node:test';
import assert from 'node:assert/strict';
import {loadDoubts,exportMarks,parseMarks,persistMarks,DOUBTS_KEY,ANSWERED_KEY,loadAnswered} from '../dist/marks.js';
import {FAVORITES_KEY} from '../dist/favorites.js';
const store=entries=>{const map=new Map(entries);return {map,getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k)};};
test('favorites and doubts are independent, deduplicated IDs in a portable backup',()=>{const out=exportMarks(new Set(['q-024']),['q-016','q-016']);assert.deepEqual(parseMarks(JSON.parse(JSON.stringify(out))),{favorites:['q-024'],doubts:['q-016']});assert.deepEqual(parseMarks({schemaVersion:1,type:'favorites',favorites:['q-024']}),{favorites:['q-024'],doubts:null});assert.throws(()=>parseMarks({schemaVersion:1,type:'question-marks',favorites:['q-024'],doubts:['../bad']}));});
test('loading doubts leaves an empty browser untouched and persists IDs only',()=>{const s=store([]);assert.deepEqual(loadDoubts(s),[]);assert.equal(s.map.size,0);persistMarks(s,['q-024'],['q-016']);assert.deepEqual([...s.map],[[FAVORITES_KEY,'["q-024"]'],[DOUBTS_KEY,'["q-016"]']]);assert.deepEqual(loadDoubts(s),['q-016']);});
test('a failed backup import restores both existing mark sets',()=>{const s=store([[FAVORITES_KEY,'["q-024"]'],[DOUBTS_KEY,'["q-016"]']]),set=s.setItem;let fail=true;s.setItem=(key,value)=>{if(key===DOUBTS_KEY&&fail){fail=false;throw Error('full');}set(key,value);};assert.throws(()=>persistMarks(s,['q-001'],['q-002']));assert.equal(s.getItem(FAVORITES_KEY),'["q-024"]');assert.equal(s.getItem(DOUBTS_KEY),'["q-016"]');});


test('answered storage defaults to unattempted, saves IDs only, and does not replace other marks',()=>{
 const s=store([]);assert.deepEqual(loadAnswered(s),[]);assert.equal(s.map.size,0);
 persistMarks(s,['q-024'],['q-016'],['q-001','q-001']);assert.deepEqual(loadAnswered(s),['q-001']);
 assert.equal(s.getItem(FAVORITES_KEY),'["q-024"]');assert.equal(s.getItem(DOUBTS_KEY),'["q-016"]');assert.equal(s.getItem(ANSWERED_KEY),'["q-001"]');
});
test('failed three-flag persistence rolls back favorites, doubts and answered together',()=>{
 const s=store([[FAVORITES_KEY,'["q-024"]'],[DOUBTS_KEY,'["q-016"]'],[ANSWERED_KEY,'["q-001"]']]),set=s.setItem;let fail=true;
 s.setItem=(key,value)=>{if(key===ANSWERED_KEY&&fail){fail=false;throw Error('full');}set(key,value);};
 assert.throws(()=>persistMarks(s,['q-003'],['q-004'],['q-005']));assert.equal(s.getItem(FAVORITES_KEY),'["q-024"]');assert.equal(s.getItem(DOUBTS_KEY),'["q-016"]');assert.equal(s.getItem(ANSWERED_KEY),'["q-001"]');
});
