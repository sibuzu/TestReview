// Isolated fixtures for group UI/reading-page QA. Never writes the real bank.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
function createGroupShadow(manifestPaths){
 const data=JSON.parse(fs.readFileSync(path.join(root,'site/dist/data.json'))),catalog={},groups=[];
 for(const input of manifestPaths){
  const manifest=JSON.parse(fs.readFileSync(path.resolve(root,input))),q=JSON.parse(fs.readFileSync(path.join(root,manifest.draftPath)));
  const members=manifest.questionIds,displayOrder=manifest.displayOrder||q.groupQuestions.map(child=>child.id);
  if(new Set(members).size!==members.length||!members.includes(q.id)||q.groupQuestions.length!==members.length)throw Error('Incomplete group fixture '+input);
  q.groupMetadata={...q.groupMetadata,groupId:manifest.groupId,retainId:q.id,originalQuestionIds:members,displayOrder};
  q.groupQuestions=displayOrder.map(id=>q.groupQuestions.find(child=>child.id===id));
  if(q.groupQuestions.some(child=>!child))throw Error('Missing displayed child');
  catalog[q.id]={members,displayOrder,revision:crypto.createHash('sha256').update(JSON.stringify([...members].sort())).digest('hex')};
  groups.push({question:q,manifest,input});
 }
 const memberIds=new Set(groups.flatMap(g=>g.manifest.questionIds));data.questions=[...data.questions.filter(q=>!memberIds.has(q.id)),...groups.map(g=>g.question)];
 const temporary=fs.mkdtempSync('/tmp/weirugo-group-shadow-');
 fs.symlinkSync(path.join(root,'site/dist/assets'),path.join(temporary,'assets'),'dir');
 for(const file of ['comic.css','comic-wrap.js','teaching-comic.js'])fs.copyFileSync(path.join(root,'site/dist',file),path.join(temporary,file));
 fs.writeFileSync(path.join(temporary,'data.json'),JSON.stringify({...data,questions:groups.map(g=>g.question)}));
 cp.execFileSync('python',[path.join(root,'site/scripts/build_review_page.py')],{env:{...process.env,WEIRUGO_DIST:temporary},stdio:'pipe'});
 return {data,catalog,groups,temporary,async install(page){
  await page.route(url=>url.pathname.endsWith('/data.json'),r=>r.fulfill({json:data}));
  await page.route(url=>url.pathname.endsWith('/question-group-data.js'),r=>r.fulfill({contentType:'text/javascript',body:'export const QUESTION_GROUPS = '+JSON.stringify(catalog)+';'}));
  for(const {question:q}of groups)await page.route(url=>url.pathname.endsWith('/'+q.id+'.html'),r=>r.fulfill({contentType:'text/html',body:fs.readFileSync(path.join(temporary,q.id+'.html'),'utf8')}));
 }};
}
module.exports={createGroupShadow};
