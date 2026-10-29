from pathlib import Path
import hashlib,json
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,20,['不約而同：前後有反差','陽奉陰違：表裡有反差','其餘三項的關係不同'][i],10)
 if i<2:
  box(20,43,140,35,'#d7e6ca');txt(90,67,['沒事先約定','表面上服從'][i],14)
  txt(90,101,'卻',21,'#b4894c')
  box(20,116,140,35,'#d1e1e9');txt(90,140,['意見或行為相同','暗地裡違背'][i],13)
  txt(90,175,['沒有先約好，結果卻一致','不是接著做，而是反向轉折'][i],9)
 else:
  for yy,head,rel in [(38,'B 得寸進尺','得了還要更多：遞進'),(80,'C 有求必應','有請求就回應：條件'),(122,'D 曉風殘月','晨風＋殘月：並列')]:
   box(11,yy,158,35,'#f8f8f1');txt(90,yy+14,head,11);txt(90,yy+29,rel,9)
  txt(90,175,'要比較兩部分如何連接',10)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-390.svg';Path(art).write_text(''.join(s))
spec={'id':'q-390','subject':'Chinese','title':'加上「卻」改說，找出前後轉折','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-390-generate.py','startedAt':'2026-10-29T05:57:40.235227+00:00','panels':[{'heading':'① 不約而同：沒約定，結果卻相同','text':'題幹已解釋不約而同：彼此沒有先約好，意見或行為卻一致。把成語前後兩部分連成白話，會發現中間適合加「卻」，呈現前後的反差。','alt':'新原生沒事先約定/卻/意見行為相同兩卡，以中間卻突出題幹指定轉折，不新增人物事先談話。'},{'heading':'② 陽奉陰違：表面服從，暗裡卻違背','text':'「陽奉」是表面順從，「陰違」是暗中違背。兩部分方向相反，改說成表面服從、暗裡卻違背，就能看出轉折，因此A與題幹同類。','alt':'原生表面服從/卻/暗地違背對照，同一版型直觀對應題幹；不把陽陰錯當天氣或光線。'},{'heading':'③ 遞進、條件、並列，要分開判讀','text':'B得寸進尺，是得到後還想要更多，偏遞進；C有求必應，是有請求就回應，偏條件；D曉風殘月，是晨風與殘月兩個景物並列。它們都不是本題要找的前後轉折。','alt':'B遞進/C條件/D並列三卡分義，D晨風殘月是景物並列，不因兩景看似不同就判轉折。'}],'fourth':{'answer':'答案：A，陽奉陰違','points':['先把兩部分各自換成白話，再看連接關係。','不約而同：沒約定，卻相同。','陽奉陰違：表面服從，暗地卻違背。']},'protectedWords':['不約而同','陽奉陰違','陽奉','陰違','得寸進尺','有求必應','曉風殘月','前後轉折','遞進','條件','並列'],'rationale':'親見22題題幹定義/四選項與紅筆A，沿題幹指定轉折做兩部分語意比較。新原生同版型卻字關係圖/其餘三類別卡，更直接教結構判斷，避免人物情節隱含先約或把陰陽誤為天氣，無來源AI。','promptSummary':'原生三格：沒約定→卻→一致；表面服從→卻→暗違；B遞進/C條件/D並列分類。精確文字原生，關係清楚不以人物情節替代。','answerCheckedAgainst':'原卷22題明示不約而同為轉折、A陽奉陰違表裡相反；四選項完整核對，B更多/C請求回應/D兩景並列，沿A。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-390-source-00312f6043.jpg'],'visualChecked':True,'answer':'A','notes':'全部題幹定義/四選項親見，學生D與訂正A區分；按原題語意關係，不把兩部分不同就一概當轉折。'},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-390.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
