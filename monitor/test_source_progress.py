import copy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from .comic_pipeline import load, save
from .source_progress import update_source


class SourceProgressTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory)
        (root/'docs/imports').mkdir(parents=True)
        # Deliberately not list order: source order is identity, not position.
        data = {'sources': [
            {'order': 62, 'url': 'https://source/62', 'questionIds': []},
            {'order': 60, 'url': 'https://source/60', 'questionIds': ['q-820']},
            {'order': 61, 'url': 'https://source/61', 'questionIds': []},
        ]}
        save(root/'docs/imports/more-gemini-progress.json', data)
        return root, copy.deepcopy(data)

    def test_only_exact_order_changes_even_when_rows_reordered(self):
        with TemporaryDirectory() as directory:
            root, before = self.fixture(directory)
            update_source(root, 62, {'sourceKey': 'gemini062', 'questionIds': ['q-835']}, source_url='https://source/62')
            after=load(root/'docs/imports/more-gemini-progress.json')
            self.assertEqual(after['sources'][1:], before['sources'][1:])
            self.assertEqual(after['sources'][0]['questionIds'], ['q-835'])

    def test_wrong_source_url_or_key_cannot_corrupt_another_source(self):
        with TemporaryDirectory() as directory:
            root, before = self.fixture(directory)
            for order, metadata, url in [(60, {}, 'https://source/62'),
                                          (60, {'sourceKey':'gemini062'}, 'https://source/60')]:
                with self.assertRaises(ValueError):
                    update_source(root, order, metadata, source_url=url)
                self.assertEqual(load(root/'docs/imports/more-gemini-progress.json'), before)

    def test_verified_url_alias_preserves_original_link_and_is_idempotent(self):
        with TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            for _ in range(2):
                row=update_source(root, 61, {'questionIds':['q-829']}, source_url='https://final/61', aliases=['https://source/61'])
            self.assertEqual(row['url'],'https://source/61')
            self.assertEqual(row['questionIds'],['q-829'])
