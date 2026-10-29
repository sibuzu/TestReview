import {validFlag,validQuestionId,validDay,validEventId} from './article-flags.js';
import {canonicalMarkQuestionId} from './question-identity.js';
import {checkedGroupFlags} from './group-marks.js';
export const flagOperationKey=op=>op.kind==='practice'?'practice/'+op.eventId:op.kind==='groupFlag'?'groupFlag/'+op.id+'/'+op.revision:op.kind+'/'+op.id;
export function checkedFlagOperations(operations,limit=250000){
 if(!Array.isArray(operations)||operations.length>limit)throw Error('標記資料格式不正確。');
 return operations.map(op=>{
  if(!op||!validQuestionId(op.id))throw Error('題目ID不正確。');
  const id=canonicalMarkQuestionId(op.id);
  if(op.kind==='groupFlag'&&Object.keys(op).every(k=>['kind','id','value','revision','operationId'].includes(k)))return {kind:'groupFlag',...checkedGroupFlags([{id,value:op.value,revision:op.revision,operationId:op.operationId}])[0]};
  if(op.kind==='flag'&&validFlag(op.value)&&Object.keys(op).every(k=>['kind','id','value'].includes(k)))return {kind:'flag',id,value:op.value};
  if(op.kind==='doubt'&&typeof op.on==='boolean'&&Object.keys(op).every(k=>['kind','id','on'].includes(k)))return {kind:'doubt',id,on:op.on};
  if(op.kind==='practice'&&validDay(op.day)&&validEventId(op.eventId)&&[1,-1].includes(op.delta)&&Object.keys(op).every(k=>['kind','id','day','eventId','delta'].includes(k)))return {kind:'practice',id,day:op.day,eventId:op.eventId,delta:op.delta};
  throw Error('標記資料格式不正確。');
 });
}
