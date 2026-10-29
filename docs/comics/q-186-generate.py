import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'Each：逐一看每張',17)
for x,y in [(25,50),(112,50),(69,118)]:
 r(x,y,62,57,'#e8f0e2');s.append(f'<path d="M{x+10} {y+17}H{x+52}M{x+10} {y+24}H{x+52}M{x+7} {y+34}H{x+55}M{x+13} {y+35}V{y+47}M{x+49} {y+35}V{y+47}" fill="none" stroke="#98795b" stroke-width="4"/>')
t(300,22,'主詞核心是 Each',17)
r(218,43,164,38,'#dcebdc');t(300,63,'Each',23)
r(218,91,164,35,'#e8edf1');t(300,110,'of the benches',18)
r(248,144,104,36,'#dcebdc');t(300,163,'makes',22)
t(500,22,'makes 與 feel分工',16)
r(418,43,164,35,'#dcebdc');t(500,62,'makes',23)
t(500,97,'us',19)
r(418,115,164,35,'#e6edf3');t(500,134,'feel',23)
t(500,179,'comfortable',20)
s.append('</svg>');Path('docs/comics/art/q-186.svg').write_text(''.join(s))
x={'id':'q-186','subject':'English','title':'Each逐一看，makes加s但feel不加','art':'docs/comics/art/q-186.svg','protectedWords':['Each','of the benches','makes','make','feel','feels','comfortable','單數','主詞核心','使役結構'],'panels':[{'heading':'① Each著重這些長椅中的每一張','text':'Each of the benches不是把所有長椅合成一個複數主詞，而是逐一說每一張。圖中分開框住每張長椅，提醒Each的單數觀點，不是只挑其中第一張。','alt':'多張長椅各自一框，示意逐一每張的分配語意；三個圖標僅為示意多張，不新增原題實際數量或只選一張的條件。'},{'heading':'② 動詞跟Each一致，不跟最近的benches走','text':'主詞核心是Each，of the benches只是指出哪一群長椅。雖然benches是複數，主句動詞仍依單數Each用makes，不能只看最靠近空格的字。','alt':'Each與makes同色，of the benches另色置中，將核心和of片語分層，不刪改原主詞或把benches當主句動詞主詞。'},{'heading':'③ makes後面的feel，是使役結構的原形','text':'完整搭配是makes us feel comfortable，讓我們感到舒服。主句makes因Each加s，但make＋受詞＋原形動詞中的feel不加s，不要寫成feels。','alt':'makes、受詞us、原形feel、形容詞comfortable依句序分層，兩個動詞有不同角色，不讓所有動詞一律一起加s。'}],'fourth':{'answer':'選 makes：Each of the benches makes us feel comfortable.','points':['Each作主詞核心，用單數動詞makes。','of the benches的複數不改變Each的配對。','makes us feel：feel在使役結構中保持原形。']},'rationale':'實看第1頁練習3原卷兩圈選形式及完整句。全文94行來源已讀，僅摘要整體主詞一致與網站，沒有本題benches詳細逐字解答；獨立以原卷核Each單數及make受詞原形。新精確SVG用分配長椅/核心與of片語/雙動詞分工，避免人物感覺舒服插圖無法解釋make或makes。答案makes不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-186-source-f221646506.jpg','site/dist/sources/gemini-m6pmkxQwUTM8.txt (entire 94-line text; no exact benches solution in archive)'],'sourceUrl':'https://share.gemini.google/m6pmkxQwUTM8','sources':[{'url':'https://dictionary.cambridge.org/uk/grammar/british-grammar/each','note':'官方搜尋結果完整Each of段說明複數名詞作of片語而主句通常單數；按國中標準主詞一致使用，未擴到口語差異。'},{'url':'https://learnenglish.britishcouncil.org/free-resources/grammar/english-grammar-reference/verbs-followed-infinitive','note':'本輪q451已實讀正文20–25及127–139，make+object+infinitive without to；本句主動用feel原形。'}],'generationMethod':'precise native SVG distributive_each grouping and head-subject versus causative-infinitive structure','answerCheckedAgainst':'Each單數→makes；of the benches為限定群組，make us feel形feel原形，原卷訂正makes與題庫一致。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-186.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
