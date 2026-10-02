#!/usr/bin/env python3
"""Verify historical version 20 and a separately reviewed, unfrozen closeout."""
import argparse
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENVELOPE = "data/releases/friday-audit-closeout.json"
EXPORT = "dist/release-audit.json"
ATTESTATION = "data/reviews/friday-closeout-review.json"
ORIGINAL_MANIFEST = "data/reviews/friday-release-manifest.json"
ORIGINAL_RECORD = "data/reviews/friday-candidate-validation.json"
MANIFEST_SHA = "e0aebcd457dd384f5d742d48d28869a427457666a6825e203d1d4ce509c22851"
RECORD_SHA = "861a5d3fae2f257585c3a6fd7e74851dee53232ffd269d47639aa9dea20f1d30"
RESEARCH_REF = "049d7c657f0e0535b8403c6fcac65183ef9442f9"
SITE_REF = "a79f62871a225a8c1ff12507c9c009d5bcecc5a8"
INPUTS = ["README.md", "dist/interface.js", "scripts/test_interface.cjs",
          "scripts/verify_release_closeout.py", "scripts/test_release_closeout.py",
          "docs/friday-release-audit.md", "data/reviews/friday-independent.json",
          "data/publications/friday-release-candidate.json",
          *["docs/review-assets/friday/" + name for name in
            ("friday-release-audit.md", "audit-fingerprints.json", "negative-probes.py",
             "negative-results.json", "runtime-probes.cjs", "runtime-results.json",
             "full-replay.json", "native-readback.json", "github-candidate-tree.json")]]
ALLOWED_CHANGES = set(INPUTS + ["dist/release.json", "docs/lab-log.md", ENVELOPE, EXPORT,
                              ATTESTATION, "data/publications/friday-reviewed.json"])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def expected_commands():
    return [["python3", "scripts/" + script] for script in
            ("check_freeze_readiness.py", "validate.py")] + [
        ["python3", "scripts/ingest_sources.py", "check"],
        *[["python3", "scripts/" + script] for script in
          ("test_comparisons.py", "test_acceptance.py", "test_ingestion.py", "test_release_candidate.py")],
        ["node", "scripts/test_ask.js"], ["node", "scripts/test_thursday_independent.cjs", "."],
        ["node", "scripts/test_receipts.js"], ["node", "scripts/test_interface.cjs"],
        *[["node", "--check", "dist/" + script] for script in
          ("app.js", "ask-engine.js", "ask-ui.js", "comparison-ui.js", "interface.js")],
        ["git", "diff", "--check"]]


def check_evidence(record):
    if record.get("result") != "pass-builder-validation-with-recorded-limits":
        raise ValueError("candidate validation result is not passing")
    checks = record.get("checks", [])
    if [check.get("command") for check in checks] != expected_commands():
        raise ValueError("required ordered validation-command inventory differs")
    if any(check.get("exit_code") != 0 for check in checks):
        raise ValueError("a required validation command failed")
    counts = {"integrity_assertions": 79, "comparison_tests": 25, "acceptance_tests": 28,
              "ingestion_tests": 7, "release_manifest_tests": 5, "ask_checks": 91,
              "archived_independent_probe_replay": 72, "dom_views": 9}
    if record.get("test_counts") != counts:
        raise ValueError("expected bounded validation counts differ")


