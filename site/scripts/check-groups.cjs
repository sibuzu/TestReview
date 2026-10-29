// Check EVERY child comic, not the first comic in a merged group.
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {createGroupShadow}=require('./group-shadow.cjs');
const root=path.resolve(__dirname,'../..'),args=process.argv.slice(2),shadowMode=args[0]==='--shadow';
const inputs=shadowMode?args.slice(1):args;if(!inputs.length)throw Error('Pass q-NNN groups, or --shadow manifest.json ...');
const shadow=shadowMode?createGroupShadow(inputs):null;
const data=shadow?.data||JSON.parse(fs.readFileSync(path.join(root,'site/dist/data.json')));
const groups=shadow?.groups||inputs.map(id=>({question:data.questions.find(q=>q.id===id),manifest:{groupId:id}}));
const compact=value=>String(value||'').replace(/\s/gu,'');
const output=path.join(root,'docs/imports/group-review/qa');fs.mkdirSync(output,{recursive:true});
const shots='/tmp/weirugo-group-checks';fs.mkdirSync(shots,{recursive:true});

function measureComic(c){
 const words=JSON.parse(c.dataset.protectedWords||'[]'),protectedBreaks=[];
 for(const el of c.querySelectorAll('.comic-text')){
  const lines=[...el.querySelectorAll('.comic-line')].map(x=>x.textContent),text=lines.join('');let offset=0;
  const boundaries=lines.slice(0,-1).map(line=>(offset+=line.length));
  for(const word of words)for(let start=text.indexOf(word);start>=0;start=text.indexOf(word,start+word.length))if(boundaries.some(end=>start<end&&end<start+word.length))protectedBreaks.push(word);
 }
 return {height:c.clientHeight,wrapErrors:c.querySelectorAll('[data-wrap-error]').length,protectedBreaks,
  overflow:[...c.querySelectorAll('.comic-line')].filter(x=>x.scrollWidth>x.clientWidth+1).map(x=>x.textContent),
  cells:[...c.querySelectorAll('.comic-cell')].map(x=>{const r=x.getBoundingClientRect();return {width:r.width,height:r.height,left:r.left,top:r.top};}),
  autoRows:getComputedStyle(c.querySelector('.comic-grid')).gridAutoRows,
  art:[...c.querySelectorAll('.comic-art')].map(x=>x.clientWidth),
  decoded:[...c.querySelectorAll('.comic-art img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,src:i.getAttribute('src')})),
  copy:[...c.querySelectorAll('.comic-copy p')].map(x=>x.textContent),fourth:c.querySelector('.comic-answer')?.textContent};
}

(async()=>{
 const browser=await chromium.launch();let totalViews=0,totalComics=0;
 try{
  for(const {question:q,manifest}of groups){
   assert.ok(q?.groupQuestions?.length>=2,'Expected a complete merged group');const children=q.groupQuestions,expectedComics=children.filter(c=>c.teachingComic).length,rows=[],errors=[];
   const page=await browser.newPage();await page.route('**/.netlify/functions/**',r=>r.abort());await require('./test-session.cjs').installTestSession(page);await page.route('**/.netlify/functions/marks**',r=>r.abort());if(shadow)await shadow.install(page);page.on('pageerror',e=>errors.push(e.message));
   for(const standalone of [false,true]){
    await page.setViewportSize({width:1440,height:1000});await page.goto('http://127.0.0.1:8765/site/'+(standalone?q.id+'.html':'index.html#question/'+q.id));await page.reload();
    const toggle=page.locator(standalone?'details.review summary':'#answer-toggle');await toggle.waitFor();
    assert.equal(standalone?await page.locator('details.review').getAttribute('open'):await toggle.getAttribute('aria-expanded'),standalone?null:'false');
    assert.deepEqual(await page.locator('[data-group-question]').evaluateAll(nodes=>nodes.map(n=>n.dataset.groupQuestion)),children.map(c=>c.id));
    assert.equal(await page.locator('.native-comic:visible').count(),0);
    if(q.passage)assert.equal(await page.locator('.reading-passage').evaluateAll((nodes,text)=>nodes.filter(n=>n.textContent.includes(text)).length,q.passage),1,'Common passage repeated');
    for(const child of children){const stem=page.locator(`[data-group-question="${child.id}"] ${standalone?'.question':'.detail-question'}`);assert.equal(compact(await stem.textContent()),compact(child.question),child.id+' incomplete stem/options');}
    await toggle.click();assert.deepEqual(await page.locator('[data-group-answer]').evaluateAll(nodes=>nodes.map(n=>n.dataset.groupAnswer)),children.map(c=>c.id));assert.equal(await page.locator('.native-comic').count(),expectedComics);
    await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(img=>{img.loading='eager';return img.decode();})));
    for(const child of children){
     const section=page.locator(`[data-group-answer="${child.id}"]`);assert.equal(compact(await section.locator(standalone?'.answer':':scope > h3').textContent()),compact(child.answer),child.id+' answer');
     assert.equal(compact(await section.locator('.explanation').textContent()),compact(child.explanation),child.id+' explanation');
     assert.equal(await section.locator('.native-comic').count(),child.teachingComic?1:0,child.id+' own comic');
     const optionBlock=section.locator(standalone?'.table-wrap':'.option-analysis');const analysis=await optionBlock.count()?await optionBlock.textContent():'';for(const option of child.optionAnalysis||[])assert.ok(compact(analysis).includes(compact(option.explanation)),child.id+' lost option analysis');
     assert.ok((await section.locator('.group-child-source').textContent()).includes(child.date));assert.equal(await section.locator('.group-child-source a').count(),1,child.id+' missing source link');
    }
    for(const width of [1440,1120,390]){
     await page.setViewportSize({width,height:1000});await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(160);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
     const comicChecks=[],textOnlyChecks=[];
     for(const child of children){
      if(!child.teachingComic){
       const evidence={id:child.id,questionScreenshot:null,answerScreenshot:null};
       if(width!==1120)for(const [kind,selector]of [['question',`[data-group-question="${child.id}"]`],['answer',`[data-group-answer="${child.id}"]`]]){
        const block=page.locator(selector),height=await block.evaluate(el=>el.getBoundingClientRect().height);await page.setViewportSize({width,height:Math.max(1000,Math.ceil(height)+320)});const file=path.join(shots,`${q.id}-${child.id}-${standalone?'standalone':'app'}-${kind}-${width}.png`);await block.screenshot({path:file});evidence[kind+'Screenshot']=file;await page.setViewportSize({width,height:1000});
       }
       textOnlyChecks.push(evidence);continue;
      }
      const comic=page.locator(`[data-group-answer="${child.id}"] .native-comic`),result=await comic.evaluate(measureComic);assert.equal(result.wrapErrors,0,child.id+' wrap');assert.deepEqual(result.protectedBreaks,[],child.id+' protected terms');assert.deepEqual(result.overflow,[],child.id+' overflow');assert.equal(result.cells.length,4);assert.equal(result.autoRows,'auto');
      const [one,two,three,four]=result.cells,close=(a,b)=>Math.abs(a-b)<1;
      if(close(one.top,two.top)){assert.ok(close(one.width,three.width)&&close(two.width,four.width));assert.ok(close(three.top,four.top)&&close(one.height,two.height)&&close(three.height,four.height));}
      else {assert.ok(result.cells.every(x=>close(x.width,one.width)));assert.ok(one.top<two.top&&two.top<three.top&&three.top<four.top);}
      assert.ok(result.art.every(w=>w<=180));assert.equal(result.decoded.length,3);assert.ok(result.decoded.every(i=>i.loaded&&!i.src.startsWith('data:')));assert.deepEqual(result.copy.map(compact),child.teachingComic.panels.map(p=>compact(p.text)));assert.equal(compact(result.fourth),compact(child.teachingComic.fourth.answer));
      let screenshot=null;if(width!==1120){await page.setViewportSize({width,height:Math.max(1000,Math.ceil(result.height)+320)});screenshot=path.join(shots,`${q.id}-${child.id}-${standalone?'standalone':'app'}-${width}.png`);await comic.screenshot({path:screenshot});await page.setViewportSize({width,height:1000});}
      comicChecks.push({id:child.id,...result,screenshot});
     }
     rows.push({standalone,width,defaultCollapsed:true,childIds:children.map(c=>c.id),expectedComicCount:expectedComics,comics:comicChecks,textOnlyChildren:textOnlyChecks,noDocumentOverflow:true});totalViews++;
    }
   }
   assert.deepEqual(errors,[]);await page.close();totalComics+=expectedComics;
   fs.writeFileSync(path.join(output,(manifest.groupId||q.id)+'-validation.json'),JSON.stringify({checkedAt:new Date().toISOString(),questionId:q.id,groupId:manifest.groupId,shadow:shadowMode,manifestInput:shadowMode?inputs.find(input=>JSON.parse(fs.readFileSync(path.resolve(root,input))).retainId===q.id):null,childIds:children.map(c=>c.id),expectedComicCount:expectedComics,isolatedDemo:true,actualCloudRequestsAborted:true,desktopMobileActuallyViewed:false,rows},null,2)+'\n');
   console.log('PASS',q.id,children.length,'children',expectedComics,'comics x6 layouts');
  }
  console.log('PASS total',totalViews,'group views',totalComics,'individual comics; evidence',output);
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
