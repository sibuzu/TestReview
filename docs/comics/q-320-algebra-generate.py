from pathlib import Path
from fractions import Fraction as F
import json,datetime,hashlib
p=Path('docs/comics/q-320.json');b=Path('docs/comics/q-320-before-algebra.json')
if not b.exists():b.write_bytes(p.read_bytes())
s=json.loads(p.read_text());budget=F(300-70,40);energy=F(1925-495,329);totals={n:(70+40*n,495+329*n) for n in range(2,7)};assert budget==F(23,4) and max(n for n,v in totals.items() if v[0]<=300 and v[1]<=1925)==4
Path('docs/comics/q-320-algebra-validation.json').write_text(json.dumps({'budgetBound':str(budget),'energyBound':str(energy),'totals':totals,'integerMaximum':4,'correctOption':'C','passed':True},ensure_ascii=False,indent=2)+'\n')
def text(x,y,t,size=22,col='#405c51'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{col}">{t}</text>'
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><rect width="1080" height="360" fill="#f7f8f0"/>']
for i,bound in enumerate([budget,energy]):
 limit=5 if i==0 else 4;xlim=60+(float(bound)-2)*60
 a += [f'<g transform="translate({360*i} 0)">',text(180,45,'金額的限制' if i==0 else '熱量的限制'),text(180,97,'n ≤ 5.75' if i==0 else 'n ≤ 1430／329',22),'<path d="M43 200H322" stroke="#7d8e80" stroke-width="2"/>',f'<path d="M50 200H{xlim}" stroke="#7fa67d" stroke-width="8"/>',f'<path d="M{xlim} 162V222" stroke="#c89347" stroke-width="2" stroke-dasharray="5 4"/>']
 for n in range(2,7):
  x=60+(n-2)*60;valid=n<=limit
  a += [f'<circle cx="{x}" cy="200" r="9" fill="{ "#6e9a70" if valid else "#f7f8f0"}" stroke="{ "#5f8e66" if valid else "#bbaaa0"}" stroke-width="2"/>',text(x,241,str(n),23)]
 a += [text(xlim,151,'5.75' if i==0 else '約4.35',18,'#b17c36'),text(180,298,'整個計算，最多5個' if i==0 else '整個計算，最多4個',22),text(180,338,'只看這一項上限',18),'</g>']
a+=['<g transform="translate(720 0)">',text(180,42,'回代選項，兩項都要過'),text(57,98,'個數',19),text(153,98,'總金額',19),text(267,98,'總熱量',19)]
for i,n in enumerate(range(2,6)):
 y=120+i*49;cost,cal=totals[n];fill='#e4edcf' if n==4 else '#fafaf2'
 a += [f'<rect x="26" y="{y}" width="308" height="42" rx="5" fill="{fill}" stroke="#becbb3"/>',text(57,y+28,str(n)),text(153,y+28,str(cost)),text(267,y+28,str(cal),22,'#aa5f47' if cal>1925 else '#405c51')]
a += [text(180,347,'300元 ／ 1925大卡',19),'</g></svg>'];art=Path('docs/comics/art/q-320-algebra.svg');art.write_text(''.join(a))
s.update(art=str(art),generationMethod='programmatic SVG exact integer bounds and joint constraint comparison',generatorFile='docs/comics/q-320-algebra-generate.py',visualChecked=False,createdAtUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),artSha256=hashlib.sha256(art.read_bytes()).hexdigest())
for k in ['nativeArt','artSHA256','promptSummary','checkedAt','completedAt','layoutEvidence','visualReview','validationFile']:s.pop(k,None)
s['panels']=[{'heading':'① 先用金額，求一個上限','text':'早餐已花70元，每個肉粽40元。70＋40n≤300，得n≤5.75；數量取整數，單看金額最多5個，還不能直接當答案。','alt':'肉粽數量上限數線，在2到6的整數候選中，金額界線5.75位於5與6之間；僅呈現金額上限，不是完整可行範圍。'},{'heading':'② 再用熱量，得到更緊的上限','text':'早餐495大卡，每個肉粽329大卡。495＋329n≤1925，得n≤1430／329，約4.35；單看熱量，最多只能4個。','alt':'相同數線尺度的熱量界線約4.35位於4與5之間；4可、5不可，熱量完全依原題資料。'},{'heading':'③ 回代，檢查兩項同時符合','text':'4個連同早餐共230元、1811大卡，都未超過限制。5個雖只花270元，熱量卻達2140大卡，已超過1925大卡，所以最多4個。','alt':'原題四候選2到5逐列總金額與總熱量，4整列綠底，5的2140紅字；不把金額及熱量相加成一個數。'}]
s['rationale']='依數學圖優先新規，舊人物版封存before-algebra，改為全新同尺度數線上限及回代選項表。原卷小吃表與題目四選項實看，來源對話僅作背景、不冒稱其中有肉粽完整解法；獨立Fraction計算23/4、1430/329及各選項總額總熱量，C不變。數線限定上限展示，不把0或1個當成午晚餐完整安排；4可分午晚各2。不延伸營養醫療建議。'
s['originalMaterialsChecked']=True;s['originalMaterials']=['site/dist/assets/questions/q-320-source-f1c681a94c.jpg','site/dist/sources/6ae05187-3f28-83ee-a9e3-89b8168480a3.txt 來源背景，未見本題完整文字解法']
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
