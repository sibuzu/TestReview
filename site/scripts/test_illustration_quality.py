import json
from pathlib import Path
import tempfile
import unittest
from illustration_quality import biology_quality


class BiologyQualityTests(unittest.TestCase):
    def test_draft_or_legacy_complete_flag_is_not_enough_for_fine_label(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);base=root/'docs/comics';base.mkdir(parents=True)
            entries=[dict(id='q-1',subject='Biology',state='complete',reasons=['biology_quality_upgrade']),
                     dict(id='q-2',subject='Biology',state='complete',reasons=['biology_quality_upgrade']),
                     dict(id='q-3',subject='Biology',state='queued',reasons=['missing_illustration'])]
            plan=base/'biology-rework-20261112/plan.json';plan.parent.mkdir();plan.write_text(json.dumps({'entries':entries}))
            (base/'q-1.json').write_text(json.dumps({'fourth':{'image':'draft.png'}}))
            (base/'q-2.json').write_text(json.dumps({'visualChecked':True,'rootReview':{'visualChecked':True,'originalVisualChecked':True,'answerAndExplanationChecked':True,'fourActualIndependentImages':True}}))
            quality=biology_quality(root)
            self.assertEqual([quality['q-'+str(i)]['state'] for i in range(1,4)],['legacy','fine','missing'])
            self.assertTrue(quality['q-1']['draftPendingReview'])
