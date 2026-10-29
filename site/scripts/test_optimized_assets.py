"""Integrity checks for shared assets and safe publication cleanup."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import optimized_assets as assets


class PublicationTests(unittest.TestCase):
    def test_asset_mapping_preserves_question_content_and_shared_references(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            image = root / 'assets/comics/art-web.webp'
            image.parent.mkdir(parents=True)
            image.write_bytes(b'existing compressed image')
            manifest = root / 'map.json'
            manifest.write_text(json.dumps({'assets/comics/art.png': {
                'web': 'assets/comics/art-web.webp', 'originalSHA256': 'original'}}))
            original = {'question': '完整原題與四選項', 'answer': 'B',
                        'images': ['assets/originals/scan.jpg'],
                        'teachingComic': {'art': 'assets/comics/art.png'}}
            published = assets.optimize_payload(original, root, manifest)
            self.assertEqual(published['question'], original['question'])
            self.assertEqual(published['answer'], original['answer'])
            self.assertEqual(published['images'], original['images'])
            self.assertEqual(published['teachingComic']['art'], 'assets/comics/art-web.webp')
            self.assertEqual(original['teachingComic']['art'], 'assets/comics/art.png')

    def test_cleanup_keeps_data_style_and_svg_references_and_archives_unused_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'dist'
            (root / 'assets').mkdir(parents=True)
            for name in ['exam.jpg', 'icon.svg', 'background.png', 'inside.jpg', 'old.png']:
                (root / 'assets' / name).write_bytes(b'original bytes')
            (root / 'styles.css').write_text('background:url(assets/background.png)')
            (root / 'assets/icon.svg').write_text('<image href="assets/inside.jpg"/>')
            archive = Path(folder) / 'originals'
            with patch.object(assets, 'ARCHIVE', archive):
                removed = assets.prune_unreferenced(root, {'images': ['assets/exam.jpg', 'assets/icon.svg']})
            self.assertEqual([r['path'] for r in removed], ['assets/old.png'])
            self.assertEqual(Path(removed[0]['archive']).read_bytes(), b'original bytes')
            for name in ['exam.jpg', 'icon.svg', 'background.png', 'inside.jpg']:
                self.assertTrue((root / 'assets' / name).exists())


if __name__ == '__main__':
    unittest.main()
