const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'../..'),site=path.join(root,'site/dist'),out=path.join(root,'.cache/score-ui');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const {handleSession}=await import(pathToFileURL(path.join(root,'netlify/lib/sessions.mjs')));
 const {handleAccountMarks}=await import(pathToFileURL(path.join(root,'netlify/lib/account-marks.mjs')));
 const {practiceDay}=await import(pathToFileURL(path.join(site,'article-flags.js')));
 const dataset=JSON.parse(fs.readFileSync(path.join(site,'data.json'))),ids=['q-271','q-298','q-296','q-304','q-501','q-835','q-820'];
 dataset.questions=dataset.questions.filter(q=>ids.includes(q.id));assert.equal(dataset.questions.length,ids.length);
 const browser=await chromium.launch(),results=[];
 try{for(const width of [1440,390,360]){
  const values=new Map(),db={list:async({prefix=''})=>({blobs:[...values.keys()].filter(k=>k.startsWith(prefix)).map(key=>({key}))}),get:async key=>structuredClone(values.get(key)??null),setJSON:async(key,value)=>values.set(key,structuredClone(value)),delete:async key=>values.delete(key)};
  values.set('v1/favorite/q-271',{on:true,color:'red'});values.set('v1/answered/q-298',{on:true});
  const context=await browser.newContext({viewport:{width,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await context.route('**/*',async route=>{
   const req=route.request(),url=new URL(req.url());
   if(url.pathname.startsWith('/.netlify/functions/')){
    const options={method:req.method(),headers:await req.allHeaders()};if(!['GET','HEAD'].includes(req.method()))options.body=req.postData();
    const response=await(url.pathname.endsWith('/session')?handleSession:handleAccountMarks)(new Request(req.url(),options),db);
    await route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});return;
   }
   if(!['127.0.0.1','test.sibuzu.com'].includes(url.hostname)){await route.abort();return;}
   if(url.pathname.endsWith('/data.json')){await route.fulfill({json:dataset});return;}
   const relative=url.pathname.replace(/^\/site\//,'/').replace(/^\//,'')||'index.html',file=path.resolve(site,relative);
   if(!file.startsWith(site+path.sep)||!fs.existsSync(file)){await route.fulfill({status:404,body:'Not found'});return;}
   const types={'.js':'text/javascript','.html':'text/html','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp'};
   await route.fulfill({path:file,contentType:types[path.extname(file)]||'application/octet-stream'});
  });
  const base=width===390?'https://test.sibuzu.com/':'http://127.0.0.1:8912/site/';
  await page.goto(base+'index.html');await page.waitForSelector('#signin-screen:not([hidden])');
  assert.equal(await page.locator('#app-shell').getAttribute('hidden'),'');
  await page.screenshot({path:path.join(out,`signin-${width}.png`)});
  async function login(user,password='1234'){
   await page.locator('#signin-user').fill(user);await page.locator('#signin-password').fill(password);await page.locator('#signin-submit').click();
   await page.waitForSelector('#app-shell:not([hidden])');await page.waitForFunction(()=>document.querySelectorAll('[data-open]').length>0);
   await page.waitForFunction(()=>document.querySelector('#sync-status').dataset.state==='synced');
  }
  await page.locator('#signin-user').fill('weiru');await page.locator('#signin-password').fill('wrong');await page.locator('#signin-submit').click();await page.waitForFunction(()=>document.querySelector('#signin-error').textContent.includes('不正確'));
  await login('weiru');
  assert.equal(await page.locator('[data-open]').count(),ids.length);assert.equal(await page.locator('#search,#sort,#volume-filter,#chapter-filter,[data-answered-scope],[data-nav="star"],#favorite-palette').count(),0);
  assert.deepEqual(await page.locator('[data-flag-filter]:checked').evaluateAll(nodes=>nodes.map(n=>Number(n.dataset.flagFilter))),[3,4,5]);
  assert.equal(await page.locator('[data-flag-count="3"]').textContent(),String(ids.length));assert.equal(values.has('v1/favorite/q-271'),false);assert.equal(values.has('v1/answered/q-298'),false);
  await page.locator('[data-nav="all"] .nav-symbol').click();assert.equal(await page.locator('#page-title').textContent(),'全部錯題');
  const dates=await page.locator('.card-date').allTextContents();assert.deepEqual(dates,[...dates].sort().reverse());
  assert.equal(await page.locator('#grid-view,#list-view,.view-switch').count(),0,'fixed list view');
  const questionIds=()=>page.locator('[data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open));
  const byDate=await questionIds();
  await page.locator('#shuffle-order').click();
  assert.equal(await page.locator('#shuffle-order').getAttribute('aria-pressed'),'true');
  const shuffled=await questionIds();assert.deepEqual([...shuffled].sort(),[...byDate].sort());
  await page.locator('[data-flag-filter="5"]').uncheck();await page.locator('[data-flag-filter="5"]').check();
  assert.deepEqual(await questionIds(),shuffled,'filter redraw does not reshuffle');
  const first=shuffled[0],currentSubject=dataset.questions.find(q=>q.id===first).subject;
  await page.locator('[data-open="'+first+'"]').click();
  assert.deepEqual(await page.locator('[data-question-nav]').evaluateAll(nodes=>nodes.map(n=>n.dataset.questionNav)),shuffled.filter(id=>dataset.questions.find(q=>q.id===id).subject===currentSubject),'sidebar follows the shuffled list');
  await page.goBack();await page.waitForSelector('#list-page:not([hidden])');
  assert.deepEqual(await questionIds(),shuffled,'return from question preserves shuffle');
  await page.locator('#date-order').click();assert.equal(await page.locator('#date-order').getAttribute('aria-pressed'),'true');
  assert.deepEqual(await questionIds(),byDate,'calendar restores newest first');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'sort toolbar fits');
  await page.screenshot({path:path.join(out,`list-${width}.png`),fullPage:true});
  await page.locator('[data-open="q-271"]').click();await page.locator('#answer-toggle').click();await page.waitForSelector('#answer-panel:not([hidden])');
  assert.equal(await page.getByText('開啟本題單頁閱讀版').count(),0);
  assert.equal(await page.locator('[data-flag-position="footer"] [data-article-flag]').count(),5);
  await page.evaluate(()=>window.__answerPanel=document.querySelector('#answer-panel'));
  await page.locator('[data-flag-position="footer"] [data-article-flag="5"]').click();
  assert.equal(await page.locator('[data-flag-position="header"] [data-article-flag="5"]').getAttribute('aria-checked'),'true');
  await page.locator('[data-flag-position="footer"] [data-article-flag="3"]').click();
  await page.evaluate(()=>document.querySelector('#answer-toggle').focus({preventScroll:true}));
  await page.keyboard.press('2');assert.equal(await page.locator('[data-article-flag="2"]').first().getAttribute('aria-checked'),'true');assert.equal(await page.locator('#answer-panel').getAttribute('hidden'),null);assert.equal(await page.evaluate(()=>window.__answerPanel===document.querySelector('#answer-panel')),true);
  assert.equal(await page.locator('[data-article-flag][aria-checked="true"]').count(),2);
  await page.keyboard.press('3');await page.keyboard.press('5');await page.keyboard.press('1');await page.keyboard.press('3');
  assert.equal(await page.locator('[data-article-flag="3"]').first().getAttribute('aria-checked'),'true');
  await page.evaluate(()=>{const input=document.createElement('textarea');input.id='test-input';document.body.append(input);input.focus();});await page.keyboard.press('2');assert.equal(await page.locator('[data-article-flag="3"]').first().getAttribute('aria-checked'),'true');await page.locator('#test-input').evaluate(el=>el.remove());
  for(const options of [{key:'2',repeat:true},{key:'2',isComposing:true},{key:'2',ctrlKey:true}])await page.locator('#detail').dispatchEvent('keydown',options);
  assert.equal(await page.locator('[data-article-flag="3"]').first().getAttribute('aria-checked'),'true');
  await page.locator('[data-nav="progress"]').click();assert.equal(await page.locator('.practice-table tbody td').first().textContent(),'0');
  // Simulate an actual previously completed question, then undo it today.
  const token=await page.evaluate(()=>JSON.parse(localStorage.getItem('weirugo:session:v1')).token),yesterday=new Date(Date.now()-86400000),oldDay=practiceDay(yesterday);
  const response=await handleAccountMarks(new Request('https://weirugo.sibuzu.com/.netlify/functions/marks',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({schemaVersion:2,operations:[{kind:'flag',id:'q-298',value:2},{kind:'practice',id:'q-298',day:oldDay,eventId:'00000000-0000-4000-8000-000000000099',delta:1}]})}),db);assert.equal(response.status,200);
  await page.locator('#sync-status').click();await page.waitForFunction(()=>document.querySelector('#sync-status').dataset.state==='synced');
  await page.locator('[data-nav="all"]').click();await page.locator('[data-flag-filter="2"]').check();await page.locator('[data-open="q-298"] .flag-indicator').click();
  assert.equal(await page.locator('[data-article-flag="2"]').first().getAttribute('aria-checked'),'true');await page.keyboard.press('3');await page.locator('[data-nav="progress"]').click();assert.equal(await page.locator('.practice-table tbody td').first().textContent(),'-1');
  await page.screenshot({path:path.join(out,`progress-${width}.png`),fullPage:true});
  await page.locator('[data-nav="all"]').click();await page.locator('[data-open="q-271"]').click();await page.keyboard.press('5');await page.waitForFunction(()=>document.querySelector('#sync-status').dataset.state==='synced');
  await page.reload();await page.waitForSelector('[data-article-flag="5"][aria-checked="true"]');assert.equal(await page.locator('#account-name').textContent(),'weiru');
  await page.locator('#sign-out').click();await page.waitForSelector('#signin-screen:not([hidden])');assert.equal(await page.evaluate(()=>localStorage.getItem('weirugo:session:v1')),null);
  await login('demo');assert.equal(await page.locator('[data-flag-count="3"]').textContent(),String(ids.length));await page.locator('[data-nav="progress"]').click();assert.equal(await page.locator('.empty-progress').count(),1);
  await page.locator('[data-nav="all"]').click();await page.locator('[data-open="q-271"]').click();await page.keyboard.press('1');await page.locator('[data-doubt]').click();await page.waitForFunction(()=>document.querySelector('#sync-status').dataset.state==='synced');
  await page.locator('#sign-out').click();await page.waitForSelector('#signin-screen:not([hidden])');await login('weiru');await page.locator('[data-open="q-271"]').click();
  assert.equal(await page.locator('[data-article-flag="5"]').first().getAttribute('aria-checked'),'true');assert.equal(await page.locator('[data-doubt]').getAttribute('aria-pressed'),'true');
  const shape=await page.locator('.flag-options').first().evaluate(el=>[...el.children].map(n=>{const r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};}));assert.ok(shape.every(n=>n.y===shape[0].y),'five icons in one row');
  if(width<=760){const title=await page.locator('#detail h1').boundingBox(),actions=await page.locator('.detail-actions').boundingBox();assert.ok(title.y>=actions.y+actions.height,'mobile title clears the five FLAG controls');}
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);assert.equal(overflow,false);assert.deepEqual(errors,[]);
  await page.screenshot({path:path.join(out,`detail-${width}.png`),fullPage:true});results.push({width,passed:true,fixedListVerified:true,shuffleAndReturnVerified:true,negativeProgressVerified:true,accountIsolationVerified:true,sharedDoubtsVerified:true,overflow,shape});await context.close();
 }
 fs.writeFileSync(path.join(root,'docs/imports/flag-account-ui-validation-2026-10-29.json'),JSON.stringify({checkedAt:new Date().toISOString(),mode:'isolated static fixtures with mocked cloud/session handlers; no real cloud calls',results,screenshots:out},null,2)+'\n');console.log('PASS',results.length,'viewport flows');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
