from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['先分情況，不能混在一起','原文誤殺，與B的假裝有別','核對原文，不補寫處罰或程序'][i],9)
 if i==0:
  for yy,head,body in [(39,'私宰自己牲畜','依馬牛／駝騾驢分別規定'),(82,'病死後不申官就剝皮','文中仍有處罰'),(125,'故殺他人牲畜','另依種類規定處罰')]:
   box(12,yy,156,34,'#f9faf6');txt(90,yy+14,head,10);txt(90,yy+28,body,8)
  txt(90,176,'誤殺者不坐：不論罪',10)
 elif i==1:
  box(14,35,152,27,'#d8e6cb');txt(90,53,'不坐＝不論罪',13)
  for yy,t in [(77,'謊稱誤殺'),(110,'成功騙過官府，認定誤殺'),(143,'才可能免罪')]:
   box(12,yy,156,23,'#d2e1e9');txt(90,yy+16,t,10)
   if yy<143:s.append(f'<path d="M{o+90} {yy+24}v6m-3-3 3 3 3-3" fill="none" stroke="#809da0"/>')
  txt(90,177,'不是只要假裝就保證免罪',9)
 else:
  for yy,a,b in [(39,'A 申請程序','節錄沒有明寫這項資訊'),(82,'C 病死即剝皮','漏掉申官條件'),(125,'D 駱駝會流放','原文是杖一百')]:
   box(12,yy,156,35,'#f9faf6');txt(90,yy+14,a,10);txt(90,yy+29,b,9)
  txt(90,177,'依題文選B，補足其條件',10)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-392.svg';Path(art).write_text(''.join(s))
spec={'id':'q-392','subject':'Chinese','title':'B的關鍵：成功騙過官府後，才可能免罪','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-392-generate.py','startedAt':'2026-10-29T06:00:08.493259+00:00','panels':[{'heading':'① 先分自己、他人、故殺與誤殺','text':'節錄分別談私宰自己牲畜、病死後不申官就剝皮、故意殺他人牲畜，不能混成同一條。原文「誤殺者不坐」的「不坐」是指不論罪，不是不能坐下。','alt':'原生古文條件分類卡，不畫殺傷牲畜或刑罰執行，不將病死本身畫成犯罪；申官條件保留。'},{'heading':'② B的假裝，要補足成功欺瞞的條件','text':'B應補足條件：若能謊稱誤殺，並騙過官府，使官府信以為真正誤殺，就有可能依「誤殺者不坐」免罪。「有可能」不能省成只要假裝就必定免罪，原文也未允許假裝。','alt':'新原生條件鏈謊稱→成功騙過官府並被認定誤殺→才可能免罪，保留使用者已確認解釋，無欺瞞手法教學或保證免罪。'},{'heading':'③ A缺明文，C漏申官，D混淆刑罰','text':'A把具體申請程序補進節錄；C忽略病死後仍須申官，不能直接剝皮；D把文中的杖一百改成流放。逐項對回原文，不能看到處罰就把各種刑罰當成同一件事。','alt':'A具體程序未明寫/C申官條件不可漏/D杖一百非流放三對照，準確依古文不外推現行法。'}],'fourth':{'answer':'答案：B；須補足成功騙過官府、可能免罪','points':['真正誤殺的原文用語是誤殺者不坐。','B是假裝，須官府信以為真，才有可能被當作誤殺。','杖刑不是流放，病死後也不能漏掉申官。']},'protectedWords':['誤殺者不坐','不坐','不論罪','私宰','病死','不申官','故殺','杖一百','有可能','必定免罪','成功騙過官府'],'rationale':'親見24全文與四項及紅筆B；嚴格沿使用者已確認維持B與假裝=若謊稱並騙過官府才可能免罪，不重開已結案疑義。古文閱讀條件分層適合原生精確分類/條件鏈，不用暴力人物、動物圖或來源AI，不外推現行法律。','promptSummary':'原生三格古文分類/已確認B條件鏈/A-C-D對文，明確成功欺瞞才可能免罪，不描畫犯罪技巧或暴力。','answerCheckedAgainst':'使用者2026-10-28明確q392維持B及假裝語意補足；現已核對詳解與原卷誤殺者不坐，保留A/C/D既有判讀。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-392-source-35c0b4be26.jpg'],'visualChecked':True,'answer':'B（成功欺瞞後可能免罪的補足義）','notes':'全文/四選項親見，維持原題與B及已確認條件限制；古代節錄非現行刑事法律建議，沒有改教材或重開老師確認。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-392.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
