import json,datetime
from pathlib import Path
from xml.sax.saxutils import escape
s=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">']
def r(x,y,w,h,c='#faf8ee'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c}" stroke="#b9cbbf"/>')
def t(x,y,v,z=17,c='#2d4d3a'):s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC,sans-serif" font-size="{z}" text-anchor="middle" dominant-baseline="middle" fill="{c}">{escape(v)}</text>')
for i in range(3):r(i*200+2,2,196,196)
t(100,22,'不能只抓「颱風」',17)
s.append('<path d="M54 67C49 44 75 35 88 49C98 26 128 35 133 55C155 50 165 77 145 88H59C41 87 39 71 54 67Z" fill="#bbcbd2"/><path d="M30 107H132Q151 107 143 98M44 124H164Q181 124 170 113M23 141H103" fill="none" stroke="#7b969b" stroke-width="3"/>')
t(100,173,'很多物品都可能被吹倒',14)
t(300,22,'後句：過馬路留意來車',15)
s.append('<path d="M232 60H368V126H232Z" fill="#82969b"/><path d="M241 92H359" stroke="#fffbe9" stroke-width="2" stroke-dasharray="14 8"/>')
s.append('<rect x="250" y="72" width="45" height="20" rx="5" fill="#dce7da"/><circle cx="259" cy="94" r="5" fill="#4f6667"/><circle cx="286" cy="94" r="5" fill="#4f6667"/>')
for x in [331,340,349]:s.append(f'<path d="M{x} 63V83M{x} 102V122" stroke="#fffbe9" stroke-width="5"/>')
t(300,156,'哪種損壞最能解釋？',16);t(300,181,'看前後因果',16)
t(500,22,'traffic lights',20)
s.append('<path d="M480 142V116" stroke="#748984" stroke-width="7"/><g transform="translate(480 116) rotate(65)"><path d="M0 0V-48" stroke="#748984" stroke-width="7"/><rect x="-13" y="-109" width="26" height="64" rx="5" fill="#526966"/><circle cx="0" cy="-96" r="7" fill="#91a1a0"/><circle cx="0" cy="-77" r="7" fill="#91a1a0"/><circle cx="0" cy="-58" r="7" fill="#91a1a0"/></g>')
t(500,163,'號誌倒下，失去指引',16)
t(500,186,'So：連起前後原因',14,c='#9b6d48')
s.append('</svg>');Path('docs/comics/art/q-014.svg').write_text(''.join(s))
x={'id':'q-014','subject':'English','title':'So前後要有因果，找與過馬路相連的號誌','art':'docs/comics/art/q-014.svg','protectedWords':['typhoon','knocked down','So','traffic lights','motorcycles','過馬路','因果關係','交通號誌'],'panels':[{'heading':'① 颱風會吹倒東西，還不夠選答案','text':'只看到typhoon與knocked down，機車似乎也可能被吹倒。但這是兩句相連的題目，不能讀到颱風就停下來，要繼續看後面說什麼。','alt':'雲與風線示意颱風，圖下提醒多種物品都可能被吹倒，不以圖像虛構原題實際災害地點或損壞比例。'},{'heading':'② So提示後句，是前句造成的結果','text':'後一句提醒過馬路要確認沒有車子來。要找哪種物品被吹倒，最能解釋這個特別提醒；重點是車流指引，不是物品是否可能被風吹倒。','alt':'道路、車輛與人行穿越線的抽象圖，只呈現後句過馬路與來車線索，沒有行人衝入車道或錯誤綠燈通行指示。'},{'heading':'③ traffic lights把兩句的意思接起來','text':'traffic lights是交通號誌。號誌倒下無法正常指引車流，所以題目接著提醒注意來車；這個因果最直接。不是說有號誌時就可以不注意車輛。','alt':'傾倒交通號誌三個燈均灰暗，配So因果文字，不出現紅綠同亮或可通行訊號，不充當實際災害通行指引。'}],'fourth':{'answer':'答案 D：traffic lights','points':['颱風、吹倒只是前半句線索。','So連起號誌損壞與過馬路留意來車。','比較哪個選項最能解釋整句因果。']},'rationale':'實看原卷10完整兩句及四選項，讀來源198–212行本題詳細解答。新原生SVG用颱風/道路來車/倒下暗燈號誌三個精確線索建立因果，避免僅背typhoon選機車。未增加受傷或錯誤交通指示；閱讀因果不是號誌正常就不用注意來車。D答不變。','originalMaterialsChecked':True,'originalMaterials':['site/dist/assets/questions/q-014-source-hires-2fb91fd088.jpg','site/dist/sources/gemini-english.txt lines 198–212'],'sourceUrl':'https://share.gemini.google/bNv4UUk9wO1L','generationMethod':'precise native SVG storm clue, road-crossing consequence and dark damaged traffic-light cause','answerCheckedAgainst':'四項可能受風影響但D交通號誌損壞最直接解釋So後過馬路留意來車，原卷B為學生作答，D正確不改。','visualChecked':False,'layoutVersion':'native-fluid-v6','nativeLayout':{'width':'100%','height':'auto','artWidth':180,'fontSize':14,'equalColumnWidths':True,'equalHeightWithinRow':True,'independentRowHeights':True,'singleColumnNaturalHeight':True,'narrowSingleColumn':True},'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('docs/comics/q-014.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
