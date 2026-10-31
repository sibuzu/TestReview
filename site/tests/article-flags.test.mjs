import test from 'node:test';
import assert from 'node:assert/strict';
import {FLAGS_KEY,PRACTICE_KEY,checkedFlags,checkedPractice,changedFlag,dailyCounts,practiceDay,persistFlagState,discardLegacyMarks} from '../dist/article-flags.js';
import {checkedFlagOperations} from '../dist/flag-protocol.js';
import {FlagSync,FLAG_OUTBOX_KEY} from '../dist/flag-sync.js';
import {SESSION_KEY,signIn,signOut,restoreSession,accountStorage} from '../dist/auth.js';
import {accountEndpoint} from '../dist/account-policy.js';
import {handleSession} from '../../netlify/lib/sessions.mjs';
import {handleAccountMarks} from '../../netlify/lib/account-marks.mjs';
const markURL='https://mytestreview.netlify.app/.netlify/functions/marks',sessionURL='https://mytestreview.netlify.app/.netlify/functions/session';
const day='2026-10-29',eventId=n=>'00000000-0000-4000-8000-'+String(n).padStart(12,'0');
const memory=()=>{const map=new Map();return {map,getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,String(v)),removeItem:k=>map.delete(k)};};
const database=()=>{const values=new Map();return {values,list:async({prefix=''})=>({blobs:[...values.keys()].filter(k=>k.startsWith(prefix)).map(key=>({key}))}),get:async key=>structuredClone(values.get(key)??null),setJSON:async(key,value)=>values.set(key,structuredClone(value)),delete:async key=>values.delete(key)};};
const api=db=>async(url,options={})=>{const req=new Request(url.startsWith('http')?url:'https://weirugo.sibuzu.com'+url,options);return url.includes('/session')?handleSession(req,db):handleAccountMarks(req,db);};
async function login(db,user='weiru',raw=memory()){return {raw,session:await signIn(raw,user,'1234',api(db))};}
async function idle(sync){for(let n=0;n<30;n++){if(sync.busy)await sync.busy;else break;}assert.equal(sync.busy,null);}
async function device(db,user='weiru',raw=memory(),fetcher=api(db)){
 const {session}=await login(db,user,raw),storage=accountStorage(raw,user),states=[];
 let local={flags:JSON.parse(storage.getItem(FLAGS_KEY)||'{}'),practice:JSON.parse(storage.getItem(PRACTICE_KEY)||'[]'),doubts:[]};
 const sync=new FlagSync({storage,getLocal:()=>local,apply:next=>{local=next;persistFlagState(storage,next.flags,next.practice,next.doubts);},status:s=>states.push(s),endpoint:markURL,getToken:()=>session.token,fetcher});
 return {sync,raw,storage,session,states,get local(){return local;},act(id,value,date=day){const before=new Set(local.practice.map(e=>e.eventId));const next=changedFlag(local.flags,local.practice,id,value,date);local={...local,...next};persistFlagState(storage,local.flags,local.practice,local.doubts);sync.queueAll([{kind:'flag',id,value},...local.practice.filter(e=>!before.has(e.eventId)).map(e=>({kind:'practice',...e}))]);}};
}

