// Reading-list navigation QA uses isolated Demo storage and never writes real cloud marks.
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {installTestSession}=require('./test-session.cjs');
const root=path.resolve(__dirname,'../..'),out=path.join(root,'.cache/reading-navigation');fs.mkdirSync(out,{recursive:true});
const subjects=[{id:'Chinese',name:'國文',icon:'文'},{id:'English',name:'英文',icon:'Aa'},{id:'Math',name:'數學',icon:'π'}];
const questions=[['q-900004','Chinese','2026-10-26'],['q-900001','English','2026-10-29'],['q-900003','Math','2026-10-27'],['q-900002','Chinese','2026-10-28']].map(([id,subject,date])=>({id,subject,date,title:id,question:'請閱讀完整題目後選擇答案。',answer:'答案 A',explanation:'此處為隔離導覽檢查資料。',sourceId:'nav-source',volume:'綜合',chapter:'綜合',tags:[],images:[],contentStatus:'完整原題',verification:'原題已核對'}));
const fixture={schemaVersion:1,revision:'reading-navigation-qa',dataUpdatedAt:'2026-10-29T00:00:00Z',subjects,sources:[],questions};
(async()=>{
 const browser=await chromium.launch(),results=[];
 try{for(const width of [1440,390,320]){
  const context=await browser.newContext({viewport:{width,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));await installTestSession(page);await page.addInitScript(()=>Math.random=()=>0);
  await page.route('**/.netlify/functions/marks',route=>route.abort());
  await page.route('**/data.json',route=>route.fulfill({json:fixture}));
  const listIds=()=>page.locator('#results [data-open]').evaluateAll(xs=>xs.map(x=>x.dataset.open));
  const navIds=()=>page.locator('#subjects [data-question-nav]').evaluateAll(xs=>xs.map(x=>x.dataset.questionNav));
  const next=()=>page.locator('.question-footer-flags [data-next-question]');
  const current=()=>page.locator('#subjects [aria-current="page"]').getAttribute('data-question-nav');
  await page.goto('http://127.0.0.1:8765/site/index.html#questions');await page.waitForSelector('#results [data-open]');
  const dateIds=await listIds();assert.deepEqual(dateIds,['q-900001','q-900002','q-900003','q-900004']);
  await page.locator('#results [data-open]').first().click();assert.deepEqual(await navIds(),dateIds);
  assert.match(await page.locator('#subject-heading').innerText(),/全部錯題\s+4/);
  assert.equal(await next().getAttribute('title'),'下一題');assert.equal(await next().locator('circle').count(),1);
  await next().click();assert.equal(await current(),dateIds[1]);
  await page.locator('[data-flag-position="footer"] [data-article-flag="2"]').click();assert.equal(await page.locator('[data-flag-position="footer"] [data-article-flag="2"]').getAttribute('aria-checked'),'true');
  assert.deepEqual(await navIds(),dateIds,'a FLAG change preserves the reading sequence until leaving');
  await next().click();assert.equal(await current(),dateIds[2],'next survives the current question leaving the FLAG filter');
  await page.goBack();await page.waitForFunction(()=>document.querySelector('#subjects [aria-current="page"]')?.dataset.questionNav==='q-900002');assert.deepEqual(await navIds(),dateIds);
  await page.locator('#subjects [data-question-nav="'+dateIds.at(-1)+'"]').click();assert.equal(await next().getAttribute('aria-disabled'),'true');
  assert.equal(await next().getAttribute('title'),'已是清單最後一題');
  await page.locator('[data-question-return]').click();await page.waitForSelector('#list-page:not([hidden])');
  assert.deepEqual(await listIds(),dateIds.filter(id=>id!=='q-900002'),'returning to the list reapplies current FLAG values');
  await page.locator('#flag-filter-2').check();await page.locator('#shuffle-order').click();
  const shuffled=await listIds();assert.notDeepEqual(shuffled,dateIds);
  await page.locator('#results [data-open]').first().click();assert.deepEqual(await navIds(),shuffled);
  await next().click();assert.equal(await current(),shuffled[1]);assert.deepEqual(await navIds(),shuffled);
  await page.locator('[data-question-return]').click();await page.waitForSelector('#list-page:not([hidden])');assert.deepEqual(await listIds(),shuffled);
  await page.locator('[data-subject="Chinese"]').click();await page.waitForSelector('#results [data-open]');const chinese=await listIds();
  await page.locator('#results [data-open]').first().click();assert.deepEqual(await navIds(),chinese);assert.match(await page.locator('#subject-heading').innerText(),/國文\s+2/);
  await page.reload();await page.waitForSelector('[data-flag-position="footer"]');assert.deepEqual(await navIds(),chinese,'reload preserves the entered list and its shuffle');
  await page.goto('http://127.0.0.1:8765/site/index.html#question/q-900001');await page.waitForSelector('[data-flag-position="footer"]');
  assert.deepEqual(await navIds(),['q-900001'],'a direct question URL keeps the subject fallback');
  await page.screenshot({path:path.join(out,'direct-'+width+'.png'),fullPage:true});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.locator('[data-nav="all"]').click();await page.waitForSelector('#results [data-open]');await page.locator('#results [data-open]').first().click();
  await page.screenshot({path:path.join(out,'all-'+width+'.png'),fullPage:true});
  const gap=await page.locator('.question-footer-flags .flag-and-next').evaluate(el=>parseFloat(getComputedStyle(el).gap));assert.equal(gap,18);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.deepEqual(errors,[]);
  results.push({width,passed:true,allSubjects:true,dateAndShufflePreserved:true,flagChangeNext:true,subjectScope:true,reloadAndBack:true,lastQuestion:true,iconAndHint:true,gap});await context.close();
 }
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({checkedAt:new Date().toISOString(),mode:'isolated local fixture; fake Demo session and real marks requests aborted',results},null,2)+'\n');console.log('PASS',JSON.stringify(results));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
