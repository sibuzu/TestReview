import test from 'node:test';
import assert from 'node:assert/strict';
import {handleMarks} from '../../netlify/lib/shared-marks.mjs';
import {MarkSync, OUTBOX_KEY} from '../dist/mark-sync.js';
const url='https://weirugo.sibuzu.com/.netlify/functions/marks';
const storage=()=>{const map=new Map();return {getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k),map};};
const store=()=>{const values=new Map();return {values,list:async()=>({blobs:[...values.keys()].map(key=>({key}))}),get:async k=>structuredClone(values.get(k)??null),setJSON:async(k,v)=>{values.set(k,structuredClone(v));}};};
const api=db=>async(_url,options={})=>handleMarks(new Request(url,options),db);
const post=operations=>new Request(url,{method:'POST',headers:{'Content-Type':'application/json','Origin':'https://weirugo.sibuzu.com'},body:JSON.stringify({schemaVersion:1,operations})});
const device=(db,local={favorites:[],doubts:[]},s=storage(),fetcher=api(db))=>{const states=[];const sync=new MarkSync({storage:s,getLocal:()=>local,apply:next=>{local=next;},status:x=>states.push(x),fetcher});return {sync,storage:s,states,get local(){return local}};};
async function idle(sync){for(let n=0;n<15&&sync.busy;n++)await sync.busy;assert.equal(sync.busy,null);}

test('first sync imports local marks without replacing another device marks',async()=>{
 const db=store();await db.setJSON('v1/favorite/q-002',{on:true});const a=device(db,{favorites:['q-001'],doubts:['q-003']});await a.sync.refresh();assert.deepEqual(a.local,{favorites:['q-001','q-002'],doubts:['q-003'],answered:[]});assert.deepEqual(db.values.get('v1/favorite/q-002'),{on:true});
});
test('cloud OFF tombstones prevent old local favorites resurrecting on first sync',async()=>{
 const db=store();await db.setJSON('v1/favorite/q-001',{on:false});const a=device(db,{favorites:['q-001'],doubts:[]});await a.sync.refresh();assert.deepEqual(a.local.favorites,[]);assert.equal(db.values.get('v1/favorite/q-001').on,false);
});
test('independent devices and independent flags do not overwrite unrelated marks',async()=>{
 const db=store(),a=device(db),b=device(db);await Promise.all([a.sync.refresh(),b.sync.refresh()]);a.sync.queue('favorite','q-001',true);b.sync.queue('doubt','q-001',true);await Promise.all([idle(a.sync),idle(b.sync)]);await Promise.all([a.sync.refresh(),b.sync.refresh()]);assert.deepEqual(a.local,{favorites:['q-001'],doubts:['q-001'],answered:[]});assert.deepEqual(b.local,a.local);
});
test('offline removal survives reload and retries without losing a remote different mark',async()=>{
 const db=store();await db.setJSON('v1/favorite/q-001',{on:true});const s=storage(),a=device(db,{favorites:['q-001'],doubts:[]},s,async()=>{throw Error('offline')});a.sync.queue('favorite','q-001',false);await idle(a.sync);assert.equal(JSON.parse(s.getItem(OUTBOX_KEY))[0].on,false);await db.setJSON('v1/doubt/q-002',{on:true});const reloaded=device(db,{favorites:[],doubts:[]},s);await reloaded.sync.refresh();assert.deepEqual(reloaded.local,{favorites:[],doubts:['q-002'],answered:[]});assert.equal(db.values.get('v1/favorite/q-001').on,false);assert.equal(s.getItem(OUTBOX_KEY),null);
});
test('a newer click during a slow write is not removed by the older acknowledgement',async()=>{
 const db=store();let release,started;const writing=new Promise(r=>started=r);let first=true;
 const fetcher=async(u,options={})=>{if(options.method==='POST'&&first){first=false;started();await new Promise(r=>release=r);}return api(db)(u,options);};
 const a=device(db,undefined,undefined,fetcher);a.sync.queue('favorite','q-001',true);await writing;a.sync.queue('favorite','q-001',false);release();await idle(a.sync);assert.deepEqual(a.local.favorites,[]);assert.equal(db.values.get('v1/favorite/q-001').on,false);
});
test('invalid bulk changes are rejected before any write; cross-origin writes are rejected',async()=>{
 const db=store();let r=await handleMarks(post([{kind:'favorite',id:'q-001',on:true},{kind:'doubt',id:'../secret',on:true}]),db);assert.equal(r.status,400);assert.equal(db.values.size,0);r=await handleMarks(new Request(url,{method:'POST',headers:{Origin:'https://elsewhere.example','Content-Type':'application/json'},body:'{}'}),db);assert.equal(r.status,403);
});
test('unchanged snapshot supports 304; OFF values remain in the snapshot',async()=>{
 const db=store();await db.setJSON('v1/favorite/q-001',{on:false});const first=await handleMarks(new Request(url),db);const payload=await first.json();assert.deepEqual(payload.marks,[{kind:'favorite',id:'q-001',on:false}]);const second=await handleMarks(new Request(url,{headers:{'If-None-Match':first.headers.get('ETag')}}),db);assert.equal(second.status,304);
});
test('a static server without Functions stays local without losing queued changes',async()=>{
 const a=device(store(),undefined,undefined,async()=>new Response('Not found',{status:404}));await a.sync.refresh();assert.equal(a.states.at(-1),'local');a.sync.queue('doubt','q-001',true);assert.equal(a.states.at(-1),'local');assert.equal(JSON.parse(a.storage.getItem(OUTBOX_KEY))[0].on,true);
});