def historical_candidate(root):
    # The two repositories have different histories, with identical candidate
    # inputs except the intentionally excluded release research pointer.
    ref = next((ref for ref in (RESEARCH_REF, SITE_REF) if subprocess.run(
        ["git", "cat-file", "-e", ref + "^{commit}"], cwd=root, capture_output=True).returncode == 0), None)
    if ref is None:
        raise ValueError("exact research/Site version 20 commit is not available locally")
    data = subprocess.check_output(["git", "archive", "--format=tar", ref], cwd=root)
    with tempfile.TemporaryDirectory(prefix="minerva-reviewed-") as temporary:
        snapshot = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            archive.extractall(snapshot, filter="data")
        subprocess.run([sys.executable, "scripts/restore_sources.py"], cwd=snapshot,
                       check=True, capture_output=True)
        spec = importlib.util.spec_from_file_location("historical_candidate", snapshot / "scripts/validate_release_candidate.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        manifest = module.verify(snapshot)
        if sha((snapshot / ORIGINAL_MANIFEST).read_bytes()) != MANIFEST_SHA:
            raise ValueError("historical candidate manifest fingerprint differs")
        if sha((snapshot / ORIGINAL_RECORD).read_bytes()) != RECORD_SHA:
            raise ValueError("historical candidate evidence fingerprint differs")
    # Keep original evidence byte-identical in the current checkout too.
    if sha((root / ORIGINAL_MANIFEST).read_bytes()) != MANIFEST_SHA or sha((root / ORIGINAL_RECORD).read_bytes()) != RECORD_SHA:
        raise ValueError("historical evidence was overwritten")
    check_evidence(json.loads((root / ORIGINAL_RECORD).read_bytes()))
    changed = set(subprocess.check_output(["git", "diff", "--name-only", ref, "--"], cwd=root, text=True).splitlines())
    changed.update(subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=root, text=True).splitlines())
    if changed - ALLOWED_CHANGES:
        raise ValueError("undeclared closeout changes: " + ", ".join(sorted(changed - ALLOWED_CHANGES)))
    for name, expected in manifest["artifacts_sha256"].items():
        if name not in ALLOWED_CHANGES and sha((root / name).read_bytes()) != expected:
            raise ValueError("reviewed artifact changed: " + name)
    return manifest


def make_envelope(root):
    release = json.loads((root / "dist/release.json").read_bytes())
    release.pop("research_commit")
    return {"schema_version": 1, "checkpoint": "friday-package-3-reviewed-tag-pending",
            "historical_candidate": {"site_version": 20, "research_commit": RESEARCH_REF,
                                     "site_source_commit": SITE_REF, "manifest_sha256": MANIFEST_SHA,
                                     "validation_record_sha256": RECORD_SHA},
            "closeout_artifacts_sha256": {name: sha((root / name).read_bytes()) for name in INPUTS},
            "release_semantics": release,
            "attestation_record": ATTESTATION,
            "attestation_boundary": "Separate reviewer attests this exact envelope after its hashes are fixed. Attestation and postpublication receipt are excluded to avoid self-reference and are bound by Git commits. Lab Log is postpublication narrative, also Git-bound. research_commit is pinned after GitHub commit and bound by the native publication receipt.",
            "freeze_decision": "partial foundation candidate approved with limits; completed tagged freeze remains blocked",
            "tag_status": "not-created; connected GitHub tools expose no tag-write operation",
            "proposed_tag": "wildcats-foundation-v0.1",
            "clean_room_crosswalk": "still-prohibited-until-actual-tagged-freeze",
            "statewide_ontology_complete": False, "tagged_freeze_complete": False,
            "freeze_authorized": False, "immutable_tag_created": False}


def verify_attestation(envelope_bytes, attestation):
    if attestation.get("result") != "pass-with-recorded-limits" or attestation.get("blocking_findings") != []:
        raise ValueError("separate closeout review has not passed")
    if attestation.get("reviewed_envelope_sha256") != sha(envelope_bytes):
        raise ValueError("separate verdict covers a different closeout envelope")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true", help="prepare envelope before separate closeout re-review")
    args = parser.parse_args()
    historical_candidate(ROOT)
    value = make_envelope(ROOT)
    if args.prepare:
        (ROOT / ENVELOPE).parent.mkdir(parents=True, exist_ok=True)
        for name in (ENVELOPE, EXPORT):
            (ROOT / name).write_bytes(encoded(value))
        print("Closeout envelope prepared; separate scoped verdict required before publication.")
        return
    original = (ROOT / ENVELOPE).read_bytes()
    if original != encoded(value) or original != (ROOT / EXPORT).read_bytes():
        raise ValueError("closeout inputs, release semantics or public envelope changed")
    verify_attestation(original, json.loads((ROOT / ATTESTATION).read_bytes()))
    print("Historical candidate and separately reviewed closeout verified; immutable GitHub tag still pending; no completed freeze claimed.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(f"closeout verification failed: {error}")
