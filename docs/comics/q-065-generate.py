from pathlib import Path
import json,hashlib
G={'山崩':['甲'],'甲':['匯流'],'丙':['丁'],'丁':['匯流'],'匯流':['乙'],'乙':['下游'],'下游':[]}
seen=set();stack=['山崩']
while stack:
 a=stack.pop()
 if a in seen:continue
 seen.add(a);stack+=G[a]
affected=[z for z in ['甲','乙','丙','丁'] if z in seen];assert affected==['甲','乙']
R={'丙':(111,44),'丁':(116,79),'匯流':(87,92),'甲':(110,137),'乙':(43,120),'山崩':(131,158),'北源':(118,29),'下游':(24,146)}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="q065arr" markerUnits="userSpaceOnUse" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0L6,3L0,6" fill="#5f94a3"/></marker><marker id="q065mud" markerUnits="userSpaceOnUse" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0L6,3L0,6" fill="#ae8248"/></marker></defs>']
for i in range(3):
 o=i*180
 def txt(x,y,t,size=10,col='#244b50'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{col}">{t}</text>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#eff3e9","#edf1f7","#faf1e4"][i]}"/><g font-family="sans-serif">')
 txt(90,18,['河網示意：甲高，不是丙最高','泥沙只循甲的下游路徑','只圈下游經過的測站'][i],9)
 if i<2:
  for a,b in [('北源','丙'),('丙','丁'),('丁','匯流'),('山崩','甲'),('甲','匯流'),('匯流','乙'),('乙','下游')]:
   aa,bb=R[a],R[b];mud=i==1 and a in ['山崩','甲','匯流','乙'];col='#ae8248' if mud else '#5f94a3';s.append(f'<path d="M{o+aa[0]} {aa[1]}L{o+bb[0]} {bb[1]}" fill="none" stroke="{col}" stroke-width="{3 if mud else 1.5}" marker-end="url(#{"q065mud" if mud else "q065arr"})"/>')
  txt(24,40,'N',8);s.append(f'<path d="M{o+24} 58V44m-3 4 3-4 3 4" fill="none" stroke="#82968b"/>')
  for z in ['甲','乙','丙','丁']:
   x,y=R[z];mud=i==1 and z in affected;s.append(f'<circle cx="{o+x}" cy="{y}" r="4" fill="{("#ae8248" if mud else "#f9faf5")}" stroke="#537d85"/>')
   dx,dy={'丙':(-12,1),'丁':(12,3),'甲':(-13,4),'乙':(-12,-2)}[z];txt(x+dx,y+dy,z,10)
  txt(87,109,'匯流',8)
  if i==1:
   x,y=R['山崩'];s.append(f'<circle cx="{o+x}" cy="{y}" r="4" fill="#ae8248"/>');txt(151,153,'山崩',8)
  txt(90,176,['箭頭為水流；不按紙面上下猜','棕線：山崩 → 甲 → 乙'][i],9)
 else:
  for j,z in enumerate(['山崩：在甲上游','甲：先測到濁水','匯流：往較低處流','乙：下游也會測到']):
   yy=33+j*32;s.append(f'<rect x="{o+13}" y="{yy}" width="154" height="24" rx="4" fill="{("#d8e6c9" if j in [1,3] else "#f8f8f1")}"/>');txt(90,yy+17,z,11)
   if j<3:s.append(f'<path d="M{o+90} {yy+25}v5m-3-3 3 3 3-3" fill="none" stroke="#829990"/>')
  txt(90,176,'丙、丁不在這股濁水下游',9)
 s.append('</g>')
