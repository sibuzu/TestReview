// Hash URLs work on Live Server and static hosts without redirect rules.
import {canonicalQuestionId} from './question-identity.js';
export function questionHash(id){return '#question/'+encodeURIComponent(canonicalQuestionId(id));}
export function listHash({subject}={}){return subject?'#subject/'+encodeURIComponent(subject):'#questions';}
export function parseRoute(hash){
 let path;try{path=decodeURIComponent(String(hash||'').replace(/^#/,''));}catch{return {kind:'questions'};}
 if(path.startsWith('question/'))return {kind:'question',id:canonicalQuestionId(path.slice(9))};
 if(path.startsWith('subject/'))return {kind:'questions',subject:path.slice(8)};
 if(['sources','starred','issues','doubts'].includes(path))return {kind:path};
 return {kind:'questions'};
}
