import json
from pathlib import Path
P=Path('docs/imports/new-gpt-20261029-b')
def write(n,title,paneldata,answer,points,words,rationale):
 q=json.loads((P/'questions'/f'q-{n}.json').read_text());s={'id':q['id'],'subject':q['subject'],'title':title,'art':f'docs/comics/art/q-{n}.svg','layoutVersion':'native-fluid-v6','panels':[{'heading':h,'text':t,'alt':a} for h,t,a in paneldata],'fourth':{'answer':answer,'points':points},'protectedWords':words,'sourceUrl':'https://chatgpt.com/share/6ae35d9f-f560-83ee-bbe9-d01ff3be9e33','originalMaterialsChecked':True,'rationale':rationale,'generationMethod':'new exact native SVG diagram; copy and reasoning in HTML'};Path(f'docs/comics/q-{n}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(P/'comics'/f'q-{n}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
write(853,'群島海岸要加總，先看地形成因',[
('① 板塊交會，形成複雜群島背景','印尼位於多個板塊交會地帶，地質作用與島弧、群島地形相關。三色只是構造概念，不是精確的印尼板塊邊界圖。','新製三區板塊交會概念與島弧關聯，明示非實際地圖。'),
('② 多座島嶼，分別有自己的海岸','把同一面積拆成幾個小方塊，就能看出陸地分散後，邊界長度可能增加。這是幾何比較，不代表印尼真的只有四個島。','一個60×60方塊與四個30×30方塊，面積皆3600平方單位。'),
('③ 全部海岸相加，不是只看外圍','示意大方塊周長240；四小塊周長合計480。同樣面積可有不同總邊界。回到題目，B的板塊背景最能連結印尼群島。','等面積比較的所有邊界用棕線標出，周長240與480可直接核算。')],
'答案 B：位板塊交界處',['群島各島的海岸線需要加總。','季風和交通位置不是本題的地形成因。','原題名次依其統計口徑，不作永久排名。'],['板塊交界','群島','海岸線'], '原卷02全文四項實看，B不變；新圖以可計算等面積分塊解釋總海岸，避免只有文字卡。')
write(855,'乙東北雨多，甲西北雨季較短',[
('① 先看甲乙，而不是先背風名','原圖乙在東北、甲在西北；由乙到甲，年雨量由多轉少。方位小圖只幫助記位置，真實雨量及圖例仍看原卷。','新製印度形狀方位概念圖，乙東北、甲西北，不冒充比例地圖。'),
('② 雨季影響時間，乙長甲短','西南季風帶來主要夏雨，東北受影響較早、西北較晚且較早撤退。時間條只表示長短，沒有新增精確日期或日數。','兩條季風影響時間示意，東北乙較長、西北甲較短，無任意日期。'),
('③ 看圖選A，不否認地形也有影響','四項以西南季風持續時間最符合本圖差異。山地也會影響局地降雨，不能把這題解成所有雨量只由季風時間決定。','乙較多、甲較少的兩支雨量概念柱，明示不另編數值。')],
'答案 A：西南季風持續時間的長短',['辨方向：乙東北 → 甲西北。','主要夏雨與西南季風相關。','雨季長短是本題四選一主因，地形仍可能影響局部。'],['西南季風','雨季','東北','西北'],'原卷03甲乙及圖例完整實看，新方位/時間/雨量關係SVG不臆造原圖數值。')
