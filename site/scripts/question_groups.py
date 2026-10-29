"""Validate group membership and generate small shared route/mark metadata."""
import hashlib
import json
import html
from pathlib import Path

def apply_groups(records, root, dest):
    path=root/'docs/question-groups.json'
    groups=json.loads(path.read_text()) if path.exists() else {}
    by_id={q['id']:q for q in records}
    asset_map_path=root/'site/asset-map.json'
    asset_map=json.loads(asset_map_path.read_text()) if asset_map_path.exists() else {}
    from optimized_assets import remap
    redirects={}
    for parent,group in groups.items():
        members=group['members'];order=group['displayOrder']
        if len(members)<2 or len(set(members))!=len(members) or set(order)!=set(members) or len(order)!=len(members):
            raise ValueError('Group membership/display order is incomplete: '+parent)
        if parent!=min(members,key=lambda id:int(id[2:])) or parent not in by_id:
            raise ValueError('Group must retain its earliest existing ID: '+parent)
        revision=hashlib.sha256(json.dumps(sorted(members),separators=(',',':')).encode()).hexdigest()
        if group.get('revision')!=revision:raise ValueError('Membership revision mismatch: '+parent)
        children=by_id[parent].get('groupQuestions',[])
        if [q['id'] for q in children]!=order or len(children)!=len(members):
            raise ValueError('The published parent must preserve every child in paper order: '+parent)
        if any(child.get('groupQuestions') for child in children):
            raise ValueError('Nested groups must be flattened with full original-child coverage.')
        for figure in by_id[parent].get('groupMetadata',{}).get('commonFigureEquivalentSources',[]):
            for key in ('src','commonSrc'):
                file=(dest/figure[key]).resolve()
                if not file.is_relative_to(dest.resolve()) or not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=figure['sha256']:
                    raise ValueError('Shared necessary figures must match their verified bytes.')
        for member in members:
            if member not in by_id or member in redirects:
                raise ValueError('Missing or overlapping original member: '+member)
            redirects[member]=parent
        # A later correction of an old child must not silently leave an older
        # embedded copy visible through its redirected bookmark.
        original_fields=('sourceId','subject','title','date','dateLabel','addedAt','question','answer','explanation','correctOption','optionAnalysis','studentAnswer','passage','tables','questionFigures','images','teachingComic','trap','explanationFigures','verificationNote','verification','contentStatus')
        for child in children:
            if child['id']==parent:continue
            latest=by_id[child['id']]
            if any(remap(child.get(key),asset_map)!=remap(latest.get(key),asset_map) for key in original_fields):
                raise ValueError('Original child changed; refresh parent.groupQuestions and its shared material before publication: '+child['id'])
    if set(groups)&{id for id,parent in redirects.items() if id!=parent}:
        raise ValueError('A group parent cannot also be another group child.')
    (dest/'question-group-data.js').write_text('// Generated from docs/question-groups.json; group redirects do not merge atomic marks.\nexport const QUESTION_GROUPS = '+json.dumps(groups,ensure_ascii=False,separators=(',',':'))+';\n')
    return [q for q in records if redirects.get(q['id'],q['id'])==q['id']]

def write_group_redirects(root,dest):
    path=root/'docs/question-groups.json'
    groups=json.loads(path.read_text()) if path.exists() else {}
    for parent,group in groups.items():
        if not (dest/(parent+'.html')).is_file():raise ValueError('Build the complete group page before redirects.')
        target='index.html#question/'+parent
        for member in group['members']:
            if member==parent:continue
            page='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WeiRuGo</title><meta http-equiv="refresh" content="0;url='+html.escape(target,quote=True)+'"><a href="'+html.escape(target,quote=True)+'">開啟完整題組</a></html>'
            temporary=dest/(member+'.html.tmp');temporary.write_text(page);temporary.replace(dest/(member+'.html'))
