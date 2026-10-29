const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url'),{createGroupShadow}=require('./group-shadow.cjs');
const root=path.resolve(__dirname,'../..'),out=path.join(root,'.cache/group-mark-ui');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const {handleSession}=await import(pathToFileURL(path.join(root,'netlify/lib/sessions.mjs')));
 const {handleAccountMarks}=await import(pathToFileURL(path.join(root,'netlify/lib/account-marks.mjs')));
 const manifest='docs/imports/group-review/drafts/group-q-029-q-031/manifest.json',shadow=createGroupShadow([manifest]);shadow.data.questions=shadow.groups.map(g=>g.question);
 const browser=await chromium.launch(),results=[];
 try{for(const width of [1440,390]){
  const values=new Map(),db={list:async({prefix=''})=>({blobs:[...values.keys()].filter(k=>k.startsWith(prefix)).map(key=>({key}))}),get:async key=>structuredClone(values.get(key)??null),setJSON:async(key,value)=>values.set(key,structuredClone(value)),delete:async key=>values.delete(key)};
  const context=await browser.newContext({viewport:{width,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));await shadow.install(page);
  await page.route('**/.netlify/functions/**',async route=>{const req=route.request(),opts={method:req.method(),headers:await req.allHeaders()};if(!['GET','HEAD'].includes(req.method()))opts.body=req.postData();const response=await(req.url().endsWith('/session')?handleSession:handleAccountMarks)(new Request(req.url(),opts),db);await route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});});
  const base='http://127.0.0.1:8765/site/index.html';await page.goto(base);
  async function synced(){await page.waitForFunction(()=>document.querySelector('#sync-status').dataset.state==='synced');}
  async function login(user){await page.locator('#signin-user').fill(user);await page.locator('#signin-password').fill('1234');await page.locator('#signin-submit').click();await page.waitForSelector('#app-shell:not([hidden])');await synced();}
  async function open(){await page.evaluate(()=>{location.hash='question/q-031';});await page.waitForSelector('[data-flag-position="header"]');}
  async function token(){return page.evaluate(()=>JSON.parse(localStorage.getItem('weirugo:session:v1')).token);}
  async function api(operations){const opts={headers:{Authorization:'Bearer '+await token()}};if(operations){opts.method='POST';opts.headers['Content-Type']='application/json';opts.body=JSON.stringify({schemaVersion:2,operations});}const r=await handleAccountMarks(new Request('https://mytestreview.netlify.app/.netlify/functions/marks',opts),db);assert.equal(r.status,200);return r.json();}
  async function flag(value){await page.locator('[data-flag-position="header"] [data-article-flag="'+value+'"]').click();await synced();assert.equal(await page.locator('[data-flag-position="footer"] [data-article-flag="'+value+'"]').getAttribute('aria-checked'),'true');}
  await login('demo');await api([{kind:'flag',id:'q-029',value:2},{kind:'flag',id:'q-031',value:5},{kind:'doubt',id:'q-031',on:true}]);await page.locator('#sync-status').click();await synced();await open();
  assert.equal(await page.locator('[data-flag-position="header"] [data-article-flag="3"]').getAttribute('aria-checked'),'true','new group defaults to general, ignoring old child flags');
  let remote=await api();assert.equal(remote.marks.filter(m=>m.kind==='practice').length,0,'no synthetic migration practice');
  await flag(3);remote=await api();assert.equal(remote.marks.filter(m=>m.kind==='groupFlag').length,1,'same effective value creates explicit group choice');assert.equal(remote.marks.filter(m=>m.kind==='practice').length,0);
  await flag(2);remote=await api();const initialEvents=remote.marks.filter(m=>m.kind==='practice'),initialNet=initialEvents.reduce((n,e)=>n+e.delta,0);assert.deepEqual(remote.marks.filter(m=>m.kind==='flag').map(m=>[m.id,m.value]),[['q-029',2],['q-031',5]],'original child states unchanged');
  await page.reload();await page.waitForSelector('[data-flag-position="header"] [data-article-flag="2"][aria-checked="true"]');await synced();
  await flag(3);await flag(2);remote=await api();const events=remote.marks.filter(m=>m.kind==='practice');assert.equal(events.length,initialEvents.length+2);assert.equal(events.reduce((n,e)=>n+e.delta,0),initialNet);assert.equal(new Set(events.map(e=>e.eventId)).size,events.length);
  assert.equal(await page.locator('[data-doubt]').getAttribute('aria-pressed'),'true');await page.locator('[data-doubt]').click();await synced();remote=await api();assert.ok(remote.marks.filter(m=>m.kind==='doubt').every(m=>m.on===false),'group cancellation clears all member doubts');
  await page.reload();await page.waitForSelector('[data-flag-position="header"] [data-article-flag="2"][aria-checked="true"]');await synced();assert.equal(await page.locator('[data-doubt]').getAttribute('aria-pressed'),'false');
  await page.locator('#sign-out').click();await page.waitForSelector('#signin-screen:not([hidden])');await login('weiru');await open();assert.equal(await page.locator('[data-flag-position="header"] [data-article-flag="3"]').getAttribute('aria-checked'),'true','other account independent');await flag(4);
  await page.locator('#sign-out').click();await page.waitForSelector('#signin-screen:not([hidden])');await login('demo');await open();assert.equal(await page.locator('[data-flag-position="header"] [data-article-flag="2"]').getAttribute('aria-checked'),'true');
  assert.equal(await page.locator('[data-group-question]').count(),2);assert.equal(await page.locator('.native-comic:visible').count(),0);await page.locator('#answer-toggle').click();assert.equal(await page.locator('.native-comic:visible').count(),2);await page.locator('img').evaluateAll(nodes=>Promise.all(nodes.map(i=>{i.loading='eager';return i.decode();})));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.deepEqual(errors,[]);await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(out,'group-'+width+'.png')});
  results.push({width,passed:true,newGroupsStartGeneral:true,rawChildrenPreserved:true,explicitOverrideReload:true,noSyntheticPractice:true,signedEvents:true,doubtCancellation:true,accountIsolation:true,oldChildURL:true});await context.close();
 }
 fs.writeFileSync(path.join(root,'docs/imports/group-review/group-mark-ui-validation.json'),JSON.stringify({checkedAt:new Date().toISOString(),mode:'shadow data and in-memory session/cloud handlers; no real cloud requests',results},null,2)+'\n');console.log('PASS',results);
 }finally{await browser.close();fs.rmSync(shadow.temporary,{recursive:true,force:true});}
})().catch(e=>{console.error(e);process.exitCode=1;});
