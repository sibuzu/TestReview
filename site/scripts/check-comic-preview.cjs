// Worker-local QA: never attach/curate or mutate another worker's artifacts.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const root=path.resolve(__dirname,'../..'),id=process.argv[2];
if(!/^q-\d+$/.test(id))throw Error('Pass one q-NNN identifier');
const html=execFileSync('python',[path.join(__dirname,'preview-comic.py'),id],{encoding:'utf8'}).trim();
const spec=JSON.parse(fs.readFileSync(path.join(root,'docs/comics',id+'.json')));
(async()=>{const browser=await chromium.launch();try{
 const page=await browser.newPage(),results=[],errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file://'+html);const comic=page.locator('.native-comic');assert.equal(await comic.isVisible(),false);await page.locator('summary').click();
 for(const width of [1440,1120,390]){
  await page.setViewportSize({width,height:1000});await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(150);
  const r=await comic.evaluate(c=>{
   const words=JSON.parse(c.dataset.protectedWords||'[]'),protectedBreaks=[];
   for(const el of c.querySelectorAll('.comic-text')){
    const lines=[...el.querySelectorAll('.comic-line')].map(l=>l.textContent),text=lines.join('');let offset=0;const ends=lines.slice(0,-1).map(l=>(offset+=l.length));
    for(const word of words)for(let start=text.indexOf(word);start>=0;start=text.indexOf(word,start+word.length))if(ends.some(end=>start<end&&end<start+word.length))protectedBreaks.push(word);
   }
   return {width:c.clientWidth,wrapErrors:c.querySelectorAll('[data-wrap-error]').length,protectedBreaks,
    overflow:[...c.querySelectorAll('.comic-line')].filter(l=>l.scrollWidth>l.clientWidth+1).map(l=>l.textContent),docOverflow:document.documentElement.scrollWidth>innerWidth,
    cells:[...c.querySelectorAll('.comic-cell')].map(l=>{const r=l.getBoundingClientRect();return {width:r.width,height:r.height,top:r.top}}),
    art:[...c.querySelectorAll('.comic-art img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.parentElement.clientWidth})),
    text:[...c.querySelectorAll('.comic-copy p')].map(p=>p.textContent)};
  });
  assert.equal(r.wrapErrors,0);assert.deepEqual(r.protectedBreaks,[]);assert.deepEqual(r.overflow,[]);assert.equal(r.docOverflow,false);assert.ok(r.art.every(i=>i.loaded&&i.width<=180));
  assert.deepEqual(r.text.map(t=>t.replace(/\s/gu,'')),spec.panels.map(p=>p.text.replace(/\s/gu,'')));
  const close=(a,b)=>Math.abs(a-b)<1,[a,b,c,d]=r.cells;
  assert.ok(close(a.width,c.width)&&close(b.width,d.width));
  if(close(a.top,b.top))assert.ok(close(a.height,b.height)&&close(c.height,d.height));else assert.ok(a.top<b.top&&b.top<c.top&&c.top<d.top);
  const screenshot='/tmp/weirugo-comic-previews/'+id+'-'+width+'.png';await comic.screenshot({path:screenshot});results.push({viewport:width,...r,screenshot});
 }
 assert.deepEqual(errors,[]);fs.writeFileSync(path.join(root,'docs/comics',id+'-preview-validation.json'),JSON.stringify({checkedAt:new Date().toISOString(),isolatedPreview:html,results},null,2)+'\n');
 console.log('PASS',id,'1440/1120/390; actually view the screenshots before reporting visual QA complete.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
