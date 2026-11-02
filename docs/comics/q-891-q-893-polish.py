import json
from pathlib import Path
from datetime import datetime,timezone
D=Path('docs/comics')
navy='#476c9b';green='#45a391';amber='#dca556';purple='#9b89b1';ink='#33475f'
head='''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><linearGradient id="paper" x2="1" y2="1"><stop stop-color="#fffdf6"/><stop offset="1" stop-color="#e9f0f4"/></linearGradient><linearGradient id="blue" x2="0" y2="1"><stop stop-color="#e9f1fc"/><stop offset="1" stop-color="#cfdef1"/></linearGradient><linearGradient id="mint" x2="0" y2="1"><stop stop-color="#dff3e9"/><stop offset="1" stop-color="#a7d8c8"/></linearGradient><filter id="shadow" x="-20%" y="-20%" width="150%" height="150%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#243c55" flood-opacity=".1"/></filter><marker id="down" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#bd8550"/></marker></defs>'''
def panel(x,body):return f'<g transform="translate({x} 0)"><rect width="360" height="360" fill="url(#paper)"/><rect x="14" y="14" width="332" height="332" rx="24" fill="#fff" opacity=".6"/>{body}</g>'
def line(x1,y1,x2,y2,c=ink,w=3,extra=''):return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" {extra}/>'
def rect(x,y,w,h,c,stroke=None,rx=12,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}" '+(f'stroke="{stroke}" stroke-width="3" ' if stroke else '')+extra+'/>'
def doc(x,y,c,scale=1):return f'<g transform="translate({x} {y}) scale({scale})">'+rect(0,0,27,36,'#fff',c,4)+line(7,10,20,10,c,2)+line(7,17,20,17,c,2)+line(7,24,16,24,c,2)+'</g>'
def save(i,svg,alts,rationale):
 art=D/'art'/f'q-{i}-polish.svg';art.write_text(head+svg+'</svg>')
 p=D/f'q-{i}.json';s=json.loads(p.read_text());s.update(art=str(art),generationMethod='new authored native SVG; exact relationships, HTML labels',styleReferenceIds=['q-153','q-154'],sourceGeneratedArtUsed=False,visualChecked=False,reworkedAt=datetime.now(timezone.utc).isoformat(),rationale=rationale)
 for k in ['rootReview','checkedAt','nativeArt','validationFile']:s.pop(k,None)
 for cell,a in zip(s['panels'],alts):cell['alt']=a
 s['diagramReview']={'sourceOriginalViewed':True,'noSVGText':True,'noInventedQuestionData':True,'colors':'甲/民事藍色，乙/告訴乃論綠色；其餘依題目HTML說明','note':'集合框面積及q891線高僅概念示意，q893長條依原表32/35/18/10比例繪製。'}
 p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
# q891: inclusion, remove the same subset, and compare the two lines.
a=rect(42,45,276,270,'url(#blue)',navy,24,'filter="url(#shadow)"')+rect(76,158,208,122,'url(#mint)',green,18)
a+=doc(80,80,navy)+doc(125,80,navy)+doc(170,80,navy)+doc(110,197,green)+doc(165,197,green)+doc(220,197,green)
b=rect(42,45,276,270,'url(#blue)',navy,24,'filter="url(#shadow)"')+rect(76,158,208,122,'none',green,18,'stroke-dasharray="7 7" opacity=".45"')+rect(76,209,208,71,'url(#mint)',green,18)+doc(110,225,green)+doc(165,225,green)
b+=doc(80,80,navy)+doc(125,80,navy)+doc(170,80,navy)+line(250,170,250,198,'#bd8550',4,'marker-end="url(#down)"')
c=''.join(line(46,y,315,y,'#dfe5ed',1) for y in [65,110,155,200,245,290])+line(46,48,46,301,ink,3)+line(46,301,315,301,ink,3)
for y,col in [(83,navy),(201,green)]:
 c+=line(66,y,275,y,col,4,'stroke-dasharray="7 7" opacity=".45"')+line(66,y+38,275,y+38,col,6)+line(295,y+2,295,y+33,'#bd8550',3,'marker-end="url(#down)"')
 for x in [84,159,246]:c+=f'<circle cx="{x}" cy="{y+38}" r="5" fill="{col}"/>'
save(891,panel(0,a)+panel(360,b)+panel(720,c),['藍色甲總集合包含綠色乙子集合；文件與框面積只示意包含關係。','保留藍色其他判決，綠色乙子集合減少；虛線顯示比較前範圍，不新增件數。','藍色甲與綠色乙的比較前位置用虛線、比較後用實線，兩者皆向下；非原卷實際月份統計。'],'件數題以集合包含、部分減少、兩條線同步下移的新製精確SVG呈現；新視覺採暖白底、藍綠層次與輕陰影，避免人物分散集合重點；不捏造原題數值。')
# q893: exact ratio bars from 32,35,18,10; stack 32+35; prosecution covers both criminal types.
a=''
for j,(n,col) in enumerate([(32,navy),(35,green),(18,amber),(10,purple)]):
 y=57+j*65;a+=rect(46,y,268,36,'#e9edf2',rx=9)+rect(46,y,268*n/35,36,col,rx=9,extra='filter="url(#shadow)"')
 a+=f'<circle cx="30" cy="{y+18}" r="5" fill="{col}"/>'
b=rect(40,66,280,48,'#f0f2f5',rx=12)+rect(40,66,280*32/67,48,navy,rx=0)+rect(40+280*32/67,66,280*35/67,48,green,rx=0)
b+=line(40,132,320,132,ink,3)+line(40,124,40,140,ink,3)+line(320,124,320,140,ink,3)
b+=line(106,159,106,187,navy,3)+line(253,159,253,187,green,3)+doc(92,207,navy,1.2)+doc(238,207,green,1.2)
# paired criminal classes lead into the same prosecution file; no implication of automatic prosecution.
c=doc(73,56,green,1.7)+doc(242,56,amber,1.7)+line(96,125,96,163,green,4)+line(265,125,265,163,amber,4)+line(96,163,180,200,green,4)+line(265,163,180,200,amber,4)
c+=rect(114,213,132,90,'url(#blue)',navy,14,'filter="url(#shadow)"')+line(140,235,219,235,navy,3)+line(140,251,219,251,navy,3)+line(140,267,199,267,navy,3)
save(893,panel(0,a)+panel(360,b)+panel(720,c),['四條由上到下藍綠橙紫長條，按原表甲32、乙35、丙18、丁10的精確比例，數字與類別見HTML。','藍色32與綠色35組成一條長條，兩段寬度按32比35計算，合計67見HTML。','綠色告訴乃論與橙色非告訴乃論兩種刑事案件皆可通往公訴途徑；是否起訴仍須符合法律要件。'],'統計題新製按32/35/18/10比例的四類長條及32+35堆疊條；第三格以分流圖顯示兩種刑事類別與公訴途徑，不以人物圖取代件數比較。全部精確數字保留HTML。')
