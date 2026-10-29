import sys,json,hashlib,datetime
from pathlib import Path
P=Path('docs/imports/new-gpt-20261029-b');qid=sys.argv[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
qpath=P/'questions'/f'{qid}.json';q=json.loads(qpath.read_text());ap=P/'asset-map.json';allassets=json.loads(ap.read_text());needed=set(q['images'])|{x['src'] for x in q['questionFigures']}|{q['teachingComic']['art']};assets=[x for x in allassets if x['targetPath'] in needed];assert len(assets)==len(needed)
vp=P/'qa'/f'{qid}-validation.json';v=json.loads(vp.read_text());assert v['passed'] and len(v['results'])==6
shots=[str(P/'qa'/f'{qid}-app-{kind}-{w}.png') for kind in ['question','comic'] for w in [1440,390]]
assert all(Path(x).exists() for x in shots)
r={'id':qid,'passed':True,'reviewerAgent':'/root/comic_lane_3','checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'questionPath':str(qpath),'questionSHA256':sha(qpath),'automatedValidation':str(vp),'automatedValidationSHA256':sha(vp),'appAndStandaloneWidths':[1440,1120,390],'actualViewed':shots,'actualViewScope':'app完整題目收合畫面及自己新四格，1440/390逐張實看；standalone三寬自動核對，不冒稱實看','completeOriginalAndOptions':True,'necessaryFiguresVisuallyChecked':True,'newComicRawVisuallyChecked':True,'answerDefaultCollapsed':True,'noOverflow':True,'personalCloudRequestsAborted':True,'sourceGeneratedArtUsed':False,'newSubstantiveIssues':[]}
rp=P/'qa'/f'{qid}-reviewed.json';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
item={'id':qid,'sourceId':'src-more-050','questionPath':str(qpath),'questionSHA256':sha(qpath),'specPath':f'docs/comics/{qid}.json','specSHA256':sha(f'docs/comics/{qid}.json'),'qaReport':str(rp),'qaReportSHA256':sha(rp),'status':'ready','assets':assets,'readyAt':r['checkedAt']}
(P/'items').mkdir(exist_ok=True);ip=P/'items'/f'{qid}-manifest.json';assert not ip.exists(),'Item already frozen';ip.write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n')
mp=P/'manifest.json';m=json.loads(mp.read_text()) if mp.exists() else {'sourcePath':str(P/'source.json'),'items':[],'duplicates':[],'skips':[],'pendingConfirmations':[]};assert not any(x['id']==qid for x in m['items']);m['items'].append(item);mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(ip)
