#!/usr/bin/env python3
"""Read-only inventory; writes only this review directory, never changes bank."""
import json,re,unicodedata,hashlib,itertools,collections,difflib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('/home/jack/git/TestReview');OUT=ROOT/'docs/imports/group-review';data=json.loads((ROOT/'site/dist/data.json').read_text());qs=data['questions'];by={q['id']:q for q in qs};sources={s['id']:s for s in data['sources']}
def norm(x):
 s=unicodedata.normalize('NFKC',x or '').lower();return ''.join(c for c in s if c.isalnum())
def h(x):return hashlib.sha256(x.encode()).hexdigest()
def qnum(k):return int(k.split('-')[-1])
def info(k):
 q=by[k];return {'id':k,'title':q['title'],'subject':q['subject'],'sourceId':q['sourceId'],'sourceURL':sources.get(q['sourceId'],{}).get('url'),'sourceLabel':q.get('sourceLabel'),'date':q.get('date'),'passageChars':len(q.get('passage','')),'hasOwnComic':bool(q.get('teachingComic')),'alreadyGrouped':bool(re.search(r'題組|【原卷第\d+題】[\s\S]*【原卷第\d+題】',q.get('title','')+'\n'+q.get('question',''))),'contentFingerprint':h(json.dumps({k:q.get(k) for k in ['question','passage','tables','questionFigures','answer','explanation','optionAnalysis']},ensure_ascii=False,sort_keys=True))}
asset_cache={};missing=[]
def asset_hash(src):
 if src not in asset_cache:
  p=ROOT/'site/dist'/src
  if p.is_file():asset_cache[src]=hashlib.sha256(p.read_bytes()).hexdigest()
  else:asset_cache[src]=None;missing.append(src)
 return asset_cache[src]
pairs=collections.defaultdict(list)
def edge(a,b,t,details):
 if a==b:return
 key=tuple(sorted([a,b],key=qnum));e={'type':t,**details}
 if e not in pairs[key]:pairs[key].append(e)
def grouped_index(vals,t):
 result=[]
 for value,members in vals.items():
  members=sorted(set(members),key=qnum)
  if len(members)<2:continue
  rec={'fingerprint':value,'questionIds':members};result.append(rec)
  for a,b in itertools.combinations(members,2):edge(a,b,t,{'fingerprint':value})
 return sorted(result,key=lambda g:qnum(g['questionIds'][0]))
ps=collections.defaultdict(list);tb=collections.defaultdict(list);fg=collections.defaultdict(list);im=collections.defaultdict(list);st=collections.defaultdict(list)
for q in qs:
 k=q['id'];p=norm(q.get('passage'))
 if len(p)>=40:ps[h(p)].append(k)
 if q.get('tables'):tb[h(norm(json.dumps(q['tables'],ensure_ascii=False,sort_keys=True)))].append(k)
 for f in q.get('questionFigures',[]):
  ah=asset_hash(f.get('src',''))
  if ah:fg[ah].append(k)
 for s in q.get('images',[]):
  ah=asset_hash(s)
  if ah:im[ah].append(k)
 st[h(norm(q.get('question')))].append(k)
exactP=grouped_index(ps,'exact_shared_passage');exactT=grouped_index(tb,'exact_shared_tables');exactF=grouped_index(fg,'same_required_figure_bytes');dup=grouped_index(st,'same_question_text');weak=[]
for hv,ids in im.items():
 ids=sorted(set(ids),key=qnum)
 if len(ids)>1:weak.append({'fingerprint':hv,'questionIds':ids,'warning':'Same original photo may contain unrelated questions; not a group proof.'})
psgs=[(q['id'],norm(q.get('passage'))) for q in qs if len(norm(q.get('passage')))>=70]
near=[]
for (a,s),(b,t) in itertools.combinations(psgs,2):
 if s==t:continue
 if len(s)/len(t)<.45 or len(t)/len(s)<.45:continue
 sn={s[i:i+5] for i in range(len(s)-4)};tn={t[i:i+5] for i in range(len(t)-4)};contain=len(sn&tn)/min(len(sn),len(tn))
 if contain>=.84:
  details={'smallerFiveGramCoverage':round(contain,4),'lengths':[len(s),len(t)]};edge(a,b,'near_shared_passage',details);near.append({'questionIds':[a,b],**details})
