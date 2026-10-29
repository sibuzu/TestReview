from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="a" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0 0L4 2L0 4Z" fill="#729b88"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="#34564d">{z}</text>')
 def r(x,y,w,h,c='#d5e3c8'):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e9","#f8efe1","#edf1e5"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'開頭：提出整體主張',11)
  s.append(f'<circle cx="{o+90}" cy="55" r="23" fill="#bfd4ad"/>');t(90,63,'合',24)
  s.append(f'<path d="M{o+90} 81V99" stroke="#729b88" stroke-width="2" marker-end="url(#a)"/>')
  r(9,105,162,46);t(90,124,'諷、直一也',13);t(90,143,'關鍵在如何運用',11)
  t(90,174,'是共同議題，不是第一個事例',8)
 elif i==1:
  t(90,18,'中段：兩例分說',11)
  r(69,30,42,28,'#d9c99e');t(90,50,'分',18)
  s.append(f'<path d="M{o+90} 58V69M{o+44} 79V69H{o+136}V79" fill="none" stroke="#729b88" stroke-width="2"/>')
  for x,z1,z2 in [(5,'伍舉進隱語','楚王淫益甚'),(98,'茅焦解衣危論','秦帝立悟')]:r(x,85,77,49,'#e6ddc8');t(x+38.5,105,z1,10);t(x+38.5,125,z2,10)
  t(90,158,'兩個不同事例，支持同一論點',9)
  t(90,176,'分說不等於只數人物數量',8)
 else:
  t(90,18,'結尾：回到運用之術',11)
  s.append(f'<circle cx="{o+90}" cy="55" r="23" fill="#bfd4ad"/>');t(90,63,'合',24)
  s.append(f'<path d="M{o+90} 81V99" stroke="#729b88" stroke-width="2" marker-end="url(#a)"/>')
  r(9,105,162,46);t(90,125,'顧用之之術何如耳',12);t(90,143,'再次重申共同立場',10)
  t(90,174,'首尾呼應：合 → 分 → 合',10)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-352.svg');a.write_text(''.join(s))
d={'id':'q-352','subject':'Chinese','title':'先總說、再舉例、回到主張：合分合','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-352-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 開頭提出看法，是合說','text':'從古今論諫開始，作者先提出共同議題，再說「諷、直一也」，關鍵在如何運用。這是統整全文的主張，尚未分別講伍舉、茅焦的事例，因此開頭是合。','alt':'新精確開頭合說圖，用共同立場諷直與運用之術承接合，不按句數將開頭拆成分。'},
{'heading':'② 中間舉兩個事例，是分說','text':'伍舉委婉進言，楚王反而更加荒淫；茅焦冒險直言，秦帝卻立刻醒悟。兩個事例分別論證：委婉或直接，不能先固定誰好誰壞，要看如何運用。這部分是分。','alt':'新精確並列雙事例：伍舉隱語與楚王淫益甚、茅焦危論與秦帝立悟，兩線互不相接，不混成同一君主或先後因果。'},
{'heading':'③ 末尾重申運用策略，又回到合說','text':'結尾說諷不宜一概讚許，直也不能輕易貶低，再次回到「顧用之之術何如耳」。它把兩例收回同一主張，形成首尾呼應；不是在末尾另加一個分說事例。','alt':'新精確結尾合說圖回到與開頭相同的運用之術，顯示首尾呼應合分合，不把原文諷不可盡與改成全不讚許。'}],
'fourth':{'answer':'答案 B：合 → 分 → 合','points':['合：提出共同議題與作者主張。','分：用伍舉、茅焦兩例分別論證。','合：再回到運用之術，重申立場。']},
'protectedWords':['古今論諫','諷、直一也','伍舉','茅焦','楚王','秦帝','顧用之之術何如耳','合說','分說','首尾呼應','運用策略'],
'originalChecked':{'images':['site/dist/assets/questions/q-352-reading-7143f9d8b0.jpg','site/dist/assets/questions/q-352-source-f2cb2814ab.jpg'],'visualChecked':True,'answer':'B','notes':'親見完整蘇洵原段/與諷少術四註及33四項結構，原B。兩次顧用之之術何如耳首尾照應；不改原文或額外認楚王秦帝確切歷史身份。'},
'sourceUrl':'https://chatgpt.com/share/6ae05238-7b84-83ec-b2f2-9a46aa7cb340','answerCheckedAgainst':'原卷B，按開頭總主張/兩人物例證/結尾重申逐段功能獨立標記，不以人物或句子數量判斷。',
'rationale':'論述結構題用精確開頭與末尾同款合說、中央並列雙例圖，比人物故事插畫直接呈現總分總，不混淆兩個例子為連續因果。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'B','structure':['合','分','合'],'examplePairs':[['伍舉進隱語','楚王淫益甚'],['茅焦解衣危論','秦帝立悟']],'examplesAreSequentialCausation':False,'openingAndClosingSharedPhrase':'顧用之之術何如耳','allObliqueAdviceBad':False,'allDirectAdviceGood':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-352.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
