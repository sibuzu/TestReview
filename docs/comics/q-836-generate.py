from pathlib import Path
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
s = ET.Element(f'{{{NS}}}svg', width='540', height='180', viewBox='0 0 540 180', role='img', attrib={'aria-label': '區分單年水情與往年季節，枯水期累積至四月、五月六月梅雨之前'})
def e(tag, **attrs):
    return ET.SubElement(s, f'{{{NS}}}{tag}', {k.replace('_', '-'): str(v) for k, v in attrs.items()})
def text(x, y, value, size=12, color='#34584e', **attrs):
    node = e('text', x=x, y=y, text_anchor='middle', font_family='Noto Sans TC,Microsoft JhengHei,sans-serif', font_size=size, fill=color, **attrs)
    node.text = value
def box(x, y, w, h, color, stroke='#a8b8a3'):
    return e('rect', x=x, y=y, width=w, height=h, rx=7, fill=color, stroke=stroke)
def arrow(x1, y1, x2, y2):
    e('path', d=f'M{x1} {y1}L{x2} {y2}', stroke='#698e7b', stroke_width=2, fill='none', marker_end='url(#arr)')
defs=e('defs')
marker=ET.SubElement(defs,f'{{{NS}}}marker',id='arr',markerWidth='5',markerHeight='5',refX='4',refY='2.5',orient='auto')
ET.SubElement(marker,f'{{{NS}}}path',d='M0 0L5 2.5L0 5Z',fill='#698e7b')
for x, color in [(0,'#f5f8f0'),(180,'#faf4e8'),(360,'#f1f7f5')]:
    e('rect',x=x,y=0,width=180,height=180,fill=color)

text(90,20,'先分清題目問什麼',12)
box(17,33,146,43,'#e0edf5')
text(90,51,'2025 當次水情',12)
text(90,69,'供水樂觀',13)
arrow(90,81,90,97)
box(17,105,146,40,'#e9edda')
text(90,129,'問：往年何時吃緊？',11.5)
text(90,168,'單次穩定 ≠ 每年都穩定',10)

text(270,20,'枯水季累積到春末',12)
for i, month in enumerate([11,12,1,2,3,4]):
    x=190+i*26
    node=box(x,35,23,29,'#f6d7ac' if month==4 else '#eee8da','#ae8050' if month==4 else '#b9b3a5')
    node.set('data-month',str(month))
    text(x+11.5,55,str(month),12)
text(270,80,'常見枯水期：11月至翌年4月',9.5)
box(208,94,124,26,'#f3dfc7')
text(270,112,'少雨累積',12)
arrow(270,124,270,137)
box(190,143,160,25,'#eadcc7')
text(270,160,'蓄水壓力＋春季農業需水',10)

text(450,20,'4月在梅雨季之前',12)
box(374,39,59,60,'#f4dbb4','#b98c50')
text(403.5,69,'4月',23)
text(403.5,88,'枯水末段',10)
box(462,39,63,60,'#dcecf5','#7aa2b7')
text(493.5,65,'5–6月',15)
text(493.5,88,'梅雨季',12)
arrow(438,69,456,69)
box(382,115,136,29,'#e2ecd7')
text(450,135,'B：4月',15)
text(450,168,'季節性風險，不是每年必缺水',9.5)
Path('docs/comics/art/q-836-seasonal-risk.svg').write_text(ET.tostring(s,encoding='unicode')+'\n')
