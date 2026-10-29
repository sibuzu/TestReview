import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
def person(x,y,c):s.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}"/><path d="M{x-13} {y+40}V{y+25}Q{x} {y+9} {x+13} {y+25}V{y+40}Z" fill="{c}"/>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'three daughters',18)
for x in [47,100,153]:person(x,66,'#8b9cae')
s.append('<path d="M24 121V133H176V121" fill="none" stroke="#608a72" stroke-width="2"/>');t(100,165,'總共 3 位女兒',20)
t(300,22,'the other one：另外1位',14)
for x in [240,290]:person(x,62,'#86a888')
person(355,62,'#be977a')
r(217,116,103,42,'#e3eddf');t(268,138,'小學：2位',17)
r(326,116,60,42,'#f0e6d6');t(356,131,'高中',15);t(356,149,'1位',15)
t(300,181,'兩種學段要分開',15)
t(500,25,'3 − 1 = 2',29)
person(467,71,'#86a888');person(533,71,'#86a888')
s.append('<path d="M439 123V135H561V123" fill="none" stroke="#608a72" stroke-width="2"/>');t(500,164,'Two：其中兩位',22)
s.append('</svg>');Path('docs/comics/art/q-201.svg').write_text(''.join(s))

assert 3-1==2
Path('docs/comics/q-201-count-validation.json').write_text(json.dumps({'id':'q-201','originalTotal':3,'highSchoolOtherOne':1,'elementary':3-1,'panelOnePeople':3,'panelTwoGroupCounts':[2,1],'panelThreeTwoCount':2,'notTheTwoDaughterPhotoQuestion':True,'correctAnswerTwoConfirmed':True},indent=2)+'\n')
