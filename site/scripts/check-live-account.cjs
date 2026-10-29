// Real cross-origin transport smoke check, using Demo only and changing no question marks.
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
(async()=>{
 const entry=process.argv[2]||'http://127.0.0.1:8765/site/index.html';
 const browser=await chromium.launch(),context=await browser.newContext(),page=await context.newPage(),responses=[];
 page.on('response',response=>{if(response.url().includes('/.netlify/functions/'))responses.push({path:new URL(response.url()).pathname,method:response.request().method(),status:response.status(),origin:new URL(response.url()).origin});});
 try{
  await page.goto(entry);await page.locator('#signin-user').fill('demo');await page.locator('#signin-password').fill('1234');await page.locator('#signin-submit').click();
  await page.waitForSelector('#app-shell:not([hidden])',{timeout:30000});await page.waitForFunction(()=>document.querySelector('#sync-status').dataset.state==='synced',{timeout:30000});
  assert.equal(await page.locator('#account-name').textContent(),'demo');assert.ok(await page.locator('[data-open]').count()>0);
  await page.locator('#sign-out').click();await page.waitForSelector('#signin-user:enabled');assert.equal(await page.evaluate(()=>localStorage.getItem('weirugo:session:v1')),null);
  const out={checkedAt:new Date().toISOString(),entry,account:'demo',result:'PASS',responses,scope:'actual cross-origin Sign In, authenticated mark read, sync and Sign Out; no question marks changed'};
  fs.writeFileSync(path.resolve(__dirname,'../../docs/imports/live-account-smoke-'+new URL(entry).hostname+'-2026-10-29.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out));
 }finally{
  try{await page.evaluate(async()=>{const s=JSON.parse(localStorage.getItem('weirugo:session:v1')||'null');if(s?.user==='demo'){await fetch('https://mytestreview.netlify.app/.netlify/functions/session',{method:'DELETE',headers:{Authorization:'Bearer '+s.token}});localStorage.removeItem('weirugo:session:v1');}});}catch{}
  await context.close();await browser.close();
 }
})().catch(error=>{console.error(error);process.exitCode=1;});
