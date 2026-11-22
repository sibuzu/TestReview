const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../../../..'),out=path.join(root,'.cache/source74-earthb-qa');
const {chromium}=require(path.join(root,'.cache/qa-tools/node_modules/playwright'));
(async()=>{const b=await chromium.launch();const results=[];try{for(let n=1175;n<=1178;n++){
 const p=await b.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto('file://'+path.join(out,`q-${n}.html`));
 assert.equal(await p.locator('.native-comic').isVisible(),false);await p.locator('summary').click();const widths=[];
 for(const w of [1440,1120,390]){await p.setViewportSize({width:w,height:1000});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
 const r=await p.locator('.native-comic').evaluate(c=>({wrapErrors:c.querySelectorAll('[data-wrap-error]').length,overflow:[...c.querySelectorAll('.comic-line')].filter(l=>l.scrollWidth>l.clientWidth+1).map(l=>l.textContent),docOverflow:document.documentElement.scrollWidth>innerWidth,images:[...c.querySelectorAll('img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.getBoundingClientRect().width})),cells:[...c.querySelectorAll('.comic-cell')].map(e=>{let r=e.getBoundingClientRect();return{width:r.width,height:r.height,top:r.top}})}));
 assert.equal(r.wrapErrors,0);assert.deepEqual(r.overflow,[]);assert.equal(r.docOverflow,false);assert.equal(r.images.length,4);assert.ok(r.images.every(i=>i.loaded&&i.width<=180.1));
 let[a,bb,c,d]=r.cells,close=(x,y)=>Math.abs(x-y)<1;assert.ok(close(a.width,c.width)&&close(bb.width,d.width));if(close(a.top,bb.top)){assert.ok(close(a.height,bb.height)&&close(c.height,d.height))}else assert.ok(a.top<bb.top&&bb.top<c.top&&c.top<d.top);
 let file=path.join(out,`q-${n}-${w}.png`);await p.screenshot({path:file,fullPage:true});widths.push({viewport:w,...r,screenshot:path.relative(root,file)});
 }assert.deepEqual(errors,[]);results.push({id:`q-${n}`,widths});await p.close();
 }fs.writeFileSync(path.join(__dirname,'qa/automated-validation.json'),JSON.stringify({passed:true,checkedAt:new Date().toISOString(),results},null,2)+'\n');console.log('PASS four questions at 1440/1120/390; four loaded figures, no overflow, collapsed answers, equal grid widths and heights.');}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
