from pathlib import Path
import concurrent.futures,json,urllib.request,urllib.error,datetime,re
R=Path('/home/jack/git/TestReview')
def run(tag):
 p=R/f'docs/imports/new-gpt-20261031-{tag}';aPath=R/f'docs/acquisition/new-gpt-20261031-{tag}.json';a=json.loads(aPath.read_text());files=json.loads((p/'user-attachment-index.json').read_text());f=next(x for x in files if x.get('fileId'));url=a['url'];sid=url.rsplit('/',1)[-1]
 req=urllib.request.Request(f'https://chatgpt.com/backend-api/share/{sid}/file/{f["fileId"]}',headers={'User-Agent':'Mozilla/5.0','Accept':'application/json','Referer':url})
 result=dict(checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),fileId=f['fileId'],method='public_share_file_endpoint_without_credentials')
 try:
  response=urllib.request.urlopen(req,timeout=20);body=response.read();result.update(httpStatus=response.status,contentType=response.headers.get('Content-Type'),bytes=len(body),metadataReturned=True)
  # A successful metadata response is saved only locally; signed download URLs are not printed.
  cache=R/f'.cache/new-gpt-20261031-{tag}';(cache/'public-first-file-metadata.json').write_bytes(body)
 except urllib.error.HTTPError as e:
  body=e.read().decode(errors='replace');title=re.search(r'<title>(.*?)</title>',body,re.I|re.S);result.update(httpStatus=e.code,contentType=e.headers.get('Content-Type'),pageTitle=title.group(1).strip() if title else None,metadataReturned=False)
 except Exception as e:result.update(error=f'{type(e).__name__}: {e}',metadataReturned=False)
 a.update(checkedAt=result['checkedAt'],state='awaiting_browser_connection',publicImageProbe=result,bridgeFailure='ECONNREFUSED127.0.0.1:9222; no listener/main Chrome process; awaiting user confirmed actual Server running at address',expectedImageCount=17 if tag=='a' else 11,downloadedImages=[],downloadedImageCount=0,visualChecked=False,noTranscriptionStarted=True)
 tmp=aPath.with_suffix('.json.tmp');tmp.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');tmp.replace(aPath)
 print(json.dumps(dict(source=tag,**result),ensure_ascii=False),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,['a','b']))
