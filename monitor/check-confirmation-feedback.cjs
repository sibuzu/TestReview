// Exercise the real Monitor UI with isolated API fixtures; never POST real records.
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),out=path.join(root,'.cache/monitor-feedback');
fs.mkdirSync(out,{recursive:true});
(async()=>{
 const baseline=await (await fetch('http://127.0.0.1:8912/api/status')).json();
 const browser=await chromium.launch(),results=[];
 try{for(const width of [1440,390,320]){
  const context=await browser.newContext({viewport:{width,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const fixture=structuredClone(baseline),posts=[];
  const card={id:'feedback-fixture',title:'意見流程隔離測試',kind:'題目核對',questions:['請確認完整原題。'],questionText:'此卡只存在測試瀏覽器，沒有加入正式確認清單。',questionUrl:'/site/index.html#question/q-875',sourceUrl:'https://example.com/source',confirmationToken:'fixture-token'};
  fixture.confirmations=[structuredClone(card)];fixture.summary.confirmations=1;
  let failNext=false;
  await page.route('**/api/status',r=>r.fulfill({json:fixture}));
  await page.route('**/api/confirm',async route=>{
   const payload=route.request().postDataJSON();posts.push(payload);
   if(failNext){failNext=false;return route.fulfill({status:503,json:{error:'隔離測試：暫時無法儲存'}});}
   const current=fixture.confirmations.find(c=>c.id===payload.id);
   if(payload.comment.trim()){
    current.userComments=[{text:payload.comment.trim(),state:'pending',submittedAt:'2026-10-31T10:00:00Z'}];current.feedbackPending=true;
    return route.fulfill({json:{ok:true,id:payload.id,state:'feedback_pending'}});
   }
   fixture.confirmations=fixture.confirmations.filter(c=>c.id!==payload.id);
   fixture.summary.confirmations=fixture.confirmations.length;
   fixture.resolvedConfirmations.unshift({...current,state:'resolved',resolvedAt:'2026-10-31T10:01:00Z',resolution:'使用者確認 OK',userComments:(current.userComments||[]).map(c=>({...c,state:'addressed'}))});
   return route.fulfill({json:{ok:true,id:payload.id}});
  });
  await page.goto('http://127.0.0.1:8912/');
  const input=()=>page.locator('[data-comment-for="feedback-fixture"]');
  const button=()=>page.locator('[data-confirm="feedback-fixture"]');
  await input().waitFor();
  const note='請補上原圖與選項，答案先保留 B。 <img src=x onerror="alert(1)">';
  await input().fill(note);await input().evaluate(el=>el.setSelectionRange(6,6));
  fixture.activity.detail+=' unrelated progress update';await page.evaluate(()=>refresh());
  assert.equal(await input().inputValue(),note);
  assert.equal(await input().evaluate(el=>document.activeElement===el&&el.selectionStart===6),true);
  await input().evaluate(el=>window.__draftInput=el);
  await input().dispatchEvent('compositionstart');
  fixture.confirmations.push({...card,id:'second-fixture',title:'另一張卡',confirmationToken:'second-token'});fixture.summary.confirmations=2;
  await page.evaluate(()=>refresh());
  assert.equal(await input().evaluate(el=>el===window.__draftInput),true);
  await input().dispatchEvent('compositionend');
  assert.equal(await input().inputValue(),note);
  assert.equal(await input().evaluate(el=>document.activeElement===el&&el.selectionStart===6),true);
  await input().locator('xpath=ancestor::article').screenshot({path:path.join(out,`draft-${width}.png`)});
  failNext=true;await button().click();
  await page.waitForFunction(()=>document.getElementById('confirm-feedback').textContent.includes('尚未儲存'));
  assert.equal(await input().inputValue(),note);assert.equal(await input().isEnabled(),true);
  await button().click();
  await page.waitForFunction(()=>document.getElementById('confirm-feedback').textContent.includes('意見已儲存'));
  await page.waitForFunction(()=>document.querySelector('.saved-comment'));
  assert.equal(await button().count(),1);assert.equal(await input().inputValue(),'');
  assert.equal(await page.locator('.saved-comment img').count(),0);
  assert.match(await page.locator('.saved-comment').first().innerText(),/請補上原圖/);
  await input().locator('xpath=ancestor::article').screenshot({path:path.join(out,`saved-${width}.png`)});
  await input().fill(' \n ');await button().click();
  await button().waitFor({state:'detached'});
  assert.equal(posts.length,3);assert.equal(posts[1].comment,note);assert.equal(posts[2].comment.trim(),'');
  await page.locator('#resolved').locator('xpath=ancestor::details').locator('summary').click();
  await page.locator('#resolved [data-review]').first().click();
  const dialog=page.locator('#confirmation-detail');await dialog.waitFor({state:'visible'});
  assert.match(await dialog.innerText(),/使用者意見/);assert.match(await dialog.innerText(),/請補上原圖/);
  assert.equal(await dialog.locator('.saved-comment img').count(),0);
  await dialog.locator('[data-close-review]').click();
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  assert.deepEqual(errors,[]);
  results.push({width,passed:true,draftAndCaretSurviveRefresh:true,compositionNotInterrupted:true,failedSavePreservesInput:true,commentRemainsPending:true,blankApproves:true,historyIncludesComment:true,htmlEscaped:true,noOverflow:true,realRecordWrites:0});
  await context.close();
 }}finally{await browser.close();}
 const report={passed:true,method:'Real Monitor HTML with isolated status and POST fixtures; backend persistence tested independently in monitor.test_server',results};
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
