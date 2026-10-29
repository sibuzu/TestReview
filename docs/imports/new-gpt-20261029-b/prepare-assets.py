import json,hashlib
from pathlib import Path
from PIL import Image
P=Path('docs/imports/new-gpt-20261029-b');R=Path('.cache/new-gpt-20261029-b-originals');O=Path('.cache/new-gpt-20261029-b-publish');O.mkdir(exist_ok=True)
assets=[]
def save(im,name):
 f=O/name;im.save(f,'WEBP',lossless=True);src='assets/originals/'+name;assets.append({'sourcePath':str(f),'targetPath':src,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'lossless':True});return src
original=[]
for i in range(1,16):
 im=Image.open(R/f'original-{i:02}.png')
 if i==3:im=im.crop((0,0,777,179))
 if i==8:im=im.crop((0,25,790,265))
 original.append(save(im,f'src-more-050-original-{i:02}.webp'))
map_by_id={851:[1],853:[2],855:[3],857:[4],859:[5],861:[6,7],863:[8,9],865:[10,11],867:[12],869:[13],871:[14],873:[15]}
figs={851:(1,(585,12,804,249),'印度甲乙丙丁作物分區原圖'),855:(3,(590,0,770,178),'印度年雨量分布原圖，保留甲乙位置及圖例'),859:(5,(651,4,788,153),'睡蓮、黃麻葉及稻穗組成的原卷國徽'),863:(8,(578,82,781,261),'原卷勒克瑙位置圖；只裁必要地圖，不重繪'),865:(10,(577,0,771,182),'同組原卷勒克瑙位置圖'),867:(12,(441,0,774,248),'2023年底CPTPP正式成員分布原圖'),869:(13,(510,0,775,181),'2011年各國GDP與累積人口百分比原圖，含甲乙丙丁及世界平均線'),871:(14,(512,0,781,207),'印度熱浪範圍、死亡人數及最高氣溫原圖')}
for n,origins in map_by_id.items():
 f=P/'questions'/f'q-{n}.json';q=json.loads(f.read_text());q['images']=[original[i-1] for i in origins]
 if n in figs:
  ix,box,alt=figs[n];fig=Image.open(R/f'original-{ix:02}.png').crop(box);src=save(fig,f'q-{n}-given.webp');q['questionFigures']=[{'src':src,'alt':alt,'caption':'原卷作答附圖'}]
 f.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
(P/'asset-map.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n');print(len(assets),'lossless assets staged, shared assets untouched')
