from pathlib import Path
import hashlib,json
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=180*i
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['炒：一部分表義，一部分表音','三：用符號表示數目','鮮：依本題常用分類'][i],9)
 if i==0:
  txt(90,75,'炒',46);box(12,92,68,51,'#f1dfb9');box(100,92,68,51,'#d3e2e9');txt(46,115,'火',21);txt(134,115,'少',21);txt(46,134,'表義',10);txt(134,134,'表音',10);txt(90,174,'形聲',15)
 elif i==1:
  txt(90,89,'三',60)
  for x in [63,90,117]:s.append(f'<circle cx="{o+x}" cy="116" r="5" fill="#a7bc89"/>')
  txt(90,144,'表示數量3',11);txt(90,174,'指事',15)
 else:
  txt(90,75,'鮮',46);box(12,92,68,51,'#dce7cb');box(100,92,68,51,'#dce7cb');txt(46,119,'魚',24);txt(134,119,'羊',24);txt(90,123,'＋',17);txt(90,157,'兩個部件合意',10);txt(90,177,'會意（本題分類）',12)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-422.svg';Path(art).write_text(''.join(s))
spec={'id':'q-422','subject':'Chinese','title':'三個字，分辨形聲、指事與會意','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-422-generate.py','startedAt':'2026-10-29T05:34:55.538752+00:00','panels':[{'heading':'① 炒：火表義、少表音，是形聲','text':'炒的左邊「火」提示與用火烹調有關，右邊「少」是聲旁，歸形聲。不能看到火與少就解成少量的火，再把它誤判為兩部分都表義的會意字。','alt':'原生大字炒拆成火表義/少表音兩個異色部件卡，角色明確，不生圖寫錯字或當成少火會意。'},{'heading':'② 三：用三條橫畫指示數目','text':'「三」用三條橫畫表示數量三，屬指事。這是用符號直接表達數目，不是描畫某個具體物體的外形；不要只因字形簡單就把它判成象形。','alt':'原生標準字三和三個計數點，強調數量3與指事；不把橫畫畫成三根木棍來誤導象形。'},{'heading':'③ 鮮：按本題常用分類為會意','text':'本題依國中常用分類，將「鮮」從魚、羊合意，歸為會意。於是炒、三、鮮依序是形聲、指事、會意，恰有三種不同造字法，符合題目任務。','alt':'原生鮮及魚羊兩部件卡，明標本題常用分類，不宣稱唯一字源或炒三鮮菜餚必定含魚羊。'}],'fourth':{'answer':'答案：B，炒三鮮','points':['炒：形聲；三：指事；鮮：依本題歸會意。','A紅/燒、C雜/麵、D扒/雞，各有重複形聲。','任務是三種不同法則，不是三個字長得不同。']},'protectedWords':['形聲','指事','會意','聲旁','表義','表音','炒三鮮','魚、羊','紅/燒','雜/麵','扒/雞'],'rationale':'親見16題四選項與藍C紅B，沿既有詳解及本題常用分類限定，不把教材簡化當唯一字源。精確字形/部件角色是教學核心，選原生SVG而非人物/食物照片，避免把三鮮實際食材或少火會意誤解；無來源AI。','promptSummary':'原生三格字形：炒=火表義/少表音；三=數目符號；鮮=魚羊合意並明標依本題分類。所有文字可校對，不由imagegen生成漢字。','answerCheckedAgainst':'原卷紅筆B與現有已核對詳解。本題採常用六書分類炒形聲/三指事/鮮會意，題意與其他組重複形聲相符；官方鮮另有說文字源不作唯一化。','officialReferences':[{'title':'教育部筆順網・三（部首手冊指事舉例）','url':'https://stroke-order.learningweb.moe.edu.tw/dictMean.jsp?ID=19977&la=0'},{'title':'教育部異體字・鮮異體（另引說文從魚羴省聲）','url':'https://dict.variants.moe.edu.tw/dictView.jsp?ID=52301'},{'title':'教育部異體字・髹研訂（論炒改從少聲）','url':'https://dict.variants.moe.edu.tw/dictView.jsp?ID=76185'}],'manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-422-source-cc596f8722.jpg'],'visualChecked':True,'answer':'B','notes':'原題要求三種不同法則、四項菜名及紅筆B已親見，沿既有明示國中本題常用分類，不另改答案/正文或重開已有限定的字源分類。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-422.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
