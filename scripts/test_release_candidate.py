"""Negative checks for the candidate manifest contract; not educational review."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import validate_release_candidate as candidate


class CandidateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ("data/reviews", "dist"):
            (self.root / folder).mkdir(parents=True)
        (self.root / "dist/release.json").write_bytes(candidate.encoded({"research_commit": None, "freeze_status": "pending-separate-release-audit"}))
        (self.root / "dist/app.js").write_bytes(b"original")
        self.inventory = patch.object(candidate, "inventory", lambda root: ["dist/app.js"])
        self.inventory.start()
        self.addCleanup(self.inventory.stop)
        record = {"result": "pass-builder-validation-with-recorded-limits", "checks": [{"exit_code": 0}]}
        manifest = candidate.make_manifest(self.root, record)
        for name, value in ((candidate.RECORD, record), (candidate.MANIFEST, manifest), (candidate.EXPORT, manifest)):
            (self.root / name).write_bytes(candidate.encoded(value))

    def test_baseline_and_commit_pointer_cycle_exclusion(self):
        candidate.verify(self.root)
        release = json.loads((self.root / "dist/release.json").read_bytes())
        release["research_commit"] = "later-exact-commit-bound-by-publication-receipt"
        (self.root / "dist/release.json").write_bytes(candidate.encoded(release))
        candidate.verify(self.root)

    def test_changed_asset_fails(self):
        (self.root / "dist/app.js").write_bytes(b"changed")
        with self.assertRaises(ValueError):
            candidate.verify(self.root)

    def test_release_semantic_change_fails(self):
        (self.root / "dist/release.json").write_bytes(candidate.encoded({"research_commit": None, "freeze_status": "authorized"}))
        with self.assertRaises(ValueError):
            candidate.verify(self.root)

    def test_public_export_change_fails(self):
        (self.root / candidate.EXPORT).write_bytes(b"{}")
        with self.assertRaises(ValueError):
            candidate.verify(self.root)

    def test_failed_evidence_cannot_pass(self):
        (self.root / candidate.RECORD).write_bytes(candidate.encoded({"result": "failed"}))
        with self.assertRaises(ValueError):
            candidate.verify(self.root)


if __name__ == "__main__":
    unittest.main()
