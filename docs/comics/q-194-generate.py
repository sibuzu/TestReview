import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'先看主詞，還不夠',17)
r(18,46,164,43,'#e6edf3');t(100,68,'Most of the food',18)
t(100,117,'food：不可數',18)
r(18,143,164,35,'#f0e6d6');t(100,161,'後面還有 can',18)
t(300,22,'can後接原形',19)
r(218,46,164,43,'#dcebdc');t(300,68,'can power ✓',23)
r(218,119,164,43,'#f1e5db');t(300,141,'can powers ×',20,c='#9b6756')
t(300,183,'不能再替power加s',15)
t(500,22,'有無can，形式不同',16)
r(418,46,164,50,'#e6edf3');t(500,62,'沒有can時',15);t(500,81,'food powers up ...',17)
r(418,116,164,58,'#dcebdc');t(500,133,'本題有can',15);t(500,157,'food can power up ...',15)
s.append('</svg>');Path('docs/comics/art/q-194.svg').write_text(''.join(s))
x={'id':'q-194','subject':'English','title':'先找can，power就用原形不加s','art':'docs/comics/art/q-194.svg','protectedWords':['Most of the food','food','can','power','powers','power up','原形動詞','不可數'],'panels':[{'heading':'① food不可數，不代表空格一定加s','text':'Most of the food的food是不可數名詞，主詞視為單數。但原句在空格前已經有can，不能只看主詞就把power改成powers。','alt':'主詞Most of the food與不可數food說明後，再突出後面還有can；不畫食物數量、營養比例或虛構大腦作用。'},{'heading':'② can後面固定用原形power','text':'can後接原形動詞，所以寫can power up，不寫can powers up。power在這裡當動詞，和up組成片語；本題填power。','alt':'can power標正確、can powers標錯，單獨凸顯s的形式差異，不把所有出現food的動詞一律改複數或原形。'},{'heading':'③ 用有無can的兩個結構做對照','text':'沒有can的現在簡單式，可說Most of the food powers up ...。本題有can，則是Most of the food can power up ...，只保留原形power。','alt':'同一food情境分沒有can的powers與有can的power兩卡，明確是句型對照示例，原題can仍保留。'}],'fourth':{'answer':'填 power：can power up the brain','points':['先找空格前的can，不只看主詞。','can＋原形power，不加s。','沒有can的powers與本題有can的power要分清。']},'rationale':'實看第7頁22題完整句、括號power及手寫powers，來源94行全文前已讀；源文僅摘要can play/助動詞原形規則，未含本題power逐字解析。新精確SVG對照主詞線索與can優先控制動詞形式，適合解釋本題誤加s，避免人物食物圖讓人誤以為題目在判斷營養醫療效果。答案power不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-194-source-1aec0fb64a.jpg','site/dist/sources/gemini-m6pmkxQwUTM8.txt lines 38–40 (general modal/base-form rule; entire source read for q-186)'],'sourceUrl':'https://share.gemini.google/m6pmkxQwUTM8','sources':[{'url':'https://dictionary.cambridge.org/uk/grammar/british-grammar/infinitives-','note':'本輪官方搜尋結果完整無to原形段列can等情態助動詞後用原形；僅記搜尋核對。'}],'generationMethod':'precise native SVG modal base-form override contrasted with subject-only present-simple agreement','answerCheckedAgainst':'Most of the food單數，但can要求原形power，不用powers；現有原卷及題庫正確訂正一致。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-194.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
