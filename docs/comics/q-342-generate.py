from pathlib import Path
import json,hashlib
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="b" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="#4d96af"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=10,c='#365b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="{c}">{z}</text>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eaf1ed","#f3eedf","#e9efdf"][i]}"/><g font-family="sans-serif">')
 if i<2:
  valley=i==0;t(90,16,'谷地：V 尖朝高處' if valley else '山脊：V 尖朝低處',11)
  t(90,32,'上方較高',9)
  for j,z in enumerate([300,200,100]):
   y=(45 if valley else 75)+30*j;edge=y+(30 if valley else -30)
   s.append(f'<path data-terrain="{"valley" if valley else "ridge"}" data-height="{z}" data-vertex="{o+90},{y}" data-edge-y="{edge}" d="M{o+30} {edge}L{o+90} {y}L{o+150} {edge}" fill="none" stroke="#a68f64" stroke-width="2"/>')
   t(18,edge+3,str(z),8,'#846a40')
  if valley:s.append(f'<path d="M{o+90} 38V150" stroke="#4d96af" stroke-width="3" marker-end="url(#b)"/>')
  else:
   for x in [40,140]:s.append(f'<path d="M{o+90} 81L{o+x} 125" stroke="#4d96af" stroke-width="2.5" marker-end="url(#b)"/>')
  t(90,165,'水沿谷地向下匯流' if valley else '水向兩側低處分流',10)
  t(90,178,'示例高度，非原圖實測數值',8)
 else:
  t(90,19,'回原圖判斷採樣條件',10)
  for y,z,c in [(35,'甲、乙、丁：較符合谷地','#d8e3ce'),(78,'丙：高地伸出的脊部','#e0d2b4'),(121,'最不可能直接採水：C','#c2d7ab')]:s.append(f'<rect x="{o+8}" y="{y}" width="164" height="31" rx="5" fill="{c}"/>');t(90,y+21,z,10)
  t(90,177,'脊部 ≠ 必在集水區之外',9)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-342.svg');a.write_text(''.join(s))
d={'id':'q-342','subject':'Geography','title':'看谷地匯流與山脊分流，找最不可能的採水點','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-342-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 河谷V形尖端朝上游高處','text':'原題註明支流未畫出，要靠等高線找可能的水道。配合高度判斷：谷地V形尖端指向上游高處，水流則往低處匯集。新圖的300、200、100是示例高度，不是原卷數值。','alt':'新精確概念等高線谷地V尖向上方高處，三線高度由300至100往下減少，藍箭頭沿谷線下流；不補畫原卷未載水道。'},
{'heading':'② 山脊向外凸出，水向兩側分流','text':'山脊的等高線凸出尖端伸向低處，與河谷的彎曲方向不同。水較容易向脊線兩側低處流走，脊部不是支流水集中的位置。不能只看形狀像V，還要讀高低方向。','alt':'新精確山脊概念線V尖朝下方低處，300至100往下減少，兩支藍箭頭由脊頂向兩旁低處，不畫脊頂有河流。'},
{'heading':'③ 丙在脊部，最不適合直接採支流水','text':'回到原圖，丙在613公尺高地向外伸出的脊部，甲、乙、丁則較符合谷地位置。因此問最不可能的採樣地點，選C丙。這不等於已證明丙整個地點不在水庫集水區內。','alt':'新判讀資訊卡比較甲乙丁谷地與丙脊部，選C；明確不推斷脊部一定在石門集水區外。'}],
'fourth':{'answer':'答案 C：丙','points':['先看等高線的高度，再辨認谷地或山脊。','谷地較能集中支流水，脊部向兩側分流。','不適合直接採支流水，不等於在集水區之外。']},
'protectedWords':['等高線','V形','上游高處','300','200','100','613公尺','甲、乙、丁','集水區','支流水'],
'originalChecked':{'images':['site/dist/assets/questions/q-342-reading-25048afbfc.jpg','site/dist/assets/questions/q-342-source-64c783965d.jpg'],'necessaryFigures':['site/dist/assets/questions/q-342-figure-8f1fe3d4ba.jpg'],'visualChecked':True,'answer':'C','notes':'親見完整共同說明支流未繪製、17四選與山圖613及丙脊部；沿已核對C，不重開既有原AI武斷集水區外的訂正。'},
'sourceUrl':'https://chatgpt.com/share/6ae05208-3ffc-83ee-be7e-99cc4705ab6d','answerCheckedAgainst':'原卷紅C，對比原圖613高地向外伸出脊部；谷V指高處、脊V指低處依高度圖模型獨立重算。',
'references':[{'title':'臺北市教學資源：表示地形的方法','url':'https://tmrc.tiec.tp.edu.tw/HTML/RSR200811191906220FM/topographytaiwan/tai07.htm','supports':'等高線同高與V谷尖指上游方向','access':'官方教育網站主文1至15行實讀'}, {'title':'NWCG Firefighter Math：Contour Lines and Intervals','url':'https://www.nwcg.gov/course/ffm/mapping/firefighter-math-55-contour-lines-and-intervals','supports':'谷線V向上游及山脊特徵','access':'官方搜尋摘錄，實開403，未冒稱全文'}],
'rationale':'以精確概念等高線對照水流方向，防把所有V都當河谷及由脊部推出集水區外。示例高度清楚標示，不用AI重畫原卷山形或虛構採樣水量。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'C','conceptElevations':[300,200,100],'valleyVertexPointsTo':'higher','ridgeVertexPointsTo':'lower','originalRidgeHeight':613,'watershedOutsideAsserted':False,'allValleysGuaranteedWet':False,'zValley':'450-(10/3)*y+(5/3)*abs(x-90)','zRidge':'550-(10/3)*y-(5/3)*abs(x-90)'},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
Path('docs/comics/q-342.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
