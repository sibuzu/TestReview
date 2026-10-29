// Comic layout QA uses an isolated, mocked Demo session and never a real token.
exports.installTestSession=async page=>{
 await page.addInitScript(()=>localStorage.setItem('weirugo:session:v1',JSON.stringify({user:'demo',token:'d'.repeat(64)})));
 await page.route('**/.netlify/functions/session',route=>route.fulfill({status:route.request().method()==='OPTIONS'?204:200,headers:{'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Authorization, Content-Type','Access-Control-Allow-Methods':'GET, POST, DELETE, OPTIONS','Content-Type':'application/json'},body:route.request().method()==='OPTIONS'?'':JSON.stringify({user:'demo'})}));
};
