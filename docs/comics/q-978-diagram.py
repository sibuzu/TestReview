from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
# Exact directional teaching diagrams; labels stay selectable in panel captions.
blue='#4d78a6';green='#439581';gold='#b99257';ink='#465c56'
head='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><linearGradient id="sand" x2="0" y2="1"><stop stop-color="#f3d895"/><stop offset="1" stop-color="#d9b776"/></linearGradient><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#b17640"/></marker></defs>'
def line(a,b,c,d,col=ink,w=3,extra=''):return f'<path d="M{a} {b}L{c} {d}" stroke="{col}" fill="none" stroke-width="{w}" stroke-linecap="round" {extra}/>'
def box(x,body):return f'<g transform="translate({x} 0)"><rect width="360" height="360" fill="#fcf9f0"/><rect x="14" y="14" width="332" height="332" rx="22" fill="#fffefb" stroke="#e8decb"/>{body}</g>'
# Basin cross section: no exact sea-level or slope claimed.
a='<path d="M35 101 C74 91 77 198 126 220 Q180 245 232 219 C285 198 288 91 325 101 L325 305 L35 305Z" fill="url(#sand)" stroke="#8c7854" stroke-width="4"/>'
a+=line(45,275,316,275,'#c29d68',2,'stroke-dasharray="6 7"')+line(64,90,124,185,'#b17640',4,'marker-end="url(#arr)"')+line(296,90,236,185,'#b17640',4,'marker-end="url(#arr)"')
# Exactly the three marked C contours, not full reconstruction of all original lines.
b=''
for rx,ry,cy,c in [(139,115,181,'#efdcad'),(103,81,189,'#cfdea9'),(65,48,197,'#9fc28c')]:b+=f'<ellipse cx="180" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}" stroke="#6d8766" stroke-width="3"/>'
b+=line(305,106,243,162,'#b17640',4,'marker-end="url(#arr)"')
# Equal-level shape alone is insufficient: compare inward rising/falling with profiles.
c='<rect x="28" y="50" width="304" height="110" rx="16" fill="#e7eff6"/><path d="M45 143 Q82 139 115 99 Q175 16 237 99 Q279 139 315 143" fill="#b6cfe0" stroke="#4d78a6" stroke-width="4"/>'
c+=line(72,137,132,93,blue,3,'marker-end="url(#arr)"')
c+='<rect x="28" y="192" width="304" height="110" rx="16" fill="#eef5e7"/><path d="M45 206 Q82 209 115 249 Q175 326 237 249 Q279 209 315 206 L315 296 L45 296Z" fill="#b8d6a7" stroke="#598464" stroke-width="4"/>'
c+=line(73,210,132,254,green,3,'marker-end="url(#arr)"')
art=Path('docs/comics/art/q-978-contours.svg');art.write_text(head+box(0,a)+box(360,b)+box(720,c)+'</svg>')
s=dict(id='q-978',subject='Geography',title='沙漠不是平原；向內降低才是盆地',art=str(art),layoutVersion='native-fluid-v6',panels=[dict(heading='① 先定位，再分清地形',text='甲位於大西洋東側、地中海南側的北非撒哈拉地區。本題配合教材的撒哈拉盆地概念；沙漠景觀不能直接當成平原。',caption='盆地剖面｜兩側高、中央低；箭頭表示由周圍往內降低。僅為輔助示意。',alt='盆地輔助剖面呈兩側高中央低，兩箭頭指向內部較低處；不表示甲的實測海拔。'),dict(heading='② 原圖C：數值向內降低',text='C已標示的等高線由外往內是2500、1500、500公尺。高度向內降低，形成周圍高、內部低的盆地。',caption='C俯視示意｜最外圈2500公尺、中圈1500公尺、最內圈500公尺；箭頭朝向內部低處。',alt='三條C標示高度的概念等高線：外圈2500、中圈1500、內圈500公尺；不重建原卷未標值的其他線。'),dict(heading='③ 比升降，不只比圈數',text='B由1200升到2400公尺，是內高外低；C由2500降到500公尺，才是盆地。選項數字並非甲地區的實測高程。',caption='上圖B｜往內升高；下圖C｜往內降低。剖面只比較方向，不按實際比例。',alt='上方B的山形剖面向中央升高，下方C的盆形剖面向中央降低，箭頭明示向內的升降方向。')],fourth=dict(answer='答案 C：外高內低的盆地',points=['C：2500 → 1500 → 500公尺，向內降低。','A低平；B、D都向內升高。','最內圈500公尺，不等於盆地最低點恰好500公尺。']),protectedWords=['撒哈拉地區','撒哈拉盆地','大西洋','地中海','等高線','公尺','盆地','實測高程','2500','1500','1200','2400'],sourceUrl='https://chatgpt.com/share/6aede186-c184-83ee-9f74-2d44b77d6587',originalMaterialsChecked=True,sourceGeneratedArtUsed=False,generationMethod='authored exact SVG contour/profile relationships plus selectable Chinese HTML captions',rationale='地形高低、等高線標高與升降方向是本題核心，以可校對SVG剖面及三條已標值等高線輔助；每格中文圖說直接標示圈位、值、單位與箭頭意義，不依顏色猜測，不沿用兩張錯AI圖。',editableDiagramScript='docs/comics/q-978-diagram.py',visualChecked=False,createdAt=datetime.now(timezone.utc).isoformat(),artSHA256=hashlib.sha256(art.read_bytes()).hexdigest(),geometryValidation={'contourDirections':{'B':[1200,1800,2400],'C':[2500,1500,500],'D':[100,300,500]},'unmarkedContourValuesInvented':False,'profilesConceptualNotScale':True,'labelsInSelectableHTML':True,'sourceAIUsed':False})
Path('docs/comics/q-978.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
