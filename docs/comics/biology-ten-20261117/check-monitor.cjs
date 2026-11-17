const {chromium}=require('../../../.cache/qa-tools/node_modules/playwright');
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const dir=__dirname,root=path.resolve(dir,'../../..');
(async()=>{
 const browser=await chromium.launch();
 try{
  const page=await browser.newPage(),errors=[],rows=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/.netlify/functions/**',r=>r.abort());
  for(const width of [1440,390]){
   await page.setViewportSize({width,height:1000});
   await page.goto('http://127.0.0.1:8912/');
   const card=page.locator('#illustration-rework');
   await card.waitFor({state:'visible'});
   const status=await page.evaluate(async()=>await (await fetch('/api/status')).json());
   const rework=status.illustrationRework;
   assert.equal(rework.total,140);
   assert.equal(rework.activeBatch.limit,10);
   const batch=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json')));
   assert.equal(rework.activeBatch.completed,batch.completedQuestionIds.length);
   assert.equal(rework.activeBatch.state,batch.state);
   const counts=await page.locator('#illustration-rework-counts').textContent();
   assert.ok(counts.includes('已驗收 '+rework.completed));
   assert.ok(counts.includes('待重製 '+rework.pending));
   assert.ok((await card.textContent()).includes('其餘重製維持暫停'));
   const badge=await page.locator('#illustration-rework-state').textContent();
   assert.equal(badge,batch.state==='active'?`生物限額 ${batch.completedQuestionIds.length}／10 題`:'本批10題已完成，已停止');
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   const screenshot=path.join(root,`.cache/biology-ten-20261117/monitor-${width}.png`);
   await card.screenshot({path:screenshot});
   rows.push({width,completed:rework.completed,pending:rework.pending,biologyPending:rework.biologyPending,batch:rework.activeBatch,badge,screenshot});
  }
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(dir,'monitor-validation.json'),JSON.stringify({checkedAt:new Date().toISOString(),results:rows,errors},null,2)+'\n');
  console.log('PASS monitor desktop/mobile bounded ten-question progress');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
