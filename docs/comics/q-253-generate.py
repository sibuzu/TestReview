from pathlib import Path
import json,datetime,hashlib
p=Path('docs/comics/q-253.json');b=Path('docs/comics/q-253-before-rework.json')
if p.exists() and not b.exists():b.write_bytes(p.read_bytes())
def text(x,y,t,size=22,col='#405c51'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{col}">{t}</text>'
def box(x,y,w,h,fill='#e6eddb'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#91a086" stroke-width="2"/>'
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#a18c5c"/></marker></defs><rect width="1080" height="360" fill="#f7f8ef"/>',text(180,36,'先定位本題時段'),'<path d="M70 65V314" stroke="#94aa90" stroke-width="4"/>']
for y,year,event in [(90,'1912','清帝退位'),(170,'1916','袁世凱去世')]:
 a += [f'<circle cx="70" cy="{y}" r="9" fill="#f7f8ef" stroke="#889b7e" stroke-width="3"/>',text(156,y-3,year,23),text(209,y+25,event,23)]
a += [box(102,235,221,85,'#f0dfb8'),text(213,267,'1917～1925',25,'#a26f31'),text(213,300,'本題：廣東建政',21),'<circle cx="70" cy="276" r="10" fill="#c29756"/>']
# Two text clues converge on the same category, not a geographic border map.
a += ['<g transform="translate(360 0)">',text(180,36,'回文章找共同線索'),box(39,69,282,61),text(180,106,'北方：軍閥林立',23),box(39,155,282,61),text(180,192,'南方：軍閥牽制',23),'<path d="M321 100H340V242L250 263M180 216V263" fill="none" stroke="#a18c5c" stroke-width="3" marker-end="url(#a)"/>',box(65,266,230,61,'#f0dfb8'),text(180,304,'軍閥勢力',25,'#a26f31'),'</g>']
# Period labels are chronology context, not a fabricated portrait or scene.
a += ['<g transform="translate(720 0)">',text(180,36,'人物相同，時期不同')]
for y,period,target in [(66,'清末','反清革命'),(151,'袁世凱掌權時','反袁'),(236,'本題1917～1925','對抗軍閥')]:
 a += [box(28,y,304,66,'#f0dfb8' if y==236 else '#edf0e3'),text(180,y+26,period,19),text(180,y+54,target,23,'#a26f31' if y==236 else '#405c51')]
a += ['</g></svg>'];art=Path('docs/comics/art/q-253.svg');art.write_text(''.join(a))
s={'id':'q-253','subject':'History','title':'先看1917年以後，再找革命對象','art':str(art),'protectedWords':['孫中山','袁世凱','清帝退位','軍閥勢力','北方軍閥','南方軍閥','1917～1925年','1916年','1912年','反清革命'],'panels':[
{'heading':'① 本題在清帝退位、袁世凱去世之後','text':'文章把範圍限定在1917～1925年。清帝已於1912年退位，袁世凱也在1916年去世；不能看到孫中山革命，就把清末或反袁事件搬進來。','alt':'依年代先後的時間軸1912清帝退位、1916袁世凱去世、1917到1925本題建政；非按年月距離比例。'},
{'heading':'② 北方與南方線索，都指向軍閥','text':'文章先說北京軍閥林立、不守國家大法，又說廣州軍政府對抗北方政府；末段提到不願再受制於南方軍閥。共同的對抗對象是軍閥勢力。','alt':'以框與箭頭整合文章北方軍閥、南方軍閥兩類線索，不畫成真實地盤疆界或軍事行軍圖。'},
{'heading':'③ 同一人物，不等於每次目標相同','text':'清末的反清革命、袁世凱掌權時的反袁，以及後來護法與籌備北伐，必須分期。這題要依文章指定年代和內容，不能套用較晚的國共對立。','alt':'清末反清、袁掌權反袁、本題1917到1925對抗軍閥分期卡；不把中國共產黨說成當時完全不存在。'}],
'fourth':{'answer':'答案 B：軍閥勢力','points':['先圈文章限定的年代。','再核對北方與南方軍閥線索。','人物相同，對抗對象仍可能改變。']},'rationale':'已實看完整閱讀原卷與第1題四選項、讀來源原對話；B與文章線索一致。為突出本題核心年代排除法和文本線索，採全新精確時間軸/分類流程SVG，避免虛構孫中山與特定軍閥會面的歷史場景或把後來國共對立提前。不沿用來源AI圖。無新增歷史結論或改答案。','generationMethod':'programmatic SVG original chronological and textual evidence comparison','generatorFile':'docs/comics/q-253-generate.py','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-253-reading-6058f42672.jpg','site/dist/assets/questions/q-253-source-b54ee1dbbb.jpg','site/dist/sources/6ae060b5-29dc-83e8-b329-d1a7781ba070.txt 第1題全文'],'sources':[{'url':'https://sunology.yatsen.gov.tw/legend/','note':'國立國父紀念館中山學術資料庫年表，核對1916袁世凱去世及1917護法背景。'},{'url':'https://edata.nlpi.edu.tw/CNH/event/event.aspx?ID=0000097','note':'國立公共資訊圖書館民國近代史護法紀要，軍閥背景核對。'}],'answerCheckedAgainst':'原文1917至1925、北方軍閥不遵法及南方軍閥牽制，B。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artSha256':hashlib.sha256(art.read_bytes()).hexdigest()};p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
