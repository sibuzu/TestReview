import json,math,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def t(x,y,v,z=16,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def ln(ps,c='#70877b',w=1.8,dash=''):s.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in ps)+f'" fill="none" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
for i in range(3):s.append(f'<rect x="{i*200+2}" y="2" width="196" height="196" rx="7" fill="#faf8ee" stroke="#bacbbb"/>')
t(100,23,'B：兩個90°＋兩側5',16)
ln([(36,55),(164,55),(164,135),(36,135),(36,55)],'#62869d',2.3)
ln([(36,65),(46,65),(46,55)],'#62869d',1.5);ln([(36,125),(46,125),(46,135)],'#62869d',1.5)
t(22,96,'5',21);t(179,96,'5',21)
t(100,165,'上下平行，距離為5',16)
t(300,23,'若右側斜接',18)
ln([(220,65),(380,65)],'#b9cbbd',1.5,'4 3');ln([(220,145),(380,145)],'#b9cbbd',1.5,'4 3')
ln([(238,145),(238,65)],'#62869d',2.8);ln([(238,145),(286,65)],'#b5824d',2.8)
ln([(238,75),(248,75),(248,65)],'#62869d',1.5)
t(223,108,'5',20,c='#557c97');t(262,51,'t',19)
ln([(238,45),(286,45)],'#9bad9c',1.5)
t(331,106,'斜接＞5',18,c='#a16c3e')
t(300,181,'已知長5，迫使t＝0',15)
t(500,23,'D的一個可能反例',17)
ln([(420,60),(537,60),(576,125),(420,125),(420,60)],'#a98255',2.4)
ln([(420,70),(430,70),(430,60)],'#a98255',1.5);ln([(420,115),(430,115),(430,125)],'#a98255',1.5)
t(478.5,47,'9',20);t(409,94,'5',20)
t(500,160,'只保證上下平行',17)
t(500,186,'右側沒有給定長度',15)
s.append('</svg>');Path('docs/comics/art/q-228.svg').write_text(''.join(s))
delta=5*math.cos(math.radians(89));H=5*math.sin(math.radians(89))
G={'A':{'TL':(0,H),'TR':(9,H),'BL':(delta,0),'BR':(9-delta,0)},'B':{'TL':(0,5),'TR':(8,5),'BL':(0,0),'BR':(8,0)},'C':{'TL':(0,H),'TR':(9,H),'BL':(delta,0),'BR':(11,0)},'D':{'TL':(0,5),'TR':(9,5),'BL':(0,0),'BR':(12,0)}}
def angle(g,a,v,b):
 u=[g[a][i]-g[v][i] for i in [0,1]];w=[g[b][i]-g[v][i] for i in [0,1]];return math.degrees(math.acos(max(-1,min(1,sum(u[i]*w[i] for i in [0,1])/(math.hypot(*u)*math.hypot(*w))))))
def sidecross(g):
 u=[g['BL'][i]-g['TL'][i] for i in [0,1]];w=[g['BR'][i]-g['TR'][i] for i in [0,1]];return u[0]*w[1]-u[1]*w[0]
vals={}
for name,g in G.items():
 v={'coordinates':g,'leftTopAngle':angle(g,'TR','TL','BL'),'leftBottomAngle':angle(g,'TL','BL','BR'),'leftLeg':math.dist(g['TL'],g['BL']),'rightLeg':math.dist(g['TR'],g['BR']),'upperBase':math.dist(g['TL'],g['TR']),'lowerBase':math.dist(g['BL'],g['BR']),'horizontalBasesParallel':g['TL'][1]==g['TR'][1] and g['BL'][1]==g['BR'][1],'legVectorCross':sidecross(g)};vals[name]=v
