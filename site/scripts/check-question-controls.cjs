// Isolated browser storage and frozen data fixture; never touches personal marks.
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
const data=JSON.parse(fs.readFileSync(path.join(root,'site/dist/data.json')));
const output=path.join(root,'.cache/question-controls');fs.mkdirSync(output,{recursive:true});
const done=new Set(['q-024','q-201','q-820']);
const colors={red:'rgb(239, 8, 8)',blue:'rgb(33, 102, 196)',orange:'rgb(255, 128, 0)',green:'rgb(80, 223, 0)',yellow:'rgb(255, 233, 0)'};
(async()=>{
 const browser=await chromium.launch({headless:true}),results=[];
 try{
 for(const width of [1440,390,360]){
  const context=await browser.newContext({viewport:{width,height:1000}}),page=await context.newPage(),errors=[],cloud=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(r.url().includes('/.netlify/functions/marks'))cloud.push(r.url());});
  await page.route('**/data.json',r=>r.fulfill({json:data}));
  await page.route('**/.netlify/functions/marks**',r=>r.abort());
  await page.addInitScript(()=>{if(!sessionStorage.getItem('controls-fixture')){
   localStorage.setItem('test-review:favorites:v1',JSON.stringify(['q-024','q-201','q-225','q-821']));
   localStorage.setItem('test-review:favorite-colors:v1',JSON.stringify({'q-024':'red','q-201':'blue','q-225':'orange','q-821':'green'}));
   localStorage.setItem('test-review:doubts:v1',JSON.stringify(['q-201','q-225']));
   localStorage.setItem('test-review:answered:v1',JSON.stringify(['q-024','q-201','q-821']));
   sessionStorage.setItem('controls-fixture','yes');
  }});
  const scope=page.locator('[data-answered-scope]'),navAll=page.locator('.all-nav-link');
  const storage=key=>page.evaluate(k=>JSON.parse(localStorage.getItem(k)||'null'),key);
  const ids=()=>page.locator('#results [data-open]').evaluateAll(els=>els.map(e=>e.dataset.open));
  const readColor=()=>page.locator('[data-detail-star]').evaluate(e=>getComputedStyle(e).color);
  const openPalette=async()=>{await page.locator('[data-detail-star]').click();assert.equal(await page.locator('#favorite-palette').isVisible(),true);};
  await page.goto('http://127.0.0.1:8912/site/index.html#questions',{waitUntil:'domcontentloaded'});
  await page.waitForSelector('#results [data-open]');
  assert.equal(await page.locator('#answered-filter').count(),0);
  assert.match(await navAll.innerText(),new RegExp('全部錯題\\s*'+data.questions.length));
  assert.equal((await ids()).length,data.questions.length);
  assert.equal(await page.locator('#results button.star,#results [data-star]').count(),0);
  await scope.click();assert.equal(await page.locator('#page-title').innerText(),'未作錯題');
  await page.locator('.all-nav').screenshot({path:path.join(output,'scope-not-done-'+width+'.png')});
  assert.equal((await ids()).length,data.questions.length-done.size);
  assert.ok(!(await ids()).includes('q-024'));
  assert.equal(await page.locator('[data-subject="Chinese"] .count').innerText(),String(data.questions.filter(q=>q.subject==='Chinese').length-1));
  await page.locator('[data-subject="English"]').click();assert.equal(await page.locator('#page-title').innerText(),'英文');
  assert.ok(!(await ids()).includes('q-201'));assert.match(await navAll.innerText(),/未作錯題/);
  await page.locator('[data-nav="star"]').click();assert.deepEqual(await ids(),['q-225']);
  const beforeFavorite=await storage('test-review:favorites:v1');
  await page.locator('[data-open="q-225"] .favorite-indicator').click();
  await page.waitForSelector('#detail [data-answered]');assert.deepEqual(await storage('test-review:favorites:v1'),beforeFavorite);
  assert.equal(await page.locator('#favorite-palette').isVisible(),false);
  assert.match(await page.locator('#detail [data-answered]').getAttribute('title'),/X key/);
  await page.locator('#answer-toggle').click();await page.evaluate(()=>window.controlDetail=document.querySelector('#detail .detail-content'));
  await page.keyboard.press('x');assert.equal(await page.locator('[data-answered]').getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator('#toast').innerText(),'已設定為「已作」');assert.equal(await page.locator('#answer-panel').isVisible(),true);
  assert.equal(await page.evaluate(()=>window.controlDetail===document.querySelector('#detail .detail-content')),true);
  await page.keyboard.press('X');assert.equal(await page.locator('[data-answered]').getAttribute('aria-pressed'),'false');
  assert.equal(await page.locator('#toast').innerText(),'已設定為「未作」');
  const beforeAnswered=await storage('test-review:answered:v1');await page.keyboard.press('Control+x');
  assert.deepEqual(await storage('test-review:answered:v1'),beforeAnswered);
  await page.evaluate(()=>{const t=document.createElement('textarea');t.id='typing-guard';document.querySelector('#detail').append(t);t.focus();});
  await page.keyboard.type('x');assert.deepEqual(await storage('test-review:answered:v1'),beforeAnswered);assert.equal(await page.locator('#typing-guard').inputValue(),'x');
  await page.keyboard.type('X');assert.deepEqual(await storage('test-review:answered:v1'),beforeAnswered);assert.equal(await page.locator('#typing-guard').inputValue(),'xX');
  await page.evaluate(()=>document.getElementById('typing-guard').remove());
  await scope.click();assert.match(await navAll.innerText(),/已作錯題\s*3/);assert.equal(await page.locator('#answer-panel').isVisible(),true);
  await page.locator('.all-nav').screenshot({path:path.join(output,'scope-done-'+width+'.png')});
  await navAll.click();assert.equal(await page.locator('#page-title').innerText(),'已作錯題');assert.deepEqual(new Set(await ids()),done);
  await page.goBack();await page.waitForSelector('#detail [data-answered]');assert.match(await navAll.innerText(),/已作錯題/);
  await page.locator('[data-question-return]').click();assert.equal(await page.locator('#page-title').innerText(),'重點收藏');assert.deepEqual(new Set(await ids()),done);
  await scope.click();assert.match(await navAll.innerText(),/全部錯題/);
  await navAll.click();await page.locator('[data-open="q-024"]').click();await page.locator('#answer-toggle').click();
  assert.equal(await readColor(),colors.red);
  await openPalette();const buttons=page.locator('#favorite-palette button');assert.equal(await buttons.count(),6);
  assert.deepEqual(await buttons.evaluateAll(els=>els.map(e=>e.dataset.favoriteColor)),['','red','blue','orange','green','yellow']);
  const boxes=await buttons.evaluateAll(els=>els.map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y}}));
  assert.equal(boxes[0].y,boxes[1].y);assert.equal(boxes[1].y,boxes[2].y);assert.equal(boxes[0].x,boxes[3].x);assert.equal(boxes[3].y,boxes[5].y);
  assert.ok(boxes[3].y>boxes[0].y);
  await page.screenshot({path:path.join(output,'palette-'+width+'.png')});
  await page.locator('#detail h1').click();assert.equal(await page.locator('#favorite-palette').isVisible(),false);assert.equal(await readColor(),colors.red);
  await openPalette();await page.keyboard.press('Escape');assert.equal(await page.locator('#favorite-palette').isVisible(),false);assert.equal(await readColor(),colors.red);
  await openPalette();await page.keyboard.press('ArrowRight');await page.keyboard.press('Enter');assert.equal(await readColor(),colors.blue);assert.equal(await page.locator('#favorite-palette').isVisible(),false);
  for(const color of ['blue','orange','green','yellow','red']){
   await openPalette();await page.locator('[data-favorite-color="'+color+'"]').click();
   assert.equal(await page.locator('#favorite-palette').isVisible(),false);assert.equal(await readColor(),colors[color]);
   assert.equal((await storage('test-review:favorite-colors:v1'))['q-024'],color);assert.equal(await page.locator('#answer-panel').isVisible(),true);
  }
  await page.reload({waitUntil:'domcontentloaded'});await page.waitForSelector('[data-detail-star]');assert.equal(await readColor(),colors.red);
  await openPalette();await page.locator('[data-favorite-color=""]').click();assert.equal(await page.locator('[data-detail-star]').innerText(),'☆');
  assert.ok(!(await storage('test-review:favorites:v1')).includes('q-024'));assert.equal((await storage('test-review:favorite-colors:v1'))['q-024'],undefined);
  await page.evaluate(()=>location.hash='#question/q-821');await page.waitForFunction(()=>document.querySelector('[data-detail-star]')?.dataset.detailStar==='q-820');
  assert.equal(await readColor(),colors.green);await openPalette();await page.locator('[data-favorite-color="orange"]').click();
  assert.ok((await storage('test-review:favorites:v1')).includes('q-820'));assert.ok(!(await storage('test-review:favorites:v1')).includes('q-821'));
  assert.equal((await storage('test-review:favorite-colors:v1'))['q-820'],'orange');assert.equal((await storage('test-review:favorite-colors:v1'))['q-821'],undefined);
  await navAll.click();assert.equal(await page.locator('[data-open="q-820"] .favorite-indicator').evaluate(e=>getComputedStyle(e).color),colors.orange);
  const listAnswered=await storage('test-review:answered:v1');await page.keyboard.press('x');assert.deepEqual(await storage('test-review:answered:v1'),listAnswered);
  assert.deepEqual(errors,[]);assert.deepEqual(cloud,[]);
  const dimensions=await page.evaluate(()=>({width:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth}));assert.equal(dimensions.width,dimensions.scrollWidth);
  if(width<761){const rows=await page.locator('.filter-controls select').evaluateAll(els=>els.map(e=>e.getBoundingClientRect().y));assert.ok(rows.every(y=>y===rows[0]));}
  await page.screenshot({path:path.join(output,'list-'+width+'.png')});
  results.push({width,result:'PASS',globalScope:'all/not-done/done, subject/favorites/history/detail',palette:'3x2 five colors plus none, read-only list, closes on selection/outside/Escape, alias and reload persistence',shortcut:'x/X updates mark and bubble without collapsing explanation; typing/modifier/list ignored',cloudRequests:cloud.length,dimensions});
  await context.close();
 }
 fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
