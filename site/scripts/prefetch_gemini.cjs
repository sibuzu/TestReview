/* Acquisition only: never marks a source curated or edits curation progress. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {execFileSync} = require('node:child_process');
const {chromium} = require('playwright');
const ROOT = path.resolve(__dirname, '../..');
const progressFile = path.join(ROOT, 'docs/imports/more-gemini-progress.json');
const orders = process.argv.slice(2).map(Number);
const sourceCount = JSON.parse(fs.readFileSync(progressFile,'utf8')).sources.length;
if(!orders.length || orders.some(n=>!Number.isInteger(n)||n<1||n>sourceCount))throw Error(`Pass Gemini source orders (1–${sourceCount})`);
fs.mkdirSync(path.join(ROOT,'docs/acquisition'),{recursive:true});
const priorStatus=path.join(ROOT,'monitor/gemini-acquisition.json');
const previous=fs.existsSync(priorStatus)?JSON.parse(fs.readFileSync(priorStatus,'utf8')).sources:[];
const queue=[...orders.map(order=>({order,state:'queued'})),...previous.filter(x=>!orders.includes(x.order))];
function status(){const completed=queue.filter(x=>x.state!=='queued').length;const value={state:completed===queue.length?'complete':'running',title:'背景取回Gemini對話與原圖',updatedAt:new Date().toISOString(),completed,total:queue.length,sources:queue};const file=path.join(ROOT,'monitor/gemini-acquisition.json');fs.writeFileSync(file+'.tmp',JSON.stringify(value,null,2)+'\n');fs.renameSync(file+'.tmp',file);}
status();
const months = {January:1,February:2,March:3,April:4,May:5,June:6,July:7,August:8,September:9,October:10,November:11,December:12};
function createdDate(line) {
  const match = line.match(/([A-Z][a-z]+) (\d{1,2}), (\d{4}) at/);
  const month = match && (months[match[1]] || Object.entries(months).find(([name])=>name.slice(0,3)===match[1])?.[1]);
  return match && month ? `${match[3]}-${String(month).padStart(2,'0')}-${match[2].padStart(2,'0')}` : '';
}
(async()=>{
  const browser = await chromium.launch({headless:true,args:['--no-sandbox']});
  const context = await browser.newContext({locale:'en-US',timezoneId:'Asia/Taipei',viewport:{width:1440,height:1000}});
  try {
    for (const order of orders) {
      const current = JSON.parse(fs.readFileSync(progressFile,'utf8')).sources[order-1];
      if (!current || !/^https:\/\/(?:share\.gemini\.google\/|gemini\.google\.com\/share\/)[A-Za-z0-9]+$/.test(current.url)) throw Error('Invalid source order/URL');
      const key = current.url.split('/').pop();
      const page = await context.newPage();
      let archive, downloaded=[], errors=[];
      try {
        await page.goto(current.url,{waitUntil:'domcontentloaded',timeout:45000});
        await page.waitForFunction(()=>document.body.innerText.includes('Created with')||/\b[A-Z][a-z]+ \d{1,2}, \d{4} at \d{1,2}:\d{2}/.test(document.body.innerText),{timeout:30000});
        await page.waitForFunction(()=>document.querySelector('message-content') || document.body.innerText.length>1000,{timeout:30000});
        const result = await page.evaluate(async()=>{
          const seen = new Map();
          const collect=()=>{for(const im of document.images){const src=im.currentSrc||im.src;if(src&&/Uploaded image/i.test(im.alt)&&!seen.has(src))seen.set(src,{src,alt:im.alt,width:im.naturalWidth,height:im.naturalHeight});}};
          collect();
          const candidates=[...document.querySelectorAll('*')].filter(e=>e.clientHeight>200&&e.scrollHeight>e.clientHeight+100&&/auto|scroll/.test(getComputedStyle(e).overflowY));
          const scroller=candidates.sort((a,b)=>b.scrollHeight-a.scrollHeight)[0]||document.scrollingElement;
          const top=scroller.scrollTop;
          for(let y=0;y<scroller.scrollHeight;y+=700){scroller.scrollTo(0,y);await new Promise(r=>setTimeout(r,90));collect();}
          scroller.scrollTo(0,top);
          return {title:document.title,text:document.body.innerText,images:[...seen.values()],allImageMetadata:[...document.images].map(im=>({alt:im.alt,width:im.naturalWidth,height:im.naturalHeight})),finalUrl:location.href};
        });
        const headerLines=result.text.split('You said')[0].split('\n');
        const createdLine=headerLines.find(t=>!t.startsWith('Published ')&&/[A-Z][a-z]+ \d{1,2}, \d{4} at /.test(t))||'';
        const publishedLine=result.text.split('\n').find(t=>t.startsWith('Published '))||'';
        archive={url:current.url,...result,createdDisplay:createdLine,createdDate:createdDate(createdLine),publishedDisplay:publishedLine,fetchedAt:new Date().toISOString()};
        fs.writeFileSync(path.join(ROOT,`docs/sources/gemini-${key}.json`),JSON.stringify(archive,null,2)+'\n');
        for (let index=0;index<result.images.length;index++) {
          const im=result.images[index];
          try {
            const originalUrl=new URL(im.src);
            if(originalUrl.hostname.endsWith('googleusercontent.com'))originalUrl.pathname=originalUrl.pathname.replace(/=(?:w|s)\d+[A-Za-z0-9_-]*$/,'')+'=s0';
            const response=await context.request.get(originalUrl.href,{timeout:20000});
            if(!response.ok())throw Error('HTTP '+response.status());
            const raw=await response.body();
            const ext=raw[0]===255&&raw[1]===216?'.jpg':raw.subarray(0,4).equals(Buffer.from([137,80,78,71]))?'.png':raw.subarray(0,4).toString()==='RIFF'?'.webp':null;
            if(!ext)throw Error('Not an image');
            const relative=`docs/source-pages/gemini-${key}-${index+1}${ext}`;
            fs.writeFileSync(path.join(ROOT,relative),raw);
            const dimensions=execFileSync('ffprobe',['-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',path.join(ROOT,relative)],{encoding:'utf8'}).trim().split(',').map(Number);
            downloaded.push({path:relative,sha256:crypto.createHash('sha256').update(raw).digest('hex'),bytes:raw.length,renderedWidth:dimensions[0],renderedHeight:dimensions[1],downloadVariant:'original_size_s0'});
          } catch(error) {errors.push({index:index+1,error:error.message});}
        }
      } catch(error) {errors.push({error:error.message});try{const text=await page.locator('body').innerText({timeout:5000});fs.writeFileSync(path.join(ROOT,`docs/sources/gemini-${key}-retry.json`),JSON.stringify({url:current.url,title:await page.title(),text,finalUrl:page.url(),checkedAt:new Date().toISOString(),errors},null,2)+'\n');}catch{}}
      finally {await page.close();}
      const progress=JSON.parse(fs.readFileSync(progressFile,'utf8'));
      const entry={...progress.sources[order-1]};
      if(archive){entry.title=archive.text.split('\n')[1]||archive.title;entry.archive=`docs/sources/gemini-${key}.json`;entry.archiveImages=archive.images.length;entry.createdDate=archive.createdDate;entry.createdDisplay=archive.createdDisplay;entry.publishedDisplay=archive.publishedDisplay;entry.downloadedImages=downloaded;entry.state=downloaded.length?'awaiting_transcription':archive.images.length?'awaiting_image_retry':'awaiting_text_review';}
      else entry.state='awaiting_source_retry';
      entry.errors=errors;entry.lastCheckedAt=new Date().toISOString();
      const result={batch:'gemini',order,url:entry.url,title:entry.title,state:archive?(downloaded.length===archive.images.length?'acquired':'partial'):'retry',checkedAt:entry.lastCheckedAt,createdDate:entry.createdDate,createdDisplay:entry.createdDisplay,archive:entry.archive,imagesExpected:archive?.images.length??null,downloadedImages:downloaded,textLength:archive?.text.length??0,errors};
      const output=path.join(ROOT,`docs/acquisition/gemini-${String(order).padStart(3,'0')}.json`);fs.writeFileSync(output+'.tmp',JSON.stringify(result,null,2)+'\n');fs.renameSync(output+'.tmp',output);Object.assign(queue.find(x=>x.order===order),{state:result.state,title:entry.title,imagesAvailable:downloaded.length,imagesExpected:result.imagesExpected});status();
      console.log(JSON.stringify({order,title:entry.title,state:entry.state,created:entry.createdDate,images:downloaded.length,expected:entry.archiveImages,textLength:archive?.text.length,errors}));
    }
  } finally {await browser.close();}
})().catch(error=>{console.error(error.message);process.exit(1)});
