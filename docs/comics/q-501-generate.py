from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="a" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0 0L4 2L0 4Z" fill="#7e9d90"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="#35564e">{z}</text>')
 def node(y,z,c='#d9e5ca',h=27,n=11):s.append(f'<rect x="{o+8}" y="{y}" width="164" height="{h}" rx="4" fill="{c}"/>');t(90,y+h*0.5+4,z,n)
 def arrow(y1,y2):s.append(f'<path d="M{o+90} {y1}V{y2}" stroke="#7e9d90" stroke-width="1.5" marker-end="url(#a)"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#f8f0e0","#ecf0ec"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,18,'黎且的計謀，先看目的',11)
  for y,z in [(34,'孔子治魯有成'),(83,'齊景公因此憂慮'),(132,'黎且獻計：使孔子離魯')]:node(y,z)
  arrow(62,80);arrow(111,129)
  t(90,177,'不是光明磊落地廣納人才',8)
 elif i==1:
  t(90,18,'原文實際敘述的連鎖結果',10)
  for j,z in enumerate(['送女樂給魯哀公','哀公樂之，怠於政','孔子進諫','哀公不聽','孔子離魯，前往楚國']):
   y=31+j*29;node(y,z,'#c4d8b3' if j==4 else '#e5ddc7',22,10)
   if j<4:arrow(y+23,y+27)
  t(90,178,'離去，不畫成被官兵強押出境',8)
 elif i==2:
  t(90,18,'用行為核對人物評語',11)
  for j,z in enumerate(['齊景公：排除，非納才','魯哀公：怠政，非自愛','孔子：進諫，非獨善','黎且：計謀達成 → D']):node(31+33*j,z,'#c4d8b3' if j==3 else '#e0e4d8',28,10)
  t(90,178,'計謀有效，不等於道德可取',8)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-501.svg');a.write_text(''.join(s))
d={'id':'q-501','subject':'Chinese','title':'按原文的目的與結果，核對人物評語','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-501-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 齊景公憂慮魯治，黎且要排除孔子','text':'孔子在魯國治理有成，齊景公卻感到憂慮。黎且出計策的目的是使孔子離開魯國，因此不能把齊景公說成光明磊落、廣納人才；要從文中行動看動機。','alt':'新精確目的鏈孔子治魯有成至齊景公憂慮至黎且獻計使孔子離魯，不額外推演重祿高位之字對象。'},
{'heading':'② 送女樂、君主怠政、進諫不聽、孔子離去','text':'原文寫黎且送女樂，魯哀公享樂而怠政；孔子進諫不被聽從，便離開前往楚國。把這條連鎖結果按順序連起來，就能看出黎且預想的排除孔子目的確實達成。','alt':'新精確五節點因果鏈依正文行動排序，不畫被官兵押逐，也不讓模型猜造女樂的16人精確隊伍。'},
{'heading':'③ D符合計謀達成，不是肯定計謀道德','text':'魯哀公沉迷而怠政，不是潔身自愛；孔子治理並進諫，也不是只顧獨善其身。黎且的計謀按預想實現，所以D符合本文。描述計謀有效，與讚許做法正當，是兩回事。','alt':'新原生四人物行為對照，D突出，將足智謀略的描述與道德肯定分開，不色情化女樂或虛構歷史肖像。'}],
'fourth':{'answer':'答案 D：黎且獻計，達成使孔子離去的目的','points':['先看計策的目的，再追蹤行為與結果。','魯君怠政，孔子進諫不聽後離去。','D描述謀略有效，沒有要求肯定其道德。']},
'protectedWords':['齊景公','黎且','孔子','魯哀公','女樂','潔身自愛','獨善其身','足智多謀','計謀達成','前往楚國'],
'originalChecked':{'images':['site/dist/assets/questions/q-501-reading-source-3c5037826e.jpg','site/dist/assets/questions/q-501-source-a0ecf1da25.jpg'],'visualChecked':True,'answer':'D','notes':'原35全段與註2/四項親見，原紅D；正文與註2為驕熒而不是現題庫驕矜，詳獨立review待確認，未改shared。原文孔子去而之楚不畫強制押逐。'},
'sourceUrl':'https://share.gemini.google/1P48K0fgDy6p','answerCheckedAgainst':'原紅D，依原文送女樂/樂之怠政/仲尼諫不聽/離魯之楚逐句獨立核，既有判答不重開。',
'rationale':'原文人物與計策包含多步因果，用精確目的及結果關係圖較人物演出更能防主客與順序混淆；不畫模糊16人隊伍，不暗示計謀達成即道德正確。',
'pendingReview':'docs/comics/q-501-original-ocr-review.json','pendingReason':'原卷驕熒恢復及原註2完整轉錄待使用者確認，D不變。四格刻意不引用誤字或未核的重祿高位白話對象。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'D','actualActionOrder':['送女樂','哀公樂之怠政','孔子進諫','不聽','孔子離魯之楚'],'moralApprovalImplied':False,'forcibleExpulsionInvented':False,'performerCountDecidedByImagegen':False,'misquotedCharacterRepeated':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-501.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
