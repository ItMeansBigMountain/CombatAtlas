import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).with_name("expire_kanban_corruption_forensics.py")
spec = importlib.util.spec_from_file_location("expiry", SCRIPT)
expiry = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(expiry)


def make_db(path: Path) -> None:
    con = sqlite3.connect(path)
    con.execute("create table t(x integer)")
    con.commit()
    con.close()


class ExpiryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.live = self.root / "kanban.db"
        make_db(self.live)
        self.ledger = self.root / "forensics/expired.jsonl"
        self.lock = self.root / "forensics/.lock"
        self.patchers = [
            mock.patch.object(expiry, "ROOT", self.root),
            mock.patch.object(expiry, "LIVE_DB", self.live),
            mock.patch.object(expiry, "LEDGER", self.ledger),
            mock.patch.object(expiry, "LOCK", self.lock),
            mock.patch.object(expiry, "open_paths", return_value=set()),
        ]
        for p in self.patchers:
            p.start()

    def tearDown(self):
        for p in reversed(self.patchers):
            p.stop()
        self.tmp.cleanup()

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch("sys.argv", [str(SCRIPT), *args]), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = expiry.main()
        return code, out.getvalue(), err.getvalue()

    def test_old_snapshot_is_logged_then_deleted(self):
        bad = self.root / "kanban.db.corrupt.abc.bak"
        bad.write_bytes(b"not sqlite")
        os.utime(bad, (1, 1))
        code, out, err = self.run_main("--apply", "--retention-days", "30", "--now", str(40 * 86400))
        self.assertEqual(code, 0, err)
        self.assertFalse(bad.exists())
        self.assertTrue(self.ledger.exists())
        self.assertIn('"deleted": 1', out)
        self.assertIn('"sha256"', self.ledger.read_text())

    def test_recent_snapshot_holds_entire_set(self):
        old = self.root / "kanban.db.corrupt.old.bak"
        recent = self.root / "kanban.db.corrupt.new.bak"
        old.write_bytes(b"old")
        recent.write_bytes(b"new")
        os.utime(old, (1, 1))
        os.utime(recent, (39 * 86400, 39 * 86400))
        code, out, err = self.run_main("--apply", "--retention-days", "30", "--now", str(40 * 86400))
        self.assertEqual(code, 0, err)
        self.assertTrue(old.exists())
        self.assertTrue(recent.exists())
        self.assertFalse(self.ledger.exists())

    def test_unhealthy_live_db_refuses_deletion(self):
        self.live.unlink()
        self.live.write_bytes(b"broken")
        bad = self.root / "kanban.db.corrupt.abc.bak"
        bad.write_bytes(b"old")
        os.utime(bad, (1, 1))
        code, out, err = self.run_main("--apply", "--now", str(40 * 86400))
        self.assertEqual(code, 1)
        self.assertTrue(bad.exists())
        self.assertIn("live Kanban database is not healthy", err)

    def test_retention_under_seven_days_is_refused(self):
        code, out, err = self.run_main("--apply", "--retention-days", "1")
        self.assertEqual(code, 2)
        self.assertIn("at least 7 days", err)


if __name__ == "__main__":
    unittest.main()
