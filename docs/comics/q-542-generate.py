import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#467b5a"/></marker></defs>']
def rect(x,y,w,h,fill='#faf8ee',r=7):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="#b7c9bd"/>')
def t(x,y,st,size=16,c='#2e4c3b',wt=500):s.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="Noto Sans CJK TC,sans-serif" font-size="{size}" fill="{c}" font-weight="{wt}">{escape(st)}</text>')
for i in range(3):rect(i*200+2,2,196,196)
t(100,20,'比較同一欄：籍貫',15,wt=700)
for y,label,quote,c in [(39,'甲','不知何許人','#e6edf3'),(108,'乙','愛州日南人','#e4eddf')]:
 rect(16,y,168,52,c);t(35,y+26,label,20);t(116,y+26,quote,16)
t(100,182,'未詳記 ／ 具體地名',15,c='#397d56')
t(300,21,'家庭記載能相容',16,wt=700)
rect(216,40,168,44,'#e6edf3');t(300,62,'甲：母老家貧',17)
rect(216,95,168,44,'#e4eddf');t(300,111,'乙：母老',17);t(300,131,'賴祿而養',16)
t(300,169,'詳略不同 ≠ 全不可信',14,c='#9c6744')
t(500,21,'受器重 ≠ 已晉升',16,wt=700)
rect(420,42,160,40,'#e4eddf');t(500,62,'德宗器之',19)
s.append('<path d="M500 84V109" stroke="#9d7855" stroke-width="2" stroke-dasharray="3 4"/>');t(500,99,'?',17,c='#9d7855')
rect(420,115,160,40,'#f1e6d6');t(500,135,'因此晉升高官？',17)
t(500,182,'原段未明寫這個結果',14,c='#9c6744')
s.append('</svg>');Path('docs/comics/art/q-542.svg').write_text(''.join(s))
spec={'id':'q-542','subject':'Chinese','title':'比較明文與詳略，不替史料補因果','art':'docs/comics/art/q-542.svg','protectedWords':['姜公輔','不知何許人','愛州日南人','母老家貧','賴祿而養','德宗器之','受器重','晉升高官','籍貫','貪慕富貴','詳略'],'panels':[{'heading':'① 同一項資料，並排才能比較','text':'甲只說不知何許人，未詳記籍貫；乙明寫愛州日南人，有具體地名。因此A比較地理資訊的精確與具體程度，能直接得到兩文支持。','alt':'籍貫欄甲不知何許人對乙愛州日南人，並排兩筆原句；沒有虛構古今地圖位置或現代行政對應。'},{'heading':'② 省略或詳略不同，不等於互相否定','text':'甲的母老家貧，與乙的母老、賴祿而養可以相容。不能因乙較簡略就說甲完全不可信；為養母而求兼官，也不足以斷定貪慕富貴。','alt':'兩筆家庭描述卡保留原句並列，未畫互相矛盾符號，不將求薪俸虛構成貪財劇情。'},{'heading':'③ 器重有寫，不代表晉升結果也寫了','text':'乙的德宗器之確實支持受器重，但這段沒有明寫因此晉升高官。D把一個有根據的前半句，接上未明示的結果與因果，推論超出本文。','alt':'德宗器之已記載卡與因此晉升高官問號卡，兩者間斷線問號表示缺證據，非已成立升遷箭頭。'}],'fourth':{'answer':'答案 A：乙的籍貫記載更具體','points':['比較同一項目，不把沒寫當成否定。','求兼官奉養母親，不等同貪慕富貴。','分清楚明文、合理推論與自行補上的因果。']},'rationale':'完整實看甲乙原卷與第30題全部四選項，讀原AI全文白話。比較題以文本證據為界：籍貫詳略、家庭相容、器重與晉升因果不混用。新製原生SVG並排來源與缺證據流程，不重演虛構歷史場景、不定位愛州日南現代地圖，A答不變，左右拾遺原文各異照留。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-542-reading-source-4549729fd5.jpg','site/dist/assets/questions/q-542-source-0ff45add7f.jpg','site/dist/sources/gemini-VAh0FUGIfRrM.txt (entire original source)'],'sourceUrl':'https://share.gemini.google/VAh0FUGIfRrM','generationMethod':'precise native SVG source comparison and unsupported-causation distinction','answerCheckedAgainst':'甲不知何許/乙愛州日南直接支持A。B全否定無據，C誤加貪念，D後半已晉升高官未明寫；題庫正確，不新增訂正。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-542.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
