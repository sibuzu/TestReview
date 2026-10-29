from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['原句的關鍵：始終不渝','C也強調真誠堅定的精神','比共同要旨，不比誰最有道理'][i],9)
 if i==0:
  for xx,z in [(37,'始'),(143,'終')]:box(xx-19,44,38,34,'#d4e4c4');txt(xx,68,z,22)
  s.append(f'<path d="M{o+57} 62H{o+123}m-5-4 5 4-5 4" fill="none" stroke="#75989a" stroke-width="2"/>')
  box(17,98,146,35,'#e6dcbf');txt(90,121,'不渝＝不改變',15);txt(90,155,'從開始到最後',11);txt(90,175,'意志堅定，不改初衷',11)
 elif i==1:
  box(14,40,152,36,'#d6e5c7');txt(90,63,'始終不渝 → 堅定',12)
  box(14,92,152,36,'#d3e0e9');txt(90,108,'精誠所至，金石為開',10);txt(90,122,'→ 真誠堅定，克服困難',9)
  txt(90,153,'相近的核心：堅定精神',11);txt(90,175,'比較意旨，不是字面重複',10)
 else:
  for j,(a,b) in enumerate([('A','助人成善'),('B','包容廣納'),('C','真誠堅定'),('D','謙抑不驕')]):
   yy=38+j*29;box(16,yy,148,23,'#d7e6c6' if a=='C' else '#f8f8f0');txt(90,yy+16,a+'：'+b,11)
  txt(90,174,'C與原句的精神最相近',11)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-387.svg';Path(art).write_text(''.join(s))
spec={'id':'q-387','subject':'Chinese','title':'名言比較先抓核心：始終不渝的堅定','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-387-generate.py','startedAt':'2026-10-29T05:51:34.979985+00:00','panels':[{'heading':'① 不渝是不改變，原句強調堅定','text':'「始終不渝」指從開始到最後都不改變，說明意志堅定。原句談偉大事業所需要的精神，所以先抓「堅定、不改初衷」這個核心，而不是只找與事業有關的句子。','alt':'原生始→終時間概念圖，延續同一準則，不渝明釋不改變，不加虛構時長或特定人生結局。'},{'heading':'② C的精誠，也在勉勵堅定的精神','text':'「精誠所至，金石為開」以真誠堅定的精神勉勵人克服困難，最能呼應原句。兩句都肯定堅定的精神，雖然用字不同，仍可以有相近的意旨。','alt':'新原生兩句核心對照卡，始終不渝→堅定，精誠所至→真誠堅定克服困難，不畫魔法裂石或保證任何事情一定成功。'},{'heading':'③ 其餘選項各有道理，主題卻不同','text':'A重成全善事，B重包容廣納，D重不恃才、不仗勢而驕。它們談的是其他可取的態度；題目要找與堅定精神最相近的一句，因此選C。','alt':'A助人成善/B包容廣納/C真誠堅定/D謙抑不驕四主題卡，C高亮，明示不是把其他良好態度判錯。'}],'fourth':{'answer':'答案：C，精誠所至，金石為開','points':['先將原名言濃縮成堅定、不改初衷。','再找各選項的共同核心，C最能呼應。','題目問最相近，不是選最有道理或最有名的一句。']},'protectedWords':['始終不渝','不改初衷','意志堅定','精誠所至','金石為開','真誠堅定','包容廣納','成全善事','不恃才','不仗勢'],'rationale':'親見15題原名言與A-D/手寫C，教育部成語典核始終不渝與精誠所至義。此題重在抽取共同要旨，新原生概念時間線/語義對照/四主題卡更直接呈現比較，不加人物情節或裂石神力，不用來源AI。','promptSummary':'原生三格語義：始→終且不改變；兩名言核心堅定對照；A-D不同態度分類，C最接近。','answerCheckedAgainst':'原卷始終不渝與四名言，官方始終不渝意志堅定/精誠所至勉勵誠心克難，沿已核對C，不另驗證題上伏爾泰歸屬為史實。','officialReferences':[{'title':'教育部成語典・始終不渝','url':'https://dict.idioms.moe.edu.tw/idiomView.jsp?ID=-116563&la=0&webMd=1'},{'title':'教育部成語典・精誠所至，金石為開','url':'https://dict.idioms.moe.edu.tw/idiomView.jsp?ID=9461&la=0&webMd=1'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-387-source-d4e79537cd.jpg'],'visualChecked':True,'answer':'C','notes':'15題原名言與四項完整親見，D不敖才原字不改，解釋按謙抑不恃才；不把B廣納與堅定混同。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-387.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
