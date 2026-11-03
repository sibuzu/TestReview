from pathlib import Path
import urllib.request,concurrent.futures,json,datetime
from bs4 import BeautifulSoup
D=Path('docs/imports/new-gpt-20261104-a/legal-evidence');D.mkdir(exist_ok=True)
sets={'B0000001':[12,13,15,75,76,77,148,153,227,758,184,187,213,980,982,967,969],'A0040003':[4,5,18,58,59,'83-2','83-3',55,56,57,35,33],'D0020010':[14,24,57,65,67],'D0020053':[11],'D0020050':[7,30],'S0080034':[2],'A0000001':[107,108,111],'I0020003':[1],'B0010001':[244]}
def fetch(t):
 code,n=t;u=f'https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode={code}&flno={n}'
 try:
  html=urllib.request.urlopen(u,timeout=20).read();s=BeautifulSoup(html,'html.parser');x=s.select_one('.law-reg-content');title=s.title.get_text(strip=True);text=x.get_text('\n',strip=True) if x else s.get_text('\n',strip=True);p=D/f'{code}-{n}.txt';p.write_text(u+'\n'+title+'\n查閱日期2026-11-04\n\n'+text+'\n');return dict(code=code,article=str(n),title=title,url=u,path=str(p),text=text)
 except Exception as e:return dict(code=code,article=str(n),url=u,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(fetch,[(c,n) for c,ns in sets.items() for n in ns]))
(D/'index.json').write_text(json.dumps(dict(checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),checkedDateTaiwan='2026-11-04',articles=rows),ensure_ascii=False,indent=2)+'\n')
for r in rows:print(r['code'],r['article'],r.get('error') or r['text'][:400].replace('\n',' '))
