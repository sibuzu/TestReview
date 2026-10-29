import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import question_index as index


class QuestionIndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.db_path = self.root/'.cache/question-index.sqlite3'
        self.passage = '康熙晚年，廣東移民獲得義民身分並爭取考試資格。'
        self.q1 = dict(id='q-001', title='歷史題組', subject='History', sourceId='src-gemini-more-060',
                       question='哪一事件？\n(A)朱一貴事件\n(B)林爽文事件', passage=self.passage,
                       answer='A', explanation='康熙晚年的事件。', verification='原題已核對')
        self.q2 = dict(self.q1, id='q-002', title='考試資格', question='何種考試？\n(A)科舉\n(B)高考', answer='A')
        self.write('site/dist/data.json', dict(revision='fixture-r1', sources=[dict(
            id='src-gemini-more-060', title='臺灣清代歷史', url='https://example.com/share/first', platform='Gemini')],
            questions=[self.q1, self.q2]))
        self.write('docs/imports/more-gemini-progress.json', {'sources': [dict(
            order=60, title='臺灣清代歷史', url='https://example.com/share/first', state='partial',
            questionIds=['q-001','q-002'], aliases=['https://example.com/share/second'])]})
        self.write('docs/question-aliases.json', {'q-003':'q-002', 'q-004':'q-003'})
        self.write('docs/comics/progress.json', {'entries':[{'id':'q-001','state':'queued'}]})
        self.draft = dict(self.q1, candidateId='gemini060-p1-q1', sourceKey='gemini060',
                          sourceUrl='https://example.com/share/third', originalQuestionNumber='p1-q1')
        self.write('docs/imports/new-gemini/gemini060/questions/one.json', self.draft)
        pending = dict(self.q2, candidateId='gemini060-p1-q2', sourceKey='gemini060',
                       verification='待核對', originalQuestionNumber='p1-q2')
        self.write('docs/imports/new-gemini/gemini060/questions/two.json', pending)
        self.write('docs/imports/new-gemini/gemini060/integrated.json', {
            'mappings':[dict(candidateId=self.draft['candidateId'],questionId='q-001')]})
        self.write('monitor/confirmations.json', {'requests':[dict(id='check-one',state='pending',
            title='原圖缺字',questionId='q-001',sourceKey='gemini060',questions=['請核對'])]})

    def write(self, path, value):
        p = self.root/path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value, ensure_ascii=False))

    def tearDown(self):
        self.tmp.cleanup()

    def open_built(self):
        index.build(self.root)
        return index.connect(self.db_path)

    def test_chinese_english_short_terms_and_subject_filter(self):
        with self.open_built() as db:
            self.assertEqual(len(index.search(db, '康熙晚年')), 2)
            self.assertEqual(len(index.search(db, '康熙 義民')), 2)
            self.assertEqual(index.search(db, '康熙晚年', subject='Math'), [])
            self.assertEqual(index.search(db, ''), [])
            self.assertEqual(index.search(db, '" OR 1=1 --'), [])
            self.assertEqual(len(index.search(db, '康熙晚年', kind='all')), 4)

    def test_alias_chain_resolves_and_all_share_urls_find_same_records(self):
        with self.open_built() as db:
            self.assertEqual(index.search(db,'q-004')[0]['id'], 'q-002')
            for url in ['https://example.com/share/first','https://example.com/share/second',
                        'https://example.com/share/third/']:
                self.assertEqual({r['id'] for r in index.search(db,url)}, {'q-001','q-002'})

    def test_published_and_pending_drafts_are_distinct_and_no_source_data_changes(self):
        data_path = self.root/'site/dist/data.json'
        before = data_path.read_bytes()
        with self.open_built() as db:
            self.assertEqual(index.stats(db)['published'], 2)
            self.assertEqual(index.stats(db)['unpublishedDrafts'], 1)
            self.assertEqual(index.search(db,'哪一事件',kind='draft')[0]['published_id'],'q-001')
            self.assertEqual(index.search(db,'何種考試',kind='draft')[0]['state'],'awaiting_confirmation')
            self.assertEqual(db.execute('SELECT count(*) FROM confirmations').fetchone()[0],1)
        self.assertEqual(data_path.read_bytes(),before)

    def test_common_reading_is_not_a_duplicate(self):
        with self.open_built() as db:
            result=index.duplicate_candidates(db,self.q2)
            exact_ids={r['id'] for r in result['exactTextCandidates']}
            shared_ids={r['id'] for r in result['sharedMaterialNotDuplicate']}
            self.assertIn('q-002',exact_ids)
            self.assertNotIn('q-001',exact_ids)
            self.assertIn('q-001',shared_ids)
            # A long shared passage cannot inflate question-only similarity.
            unrelated=dict(self.q1,question='完全不同的數學題：求三角形面積。')
            self.assertEqual(index.duplicate_candidates(db,unrelated)['similarStems'],[])

    def test_different_material_with_same_stem_requires_review(self):
        with self.open_built() as db:
            q=dict(self.q1,passage='另一個朝代的文章。')
            self.assertTrue(all(x['relation']=='same_stem_different_material'
                                for x in index.duplicate_candidates(db,q)['exactTextCandidates']))

    def test_group_keeps_members_and_shared_passage(self):
        self.write('docs/imports/new-gemini/gemini060/integrated.json', {'mappings':[
            dict(candidateId='gemini060-p1-q1',questionId='q-001'),
            dict(candidateId='gemini060-p1-q2',questionId='q-001')]})
        self.write('docs/imports/new-gemini/gemini060/group-one.json', {
            'type':'shared_passage_question_group','groupKey':'group1','commonPassage':self.passage,
            'subQuestions':[self.draft,dict(self.q2,candidateId='gemini060-p1-q2',originalQuestionNumber='p1-q2')]})
        with self.open_built() as db:
            self.assertEqual(db.execute('SELECT published_id FROM question_groups').fetchone()[0],'q-001')
            self.assertEqual(db.execute('SELECT count(*) FROM group_members').fetchone()[0],2)
            self.assertEqual(db.execute('SELECT count(*) FROM passages WHERE text=?',(self.passage,)).fetchone()[0],1)

    def test_source_reuse_links_and_inline_choices_are_independent_of_explanation_table(self):
        progress=json.loads((self.root/'docs/imports/more-gemini-progress.json').read_text())
        progress['sources'].append(dict(order=61,title='另一分享來源',state='complete',url='https://example.com/reused'))
        self.write('docs/imports/more-gemini-progress.json',progress)
        self.write('docs/imports/new-gemini/gemini061/manifest.json', {
            'sourceKey':'gemini061','duplicates':[{'existingQuestionId':'q-004'}]})
        q=dict(self.q1,optionAnalysis=[{'label':'A','text':'朱一貴事件'},
                                      {'label':'B','text':'林爽文事件'}])
        with self.open_built() as db:
            self.assertIn('q-001',{r['id'] for r in index.duplicate_candidates(db,q)['exactTextCandidates']})
            self.assertEqual([r['id'] for r in index.search(db,'https://example.com/reused')],['q-002'])
            self.assertEqual(db.execute("SELECT relation FROM record_sources WHERE record_key='published:q-002' AND source_id='src-gemini-more-061'").fetchone()[0],'confirmed_reuse')

    def test_staleness_detects_new_draft_and_failed_build_preserves_old_database(self):
        with self.open_built() as db:
            self.assertFalse(index.is_stale(db,self.root))
        prior=self.db_path.read_bytes()
        bad=self.root/'docs/imports/new-gemini/gemini060/questions/partial.json'
        bad.write_text('{')
        with index.connect(self.db_path) as db:
            self.assertTrue(index.is_stale(db,self.root))
        with self.assertRaises(json.JSONDecodeError):
            index.build(self.root)
        self.assertEqual(self.db_path.read_bytes(),prior)
        bad.unlink()
        with patch.object(index,'fingerprint',side_effect=[index.fingerprint(self.root),[]]):
            with self.assertRaisesRegex(RuntimeError,'Inputs changed'):
                index.build(self.root)
        self.assertEqual(self.db_path.read_bytes(),prior)

    def test_unprocessed_source_conversation_is_searchable_before_question_drafts(self):
        self.write('docs/sources/gemini-first.json', {'text':'這是尚未拆題的海岸侵蝕與海蝕平臺對話。'})
        with self.open_built() as db:
            self.assertEqual(index.search(db,'海岸侵蝕'),[])
            self.assertEqual(index.search_sources(db,'海岸侵蝕')[0]['id'],'src-gemini-more-060')
            self.assertEqual(index.search_sources(db,'侵蝕')[0]['id'],'src-gemini-more-060')
            self.assertEqual(index.search_sources(db,'" OR 1=1 --'),[])

    def test_cannot_publish_database_or_collapse_case_and_math_symbols(self):
        with self.assertRaises(ValueError):
            index.build(self.root,self.root/'site/dist/questions.sqlite3')
        self.assertNotEqual(index.digest('AB'),index.digest('ab'))
        self.assertNotEqual(index.digest('x²'),index.digest('x2'))
        self.assertNotEqual(index.digest('H₂O'),index.digest('H2O'))
        self.assertNotEqual(index.digest('a part'),index.digest('apart'))
        self.assertEqual(index.digest('甲 乙'),index.digest('甲\n乙'))

    def test_cancelled_future_source_draft_is_kept_on_disk_but_not_active_index(self):
        self.write('monitor/import-control.json', {'state':'paused','lastAllowedSourceOrder':60})
        self.write('docs/imports/new-gemini/gemini061/questions/one.json', dict(
            self.draft,candidateId='gemini061-p1-q1',sourceKey='gemini061',title='已取消未入庫稿'))
        with self.open_built() as db:
            self.assertEqual(index.stats(db)['drafts'],2)
            self.assertEqual(index.stats(db)['importState'],'paused')
            self.assertEqual(index.search(db,'已取消未入庫稿',kind='all'),[])
        self.assertTrue((self.root/'docs/imports/new-gemini/gemini061/questions/one.json').exists())

    def test_group_receipt_publishes_each_child_without_fake_pending_drafts(self):
        self.write('docs/imports/new-gemini/gemini060/integrated.json', {'mappings':[
            dict(candidateId='group1',questionId='q-001')]})
        self.write('docs/imports/new-gemini/gemini060/group-one.json', {
            'type':'shared_passage_question_group','groupKey':'group1','sourceKey':'gemini060',
            'commonPassage':self.passage,'subQuestions':[self.draft,dict(self.q2,
             candidateId='gemini060-p1-q2',originalQuestionNumber='p1-q2')]})
        with self.open_built() as db:
            self.assertEqual(index.stats(db)['unpublishedDrafts'],0)
            self.assertEqual(db.execute('SELECT published_id FROM question_groups').fetchone()[0],'q-001')

    def test_user_skipped_draft_is_not_active_and_pending_wording_is_recognized(self):
        self.write('docs/imports/new-gemini/gemini060/manifest.json', {
            'sourceKey':'gemini060','userSkippedOriginalKeys':['p1-q1']})
        pending=json.loads((self.root/'docs/imports/new-gemini/gemini060/questions/two.json').read_text())
        pending['verification']='待核對原題'
        self.write('docs/imports/new-gemini/gemini060/questions/two.json',pending)
        with self.open_built() as db:
            self.assertEqual(index.stats(db)['drafts'],1)
            self.assertEqual(index.stats(db)['unpublishedDrafts'],1)
            self.assertEqual(index.search(db,'何種考試',kind='draft')[0]['state'],'awaiting_confirmation')
        self.assertTrue((self.root/'docs/imports/new-gemini/gemini060/questions/one.json').exists())


if __name__=='__main__':
    unittest.main()