test('five exclusive flags reject invalid values and start without importing legacy marks',()=>{
 assert.deepEqual(checkedFlags({}),{});for(const value of [0,6,'3',true,null])assert.throws(()=>checkedFlags({'q-001':value}));
 const s=memory();for(const key of ['test-review:favorites:v1','test-review:answered:v1','test-review:favorite-colors:v1'])s.setItem(key,'["q-001"]');
 s.setItem('test-review:doubts:v1','["q-002"]');s.setItem('test-review:mark-outbox:v1',JSON.stringify([{kind:'favorite',id:'q-001',on:true},{kind:'doubt',id:'q-002',on:false}]));
 assert.deepEqual(discardLegacyMarks(s),[{kind:'doubt',id:'q-002',on:false}]);assert.deepEqual([...s.map.keys()],['test-review:doubts:v1']);
});
test('same-day general to done and back has zero net work; different-day undo can be negative',()=>{
 let state=changedFlag({},[],'q-001',2,day,eventId(1));assert.deepEqual(dailyCounts(state.practice),[{day,count:1}]);
 state=changedFlag(state.flags,state.practice,'q-001',3,day,eventId(2));assert.deepEqual(dailyCounts(state.practice),[{day,count:0}]);
 state=changedFlag(state.flags,state.practice,'q-001',2,day,eventId(3));state=changedFlag(state.flags,state.practice,'q-001',3,'2026-10-30',eventId(4));
 assert.deepEqual(dailyCounts(state.practice),[{day:'2026-10-30',count:-1},{day,count:1}]);
});
test('all non-general flags count entry/exit, while changing between them does not count',()=>{
 let s=changedFlag({},[],'q-001',1,day,eventId(1));s=changedFlag(s.flags,s.practice,'q-001',5,day,eventId(2));s=changedFlag(s.flags,s.practice,'q-001',4,day,eventId(3));
 assert.equal(s.practice.length,1);s=changedFlag(s.flags,s.practice,'q-001',3,day,eventId(4));assert.equal(dailyCounts(s.practice)[0].count,0);
 s=changedFlag(s.flags,s.practice,'q-001',3,day,eventId(5));assert.equal(s.practice.length,2);
});
test('practice is deduplicated by action ID, not by question/day; Taipei midnight and real dates are respected',()=>{
 const e={id:'q-001',day,eventId:eventId(1),delta:1};assert.equal(checkedPractice([e,e]).length,1);assert.throws(()=>checkedPractice([e,{...e,delta:-1}]));
 assert.throws(()=>checkedPractice([{...e,day:'2026-02-30'}]));assert.equal(practiceDay(new Date('2026-10-29T16:00:00Z')),'2026-10-30');
 assert.deepEqual(checkedFlags({'q-821':5}),{'q-820':5});
});
test('FLAG, daily net events and shared doubts roll back together when storage fails',()=>{
 const base=memory();persistFlagState(base,{'q-001':3},[],[]);const before=[...base.map];let fail=true;
 const storage={...base,setItem(k,v){if(k===PRACTICE_KEY&&fail){fail=false;throw Error('full');}base.setItem(k,v);}};
 assert.throws(()=>persistFlagState(storage,{'q-001':2},[{id:'q-001',day,eventId:eventId(1),delta:1}],['q-002']));assert.deepEqual([...base.map],before);
});
test('accounts have separate local flags/outboxes but share local doubts',()=>{
 const raw=memory(),a=accountStorage(raw,'weiru'),b=accountStorage(raw,'demo');a.setItem(FLAGS_KEY,'{"q-001":5}');a.setItem(FLAG_OUTBOX_KEY,'[]');
 assert.equal(b.getItem(FLAGS_KEY),null);assert.equal(b.getItem(FLAG_OUTBOX_KEY),null);b.setItem('test-review:doubts:v1','["q-002"]');assert.equal(a.getItem('test-review:doubts:v1'),'["q-002"]');
});
test('Sign In accepts only the two fixed accounts and stores a token, never the password',async()=>{
 const db=database(),raw=memory();await assert.rejects(()=>signIn(raw,'other','1234',api(db)));await assert.rejects(()=>signIn(raw,'weiru','bad',api(db)));
 assert.equal(raw.getItem(SESSION_KEY),null);const s=await signIn(raw,'weiru','1234',api(db));assert.deepEqual(JSON.parse(raw.getItem(SESSION_KEY)),s);assert.equal(s.password,undefined);
 const row=[...db.values.values()][0];assert.deepEqual(row,{user:'weiru'});assert.ok(![...db.values.keys()][0].includes(s.token));
});
test('sessions have no expiry, survive network outages, and Sign Out revokes only that browser token',async()=>{
 const db=database(),a=await login(db),b=await login(db);
 assert.deepEqual(await restoreSession(a.raw,async()=>{throw Error('offline');}),a.session);
 await signOut(a.raw,a.session,api(db));assert.equal(a.raw.getItem(SESSION_KEY),null);
 assert.equal((await handleSession(new Request(sessionURL,{headers:{Authorization:'Bearer '+a.session.token}}),db)).status,401);
 assert.deepEqual(await restoreSession(b.raw,api(db)),b.session);
});
test('all entry URLs use cloud APIs and cross-origin preflight allows bearer authorization',async()=>{
 for(const href of ['https://test.sibuzu.com','http://localhost:5500','https://monitor.sibuzu.com','https://monitor-test.sibuzu.com','http://127.0.0.1:8912','https://mytestreview.netlify.app'])assert.equal(accountEndpoint('marks',href),markURL);
 const db=database();for(const origin of ['https://test.sibuzu.com','http://127.0.0.1:8765','https://monitor-test.sibuzu.com','http://127.0.0.1:8912']){
  const r=await handleSession(new Request(sessionURL,{method:'OPTIONS',headers:{Origin:origin}}),db);assert.equal(r.status,204);assert.equal(r.headers.get('Access-Control-Allow-Origin'),origin);assert.match(r.headers.get('Access-Control-Allow-Headers'),/Authorization/);
 }
});
test('anonymous reads/writes are rejected; invalid changes are rejected before mutation',async()=>{
 const db=database();assert.equal((await handleAccountMarks(new Request(markURL),db)).status,401);const a=await login(db);
 const headers={'Content-Type':'application/json',Authorization:'Bearer '+a.session.token};
 const r=await handleAccountMarks(new Request(markURL,{method:'POST',headers,body:JSON.stringify({schemaVersion:2,operations:[{kind:'flag',id:'q-001',value:4},{kind:'flag',id:'q-002',value:9}]})}),db);
 assert.equal(r.status,400);assert.equal([...db.values.keys()].filter(k=>k.startsWith('users/')).length,0);
 assert.throws(()=>checkedFlagOperations([{kind:'flag',id:'../secret',value:3}]));
});
test('old cloud favorite/answered data is deleted, never migrated; shared doubts survive',async()=>{
 const db=database();await db.setJSON('v1/favorite/q-001',{on:true,color:'red'});await db.setJSON('v1/answered/q-001',{on:true});await db.setJSON('v1/doubt/q-002',{on:true});
 const a=await device(db);await a.sync.refresh();assert.deepEqual(a.local.flags,{});assert.deepEqual(a.local.doubts,['q-002']);assert.equal(db.values.has('v1/favorite/q-001'),false);assert.equal(db.values.has('v1/answered/q-001'),false);
 const r=await handleAccountMarks(new Request(markURL,{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+a.session.token},body:JSON.stringify({schemaVersion:1,operations:[{kind:'favorite',id:'q-001',on:true}]})}),db);assert.equal(r.status,409);
});
test('cloud flags and net progress are private per account; doubts are shared',async()=>{
 const db=database(),a=await device(db,'weiru'),b=await device(db,'demo');await a.sync.refresh();await b.sync.refresh();
 a.act('q-001',2);a.sync.queueAll([{kind:'doubt',id:'q-002',on:true}]);await idle(a.sync);await b.sync.refresh();assert.deepEqual(b.local.flags,{});assert.deepEqual(b.local.practice,[]);assert.deepEqual(b.local.doubts,['q-002']);
 b.act('q-001',5);await idle(b.sync);await a.sync.refresh();assert.equal(a.local.flags['q-001'],2);assert.equal(b.local.flags['q-001'],5);
 const another=await device(db,'weiru');await another.sync.refresh();assert.deepEqual(another.local,a.local);
});
test('offline round trip preserves both signed actions and final general state through reload/retry',async()=>{
 const db=database(),raw=memory(),a=await device(db,'weiru',raw,async()=>{throw Error('offline');});a.act('q-001',2);await idle(a.sync);a.act('q-001',3);await idle(a.sync);
 const pending=JSON.parse(a.storage.getItem(FLAG_OUTBOX_KEY));assert.equal(pending.filter(op=>op.kind==='practice').length,2);assert.equal(pending.find(op=>op.kind==='flag').value,3);
 const reloaded=await device(db,'weiru',raw);await reloaded.sync.refresh();assert.equal(reloaded.local.flags['q-001'],3);assert.equal(dailyCounts(reloaded.local.practice)[0].count,0);assert.equal(reloaded.storage.getItem(FLAG_OUTBOX_KEY),null);
 await reloaded.sync.refresh();assert.equal(reloaded.local.practice.length,2);
});
test('newer flag and negative event survive an older slow acknowledgement',async()=>{
 const db=database();let release,started;const began=new Promise(resolve=>started=resolve);let first=true;
 const fetcher=async(url,options={})=>{if(options.method==='POST'&&first){first=false;started();await new Promise(resolve=>release=resolve);}return api(db)(url,options);};
 const a=await device(db,'weiru',memory(),fetcher);a.act('q-001',2);await began;a.act('q-001',3);release();await idle(a.sync);assert.equal(a.local.flags['q-001'],3);assert.equal(dailyCounts(a.local.practice)[0].count,0);assert.equal(a.local.practice.length,2);
});

test('offline shared-doubt cancellation syncs when either account next signs in, without transferring private flags',async()=>{
 const db=database(),raw=memory();await db.setJSON('v1/doubt/q-002',{on:true});
 const demo=await device(db,'demo',raw,async()=>{throw Error('offline');});demo.act('q-001',5);demo.sync.queueAll([{kind:'doubt',id:'q-002',on:false}]);await idle(demo.sync);
 const weiru=await device(db,'weiru',raw);await weiru.sync.refresh();assert.deepEqual(weiru.local.flags,{});assert.deepEqual(weiru.local.practice,[]);assert.deepEqual(weiru.local.doubts,[]);assert.equal(db.values.get('v1/doubt/q-002').on,false);
 assert.ok(demo.storage.getItem(FLAG_OUTBOX_KEY),'Demo private work remains in Demo outbox');
});
