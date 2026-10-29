from pathlib import Path
from fractions import Fraction as F
import json,datetime,hashlib
p=Path('docs/comics/q-324.json');b=Path('docs/comics/q-324-before-algebra.json')
if not b.exists():b.write_bytes(p.read_bytes())
s=json.loads(p.read_text());ratio=F(360,480);lower=F(200)*ratio;assert lower==150 and 2*lower==300 and 2*200==400
Path('docs/comics/q-324-algebra-validation.json').write_text(json.dumps({'volumeRatio':str(ratio),'middleYellowLower':100,'middleYellowUpperInclusive':200,'largeRedLowerExclusive':200,'derivedMiddleLowerExclusive':150,'twoMiddleRange':{'lower':300,'lowerIncluded':False,'upper':400,'upperIncluded':True},'givenThresholdsOnly':[300,400],'correctOption':'D','passed':True},ensure_ascii=False,indent=2)+'\n')
def text(x,y,t,size=22,col='#405c51'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{col}">{t}</text>'
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#b57b5f"/></marker></defs><rect width="1080" height="360" fill="#f7f8ef"/>',text(180,38,'同濃度，容量比3：4')]
a += [text(62,109,'中杯',20),'<rect x="108" y="78" width="162" height="46" fill="#efdaa1" stroke="#b99b49"/>',text(189,109,'360毫升',21),text(62,191,'大杯',20),'<rect x="108" y="160" width="216" height="46" fill="#e7bfb1" stroke="#b88069"/>',text(215,191,'480毫升',21),text(180,267,'每毫升含量相同',21),text(180,310,'總含量也成3：4',23)]
# Intersect middle-cup conditions on the same milligram scale.
def mx(v):return 50+(v-75)*1.4
a += ['<g transform="translate(360 0)">',text(180,34,'一中杯的含量 m',22)]
for y,label in [(106,'黃色原條件'),(191,'大杯推下限'),(276,'合併兩條件')]:
 a += [text(180,y-30,label,18),f'<path d="M50 {y}H326" stroke="#ccd4c6" stroke-width="2"/>']
a += [f'<path d="M{mx(100)} 106H{mx(200)}" stroke="#c5a14a" stroke-width="7"/>',f'<path d="M{mx(150)} 191H323" stroke="#b57b5f" stroke-width="7" marker-end="url(#a)"/>',f'<path d="M{mx(150)} 276H{mx(200)}" stroke="#72956d" stroke-width="8"/>']
for y,l,r in [(106,100,200),(191,150,None),(276,150,200)]:
 a += [f'<circle cx="{mx(l)}" cy="{y}" r="8" fill="#f7f8ef" stroke="#8a7956" stroke-width="3"/>',text(mx(l),y+27,str(l),18)]
 if r:a += [f'<circle cx="{mx(r)}" cy="{y}" r="8" fill="#72956d" stroke="#5b7f5c" stroke-width="2"/>',text(mx(r),y+27,str(r),18)]
a += [text(180,346,'毫克：150＜m≤200',20),'</g>']
# Final range and the two problem-supplied upper limits share one exact scale.
def tx(v):return 45+(v-200)*1.05
a += ['<g transform="translate(720 0)">',text(180,36,'兩杯中杯：總量2m',22),'<path d="M45 126H327" stroke="#cbd4c4" stroke-width="2"/>',f'<path d="M{tx(300)} 126H{tx(400)}" stroke="#73986b" stroke-width="9"/>',f'<circle cx="{tx(300)}" cy="126" r="9" fill="#f7f8ef" stroke="#688964" stroke-width="3"/><circle cx="{tx(400)}" cy="126" r="9" fill="#688964"/>',text(tx(300),162,'300',20),text(tx(400),162,'400',20),text(180,208,'300＜總量≤400',22),text(180,264,'題給我國上限：300',20,'#a3644f'),text(180,304,'題給歐盟上限：400',20,'#4c775a'),text(180,344,'單位：毫克',18),'</g></svg>']
art=Path('docs/comics/art/q-324-algebra.svg');art.write_text(''.join(a))
s.update(art=str(art),generationMethod='programmatic SVG exact volume ratio and open/closed interval intersection',generatorFile='docs/comics/q-324-algebra-generate.py',visualChecked=False,createdAtUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),artSha256=hashlib.sha256(art.read_bytes()).hexdigest())
for k in ['nativeArt','artSHA256','promptFile','checkedAt','validationFile']:s.pop(k,None)
s['panels']=[{'heading':'① 同濃度，含量隨容量成比例','text':'中杯360毫升、大杯480毫升，容量比為3：4。每毫升含量相同，所以中杯咖啡因含量，也是大杯的3／4；不能只看杯子顏色。','alt':'360與480毫升的精確3比4等高條形，不把容量和咖啡因含量混為相同單位。'},{'heading':'② 黃色上限，合併大杯推得的下限','text':'設一中杯含量為m。黃色給100＜m≤200；大杯紅色超過200毫克，乘3／4可得m＞150。合併後，150＜m≤200。','alt':'同尺度三條含量範圍：中杯黃色100開200閉、大杯推出150開往右、交集150開200閉；實心為包含端點，空心為不包含。'},{'heading':'③ 兩杯乘2，再比題給上限','text':'兩中杯總量是2m，故300＜2m≤400毫克。一定超過題給我國300毫克上限，卻不超過題給歐盟400毫克上限，所以選D。','alt':'總量範圍300開400閉，搭配原卷所給兩個上限；僅數學判讀原題，不延伸一般健康安全建議。'}]
s['protectedWords']=['咖啡因','每毫升','不超過','3／4','100＜m≤200','150＜m≤200','m＞150','300＜2m≤400','150毫克','200毫克','300毫克','400毫克']
s['rationale']='依數學精確圖新規，把原人物版保存before-algebra，改新容量比與區間交集SVG。原卷題幹、兩表、四選項實看，來源相關顏色段落已讀；以Fraction獨立驗3/4推150開下限及兩杯300開400閉，保留使用者已確認D，不重開既有原AI漏條件訂正。每個空實心端點精確符合嚴格不等式，僅採題給數據，不做現行醫療營養指引。'
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
