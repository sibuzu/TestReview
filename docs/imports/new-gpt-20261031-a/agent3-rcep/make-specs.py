from pathlib import Path
import json
P=Path('docs/imports/new-gpt-20261031-a/agent3-rcep');URL=json.loads((P/'source.json').read_text())['url']
I='#35594f';B='#639abc';G='#90b58a';O='#d4a359'
def circle(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{I}" stroke-width="2"/>'
def rect(x,y,w,h,c,r=4):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" stroke="{I}" stroke-width="2"/>'
def line(x,y,x2,y2,c=I,w=2):return f'<path d="M{x} {y}L{x2} {y2}" stroke="{c}" stroke-width="{w}"/>'
def path(d,c=I,fill='none',w=2):return f'<path d="{d}" stroke="{c}" fill="{fill}" stroke-width="{w}"/>'
def network(cx,cy):
 pts=[(cx-32,cy-25),(cx+32,cy-25),(cx-32,cy+25),(cx+32,cy+25)]
 return ''.join(line(cx,cy,x,y,B) for x,y in pts)+circle(cx,cy,9,G)+''.join(circle(x,y,6,B) for x,y in pts)
def writeart(qid,ps):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180">'
 for i,p in enumerate(ps):s+=f'<g transform="translate({i*180} 0)"><rect width="180" height="180" fill="{["#f8f4e9","#eef4ec","#eef3f7"][i]}"/>'+p+'</g>'
 s+='</svg>';p=Path(f'docs/comics/art/q-{qid}.svg');p.write_text(s);return str(p)
a884=writeart(884,[rect(10,25,76,130,'#e4eedc',18)+circle(48,63,12,G)+circle(48,115,10,B)+rect(96,25,74,130,'#e1eaf0',18)+circle(133,63,10,O)+circle(133,115,10,O),line(23,148,161,148)+rect(43,31,29,117,G,0)+rect(107,113,29,35,B,0),rect(15,28,62,121,'#fffaf0')+rect(103,28,62,121,'#e6f0f5')+circle(46,88,17,G)+network(134,88)])
# Precise latitude positions are a coordinate concept, not a border map. Grey equator is y90.
y=lambda lat:90-lat*1.35
p1=rect(12,17,156,146,'#e5f1f7',12)+line(12,90,168,90,'#b5b5a0',3)+circle(43,y(35),5,B)+circle(116,y(36),5,B)+circle(63,y(-25),6,O)+circle(137,y(-41),6,O)
p2=rect(15,18,150,63,'#dae7d6',18)+circle(56,50,7,B)+circle(123,50,7,B)+rect(15,104,150,55,'#f0e0c2',18)+circle(63,131,8,O)+circle(135,131,8,O)
p3=rect(10,20,160,140,'#d9ebf5',10)+path('M10 20H129L136 45L118 70L127 102L104 129L111 160H10Z',I,'#dfe8cf')+circle(61,88,7,O)+path('M54 88l7-7 7 7-7 7Z',I,'#f2ce91')
a888=writeart(888,[p1,p2,p3])
rows={884:('先分區位，再合併人口與語言線索',a884,[('① 南亞先排除東南亞','印度、孟加拉在南亞；越南、菲律賓在東南亞。分類圖不按人口面積比例繪製。','左右兩個區域分類框，南亞兩國與東南亞兩國分開，名稱在HTML。'),('② 南亞內再比人口','印度人口多於孟加拉，符合「南亞人口最多」。長條只表示高低比較，不另編統計數值。','左高右低兩柱，只表示印度人口大於孟加拉的相對關係。'),('③ 前後兩段別混在一起','通行英語是輔助線索；前段甲國是印度，後段RCEP成員則另看原圖，印度不在其中。','兩段文章分開的概念頁：左單一國家，右區域合作網絡。')],'答案 B：印度',['兩個核心條件：南亞＋人口最多。','菲律賓只符合英語線索，不符合區位。','同文提到印度，不代表它是RCEP成員。']),886:('產業名稱先找準，再判斷投入要素','docs/comics/art/q-886-v2.png',[('① 醫藥重視研發與設備','研發、實驗設備、專業人才都需要投入。插畫是現代概念情境，不冒稱特定藥廠實景。','新製成年研究員在實驗室用顯微鏡，無劑量或醫療建議。'),('② 機械重視工程技術','精密零件、設備與製造技術，不能只靠大量廉價勞工完成。','新製成年工程師檢查精密零件，非機械操作教學。'),('③ 兩者共同需要資金與技術','本題比的是文章所指的醫藥、機械，不是由印度人口多就猜所有產業靠廉價勞工。','新製研究員與工程師共同討論原型與設備，代表知識與設備投入。')],'答案 B：需要較高的資金與技術',['回文章找醫藥、機械兩產業。','共同重點是研發、設備與專業技術。','不是說完全不用勞力或每件產品都高價。']),888:('看到「皆」，用反例檢查全體',a888,[('① 澳洲、紐西蘭在南半球','圖中灰線示意赤道；兩個橘點位在南側，因此不是所有成員都在北半球。','緯度概念圖：中國、日本在北，澳洲、紐西蘭在南；點位按代表緯度，不畫國界。'),('② 澳洲、紐西蘭也不在歐亞大陸','兩國屬大洋洲，同時排除「皆在歐亞大陸」；中國、日本等也不是位處印度半島。','大洲分類的上下兩框，上方亞陸範例、下方大洋洲範例，非疆界地圖。'),('③ 臨近不等於每國都臨海','C按圖中的亞太區域分布概括。寮國是內陸國，不能教成每個成員都有太平洋海岸。','抽象陸地與海洋圖，中間內陸點被陸地包圍，非寮國實際國界。')],'答案 C：皆臨近太平洋',['看澳洲、紐西蘭，排除B與D。','A也有中國、日本等反例。','臨近是本題區域概括，不等於直接瀕臨海洋。'])}
for qid,(title,art,pan,ans,pts) in rows.items():
 s={'id':f'q-{qid}','subject':'Geography','title':title,'art':art,'layoutVersion':'native-fluid-v6','panels':[{'heading':a,'text':b,'alt':c} for a,b,c in pan],'fourth':{'answer':ans,'points':pts},'protectedWords':['印度','孟加拉','菲律賓','南亞','東南亞','太平洋','澳洲','紐西蘭','歐亞大陸','RCEP'],'sourceUrl':URL,'originalMaterialsChecked':True,'sourceGeneratedArtUsed':False,'generationMethod':'built-in imagegen fresh wordless anime situations + HTML' if qid==886 else 'new native exact relation/coordinate concept SVG + HTML','rationale':'共同原文章、地圖、全部三子四選項親見並官方核定。逐題自己新製：28區位條件交集，29研發與設備情境，30南半球反例與內陸/臨海區分。'};Path(f'docs/comics/q-{qid}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print('3 new full specs')
