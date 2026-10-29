import test,{beforeEach,afterEach} from 'node:test';
import assert from 'node:assert/strict';
import {QUESTION_GROUPS} from '../dist/question-group-data.js';
import {canonicalQuestionId,canonicalMarkQuestionId} from '../dist/question-identity.js';
import {GROUP_FLAGS_KEY,checkedGroupFlags,effectiveFlag,changedGroupFlag} from '../dist/group-marks.js';
import {FLAGS_KEY,PRACTICE_KEY,checkedFlags,checkedPractice,dailyCounts,persistFlagState} from '../dist/article-flags.js';
import {checkedFlagOperations,flagOperationKey} from '../dist/flag-protocol.js';
import {FlagSync,FLAG_OUTBOX_KEY} from '../dist/flag-sync.js';
import {signIn,accountStorage} from '../dist/auth.js';
import {handleSession} from '../../netlify/lib/sessions.mjs';
import {handleAccountMarks} from '../../netlify/lib/account-marks.mjs';

const day='2026-10-29',uuid=n=>'00000000-0000-4000-8000-'+String(n).padStart(12,'0');
const group={members:['q-029','q-031'],revision:'r1',displayOrder:['q-029','q-031']};
let previous;
beforeEach(()=>{previous={...QUESTION_GROUPS};QUESTION_GROUPS['q-029']=structuredClone(group);});
afterEach(()=>{for(const key of Object.keys(QUESTION_GROUPS))delete QUESTION_GROUPS[key];Object.assign(QUESTION_GROUPS,previous);});
const row=(value=2,n=1,revision='r1')=>({id:'q-029',value,revision,operationId:uuid(n)});
const op=(value=2,n=1,revision='r1')=>({kind:'groupFlag',...row(value,n,revision)});
const memory=()=>{const map=new Map();return {map,getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,String(v)),removeItem:k=>map.delete(k)};};
const database=()=>{const values=new Map();return {values,list:async({prefix=''})=>({blobs:[...values.keys()].filter(k=>k.startsWith(prefix)).map(key=>({key}))}),get:async key=>structuredClone(values.get(key)??null),setJSON:async(key,value)=>values.set(key,structuredClone(value)),delete:async key=>values.delete(key)};};
const url='https://mytestreview.netlify.app/.netlify/functions/marks';
const api=db=>async(address,options={})=>address.includes('/session')?handleSession(new Request(address,options),db):handleAccountMarks(new Request(address,options),db);
async function idle(sync){for(let i=0;i<40&&sync.busy;i++)await sync.busy;assert.equal(sync.busy,null);}
async function device(db,user='weiru',raw=memory(),fetcher=api(db)){
 const session=await signIn(raw,user,'1234',api(db)),storage=accountStorage(raw,user),statuses=[];
 let local={flags:JSON.parse(storage.getItem(FLAGS_KEY)||'{}'),groupFlags:JSON.parse(storage.getItem(GROUP_FLAGS_KEY)||'[]'),practice:JSON.parse(storage.getItem(PRACTICE_KEY)||'[]'),doubts:[]};
 const sync=new FlagSync({storage,getLocal:()=>local,apply:state=>{local=state;persistFlagState(storage,state.flags,state.practice,state.doubts,state.groupFlags);},status:s=>statuses.push(s),getToken:()=>session.token,endpoint:url,fetcher});
 return {session,storage,raw,sync,statuses,get local(){return local;},act(value,n,date=day){const existing=new Set(local.practice.map(e=>e.eventId)),next=changedGroupFlag(local.flags,local.groupFlags,local.practice,'q-029',value,date,uuid(n),uuid(n+100));local={...local,groupFlags:next.groupFlags,practice:next.practice};persistFlagState(storage,local.flags,local.practice,local.doubts,local.groupFlags);sync.queueAll([next.operation,...local.practice.filter(e=>!existing.has(e.eventId)).map(e=>({kind:'practice',...e}))]);}};
}

