import {createHash} from 'node:crypto';
import {allowedAccountOrigin,accountCORS} from '../../site/dist/account-policy.js';
import {checkedFlagOperations,flagOperationKey} from '../../site/dist/flag-protocol.js';
const json=(data,status=200,extra={})=>new Response(JSON.stringify(data),{status,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff',...extra}});
async function chunks(items,action){const out=[];for(let n=0;n<items.length;n+=20)out.push(...await Promise.all(items.slice(n,n+20).map(action)));return out;}
export async function handleArticleMarks(request,store){
 const origin=request.headers.get('Origin');
 if(!allowedAccountOrigin(origin))return json({error:'來源格式不正確。'},403);
 let response;
 if(request.method==='OPTIONS')response=new Response(null,{status:204});
 else response=await handleRequest(request,store);
 response.headers.set('Cache-Control','no-store');
 return accountCORS(response,origin);
}
async function handleRequest(request,store){
 if(request.method==='GET'){
  const [{blobs:old},{blobs:current}]=await Promise.all([store.list({prefix:'v1/'}),store.list({prefix:'v2/'})]);
  await chunks(old.filter(b=>/^v1\/(favorite|answered)\/q-\d{3,6}$/.test(b.key)),b=>store.delete(b.key));
  const marks=(await chunks([...old,...current].filter(b=>/^v1\/doubt\/q-\d{3,6}$/.test(b.key)||/^v2\/flag\/q-\d{3,6}$/.test(b.key)),async({key})=>{
   const value=await store.get(key,{type:'json',consistency:'strong'}),[,kind,id]=key.split('/');
   try{return checkedFlagOperations([{kind,id,...(kind==='flag'?{value:value?.value}:{on:value?.on})}])[0];}catch{return null;}
  })).filter(Boolean);
  for(const {key} of current){const match=key.match(/^v2\/practice\/([0-9a-f-]{36})\/(\d{4}-\d{2}-\d{2})\/(q-\d{3,6})\/(plus|minus)$/i);if(match){try{marks.push(...checkedFlagOperations([{kind:'practice',eventId:match[1],day:match[2],id:match[3],delta:match[4]==='plus'?1:-1}]));}catch{}}}
  marks.sort((a,b)=>flagOperationKey(a).localeCompare(flagOperationKey(b)));
  const payload={schemaVersion:2,kinds:['flag','doubt','practice'],defaultFlag:3,marks};
  const etag='"'+createHash('sha256').update(JSON.stringify(payload)).digest('hex')+'"';
  if(request.headers.get('If-None-Match')===etag)return new Response(null,{status:304,headers:{ETag:etag}});
  return json(payload,200,{ETag:etag});
 }
 if(request.method!=='POST')return json({error:'只接受GET或POST。'},405,{Allow:'GET, POST'});
 if(!request.headers.get('Content-Type')?.startsWith('application/json'))return json({error:'請使用JSON格式。'},415);
 let operations;
 try{
  const text=await request.text();if(text.length>16384)return json({error:'單次標記資料過大。'},413);
  const body=JSON.parse(text);if(body.schemaVersion!==2)return json({error:'請重新整理，使用新的FLAG標記。'},409);
  operations=checkedFlagOperations(body.operations,100);if(!operations.length)throw Error();
 }catch{return json({error:'標記資料格式不正確。'},400);}
 const unique=[...new Map(operations.map(op=>[flagOperationKey(op),op])).values()];
 for(const op of unique){
  const key=op.kind==='doubt'?'v1/doubt/'+op.id:op.kind==='practice'?'v2/'+flagOperationKey(op)+'/'+op.day+'/'+op.id+'/'+(op.delta===1?'plus':'minus'):'v2/'+flagOperationKey(op);
  await store.setJSON(key,op.kind==='flag'?{value:op.value}:op.kind==='doubt'?{on:op.on}:{recorded:true});
 }
 return json({schemaVersion:2,applied:unique});
}
