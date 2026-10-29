from pathlib import Path
import hashlib,json
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['A偷換行為，B偷換狀態','C把外型誤當材質','D能由原文明確推出'][i],10)
 if i==0:
  for yy,a,b in [(38,'原文：德軍使用毒氣','A改成：德國發明面具'),(101,'原文：毒氣','B改成：固態毒素')]:
   box(10,yy,160,48,'#fafaf5');txt(90,yy+17,a,10);txt(90,yy+37,b,10,'#a47748')
  txt(90,174,'主體的行為、事物狀態要對準',9)
 elif i==1:
  box(17,40,146,36,'#d5e5c7');txt(90,55,'原文說的是外型',9);txt(90,71,'酷似豬鼻',16)
  txt(90,100,'≠',23)
  box(17,116,146,36,'#eedfbe');txt(90,131,'C說的是材質',9);txt(90,147,'用豬皮製作',14)
  txt(90,176,'長得像，不能直接推材料',10)
 else:
  box(17,39,146,36,'#d5e5c7');txt(90,54,'原文',9);txt(90,70,'廣泛應用到各個領域',11)
  s.append(f'<path d="M{o+90} 82v16m-4-4 4 4 4-4" fill="none" stroke="#7c9a9a" stroke-width="1.5"/>')
  box(17,109,146,38,'#d1e0e9');txt(90,125,'D',10);txt(90,141,'用途不限於戰場',14)
  txt(90,175,'沒有多加原文未說的資訊',9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-395.svg';Path(art).write_text(''.join(s))
spec={'id':'q-395','subject':'Chinese','title':'逐項比對：誰做什麼、外型、材質、用途','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-395-generate.py','startedAt':'2026-10-29T06:07:24.568725+00:00','panels':[{'heading':'① A、B先查主體行為與物質狀態','text':'原文說德軍使用毒氣，A卻改成德國發明防毒面具，使用者不等於發明者；B又把毒氣改成固態毒素，改動了物質狀態。兩項都沒有忠實保留原文資訊。','alt':'原生原文/選項雙列核對卡，A使用對發明、B毒氣對固態，無戰爭毒氣實驗或製造裝置。'},{'heading':'② C把像什麼，偷換成用什麼做','text':'「外型酷似豬鼻」只在說外觀相像，並沒有說面具用豬皮製成。外型與材質是兩種不同資訊，不能因為長得像，就自行補上製作材料。','alt':'新原生外型酷似豬鼻與材質豬皮兩分類卡中間不等號，避免新畫剝皮或把外型比喻當材質證據。'},{'heading':'③ D的不限戰場，有明確句子支持','text':'末句說面具「已被廣泛應用到各個領域」，可以直接推出用途不限於戰場，故D正確。本題是根據材料比對敘述，重點在有沒有原文支持。','alt':'原文廣泛各領域到D不限戰場的推論圖，不加原文未列的特定場所/用途或濾毒安全保證。'}],'fourth':{'answer':'答案：D，防毒面具已不限在戰場使用','points':['A換了行為：使用毒氣，不等於發明面具。','B換了狀態；C換了資訊類別：外型不是材質。','D有末句廣泛應用到各個領域直接支持。']},'protectedWords':['防毒面具','物質狀態','固態毒素','發明者','使用者','外型','材質','酷似豬鼻','廣泛應用','各個領域','不限於戰場'],'rationale':'親見完整材料含罐頭段與28四選項，獨立比對D末句、A主體行為/B狀態/C類別。此題重資訊類別核對，選新原生分類/不等號/原文推論圖，比再演戰場或豬泥土更直接且不誤教通俗故事為科學機制；不使用來源AI。','promptSummary':'原生三格：A使用對發明/B氣態對固態；C外型像對材質是；D原文明言廣泛各領域推不限戰場。精確文字與關係圖，不描毒物製造或實驗。','answerCheckedAgainst':'原卷整篇材料及28全部A-D；D末句有據，A使用偷換發明、B毒氣偷換固態、C外型偷換豬皮，沿已核定D，非獨立確認其發明史或泥土防護效力。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-395-reading-5ccda4cd21.jpg','site/dist/assets/questions/q-395-source-84f48b92b4.jpg'],'visualChecked':True,'answer':'D','notes':'整篇包含戰爭/豬/面具及罐頭段與題28四項親見，僅依材料做閱讀，不引申實際防護建議或所有土壤可濾毒等規則。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-395.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
