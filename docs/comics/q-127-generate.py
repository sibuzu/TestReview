from pathlib import Path
import math,json,hashlib,datetime
A=(11*math.cos(math.radians(50)),11*math.sin(math.radians(50)));B=(0,0);C=(11,0);D=(A[0]-5,A[1]);E=(6*A[0]/11,6*A[1]/11);F=(4,0);T=(6,0);P=(A[0]+5/7*(F[0]-A[0]),A[1]*2/7)
pts=dict(A=A,B=B,C=C,D=D,E=E,F=F,T=T,P=P)
def dist(a,b):return math.dist(pts[a],pts[b])
def angle(a,b,c):
 u=[pts[a][i]-pts[b][i] for i in [0,1]];v=[pts[c][i]-pts[b][i] for i in [0,1]]
 return math.degrees(math.acos(sum(u[i]*v[i] for i in [0,1])/math.hypot(*u)/math.hypot(*v)))
checks={'ADE':angle('A','D','E'),'DEA':angle('D','E','A'),'EAC':angle('E','A','C'),'ACB':angle('A','C','B')};assert all(abs(v-65)<1e-8 for v in checks.values());assert abs(dist('A','P')/dist('A','F')-5/7)<1e-9
Path('docs/comics/q-127-geometry-validation.json').write_text(json.dumps({'coordinates':pts,'givenAngles':checks,'BE':dist('B','E'),'BF':dist('B','F'),'FC':dist('F','C'),'AD':dist('A','D'),'BT':dist('B','T'),'FT':dist('F','T'),'AP_over_AF':dist('A','P')/dist('A','F'),'AP_over_PF':dist('A','P')/dist('P','F'),'BC_order':['B','F','T','C'],'passed':True},ensure_ascii=False,indent=2)+'\n')
def xy(k):return(40+25*pts[k][0],292-25*pts[k][1])
def path(keys):return ' '.join(f'{xy(k)[0]},{xy(k)[1]}' for k in keys)
def line(keys,color='#536e62',w=3,dash=None,fill='none'):
 return f'<polyline points="{path(keys)}" fill="{fill}" stroke="{color}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def txt(x,y,t,size=20,color='#405c51'):
 return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{color}" text-anchor="middle">{t}</text>'
def labels(keys):
 offsets={'A':(9,-12),'B':(-12,20),'C':(10,20),'D':(-13,-11),'E':(-17,0),'F':(-6,22),'T':(10,22),'P':(16,-3)};r=[]
 for k in keys:
  x,y=xy(k);dx,dy=offsets[k];r += [txt(x+dx,y+dy,k)]
 return ''.join(r)
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><rect width="1080" height="360" fill="#f7f8f0"/>']
for panel in range(3):
 a += [f'<g transform="translate({360*panel} 0)">']
 if panel==2:
  a += [line(['A','D','P','A'],w=1,fill='#f2d4a5',color='#d6b37a'),line(['F','T','P','F'],w=1,fill='#b8d5bd',color='#94b79e')]
 a += [line(['A','B','C','A']),line(['A','D','E']),line(['E','P']),line(['A','F'])]
 if panel>=1:a += [line(['P','T'],color='#b9813d',dash='6 5')]
 if panel==0:
  a += [line(['A','B'],color='#779c56',w=5),line(['B','C'],color='#779c56',w=5),line(['A','D'],color='#c29149',w=5),line(['A','E'],color='#c29149',w=5),labels(['A','B','C','D','E','F','P']),txt(159,72,'5',22,'#ad772f'),txt(162,126,'5',20,'#ad772f'),txt(66,240,'6',20),txt(84,322,'4'),txt(236,322,'7'),txt(180,351,'AB＝BC＝11',19)]
 elif panel==1:
  a += [line(['B','T'],color='#6c9b73',w=6),line(['A','D'],color='#6c9b73',w=5),labels(['A','B','C','D','E','F','T','P']),txt(180,30,'AD ∥ BC',21),txt(166,279,'2',19,'#b77931'),'<path d="M40 329V335H190V329" fill="none" stroke="#6c9b73" stroke-width="2"/>',txt(111,356,'BT＝6',18)]
 else:
  a += [line(['A','D'],color='#bc853d',w=6),line(['F','T'],color='#659777',w=6),line(['A','P'],color='#bd8642',w=5),line(['P','F'],color='#659777',w=5),labels(['A','B','C','D','E','F','T','P']),txt(159,70,'AD＝5',19,'#a76f2e'),txt(173,279,'2',19,'#4d8061'),txt(180,344,'AP：PF＝5：2',21)]
 a += ['</g>']
a+=['</svg>'];art=Path('docs/comics/art/q-127.svg');art.write_text(''.join(a))
s={'id':'q-127','subject':'Math','title':'先補出對應邊，再換成部分比全長','art':str(art),'protectedWords':['AD∥BC','AB＝BC','AE＝AD＝5','BT＝BE＝6','FT＝2','AP：PF','AP：AF','5：2','5：7','等腰三角形','相似三角形','65°','115°','50°'], 'panels':[
{'heading':'① 兩個等腰三角形，求出AD','text':'△ABC中，A、C兩角都65°，所以AB＝BC＝4＋7＝11。扣掉BE＝6，得AE＝5。△ADE也有兩個65°，因此AE＝AD＝5。','alt':'依精確角度構造全圖，綠色AB與BC等長11，橙色AE與AD等長5；E在AB、F在BC、P為AF與DE交點。'},
{'heading':'② 角度推平行，延長DE到T','text':'∠DAE＝50°，所以∠DAC＝115°，與C角65°互補，得AD∥BC。延長DE交BC於T；△BET兩個角都是65°，故BT＝BE＝6，減BF＝4得FT＝2。','alt':'新輔助線DE延長段虛線至T；B、F、T、C的順序忠實標示，BT6不是BF4，AD與BC平行。'},
{'heading':'③ 相似先得兩段比，再合成全長','text':'△ADP與△FTP相似，AD對應FT，所以AP：PF＝5：2。題目要AP：AF；整段AF是5＋2＝7份，因此AP：AF＝5：7。','alt':'相似的ADP橙色、FTP綠色，AD5對應FT2，AP及PF分色；不把BF作相似對應邊。'}],
'fourth':{'answer':'答案 B：AP：AF＝5：7','points':['輔助點T是DE與BC的交點。','對應邊是AD與FT，不是BF。','5：2是AP：PF；題目要部分比全長。']},
'rationale':'依使用者重新製作幾何四格要求，實看原卷題幹及圖十三，讀取原對話補照後修正的完整解法。以新精確座標SVG分步著色；獨立構造B0 C11、AB11且B角50、AE5 AD5，驗四角65及BE6 BF4 FC7，DE交BC於T6，AP/AF5/7；保留B，不沿用來源AI圖。來源舊錯誤5/9已在補照後更正，本次不重開。','generationMethod':'programmatic SVG exact geometry three-step proof','generatorFile':'docs/comics/q-127-generate.py','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-127-source-6ae46440ff.jpg','site/dist/assets/questions/q-127-figure-source-1ac49e2af0.jpg','site/dist/sources/6ae05f86-8ce4-83ec-9e4e-ea3d50edbfd8.txt lines 412–572'],'answerCheckedAgainst':'坐標獨立驗四65°、各邊長及交點P，AP/AF=5/7，B。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artSha256':hashlib.sha256(art.read_bytes()).hexdigest()};Path('docs/comics/q-127.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
