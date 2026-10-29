import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from question_groups import apply_groups,write_group_redirects

class GroupMetadataTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.dest=self.root/'dist';self.dest.mkdir();(self.root/'docs').mkdir()
  self.children=[{'id':'q-001','question':'原題一'},{'id':'q-002','question':'原題二'}]
  self.records=[dict(self.children[0],groupQuestions=self.children),self.children[1]]
  self.group={'members':['q-001','q-002'],'displayOrder':['q-001','q-002'],
   'revision':hashlib.sha256(b'["q-001","q-002"]').hexdigest()}
 def tearDown(self):self.tmp.cleanup()
 def write(self,groups):
  (self.root/'docs/question-groups.json').write_text(json.dumps(groups))
 def test_valid_group_keeps_full_children_and_generates_only_route_metadata(self):
  self.write({'q-001':self.group});result=apply_groups(self.records,self.root,self.dest)
  self.assertEqual([q['id'] for q in result],['q-001']);self.assertEqual(result[0]['groupQuestions'],self.children)
  self.assertIn(self.group['revision'],(self.dest/'question-group-data.js').read_text())
  self.assertEqual(len(self.records),2,'input evidence is not destructively filtered')
 def test_membership_revision_survives_typo_fix_but_incomplete_order_is_rejected(self):
  self.children[1]['question']='訂正原題二';self.write({'q-001':self.group});apply_groups(self.records,self.root,self.dest)
  self.group['displayOrder']=['q-001'];self.write({'q-001':self.group})
  with self.assertRaises(ValueError):apply_groups(self.records,self.root,self.dest)
 def test_equivalent_required_figures_must_match_actual_bytes(self):
  (self.dest/'assets').mkdir();(self.dest/'assets/a.svg').write_bytes(b'one');(self.dest/'assets/b.svg').write_bytes(b'two')
  self.records[0]['groupMetadata']={'commonFigureEquivalentSources':[{'src':'assets/a.svg','commonSrc':'assets/b.svg','sha256':hashlib.sha256(b'one').hexdigest()}]}
  self.write({'q-001':self.group})
  with self.assertRaises(ValueError):apply_groups(self.records,self.root,self.dest)
  (self.dest/'assets/b.svg').write_bytes(b'one');apply_groups(self.records,self.root,self.dest)
 def test_missing_child_snapshot_or_wrong_parent_cannot_hide_original_entries(self):
  self.records[0]['groupQuestions']=self.children[:1];self.write({'q-001':self.group})
  with self.assertRaises(ValueError):apply_groups(self.records,self.root,self.dest)
 def test_old_reading_page_redirects_only_after_parent_is_built(self):
  self.write({'q-001':self.group})
  with self.assertRaises(ValueError):write_group_redirects(self.root,self.dest)
  (self.dest/'q-001.html').write_text('complete group');(self.dest/'q-002.html').write_text('old single')
  write_group_redirects(self.root,self.dest)
  self.assertIn('index.html#question/q-001',(self.dest/'q-002.html').read_text())
  self.assertEqual((self.dest/'q-001.html').read_text(),'complete group')
 def test_later_child_correction_cannot_publish_a_stale_embedded_snapshot(self):
  self.write({'q-001':self.group})
  self.records[1]=dict(self.children[1],question='已確認的訂正題文')
  with self.assertRaisesRegex(ValueError,'Original child changed'):apply_groups(self.records,self.root,self.dest)
  self.records[0]['groupQuestions']=[self.children[0],dict(self.records[1])]
  apply_groups(self.records,self.root,self.dest)

if __name__=='__main__':unittest.main()