s.append('</svg>');art='docs/comics/art/q-065.svg';Path(art).write_text(''.join(s))
Path('docs/comics/q-065-topology-validation.json').write_text(json.dumps({'directedRiverGraph':G,'downstreamReachableFromLandslide':sorted(seen),'affectedStations':affected,'unaffectedStations':['丙','丁'],'highestStationFromOriginalContours':'甲','sketchStationCoordinates':R,'originalFigureVisualReferenceApproxPixels':{'甲':[247,266],'乙':[126,207],'丙':[225,90],'丁':[245,148],'匯流':[199,165]},'checks':{'directedReachability':True,'noReverseIntoOtherTributary':True,'northUpButNotHeightAxis':True},'note':'原生圖只保留原卷河網拓撲/大致方位，不重造等高線/精確標高/比例尺；海拔判斷仍依原卷圖。'},ensure_ascii=False,indent=2)+'\n')
spec={'id':'q-065','subject':'Geography','title':'從最高站甲向下游追：濁水經甲，再到乙','art':art,'artMode':'deterministic-svg','generatorFile':'docs/comics/q-065-generate.py','startedAt':'2026-10-29T06:17:19.927762+00:00','panels':[{'heading':'① 先讀等高線，找最高站甲','text':'原卷的等高線可用來比較各站海拔，最高的是甲。丙雖畫在較北的位置，北方並不等於高處。圖中簡化河網只用來追流向，海拔仍須回原卷等高線判讀。','alt':'新原生河網關係圖保持丙丁北側、甲東南、乙西南與中央匯流，北箭頭存在但不是海拔軸；不重造精確等高線。'},{'heading':'② 山崩在甲上游，泥沙先到甲','text':'題目把山崩放在最高測站的上游，所以濁水先經過甲，再順河道流到匯流處，接著到乙。棕色路線呈現這股泥沙向低處移動的路徑。','alt':'同一河網用棕色箭頭追山崩→甲→匯流→乙，甲乙測站填棕，另一丙丁支流保藍，不因甲在圖下方就畫錯水流。'},{'heading':'③ 丙、丁在另一支流，不會被逆流掃到','text':'丙、丁的河水流向匯流處，卻不在甲這股濁水的下游路徑。不能看到支流相接，就把全部測站都圈起來；依流向只圈甲、乙，因此選A。','alt':'原生單向流程卡把山崩/甲/匯流/乙排順序，丙丁排除；非濁水任意分向或所有連接點皆受影響。'}],'fourth':{'answer':'答案：A，甲、乙','points':['最高測站靠等高線判，不靠北方或紙面上下。','山崩在甲上游，濁水沿甲→匯流→乙走。','另一支流丙、丁不在這股濁水的下游。']},'protectedWords':['等高線','甲、乙','丙、丁','匯流處','最高測站','下游路徑','甲→匯流→乙'],'rationale':'親見32完整題幹/四選項及原卷圖七細圖/圖例公尺與站點，獨立沿甲東南→中央匯流→乙西南，丙丁另一支流核A。地理本題重精確河網拓撲和流向，新原生SVG比人物或AI地形更準確；另獨立有向圖可達性驗證，只示意不假造原圖標高/比例。無來源AI。','promptSummary':'新原生三格：原卷河網大致方位及箭頭；棕色山崩泥沙路徑只過甲乙；單向站點流程。保留北箭頭與圖非海拔軸提醒，不重製等高線。','answerCheckedAgainst':'原卷32最高站上游山崩條件及圖七等高線/河道/甲乙丙丁，甲最高，流經甲/乙而不逆入丙丁；獨立有向圖可達性只得甲乙，沿A。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-065-source-202f9b4507.jpg'],'necessaryFigures':['site/dist/assets/questions/q-065-figure-7844cff00f.jpg'],'visualChecked':True,'answer':'A','notes':'原卷全題四項與必要等高線細圖實看，原圖北箭頭/高度單位公尺/匯流站位核對，新圖僅拓撲教學，甲在畫面較南仍較高。'},'topologyValidation':'docs/comics/q-065-topology-validation.json','artSHA256':hashlib.sha256(Path(art).read_bytes()).hexdigest()}
Path('docs/comics/q-065.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
