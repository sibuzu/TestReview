import unittest
from monitor.comic_queue import next_entry, subject_stats


class ComicQueueTest(unittest.TestCase):
    def entry(self, subject, n, state='queued', date='2026-10-01'):
        return dict(id=f'q-{n:03}', subject=subject, state=state, date=date)

    def test_squared_completed_score_precedes_percentage_and_newest_is_selected(self):
        entries = [self.entry('Chinese', i, 'complete' if i < 10 else 'queued') for i in range(100)]
        entries += [self.entry('Earth', 100+i, 'complete' if i < 2 else 'queued') for i in range(10)]
        entries[-1]['date'] = '2026-10-20'
        # Chinese: 10/100 complete, score 1. Earth: 2/10 complete, score .4.
        # Earth wins even though Chinese has the lower completion percentage.
        self.assertEqual(next_entry(entries)['id'], 'q-109')
        row = subject_stats(entries)[0]
        self.assertEqual((row['subject'], row['completed'], row['total']), ('Earth', 2, 10))
        self.assertEqual(row['priorityScore'], .4)

    def test_equal_score_prefers_larger_remaining_count(self):
        entries = [self.entry('Chinese', 1), self.entry('Chinese', 2), self.entry('Earth', 3)]
        self.assertEqual(next_entry(entries)['subject'], 'Chinese')

    def test_sort_uses_exact_score_before_display_rounding(self):
        entries = [self.entry('Chinese', i, 'complete' if i < 5 else 'queued') for i in range(124)]
        entries += [self.entry('Earth', 200+i, 'complete' if i < 1 else 'queued') for i in range(5)]
        # Both display as .20, but 1/5 is smaller than 25/124.
        self.assertEqual(next_entry(entries)['subject'], 'Earth')

    def test_all_settled_kinds_count_but_confirmations_do_not(self):
        entries = [self.entry('Chinese', 1, 'complete'), self.entry('Chinese', 2, 'existing_ai'),
                   self.entry('Chinese', 3, 'not_suitable'), self.entry('Chinese', 4, 'awaiting_confirmation'),
                   self.entry('Chinese', 5)]
        row = subject_stats(entries)[0]
        self.assertEqual((row['completed'], row['remaining'], row['available']), (3, 2, 1))
        self.assertEqual(row['priorityScore'], 9/5)

    def test_completion_recalculates_and_waiting_subject_does_not_block(self):
        entries = [self.entry('Earth', 1), self.entry('Earth', 2), self.entry('Chinese', 3)]
        self.assertEqual(next_entry(entries)['subject'], 'Earth')
        entries[0]['state'] = 'existing_ai'
        self.assertEqual(next_entry(entries)['subject'], 'Chinese')
        entries[2]['state'] = 'awaiting_confirmation'
        self.assertEqual(next_entry(entries)['subject'], 'Earth')
        entries[1]['state'] = 'not_suitable'
        self.assertIsNone(next_entry(entries))
