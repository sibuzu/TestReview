import hashlib
import json
from pathlib import Path
import tempfile
from concurrent.futures import ThreadPoolExecutor
import unittest
from monitor import group_queue as q

class GroupQueueTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.write('docs/inventory.json',{'baseline':{'revision':'frozen'},'questionManifest':[{'id':'q-001','sourceId':'src1'},{'id':'q-002','sourceId':'src1'},{'id':'q-003','sourceId':'src1'},{'id':'q-004','sourceId':'src2'}],'candidateComponents':[{'candidateId':'one','questionIds':['q-001','q-002']},{'candidateId':'two','questionIds':['q-003','q-004']}],'weakSharedOriginalPhotoSets':[{'fingerprint':'ab'*32,'questionIds':['q-001','q-002']}]})
  self.proof=self.root/'proof.jpg';self.proof.write_bytes(b'original-paper')
  q.initialize('docs/inventory.json',self.root)
 def tearDown(self):self.tmp.cleanup()
 def write(self,name,value):
  p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value));return name
 def report(self,cid,ids,decision='confirmed',discovered=None,same_paper=False):
  groups=[] if decision=='rejected' else [{'questionIds':ids,'retainId':ids[0],'subject':'History','printedRange':'第1至2題','reason':'共用題頭與相同原卷已核','sameOriginalPaper':same_paper,'originalEvidence':[{'path':'proof.jpg','sha256':hashlib.sha256(self.proof.read_bytes()).hexdigest(),'visualChecked':True,'visibleHeader':'回答1至2題'}]}]
  return self.write(cid+'.json',{'candidateId':cid,'questionIds':ids,'decision':decision,'confirmedGroups':groups,'discoveredQuestionIds':discovered or [],'coverage':{'allMembersAccountedFor':True}})
 def test_concurrent_workers_claim_distinct_reviews_and_cannot_merge_early(self):
  with ThreadPoolExecutor(2) as pool:claims=list(pool.map(lambda a:q.claim_review(a,root=self.root),['worker2','worker3']))
  self.assertEqual(len({c['id'] for c in claims}),2)
  with self.assertRaises(ValueError):q.claim_merge('worker2',self.root)
 def test_original_hash_and_same_paper_required_across_sources(self):
  q.claim_review('worker2','two',self.root);p=self.report('two',['q-003','q-004'])
  with self.assertRaises(ValueError):q.record_review(p,'worker2',root=self.root)
  data=q.read(self.root/p);data['confirmedGroups'][0]['sameOriginalPaper']=True;data['confirmedGroups'][0]['originalEvidence'][0]['sha256']='bad';self.write(p,data)
  with self.assertRaises(ValueError):q.record_review(p,'worker2',root=self.root)
  self.assertEqual(q.read(self.root/q.QUEUE)['groups'],[])
 def test_expanded_member_found_in_original_is_retained_and_counted(self):
  p=self.report('one',['q-001','q-002','q-003'],discovered=['q-003']);q.record_review(p,'worker2',existing=True,root=self.root)
  result=q.summary(q.read(self.root/q.QUEUE));self.assertEqual((result['confirmedGroups'],result['groupedQuestions']),(1,3));self.assertFalse(result['reviewComplete'])
  self.assertEqual(q.read(self.root/q.QUEUE)['candidates'][0]['seedQuestionIds'],['q-001','q-002'])
 def test_whole_review_gate_then_atomic_merge_and_complete_handoff(self):
  q.record_review(self.report('one',['q-001','q-002']),'worker2',existing=True,root=self.root)
  q.record_review(self.report('two',['q-003','q-004'],decision='rejected'),'worker2',existing=True,root=self.root)
  self.assertTrue(q.summary(q.read(self.root/q.QUEUE))['reviewComplete'])
  with self.assertRaises(ValueError):q.claim_merge('worker2',self.root)
  with self.assertRaises(ValueError):q.reported_summary('worker2',self.root)
  q.reported_summary('/root',self.root)
  with ThreadPoolExecutor(2) as pool:claims=list(pool.map(lambda a:q.claim_merge(a,self.root),['worker2','worker3']))
  self.assertEqual(sum(c is not None for c in claims),1);group=next(c for c in claims if c)
  draft=self.write('draft.json',{'children':['q-001','q-002']})
  bad=self.write('bad.json',{'questionIds':['q-001'],'retainId':'q-001','draftPath':draft,'childCoverage':['q-001']})
  with self.assertRaises(ValueError):q.stage_group(group['id'],bad,group['owner'],self.root)
  manifest=self.write('manifest.json',{'questionIds':['q-001','q-002'],'retainId':'q-001','draftPath':draft,'childCoverage':['q-001','q-002']})
  q.stage_group(group['id'],manifest,group['owner'],self.root);q.integration(group['id'],'integrator',root=self.root);q.integration(group['id'],'integrator',True,self.root)
  self.assertEqual(q.summary(q.read(self.root/q.QUEUE))['mergeStates'],{'integrated':1})
 def test_retries_do_not_duplicate_groups_and_inventory_cannot_be_reset(self):
  p=self.report('one',['q-001','q-002']);q.record_review(p,'worker2',existing=True,root=self.root);q.record_review(p,'worker2',existing=True,root=self.root)
  self.assertEqual(q.summary(q.read(self.root/q.QUEUE))['confirmedGroups'],1)
  q.initialize('docs/inventory.json',self.root)
  data=q.read(self.root/'docs/inventory.json');data['baseline']['revision']='different';self.write('docs/inventory.json',data)
  with self.assertRaises(ValueError):q.initialize('docs/inventory.json',self.root)
 def test_failed_review_does_not_settle_candidate_or_drop_members(self):
  p=self.report('one',['q-001']);
  with self.assertRaises(ValueError):q.record_review(p,'worker2',existing=True,root=self.root)
  data=q.read(self.root/q.QUEUE);self.assertEqual(data['candidates'][0]['state'],'queued');self.assertEqual(data['groups'],[])
 def test_dependency_leads_preserve_baseline_and_can_find_an_existing_mate(self):
  self.write('discovery.json',{'id':'q-001','finding':'承上題'})
  q.add_candidate('dependency-one',['q-001'],'discovery.json',self.root)
  result=q.summary(q.read(self.root/q.QUEUE));self.assertEqual(result['candidates'],3);self.assertEqual(result['baselineQuestions'],4)
  q.add_candidate('dependency-one',['q-001'],'discovery.json',self.root)
  self.assertEqual(q.summary(q.read(self.root/q.QUEUE))['candidates'],3)
  with self.assertRaises(ValueError):q.add_candidate('bad',['q-999'],'discovery.json',self.root)
 def test_user_ai_exclusions_do_not_erase_review_history_or_count_removed_groups(self):
  q.record_review(self.report('one',['q-001','q-002']),'worker2',existing=True,root=self.root)
  self.write('removed.json',{'ids':['q-001','q-002']})
  with self.assertRaises(ValueError):q.exclude_questions(['q-001'],'AI practice','removed.json',self.root)
  result=q.exclude_questions(['q-001','q-002'],'AI practice','removed.json',self.root)
  self.assertEqual((result['baselineQuestions'],result['activeBaselineQuestions'],result['confirmedGroups']),(4,2,0))
  queue=q.read(self.root/q.QUEUE);self.assertEqual(queue['groups'][0]['state'],'superseded');self.assertEqual(queue['candidates'][0]['state'],'confirmed')
  q.exclude_questions(['q-001','q-002'],'AI practice','removed.json',self.root)
  self.assertEqual(len(q.read(self.root/q.QUEUE)['scopeChanges']),1)

if __name__=='__main__':unittest.main()
