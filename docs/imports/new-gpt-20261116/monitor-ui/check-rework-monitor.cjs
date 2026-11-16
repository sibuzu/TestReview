const fs=require('node:fs'),assert=require('node:assert/strict');
const {chromium}=require('../../../../.cache/qa-tools/node_modules/playwright');
(async()=>{const browser=await chromium.launch({headless:true});try{const results=[];
for(const width of [1440,390]){const page=await browser.newPage({viewport:{width,height:1000}}),errors=[],remote=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():(remote.push(route.request().url()),route.abort()));
await page.goto('http://127.0.0.1:8912/');const section=page.locator('#illustration-rework');await section.waitFor({state:'visible'});
const stats=await page.evaluate(()=>{const s=document.getElementById('illustration-rework');return {text:s.innerText,overflow:document.documentElement.scrollWidth>innerWidth,rows:[...document.querySelectorAll('#illustration-rework-subjects tr')].map(r=>[...r.children].map(c=>c.textContent)),resume:document.getElementById('illustration-rework-resume').textContent};});
assert.equal(stats.overflow,false);assert.match(stats.text,/目前暫停/);assert.match(stats.text,/已驗收 65 原問/);assert.match(stats.text,/待重製 75 原問/);assert.deepEqual(stats.rows.find(r=>r[0]==='生物'),['生物','17','29','0']);assert.match(stats.resume,/將生物的舊解說圖改為精美解說圖/);assert.match(stats.resume,/繼續非生物圖解重製/);assert.match(stats.resume,/q-081/);
const screenshot=`.cache/intake-20261116/rework-monitor-${width}.png`;await section.screenshot({path:screenshot});
await page.locator('#illustration-rework-reassess > summary').click();assert.equal(await page.locator('#illustration-rework-reassess a').getAttribute('href'),'http://127.0.0.1:8912/site/index.html#question/q-080');assert.match(await page.locator('#illustration-rework-reassess').innerText(),/伊拉克戰亂/);
await page.locator('#illustration-rework-pending-title').click();assert.equal(await page.locator('#illustration-rework-pending article').count(),75);
await page.locator('#refresh').click();await page.waitForTimeout(250);await page.evaluate(()=>render(data));assert.equal(await page.locator('#illustration-rework-reassess').getAttribute('open'),'');
assert.deepEqual(errors,[]);assert.deepEqual(remote,[]);results.push({viewport:width,...stats,screenshot,pageErrors:errors,remoteCalls:remote.length});await page.close();}
fs.writeFileSync('.cache/intake-20261116/rework-monitor-validation.json',JSON.stringify({passed:true,results},null,2)+'\n');console.log('PASS 1440/390 real monitor, counts, grouped links, commands, refresh, no remote writes');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
