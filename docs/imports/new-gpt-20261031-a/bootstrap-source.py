from pathlib import Path
import json
R=Path('/home/jack/git/TestReview');P=R/'docs/imports/new-gpt-20261031-a'
for d in ['questions','qa','reviews']:(P/d).mkdir(exist_ok=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
source=dict(id='src-more-051',url='https://chatgpt.com/share/6ae5b2dc-89a8-83e8-9d82-7bb25a2a1174',title='第6題錯題解析',date='2026-10-30',dateLabel='首次出題日期',dateBasis='原始user.create_time轉Asia/Taipei，全17User訊息皆10/30；不採分享或匯入日',transcriptPath=str((P/'transcript.txt').relative_to(R)),archivePath=str((P/'archive.json').relative_to(R)),originalImageMapPath=str((P/'original-image-map.json').relative_to(R)),images=[],state='transcribing',excludedContent='只收本次User明確原問；鄰題及來源AI另編延伸/變形/模擬練習不收，來源AI解說圖不沿用')
if not (P/'source.json').exists():dump(P/'source.json',source)
if not (P/'asset-map.json').exists():dump(P/'asset-map.json',[])
if not (P/'manifest.json').exists():dump(P/'manifest.json',dict(sourcePath=str((P/'source.json').relative_to(R)),items=[],duplicates=[],skips=[],pendingConfirmations=[]))
s=(R/'docs/imports/new-gpt-20261029-a/item_helpers.py').read_text().replace('new-gpt-20261029-a','new-gpt-20261031-a').replace('src-more-049','src-more-051').replace("date='2026-10-29'","date='2026-10-30'").replace('已逐字實看原卷、完整上文及全部選項；答案與原卷紅筆及獨立推理對照，未使用來源AI圖。','已實看原卷完整題文、必要材料及全部選項；與原卷訂正及獨立推導對照，未使用來源AI圖。')
(P/'item_helpers.py').write_text(s)
f=(R/'docs/imports/new-gpt-20261029-a/finish-item.py').read_text().replace('new-gpt-20261029-a','new-gpt-20261031-a').replace('src-more-049','src-more-051')
(P/'finish-item.py').write_text(f)
