import {QUESTION_ALIASES} from './question-alias-data.js';
import {QUESTION_GROUPS} from './question-group-data.js';

// Duplicate identities predate groups. Keep every group's child marks independent.
export function canonicalMarkQuestionId(id){
 const seen=new Set();
 while(QUESTION_ALIASES[id]&&!seen.has(id)){seen.add(id);id=QUESTION_ALIASES[id];}
 return id;
}

export function canonicalQuestionId(id){
 const seen=new Set();
 const redirects={...QUESTION_ALIASES};
 for(const [parent,group] of Object.entries(QUESTION_GROUPS))for(const member of group.members)if(member!==parent)redirects[member]=parent;
 while(redirects[id]&&!seen.has(id)){seen.add(id);id=redirects[id];}
 return id;
}
export function equivalentQuestionIds(id){
 const canonical=canonicalQuestionId(id);
 const ids=new Set([canonical,...Object.keys(QUESTION_ALIASES),...Object.values(QUESTION_GROUPS).flatMap(g=>g.members)]);
 return [...ids].filter(candidate=>canonicalQuestionId(candidate)===canonical);
}
export function hasQuestionMark(ids,id){return equivalentQuestionIds(id).some(candidate=>ids.has(candidate));}
export function toggleQuestionMark(ids,id){
 const on=!hasQuestionMark(ids,id),next=new Set(ids);
 for(const candidate of equivalentQuestionIds(id))next.delete(candidate);
 if(on)next.add(canonicalQuestionId(id));
 return next;
}
