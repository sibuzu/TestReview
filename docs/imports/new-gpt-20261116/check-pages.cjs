// Local publication QA only. Uses an isolated mocked Demo session.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(path.resolve(__dirname,'../../../.cache/qa-tools/node_modules/playwright'));
const root=path.resolve(__dirname,'../../..'),ids=process.argv.slice(2);
assert.ok(ids.length&&ids.every(id=>/^q-\d+$/.test(id)),'Pass published question IDs.');
const shots=path.join(__dirname,'qa');fs.mkdirSync(shots,{recursive:true});
const data=JSON.parse(fs.readFileSync(path.join(root,'site/dist/data.json')));
(async()=>{
 const browser=await chromium.launch({headless:true}),results=[];
 try{
  for(const id of ids){
   const q=data.questions.find(q=>q.id===id);assert.ok(q,id+' is published');
   const errors=[],page=await browser.newPage();
   page.on('pageerror',e=>errors.push(e.message));
   await page.route('**/.netlify/functions/**',route=>route.abort());
   await require(path.join(root,'site/scripts/test-session.cjs')).installTestSession(page);
   for(const standalone of [false,true])for(const width of [1440,390]){
    await page.setViewportSize({width,height:1000});
    const url='http://127.0.0.1:8912/site/'+(standalone?id+'.html?qa='+width:'index.html?qa='+width+'#question/'+id);
    const response=await page.goto(url);assert.equal(response.status(),200);
    await page.locator(standalone?'h1':'#detail h1').waitFor();
    const title=await page.locator(standalone?'h1':'#detail h1').innerText();
    assert.ok(title.includes(q.title.replace(/（待更新）$/,'')),id+' title');
    const panel=page.locator(standalone?'details.review': '#answer-panel');
    assert.equal(standalone?await panel.evaluate(el=>el.open):await panel.isVisible(),false,id+' answer initially collapsed');
    await page.locator(standalone?'details.review summary':'#answer-toggle').click();
    assert.equal(standalone?await panel.evaluate(el=>el.open):await panel.isVisible(),true,id+' answer expanded');
    const container=page.locator(standalone?'main':'#detail');
    await page.evaluate(()=>document.fonts.ready);
    await page.waitForFunction(()=>[...document.querySelectorAll('main img')].every(i=>i.complete&&i.naturalWidth>0));
    const result=await container.evaluate(el=>({
     documentOverflow:document.documentElement.scrollWidth>innerWidth+1,
     images:[...el.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0,width:i.naturalWidth,height:i.naturalHeight})),
     questionText:el.querySelector('.question,.question-text')?.innerText||'',
     text:el.innerText
    }));
    assert.equal(result.documentOverflow,false,id+' '+width+' page overflow');
    assert.ok(result.images.every(i=>i.loaded),id+' all original figures decoded');
    const compact=text=>text.replace(/\s/gu,'');
    for(const child of q.groupQuestions||[q]){assert.ok(compact(result.text).includes(compact(child.answer)),child.id+' answer wording preserved');for(const line of child.question.split('\n'))assert.ok(compact(result.text).includes(compact(line)),child.id+' complete stem and original option text preserved');if(child.passage)assert.ok(compact(result.text).includes(compact(child.passage)),child.id+' complete shared material preserved');}
    const shot=path.join(shots,`${id}-${standalone?'standalone':'app'}-${width}.png`);
    // Avoid Chromium painting fixed controls over a tall element screenshot.
    // Geometry checks above use the normal viewport; only capture fits height.
    const screenshotViewportHeight=Math.max(1000,Math.ceil((await container.boundingBox()).height)+160);
    await page.setViewportSize({width,height:screenshotViewportHeight});
    await container.scrollIntoViewIfNeeded();
    await container.screenshot({path:shot});
    results.push({id,standalone,width,url,title,...result,screenshot:path.relative(root,shot),screenshotViewportHeight});
    await page.setViewportSize({width,height:1000});
    await page.locator(standalone?'details.review summary':'#answer-toggle').click();
    assert.equal(standalone?await panel.evaluate(el=>el.open):await panel.isVisible(),false,id+' shared answer/explanation/evidence collapse');
   }
   assert.deepEqual(errors,[],id+' no JavaScript errors');await page.close();
  }
 }finally{await browser.close();}
 const record={checkedAt:new Date().toISOString(),passed:true,questionIds:ids,viewports:[1440,390],views:['app','standalone'],testSession:'mock Demo; no real tokens',visualInspectionPending:true,results};
 fs.writeFileSync(path.join(shots,'validation-'+ids.join('-')+'.json'),JSON.stringify(record,null,2)+'\n');
 console.log('PASS',ids.join(', '),results.length+' layouts; view saved screenshots before claiming visual inspection.');
})().catch(error=>{console.error(error);process.exitCode=1});
