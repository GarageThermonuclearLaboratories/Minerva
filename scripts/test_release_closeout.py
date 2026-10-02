"""Reject incomplete validation evidence and stale closeout review boundaries."""
import copy
import unittest
import verify_release_closeout as closeout


class CloseoutTests(unittest.TestCase):
    def setUp(self):
        self.record = {"result": "pass-builder-validation-with-recorded-limits",
                       "checks": [{"command": command, "exit_code": 0} for command in closeout.expected_commands()],
                       "test_counts": {"integrity_assertions": 79, "comparison_tests": 25, "acceptance_tests": 28,
                                       "ingestion_tests": 7, "release_manifest_tests": 5, "ask_checks": 91,
                                       "archived_independent_probe_replay": 72, "dom_views": 9}}

    def test_exact_evidence_passes(self):
        closeout.check_evidence(self.record)

    def test_missing_command_fails(self):
        self.record["checks"].pop()
        with self.assertRaises(ValueError):
            closeout.check_evidence(self.record)

    def test_duplicate_command_fails(self):
        self.record["checks"][1] = copy.deepcopy(self.record["checks"][0])
        with self.assertRaises(ValueError):
            closeout.check_evidence(self.record)

    def test_failed_command_fails(self):
        self.record["checks"][0]["exit_code"] = 1
        with self.assertRaises(ValueError):
            closeout.check_evidence(self.record)

    def test_false_count_fails(self):
        self.record["test_counts"]["ask_checks"] = 1
        with self.assertRaises(ValueError):
            closeout.check_evidence(self.record)

    def test_attestation_binds_exact_envelope(self):
        envelope = b"exact candidate"
        review = {"result": "pass-with-recorded-limits", "blocking_findings": [],
                  "reviewed_envelope_sha256": closeout.sha(envelope)}
        closeout.verify_attestation(envelope, review)
        with self.assertRaises(ValueError):
            closeout.verify_attestation(b"later change", review)

    def test_blocking_review_fails(self):
        envelope = b"candidate"
        with self.assertRaises(ValueError):
            closeout.verify_attestation(envelope, {"result": "pass-with-recorded-limits", "blocking_findings": ["unrepaired"],
                                                   "reviewed_envelope_sha256": closeout.sha(envelope)})


if __name__ == "__main__":
    unittest.main()
