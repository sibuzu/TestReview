import {accountEndpoint} from './account-policy.js';
export const SESSION_KEY='weirugo:session:v1';
export function readSession(storage){
 try{const row=JSON.parse(storage.getItem(SESSION_KEY)||'null');return ['weiru','demo'].includes(row?.user)&&/^[0-9a-f]{64}$/.test(row?.token)?{user:row.user,token:row.token}:null;}catch{return null;}
}
async function request(options={},fetcher=globalThis.fetch.bind(globalThis)){
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
 try{return await fetcher(accountEndpoint('session'),{...options,cache:'no-store',signal:controller.signal});}finally{clearTimeout(timer);}
}
export async function signIn(storage,user,password,fetcher){
 let response;try{response=await request({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user,password})},fetcher);}catch{throw Error('暫時無法連線，請稍後再試。');}
 let body;try{body=await response.json();}catch{throw Error('暫時無法Sign In，請稍後重試。');}if(!response.ok)throw Error(body.error||'暫時無法Sign In。');
 const session={user:body.user,token:body.token};if(!['weiru','demo'].includes(session.user)||!/^[0-9a-f]{64}$/.test(session.token))throw Error('Sign In回應不正確。');
 storage.setItem(SESSION_KEY,JSON.stringify(session));return session;
}
export async function restoreSession(storage,fetcher){
 const session=readSession(storage);if(!session)return null;
 try{const response=await request({headers:{Authorization:'Bearer '+session.token}},fetcher);if(response.status===401){storage.removeItem(SESSION_KEY);return null;}if(response.ok){const body=await response.json();if(body.user!==session.user){storage.removeItem(SESSION_KEY);return null;}}}catch{}
 // Network outages do not expire a remembered session.
 return session;
}
export async function signOut(storage,session,fetcher){
 storage.removeItem(SESSION_KEY);
 if(session)try{await request({method:'DELETE',headers:{Authorization:'Bearer '+session.token},keepalive:true},fetcher);}catch{}
}
export function accountStorage(storage,user){
 if(!['weiru','demo'].includes(user))throw Error('Unknown account');
 const prefix='weirugo:user:'+user+':',shared='test-review:doubts:v1';
 const keyFor=key=>key===shared?key:prefix+key;
 // Only the first account inherits any work made during the pre-sign-in preview.
 if(user==='weiru')for(const key of ['weirugo:article-flags:v1','weirugo:practice-days:v1','weirugo:flag-outbox:v1']){
  const value=storage.getItem(key);if(value!==null){if(storage.getItem(keyFor(key))===null)storage.setItem(keyFor(key),value);storage.removeItem(key);}
 }
 return {getItem:key=>storage.getItem(keyFor(key)),setItem:(key,value)=>storage.setItem(keyFor(key),value),removeItem:key=>storage.removeItem(keyFor(key)),ownsKey:key=>key===shared||key?.startsWith(prefix)};
}
