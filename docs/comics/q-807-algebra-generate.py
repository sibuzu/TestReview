from pathlib import Path
from fractions import Fraction as F
import json,hashlib,datetime
old=Path('docs/comics/q-807.json');backup=Path('docs/comics/q-807-before-algebra.json')
if not backup.exists():backup.write_bytes(old.read_bytes())
s=json.loads(old.read_text())
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#b78239"/></marker></defs><rect width="1080" height="360" fill="#f7f8f0"/>']
def txt(x,y,t,size=22,col='#405c51'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{col}" font-family="sans-serif" font-size="{size}">{t}</text>'
subs=['₁','₂','₃','₄','₅','₆','₇','₈','₉','₁₀','₁₁','₁₂']
p += [txt(88,42,'奇數位置'),txt(260,42,'偶數位置')]
for k in range(6):
 y=65+k*43
 p += [f'<rect x="48" y="{y}" width="80" height="34" rx="7" fill="#e6edd3" stroke="#77965c"/><rect x="220" y="{y}" width="80" height="34" rx="7" fill="#dfebee" stroke="#658f9a"/>',txt(88,y+25,'a'+subs[2*k],24),txt(260,y+25,'a'+subs[2*k+1],24),f'<path d="M137 {y+18}H207" stroke="#b78239" stroke-width="2" marker-end="url(#a)"/>',txt(174,y+9,'+d',19)]
p += [txt(180,348,'6對相鄰項',20)]
# bar lengths refer to aggregate sums, not the individual terms (some terms may be negative)
p+=['<g transform="translate(360 0)">',txt(180,38,'兩組的和'),txt(78,99,'奇數項和',20),txt(78,170,'偶數項和',20),'<rect x="130" y="71" width="100" height="40" fill="#d4dfb6" stroke="#789159"/><rect x="130" y="142" width="180" height="40" fill="#d5e5e9" stroke="#608e9a"/>',txt(180,99,'10'),txt(220,170,'18'),'<path d="M231 125H309" stroke="#b78239" stroke-width="3"/>',txt(273,116,'差8',20),txt(180,229,'6個相同的差')]
for k in range(6):
 p+=[f'<rect x="{39+k*47}" y="250" width="47" height="47" fill="#f4e7c3" stroke="#b88c48"/>',txt(62.5+k*47,281,'d')]
p += [txt(180,333,'總共 6d＝8',22),'</g>']
# positions, not positive term values, shown on this index schematic
p += ['<g transform="translate(720 0)">',txt(180,44,'相鄰與隔項'),'<path d="M46 180H318" stroke="#728b7e" stroke-width="3"/>']
for x,t in [(70,'a₁'),(180,'a₂'),(290,'a₃')]:
 p += [f'<circle cx="{x}" cy="180" r="7" fill="#fcfcf2" stroke="#63867b" stroke-width="3"/>',txt(x,218,t,25)]
p+=['<path d="M74 145H174M184 145H284" stroke="#b78239" stroke-width="3" marker-end="url(#a)"/>',txt(125,131,'+d'),txt(235,131,'+d'),'<path d="M72 256Q180 310 285 256" stroke="#688c9b" stroke-width="3" fill="none" marker-end="url(#a)"/>',txt(180,320,'+2d',24),'</g></svg>']
art=Path('docs/comics/art/q-807-algebra.svg');art.write_text(''.join(p))
a=[F(-5)+i*F(4,3) for i in range(12)];odd=sum(a[::2]);even=sum(a[1::2]);diff=[a[i+1]-a[i] for i in range(0,12,2)]
assert odd==10 and even==18 and len(diff)==6 and all(d==F(4,3) for d in diff)
Path('docs/comics/q-807-algebra-validation.json').write_text(json.dumps({'terms':[str(v) for v in a],'oddSum':str(odd),'evenSum':str(even),'pairDifferences':[str(v) for v in diff],'correctOption':'B','thirdPanel':'index relation only, no assumption all values positive','passed':True},ensure_ascii=False,indent=2)+'\n')
s.update(art=str(art),generationMethod='programmatic SVG exact adjacent-pair algebra relationship diagrams',generatorFile='docs/comics/q-807-algebra-generate.py',visualChecked=False,createdAtUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),artSha256=hashlib.sha256(art.read_bytes()).hexdigest())
for k in ['nativeArt','artSHA256','promptFile','editPromptFile','checkedAt','validationFile']:s.pop(k,None)
s['panels']=[{'heading':'① 12項，逐對看相鄰的差','text':'綠框為奇數位置，藍框為下一個偶數位置：第2項配第1項，一直到第12項配第11項。每一對相鄰，所以偶數項減前一奇數項都等於d。','alt':'精確6列奇偶位置配對，每列從奇數項到下一偶數項標+d；共12個框、6個相鄰差，未省略成3對。'},{'heading':'② 兩組和的差，就是6個d','text':'偶數項和18減奇數項和10，總差為8。六對相加得到6d＝8，所以d＝8／6＝4／3；分母用配對數6，並不是總項數12。','alt':'兩條長度比10比18的總和條，和的差8；下方6個等寬d框示意6個相同公差，不把個別項畫成必為正數。'},{'heading':'③ 隔一項，才會差2d','text':'從第1項到第2項只走一步，差d；從第1項到第3項走了兩步，差2d。不要把奇數位置內相隔兩項的差，誤套到本題相鄰奇偶配對。','alt':'依序a1、a2、a3的項次示意，每步+d，兩步+2d；不是個別數值正負的數線。'}]
s['rationale']='依使用者最新數學圖優先規則，原人物版另存q-807-before-algebra.json，本版以全新精確6對SVG替換。重看原卷第18題及來源message189全文，獨立以Fraction建12項，6對差皆4/3、奇和10、偶和18精確回代通過；B不變。條形圖只表總和，不假定每項均為正；項次圖只表相鄰與隔項關係，不是數值數線。不沿用來源AI圖。'
s['protectedWords']=['奇數位置','偶數位置','奇數項','偶數項','相鄰配對','6d＝8','4／3','12項','6對','差2d','差d','2d']
old.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
