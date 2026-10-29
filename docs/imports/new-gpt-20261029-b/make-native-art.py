from pathlib import Path
from html import escape
import json
P=Path('docs/imports/new-gpt-20261029-b');D=Path('docs/comics/art')
def txt(x,y,s,size=13,fill='#29483e'):return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{fill}">{escape(s)}</text>'
def rect(x,y,w,h,fill='#d4e5c8'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}"/>'
def line(x,y,x2,y2,color='#63867e',width=2):return f'<path d="M{x} {y}L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none"/>'
def arrow(x,y,x2,y2):return line(x,y,x2,y2)+f'<path d="M{x2-5} {y2-4}L{x2} {y2}L{x2-5} {y2+4}" fill="none" stroke="#63867e" stroke-width="2"/>'
def make(qid,panels):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><style>text{font-family:"Noto Sans CJK TC","Noto Sans",sans-serif}</style>'
 for i,c in enumerate(panels):s+=f'<g transform="translate({i*200})">'+rect(1,1,198,198,'#f5f3e9')+c+'</g>'
 s+='</svg>';f=D/(qid+'.svg');f.write_text(s);return str(f)
arts={}
# Exact perimeter comparison: same total area, different fragmentation; not a map.
a=txt(100,20,'板塊交會的構造背景')+'<path d="M2 50L115 110L2 190Z" fill="#d3e3be"/><path d="M198 35L115 110L198 190Z" fill="#d5e7ed"/><path d="M2 50L115 110L198 35" fill="#ead8be"/>'+line(115,110,45,65)+line(115,110,175,58)+line(115,110,100,185)+txt(98,147,'島弧與群島',15)+txt(100,185,'構造概念，非實際板塊圖',10)
b=txt(100,20,'同面積，陸地分成多塊')+rect(20,55,60,60)+''.join(rect(x,y,30,30) for x,y in [(114,48),(156,48),(114,96),(156,96)])+txt(50,142,'1個大方塊',12)+txt(147,142,'4個小方塊',12)+txt(100,176,'示意面積相同；非真實島數',10)
c=txt(100,20,'把各島海岸全部加總')+rect(20,50,60,60)+''.join(rect(x,y,30,30) for x,y in [(114,44),(156,44),(114,91),(156,91)])+'<path d="M20 50h60v60H20Z M114 44h30v30h-30Z M156 44h30v30h-30Z M114 91h30v30h-30Z M156 91h30v30h-30Z" stroke="#b78546" stroke-width="3" fill="none"/>'+txt(50,145,'周長 240',12)+txt(149,145,'合計 480',12)+txt(100,177,'相同單位；幾何概念示意',10)
arts['q-853']=make('q-853',[a,b,c])
# Longitude relations and season duration without invented dates or rain amounts.
a=txt(100,20,'先找原圖甲、乙方位')+'<path d="M45 45L150 43L177 67L153 94L115 183L78 119L50 92Z" fill="#dce7ce" stroke="#9bad96"/>'+txt(61,68,'甲',22)+txt(151,68,'乙',22)+txt(44,40,'西北',11)+txt(164,40,'東北',11)+line(143,82,75,82)+txt(100,114,'乙 → 甲',15)+txt(100,190,'方位示意，非比例地圖',10)
b=txt(100,23,'西南季風影響的時間')+txt(20,69,'乙',16)+rect(39,50,145,25,'#a6cad7')+txt(110,68,'雨季較長',12)+txt(20,122,'甲',16)+rect(79,103,76,25,'#d3dfc2')+txt(117,121,'較短',12)+txt(100,171,'示意長短，不代表精確日數',10)
c=txt(100,23,'回圖例讀兩地雨量')+rect(30,52,50,103,'#83b0d2')+rect(122,125,50,30,'#e5ca8d')+txt(55,176,'乙較多',14)+txt(147,176,'甲較少',14)+txt(100,40,'不另編降雨數字',10)
arts['q-855']=make('q-855',[a,b,c])
(P/'native-arts.json').write_text(json.dumps(arts,indent=2)+'\n')
print(arts)
