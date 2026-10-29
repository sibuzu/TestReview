"""Two-phase, locked queue: verify every candidate, then prepare complete group drafts."""
import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
QUEUE = Path('docs/imports/group-review/queue.json')
REVIEWED = {'confirmed', 'split', 'rejected', 'skipped'}

def now():
    return datetime.now(timezone.utc).isoformat()

def read(path):
    return json.loads(path.read_text())

def local_file(root, relative):
    path = (root/relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Expected an existing local evidence file: '+str(relative))
    return path

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

@contextmanager
def edit(root=ROOT):
    lock = root/'.cache/locks/group-queue.lock'
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        path = root/QUEUE
        data = read(path) if path.exists() else {}
        yield data
        path.parent.mkdir(parents=True, exist_ok=True)
        data['updatedAt'] = now()
        fd, name = tempfile.mkstemp(dir=path.parent, prefix='queue-', suffix='.tmp')
        try:
            with os.fdopen(fd, 'w') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
                out.write('\n')
                out.flush()
                os.fsync(out.fileno())
            os.replace(name, path)
        finally:
            if os.path.exists(name):
                os.unlink(name)

def initialize(inventory='docs/imports/group-review/inventory-v1.json', root=ROOT):
    path = local_file(root, inventory)
    inv = read(path)
    with edit(root) as queue:
        if queue:
            if queue.get('inventorySHA256') != digest(path):
                raise ValueError('An active review inventory cannot be replaced.')
            return summary(queue)
        candidates = []
        for item in inv['candidateComponents']:
            candidates.append({'id': item['candidateId'], 'questionIds': item['questionIds'],
                               'kind': 'shared_material', 'state': 'queued', 'photoHints': []})
        for item in inv.get('weakSharedOriginalPhotoSets', []):
            ids = set(item['questionIds'])
            covered = next((c for c in candidates if ids <= set(c['questionIds'])), None)
            if covered:
                covered['photoHints'].append(item['fingerprint'])
            else:
                candidates.append({'id': 'photo-'+item['fingerprint'][:16],
                                   'questionIds': item['questionIds'], 'kind': 'shared_original_only',
                                   'state': 'queued', 'photoHints': [item['fingerprint']]})
        queue.update(schemaVersion=1, inventory=inventory, inventorySHA256=digest(path),
                     baseline=inv['baseline'], baselineQuestionIds=[q['id'] for q in inv['questionManifest']],
                     createdAt=now(), candidates=candidates, groups=[], reviewSummaryReported=False)
        return summary(queue)

def summary(queue):
    candidates = queue.get('candidates', [])
    groups = [g for g in queue.get('groups', []) if g['state'] != 'superseded']
    states = Counter(c['state'] for c in candidates)
    review_done = bool(candidates) and all(c['state'] in REVIEWED for c in candidates)
    by_subject = defaultdict(lambda: {'groups': 0, 'questions': 0})
    for group in groups:
        row = by_subject[group['subject']]
        row['groups'] += 1
        row['questions'] += len(group['questionIds'])
    return {'phase': 'review' if not review_done else ('merge' if queue.get('reviewSummaryReported') else 'waiting_summary'), 'reviewComplete': review_done,
            'baselineQuestions': len(queue.get('baselineQuestionIds', [])),
            'activeBaselineQuestions':len(set(queue.get('baselineQuestionIds',[]))-set(queue.get('excludedQuestionIds',[]))),
            'excludedQuestions':len(queue.get('excludedQuestionIds',[])),
            'candidates': len(candidates), 'reviewed': sum(states[s] for s in REVIEWED),
            'awaitingConfirmation': states['needs_confirmation'], 'reviewing': states['reviewing'],
            'confirmedGroups': len(groups), 'groupedQuestions': sum(len(g['questionIds']) for g in groups),
            'mergeStates': dict(Counter(g['state'] for g in groups)), 'subjects': dict(by_subject),
            'reviewSummaryReported': queue.get('reviewSummaryReported', False)}

def exclude_questions(question_ids, reason, report_path, root=ROOT):
    proof=local_file(root,report_path)
    with edit(root) as queue:
        ids=set(question_ids)
        if not ids <= set(queue['baselineQuestionIds']):
            raise ValueError('Exclusions must refer to the frozen baseline.')
        if any(set(g['questionIds']) & ids and not set(g['questionIds']) <= ids
               for g in queue['groups'] if g['state']!='superseded'):
            raise ValueError('Mixed groups need a fresh reviewed split before exclusion.')
        for group in queue['groups']:
            if set(group['questionIds']) <= ids and group['state']!='superseded':
                if group['state']!='confirmed':raise ValueError('Cannot exclude work already merging.')
                group.update(state='superseded',supersededAt=now(),supersededReason=reason)
        previous=set(queue.get('excludedQuestionIds',[]))
        queue['excludedQuestionIds']=sorted(previous|ids)
        if ids-previous:
            queue.setdefault('scopeChanges',[]).append({'at':now(),'reason':reason,
                'excludedQuestionIds':sorted(ids-previous),'report':report_path,'reportSHA256':digest(proof)})
            queue['reviewSummaryReported']=False
        for candidate in queue['candidates']:
            candidate['excludedQuestionIds']=sorted(set(candidate['questionIds']) & (previous|ids))
        return summary(queue)

def add_candidate(candidate_id, question_ids, evidence_path, root=ROOT):
    """Append a documented dependency lead without replacing the frozen inventory."""
    proof = local_file(root, evidence_path)
    with edit(root) as queue:
        ids = sorted(set(question_ids), key=lambda qid:int(qid[2:]))
        if not ids or not set(ids) <= set(queue['baselineQuestionIds']):
            raise ValueError('A supplemental lead must reference existing baseline questions.')
        if any(g['state'] not in {'confirmed', 'superseded'} for g in queue['groups']):
            raise ValueError('Cannot change review scope after merging starts.')
        old = next((c for c in queue['candidates'] if c['id']==candidate_id), None)
        if old:
            if old['questionIds'] != ids:
                raise ValueError('Cannot replace an existing lead.')
            return summary(queue)
        queue['candidates'].append({'id':candidate_id,'questionIds':ids,
            'kind':'continuation_reference','state':'queued','photoHints':[],
            'discoveryEvidence':evidence_path,'discoverySHA256':digest(proof)})
        queue['reviewSummaryReported'] = False
        return summary(queue)

def reported_summary(agent, root=ROOT):
    with edit(root) as queue:
        if agent != '/root' or not summary(queue)['reviewComplete']:
            raise ValueError('Root reports the totals after every candidate has been reviewed.')
        queue['reportedSummary'] = dict(summary(queue),reportedAt=now())
        queue['reviewSummaryReported'] = True
        return summary(queue)

def claim_review(agent, candidate_id=None, root=ROOT):
    with edit(root) as queue:
        if not queue:
            raise ValueError('Initialize the inventory first.')
        current = next((c for c in queue['candidates'] if c.get('owner') == agent and c['state'] == 'reviewing'), None)
        if current:
            return current
        candidate = next((c for c in queue['candidates'] if c['state'] == 'queued' and
                          (candidate_id is None or c['id'] == candidate_id)), None)
        if candidate:
            candidate.update(state='reviewing', owner=agent, startedAt=now())
        return candidate

def record_review(report_path, agent, existing=False, root=ROOT):
    path = local_file(root, report_path)
    report = read(path)
    with edit(root) as queue:
        candidate = next(c for c in queue['candidates'] if c['id'] == report['candidateId'])
        if candidate['state'] in REVIEWED and candidate.get('reportSHA256') == digest(path):
            return summary(queue)
        if not existing and (candidate['state'] not in {'reviewing', 'needs_confirmation'} or candidate.get('owner') != agent):
            raise ValueError('Review must belong to the worker holding this candidate.')
        if existing and candidate['state'] != 'queued':
            raise ValueError('Bootstrap cannot replace another active review.')
        inventory = read(local_file(root, queue['inventory']))
        members = {q['id']: q for q in inventory['questionManifest']}
        discovered = set(report.get('discoveredQuestionIds', []))
        expected_ids = set(candidate['questionIds']) | discovered
        if not discovered <= set(members) or set(report['questionIds']) != expected_ids or not report.get('coverage', {}).get('allMembersAccountedFor'):
            raise ValueError('Every candidate member must be accounted for.')
        decision = report['decision']
        if decision not in REVIEWED | {'needs_confirmation'}:
            raise ValueError('Unknown review decision.')
        proposed = report.get('confirmedGroups', [])
        if decision in {'confirmed', 'split'} and not proposed:
            raise ValueError('Confirmed review requires at least one genuine group.')
        if decision in {'rejected', 'skipped'} and proposed:
            raise ValueError('Rejected candidate cannot silently publish a group.')
        used = set()
        prepared = []
        for group in proposed:
            ids = sorted(set(group['questionIds']), key=lambda qid:int(qid[2:]))
            if set(ids)&set(queue.get('excludedQuestionIds',[])):
                raise ValueError('User-excluded AI practice cannot enter a merged group.')
            if len(ids) < 2 or not set(ids) <= expected_ids or used & set(ids):
                raise ValueError('Groups must preserve distinct candidate members.')
            used.update(ids)
            if group['retainId'] != ids[0] or not group.get('subject') or not group.get('printedRange') or not group.get('reason'):
                raise ValueError('A group needs its oldest ID, subject and printed-paper rationale.')
            evidence = group.get('originalEvidence', [])
            if not evidence:
                raise ValueError('Original-paper evidence is required.')
            for item in evidence:
                proof = local_file(root, item['path'])
                if not item.get('visualChecked') or digest(proof) != item.get('sha256') or not item.get('visibleHeader'):
                    raise ValueError('Original evidence must be viewed and match its saved hash.')
            if group.get('groupType') == 'ai_extension_group':
                discussion = group.get('discussionEvidence', [])
                if not discussion:
                    raise ValueError('AI extension groups require the discussion declaration.')
                for item in discussion:
                    proof = local_file(root, item['path'])
                    if not item.get('textChecked') or digest(proof) != item.get('sha256') or not item.get('visibleHeader'):
                        raise ValueError('Extension-group discussion evidence must be read and hashed.')
            source_ids = {members[qid]['sourceId'] for qid in ids}
            if len(source_ids) > 1 and not group.get('sameOriginalPaper'):
                raise ValueError('Across sources, explicitly verify the same original paper.')
            key = 'group-'+'-'.join(ids)
            duplicate = next((g for g in queue['groups'] if g['id'] == key), None)
            if duplicate:
                continue
            if any(set(ids) & set(g['questionIds']) for g in queue['groups'] if g['state'] != 'superseded'):
                raise ValueError('Overlapping groups need a reconciled review before merging.')
            prepared.append({'id': key, 'questionIds': ids, 'retainId': ids[0], 'subject': group['subject'],
                             'state': 'confirmed', 'reviewReport': report_path, 'reviewSHA256': digest(path),
                             'confirmedBy': agent, 'confirmedAt': now(), 'sourceIds': sorted(source_ids)})
        queue['groups'].extend(prepared)
        if discovered:
            candidate.setdefault('seedQuestionIds', candidate['questionIds'][:])
            candidate['questionIds'] = sorted(expected_ids, key=lambda qid:int(qid[2:]))
            candidate['discoveredQuestionIds'] = sorted(discovered)
        candidate.update(state=decision, owner=agent, reviewedAt=now(), report=report_path, reportSHA256=digest(path))
        return summary(queue)

def claim_merge(agent, root=ROOT):
    with edit(root) as queue:
        if not summary(queue)['reviewComplete']:
            raise ValueError('Finish the entire candidate review phase before merging.')
        if not queue.get('reviewSummaryReported'):
            raise ValueError('Report the verified total and subject counts before merging.')
        current = next((g for g in queue['groups'] if g.get('owner') == agent and g['state'] == 'merging'), None)
        if current:
            return current
        group = next((g for g in queue['groups'] if g['state'] == 'confirmed'), None)
        if group:
            group.update(state='merging', owner=agent, startedAt=now())
        return group

def stage_group(group_id, manifest_path, agent, root=ROOT):
    path = local_file(root, manifest_path)
    manifest = read(path)
    with edit(root) as queue:
        group = next(g for g in queue['groups'] if g['id'] == group_id)
        if group['state'] != 'merging' or group.get('owner') != agent:
            raise ValueError('Only the claimed merge worker may hand off the group.')
        if set(manifest['questionIds']) != set(group['questionIds']) or manifest['retainId'] != group['retainId']:
            raise ValueError('Merged draft must preserve every original member.')
        local_file(root, manifest['draftPath'])
        if set(manifest.get('childCoverage', [])) != set(group['questionIds']):
            raise ValueError('Full child-question coverage is required.')
        group.update(state='ready', manifest=manifest_path, manifestSHA256=digest(path), readyAt=now())
        return group

def integration(group_id, agent, done=False, root=ROOT):
    with edit(root) as queue:
        group = next(g for g in queue['groups'] if g['id'] == group_id)
        if done:
            if group['state'] != 'integrating' or group.get('integrator') != agent:
                raise ValueError('Integration must have an explicit owner.')
            group.update(state='integrated', integratedAt=now())
        else:
            if group['state'] != 'ready':
                raise ValueError('A complete, handed-off draft is required.')
            group.update(state='integrating', integrator=agent, integrationStartedAt=now())
        return group

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init').add_argument('--inventory', default='docs/imports/group-review/inventory-v1.json')
    sub.add_parser('status')
    for name in ('claim-review', 'review', 'claim-merge', 'stage', 'begin', 'integrated', 'reported'):
        cmd = sub.add_parser(name)
        cmd.add_argument('--agent', required=True)
        if name == 'claim-review': cmd.add_argument('--candidate')
        if name == 'review':
            cmd.add_argument('--report', required=True)
            cmd.add_argument('--existing', action='store_true')
        if name in ('stage', 'begin', 'integrated'): cmd.add_argument('--group', required=True)
        if name == 'stage': cmd.add_argument('--manifest', required=True)
    args = parser.parse_args()
    if args.command == 'init': result = initialize(args.inventory)
    elif args.command == 'status': result = summary(read(ROOT/QUEUE))
    elif args.command == 'claim-review': result = claim_review(args.agent, args.candidate)
    elif args.command == 'review': result = record_review(args.report, args.agent, args.existing)
    elif args.command == 'claim-merge': result = claim_merge(args.agent)
    elif args.command == 'stage': result = stage_group(args.group, args.manifest, args.agent)
    elif args.command == 'reported': result = reported_summary(args.agent)
    else: result = integration(args.group, args.agent, args.command == 'integrated')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
