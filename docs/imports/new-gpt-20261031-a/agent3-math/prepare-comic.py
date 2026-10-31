import json,sys,hashlib
from pathlib import Path
from PIL import Image
p=Path('docs/imports/new-gpt-20261031-a/agent3-math');qid=sys.argv[1];s=json.loads(Path(f'docs/comics/{qid}.json').read_text());art=Path(s['art']);o=Path('.cache/new-gpt-20261031-a-agent3-math-publish');suffix='.svg' if art.suffix=='.svg' else '.webp';f=o/(qid+'-new-art'+suffix)
if suffix=='.svg':f.write_bytes(art.read_bytes())
else:Image.open(art).save(f,'WEBP',quality=88)
target='assets/comics/'+f.name
qpath=p/'questions'/f'{qid}.json';q=json.loads(qpath.read_text());q['teachingComic']={k:s[k] for k in ['title','panels','fourth','protectedWords']};q['teachingComic']['art']=target;qpath.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
a=p/'asset-map.json';rows=json.loads(a.read_text());rows=[x for x in rows if x['targetPath']!=target];rows.append({'sourcePath':str(f),'targetPath':target,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'lossless':suffix=='.svg'});a.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(p/'comics'/f'{qid}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print(qid,target)
