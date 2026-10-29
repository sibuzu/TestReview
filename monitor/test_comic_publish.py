import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from pathlib import Path
from . import comic_publish
from .comic_pipeline import save


class PublishCountingTests(unittest.TestCase):
    def test_counts_verified_rework_rounds_after_successful_push_only(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'docs/comics').mkdir(parents=True)
            (root/'.cache').mkdir()
            save(root/'docs/comics/commit-policy.json', {'baselineAt':'2026-10-29T00:00:00+00:00','batchSize':20})
            jobs=[
                {'id':'q-1','state':'integrated','decision':'complete','integratedAt':'2026-10-28T23:59:00+00:00'},
                {'id':'q-1','state':'integrated','decision':'complete','integratedAt':'2026-10-29T01:00:00+00:00'},
                {'id':'q-2','state':'integrated','decision':'not_suitable','integratedAt':'2026-10-29T01:01:00+00:00'},
                {'id':'q-3','state':'ready','decision':'complete'},
                {'id':'q-4','state':'blocked','decision':'awaiting_confirmation'},
                {'id':'q-5','state':'integrated','decision':'complete','integratedAt':'2026-10-29T01:02:00+00:00'}]
            save(root/'docs/comics/pipeline.json', {'jobs':jobs})
            with patch.object(comic_publish,'ROOT',root):
                self.assertEqual([j['id'] for j in comic_publish.pending_batch()[3]],['q-1','q-5'])
                save(root/'.cache/comic-publish-state.json',{'throughIntegratedAt':'2026-10-29T01:00:00+00:00'})
                self.assertEqual([j['id'] for j in comic_publish.pending_batch()[3]],['q-5'])
