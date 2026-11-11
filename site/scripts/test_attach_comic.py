import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).with_name('attach-comic.py')
spec = importlib.util.spec_from_file_location('attach_comic', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RetainedFiguresTests(unittest.TestCase):
    def test_official_guide_survives_first_comic_without_prior_override(self):
        guide = {'src': 'assets/questions/q-051-official-guide.jpg', 'alt': '官方導覽圖'}
        self.assertEqual(module.retained_figures('q-051', {}, [guide]), [guide])

    def test_explicit_removal_is_preserved_instead_of_resurrecting_base_figure(self):
        self.assertEqual(module.retained_figures('q-1', {'explanationFigures': []},
                         [{'src':'assets/questions/removed-source-ai.jpg'}]), [])

    def test_only_our_previous_flat_comic_is_replaced(self):
        guide = {'src':'assets/questions/official-map.jpg'}
        figures = [guide, {'src':'assets/comics/q-051.png'}]
        self.assertEqual(module.retained_figures('q-051', {'explanationFigures':figures}, []), [guide])

class IndependentImageTests(unittest.TestCase):
    def test_attach_publishes_each_image_and_standalone_keeps_fourth_answer(self):
        import json
        import tempfile
        from unittest.mock import patch
        from teaching_comic import render_comic
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for directory in ['docs/comics', 'docs/complete-questions', 'site/dist/assets/comics']:
                (root/directory).mkdir(parents=True)
            images = []
            for index in range(4):
                relative = f'docs/comics/image-{index}.svg'
                (root/relative).write_text(f'<svg xmlns="http://www.w3.org/2000/svg"><title>image {index}</title></svg>')
                images.append(relative)
            spec = dict(id='q-1', title='生物測試', art=images[0],
                        panels=[dict(heading=f'第{i+1}圖', text=f'解說{i+1}', alt=f'構造{i+1}', image=images[i]) for i in range(3)],
                        fourth=dict(answer='A：完整答案', points=['完整重點'], image=images[3], alt='總結構造'))
            (root/'docs/comics/q-1.json').write_text(json.dumps(spec))
            (root/'site/dist/data.json').write_text(json.dumps({'questions': []}))
            with patch.object(module, 'ROOT', root), patch.object(module, 'optimize_payload', side_effect=lambda value:value):
                module.attach('q-1')
            comic = json.loads((root/'docs/complete-questions/q-1.json').read_text())['teachingComic']
            paths = [p['image'] for p in comic['panels']]+[comic['fourth']['image']]
            self.assertEqual(len(set(paths)), 4)
            self.assertTrue(all((root/'site/dist'/path).exists() for path in paths))
            self.assertEqual(comic['fourth']['alt'], '總結構造')
            html = render_comic(comic, lambda path:path)
            self.assertEqual(html.count('<img '), 4)
            self.assertEqual(html.count('comic-art-single'), 4)
            self.assertNotIn('--panel:', html)
            self.assertIn('A：完整答案', html)
            self.assertIn('完整重點', html)
            self.assertEqual(json.loads((root/'docs/comics/q-1.json').read_text())['layoutVersion'], 'native-four-images-v7')


    def test_group_attach_refreshes_each_embedded_lesson_without_duplicate_parent_comic(self):
        import json
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for directory in ['docs/comics', 'docs/complete-questions', 'site/dist/assets/comics']:
                (root/directory).mkdir(parents=True)
            images=[]
            for i in range(4):
                name=f'docs/comics/step-{i}.svg';(root/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg"><title>{i}</title></svg>');images.append(name)
            def comic_spec(qid):
                return dict(id=qid,title=qid,art=images[0],panels=[dict(heading='構造',text='完整解說',alt='原圖',image=images[i]) for i in range(3)],fourth=dict(answer='A',points=['重點'],image=images[3],alt='第四圖'))
            parent=dict(id='q-1',question='共同材料',teachingComic={'art':'old-parent'},groupQuestions=[
                dict(id='q-1',question='第一原問',answer='A',teachingComic={'art':'old-1'}),
                dict(id='q-2',question='第二原問',answer='B',teachingComic={'art':'old-2'})])
            (root/'docs/question-groups.json').write_text(json.dumps({'q-1':{'members':['q-1','q-2']}}))
            (root/'docs/complete-questions/q-1.json').write_text(json.dumps(parent))
            (root/'docs/complete-questions/q-2.json').write_text(json.dumps(parent['groupQuestions'][1]))
            (root/'site/dist/data.json').write_text(json.dumps({'questions':[]}))
            for qid in ['q-1','q-2']:(root/f'docs/comics/{qid}.json').write_text(json.dumps(comic_spec(qid)))
            with patch.object(module,'ROOT',root),patch.object(module,'optimize_payload',side_effect=lambda value:value):
                module.attach('q-1');module.attach('q-2')
            final=json.loads((root/'docs/complete-questions/q-1.json').read_text())
            self.assertIsNone(final['teachingComic'])
            self.assertEqual(final['question'],'共同材料')
            self.assertEqual([(q['question'],q['answer']) for q in final['groupQuestions']],[('第一原問','A'),('第二原問','B')])
            self.assertTrue(all(c['teachingComic']['fourth']['image'] for c in final['groupQuestions']))
            self.assertEqual(final['groupQuestions'][1]['teachingComic'],json.loads((root/'docs/complete-questions/q-2.json').read_text())['teachingComic'])


if __name__ == '__main__':
    unittest.main()
