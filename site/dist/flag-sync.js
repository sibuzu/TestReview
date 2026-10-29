import {accountEndpoint} from './account-policy.js';
import {checkedFlagOperations,flagOperationKey} from './flag-protocol.js';
import {checkedFlags,checkedPractice} from './article-flags.js';
export const FLAG_OUTBOX_KEY='weirugo:flag-outbox:v1';

export class FlagSync{
 constructor({storage,getLocal,apply,status,getToken=()=>null,fetcher=globalThis.fetch.bind(globalThis),endpoint=accountEndpoint('marks')}){
  Object.assign(this,{storage,getLocal,apply,status,getToken,fetcher,endpoint});
  this.localOnly=endpoint===null;this.pending=new Map();this.sequence=0;this.snapshot=[];this.etag='';
  if(this.localOnly){this.available=false;try{storage.removeItem(FLAG_OUTBOX_KEY);}catch{}return;}
  try{for(const op of checkedFlagOperations(JSON.parse(storage.getItem(FLAG_OUTBOX_KEY)||'[]')))this.pending.set(flagOperationKey(op),{...op,seq:++this.sequence});}catch{}
 }
 persist(){try{if(this.pending.size)this.storage.setItem(FLAG_OUTBOX_KEY,JSON.stringify([...this.pending.values()].map(({seq,...op})=>op)));else this.storage.removeItem(FLAG_OUTBOX_KEY);}catch{}}
 queueAll(operations){
  if(this.localOnly){this.status('local');return;}
  for(const op of checkedFlagOperations(operations))this.pending.set(flagOperationKey(op),{...op,seq:++this.sequence});
  this.persist();this.status(this.available===false?'local':'pending');if(this.available!==false)void this.refresh();
 }
 importLocalUnknown(){
  const local=this.getLocal(),remote=new Set(this.snapshot.map(flagOperationKey));
  const operations=[...Object.entries(checkedFlags(local.flags||{})).map(([id,value])=>({kind:'flag',id,value})),
   ...(local.doubts||[]).map(id=>({kind:'doubt',id,on:true})),...checkedPractice(local.practice||[]).map(event=>({kind:'practice',...event}))];
  for(const op of checkedFlagOperations(operations)){const key=flagOperationKey(op);if(!remote.has(key)&&!this.pending.has(key))this.pending.set(key,{...op,seq:++this.sequence});}
  this.persist();
 }
 publish(){
  const all=new Map(this.snapshot.map(op=>[flagOperationKey(op),op]));for(const op of this.pending.values())all.set(flagOperationKey(op),op);
  const flags={},doubts=[],practice=[];
  for(const op of all.values()){
   if(op.kind==='flag')flags[op.id]=op.value;
   if(op.kind==='doubt'&&op.on)doubts.push(op.id);
   if(op.kind==='practice')practice.push({id:op.id,day:op.day,eventId:op.eventId,delta:op.delta});
  }
  this.apply({flags:checkedFlags(flags),doubts:doubts.sort(),practice:checkedPractice(practice)});
 }
 refresh(){
  if(this.localOnly){this.available=false;this.status('local');return Promise.resolve();}
  if(this.busy){this.again=true;return this.busy;}
  this.busy=this.run().finally(()=>{this.busy=null;if(this.again){this.again=false;void this.refresh();}});return this.busy;
 }
 async request(options={}){
  if(this.localOnly)throw Error('Local-only entry.');
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
  const token=this.getToken(),headers={...options.headers,...(token?{Authorization:'Bearer '+token}:{})};
  try{return await this.fetcher(this.endpoint,{...options,headers,cache:'no-store',signal:controller.signal});}finally{clearTimeout(timer);}
 }
 async run(){
  if(this.localOnly){this.status('local');return;}
  this.status('syncing');
  try{
   const response=await this.request({headers:this.etag?{'If-None-Match':this.etag}:{}});
   if(response.status===404){this.available=false;this.status('local');return;}
   this.available=true;
   if(response.status!==304){
    if(!response.ok)throw Error('Cloud unavailable');
    const body=await response.json();this.serverVersion=body.schemaVersion;
    if(this.serverVersion===2){this.snapshot=checkedFlagOperations(body.marks);this.serverKinds=['flag','doubt','practice'];}
    else if(this.serverVersion===1){this.snapshot=checkedFlagOperations(body.marks.filter(op=>op.kind==='doubt'));this.serverKinds=['doubt'];}
    else throw Error('Unsupported version');
    this.etag=response.headers.get('ETag')||'';
   }
   this.importLocalUnknown();this.publish();
   while(this.pending.size){
    const batch=[...this.pending.values()].filter(op=>this.serverKinds.includes(op.kind)).slice(0,100);if(!batch.length)break;
    const sent=batch.map(({seq,...op})=>op);
    const response=await this.request({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({schemaVersion:this.serverVersion,operations:sent})});
    if(!response.ok)throw Error('Cloud write failed');
    const ack=await response.json(),applied=checkedFlagOperations(ack.applied,100);
    if(JSON.stringify(applied)!==JSON.stringify(sent))throw Error('Cloud acknowledgement mismatch');
    for(const op of batch)if(this.pending.get(flagOperationKey(op))?.seq===op.seq)this.pending.delete(flagOperationKey(op));
    const merged=new Map(this.snapshot.map(op=>[flagOperationKey(op),op]));for(const op of sent)merged.set(flagOperationKey(op),op);
    this.snapshot=[...merged.values()];this.etag='';this.persist();this.publish();
   }
   this.status(this.pending.size?'pending':'synced');
  }catch{this.status('pending');}
 }
}
