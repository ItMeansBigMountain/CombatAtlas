import json
import tempfile
import unittest
from pathlib import Path

from toolkit.lib.storage import JsonStore
from toolkit.tools.where_was_i import WhereWasITracker
from toolkit.tools.clipboard_history import ClipboardHistory
from toolkit.tools.location_reminders import LocationReminderStore, distance_meters
from toolkit.agent_tick import run_tick


class PocketToolkitTests(unittest.TestCase):
    def test_where_was_i_logs_and_summarizes_points(self):
        with tempfile.TemporaryDirectory() as tmp:
            tracker = WhereWasITracker(JsonStore(Path(tmp) / 'where.json'))
            tracker.log_point(latitude=40.0, longitude=-74.0, label='Coffee', note='Met client')
            tracker.log_point(latitude=40.001, longitude=-74.001, label='Gym')
            today = tracker.timeline_for_date()
            self.assertEqual(len(today), 2)
            self.assertEqual(today[0]['label'], 'Coffee')
            self.assertIn('Coffee', tracker.daily_summary())

    def test_clipboard_history_dedupes_and_limits_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            history = ClipboardHistory(JsonStore(Path(tmp) / 'clip.json'), limit=2)
            history.capture('alpha')
            history.capture('alpha')
            history.capture('beta')
            history.capture('gamma')
            entries = history.entries()
            self.assertEqual([item['text'] for item in entries], ['gamma', 'beta'])
            self.assertEqual(history.search('bet')[0]['text'], 'beta')

    def test_location_reminders_find_nearby_uncompleted_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocationReminderStore(JsonStore(Path(tmp) / 'reminders.json'))
            reminder = store.add('Buy printer paper', latitude=40.0, longitude=-74.0, radius_m=150)
            self.assertTrue(distance_meters(40.0, -74.0, 40.001, -74.001) < 150)
            nearby = store.nearby(latitude=40.001, longitude=-74.001)
            self.assertEqual(nearby[0]['id'], reminder['id'])
            store.complete(reminder['id'])
            self.assertEqual(store.nearby(latitude=40.001, longitude=-74.001), [])
    def test_agent_tick_captures_location_clipboard_and_nearby_reminders(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocationReminderStore(JsonStore(Path(tmp) / 'location_reminders.json'))
            store.add('Grab milk', latitude=40.0, longitude=-74.0, radius_m=150)
            result = run_tick(
                data_dir=Path(tmp),
                location_provider=lambda: {'latitude': 40.001, 'longitude': -74.001, 'horizontal_accuracy': 12},
                clipboard_provider=lambda: 'https://example.com/useful-link',
                notify_func=lambda title, message: None,
            )
            self.assertTrue(result['location_logged'])
            self.assertEqual(result['clipboard_captured']['kind'], 'url')
            self.assertEqual(result['nearby_reminders'][0]['text'], 'Grab milk')


if __name__ == '__main__':
    unittest.main()
