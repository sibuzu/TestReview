import json,datetime
from pathlib import Path
from fractions import Fraction
from xml.sax.saxutils import escape
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#3a8060"/></marker></defs>']
def rect(x,y,w,h,fill='#faf8ed',r=7): parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="#b7ccc0"/>')
def t(x,y,s,size=16,c='#284c3c',weight=500): parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" font-weight="{weight}" fill="{c}">{escape(s)}</text>')
for i in range(3):rect(i*200+2,2,196,196)
t(100,23,'14 ＜ 7x → x ＞ 2',17,weight=700)
parts.append('<path d="M24 103H182" stroke="#6e8074" stroke-width="2"/><path d="M58 83H184" stroke="#3a8060" stroke-width="3" marker-end="url(#a)"/>')
for n in range(1,6):
 x=28+(n-1)*34
 parts.append(f'<path d="M{x} 98V108" stroke="#6e8074"/>');t(x,125,str(n),15)
 if n>=3:parts.append(f'<circle cx="{x}" cy="83" r="5" fill="#3a8060"/>')
parts.append('<circle cx="62" cy="83" r="6" stroke="#3a8060" stroke-width="2" fill="#faf8ed"/>')
t(100,157,'2不取；只取整數點',15);t(100,182,'3、4、5、…',20,c='#3a8060',weight=700)
t(300,23,'x → 7x−5',22,weight=700)
for y,n,v in [(48,3,16),(81,4,23),(114,5,30),(159,17,114)]:
 rect(218,y,52,28,'#e4ede4');t(244,y+14,str(n),17);t(291,y+14,'→',19);rect(316,y,68,28,'#e2ebf2');t(350,y+14,str(v),17)
t(244,151,'⋮',18);t(350,151,'⋮',18)
t(500,21,'代回 x＝(值＋5)/7',16,weight=700)
rows=[('A  2','1','×'),('B  9','2','×'),('C  73','78/7','×'),('D  114','17','✓')]
for i,(lab,val,ok) in enumerate(rows):
 y=42+i*35;rect(412,y,176,30,'#e0eee2' if i==3 else '#fffdf8');t(447,y+15,lab,15);t(513,y+15,val,16);t(572,y+15,ok,18,c='#337d53' if i==3 else '#aa6446',weight=700)
t(500,188,'整數 ＋ 大於2',15)
parts.append('</svg>');Path('docs/comics/art/q-322.svg').write_text(''.join(parts))
s={'id':'q-322','subject':'Math','title':'範圍與整數，兩個條件都要過關','art':'docs/comics/art/q-322.svg','protectedWords':['整數','端點','x＞2','x＝2','x＝17','x＝78/7','7x−5','78/7','114','嚴格大於'],'panels':[{'heading':'① 先解不等式，2是空心端點','text':'−5x＋11＜2x−3，兩邊加5x、再加3，得14＜7x。除以正數7，不等號方向不變，得x＞2。x是整數，只能取3、4、5、…。','alt':'等距數線2處空心圓，向右射線及3/4/5綠色整數點，1和2不列入整數解。'},{'heading':'② 代數式的值不是任意大於9的數','text':'x每增加1，7x−5就增加7，例如16、23、30、…。因此不能只看選項是否大於9；還要確認它能由符合條件的整數x算出。','alt':'輸入輸出配對3→16、4→23、5→30，省略號後17→114；只作表格，不把跨段間距畫成相同數線尺度。'},{'heading':'③ 四個選項都代回，檢查兩關','text':'設選項值為v，則x＝(v＋5)/7。A得1，B得2，都不大於2；C得78/7，雖大於2卻非整數；D得17，同時符合兩條件。','alt':'四列逆算表：A2→1叉、B9→2叉、C73→78/7叉、D114→17勾；端點和非整數分開判斷。'}],'fourth':{'answer':'答案 D：114可由x＝17得到','points':['x＞2，不包含端點2。','C雖大於9，反算x卻不是整數。','D回代不等式與7x−5，兩者皆符合。']},'rationale':'舊not_suitable理由只看人物場景，依最新數學規則重審，以嚴格端點數線、離散輸入輸出及逆算表具體呈現兩條件交集。完整原卷第8題與A2/B9/C73/D114已實看，正確D不變；來源全文只含不等式整數解一般整理，未假稱原AI逐題解說本題。','supersedesReview':'docs/comics/q-322-review.json','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-322-source-1c371edfb0.jpg','site/dist/sources/6ae05187-3f28-83ee-a9e3-89b8168480a3.txt lines 240–305 (general inequality review only)'],'sourceUrl':'https://chatgpt.com/share/6ae05187-3f28-83ee-a9e3-89b8168480a3','generationMethod':'precise native SVG open endpoint integer number line and input-output inverse table','answerCheckedAgainst':'14<7x得x>2。四選項反解1、2、78/7、17，僅17是整數且>2。回代x17：-74<31，7×17−5=114。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-322.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
rows=[]
for label,v in zip('ABCD',[2,9,73,114]):
 x=Fraction(v+5,7);valid=x>2 and x.denominator==1;rows.append({'option':label,'value':v,'x':str(x),'greaterThan2':x>2,'integer':x.denominator==1,'valid':valid})
assert [r['option'] for r in rows if r['valid']]==['D']
assert -5*17+11<2*17-3 and 7*17-5==114
Path('docs/comics/q-322-algebra-validation.json').write_text(json.dumps({'id':'q-322','pass':True,'rows':rows,'endpoint':'strict x>2 excludes2; filled integer points3,4,5 on exact equal spacing','sequence':'x3/4/5/17 maps16/23/30/114; ellipsis explicitly not equal distance scale','backSubstitution':{'lhs':-74,'rhs':31,'expression':114},'originalActuallyViewed':True},ensure_ascii=False,indent=2)+'\n')
