// Use the site's direct Netlify API so Cloudflare does not block cross-origin preflight.
export const ACCOUNT_API_ORIGIN='https://mytestreview.netlify.app';
export function accountEndpoint(name){return ACCOUNT_API_ORIGIN+'/.netlify/functions/'+name;}
export function allowedAccountOrigin(origin){
 if(!origin)return true;
 try{const url=new URL(origin);return ['https:','http:'].includes(url.protocol)&&url.origin===origin;}catch{return false;}
}
export function accountCORS(response,origin){
 response.headers.set('Cache-Control','no-store');
 if(origin&&allowedAccountOrigin(origin))for(const [key,value] of Object.entries({'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Methods':'GET, POST, DELETE, OPTIONS','Access-Control-Allow-Headers':'Content-Type, Authorization, If-None-Match','Access-Control-Expose-Headers':'ETag','Vary':'Origin'}))response.headers.set(key,value);
 return response;
}