# Inline materials may be embedded in a stem, rather than passage field.
chunks=collections.defaultdict(set);stem_text={}
for q in qs:
 s=norm(q.get('question'));stem_text[q['id']]=s
 if len(s)>=130:
  for i in range(0,len(s)-39,12):chunks[s[i:i+40]].add(q['id'])
shared=collections.Counter()
for ids in chunks.values():
 if 1<len(ids)<30:
  for a,b in itertools.combinations(sorted(ids,key=qnum),2):shared[(a,b)]+=1
inline=[]
for (a,b),count in shared.items():
 if count<2 or stem_text[a]==stem_text[b]:continue
 m=difflib.SequenceMatcher(None,stem_text[a],stem_text[b],autojunk=False).find_longest_match()
 if m.size>=90:
  details={'commonRunChars':m.size,'commonRunPreview':stem_text[a][m.a:m.a+min(m.size,180)]};edge(a,b,'long_inline_question_overlap',details);inline.append({'questionIds':[a,b],**details})
strong_types={'exact_shared_passage','exact_shared_tables','same_required_figure_bytes','near_shared_passage','long_inline_question_overlap'}
graph=collections.defaultdict(set)
for (a,b),ev in pairs.items():
 if any(e['type'] in strong_types for e in ev):graph[a].add(b);graph[b].add(a)
components=[];seen=set()
for k in sorted(graph,key=qnum):
 if k in seen:continue
 todo=[k];comp=[]
 while todo:
  cur=todo.pop()
  if cur in seen:continue
  seen.add(cur);comp.append(cur);todo.extend(graph[cur]-seen)
 comp.sort(key=qnum);components.append({'candidateId':'candidate-'+comp[0],'questionIds':comp,'members':[info(i) for i in comp],'pairEvidence':[{'questionIds':[a,b],'evidence':e} for (a,b),e in pairs.items() if a in comp and b in comp],'status':'unverified','warning':'Connected material candidates, not confirmed indivisible groups. Verify exact printed shared instructions/number range/figure before drafting.'})
summary={'questionCount':len(qs),'passageQuestionCount':sum(bool(q.get('passage')) for q in qs),'tableQuestionCount':sum(bool(q.get('tables')) for q in qs),'requiredFigureQuestionCount':sum(bool(q.get('questionFigures')) for q in qs),'exactPassageSets':len(exactP),'exactTableSets':len(exactT),'requiredFigureByteSets':len(exactF),'nearPassagePairs':len(near),'inlineMaterialPairs':len(inline),'sameQuestionTextSets':len(dup),'materialCandidateComponents':len(components),'materialCandidateQuestions':sum(len(c['questionIds']) for c in components),'weakSharedOriginalPhotoSets':len(weak),'missingReferencedAssets':len(set(missing))}
report={'schemaVersion':1,'generatedAt':datetime.now(timezone.utc).isoformat(),'baseline':{'dataUpdatedAt':data.get('dataUpdatedAt'),'revision':data.get('revision'),'questionIdsFingerprint':h('|'.join(q['id'] for q in qs))},'summary':summary,'scope':'Existing published bank only; no new sources; exact content is candidate evidence, original paper must verify groups. Same question text is duplicate candidate, not automatic deletion.','candidateComponents':components,'exactPassageSets':exactP,'exactTableSets':exactT,'requiredFigureByteSets':exactF,'nearPassagePairs':near,'inlineMaterialPairs':inline,'sameQuestionTextSets':dup,'weakSharedOriginalPhotoSets':weak,'questionManifest':[info(q['id']) for q in qs],'missingReferencedAssets':sorted(set(missing))}
(OUT/'inventory-v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');lines=['# 題組回查第一輪盤點','',f'現有正式題庫：{len(qs)}筆；候選材料群：{len(components)}群／{summary["materialCandidateQuestions"]}筆。尚未核原卷，不當作可合併數。','', '|候選|題號|科目|共用線索|','|---|---|---|---|']
for c in components:
 ts=sorted({e['type'] for p in c['pairEvidence'] for e in p['evidence']});lines.append('|'+c['candidateId']+'|'+'、'.join(c['questionIds'])+'|'+'、'.join(sorted({m['subject'] for m in c['members']}))+'|'+'、'.join(ts)+'|')
lines+=['','同張原卷照片另有'+str(len(weak))+'組弱線索，照片可能包含不相關題目，將另看原卷題號範圍。','相同題文另有'+str(len(dup))+'組重複候選，不吞掉不同小題。']
(OUT/'inventory-v1.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2));print('\n'.join(lines[5:]))
