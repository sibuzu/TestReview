import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,21,'稱讚你很體貼',17)
r(18,43,164,43,'#e6edf3');t(100,65,'nice of you',22)
s.append('<path d="M100 88V105M100 105H55V121M100 105H145V121" fill="none" stroke="#608a72" stroke-width="2"/>')
r(14,123,82,53,'#dcebdc');t(55,140,'walk',20);t(55,162,'Lucky',17)
r(105,123,82,53,'#f0e6d6');t(146,140,'prepare',17);t(146,162,'food',18)
t(300,21,'兩件好意行為並列',17)
r(219,46,162,43,'#dcebdc');t(300,67,'to walk Lucky',19)
t(300,111,'and',20)
r(219,135,162,43,'#dcebdc');t(300,157,'to prepare food',18)
t(500,21,'兩格必須一起核對',16)
for y,label,left,right,c in [(51,'B','for ×','prepare ✓','#f1e7da'),(117,'D','of ✓','to prepare ✓','#dcebdc')]:
 r(416,y,168,51,c);t(500,y+15,label+'：'+left,17);t(500,y+37,right,16)
t(500,185,'B錯在第一格',15,c='#9b6949')
s.append('</svg>');Path('docs/comics/art/q-451.svg').write_text(''.join(s))
x={'id':'q-451','subject':'English','title':'nice of you稱讚人，兩件行為用平行結構','art':'docs/comics/art/q-451.svg','protectedWords':['nice of you','Lucky','to walk','to prepare','prepare','prepared','preparing','平行結構','不定詞','for'],'panels':[{'heading':'① nice是在稱讚對方的體貼行為','text':'你在我不在城裡時幫忙遛Lucky、準備食物，真是體貼。此處用It was nice of you to V，第一格選of；不是在說這件事對你有什麼好處。','alt':'nice of you稱讚卡分到遛Lucky與準備食物兩項行為，標示同一位好心幫忙者，不把nice誤解成狗的外貌。'},{'heading':'② to walk與to prepare兩件事並列','text':'遛狗與準備食物都承接前面的to V。D的to prepare和to walk形成平行結構；prepared或preparing不適合直接放進這裡的並列位置。','alt':'to walk Lucky及to prepare food上下並列，中間and，兩個不定詞用同色，沒有把主句was誤套成每一動詞都要過去式。'},{'heading':'③ B的prepare可省to，但for不合本意','text':'and後第二個to可以省略，所以prepare本身可以與前面的to walk並列。B仍不選，錯在for；D的of與to prepare兩格都正確。','alt':'B選項第一格for標錯而prepare標可用；D的of與to prepare都標可用，避免教成第二個to永遠不可省略。'}],'fourth':{'answer':'答案 D：of；to prepare','points':['稱讚人的體貼：nice of＋人＋to V。','to walk與to prepare構成平行結構。','B錯在for，不能把prepare單獨判錯。']},'rationale':'完整實看原卷38題兩句對話及四組選項，來源1110–1205行本題解說實讀。新原生SVG聚焦稱讚對象、兩項並列行為與雙空同時核對。保留既有詳解第二個to可省的正確界線，英國文化協會教師正文範例支持省略重複to；D答不變，不擴大為所有nice for一概錯。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-451-source-953d139879.jpg','site/dist/sources/6ae053e4-e970-83ee-b3d3-0c236904b680.txt lines 1110–1205'],'sourceUrl':'https://chatgpt.com/share/6ae053e4-e970-83ee-b3d3-0c236904b680','sources':[{'url':'https://learnenglish.britishcouncil.org/free-resources/grammar/english-grammar-reference/verbs-followed-infinitive','note':'實讀官方教師Peter M.回覆199–210行，說明省略重複to，並例示and並列後可省to。'},{'url':'https://dictionary.cambridge.org/uk/grammar/british-grammar/infinitives-','note':'官方搜尋結果完整說明to-infinitive為to加原形；未宣稱已讀網頁正文。'}],'generationMethod':'precise native SVG praise-target mapping and parallel-infinitive comparison','answerCheckedAgainst':'稱讚對方體貼nice of you；to walk and to prepare並列。B的prepare可省to但for不合本題，C的prepared不平行，D正確。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-451.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