assert all(abs(vals[k]['leftLeg']-5)<1e-9 for k in vals)
assert all(abs(vals[k]['leftTopAngle']-89)<1e-8 and abs(vals[k]['leftBottomAngle']-91)<1e-8 for k in ['A','C'])
assert abs(vals['A']['rightLeg']-5)<1e-9
assert all(abs(vals[k]['leftTopAngle']-90)<1e-8 and abs(vals[k]['leftBottomAngle']-90)<1e-8 for k in ['B','D'])
assert abs(vals['B']['rightLeg']-5)<1e-9
assert all(abs(vals[k]['legVectorCross'])>1e-6 for k in ['A','C','D'])
assert abs(vals['B']['legVectorCross'])<1e-9
Path('docs/comics/q-228-geometry-validation.json').write_text(json.dumps({'id':'q-228','counterexampleOnly_A_C_D_NotOriginalExtraData':True,'B_exampleWidth8_NotGiven':True,'optionChecks':vals,'B_generalProof':'rightSideSquared=5²+t² and rightSide=5 implies t²=0, so t=0','hypothesisDiagramOnly':{'parallelLineGap':5,'drawnHorizontalOffset_NotGiven':3,'slantedLength':math.sqrt(34),'slantedLengthGreaterThan5':True},'D_displayScaleIsotropic':13,'independentAllGivenConstraintsPass':True},ensure_ascii=False,indent=2)+'\n')
x={'id':'q-228','subject':'Math','title':'B的條件迫使右側垂直，其餘用反例檢查','art':'docs/comics/art/q-228.svg','protectedWords':['90°','89°','91°','平行四邊形','長方形','等腰梯形','直角梯形','充分條件','畢氏定理'],'panels':[{'heading':'① B的兩個90°，先得到上下平行','text':'左側同時垂直上邊與下邊，所以這兩邊平行。左側長5，兩平行線的距離就是5；B又給右側長5，這個等長條件要一起用。','alt':'B畫符合條件的矩形，左上左下兩直角標記、左右皆5；未把未給的上邊長度9移入B，右側直角結論由下一格論證。'},{'heading':'② 斜接會超過5，因此右側必須垂直','text':'若右側上下端點有水平差t，依畢氏定理，長度平方等於5²加上t²。已知右側也長5，只能t＝0。因此四角都是直角，B一定是長方形，也是平行四邊形。','alt':'假設右側斜接的輔助圖，垂直距離5、水平t，斜邊明標大於5；不把非零t的斜邊錯標5。原條件長5迫使t為0。'},{'heading':'③ 其餘圖仍可能是梯形，不能只靠目測','text':'A的89°與91°只保證上下平行，兩腿等長仍可能是等腰梯形。C、D缺少右側限制；圖中D的直角梯形反例，就符合左側5、上邊9與兩個90°。','alt':'D精確反例上邊9、左邊5、左兩角90，右側斜接且長度未給；未把反例底邊12當原題新增條件，A/C反例另存驗算。'}],'fourth':{'answer':'答案 B：給定條件足以判成長方形','points':['兩直角確定上下平行，相距5。','右側也長5，必垂直，形成長方形。','其餘條件容許非平行四邊形反例，不能目測補條件。']},'rationale':'實看4-3第1題完整四幅原卷條件（C也有89/91）及givenSVG，讀來源1574–1587判B摘要，獨立用畢氏排斜接。另逐項精確構造A等腰梯形左89/91雙腿5、C左89/91左5上9斜右、D左90/90左5上9斜右，三者均符合已知卻左右不平行。新SVG B條件/假設斜接長>5/D反例，不誇大89°成別的角；B答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-228-source-3737014927.jpg','site/dist/assets/questions/q-228-given.svg (all exact option conditions read)','site/dist/sources/gemini-GD2msWyGjhx0.txt lines 1574–1587'],'sourceUrl':'https://share.gemini.google/GD2msWyGjhx0','generationMethod':'precise native SVG sufficient-condition rectangle, hypothetical oblique segment and a validated right-trapezoid counterexample','answerCheckedAgainst':'B平行線距5且右線段5→水平差0→矩形；A/C/D皆有精確非平行四邊形反例符合原給邊角，B唯一足以判定。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-228.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
