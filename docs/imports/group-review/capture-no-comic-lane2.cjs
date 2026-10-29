const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('/home/jack/ai/Chemery/node_modules/playwright');
const root=path.resolve(__dirname,'../../..');
const input=process.argv[2];
const {createGroupShadow}=require(path.join(root,'site/scripts/group-shadow.cjs'));
const shadow=createGroupShadow([input]),q=shadow.groups[0].question;
const without=q.groupQuestions.filter(c=>!c.teachingComic);
if(!without.length)process.exit(0);
(async()=>{
 const browser=await chromium.launch();
 try{
  const page=await browser.newPage();
  await page.route('**/.netlify/functions/**',r=>r.abort());
  await require(path.join(root,'site/scripts/test-session.cjs')).installTestSession(page);
  await shadow.install(page);
  for(const width of [1440,390]){
   await page.setViewportSize({width,height:1400});
   await page.goto('http://127.0.0.1:8765/site/index.html#question/'+q.id);
   await page.locator('#answer-toggle').waitFor();
   await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(img=>{img.loading='eager';return img.decode();})));
   await page.evaluate(()=>document.fonts.ready);
   for(const child of without)await page.locator(`[data-group-question="${child.id}"]`).screenshot({path:`/tmp/weirugo-group-checks/${q.id}-${child.id}-no-comic-question-${width}.png`});
   if(await page.locator('#answer-toggle').getAttribute('aria-expanded')!=='true')await page.locator('#answer-toggle').click();
   for(const child of without)await page.locator(`[data-group-answer="${child.id}"]`).screenshot({path:`/tmp/weirugo-group-checks/${q.id}-${child.id}-no-comic-answer-${width}.png`});
  }
  console.log('NO_COMIC_CAPTURED',without.map(c=>c.id).join(','));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
