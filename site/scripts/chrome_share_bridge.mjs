// Reuse an authorized live instance when one exists; stdin accepts prefetch JSONL.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';
import {createRequire} from 'node:module';
// Reuse the same WebSocket implementation as the local browser QA tools. A
// Chrome Allow prompt can outlast the native client's HTTP handshake timeout.
const {ws: ApprovalWebSocket}=createRequire(import.meta.url)('/home/jack/ai/Chemery/node_modules/playwright-core/lib/utilsBundle.js');
let endpoint=process.env.CHROME_DEVTOOLS_WS_URL;
if(!endpoint){
  const [port,route]=fs.readFileSync(path.join(os.homedir(),'.config/google-chrome/DevToolsActivePort'),'utf8').trim().split('\n');
  endpoint=`ws://127.0.0.1:${port}${route}`;
}
// A WSL process can use an explicit loopback relay to the authorized Windows
// Chrome, whose localhost and DevToolsActivePort differ from the Linux profile.
const endpointUrl=new URL(endpoint);
if(endpointUrl.protocol!=='ws:'||!['127.0.0.1','localhost','[::1]'].includes(endpointUrl.hostname))throw Error('Chrome bridge requires a loopback WebSocket endpoint');
const socket=new ApprovalWebSocket(endpointUrl.href,{handshakeTimeout:15*60*1000});
let seq=0;const pending=new Map();
function send(method,params={},sessionId){return new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})}));setTimeout(()=>{if(pending.has(id)){pending.delete(id);reject(Error('CDP request timed out'));}},45000).unref();});}
socket.addEventListener('message',event=>{const m=JSON.parse(event.data);if(!m.id)return;const p=pending.get(m.id);if(!p)return;pending.delete(m.id);if(m.error)p.reject(Error(m.error.message));else p.resolve(m.result);});
socket.addEventListener('error',()=>console.error('Chrome connection failed'));
console.log('Waiting for the Chrome connection approval...');
await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
console.log('Chrome connected. Ready for JSON commands.');
const shares=async()=>{const {targetInfos}=await send('Target.getTargets');return targetInfos.filter(t=>t.type==='page'&&t.url.startsWith('https://chatgpt.com/share/')).map(t=>({id:t.targetId,title:t.title,url:t.url}));};
console.log(JSON.stringify({shares:await shares()}));
const sessions=new Map();async function session(targetId){if(!sessions.has(targetId))sessions.set(targetId,(await send('Target.attachToTarget',{targetId,flatten:true})).sessionId);return sessions.get(targetId);}
const lines=readline.createInterface({input:process.stdin,terminal:false});
for await(const line of lines){if(!line.trim())continue;try{const command=JSON.parse(line);let result;if(command.action==='list')result=await shares();else if(command.action==='new'){const u=new URL(command.url);if(u.origin!=='https://chatgpt.com'||!u.pathname.startsWith('/share/'))throw Error('Only explicit ChatGPT share pages are supported');result=await send('Target.createTarget',{url:u.href});}else if(command.action==='evaluate'){const s=await session(command.targetId);const r=await send('Runtime.evaluate',{expression:command.expression,returnByValue:true,awaitPromise:true,userGesture:true},s);if(r.exceptionDetails)throw Error(r.exceptionDetails.text);result=r.result.value;}else if(command.action==='save'){const s=await session(command.targetId);const r=await send('Runtime.evaluate',{expression:command.expression,returnByValue:true,awaitPromise:true,userGesture:true},s);if(r.exceptionDetails)throw Error(r.exceptionDetails.text);const value=r.result.value;if(!value?.base64)throw Error(JSON.stringify(value));fs.writeFileSync(command.path,Buffer.from(value.base64,'base64'));result={saved:command.path,bytes:fs.statSync(command.path).size,mime:value.mime,width:value.width,height:value.height};}else if(command.action==='close'){socket.close();break;}else throw Error('Unknown command');console.log(JSON.stringify({ok:true,result}));}catch(error){console.log(JSON.stringify({ok:false,error:error.message}));}}
