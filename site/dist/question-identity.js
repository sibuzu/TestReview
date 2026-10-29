import {QUESTION_ALIASES} from './question-alias-data.js';

export function canonicalQuestionId(id){
 const seen=new Set();
 while(QUESTION_ALIASES[id]&&!seen.has(id)){seen.add(id);id=QUESTION_ALIASES[id];}
 return id;
}
export function equivalentQuestionIds(id){
 const canonical=canonicalQuestionId(id);
 return [canonical,...Object.keys(QUESTION_ALIASES).filter(alias=>canonicalQuestionId(alias)===canonical)];
}
export function hasQuestionMark(ids,id){return equivalentQuestionIds(id).some(candidate=>ids.has(candidate));}
export function toggleQuestionMark(ids,id){
 const on=!hasQuestionMark(ids,id),next=new Set(ids);
 for(const candidate of equivalentQuestionIds(id))next.delete(candidate);
 if(on)next.add(canonicalQuestionId(id));
 return next;
}
