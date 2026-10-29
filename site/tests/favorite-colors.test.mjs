import test from 'node:test';
import assert from 'node:assert/strict';
import {FAVORITE_COLOR_KEY,FAVORITE_COLORS,checkedFavoriteColors,loadFavoriteColors} from '../dist/favorite-colors.js';
import {persistMarks,DOUBTS_KEY,ANSWERED_KEY} from '../dist/marks.js';
import {FAVORITES_KEY} from '../dist/favorites.js';
import {handleMarks} from '../../netlify/lib/shared-marks.mjs';
import {MarkSync,OUTBOX_KEY} from '../dist/mark-sync.js';

const url='https://weirugo.sibuzu.com/.netlify/functions/marks';
const storage=()=>{const map=new Map();return {map,getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k)};};
const store=()=>{const values=new Map();return {values,list:async()=>({blobs:[...values.keys()].map(key=>({key}))}),get:async k=>structuredClone(values.get(k)??null),setJSON:async(k,v)=>values.set(k,structuredClone(v))};};
const api=db=>async(_url,opts={})=>handleMarks(new Request(url,opts),db);
const post=ops=>new Request(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({schemaVersion:1,operations:ops})});
const device=(db,local={favorites:[],doubts:[],answered:[],favoriteColors:{}},s=storage(),fetcher=api(db))=>{
 const states=[];const sync=new MarkSync({storage:s,getLocal:()=>local,apply:x=>local=x,status:x=>states.push(x),fetcher,endpoint:url});
 return {sync,storage:s,states,get local(){return local}};
};
async function idle(sync){for(let n=0;n<20&&sync.busy;n++)await sync.busy;assert.equal(sync.busy,null);}

