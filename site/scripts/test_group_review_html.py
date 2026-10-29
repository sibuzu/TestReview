import copy
import hashlib
import html
import json
from pathlib import Path
import tempfile
import unittest

from group_review_html import render_group_page,child_materials,ordered_children

ROOT=Path(__file__).resolve().parents[2]


class GroupReadingPageTests(unittest.TestCase):
    def setUp(self):
        self.question=json.loads((ROOT/'docs/imports/group-review/drafts/group-q-029-q-031/question.json').read_text())
        self.data=json.loads((ROOT/'site/dist/data.json').read_text())

    def render(self,q=None):
        return render_group_page(q or self.question,{s['id']:s['name']for s in self.data['subjects']},{s['id']:s for s in self.data['sources']},'',lambda s:html.escape(str(s or '')),lambda p:p,lambda table:'<table>'+html.escape(table['caption'])+'</table>',lambda:'<script>trusted support</script>',ROOT/'site/dist')

    def test_common_material_once_all_child_questions_and_answers_retained(self):
        q=self.question;q['question']='PARENT SEARCH TEXT ONLY';q['answer']='PARENT ANSWER NOT A CHILD'
        page=self.render(q)
        self.assertEqual(page.count('class="reading-passage"'),1)
        self.assertEqual(page.count('class="group-question"'),2)
        self.assertEqual(page.count('class="group-answer"'),2)
        self.assertNotIn(q['question'],page);self.assertNotIn(q['answer'],page)
        for child in q['groupQuestions']:
            self.assertIn(html.escape(child['question']),page)
            self.assertIn(html.escape(child['answer']).replace('\n','<br>'),page)
            for option in child['optionAnalysis']:
                self.assertIn(html.escape(option['text']),page)
                self.assertIn(html.escape(option['explanation']),page)

    def test_rendering_does_not_rewrite_complete_child_snapshots(self):
        before=copy.deepcopy(self.question);self.render();self.assertEqual(before,self.question)

    def test_each_child_comic_survives_even_when_both_use_the_same_art(self):
        q=self.question;q.pop('teachingComic',None);q['groupQuestions'][1]['teachingComic']['art']=q['groupQuestions'][0]['teachingComic']['art']
        page=self.render(q)
        self.assertEqual(page.count('class="native-comic"'),2)
        self.assertEqual(page.count('<script>trusted support</script>'),1)
        for child in q['groupQuestions']:self.assertIn(html.escape(child['teachingComic']['fourth']['answer']),page)

    def test_specific_material_is_not_lost_when_common_prefix_is_removed(self):
        child=copy.deepcopy(self.question['groupQuestions'][0]);child['passage']=self.question['passage']+'\n本小題額外條件';child['tables']=[{'caption':'子題專用表','headers':['A'],'rows':[['B']]}]
        material,captions=child_materials(child,self.question,ROOT/'site/dist')
        self.assertEqual(material['passage'],'本小題額外條件');self.assertEqual(material['tables'],child['tables']);self.assertEqual(captions,[])
        child['passage']='不同措辭不能猜作共文';self.assertEqual(child_materials(child,self.question,ROOT/'site/dist')[0]['passage'],child['passage'])

    def test_original_paper_order_can_differ_from_retained_question_id(self):
        q=self.question;q['groupMetadata']['displayOrder']=['q-031','q-029'];page=self.render(q)
        self.assertLess(page.index('data-group-question="q-031"'),page.index('data-group-question="q-029"'))
        self.assertLess(page.index('data-group-answer="q-031"'),page.index('data-group-answer="q-029"'))

    def test_child_sources_dates_and_original_responses_are_inside_one_collapsed_review(self):
        page=self.render();self.assertEqual(page.count('<details class="review">'),1);self.assertNotIn('<details class="review" open',page)
        self.assertEqual(page.count('原AI對話 ↗'),2)
        for child in self.question['groupQuestions']:
            self.assertIn(child['date'],page)
            if child.get('studentAnswer'):self.assertIn('原卷作答：<b>'+html.escape(child['studentAnswer'])+'</b>',page)
        self.assertLess(page.index('<details'),page.index('原AI對話 ↗'))

    def test_question_text_is_escaped_and_group_sources_cannot_inject_links(self):
        q=self.question;q['groupQuestions'][0]['question']='<script>alert(1)</script>';page=self.render(q)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;',page);self.assertNotIn('<script>alert(1)',page)

    def test_shared_equivalent_images_require_the_exact_declared_bytes_and_keep_distinct_captions(self):
        with tempfile.TemporaryDirectory()as folder:
            base=Path(folder);(base/'assets').mkdir();(base/'assets/a.svg').write_bytes(b'same');(base/'assets/b.svg').write_bytes(b'same')
            digest=hashlib.sha256(b'same').hexdigest();parent={'questionFigures':[{'src':'assets/a.svg','caption':'共同圖'}],'groupMetadata':{'commonFigureEquivalentSources':[{'src':'assets/b.svg','commonSrc':'assets/a.svg','sha256':digest}]}}
            child={'questionFigures':[{'src':'assets/b.svg','caption':'本小題圖說'}]}
            specific,captions=child_materials(child,parent,base);self.assertEqual(specific['questionFigures'],[]);self.assertEqual(captions,['本小題圖說'])
            (base/'assets/b.svg').write_bytes(b'different');specific,_=child_materials(child,parent,base);self.assertEqual(specific['questionFigures'],child['questionFigures'])

    def test_common_table_matching_is_structural_not_an_approximate_caption_match(self):
        table={'caption':'表一','headers':['A'],'rows':[['1']]};child={'tables':[copy.deepcopy(table),{**table,'rows':[['2']]}]};parent={'tables':[table]}
        specific,_=child_materials(child,parent,ROOT/'site/dist');self.assertEqual(specific['tables'],[{**table,'rows':[['2']]}])


if __name__=='__main__':unittest.main()
