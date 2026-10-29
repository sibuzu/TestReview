import json,hashlib,datetime
from pathlib import Path
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="arr" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#d3a245"/></marker></defs><rect width="1080" height="360" fill="#f5f8ef"/>']
def text(x,y,t,size=20,c='#435d52'):
 return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{c}" text-anchor="middle">{t}</text>'
def euglena(x,y,s=1,green=True,outline='#529276',features=False):
 r=f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -100C53 -88 70 35 0 108C-50 40 -47 -61 0 -100Z" fill="#e5efd4" stroke="{outline}" stroke-width="4"/><path d="M0 -100C8 -139 -48 -114 -35 -145C-17 -172 24 -146 20 -168" fill="none" stroke="{outline if not features else "#d69639"}" stroke-width="4"/><ellipse cx="-10" cy="-62" rx="7" ry="10" fill="{ "#d96c4d" if features else "#d8917e"}"/><ellipse cx="0" cy="10" rx="13" ry="16" fill="#ccd6d7"/>'
 for cx,cy,ang in [(-20,-27,-25),(21,-21,25),(-18,49,-25),(18,52,20)]:
  r+=f'<ellipse cx="{cx}" cy="{cy}" rx="8" ry="19" transform="rotate({ang} {cx} {cy})" fill="{ "#589a59" if green else "#bdcbb5"}"/>'
 return r+'</g>'
def plant(x,y,s=1,green=True,wall=False):
 r=f'<g transform="translate({x} {y}) scale({s})"><rect x="-47" y="-90" width="94" height="185" rx="13" fill="#f0ebd5" stroke="{ "#ba8b49" if wall else "#8b9c71"}" stroke-width="{9 if wall else 5}"/><rect x="-39" y="-82" width="78" height="169" rx="9" fill="#e6efd9" stroke="#75a68b" stroke-width="2"/><rect x="-21" y="-53" width="43" height="117" rx="16" fill="#d7e8eb"/><ellipse cx="25" cy="-7" rx="9" ry="12" fill="#ccd6d7"/>'
 for cx,cy,ang in [(-27,-60,0),(25,-58,0),(-28,21,0),(23,67,65),(-24,68,20)]:
  r+=f'<ellipse cx="{cx}" cy="{cy}" rx="7" ry="14" transform="rotate({ang} {cx} {cy})" fill="{ "#589a59" if green else "#bdcbb5"}"/>'
 return r+'</g>'
# Same organelle appears in both cells; illustrations are simplified, not to scale.
parts += [euglena(100,213,.77),plant(260,213,.77),text(100,328,'眼蟲'),text(260,328,'葉肉細胞')]
parts += ['<circle cx="180" cy="49" r="21" fill="#efd28a"/>','<path d="M164 75L111 123M197 75L253 126" stroke="#d3a245" stroke-width="3" marker-end="url(#arr)"/>']
# Distinguish flexible pellicle from a plant cell wall rather than drawing an imaginary wall on Euglena.
parts+=['<g transform="translate(360 0)">',euglena(100,213,.77,False,outline='#cf8367'),plant(260,213,.77,False,True),text(100,50,'表膜'),text(260,50,'細胞壁'),'<path d="M100 62L76 134M260 62L292 145" stroke="#967354" stroke-width="2" fill="none"/>',text(100,328,'眼蟲'),text(260,328,'葉肉細胞'),'</g>']
# The protruding flagellum and red eyespot are not miniature animal eyes or a plant common trait.
parts+=['<g transform="translate(720 0)">',euglena(184,218,.9,False,features=True),text(75,58,'鞭毛'),text(292,143,'眼點'),'<path d="M88 68L164 87M268 151L181 161" stroke="#bd8b53" stroke-width="2" fill="none"/>',text(182,340,'眼蟲局部特徵'),'</g></svg>']
p=Path('docs/comics/art/q-308.svg');p.write_text(''.join(parts))
spec={
'id':'q-308','subject':'Biology','title':'找共同特徵，要同時核對兩邊','art':str(p),
'protectedWords':['眼蟲','綠色植物','光合作用','葉綠體','細胞壁','表膜','鞭毛','眼點','原生生物界','植物界','葉肉細胞'],
'panels':[
{'heading':'① 共同點：葉綠體與光合作用','text':'本題的眼蟲有葉綠體，能利用光製造養分；綠色植物的葉肉細胞也有葉綠體。可行光合作用，正是A要比較的共同特徵。','alt':'原創簡化眼蟲與葉肉細胞結構，綠色橢圓表示葉綠體，日光箭頭指向兩者；非實際大小或葉綠體數量比例。'},
{'heading':'② 植物有細胞壁，眼蟲卻沒有','text':'B不能只看植物那一半。眼蟲的體表有表膜，並不是植物的細胞壁；圖中分別標出兩者的外層，避免把外形輪廓都當成細胞壁。','alt':'同樣兩個細胞分別標示眼蟲表膜與葉肉細胞厚細胞壁；簡化結構不畫眼蟲具有植物式細胞壁。'},
{'heading':'③ 眼蟲有的，不一定是共同點','text':'眼蟲會用鞭毛運動，眼點與對光的反應有關。但C、D說的是眼蟲的特徵，並非它與一般綠色植物共有的特徵。','alt':'眼蟲前端長鞭毛與紅色眼點示意，眼點不是視物的眼睛；不把鞭毛或眼點標成葉綠體。'}],
'fourth':{'answer':'答案 A：可行光合作用','points':['相似特徵，要在比較的兩邊都成立。','眼蟲沒有植物的細胞壁。','有植物相似特徵，不等於歸入植物界。']},
'rationale':'已實看第11題完整原卷、全部選項及作答附圖，讀取來源原對話相應段落；A與詳細解說一致。以全新程式結構SVG直接比較葉綠體、表膜/細胞壁和鞭毛眼點，比人物更能釐清B陷阱；不沿用來源AI圖。限本題具葉綠體眼蟲，不推成所有眼蟲皆能光合作用；五界歸屬採講義不改現代分類。',
'generationMethod':'original programmatic SVG simplified biological cell comparison','generatorFile':'docs/comics/q-308-generate.py',
'originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-308-source-2f53cb0d72.jpg','site/dist/assets/questions/q-308-figure-bf1b99b1e6.jpg','site/dist/sources/6ae0de73-5310-83ec-9332-f7f22d61959a.txt lines 228–295'],
'sources':[{'url':'https://milnepublishing.geneseo.edu/botany/chapter/euglena/','note':'SUNY Geneseo botany text, structure and energy sections; photosynthetic forms chloroplasts, flexible pellicle, some forms lack chloroplasts.'},{'url':'https://botit.botany.wisc.edu/botany_130/diversity/euglena-old/Euglena.html','note':'University of Wisconsin botany, pellicle not cell wall, one emerged flagellum, eyespot near anterior.'}],
'answerCheckedAgainst':'原卷四選項：A共同光合作用成立；B缺細胞壁，C/D非一般植物共有特徵。',
'visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},
'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artSha256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('docs/comics/q-308.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
