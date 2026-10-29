from pathlib import Path
import json,hashlib
art=Path('docs/comics/art/q-812.svg');p=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-label="A同義重複，B受事重複，C動詞搭配三種語病對照"><style>text{font-family:"Noto Sans CJK TC",sans-serif;text-anchor:middle;fill:#274b48}.h{font-size:24px;font-weight:700}.w{font-size:25px;font-weight:600}.s{font-size:20px}.bad{fill:#a65746}.good{fill:#3c7659}</style><rect width="900" height="300" fill="#faf8ed"/>']
def box(x,y,w,h,words,color='#e7eee0',tc='good',size=25):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}"/><text x="{x+w/2}" y="{y+h/2+size*.36}" class="w {tc}" style="font-size:{size}px">{words}</text>'
p.append('<g id="a"><text x="150" y="35" class="h">A　同義重複</text>')
p.append(box(38,64,224,54,'發自內心','#f0e3dc','bad'));p.append(box(38,133,224,54,'由衷','#f0e3dc','bad'));p.append('<path d="M55 205 H245" stroke="#8c9c88" stroke-width="2"/><text x="150" y="237" class="s">同樣表達出於本心</text><text x="150" y="272" class="w good">擇一即可</text></g>')
p.append('<g id="b" transform="translate(300 0)"><text x="150" y="35" class="h">B　受事表達重複</text>')
p.append(box(25,64,250,54,'被挨罵','#f0e3dc','bad'));p.append('<text x="150" y="153" class="s">可改為</text>');p.append(box(25,172,250,47,'一定挨罵'));p.append(box(25,235,250,47,'一定被責罵'));p.append('</g>')
p.append('<g id="c" transform="translate(600 0)"><text x="150" y="35" class="h">C　動詞搭配不當</text>');p.append(box(25,64,250,54,'恢復身體疲勞','#f0e3dc','bad',24));p.append('<text x="150" y="153" class="s">可改為</text>');p.append(box(25,172,250,47,'消除身體疲勞',size=24));p.append(box(25,235,250,47,'恢復體力'));p.append('</g></svg>');art.write_text(''.join(p))
d={'id':'q-812','subject':'Chinese','title':'分清同義重複、受事重複與動詞搭配','art':str(art),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-812-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① A：發自內心與由衷，語意重複','text':'由衷已含出於內心、真誠的意思，再接發自內心，表達重複。可刪一個，寫我由衷感謝父母的照顧，或我發自內心感謝父母的照顧；不必把兩個意思相同的修飾疊用。','alt':'全新精確SVG把原A發自內心與由衷分兩框，標同樣出於本心、擇一，未變更原選項。'},
{'heading':'② B：原題是被挨罵，不能漏掉被字','text':'挨罵本身就是受責罵，再加被，受事表達重複。原題一定被挨罵，可改成一定挨罵，或一定被責罵。這裡要分析原卷的被挨罵，不能先改成一定被罵，再判原句沒有語病。','alt':'全新精確SVG保留原B被挨罵為檢查對象，兩可改句一定挨罵/一定被責罵分框，未把被挨罵偷換成被罵。'},
{'heading':'③ C：要恢復體力，不是恢復疲勞','text':'請假是為了消除疲勞、恢復體力；恢復身體疲勞，反而像要讓疲勞再回來。問題在動詞與後面語詞的搭配，可改消除身體疲勞，或恢復體力，不必改動請假的時間。','alt':'全新精確SVG保留原C恢復身體疲勞，兩改法消除身體疲勞/恢復體力清楚對照，不把疲勞與體力交換含義。'}],
'fourth':{'answer':'答案 D：即使勸說，卻依然明知故犯','points':['D 表達讓步轉折，語意完整，四項中沒有 A～C 的搭配錯誤。','A 檢查同義重複；B 檢查被與挨罵。','C 檢查恢復或消除，後面接的是體力或疲勞。']},
'protectedWords':['發自內心','由衷','語意重複','出於內心','挨罵','被挨罵','被責罵','受責罵','一定挨罵','一定被責罵','受事表達','恢復體力','恢復疲勞','身體疲勞','消除','體力','疲勞','明知故犯','讓步轉折','苦口婆心'],
'originalChecked':{'images':['site/dist/assets/questions/q-812-source-1.jpg'],'visualChecked':True,'answer':'D','notes':'親見17四項與紅改D；B原印一定被挨罵、C恢復身體疲勞均照原分析。既有來源AI誤判訂正卡不重開，原卷D答案沿用。'},
'sourceUrl':'https://gemini.google.com/share/ec6c955b81b3','answerCheckedAgainst':'原卷四項與紅改D，A同義B受事C動受搭配，D讓步轉折語義完整；沿用既已獨立核定D，不重開來源AI舊誤判。',
'references':[{'title':'教育部簡編辭典：由衷','url':'https://dict.concised.moe.edu.tw/dictView.jsp?ID=41283&la=0&powerMode=0','supports':'出於本心、真心誠意，核對A同義重複','access':'官方主文已讀'},{'title':'教育部重編辭典：挨罵','url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=147077&la=0&powerMode=0','supports':'挨罵為受責罵，核對B受事含義','access':'已讀官方搜尋結果全文釋義，不以被罵替換原題被挨罵'}],
'rationale':'三類語病直接標字與兩種改法，以可核對語義結構替代無助於判句的生活畫面；第四格保留D與讓步語意，不重開既有來源AI訂正卡。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'D','bOriginalKept':'一定被挨罵','cOriginalKept':'恢復身體疲勞','correctionsAreSuggestionsNotOriginalReplacement':True,'dClauseDirection':'即使勸說仍故犯','newContentDoubt':False},'artSHA256':hashlib.sha256(art.read_bytes()).hexdigest()};Path('docs/comics/q-812.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
