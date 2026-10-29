from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from comic_policy import apply_comic_policy


class ArtworkPolicyTests(unittest.TestCase):
    def test_remove_source_ai_explanations_preserves_exam_and_official_material(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'docs/comics').mkdir(parents=True)
            (root/'docs/comics/policy.json').write_text('{"reuseSourceAI":false}')
            questions = [{'question': '完整原題', 'answer': 'C',
                          'images': ['assets/originals/exam.jpg'],
                          'questionFigures': [{'src': 'assets/questions/exam-cartoon.jpg', 'alt': '原卷漫畫'}],
                          'explanationFigures': [
                              {'src': 'assets/explanations/source-ai-old.webp', 'caption': '來源AI解說'},
                              {'src': 'assets/explanations/official.jpg', 'caption': '來源對話提供的官方導覽，非AI生成圖'},
                              {'src': 'assets/explanations/proof.svg', 'caption': '精確作圖'}]}]
            apply_comic_policy(questions, root)
            q = questions[0]
            self.assertEqual(q['question'], '完整原題')
            self.assertEqual(q['answer'], 'C')
            self.assertEqual(q['images'], ['assets/originals/exam.jpg'])
            self.assertEqual(q['questionFigures'][0]['src'], 'assets/questions/exam-cartoon.jpg')
            self.assertEqual([f['src'] for f in q['explanationFigures']],
                             ['assets/explanations/official.jpg', 'assets/explanations/proof.svg'])


if __name__ == '__main__':
    unittest.main()
