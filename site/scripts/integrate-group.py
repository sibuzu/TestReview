"""Prepare one reviewed group; publication and formal page QA remain separate."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from monitor.group_queue import integration
from monitor.comic_pipeline import load,save


def prepare(group_id):
    queue=load(ROOT/'docs/imports/group-review/queue.json')
    group=next(g for g in queue['groups']if g['id']==group_id)
    owner='/root/comic_lane_1'
    if group['state']=='ready':integration(group_id,owner,root=ROOT)
    elif group['state']!='integrating' or group.get('integrator')!=owner:
        raise ValueError('Only the integration owner can resume its reviewed group.')
    manifest_path=ROOT/group['manifest'];manifest=load(manifest_path)
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest()!=group['manifestSHA256']:
        raise ValueError('The handed-off manifest changed.')
    proposed=load(ROOT/manifest['draftPath']);members=manifest['questionIds'];order=manifest['displayOrder']
    if len(set(members))!=len(members)or set(order)!=set(members)or proposed['id']!=min(members,key=lambda qid:int(qid[2:])):
        raise ValueError('Incomplete membership or wrong retained ID.')
    children={child['id']:child for child in proposed['groupQuestions']}
    if set(children)!=set(members):raise ValueError('Missing child snapshot.')
    proposed['groupQuestions']=[children[qid]for qid in order]
    proposed['groupMetadata']={**proposed.get('groupMetadata',{}),'groupId':group_id,'retainId':proposed['id'],'originalQuestionIds':members,'displayOrder':order}
    # Use the same bounded schema that the app imports, including optional
    # defaults. Every original child's public fields must survive exactly.
    js="import {validateQuestion} from './site/dist/core.js';let text='';for await(const part of process.stdin)text+=part;process.stdout.write(JSON.stringify(validateQuestion(JSON.parse(text))));"
    normalized=json.loads(subprocess.run(['node','--input-type=module','-e',js],cwd=ROOT,input=json.dumps(proposed,ensure_ascii=False),text=True,capture_output=True,check=True).stdout)
    before=load(ROOT/'site/dist/data.json');existing={q['id']:q for q in before['questions']}
    for child in normalized['groupQuestions']:
        raw={k:v for k,v in child.items()if k!='originalQuestionNumber'}
        current=existing.get(child['id'])
        if current and not current.get('groupQuestions'):
            if raw!=current:raise ValueError('Stale original child: '+child['id'])
        else:
            previous=next((member for q in existing.values()for member in q.get('groupQuestions',[])if member['id']==child['id']),None)
            if previous!=child:raise ValueError('Missing or stale grouped child: '+child['id'])
    config=load(ROOT/'docs/question-groups.json')
    revision=hashlib.sha256(json.dumps(sorted(members),separators=(',',':')).encode()).hexdigest()
    entry={'members':members,'displayOrder':order,'revision':revision}
    if normalized['id']in config and config[normalized['id']]!=entry:raise ValueError('Membership changed during integration.')
    for parent,value in config.items():
        if parent!=normalized['id']and set(value['members'])&set(members):raise ValueError('Group membership overlaps.')
    override=ROOT/'docs/complete-questions'/f"{normalized['id']}.json"
    backup=ROOT/'.cache/group-integration'/group_id/'before-override.json';backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists()and override.exists():backup.write_bytes(override.read_bytes())
    save(override,normalized);config[normalized['id']]=entry;save(ROOT/'docs/question-groups.json',config)
    receipt={'preparedAt':datetime.now(timezone.utc).isoformat(),'groupId':group_id,'retainId':normalized['id'],'originalIds':members,'displayOrder':order,'revision':revision,'manifest':group['manifest'],'manifestSHA256':group['manifestSHA256'],'originalCoveragePreserved':True,'existingComicsPreserved':sum(bool(c.get('teachingComic'))for c in normalized['groupQuestions']),'newComicEvents':0,'duplicateAliasFileUnchanged':True,'previousOverrideBackup':str(backup),'formalQAComplete':False}
    folder=ROOT/'docs/imports/group-review/integrated';folder.mkdir(parents=True,exist_ok=True);save(folder/(group_id+'-preparation.json'),receipt)
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('group_id');args=parser.parse_args()
    print(json.dumps(prepare(args.group_id),ensure_ascii=False,indent=2))
