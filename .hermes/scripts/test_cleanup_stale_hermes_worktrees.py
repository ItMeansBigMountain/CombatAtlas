#!/usr/bin/env python3
import importlib.util
import os
from pathlib import Path
import tempfile
import time
import unittest

SPEC = importlib.util.spec_from_file_location("cleanup", "/opt/data/scripts/cleanup_stale_hermes_worktrees.py")
cleanup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cleanup)


class CleanupSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.old_tmp = cleanup.TMP_ROOT
        cleanup.TMP_ROOT = self.root
        self.now = time.time()

    def tearDown(self):
        cleanup.TMP_ROOT = self.old_tmp
        self.temp.cleanup()

    def make_dir(self, name, age_hours=72):
        path = self.root / name
        path.mkdir()
        (path / "payload").write_bytes(b"x" * 4096)
        stamp = self.now - age_hours * 3600
        os.utime(path, (stamp, stamp))
        return path

    def test_old_allowlisted_directory_is_eligible(self):
        path = self.make_dir("hermez-reconcile.ABC123")
        self.assertEqual(cleanup.classify(path, 48, set(), self.now), (True, "stale_allowlisted_worktree"))

    def test_unknown_prefix_is_never_eligible(self):
        path = self.make_dir("important-project")
        self.assertEqual(cleanup.classify(path, 48, set(), self.now)[1], "prefix_not_allowed")

    def test_recent_directory_is_protected(self):
        path = self.make_dir("hermez-reconcile.RECENT", age_hours=2)
        self.assertEqual(cleanup.classify(path, 48, set(), self.now)[1], "within_grace_period")

    def test_keep_marker_protects_directory(self):
        path = self.make_dir("hermez-reconcile.KEEP")
        (path / cleanup.KEEP_MARKER).touch()
        self.assertEqual(cleanup.classify(path, 48, set(), self.now)[1], "keep_marker")

    def test_process_reference_protects_directory(self):
        path = self.make_dir("hermez-reconcile.ACTIVE")
        child = path / "child"
        child.mkdir()
        stamp = self.now - 72 * 3600
        os.utime(path, (stamp, stamp))
        self.assertEqual(cleanup.classify(path, 48, {child.resolve()}, self.now)[1], "active_process_reference")

    def test_symlink_is_never_deleted(self):
        target = self.make_dir("important-project")
        link = self.root / "hermez-reconcile.LINK"
        link.symlink_to(target, target_is_directory=True)
        self.assertEqual(cleanup.classify(link, 48, set(), self.now)[1], "not_real_directory")


if __name__ == "__main__":
    unittest.main()
