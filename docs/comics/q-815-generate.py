from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-815.svg');p=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-label="可求與不可求兩條件，對照不義富貴如浮雲"><rect width="900" height="300" fill="#faf8ed"/><style>text{font-family:"Noto Sans CJK TC",sans-serif;text-anchor:middle;fill:#294c48}.h{font-size:26px;font-weight:700}.w{font-size:25px;font-weight:700}.s{font-size:20px}</style>']
def box(x,y,w,h,t,c='#e5eddf'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="13" fill="{c}"/><text x="{x+w/2}" y="{y+h/2+9}" class="w">{t}</text>'
for i in range(3):
 p.append(f'<g id="panel-{i}" transform="translate({300*i} 0)">')
 if i==0:
  p.append('<text x="150" y="38" class="h">如可求</text>');p.append(box(25,65,250,56,'雖執鞭之士','#f0e8d6'));p.append('<path d="M150 128 V159 M143 152 L150 160 L157 152" fill="none" stroke="#8a9d88" stroke-width="3"/>');p.append(box(25,173,250,56,'吾亦為之'));p.append('<text x="150" y="267" class="s">較卑微工作，也願做</text>')
 elif i==1:
  p.append('<text x="150" y="38" class="h">如不可求</text>');p.append(box(25,65,250,56,'從吾所好','#e0eaf0'));p.append('<path d="M150 128 V159 M143 152 L150 160 L157 152" fill="none" stroke="#8a9d88" stroke-width="3"/>');p.append(box(25,173,250,56,'依志趣，不強逐'));p.append('<text x="150" y="267" class="s">不為富貴失去原則</text>')
 else:
  p.append('<text x="150" y="38" class="h">B　最相近</text>');p.append(box(18,65,264,56,'不義而富且貴','#f0e3dc'));p.append(box(18,136,264,56,'於我如浮雲','#e0eaf0'));p.append('<path d="M45 213 H255" stroke="#8a9d88" stroke-width="2"/><text x="150" y="248" class="w">重道義，不苟求</text><text x="150" y="280" class="s">不是一概排斥富貴</text>')
 p.append('</g>')
p.append('</svg>');a.write_text(''.join(p))
d={'id':'q-815','subject':'Chinese','title':'富貴要有取捨，不為富貴失去原則','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-815-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 如可求：不是一概拒絕富貴','text':'可求時，雖執鞭之士，吾亦為之，表示即使是較卑微的工作，也願意去做。不能把整段讀成厭棄一切富貴；先保留這個可求的條件，再看後半句如何選擇。','alt':'全新精確SVG將原文如可求/雖執鞭之士/吾亦為之依條件連接，不畫鞭打他人或臆造孔子實際受雇事件。'},
{'heading':'② 如不可求：從吾所好，不勉強追逐','text':'不可求時，便依自己的志趣，不勉強追逐。這組取捨著重追求富貴仍要有原則；A 和 D 談勤勞、勤儉能致富，並沒有回答不可求時如何自處。','alt':'全新精確SVG如不可求/從吾所好/依志趣不強逐的條件關係，不等同懶惰不做事或所有求富貴皆不義。'},
{'heading':'③ 不義富貴如浮雲，最貼近這項原則','text':'B 著重富貴若不合道義，便不強求，最接近題幹的取捨態度。C 談富貴短暫、名聲長存，焦點不同；不是字句都提到富貴，就能概括孔子在本段的意思。','alt':'全新精確SVG保留B不義而富且貴/於我如浮雲原句，標重道義不苟求，不把浮雲畫成金錢飛走或解釋成所有富者不義。'}],
'fourth':{'answer':'答案 B：不義而富且貴，於我如浮雲','points':['可求與不可求，是理解前後兩句的關鍵條件。','既非排斥所有富貴，也非只談勤勞致富。','重道義、不苟求，最符合四選項中的 B。']},
'protectedWords':['富貴','如可求','如不可求','執鞭之士','吾亦為之','從吾所好','取捨','志趣','原則','勤勞','勤儉','道義','不苟求','不義','名聲長存','孔子','可求','不可求','強求'],
'originalChecked':{'images':['site/dist/assets/questions/q-815-source-1.jpg'],'visualChecked':True,'answer':'B','notes':'親見23完整問句引文/四項與紅改B。兩個如條件與從吾所好對讀，既有B取捨原則沿用，不另加歷史受雇或階級指涉。'},
'sourceUrl':'https://gemini.google.com/share/ec6c955b81b3','answerCheckedAgainst':'原卷可求/不可求的條件與四項主題比較，B重不義與取捨，A/D勤勞勤儉、C名聲長存焦點不同；沿用既已核定B。',
'rationale':'兩條件和B核心三格結構圖，精確呈現不一概拒富貴、不苟求的語意；避免畫執鞭成暴力或臆造人物事件。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'answer':'B','conditionalPhrasesKept':['如可求','如不可求'],'allWealthRejected':False,'allWealthIsUnjust':False,'wealthPursuitWithoutPrinciplesEndorsed':False,'whippingOrActualEmploymentInvented':False,'CIsAboutLongLastingReputation':True},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-815.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
