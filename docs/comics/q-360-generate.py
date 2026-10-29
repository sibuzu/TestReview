from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def box(y,t,color='#dce8d0',size=11):s.append(f'<rect x="{o+12}" y="{y}" width="156" height="30" rx="5" fill="{color}"/>');txt(90,y+20,t,size)
 def line(x,y,xx,yy,col='#879f92',w=1.5):s.append(f'<path d="M{o+x} {y}L{o+xx} {yy}" fill="none" stroke="{col}" stroke-width="{w}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#edf2e8","#edf2f5","#faf1e4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  txt(90,18,'回原圖讀價格趨勢',10);line(31,130,159,130);line(31,130,31,41);txt(15,38,'價',9);txt(166,143,'年',9)
  points=[(41,119),(64,110),(90,101),(120,82),(149,47)]
  for (x,y),(xx,yy) in zip(points,points[1:]):line(x,y,xx,yy,'#78995d',2.5)
  for x,y in points:s.append(f'<circle cx="{o+x}" cy="{y}" r="2.5" fill="#a87e3e"/>')
  txt(47,148,'2006後',9);txt(145,148,'2012',9);txt(90,166,'大致上升，後段更明顯',10);txt(90,179,'趨勢示意，非數值重繪',8)
 elif i==1:
  txt(90,18,'B如何接到供給與價格？',10)
  for y,t in [(35,'若過捕使野生資源減少'),(88,'可取得的鰻苗供給減少'),(141,'其他條件相同，價格易升')]:
   box(y,t,size=10)
   if y<141:line(90,y+32,90,y+49);line(86,y+44,90,y+49);line(94,y+44,90,y+49)
 else:
  txt(90,18,'合理解釋 ≠ 證明唯一原因',10)
  for y,t in [(34,'A 本地搶購：題幹未說'),(73,'C 育種升質：沒有依據'),(112,'D 特定越界：圖無事件')]:box(y,t,'#f8f7ef',10)
  txt(90,165,'依原題野生苗情境選B',11);txt(90,179,'不把歷史目前當永久結論',8)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-360.svg';Path(art).write_text(''.join(s))
q={'id':'q-360','subject':'Geography','title':'野生苗供給減少，價格較可能上升','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-360-generate.py','layoutVersion':'native-fluid-v6','panels':[{'heading':'① 先看原圖：2006年後大致上升','text':'這是2004至2012年的鰻苗歷史價格圖。2006年後大致上升，2010至2012年升幅更明顯；判讀時先抓走勢，不把它當成今天的價格。','alt':'新製2006後上升且後段較快的定性趨勢線，不設金額刻度，明示非原數值重繪，原卷完整價格圖保留。'},{'heading':'② 苗源靠野生，資源減少會影響供給','text':'依題幹的野生苗供給設定，若長期過捕使資源減少，可取得的鰻苗就變少。在需求等其他條件大致相同時，價格較可能上升，因此B最合理。','alt':'新製過捕使野生資源減少到鰻苗供給減少再到同條件價格易升的條件鏈，若字及其他條件限制保留。'},{'heading':'③ 價格圖不是每種原因的證據','text':'題幹沒有臺灣民眾搶購、育種提升品質或特定越界事件的證據。B最合這個情境，但一張價格圖不能證明所有漲價都由過捕造成，實際仍可能受海況、需求等影響。','alt':'A搶購/C育種/D越界各缺文字證據的比較卡，不因漲價就斷言唯一資源原因或特定事件。'}],'fourth':{'answer':'答案 B：過捕使資源與鰻苗供給減少','points':['歷史圖讀上升趨勢，依原題野生苗情境推理。','供給減少、其他條件相同時，價格較易上升。','不把養成成魚等同人工繁殖，也不把原題目前當永久技術結論。']},'protectedWords':['2004至2012年','2006年','2010至2012年','鰻苗','歷史價格圖','野生苗','長期過捕','其他條件','供給減少','育種','越界事件','人工繁殖'],'originalChecked':{'images':['site/dist/assets/questions/q-360-source-216cf3c9d1.jpg'],'necessaryFigures':['site/dist/assets/questions/q-360-figure-b037552746.jpg'],'visualChecked':True,'answer':'B','notes':'親見40完整段落與四項及原2004至2012元/尾價格圖，2006低點後上升、2010後更快；B沿用，價格圖只作趨勢證據。'},'answerCheckedAgainst':'原題強調野生苗源且歷史價格上升，四項B的資源/供給縮減最符合；不新增實際鰻魚繁殖現況斷言、不以價格單獨證因果，沿既有技術時點限制。','rationale':'新定性歷史趨勢線、供給條件鏈與選項證據卡能直接呈現價格推理，精確文字HTML。圖不捏造年度金額，不沿用來源AI，也不讓人物捕魚圖暗示已證實過捕量。','sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'selected':'B','originalYears':[2004,2012],'newTrendChartHasActualPriceValues':False,'priceAloneProvesOverfishing':False,'currentTechnologyClaimAdded':False,'conditionalSupplyPriceRelation':True},'artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
D=json.loads(Path('site/dist/data.json').read_text());sid=next(x['sourceId'] for x in D['questions'] if x['id']=='q-360');q['sourceUrl']=next(x['url'] for x in D['sources'] if x['id']==sid)
Path('docs/comics/q-360.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
