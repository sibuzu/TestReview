"""Four authored explanatory landscapes, not a reconstructed geographic map."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'docs/comics/art'
HERE = Path(__file__).parent
OUT.mkdir(exist_ok=True)

def svg(body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
<defs>
<linearGradient id="sky" x2="0" y2="1"><stop stop-color="#d5edfa"/><stop offset="1" stop-color="#fff8e9"/></linearGradient>
<linearGradient id="sea" x2="0" y2="1"><stop stop-color="#6dc6df"/><stop offset="1" stop-color="#267896"/></linearGradient>
<linearGradient id="slope"><stop stop-color="#61956a"/><stop offset=".55" stop-color="#a9b184"/><stop offset="1" stop-color="#c6a470"/></linearGradient>
<marker id="blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#187697"/></marker>
<marker id="gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#b77530"/></marker>
</defs><rect width="600" height="600" rx="22" fill="url(#sky)"/>
<g font-family="Noto Sans CJK TC, sans-serif" font-size="30" fill="#23434c" text-anchor="middle">{body}</g></svg>'''

def cloud(x,y,s=1):
    return f'<g transform="translate({x} {y}) scale({s})" fill="#f6fcff" stroke="#91afbd" stroke-width="3"><path d="M-75 35C-120 35-122-17-80-22C-85-65-28-80-9-47C20-90 84-57 70-18C122-12 115 40 70 40H-75Z"/></g>'

def rain(x,y,count=5):
    return ''.join(f'<path d="M{x+19*i} {y}l-12 30" stroke="#2589b0" stroke-width="7" stroke-linecap="round"/>' for i in range(count))

def mountain():
    return '<path d="M0 480H135L220 352L296 266L347 212L395 306L455 354L520 440L600 465V600H0Z" fill="url(#slope)"/><path d="M135 480L220 352L296 266L347 212L395 306L455 354L520 440" fill="none" stroke="#516d56" stroke-width="5"/><path d="M347 212L327 287L359 269L395 306" fill="#dbd9bd" opacity=".8"/>'

body1='''<text x="300" y="48" font-weight="bold">風的名稱看「從哪裡來」</text>
<circle cx="300" cy="290" r="185" fill="#bde4ed" stroke="#4c859b" stroke-width="4"/>
<ellipse cx="300" cy="290" rx="95" ry="185" fill="none" stroke="#73a9bb" stroke-width="3"/>
<path d="M118 255Q300 312 482 255M135 206Q300 253 465 206M175 150Q300 182 425 150M115 320Q300 375 485 320M140 382Q300 425 460 382" fill="none" stroke="#73a9bb" stroke-width="3"/>
<path d="M132 210Q300 253 468 210L482 255Q300 312 118 255Z" fill="#e7c76d" opacity=".8"/>
<path d="M132 257Q300 312 468 257" fill="none" stroke="#fff5c7" stroke-width="4"/>
<path d="M125 245Q265 235 417 196" fill="none" stroke="#187697" stroke-width="14" marker-end="url(#blue)"/>
<text x="64" y="298" font-size="40" font-weight="bold">西</text><text x="538" y="236" font-size="40" font-weight="bold">東</text>
<text x="300" y="516" font-weight="bold">北半球中緯度：西風帶</text>
<text x="300" y="558" font-size="24">風帶位置示意，非當日天氣圖</text>'''

body2='<text x="300" y="48" font-weight="bold">濕空氣遇山地抬升</text>'+mountain()+'''
<path d="M0 477H140V600H0Z" fill="url(#sea)"/>
<path d="M12 510q22-15 44 0t44 0M0 548q22-15 44 0t44 0t44 0" fill="none" stroke="#b9e9ef" stroke-width="5"/>
<path d="M30 355C145 355 211 284 278 210" fill="none" stroke="#187697" stroke-width="14" marker-end="url(#blue)"/>
<path d="M28 410C142 410 205 355 248 298" fill="none" stroke="#187697" stroke-width="9" marker-end="url(#blue)"/>
<text x="84" y="455" font-size="27">海上水氣</text><text x="175" y="184" font-size="29">抬升、冷卻</text>'''+cloud(334,130,.7)+rain(280,165,5)+'''
<text x="390" y="527" font-weight="bold">亞特拉斯山地</text>
<text x="380" y="567" font-size="23">機制剖面；非比例、非特定測站</text>'''

body3='<text x="300" y="48" font-weight="bold">山地兩側，雨量可有差異</text>'+mountain()+cloud(240,155,.8)+rain(178,197,6)+'''
<path d="M25 310C104 303 150 257 179 216" fill="none" stroke="#187697" stroke-width="12" marker-end="url(#blue)"/>
<path d="M365 175C418 200 476 287 548 308" fill="none" stroke="#b77530" stroke-width="11" marker-end="url(#gold)"/>
<path d="M454 355L520 440L600 465V600H417Z" fill="#d7b881" opacity=".65"/>
<text x="126" y="423" font-weight="bold">迎風側</text><text x="492" y="423" font-weight="bold">背風側</text>
<text x="142" y="535" font-size="26">降水較有利</text><text x="463" y="535" font-size="26">水氣已減少</text>
<text x="300" y="577" font-size="23">不代表每個國家、每個地點都多雨</text>'''

body4='<text x="300" y="48" font-weight="bold">部分降水匯集成水源</text>'+mountain()+cloud(285,132,.75)+rain(213,175,6)+'''
<path d="M277 299Q252 337 243 365Q228 386 212 415Q191 441 183 475Q168 504 191 526Q222 559 277 600" fill="none" stroke="#307fac" stroke-width="15" stroke-linecap="round"/>
<path d="M205 366Q218 404 212 415M282 388Q260 423 207 447M131 465Q150 485 177 490" fill="none" stroke="#53a7c4" stroke-width="7" stroke-linecap="round"/>
<path d="M0 480H110V600H0Z" fill="url(#sea)"/>
<path d="M38 333C123 326 179 258 212 213" fill="none" stroke="#187697" stroke-width="10" marker-end="url(#blue)"/>
<text x="90" y="290" font-size="25">西風帶來水氣</text>
<text x="435" y="491" font-size="28">溪流、水源</text>
<path d="M382 481L230 507" stroke="#23434c" stroke-width="3"/>
<text x="398" y="559" font-size="23">新製匯流示意，非實際河道</text>'''

for i,b in enumerate([body1,body2,body3,body4],1):
    (OUT/f'q-1065-four-image-v2-panel-{i}.svg').write_text(svg(b))

imgs=[f'docs/comics/art/q-1065-four-image-v2-panel-{i}.svg' for i in range(1,5)]
spec=dict(id='q-1065',subject='Geography',title='西風送來海上水氣，山地抬升形成降水',art=imgs[0],panels=[
 dict(heading='① 西風是從西側吹來的風',text='第一圖以風向箭頭和北半球中緯度風帶示意盛行西風。題目位置是北非地中海沿岸，冬半年可受西風帶影響。',caption='新製風帶概念圖｜箭頭表示來向，不是實際地圖或當日預報。',alt='球面中緯度帶與由西側吹向東側的箭頭，左右標明西與東。',image=imgs[0]),
 dict(heading='② 海上濕氣遇山抬升、冷卻',text='第二圖畫海洋與山地剖面：帶水氣的氣流被地形迫使上升，冷卻後可凝結成雲、形成降水。這是亞特拉斯山地截留部分水氣的機制。',caption='新製機制剖面｜箭頭由海洋移入並沿迎風坡抬升。',alt='藍色氣流從海洋向山地抬升，迎風坡上方有雲和雨線；山地非實際剖面比例。',image=imgs[1]),
 dict(heading='③ 有地形雨，不代表全國都多雨',text='第三圖比較迎風與背風：迎風側較有利於降水，越過山地後水氣可能減少。不能把題幹的寶貴水源，理解成突尼西亞、阿爾及利亞所有地點都很濕潤。',caption='新製兩側比較｜只示地形效應，不給虛構雨量數值。',alt='迎風側以藍色氣流、雲雨表示較有利降水；背風側為水氣減少的氣流及較乾燥山坡。',image=imgs[2])
],fourth=dict(answer='答案 D：盛行西風',points=['第四圖以降水沿山坡匯成溪流，連結題幹的寶貴水源。','選項A、B、C是季風名稱；本題要辨認中緯度盛行風帶。','先判位置與風帶，不能只因來自海上，就套成亞洲西南季風。'],image=imgs[3],alt='西風從海洋帶來濕氣，山坡降水沿分支匯為溪流；河道為新製教學示意。'),protectedWords=['盛行西風','西風帶','亞特拉斯山地','阿爾及利亞','突尼西亞','地形雨','迎風側','背風側'],generationMethod='four authored native SVG wind-belt, mountain-airflow, rain-shadow and catchment diagrams',generatorFile='docs/comics/biology-rework-20261112/q-1065/generate.py',sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/assets/originals/q-1065-original-cad68550fbab.jpg'],answerCheckedAgainst='已實看完整原卷第16題及四選項；北非亞特拉斯山地攔截海上濕氣，原答案D盛行西風保持。',rationale='原先為文字流程框；四張新製實際概念圖分別表示風帶來向、地形抬升、迎背風差異與降水匯流。不畫未查證國界、特定河川或量測數據，不新增原題條件。',producerAgent='/root/comic_lane_1',visualChecked=False,sources=[dict(url='https://eol.jsc.nasa.gov/Collections/EarthObservatory/articles/WetAndDryMorocco.htm',support='NASA/JSC：大西洋西風帶來水氣，Atlas隔開較濕沿岸與撒哈拉；山地有雨影效應。'),dict(url='https://gpm.nasa.gov/resources/faq/what-effect-do-mountainous-orographic-regions-have-measuring-precipitation',support='NASA GPM：氣流被地形迫升、冷卻，可增強降水。'),dict(url='https://www.adaptation-undp.org/explore/arab-states/tunisia',support='UNDP：突尼西亞北部地中海氣候冬季較有雨，其他區域為半乾旱或沙漠；不能概括全國多雨。'),dict(url='https://oceanservice.noaa.gov/facts/horse-latitudes.html',support='NOAA：副熱帶向高緯度的氣流為盛行西風；圖示風帶是概念而非固定天氣。')])
(ROOT/'docs/comics/q-1065.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
