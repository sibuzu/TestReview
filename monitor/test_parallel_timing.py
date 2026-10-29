import unittest
from .parallel_timing import measure


class ParallelTimingTests(unittest.TestCase):
    def test_first_twenty_uses_wall_clock_and_excludes_pending_and_baseline(self):
        batch = {'startedAt': '2026-10-28T16:00:00+00:00', 'target': 20,
                 'baselineSettledIds': ['old'],
                 'baselines': [{'averageSecondsPerWork': 120}]}
        entries = [{'id': f'q-{i}', 'state': 'complete' if i % 2 else 'existing_ai',
                    'completedAt': f'2026-10-28T16:{i:02}:00+00:00'} for i in range(1, 22)]
        entries += [{'id': 'old', 'state': 'complete', 'completedAt': '2026-10-28T16:00:01+00:00'},
                    {'id': 'pending', 'state': 'awaiting_confirmation', 'completedAt': '2026-10-28T16:00:02+00:00'}]
        result = measure(batch, list(reversed(entries)))
        self.assertEqual(result['completed'], 20)
        self.assertEqual(result['averageSecondsPerQuestion'], 60)
        self.assertEqual(result['elapsedSeconds'], 1200)
        self.assertEqual(result['comparisons'][0]['speedup'], 2)
        self.assertEqual(result['comparisons'][0]['changePercent'], -50)
        self.assertEqual(result['mix'], {'complete': 10, 'existing_ai': 10})
        self.assertEqual(measure(result, []), result)

    def test_incomplete_does_not_publish_final_average(self):
        result = measure({'state': 'running', 'startedAt': '2026-10-28T16:00:00+00:00',
                          'target': 20, 'baselineSettledIds': [], 'baselines': []}, [])
        self.assertEqual(result['state'], 'running')
        self.assertEqual(result['completed'], 0)
        self.assertNotIn('averageSecondsPerQuestion', result)
