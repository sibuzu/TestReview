from pathlib import Path
from PIL import Image
p=Path(__file__).parent/'crops';p.mkdir(exist_ok=True)
a=[(8,'q-1112-original',(18,602,1060,807)),(8,'q-1112-figure',(826,604,1045,802)),(9,'q-1113-original',(45,703,1045,865)),(10,'q-1114-original',(40,399,1050,742)),(11,'q-1115-original',(12,779,1080,1040)),(12,'q-1116-original',(24,896,1080,1123)),(13,'q-1117-original',(50,360,1060,600)),(13,'q-1117-figure',(853,390,1045,483)),(14,'q-1118-original',(50,948,1060,1193)),(14,'q-1118-device',(865,949,1045,1065)),(14,'q-1118-options',(144,1072,1015,1190)),(15,'q-1119-original',(44,220,1070,445)),(15,'q-1119-figure',(860,239,1070,349)),(16,'q-1120-passage',(24,817,1065,1097)),(16,'q-1120-original',(43,1177,1065,1304))]
for i,n,b in a:Image.open(f'docs/source-pages/chatgpt-6afb1a9c-{i}.jpg').crop(b).save(p/f'{n}.jpg',quality=95)
