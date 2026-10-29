from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from fractions import Fraction as F
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#6b8a7d"/></marker></defs><g font-family="Noto Sans CJK TC,sans-serif" fill="#234344" text-anchor="middle"><path fill="#eff3e9" d="M0 0h180v180H0Z"/><path fill="#edf1f7" d="M180 0h180v180H180Z"/><path fill="#f5efdf" d="M360 0h180v180H360Z"/>']
s.append('<text x="90" y="22" font-size="12">除以負數，不等號反向</text><text x="90" y="49" font-size="19">x＞−1.5</text><path d="M38 74H164" stroke="#6b8a7d" stroke-width="2" marker-end="url(#a)"/><circle cx="38" cy="74" r="4" fill="#eff3e9" stroke="#6b8a7d"/><path d="M12 108H170" stroke="#8c9f98"/>')
for val in [-2,-1,0,1,2]:
 x=20+(val+2)*36;s.append(f'<path d="M{x} 104V112" stroke="#8c9f98"/><text x="{x}" y="127" font-size="12">{str(val).replace("-","−")}</text>')
 if val>=-1:s.append(f'<circle cx="{x}" cy="108" r="3" fill="#6b8a7d"/>')
s.append('<text x="90" y="163" font-size="14">x整數：從−1開始</text>')
s.append('<text x="270" y="22" font-size="14">整數x，P未必整數</text><text x="228" y="48" font-size="13">x</text><text x="306" y="48" font-size="13">P</text>')
for i,(x,p) in enumerate([('−1','4/5'),('0','6/5'),('1','8/5'),('2','2')]):
 y=70+28*i
 if i==3:s.append(f'<rect x="201" y="{y-18}" width="138" height="25" rx="5" fill="#d0dfc5"/>')
 s.append(f'<text x="228" y="{y}" font-size="15">{x}</text><text x="306" y="{y}" font-size="15">{p}</text>')
s.append('<path d="M267 35V166M201 54H339" stroke="#8da3ad"/>')
s.append('<text x="450" y="22" font-size="14">反查選項對應的x</text><g font-size="12"><text x="382" y="51">P</text><text x="423" y="51">x</text><text x="489" y="51">檢查</text></g>')
for i,(p,x,label) in enumerate([('0','−3','不合範圍'),('1','−1/2','不是整數'),('2','2','兩條件皆合')]):
 y=80+33*i;col='#a65e5a' if i<2 else '#3d7556';s.append(f'<text x="382" y="{y}" font-size="15" fill="{col}">{p}</text><text x="423" y="{y}" font-size="14" fill="{col}">{x}</text><text x="489" y="{y}" font-size="11" fill="{col}">{label}</text>')
s.append('</g></svg>');p=Path('docs/comics/art/q-323.svg');p.write_text(''.join(s));ET.fromstring(p.read_text())
checks={'bound':'x > -3/2; integer x >= -1','xValues':[-1,0,1,2],'pValues':[str(F(2*x+6,5)) for x in [-1,0,1,2]],'optionBackSubstitution':{str(k):str(F(5*k-6,2)) for k in range(4)},'firstIntegerP':'2','correspondingX':2,'correctOption':'C','passed':True};assert checks['pValues']==['4/5','6/5','8/5','2']
Path('docs/comics/q-323-algebra-validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
d={'id':'q-323','subject':'Math','title':'x要整數，P也要整數，兩條件一起查','art':str(p),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-323-generate.py','startedAt':'2026-10-29T02:26:31.644399+00:00','panels':[{'heading':'① 先解不等式，再取整數x','text':'−3x＋5＜8−x，移項得−2x＜3。除以−2要反向，所以x＞−1.5；x為整數，可從−1、0、1、2依序檢查。','alt':'x＞−1.5的開口射線與整數點−1/0/1/2，−1.5不納入，最小整數x為−1。'},{'heading':'② 最小x，不一定給整數P','text':'代入x＝−1、0、1、2，P依序為4/5、6/5、8/5、2。第一個整數是2；不能把4/5直接向上取成1，就省略檢查對應的x。','alt':'對照表x與P的四筆精確分數，最後一列x2/P2著綠色；不把4/5或6/5當整數。'},{'heading':'③ 反查較小選項，排除漏條件','text':'P＝0時x＝−3，不符合範圍；P＝1時x＝−1/2，不是整數。P＝2時x＝2，兩條件都符合，因此最小整數值為2，選C。','alt':'P0/1/2對應x−3/−1/2/2分別標不合範圍、非整數、兩條件皆合，不把P整數與x整數混同。'}],'fourth':{'answer':'答案 C：P的最小整數值是2','points':['不等式除以負數，方向要反轉。','x≥−1且x為整數；P也必須是整數。','P隨x增加，從最小x依序查，第一個整數P為2。']},'protectedWords':['−2x＜3','x＞−1.5','x＝−1','P＝1','P＝2','x＝−1/2','x＝2','最小整數值','4/5','6/5','8/5'],'rationale':'實看原卷第9題全部條件及四選項，C不變。新精確整數射線/代入表/選項反查表分別處理除負數反向、x與P兩個整數條件；分數用Fraction獨立驗算，不用人物情境或無助的裝飾圖。','promptSummary':'原生SVG：x>-1.5開口射線及整數點；x -1/0/1/2與P 4/5/6/5/8/5/2表；P0/1/2反查x-3/-1/2/2。','answerCheckedAgainst':'原卷x整數與−3x+5<8−x、P=(2x+6)/5及A0 B1 C2 D3；獨立Fraction回代第一整數P2/x2。','manualLineBreaks':False,'layoutVersion':'native-fluid-v6','sourceAIUsed':False,'originalChecked':{'images':['site/dist/assets/questions/q-323-source-3a5d765250.jpg'],'visualChecked':True,'answer':'C','notes':'實看x整數、P最小整數兩條件與1/5係數，原黑A紅C；不把最小x或非整數P取整冒充答案。'},'artSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'algebraValidation':'docs/comics/q-323-algebra-validation.json'}
Path('docs/comics/q-323.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
