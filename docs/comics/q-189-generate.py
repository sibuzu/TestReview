import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'Each同時通過兩關',17)
r(18,47,164,39,'#dcebdc');t(100,67,'Each of ... ✓',20)
r(18,112,164,39,'#dcebdc');t(100,132,'Each ... is ✓',20)
t(100,179,'可接of，而且是單數',15)
t(300,22,'Every不能直接接of',16)
r(218,46,164,42,'#f1e5db');t(300,67,'Every of ... ×',20,c='#9b6756')
t(300,109,'修正示例',15)
r(218,128,164,44,'#dcebdc');t(300,151,'Every one of ... ✓',16)
t(500,22,'本句women為複數',16)
r(418,44,164,41,'#e6edf3');t(500,65,'Both ... are',20)
r(418,99,164,41,'#e6edf3');t(500,120,'All ... are',20)
t(500,173,'原句卻是 is',19,c='#9b6756')
s.append('</svg>');Path('docs/comics/art/q-189.svg').write_text(''.join(s))
x={'id':'q-189','subject':'English','title':'接of又配is，Each同時符合兩關','art':'docs/comics/art/q-189.svg','protectedWords':['Each','Every','Every one of','Both','All','of the women','is','are','單數','複數'],'panels':[{'heading':'① 先看of the women，再看is','text':'Each可以直接接of the women，主詞指這些女性中的每一位，視為單數，正好配is。兩個線索一起用，Each同時符合，選D。','alt':'Each of及Each搭配is兩項分開打勾，表示句型與主謂一致兩個條件，不使用女性身形圖代替文法判斷。'},{'heading':'② Every不能直接接of','text':'Every雖也可表每個，卻不能寫Every of the women。若改成Every one of the women才是正確結構；原題空格只能填Every，沒有one，所以A不選。','alt':'Every of標叉，下方Every one of標正確且註修正示例，不把補入one後的句子冒稱原題選項。'},{'heading':'③ Both與All在這句指多位，應配are','text':'Both of the women指兩位都，All of the women指這些女性全都，這裡都是複數，應接are。但原句已給is，所以B、C不符合。','alt':'Both與All在women情境配are兩行對照原is；沒有把All用於不可數名詞時也說成必須複數。'}],'fourth':{'answer':'答案 D：Each','points':['Each可直接接of the women。','Each作主詞核心，搭配單數is。','Every需加one；Both、All在本句則應配are。']},'rationale':'實看第1頁練習7原卷完整句及四選項；同來源全文94行在前題已讀，未留本題逐字解析。獨立以of結構與is單數雙條件核D。新精確SVG展示通關/Every補one/本句BothAll複數，不以女性體型示意文法，也不把All一律泛稱複數。答案D不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-189-source-8198f37e1e.jpg','site/dist/sources/gemini-m6pmkxQwUTM8.txt (entire source read with q-186; no exact women question solution archived)'],'sourceUrl':'https://share.gemini.google/m6pmkxQwUTM8','sources':[{'url':'https://dictionary.cambridge.org/grammar/british-grammar/each-or-every.','note':'官方搜尋結果完整列each of／every one of且否定Every of，僅記搜尋核對。'},{'url':'https://dictionary.cambridge.org/uk/grammar/british-grammar/each','note':'本輪官方搜尋結果完整Each of段核單數動詞；僅記搜尋核對，不擴展口語差異。'}],'generationMethod':'precise native SVG two-constraint grammar filter with corrected structural contrast','answerCheckedAgainst':'直接of後接the women且主句is，Each兩條件皆可；Every須one、Both/All women配are，D。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-189.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
