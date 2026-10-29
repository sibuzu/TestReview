from pathlib import Path
import json,hashlib,math
art=Path('docs/comics/art/q-811.svg')
shape='M105 90 C105 133 87 165 103 194 Q150 236 197 194 C213 165 195 133 195 90 Z'
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-label="虛欹、中正、滿覆三種文字狀態示意，非實物復原">','<rect width="900" height="300" fill="#faf7ed"/>','<style>text{font-family:"Noto Sans CJK TC",sans-serif;text-anchor:middle;fill:#284a48} .title{font-size:23px;font-weight:700}.state{font-size:22px;font-weight:700}.small{font-size:16px}</style>']
states=[('虛：空著',-25,'欹：傾斜','#a46730',None),('中：水量適中',0,'正：端正','#3b735b',165),('滿：過盈',105,'覆：傾覆','#a65746',174)]
for i,(title,angle,state,color,water) in enumerate(states):
    parts.append(f'<g id="state-{i}" data-rotation="{angle}" data-water="{water}" transform="translate({i*300} 0)"><text x="150" y="31" class="title">{title}</text>')
    parts.append('<path d="M45 243 V73 M255 243 V73 M32 245 H268" fill="none" stroke="#9f9278" stroke-width="9" stroke-linecap="round"/><path d="M45 140 H255" stroke="#9f9278" stroke-width="6"/>')
    parts.append(f'<defs><clipPath id="vessel-clip-{i}"><path d="{shape}" transform="rotate({angle} 150 140)"/></clipPath></defs>')
    parts.append(f'<g transform="rotate({angle} 150 140)"><path d="{shape}" fill="#ebd3a7" stroke="#6e705c" stroke-width="4"/></g>')
    if water is not None:
        parts.append(f'<rect id="water-{i}" x="50" y="{water}" width="210" height="85" fill="#83bdcf" clip-path="url(#vessel-clip-{i})"/>')
    parts.append(f'<g transform="rotate({angle} 150 140)"><path d="{shape}" fill="none" stroke="#6e705c" stroke-width="4"/><ellipse cx="150" cy="90" rx="45" ry="9" fill="#f9efd6" stroke="#6e705c" stroke-width="4"/></g><circle cx="150" cy="140" r="7" fill="#7f7864" stroke="#fff9ed" stroke-width="2"/>')
    if i==2:parts.append('<path id="spill" d="M190 192 C207 203 204 219 225 232" fill="none" stroke="#65a9c2" stroke-width="7" stroke-linecap="round"/><path d="M235 224 Q224 238 235 242 Q246 238 235 224Z" fill="#65a9c2"/>')
    parts.append(f'<text x="150" y="276" class="state" style="fill:{color}">{state}</text></g>')
parts.append('</svg>');art.write_text(''.join(parts))
d={'id':'q-811','subject':'Chinese','title':'由中則正、滿則覆，讀出適中與戒盈','art':str(art),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-811-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 虛則欹：空著時傾斜','text':'虛是空，欹是傾斜。原文先說虛則欹，試水後也見虛而欹；空著並非本文端正的狀態。圖只對照文字中的姿態，並非古器實物復原，也不規定固定水量比例。','alt':'全新精確SVG以旋轉負25度的簡化器形對照虛/欹，沒有水，姿態示意非考古復原或機構設計圖。'},
{'heading':'② 中則正：水量適中，器身端正','text':'中則正和實際觀察中而正互相印證：注入適當水量，器身才能端正，正是 A 的說法。中在這裡指適中，不必把圖中水線硬當成實物剛好一半容量。','alt':'全新精確SVG同款器形零度端正、水平藍色水線，對照適中與正，不把示意水線量化為半容量。'},
{'heading':'③ 滿則覆：過盈反而傾覆','text':'水滿後器身傾覆，孔子由此感嘆惡有滿而不覆者哉。惡有是反問哪有，重點在警惕自滿；不是說統治者作惡多端，也不是用實用功能蓋過警戒的象徵意義。','alt':'全新精確SVG同款器形旋轉105度、倒出水滴表示滿後傾覆瞬間；沒有加人事災難或作惡統治者。'}],
'fourth':{'answer':'答案 A：水量適中，欹器才端正','points':['虛：欹；中：正；滿：覆，三狀態不可混。','孔子的感嘆引出戒盈，非批評惡人未受報。','D 的虛懷若谷，未扣住本段適中、戒盈的直接寓意。']},
'protectedWords':['欹器','虛則欹','中則正','滿則覆','虛而欹','中而正','水量適中','適當水量','端正','傾覆','孔子','惡有','哪有','戒盈','自滿','虛懷若谷','象徵意義','實用功能','器身'],
'originalChecked':{'images':['site/dist/assets/questions/q-811-source-1.jpg'],'visualChecked':True,'answer':'A','notes':'親見16全文/四項及原卷紅改A。虛欹/中正/滿覆與末反問對照，保持A，不增器物歷史尺寸、注音或流體力學推論。'},
'sourceUrl':'https://gemini.google.com/share/ec6c955b81b3','answerCheckedAgainst':'原卷虛則欹中則正滿則覆及試水三結果；MOE欹形義傾斜不正引用荀子宥坐全文主文已讀。',
'references':[{'title':'教育部重編辭典：惡有','url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=158794&la=1&powerMode=0','supports':'惡有為怎麼有/那裡有，對應反問哪有而非作惡','access':'主文已讀，不另加字音題或當代政治指涉'},{'title':'教育部重編辭典：欹（傾斜義）','url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=10522&la=1&powerMode=0','supports':'傾斜不正及虛則欹/中則正/滿則覆引用','access':'主文已讀，未另加字音，不以示意圖充當實物機構復原'}],
'rationale':'同款器形的精確狀態對照，比人物情境更直接驗證A；不把中量化為50%，不把惡有誤解作惡，也不讓D虛的字面誤導空即正。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'sameVesselPathAllStates':True,'rotationsDegrees':[-25,0,105],'emptyHasWater':False,'middleWaterlineHorizontal':True,'fullShownAtOverturningInstant':True,'actualCapacityFractionsClaimed':False,'archaeologicalReconstructionClaimed':False,'answer':'A'},'artSHA256':hashlib.sha256(art.read_bytes()).hexdigest()};Path('docs/comics/q-811.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
