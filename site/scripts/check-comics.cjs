// Browser checks for an explicitly selected, visually reviewed comic batch.
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
const ids=process.argv.slice(2);
if(!ids.length||ids.some(id=>!/^q-\d+$/.test(id)))throw Error('Pass q-NNN identifiers.');
const shotDir='/tmp/weirugo-comic-checks';fs.mkdirSync(shotDir,{recursive:true});
(async()=>{
 const browser=await chromium.launch();
 try {
  const page=await browser.newPage(),errors=[],results=[];
  await page.route('**/.netlify/functions/**',r=>r.abort());
  await require('./test-session.cjs').installTestSession(page);
  page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/.netlify/functions/marks**',r=>r.abort());
  for(const id of ids)for(const standalone of [false,true]){
   await page.setViewportSize({width:1440,height:1000});
   await page.goto('http://127.0.0.1:8765/site/'+(standalone?id+'.html':'index.html?comic=check#question/'+id));
   const comic=page.locator('.native-comic');
   assert.equal(await comic.isVisible(),false,id+' must start collapsed');
   await page.locator(standalone?'details.review summary':'#answer-toggle').click();
   await comic.scrollIntoViewIfNeeded();
   await page.waitForFunction(()=>[...document.querySelectorAll('.native-comic .comic-art img')].every(i=>i.complete&&i.naturalWidth>0));
   for(const width of [1440,1120,390]){
    await page.setViewportSize({width,height:1000});
    await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(150);
    const result=await comic.evaluate(c=>{
     const words=JSON.parse(c.dataset.protectedWords||'[]').filter(w=>typeof w==='string'&&w.length>=2),protectedBreaks=[];
     for(const el of c.querySelectorAll('.comic-text')){
      const lines=[...el.querySelectorAll('.comic-line')].map(x=>x.textContent),text=lines.join('');
      let offset=0;const boundaries=lines.slice(0,-1).map(line=>(offset+=line.length));
      for(const word of words)for(let start=text.indexOf(word);start>=0;start=text.indexOf(word,start+word.length)){
       if(boundaries.some(end=>start<end&&end<start+word.length))protectedBreaks.push({word,text});
      }
     }
     return {
     width:c.clientWidth,height:c.clientHeight,wrapErrors:c.querySelectorAll('[data-wrap-error]').length,
     protectedBreaks,
     cells:[...c.querySelectorAll('.comic-cell')].map(x=>{const r=x.getBoundingClientRect();return {width:r.width,height:r.height,left:r.left,top:r.top};}),
     autoRows:getComputedStyle(c.querySelector('.comic-grid')).gridAutoRows,
     overflow:[...c.querySelectorAll('.comic-line')].filter(x=>x.scrollWidth>x.clientWidth+1).map(x=>x.textContent),
     docOverflow:document.documentElement.scrollWidth>innerWidth,
     art:[...c.querySelectorAll('.comic-art')].map(x=>x.clientWidth),
     artImages:[...c.querySelectorAll('.comic-art img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.naturalWidth,height:i.naturalHeight,src:i.getAttribute('src')})),
     text:[...c.querySelectorAll('.comic-copy p')].map(x=>x.textContent),
    };});
    assert.equal(result.wrapErrors,0,id+' wrap');assert.deepEqual(result.overflow,[],id+' overflow');
    assert.deepEqual(result.protectedBreaks,[],id+' protected vocabulary must stay within one line');
    assert.equal(result.docOverflow,false,id+' document overflow');
    const [one,two,three,four]=result.cells;
    const close=(a,b)=>Math.abs(a-b)<1;
    assert.equal(result.autoRows,'auto',id+' content-driven row heights');
    if(close(one.top,two.top)){
     assert.ok(close(one.width,three.width)&&close(two.width,four.width),id+' equal widths within columns');
     assert.ok(close(three.top,four.top)&&close(one.height,two.height)&&close(three.height,four.height),id+' equal heights within each row');
    }else{
     assert.ok(result.cells.every(x=>close(x.width,one.width)),id+' equal widths in one column');
     assert.ok(one.top<two.top&&two.top<three.top&&three.top<four.top,id+' single-column reading order');
    }
    assert.ok(result.art.every(w=>w<=180));
    assert.equal(result.artImages.length,3,id+' three loaded illustration panels');
    assert.ok(result.artImages.every(i=>i.loaded&&i.width>0&&i.height>0),id+' image decoding');
    assert.ok(result.artImages.every(i=>i.src&&!i.src.startsWith('data:')),id+' shared assets rather than embedded image copies');
    const spec=JSON.parse(fs.readFileSync(path.join(root,'docs/comics',id+'.json')));
    assert.deepEqual(result.text.map(t=>t.replace(/\s/gu,'')),spec.panels.map(p=>p.text.replace(/\s/gu,'')),id+' must retain all copy');
    const shot=path.join(shotDir,`${id}-${standalone?'standalone':'app'}-${width}.png`);
    // Chromium temporarily expands the viewport for an element taller than the
    // screen. Fixed page controls can then be painted over that element's clip.
    // Keep the tested width and fit the whole comic before taking its evidence.
    const screenshotHeight=Math.max(1000,Math.ceil(result.height)+320);
    await page.setViewportSize({width,height:screenshotHeight});
    await comic.scrollIntoViewIfNeeded();
    await comic.screenshot({path:shot});
    results.push({id,standalone,viewport:width,...result,screenshot:shot,screenshotViewportHeight:screenshotHeight});
    await page.setViewportSize({width,height:1000});
   }
  }
  assert.deepEqual(errors,[]);
  const record={checkedAt:new Date().toISOString(),results};
  for(const id of ids)fs.writeFileSync(path.join(root,'docs/comics',id+'-validation.json'),JSON.stringify({...record,results:results.filter(r=>r.id===id)},null,2)+'\n');
  console.log('PASS',results.length,'layout checks; screenshots in',shotDir);
 } finally {await browser.close();}
})();