test('monitor and Live Server use the same production endpoint, while Netlify uses its own function',async()=>{
 const {marksEndpointFor}=await import('../dist/mark-protocol.js');
 for(const origin of ['http://127.0.0.1:8765','http://localhost:5500','https://monitor.sibuzu.com'])assert.equal(marksEndpointFor(origin+'/site/index.html'),'https://weirugo.sibuzu.com/.netlify/functions/marks');
 assert.equal(marksEndpointFor('https://weirugo.sibuzu.com/'),'/.netlify/functions/marks');
 assert.equal(marksEndpointFor('https://preview--weirugo.netlify.app/'),'/.netlify/functions/marks');
});
test('trusted companion origins can preflight, read ETags and write shared marks',async()=>{
 const db=store();const origin='http://127.0.0.1:8765';
 const preflight=await handleMarks(new Request(url,{method:'OPTIONS',headers:{Origin:origin,'Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'content-type'}}),db);
 assert.equal(preflight.status,204);assert.equal(preflight.headers.get('Access-Control-Allow-Origin'),origin);
 const response=await handleMarks(new Request(url,{method:'POST',headers:{Origin:origin,'Content-Type':'application/json'},body:JSON.stringify({schemaVersion:1,operations:[{kind:'favorite',id:'q-001',on:true}]})}),db);
 assert.equal(response.status,200);assert.equal(response.headers.get('Access-Control-Allow-Origin'),origin);
 const snapshot=await handleMarks(new Request(url,{headers:{Origin:'https://monitor.sibuzu.com'}}),db);assert.equal(snapshot.headers.get('Access-Control-Expose-Headers'),'ETag');assert.equal((await snapshot.json()).marks[0].on,true);
});


test('answered marks sync across devices independently of favorite and doubt, including OFF tombstones',async()=>{
 const db=store(),a=device(db,{favorites:['q-001'],doubts:[],answered:['q-002']}),b=device(db);
 await a.sync.refresh();await b.sync.refresh();assert.deepEqual(b.local,{favorites:['q-001'],doubts:[],answered:['q-002']});
 b.sync.queue('answered','q-002',false);b.sync.queue('doubt','q-002',true);await idle(b.sync);await a.sync.refresh();
 assert.deepEqual(a.local,{favorites:['q-001'],doubts:['q-002'],answered:[]});
 const old=device(db,{favorites:[],doubts:[],answered:['q-002']});await old.sync.refresh();assert.deepEqual(old.local.answered,[]);
 assert.equal(db.values.get('v1/answered/q-002').on,false);
});
test('offline answered cancellation survives reload and does not erase other cloud marks',async()=>{
 const db=store();await db.setJSON('v1/answered/q-001',{on:true});await db.setJSON('v1/favorite/q-002',{on:true});
 const s=storage(),a=device(db,{favorites:[],doubts:[],answered:['q-001']},s,async()=>{throw Error('offline')});
 a.sync.queue('answered','q-001',false);await idle(a.sync);assert.deepEqual(JSON.parse(s.getItem(OUTBOX_KEY)),[{kind:'answered',id:'q-001',on:false}]);
 const reloaded=device(db,{favorites:[],doubts:[],answered:[]},s);await reloaded.sync.refresh();
 assert.deepEqual(reloaded.local,{favorites:['q-002'],doubts:[],answered:[]});assert.equal(db.values.get('v1/answered/q-001').on,false);assert.equal(s.getItem(OUTBOX_KEY),null);
});
test('an old deployed backend defers answered writes without blocking favorites; deployment flushes them',async()=>{
 const db=store();let upgraded=false;const writes=[];
 const fetcher=async(u,options={})=>{
  if(options.method==='POST'){const ops=JSON.parse(options.body).operations;writes.push(ops);if(!upgraded&&ops.some(op=>op.kind==='answered'))return new Response('{}',{status:400});return api(db)(u,options);}
  const response=await api(db)(u,options);if(upgraded||response.status===304)return response;
  const payload=await response.json();delete payload.kinds;return new Response(JSON.stringify(payload),{headers:{'Content-Type':'application/json'}});
 };
 const a=device(db,{favorites:['q-001'],doubts:[],answered:['q-002']},undefined,fetcher);
 await a.sync.refresh();assert.deepEqual(a.local,{favorites:['q-001'],doubts:[],answered:['q-002']});assert.equal(a.states.at(-1),'pending');
 assert.ok(writes.flat().every(op=>op.kind!=='answered'));assert.equal(db.values.get('v1/favorite/q-001').on,true);assert.equal(db.values.has('v1/answered/q-002'),false);
 upgraded=true;await a.sync.refresh();assert.equal(db.values.get('v1/answered/q-002').on,true);assert.equal(a.states.at(-1),'synced');assert.equal(a.storage.getItem(OUTBOX_KEY),null);
});
