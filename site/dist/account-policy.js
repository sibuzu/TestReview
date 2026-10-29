export const ACCOUNT_API_ORIGIN='https://weirugo.sibuzu.com';
export function accountEndpoint(name,href=globalThis.location?.href){
 const path='/.netlify/functions/'+name;
 try{if(new URL(href).origin===ACCOUNT_API_ORIGIN)return path;}catch{}
 return ACCOUNT_API_ORIGIN+path;
}
export function allowedAccountOrigin(origin){
 if(!origin)return true;
 try{const url=new URL(origin);return ['https:','http:'].includes(url.protocol)&&url.origin===origin;}catch{return false;}
}
export function accountCORS(response,origin){
 response.headers.set('Cache-Control','no-store');
 if(origin&&allowedAccountOrigin(origin))for(const [key,value] of Object.entries({'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Methods':'GET, POST, DELETE, OPTIONS','Access-Control-Allow-Headers':'Content-Type, Authorization, If-None-Match','Access-Control-Expose-Headers':'ETag','Vary':'Origin'}))response.headers.set(key,value);
 return response;
}
