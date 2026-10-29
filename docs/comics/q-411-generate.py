from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 def line(x,y,xx,yy,col='#849d91',w=1.5,dash=''):s.append(f'<path d="M{o+x} {y}L{o+xx} {yy}" fill="none" stroke="{col}" stroke-width="{w}" {dash}/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,19,['先讀橫軸與縱軸','距離愈遠，原料運費愈高','100公斤原料 → 10公斤產品'][i],9)
 if i<2:
  line(37,125,157,125);line(151,122,157,125);line(157,125,151,128);line(37,125,37,35);line(34,41,37,35);line(37,35,40,41)
  s.append(f'<text x="{o+16}" y="81" text-anchor="middle" writing-mode="vertical-rl" font-size="10" fill="#244b50">原料運輸成本</text>')
  if i==0:
   txt(100,150,'原料產地與工廠距離',10);txt(98,83,'比較的是兩者關係',10);txt(90,175,'不把原料重量當成橫軸',9)
  else:
   line(50,116,143,46,'#789d5a',2.6)
   for x,y in [(65,105),(126,59)]:
    line(x,125,x,y,'#b9bcac',.9,'stroke-dasharray="2 2"');line(37,y,x,y,'#b9bcac',.9,'stroke-dasharray="2 2"');s.append(f'<circle cx="{o+x}" cy="{y}" r="3.5" fill="#ad824a"/>')
   txt(65,142,'近',9);txt(126,142,'遠',9);txt(89,109,'較低',9);txt(126,47,'較高',9);txt(90,175,'圖A：向右上升的正向關係',9)
 else:
  txt(90,39,'原料100公斤',11)
  for j in range(10):
   x=44+(j%5)*19;y=48+(j//5)*19;s.append(f'<rect x="{o+x}" y="{y}" width="15" height="15" rx="1" fill="#b5c998"/>')
  line(90,87,90,101);line(86,97,90,101);line(90,101,94,97)
  s.append(f'<rect x="{o+82}" y="109" width="15" height="15" rx="1" fill="#91b5c1"/>')
  txt(90,140,'產品10公斤',11);txt(90,158,'每一小格都代表10公斤',9);txt(90,176,'減重是線索；仍要回到坐標',9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-411.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-411-relation-validation.json').write_text(json.dumps({'originalXAxis':'原料產地與工廠距離','originalYAxis':'原料運輸成本','selectedRelation':'positive','twoIllustrativePoints':{'near':[65,105],'far':[126,59],'screenYIncreasesDown':True,'farCostHigher':True},'pointsAreQualitativeNotActualRates':True,'rawWeight':100,'productWeight':10,'unitWeight':10,'rawBlocks':10,'productBlocks':1,'noZeroCostOrActualSlopeAssumed':True,'modelScope':'其他條件相同的國中簡化區位模型，不把實際運輸計價一概視為固定線性費率。'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-411','subject':'Geography','title':'讀準坐標：原料產地愈遠，原料運費愈高','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-411-generate.py','startedAt':'2026-10-29T06:31:29.567067+00:00','panels':[{'heading':'① 橫軸是距離，縱軸是原料運費','text':'先讀清楚原圖坐標：橫軸是原料產地與工廠的距離，縱軸是原料運輸成本。本題要比較的是距離改變時的原料運費，不是把100公斤與10公斤直接畫到這兩軸上。','alt':'新原生精確讀軸示意，橫距離縱原料運費，沒有把原料/產品重量錯當座標量。'},{'heading':'② 其他條件相同，向右就應往上','text':'依本題的簡化模型，原料重量、運輸方式等條件相同時，距離愈遠，原料運費愈高。因此應選向右上升的A；B下降、C不變，都不合這個關係。','alt':'新精確定性正向線與近低/遠高兩點、虛線對軸，沒有數字費率或必定零成本原點假設。'},{'heading':'③ 大幅減重是線索，別忘本題在問什麼','text':'100公斤原料只製成10公斤產品，表示加工後重量大減。若只比較重量運輸負擔，靠近原料地能減少大量原料的長途運送；但選圖仍須回到原料運費與距離的關係。','alt':'10格原料與1格產品，每格10公斤精確等量，顯示100→10減重；不把格數當金錢或推無其他選址因素。'}],'fourth':{'answer':'答案：A，向右上升','points':['先確認兩軸的名稱，再判斷增減。','距離愈遠，原料運費愈高，是正向關係。','D垂直線不能表達距離改變時的運費關係。']},'protectedWords':['100公斤','10公斤','原料運費','原料產地','運輸方式','向右上升','正向關係','長途運送'],'rationale':'親見14完整題文與原卷四幅圖/必要細圖，沿已核對A（原AI前B後A已結案不重問）。精確坐標/定性兩點/等重量格圖能直接釐清坐標與減重資訊，原生SVG優於人物貨車，無來源AI、不宣稱實際費率線性。','promptSummary':'原生三格：只讀兩軸；A向右上升近低遠高；100→10等格重量比較。原圖四選項仍保持必要附圖，本新圖是推理解說非重製原卷。','answerCheckedAgainst':'原卷橫軸原料產地距工廠、縱軸原料運輸成本，四幅A上升/B下降/C水平/D垂直；100→10保持原數，本題同條件模型沿A。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-411-source-ccab60f9ac.jpg'],'necessaryFigures':['site/dist/assets/questions/q-411-figure-5861ae70c0.jpg'],'visualChecked':True,'answer':'A','notes':'原卷全題與四幅圖/軸名完整實看，原卷藍B紅A與已訂正詳解一致；新圖定性線沒有實際價格或保證完全過原點。'},'relationValidation':'docs/comics/q-411-relation-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-411.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
