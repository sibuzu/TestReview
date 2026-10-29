import {QUESTION_GROUPS} from './question-group-data.js';
import {canonicalMarkQuestionId} from './question-identity.js';
import {DEFAULT_FLAG,validFlag,validQuestionId,validDay,validEventId,checkedFlags,checkedPractice,practiceDay} from './article-flags.js';

export const GROUP_FLAGS_KEY='weirugo:group-flags:v1';
export const validGroupRevision=value=>typeof value==='string'&&/^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$/.test(value);
const recordKey=record=>record.id+'/'+record.revision;

// Keep raw member state and previous membership revisions. Route redirects must
// never collapse distinct original FLAGs or turn the oldest child into an
// explicit whole-group choice.
export function checkedGroupFlags(value){
 if(!Array.isArray(value))throw Error('題組FLAG格式不正確。');
 const records=new Map(),operations=new Map();
 for(const record of value){
  if(!record||Object.keys(record).some(k=>!['id','value','revision','operationId'].includes(k))||!validQuestionId(record.id)||!validFlag(record.value)||!validGroupRevision(record.revision)||!validEventId(record.operationId))throw Error('題組FLAG格式不正確。');
  const clean={id:canonicalMarkQuestionId(record.id),value:record.value,revision:record.revision,operationId:record.operationId};
  if(operations.has(clean.operationId)&&JSON.stringify(operations.get(clean.operationId))!==JSON.stringify(clean))throw Error('題組FLAG操作識別碼重複。');
  operations.set(clean.operationId,clean);records.set(recordKey(clean),clean);
 }
 return [...records.values()].sort((a,b)=>recordKey(a).localeCompare(recordKey(b)));
}

export function effectiveFlag(flags,groupFlags,id,groups=QUESTION_GROUPS){
 const raw=checkedFlags(flags),key=canonicalMarkQuestionId(id),group=groups[key];
 if(!group)return raw[key]??DEFAULT_FLAG;
 const explicit=checkedGroupFlags(groupFlags).find(record=>record.id===key&&record.revision===group.revision);
 if(explicit)return explicit.value;
 // A merged question is a new review item: old child FLAGs are not inherited.
 return DEFAULT_FLAG;
}

export function changedGroupFlag(flags,groupFlags,practice,id,value,day=practiceDay(),eventId=globalThis.crypto.randomUUID(),operationId=globalThis.crypto.randomUUID(),groups=QUESTION_GROUPS){
 const key=canonicalMarkQuestionId(id),group=groups[key];
 if(!validQuestionId(key)||!group||!validGroupRevision(group.revision)||!validFlag(value)||!validDay(day)||!validEventId(operationId))throw Error('題組FLAG格式不正確。');
 const previous=effectiveFlag(flags,groupFlags,key,groups),delta=previous===3&&value!==3?1:previous!==3&&value===3?-1:0;
 const record={id:key,value,revision:group.revision,operationId};
 const next=checkedGroupFlags([...checkedGroupFlags(groupFlags).filter(row=>recordKey(row)!==recordKey(record)),record]);
 return {groupFlags:next,practice:checkedPractice([...practice,...(delta?[{id:key,day,eventId,delta}]:[])]),operation:{kind:'groupFlag',...record}};
}
