from PIL import Image
from pathlib import Path
import json,hashlib
P=Path(__file__).parent;(P/'crops').mkdir(exist_ok=True)
boxes={5:(5,(40,795,1075,1070)),6:(6,(35,815,1065,1052)),7:(7,(45,455,1075,690)),8:(8,(20,795,1068,1155)),9:(9,(45,335,1075,568)),10:(10,(35,655,1075,890)),11:(12,(40,160,1078,432)),12:(12,(25,410,1078,700)),13:(13,(80,270,1080,530)),14:(14,(45,450,1075,750)),15:(15,(40,835,1078,1200)),16:(16,(45,260,1078,645)),17:(17,(70,185,1065,480)),18:(18,(45,390,1078,700))}
a=[]
for i,(source,b) in boxes.items():
 p=P/'crops'/f's72-history-{i:02}-original.jpg';Image.open(f'docs/source-pages/chatgpt-6afc7636-{source}.jpg').crop(b).save(p,quality=96)
 a.append(dict(candidateId=f's72-history-{i:02}',sourceImageIndex=source,box=b,path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(P/'crop-records.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
