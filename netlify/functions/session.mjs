import {getStore} from '@netlify/blobs';
import {handleSession} from '../lib/sessions.mjs';
import {accountCORS} from '../../site/dist/account-policy.js';
export default async request=>{
 try{return await handleSession(request,getStore({name:'testreview-shared-marks',consistency:'strong'}));}
 catch{return accountCORS(new Response(JSON.stringify({error:'暫時無法Sign In，請稍後重試。'}),{status:503,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'}}),request.headers.get('Origin'));}
};
