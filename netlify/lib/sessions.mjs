import {createHash,randomBytes,timingSafeEqual} from 'node:crypto';
import {allowedAccountOrigin,accountCORS} from '../../site/dist/account-policy.js';
const users=new Set(['weiru','demo']);
const json=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'}});
const sessionKey=token=>'sessions/v1/'+createHash('sha256').update(token).digest('hex');
export async function sessionUser(request,store){
 const match=request.headers.get('Authorization')?.match(/^Bearer ([0-9a-f]{64})$/);
 if(!match)return null;
 const row=await store.get(sessionKey(match[1]),{type:'json',consistency:'strong'});
 return users.has(row?.user)?row.user:null;
}
export async function handleSession(request,store){
 const origin=request.headers.get('Origin');if(!allowedAccountOrigin(origin))return json({error:'來源格式不正確。'},403);
 if(request.method==='OPTIONS')return accountCORS(new Response(null,{status:204}),origin);
 return accountCORS(await sessionRequest(request,store),origin);
}
async function sessionRequest(request,store){
 if(request.method==='POST'){
  if(!request.headers.get('Content-Type')?.startsWith('application/json'))return json({error:'請使用JSON格式。'},415);
  let user,password;
  try{const text=await request.text();if(text.length>4096)throw Error();const body=JSON.parse(text);user=typeof body.user==='string'?body.user.trim().toLowerCase():'';password=body.password;}catch{return json({error:'帳號或密碼不正確。'},400);}
  const supplied=Buffer.from(typeof password==='string'?password:'');
  if(!users.has(user)||supplied.length!==4||!timingSafeEqual(supplied,Buffer.from('1234')))return json({error:'帳號或密碼不正確。'},401);
  const token=randomBytes(32).toString('hex');await store.setJSON(sessionKey(token),{user});
  return json({user,token});
 }
 const user=await sessionUser(request,store);if(!user)return json({error:'請先Sign In。'},401);
 if(request.method==='GET')return json({user});
 if(request.method==='DELETE'){
  await store.delete(sessionKey(request.headers.get('Authorization').slice(7)));
  return new Response(null,{status:204,headers:{'Cache-Control':'no-store'}});
 }
 return json({error:'不支援此方法。'},405);
}
export function accountStore(store,user){
 if(!users.has(user))throw Error('Unknown account');
 const prefix='users/'+user+'/',map=key=>key.startsWith('v2/')?prefix+key:key;
 return {
  async list(options){const actual=map(options.prefix),result=await store.list({...options,prefix:actual});return {...result,blobs:result.blobs.filter(row=>row.key.startsWith(actual)).map(row=>({...row,key:row.key.startsWith(prefix)?row.key.slice(prefix.length):row.key}))};},
  get:(key,options)=>store.get(map(key),options),
  setJSON:(key,value)=>store.setJSON(map(key),value),
  delete:key=>store.delete(map(key)),
 };
}
