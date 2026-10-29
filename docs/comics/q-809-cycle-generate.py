from pathlib import Path
import json,math,hashlib,datetime
p=Path('docs/comics/q-809.json');b=Path('docs/comics/q-809-before-cycle.json')
if not b.exists():b.write_bytes(p.read_bytes())
s=json.loads(p.read_text());seq={k:[(start+10*i)%7 for i in range(6)] for k,start in zip('ABCD',range(4))};days=['一','二','三','四','五','六','日'];assert seq['C']==[2,5,1,4,0,3];assert [k for k,v in seq.items() if 6 not in v]==['C']
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#c28d42"/></marker></defs><rect width="1080" height="360" fill="#f7f8ef"/>']
def text(x,y,t,size=23,col='#405c51'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{col}">{t}</text>'
# Week positions, clockwise, starting Monday at top.
coords=[]
for i in range(7):
 t=-math.pi/2+2*math.pi*i/7;coords.append((180+112*math.cos(t),185+112*math.sin(t)))
a+=['<circle cx="180" cy="185" r="112" fill="none" stroke="#cbd5c5" stroke-width="3"/>',text(180,35,'一週循環')]
for i,(x,y) in enumerate(coords):
 selected=2<=i<=5;fill='#f1dab1' if selected else '#edf0e3';color='#b36e30' if selected else '#637e6b'
 a += [f'<circle cx="{x}" cy="{y}" r="24" fill="{fill}" stroke="{color}" stroke-width="2"/>',text(x,y+8,days[i],22,color)]
# Three separate clockwise edges: Wed→Thu→Fri→Sat, not a misleading shortcut equal to one day.
for i in [2,3,4]:
 t1=-math.pi/2+2*math.pi*(i+.24)/7;t2=-math.pi/2+2*math.pi*(i+.76)/7
 x1,y1=180+112*math.cos(t1),185+112*math.sin(t1);x2,y2=180+112*math.cos(t2),185+112*math.sin(t2)
 a += [f'<path d="M{x1} {y1}A112 112 0 0 1{x2} {y2}" fill="none" stroke="#c28d42" stroke-width="4" marker-end="url(#a)"/>']
a += [text(180,181,'10＝7＋3',20),text(180,211,'往後3天',20),text(180,344,'三 → 六',23)]
# All six visits and exactly five ten-day intervals.
a += ['<g transform="translate(360 0)">',text(180,35,'6次兌換，5個間隔',22)]
for i,d in enumerate(seq['C']):
 y=59+i*44
 a += [text(64,y+21,f'第{i+1}次',19),f'<rect x="128" y="{y}" width="66" height="32" rx="7" fill="#e0ebcc" stroke="#7a9967"/>',text(161,y+24,days[d],23),text(270,y+22,f'{i*10}天',19)]
 if i<5:a += [f'<path d="M211 {y+21}V{y+54}" stroke="#c28d42" stroke-width="2" marker-end="url(#a)"/>']
a += [text(180,344,'從首次起算經過天數',18),'</g>']
# Four choices, six visits, one forbidden weekday.
a += ['<g transform="translate(720 0)">',text(180,35,'逐列檢查星期日',22)]
for k in range(6):a += [text(96+42*k,73,str(k+1),18)]
for j,(key,v) in enumerate(seq.items()):
 y=103+j*54;a += [text(39,y+24,key,22)]
 for k,d in enumerate(v):
  x=79+42*k;fill='#f1d3c5' if d==6 else '#e3edd2' if key=='C' else '#eff0e7';stroke='#bb7058' if d==6 else '#8b9b7b'
  a += [f'<rect x="{x}" y="{y}" width="35" height="35" rx="6" fill="{fill}" stroke="{stroke}"/>',text(x+17.5,y+25,days[d],21,'#a65340' if d==6 else '#405c51')]
a += [text(180,344,'C：六次都不是星期日',20),'</g></svg>']
art=Path('docs/comics/art/q-809-cycle.svg');art.write_text(''.join(a))
Path('docs/comics/q-809-cycle-validation.json').write_text(json.dumps({'daysElapsed':[10*i for i in range(6)],'visitCount':6,'intervalCount':5,'optionSequences':{k:[days[d] for d in v] for k,v in seq.items()},'uniqueSundayFree':['C'],'clockwiseHighlightedSteps':['三到四','四到五','五到六'],'passed':True},ensure_ascii=False,indent=2)+'\n')
s.update(art=str(art),generationMethod='programmatic SVG exact weekday cycle and six-visit option table',generatorFile='docs/comics/q-809-cycle-generate.py',visualChecked=False,createdAtUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),artSha256=hashlib.sha256(art.read_bytes()).hexdigest())
for k in ['nativeArt','artSHA256','promptFile','checkedAt','validationFile']:s.pop(k,None)
s['panels']=[{'heading':'① 過10天，星期只往後推3天','text':'一週有7天，10＝7＋3。完整的一週回到同一星期，再多走3天；從星期三出發，依序經過四、五，到星期六。','alt':'七日順時針循環，星期三到四、四到五、五到六三段箭頭，10天的星期位移是3天。'},{'heading':'② 六次兌換，只有五個間隔','text':'從星期三列滿6次：三、六、二、五、一、四。以首次為起點，經過0、10、20、30、40、50天；相鄰兩次都差10天。','alt':'六列兌換星期與首次後經過天數，恰好五支間隔箭頭，不畫實際月份與日期。'},{'heading':'③ 其他選項都碰到星期日','text':'A從星期一開始，第3次遇星期日；B在第5次、D在第2次遇星期日。C的六次都沒有星期日，因此符合題意。','alt':'四選項各六次的精確星期表，星期日以橙紅色框突出，C六格皆無星期日，列數與次數不省略。'}]
s['rationale']='依使用者數學優先精確關係圖新規，把原人物版封存before-cycle，替換原創星期循環SVG、六次與五間隔表、四選項精確排除表。重看原卷23題及來源全文，獨立模7列舉ABCD六次星期，唯一C無日；保留原題與C，不虛構月份日期或真實店家資訊。全部圖均新製、不採來源AI圖。'
s['protectedWords']=['小君','星期三','星期日','星期一','星期六','10＝7＋3','6次兌換','5個間隔','差10天','第3次','第5次','第2次']
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
