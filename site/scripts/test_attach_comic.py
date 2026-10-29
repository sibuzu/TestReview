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


if __name__ == '__main__':
    unittest.main()
