const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const {chromium}=require(path.resolve('.cache/qa-tools/node_modules/playwright'));const root=process.cwd();
const base=path.join(root,'docs/imports/new-gpt-20261119-73/lane2'),out=path.join(root,'.cache/intake-20261119-73-lane2');fs.mkdirSync(out,{recursive:true});
(async()=>{const browser=await chromium.launch();try{const page=await browser.newPage();const all=[];
for(const id of ['q-1157','q-1158','q-1159','q-1160','q-1161','q-1162']){
 const spec=JSON.parse(fs.readFileSync(path.join(base,'specs',id+'.json')));const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file://'+path.join(base,'qa',id+'-preview.html'));const comic=page.locator('.native-comic');assert.equal(await comic.isVisible(),false);await page.locator('summary').click();
 const results=[];
 for(const width of [1440,1120,390]){
 await page.setViewportSize({width,height:1100});await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(150);
 const r=await comic.evaluate(c=>({wrapErrors:c.querySelectorAll('[data-wrap-error]').length,overflow:[...c.querySelectorAll('.comic-line')].filter(l=>l.scrollWidth>l.clientWidth+1).map(l=>l.textContent),docOverflow:document.documentElement.scrollWidth>innerWidth,art:[...c.querySelectorAll('.comic-art img')].map(i=>({src:i.src.slice(0,30),loaded:i.complete&&i.naturalWidth>0,width:i.parentElement.clientWidth})),text:[...c.querySelectorAll('.comic-copy p')].map(p=>p.textContent)}));
 assert.equal(r.wrapErrors,0);assert.deepEqual(r.overflow,[]);assert.equal(r.docOverflow,false);assert.equal(r.art.length,4);assert.ok(r.art.every(x=>x.loaded&&x.width<=180));assert.deepEqual(r.text.map(x=>x.replace(/\s/gu,'')),spec.panels.map(p=>p.text.replace(/\s/gu,'')));
 const screenshot=path.join(out,id+'-preview-'+width+'.png');await comic.screenshot({path:screenshot});results.push({width,...r,screenshot});
 }
 const imgs=spec.panels.map(p=>p.image).concat(spec.fourth.image);const gallery='<meta charset="utf-8"><style>body{margin:0;background:white}.g{display:grid;grid-template-columns:630px 630px;gap:8px}figure{margin:0}img{width:630px;height:630px}figcaption{font:20px sans-serif}</style><div class="g">'+imgs.map((im,i)=>`<figure><figcaption>${id} panel ${i+1}</figcaption><img src="file://${root}/${im}"></figure>`).join('')+'</div>';
 const file=path.join(out,id+'-art-gallery.html');fs.writeFileSync(file,gallery);await page.setViewportSize({width:1300,height:1350});await page.goto('file://'+file);await page.evaluate(()=>document.fonts.ready);await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));const artScreenshot=path.join(out,id+'-art-contact.png');await page.locator('.g').screenshot({path:artScreenshot});assert.deepEqual(errors,[]);
 const report={id,passed:true,checkedAt:new Date().toISOString(),results,artScreenshot,actualViewed:false};fs.writeFileSync(path.join(base,'qa',id+'-validation.json'),JSON.stringify(report,null,2)+'\n');all.push(report);console.log('PASS',id);
}
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