test('new groups always start at general three, regardless of old child flags',()=>{
 const flags={'q-029':2},copy=structuredClone(flags);assert.equal(effectiveFlag(flags,[],'q-029'),3);
 assert.equal(effectiveFlag({'q-029':1,'q-031':2},[],'q-029'),3);
 assert.equal(effectiveFlag({'q-029':5},[],'q-029'),3);assert.equal(effectiveFlag({},[],'q-029'),3);
 assert.equal(effectiveFlag({'q-031':4},[],'q-031'),4,'raw child query remains independent');assert.deepEqual(flags,copy);
});
test('an explicit whole-group choice wins over old child five; the oldest raw child is not an explicit choice',()=>{
 const flags={'q-029':2,'q-031':5};assert.equal(effectiveFlag(flags,[],'q-029'),3);
 assert.equal(effectiveFlag(flags,[row(2)],'q-029'),2);assert.deepEqual(flags,{'q-029':2,'q-031':5});
});
test('membership revisions keep historical explicit choices but do not apply them to new membership',()=>{
 const historical=[row(1,1,'r0')];assert.equal(effectiveFlag({},historical,'q-029'),3);
 const next=changedGroupFlag({},historical,[],'q-029',2,day,uuid(2),uuid(3));assert.equal(next.groupFlags.length,2);
 assert.equal(effectiveFlag({},next.groupFlags,'q-029'),2);QUESTION_GROUPS['q-029'].revision='r2';assert.equal(effectiveFlag({},next.groupFlags,'q-029'),3);
});
test('choosing default general saves explicit intent without generating a practice event',()=>{
 const flags={'q-029':5,'q-031':3},next=changedGroupFlag(flags,[],[],'q-029',3,day,uuid(1),uuid(2));
 assert.deepEqual(next.practice,[]);assert.deepEqual(next.groupFlags,[row(3,2)]);assert.deepEqual(next.operation,op(3,2));
 assert.equal(effectiveFlag({'q-029':1,'q-031':1},next.groupFlags,'q-029'),3);
});
test('only actual group general transitions add signed UUID events; legacy child history is unchanged',()=>{
 const legacy={id:'q-031',day,eventId:uuid(9),delta:1};let next=changedGroupFlag({},[],[legacy],'q-029',2,day,uuid(1),uuid(2));
 next=changedGroupFlag({},next.groupFlags,next.practice,'q-029',3,day,uuid(3),uuid(4));assert.equal(dailyCounts(next.practice)[0].count,1);assert.deepEqual(next.practice.find(e=>e.eventId===uuid(9)),legacy);
 next=changedGroupFlag({},next.groupFlags,next.practice,'q-029',4,day,uuid(5),uuid(6));const count=next.practice.length;
 next=changedGroupFlag({},next.groupFlags,next.practice,'q-029',5,day,uuid(7),uuid(8));assert.equal(next.practice.length,count);
 next=changedGroupFlag({},next.groupFlags,next.practice,'q-029',3,'2026-10-30',uuid(10),uuid(11));assert.equal(dailyCounts(next.practice)[0].count,-1);
});
test('group validation rejects traversal, malformed UUIDs and operation-ID conflicts',()=>{
 for(const bad of [{...row(),revision:'../x'},{...row(),operationId:'bad'},{...row(),value:9},{...row(),extra:true}])assert.throws(()=>checkedGroupFlags([bad]));
 assert.throws(()=>checkedGroupFlags([row(2,1),row(5,1)]));assert.equal(checkedGroupFlags([row(),row()]).length,1);
 assert.deepEqual(checkedGroupFlags([{...row(),id:'q-821'}]),[{...row(),id:'q-820'}],'pre-existing duplicate alias remains compatible');
});
test('group routes redirect but atomic flags, doubts and daily IDs do not collapse',()=>{
 assert.equal(canonicalQuestionId('q-031'),'q-029');assert.equal(canonicalMarkQuestionId('q-031'),'q-031');
 assert.deepEqual(checkedFlags({'q-029':2,'q-031':5}),{'q-029':2,'q-031':5});
 const events=[{id:'q-029',day,eventId:uuid(1),delta:1},{id:'q-031',day,eventId:uuid(2),delta:1}];assert.deepEqual(checkedPractice(events).map(e=>e.id).sort(),['q-029','q-031']);assert.equal(dailyCounts(events)[0].count,2);
 assert.equal(checkedFlagOperations([{kind:'doubt',id:'q-031',on:true}])[0].id,'q-031');
});
test('the group outbox keys membership revisions separately and rejects unknown protocol fields',()=>{
 assert.notEqual(flagOperationKey(op(2,1,'r0')),flagOperationKey(op(2,2,'r1')));assert.deepEqual(checkedFlagOperations([op()]),[op()]);
 assert.throws(()=>checkedFlagOperations([{...op(),unexpected:true}]));
});
test('group flags join the same atomic local rollback as raw flags, events and shared doubts',()=>{
 const base=memory();persistFlagState(base,{'q-029':5},[],['q-031'],[row(5)]);const before=[...base.map];let fail=true;
 const storage={...base,setItem(key,value){if(key===GROUP_FLAGS_KEY&&fail){fail=false;throw Error('full');}base.setItem(key,value);}};
 assert.throws(()=>persistFlagState(storage,{'q-029':2},[{id:'q-029',day,eventId:uuid(9),delta:1}],[],[row(2,2)]));assert.deepEqual([...base.map],before);
});
test('cloud stores group revisions separately, never overwrites children, and retries preserve original daily events',async()=>{
 const db=database();await db.setJSON('users/weiru/v2/flag/q-029',{value:2});await db.setJSON('users/weiru/v2/flag/q-031',{value:5});
 const d=await device(db);const operations=[op(1,1,'r0'),op(2,2,'r1'),{kind:'practice',id:'q-029',day,eventId:uuid(3),delta:1},{kind:'practice',id:'q-031',day,eventId:uuid(4),delta:1}];
 const options={method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+d.session.token},body:JSON.stringify({schemaVersion:2,operations})};
 for(let i=0;i<2;i++)assert.equal((await api(db)(url,options)).status,200);
 await d.sync.refresh();assert.deepEqual(d.local.flags,{'q-029':2,'q-031':5});assert.equal(d.local.groupFlags.length,2);assert.equal(effectiveFlag(d.local.flags,d.local.groupFlags,'q-029'),2);assert.equal(d.local.practice.length,2);assert.equal(dailyCounts(d.local.practice)[0].count,2);
 assert.deepEqual(db.values.get('users/weiru/v2/flag/q-031'),{value:5});assert.deepEqual(db.values.get('users/weiru/v2/groupFlag/q-029/r1'),{value:2,operationId:uuid(2)});
});
test('whole-group intent and its offline cache remain private to each signed-in account',async()=>{
 const db=database(),raw=memory(),a=await device(db,'weiru',raw),b=await device(db,'demo',raw);a.act(2,1);await idle(a.sync);b.act(5,2);await idle(b.sync);await a.sync.refresh();
 assert.equal(effectiveFlag(a.local.flags,a.local.groupFlags,'q-029'),2);assert.equal(effectiveFlag(b.local.flags,b.local.groupFlags,'q-029'),5);assert.notEqual(a.storage.getItem(GROUP_FLAGS_KEY),b.storage.getItem(GROUP_FLAGS_KEY));
});
test('invalid group operations reject a whole server batch before any private mutation',async()=>{
 const db=database(),d=await device(db);const r=await api(db)(url,{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+d.session.token},body:JSON.stringify({schemaVersion:2,operations:[{kind:'flag',id:'q-031',value:2},{...op(),revision:'../escape'}]})});
 assert.equal(r.status,400);assert.equal([...db.values.keys()].filter(k=>k.startsWith('users/')).length,0);
});
test('offline group undo survives reload and retry with both signed events, not one event per question/day',async()=>{
 const db=database(),raw=memory(),d=await device(db,'weiru',raw,async()=>{throw Error('offline');});d.act(2,1);await idle(d.sync);d.act(3,2);await idle(d.sync);
 const pending=JSON.parse(d.storage.getItem(FLAG_OUTBOX_KEY));assert.equal(pending.filter(o=>o.kind==='practice').length,2);assert.equal(pending.find(o=>o.kind==='groupFlag').value,3);
 const reloaded=await device(db,'weiru',raw);await reloaded.sync.refresh();await reloaded.sync.refresh();assert.equal(effectiveFlag(reloaded.local.flags,reloaded.local.groupFlags,'q-029'),3);assert.equal(reloaded.local.practice.length,2);assert.equal(dailyCounts(reloaded.local.practice)[0].count,0);assert.equal(reloaded.storage.getItem(FLAG_OUTBOX_KEY),null);
});
test('newer explicit group selection and undo survive an older slow cloud acknowledgement',async()=>{
 const db=database();let release,started,first=true;const began=new Promise(resolve=>started=resolve);
 const fetcher=async(address,options={})=>{if(options.method==='POST'&&first){first=false;started();await new Promise(resolve=>release=resolve);}return api(db)(address,options);};
 const d=await device(db,'weiru',memory(),fetcher);d.act(2,1);await began;d.act(3,2);release();await idle(d.sync);
 assert.equal(effectiveFlag(d.local.flags,d.local.groupFlags,'q-029'),3);assert.equal(d.local.groupFlags[0].operationId,uuid(102));assert.equal(d.local.practice.length,2);assert.equal(dailyCounts(d.local.practice)[0].count,0);assert.equal(db.values.get('users/weiru/v2/groupFlag/q-029/r1').value,3);
});
test('older v2 servers leave whole-group changes queued until their advertised capability is available',async()=>{
 const db=database();let supportsGroups=false,groupPosts=0;
 const fetcher=async(address,options={})=>{if(options.method==='POST'){const operations=JSON.parse(options.body).operations;groupPosts+=operations.filter(o=>o.kind==='groupFlag').length;}const r=await api(db)(address,options);if(!options.method&&!supportsGroups){const body=await r.json();body.kinds=['flag','doubt','practice'];return new Response(JSON.stringify(body),{status:200,headers:{'Content-Type':'application/json'}});}return r;};
 const d=await device(db,'weiru',memory(),fetcher);d.act(2,1);await idle(d.sync);assert.equal(groupPosts,0);assert.ok(d.sync.pending.size);assert.equal(effectiveFlag(d.local.flags,d.local.groupFlags,'q-029'),2);
 supportsGroups=true;await d.sync.refresh();assert.equal(groupPosts,1);assert.equal(d.sync.pending.size,0);
});
test('a first read after grouping retains old child flags and creates neither explicit group flags nor synthetic progress',async()=>{
 const db=database();await db.setJSON('users/weiru/v2/flag/q-029',{value:2});await db.setJSON('users/weiru/v2/flag/q-031',{value:5});
 const d=await device(db);await d.sync.refresh();assert.deepEqual(d.local.flags,{'q-029':2,'q-031':5});assert.deepEqual(d.local.groupFlags,[]);assert.deepEqual(d.local.practice,[]);assert.equal(effectiveFlag(d.local.flags,d.local.groupFlags,'q-029'),3);assert.equal([...db.values.keys()].filter(k=>k.includes('/groupFlag/')||k.includes('/practice/')).length,0);
});

test('long membership revisions are split into server-sized batches without losing historical intent',async()=>{
 const db=database(),sizes=[];const fetcher=async(address,options={})=>{if(options.method==='POST')sizes.push(options.body.length);return api(db)(address,options);};
 const d=await device(db,'weiru',memory(),fetcher);d.sync.queueAll(Array.from({length:100},(_,n)=>op(2,n+1000,'r'+n+'x'.repeat(120))));await idle(d.sync);
 assert.ok(sizes.length>=2);assert.ok(sizes.every(size=>size<=16384));assert.equal(d.sync.pending.size,0);assert.equal(d.local.groupFlags.length,100);
});
