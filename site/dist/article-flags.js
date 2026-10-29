import {canonicalQuestionId} from './question-identity.js';

export const FLAGS_KEY='weirugo:article-flags:v1';
export const PRACTICE_KEY='weirugo:practice-days:v1';
export const DEFAULT_FLAG=3;
export const FLAG_OPTIONS=Object.freeze([
 {value:1,label:'不重要',color:'#89929c'},
 {value:2,label:'已作',color:'#22a06b'},
 {value:3,label:'一般',color:'#3b82f6'},
 {value:4,label:'重要',color:'#f59e0b'},
 {value:5,label:'很重要',color:'#ef4444'},
]);
export const validQuestionId=id=>typeof id==='string'&&/^q-\d{3,6}$/.test(id);
export const validFlag=value=>Number.isInteger(value)&&value>=1&&value<=5;
export const validEventId=id=>typeof id==='string'&&/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id);
export function validDay(day){return typeof day==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(day)&&Number.isFinite(Date.parse(day+'T00:00:00Z'))&&new Date(day+'T00:00:00Z').toISOString().slice(0,10)===day;}
export function checkedFlags(value){
 if(!value||typeof value!=='object'||Array.isArray(value))throw Error('FLAG格式不正確。');
 const out={};
 for(const [id,flag] of Object.entries(value)){
  if(!validQuestionId(id)||!validFlag(flag))throw Error('FLAG格式不正確。');
  const key=canonicalQuestionId(id);if(!(key in out)||id===key)out[key]=flag;
 }
 return out;
}
export function checkedPractice(value){
 if(!Array.isArray(value))throw Error('每日進度格式不正確。');
 const records=new Map();
 for(const item of value){
  if(!item||!validQuestionId(item.id)||!validDay(item.day)||!validEventId(item.eventId)||![1,-1].includes(item.delta))throw Error('每日進度格式不正確。');
  const event={id:canonicalQuestionId(item.id),day:item.day,eventId:item.eventId,delta:item.delta};
  if(records.has(event.eventId)&&JSON.stringify(records.get(event.eventId))!==JSON.stringify(event))throw Error('進度紀錄識別碼重複。');
  records.set(event.eventId,event);
 }
 return [...records.values()].sort((a,b)=>b.day.localeCompare(a.day)||a.eventId.localeCompare(b.eventId));
}
export function practiceDay(date=new Date()){
 const parts=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(date);
 return ['year','month','day'].map(type=>parts.find(p=>p.type===type).value).join('-');
}
export function dailyCounts(events){
 const counts=new Map();for(const {day,delta} of checkedPractice(events))counts.set(day,(counts.get(day)||0)+delta);
 return [...counts].map(([day,count])=>({day,count})).sort((a,b)=>b.day.localeCompare(a.day));
}
export function changedFlag(flags,events,id,value,day=practiceDay(),eventId=globalThis.crypto.randomUUID()){
 if(!validQuestionId(id)||!validFlag(value)||!validDay(day))throw Error('FLAG格式不正確。');
 const next=checkedFlags(flags),key=canonicalQuestionId(id),previous=next[key]??DEFAULT_FLAG;
 next[key]=value;
 const delta=previous===3&&value!==3?1:previous!==3&&value===3?-1:0;
 return {flags:next,practice:checkedPractice([...events,...(delta?[{id:key,day,eventId,delta}]:[])])};
}
export function persistFlagState(storage,flags,practice,doubts){
 const checked={flags:checkedFlags(flags),practice:checkedPractice(practice)},keys=[FLAGS_KEY,PRACTICE_KEY],values=[checked.flags,checked.practice];
 if(doubts!==undefined){
  if(!Array.isArray(doubts)||doubts.some(id=>!validQuestionId(id)))throw Error('疑義格式不正確。');
  checked.doubts=[...new Set(doubts.map(canonicalQuestionId))].sort();keys.push('test-review:doubts:v1');values.push(checked.doubts);
 }
 const previous=keys.map(key=>storage.getItem(key));
 try{keys.forEach((key,i)=>storage.setItem(key,JSON.stringify(values[i])));}
 catch(error){keys.forEach((key,i)=>{try{if(previous[i]===null)storage.removeItem(key);else storage.setItem(key,previous[i]);}catch{}});throw error;}
 return checked;
}
export function discardLegacyMarks(storage){
 // The user explicitly requested deleting old favorites/answered, not migrating them.
 const outbox='test-review:mark-outbox:v1';let doubts=[];
 try{doubts=JSON.parse(storage.getItem(outbox)||'[]').filter(op=>op.kind==='doubt'&&validQuestionId(op.id)&&typeof op.on==='boolean');}catch{}
 for(const key of ['test-review:favorites:v1','test-review:answered:v1','test-review:favorite-colors:v1',outbox])storage.removeItem(key);
 return doubts;
}

const FLAG_PATH="M6 4.6405C8.14486 3.74467 9.6336 4.18817 11.3124 4.81067C11.4311 4.85469 11.5513 4.89999 11.6733 4.94593C13.3072 5.56146 15.2418 6.29025 17.7738 5.55804C17.8375 5.53959 17.9132 5.55221 17.9674 5.58773C17.9883 5.60145 17.9973 5.61409 18 5.61808C18 5.61771 18 5.61838 18 5.61808V14.2515C15.8581 14.7894 14.3554 14.3169 12.6399 13.7776C12.448 13.7172 12.2535 13.6561 12.0551 13.5954C11.0694 13.2939 9.9815 13.0088 8.73583 13.0151C7.88099 13.0195 6.97966 13.1602 6 13.4946V4.6405ZM18 14.2793C18 14.2796 18 14.2796 18 14.2793V14.2793ZM6 15.637C7.06717 15.1778 7.95744 15.0191 8.74594 15.0151C9.68064 15.0104 10.5334 15.2214 11.4701 15.5079C11.657 15.5651 11.8472 15.6255 12.0411 15.6871C13.7733 16.2375 15.806 16.8834 18.556 16.1737C19.4513 15.9427 20 15.1264 20 14.2793V5.61808C20 4.07013 18.4318 3.28578 17.2182 3.63676C15.3407 4.17972 13.9832 3.67282 12.3112 3.04849C12.2112 3.01116 12.1101 2.97341 12.0077 2.93544C10.1745 2.25566 8.06074 1.59139 5.17004 2.81992C4.41981 3.13876 4 3.87464 4 4.61804V21C4 21.5523 4.44772 22 5 22C5.55228 22 6 21.5523 6 21V15.637Z";

export function flagIcon(value){
 if(value===2)return '<svg class="article-flag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>';
 return '<svg class="article-flag-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="'+FLAG_PATH+'"/></svg>';
}