test('only the five selected colors are accepted and a fresh browser stays untouched',()=>{
 assert.deepEqual(Object.keys(FAVORITE_COLORS),['red','blue','orange','green','yellow']);
 const s=storage();assert.deepEqual(loadFavoriteColors(s),{});assert.equal(s.map.size,0);
 for(const invalid of [null,[],{'q-001':'magenta'},{'q-001':'url(evil)'},{'../private':'red'}])assert.throws(()=>checkedFavoriteColors(invalid));
});
test('color persistence is atomic with all three existing marks',()=>{
 const s=storage();persistMarks(s,['q-001'],['q-002'],['q-003'],{'q-001':'blue'});
 assert.deepEqual(loadFavoriteColors(s),{'q-001':'blue'});
 const before=new Map(s.map),set=s.setItem;let fail=true;s.setItem=(key,value)=>{if(key===FAVORITE_COLOR_KEY&&fail){fail=false;throw Error('storage full');}set(key,value);};
 assert.throws(()=>persistMarks(s,['q-004'],[],[],{'q-004':'red'}));assert.deepEqual(s.map,before);
 assert.equal(s.getItem(FAVORITES_KEY),'["q-001"]');assert.equal(s.getItem(DOUBTS_KEY),'["q-002"]');assert.equal(s.getItem(ANSWERED_KEY),'["q-003"]');
});
test('changing color without changing favorite membership syncs to another device',async()=>{
 const db=store(),a=device(db),b=device(db);await a.sync.refresh();a.sync.queue('favorite','q-001',true,'red');await idle(a.sync);await b.sync.refresh();
 assert.deepEqual(b.local.favoriteColors,{'q-001':'red'});assert.deepEqual(b.local.favorites,['q-001']);
 b.sync.queue('favorite','q-001',true,'blue');b.sync.queue('answered','q-002',true);await idle(b.sync);await a.sync.refresh();
 assert.deepEqual(a.local.favoriteColors,{'q-001':'blue'});assert.deepEqual(a.local.answered,['q-002']);assert.equal(db.values.get('v1/favorite/q-001').color,'blue');
});
test('offline color survives reload and OFF tombstones cannot resurrect it',async()=>{
 const db=store();await db.setJSON('v1/favorite/q-001',{on:true});const s=storage();
 const a=device(db,{favorites:['q-001'],doubts:[],answered:[],favoriteColors:{'q-001':'green'}},s,async()=>{throw Error('offline')});
 a.sync.queue('favorite','q-001',true,'green');await idle(a.sync);assert.equal(JSON.parse(s.getItem(OUTBOX_KEY))[0].color,'green');
 const reloaded=device(db,a.local,s);await reloaded.sync.refresh();assert.equal(reloaded.local.favoriteColors['q-001'],'green');assert.equal(s.getItem(OUTBOX_KEY),null);
 await handleMarks(post([{kind:'favorite',id:'q-001',on:false}]),db);
 const stale=device(db,a.local);await stale.sync.refresh();assert.deepEqual(stale.local.favorites,[]);assert.deepEqual(stale.local.favoriteColors,{});
});
test('a rapid newer color is not dropped by an earlier slow acknowledgement',async()=>{
 const db=store();let release,started,first=true;const writing=new Promise(r=>started=r);
 const fetcher=async(u,o={})=>{if(o.method==='POST'&&first){first=false;started();await new Promise(r=>release=r);}return api(db)(u,o);};
 const a=device(db,undefined,undefined,fetcher);a.sync.queue('favorite','q-001',true,'red');await writing;a.sync.queue('favorite','q-001',true,'orange');release();await idle(a.sync);
 assert.equal(a.local.favoriteColors['q-001'],'orange');assert.equal(db.values.get('v1/favorite/q-001').color,'orange');
});
test('old backend defers only color operations and flushes them after deployment',async()=>{
 const db=store();let upgraded=false;const writes=[];
 const fetcher=async(u,o={})=>{if(o.method==='POST'){writes.push(JSON.parse(o.body).operations);return api(db)(u,o);}const r=await api(db)(u,o);if(upgraded||r.status===304)return r;const body=await r.json();delete body.favoriteColors;return new Response(JSON.stringify(body));};
 const a=device(db,undefined,undefined,fetcher);a.sync.queue('favorite','q-001',true,'blue');a.sync.queue('answered','q-002',true);await idle(a.sync);
 assert.equal(a.states.at(-1),'pending');assert.equal(db.values.get('v1/answered/q-002').on,true);assert.ok(writes.flat().every(op=>!op.color));assert.equal(a.local.favoriteColors['q-001'],'blue');
 upgraded=true;await a.sync.refresh();assert.equal(a.states.at(-1),'synced');assert.equal(db.values.get('v1/favorite/q-001').color,'blue');
});
test('legacy ON preserves an existing color; OFF then legacy ON resets to yellow',async()=>{
 const db=store();await handleMarks(post([{kind:'favorite',id:'q-001',on:true,color:'blue'}]),db);
 await handleMarks(post([{kind:'favorite',id:'q-001',on:true}]),db);assert.equal(db.values.get('v1/favorite/q-001').color,'blue');
 await handleMarks(post([{kind:'favorite',id:'q-001',on:false}]),db);assert.deepEqual(db.values.get('v1/favorite/q-001'),{on:false});
 await handleMarks(post([{kind:'favorite',id:'q-001',on:true}]),db);const a=device(db,{favorites:['q-001'],doubts:[],answered:[],favoriteColors:{'q-001':'blue'}});await a.sync.refresh();assert.equal(a.local.favoriteColors['q-001'],'yellow');
});
test('invalid colors reject an entire bulk write without touching other flags',async()=>{
 const db=store();for(const bad of [{kind:'favorite',id:'q-001',on:true,color:'magenta'},{kind:'doubt',id:'q-001',on:true,color:'red'},{kind:'favorite',id:'q-001',on:false,color:'red'}]){
  const response=await handleMarks(post([{kind:'answered',id:'q-002',on:true},bad]),db);assert.equal(response.status,400);assert.equal(db.values.size,0);
 }
});
