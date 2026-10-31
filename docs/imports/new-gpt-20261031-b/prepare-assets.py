from PIL import Image
from pathlib import Path
import json,hashlib
P=Path('docs/imports/new-gpt-20261031-b');O=Path('.cache/new-gpt-20261031-b-publish');O.mkdir(exist_ok=True);rows=[]
def save(im,name):
 p=O/name;im.save(p,'WEBP',lossless=True);target='assets/originals/'+name;rows.append({'sourcePath':str(p),'targetPath':target,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lossless':True});return target
for n in range(1,12):save(Image.open(f'.cache/new-gpt-20261031-b-originals/user-{n:03}.png'),f'src-more-052-original-{n:02}.webp')
# Actual original plot only; all axes/甲乙 preserved. No redraw, no removal of overlapping original marks.
im=Image.open('.cache/new-gpt-20261031-b-originals/user-009.png');crop=im.crop((460,0,607,107));crop.save('.cache/new-gpt-20261031-b-originals/q-891-given.png');target=save(crop,'q-891-given.webp');qp=P/'questions/q-891.json';q=json.loads(qp.read_text());q['questionFigures']=[{'src':target,'alt':'原卷刑事判決件數圖，甲總數、乙其中告訴乃論件數；縱軸件數、橫軸時間（月）','caption':'原卷作答附圖'}];qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
(P/'asset-map.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
