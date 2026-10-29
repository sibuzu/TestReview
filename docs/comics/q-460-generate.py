from pathlib import Path
import json,hashlib,datetime
p=Path('docs/comics/q-460.json')
if p.exists():
 b=Path('docs/comics/q-460-before-rework.json')
 if not b.exists():b.write_bytes(p.read_bytes())
def txt(x,y,t,size=22,c='#405c51'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{c}">{t}</text>'
def box(x,y,w,h,fill):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#8b9d85" stroke-width="2"/>'
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#ad8647"/></marker></defs><rect width="1080" height="360" fill="#f7f8ef"/>',txt(180,35,'加鹼先消耗H⁺'),box(36,72,288,65,'#e2eadd'),txt(180,113,'H⁺ ＋ OH⁻ → H₂O',25),'<path d="M180 145V204" fill="none" stroke="#ad8647" stroke-width="3" marker-end="url(#a)"/>',box(64,223,232,75,'#e4ecd7'),txt(180,270,'H⁺減少',28),txt(180,340,'判斷原平衡的擾動',20)]
a+=['<g transform="translate(360 0)">',txt(180,35,'向左移動的期間'),box(20,98,143,80,'#f1dea2'),txt(91,146,'CrO₄²⁻',25),box(197,98,143,80,'#f1c998'),txt(269,146,'Cr₂O₇²⁻',25),'<path d="M269 209H93" fill="none" stroke="#ad8647" stroke-width="5" marker-end="url(#a)"/>',txt(180,252,'黃色鉻酸根增加',21),box(34,281,292,54,'#e7eddc'),txt(180,317,'正反應速率 ＜ 逆反應速率',19),'</g>']
a+=['<g transform="translate(720 0)">',txt(180,35,'時間點不能混用')]
for y,label,symbol,fill in [(66,'原平衡','正＝逆','#e4eadb'),(157,'移動期間','正＜逆','#f0dfb6'),(248,'新平衡','正＝逆','#e4eadb')]:
 a += [box(34,y,292,65,fill),txt(180,y+26,label,19),txt(180,y+54,symbol,25)]
 if y<248:a += [f'<path d="M180 {y+67}V{y+86}" fill="none" stroke="#ad8647" stroke-width="2" marker-end="url(#a)"/>']
a+=['</g></svg>'];art=Path('docs/comics/art/q-460.svg');art.write_text(''.join(a))
Path('docs/comics/q-460-chemistry-validation.json').write_text(json.dumps({'acidBaseReaction':'H⁺+OH⁻→H₂O','balancedIonicEquationUsed':'2CrO₄²⁻+2H⁺⇌Cr₂O₇²⁻+H₂O','addedNaOH':'H⁺ decreases','shift':'left','duringShift':'forward rate < reverse rate','afterNewEquilibrium':'forward rate = reverse rate','correctOption':'D as already user confirmed','originalMolecularCoefficientIssue':'already resolved, not reopened','passed':True},ensure_ascii=False,indent=2)+'\n')
s={'id':'q-460','subject':'Physics-Chemistry','title':'向左移動是過程，新平衡再度等速','art':str(art),'protectedWords':['NaOH','OH⁻','H⁺','H₂O','鉻酸根','二鉻酸根','臨時約法','平衡向左','正反應速率','逆反應速率','正＜逆','正＝逆','CrO₄²⁻','Cr₂O₇²⁻'],'panels':[
{'heading':'① 加NaOH，先看H⁺怎麼變','text':'NaOH提供OH⁻，與H⁺形成水，使H⁺減少。採詳解已配平的淨離子式判斷，H⁺在左側；平衡會往補充H⁺的左方調整。','alt':'精確酸鹼中和H正加OH負生成水，指出H正減少，不沿用原卷未配平分子式作錯誤原子示意。'},
{'heading':'② 左移期間：逆反應較快','text':'向左調整時，逆反應速率較大，黃色鉻酸根增加。這就是D描述的變化過程；不是正反應較快，也不代表所有二鉻酸根完全消失。','alt':'二鉻酸根到鉻酸根方向箭頭向左，黃色鉻酸根增加，正反應速率小於逆反應速率；未畫定量濃度、速率數值或0.1公克必定完全轉化。'},
{'heading':'③ 到新平衡後，兩速率再次相等','text':'原平衡與最後的新平衡，都有正反應速率＝逆反應速率。A若指最後重新平衡也有道理；本題標準答案D，著重加鹼引起的移動期間。','alt':'三個時間點依序原平衡正等逆、移動期間正小逆、新平衡正等逆；等號不表示濃度相等，也不比較不同時間的速率絕對值。'}],
'fourth':{'answer':'標準答案 D：左移期間正＜逆，溶液偏黃','points':['先判加鹼使H⁺減少。','再判平衡左移，黃色鉻酸根增加。','到新平衡時正＝逆，不把D記成永遠如此。']},'rationale':'已實看原卷題幹、原印分子式、教用D及四選項，來源完整解析時點提醒已讀。使用者已確認D、A可描述最後狀態及原式係數訂正，本次全部維持，不重開同項；新製SVG只用已配平淨離子式、H正中和及三時間點流程，不沿用來源AI圖，不畫具體未知速率曲線或轉化量。','generationMethod':'programmatic SVG exact perturbation pathway and equilibrium time-state comparison','generatorFile':'docs/comics/q-460-generate.py','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-460-source-22b9f01117.jpg','site/dist/sources/6ae05f2b-7c7c-83e8-9959-f588a97ed563.txt lines 661–809','site/dist/data.json 使用者已確認D和時點/配平提醒'],'sources':[{'url':'https://chem.washington.edu/lecture-demos/chromate-dichromate-equilibrium','note':'華盛頓大學化學系：二鉻酸根加NaOH由橙向黃，方向核對。'}],'answerCheckedAgainst':'已確認D，平衡左移期間正小逆，黃色鉻酸根增加；新平衡恢復正等逆。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artSha256':hashlib.sha256(art.read_bytes()).hexdigest()};s['protectedWords'].remove('臨時約法');p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
