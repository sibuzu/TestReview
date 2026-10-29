from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['A、C都差在聲調','B：兩字完整讀音相同','D：凌多一個介音ㄧ'][i],10)
 if i==0:
  for yy,head,a,b in [(40,'A：委／萎','ㄨㄟˇ','ㄨㄟ'),(103,'C：坷／苛','ㄎㄜˇ','ㄎㄜ')]:
   txt(90,yy,head,10);box(15,yy+7,68,30,'#dfebcf');box(97,yy+7,68,30,'#f2e2c5');txt(49,yy+28,a,15);txt(131,yy+28,b,15);txt(49,yy+51,'第三聲',9);txt(131,yy+51,'第一聲',9)
  txt(90,174,'不只比符號，也要比聲調',9)
 elif i==1:
  for xx,z in [(47,'偽'),(133,'為')]:
   txt(xx,58,z,26);box(xx-33,71,66,32,'#dbe8c9');txt(xx,93,'ㄨㄟˋ',17)
  txt(90,90,'＝',15);txt(90,126,'為國：替國家',12);txt(90,153,'都是第四聲',11);txt(90,174,'不同字，也可以同音',10)
 else:
  for yy,z,parts in [(62,'稜',['ㄌ','','ㄥ','ˊ']),(110,'凌',['ㄌ','ㄧ','ㄥ','ˊ'])]:
   txt(23,yy,z,20)
   for j,part in enumerate(parts):
    xx=52+29*j;box(xx-12,yy-20,25,30,'#f2dcb6' if part=='ㄧ' else '#dce6df');txt(xx,yy+1,part,17)
  txt(90,150,'ㄌㄥˊ ≠ ㄌㄧㄥˊ',13);txt(90,174,'同為二聲，仍不相同',10)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-510.svg';Path(art).write_text(''.join(s))
spec={'id':'q-510','subject':'Chinese','title':'同音要全對：聲調與介音都不能漏','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-510-generate.py','startedAt':'2026-10-29T05:31:49.627581+00:00','panels':[{'heading':'① A與C：聲調不同就不是同音','text':'「委」以重任讀ㄨㄟˇ，枯「萎」讀ㄨㄟ；坎「坷」讀ㄎㄜˇ，「苛」責讀ㄎㄜ。兩組都是第三聲對第一聲，所以A、C都不相同；一聲注音通常不另加聲調符號。','alt':'新原生兩組聲調比較卡，A委三聲萎一聲、C坷三聲苛一聲，注音大字清晰且一聲不加虛構聲調符號。'},{'heading':'② B：偽造與為國，都讀ㄨㄟˋ','text':'「偽」造文書讀ㄨㄟˋ；「為」國爭光的「為」有替的意思，也讀ㄨㄟˋ。兩字的完整注音與第四聲相同，故選B；別把這裡的「為」讀成ㄨㄟˊ。','alt':'偽和為兩不同字搭同一ㄨㄟˋ讀音卡，以為國替國家語意核定本題多音字，不泛稱為所有語境都四聲。'},{'heading':'③ D：二聲相同，介音卻不同','text':'模「稜」兩可讀ㄌㄥˊ；「凌」虐讀ㄌㄧㄥˊ。「凌」的讀音多了介音ㄧ，雖然兩字都是第二聲，仍不能判成同音。','alt':'稜/凌注音逐格對齊，凌額外ㄧ以橙色框突出，兩字二聲均保留，明確是介音差異而非調號。'}],'fourth':{'answer':'答案：B，偽、為皆讀ㄨㄟˋ','points':['先看原題引號圈哪一字，再按詞語確認讀音。','A、C差聲調；D差介音ㄧ。','形似或同聲調，都不足以證明完全同音。']},'protectedWords':['ㄨㄟˇ','ㄨㄟˋ','ㄨㄟˊ','ㄌㄥˊ','ㄌㄧㄥˊ','ㄎㄜˇ','ㄎㄜ','枯萎','坎坷','苛責','模稜兩可','凌虐','介音ㄧ','為國爭光'],'rationale':'親見原卷12四選項，C引號在坷不是坎，沿已核對B不重開舊OCR。教育部簡編/成語典/小字典主文核聲調與介音。教學重點是精確音節對照，因此新原生SVG注音大字卡/聲調對照/ㄧ差異，比人物或文字生圖更準確；無來源AI。','promptSummary':'原生三格精確注音：A/C三聲與一聲卡；B偽/為皆ㄨㄟˋ及替義；D逐格對齊ㄌ[空]ㄥˊ與ㄌㄧㄥˊ，介音ㄧ高亮。','answerCheckedAgainst':'原卷四選項與紅筆B；官方枯萎18550、坎坷18423、苛責17936、模稜成語612、凌虐65485、偽小字典D0002926及為D0002104，逐字語境核音。','officialReferences':[{'title':'教育部簡編本・枯萎','url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=18550&la=0&powerMode=0'},{'title':'教育部簡編本・坎坷','url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=18423&la=0&powerMode=0'},{'title':'教育部簡編本・苛責','url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=17936&la=0&powerMode=0'},{'title':'教育部成語典・模稜兩可','url':'https://dict.idioms.moe.edu.tw/idiomView.jsp?ID=612&webMd=1'},{'title':'教育部重編本・凌虐','url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=65485&q=1&word=%E5%87%8C'},{'title':'教育部小字典・偽','url':'https://dict.mini.moe.edu.tw/SearchIndex/word_detail?wordID=D0002926'},{'title':'教育部小字典・為','url':'https://dict.mini.moe.edu.tw/SearchIndex/word_detail?wordID=D0002104'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-510-source-d24ec06c72.jpg'],'visualChecked':True,'answer':'B','notes':'四選項親見，C坷引用位置與枯萎/為國等語境已還原，學生C和紅筆B區分；無新增文字訂正或另開確認。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-510.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
