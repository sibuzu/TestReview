import {handleArticleMarks} from './article-marks.mjs';
import {sessionUser,accountStore} from './sessions.mjs';
import {allowedAccountOrigin,accountCORS} from '../../site/dist/account-policy.js';
export async function handleAccountMarks(request,store){
 const origin=request.headers.get('Origin');
 if(!allowedAccountOrigin(origin))return new Response(JSON.stringify({error:'來源格式不正確。'}),{status:403});
 if(request.method==='OPTIONS')return handleArticleMarks(request,store);
 const user=await sessionUser(request,store);
 if(!user)return accountCORS(new Response(JSON.stringify({error:'請先Sign In。'}),{status:401,headers:{'Content-Type':'application/json'}}),origin);
 return handleArticleMarks(request,accountStore(store,user));
}
