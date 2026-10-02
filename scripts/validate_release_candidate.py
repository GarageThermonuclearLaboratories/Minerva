#!/usr/bin/env python3
"""Run bounded Friday checks (--write), or verify their hash-bound candidate."""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "data/reviews/friday-release-manifest.json"
RECORD = "data/reviews/friday-candidate-validation.json"
EXPORT = "dist/release-manifest.json"
EXCLUDED = {MANIFEST, RECORD, EXPORT, "dist/release.json"}
BASE_GITHUB = "5da24fefc43e2c396e045fbfeb75c7cfdeaa65ea"
BASE_SITE = "98297ced98c362ece155ab7ca9453fa83bee3a0f"


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def sha(content):
    return hashlib.sha256(content).hexdigest()


def inventory(root):
    # Complete delivery assets, research inputs, archive/processing products,
    # review evidence and executable checks. Publication receipts and narrative
    # history are commit-bound, not self-referential manifest inputs.
    paths = set()
    for folder in ("dist", "sources", "scripts", "schema", "data"):
        for path in (root / folder).rglob("*"):
            name = path.relative_to(root).as_posix()
            if (path.is_file() and "__pycache__" not in path.parts
                    and name not in EXCLUDED and not name.startswith("data/publications/")):
                paths.add(name)
    paths.update(("package.json", "package-lock.json", "requirements.txt",
                  ".openai/hosting.json", "docs/foundation-specification.md",
                  "docs/decisions.md", "docs/friday-release-candidate.md"))
    return sorted(paths)


def release_semantics(root):
    release = json.loads((root / "dist/release.json").read_bytes())
    release.pop("research_commit")  # exact pointer is bound by native receipt
    return release


def make_manifest(root, record):
    return {
        "schema_version": 1,
        "candidate_id": "wildcats-friday-v0.1-candidate-2026-10-02",
        "ontology_release": "wildcats-0.0.8-wednesday-comparisons",
        "policy_snapshot": "2026-09-28",
        "status": "validated-unfrozen-candidate-awaiting-separate-release-audit",
        "base_checkpoint": {"site_version": 19, "github_commit": BASE_GITHUB,
                            "site_source_commit": BASE_SITE},
        "validation_record": RECORD,
        "validation_record_sha256": sha(encoded(record)),
        "artifacts_sha256": {name: sha((root / name).read_bytes()) for name in inventory(root)},
        "release_semantics": release_semantics(root),
        "coverage": {"nodes": 26, "edges": 31, "parsed_expectations": 9,
                     "findings": 0, "source_records": 47, "archived_pdfs": 42,
                     "archived_pages": 1237, "comparisons": 3},
        "review_boundary": "Builder validation and replay of Thursday's archived harness, not a new independent verdict. User acceptance applies to Site version 18; later status changes are builder-checked.",
        "hash_boundary": "All dist assets except this manifest/export and release.json are hashed. Release metadata is canonicalized without research_commit to avoid a self-referential commit hash. Data, sources, scripts, schema, dependencies, hosting configuration and named scope documents are hashed. Other documentation, README, Lab Log and publication receipts are bound by Git commits, not this artifact inventory. The native publication receipt binds the exact candidate GitHub commit, Site source commit, saved version and archive hash afterward.",
        "clean_room": "No Garage ontology was consulted or introduced. Compliance is a documented construction boundary, not proven by a hash or automated contamination detector.",
        "remaining_gate": "separate final release audit of this exact candidate, repairs if needed, and explicit freeze decision",
        "freeze_authorized": False,
        "immutable_tag_authorized": False,
    }


def verify(root):
    record = json.loads((root / RECORD).read_bytes())
    manifest = json.loads((root / MANIFEST).read_bytes())
    if record.get("result") != "pass-builder-validation-with-recorded-limits":
        raise ValueError("validation record is not a passing builder result")
    if not record.get("checks") or any(check.get("exit_code") != 0 for check in record["checks"]):
        raise ValueError("validation evidence has missing or failed commands")
    if manifest != make_manifest(root, record):
        raise ValueError("candidate inventory, hashes or release semantics changed; revalidate before audit")
    if (root / MANIFEST).read_bytes() != (root / EXPORT).read_bytes():
        raise ValueError("public release manifest differs")
    if sha((root / RECORD).read_bytes()) != manifest["validation_record_sha256"]:
        raise ValueError("validation record bytes differ")
    return manifest


def run_checks(root):
    if sys.flags.optimize:
        raise ValueError("run without Python optimization; existing validators use assertions")
    import fitz
    jsdom = subprocess.check_output(["node", "-p", "require('jsdom/package.json').version"], cwd=root, text=True).strip()
    if fitz.VersionBind != "1.26.6" or jsdom != "27.4.0":
        raise ValueError("install the pinned PyMuPDF and jsdom versions before validation")
    commands = [
        [sys.executable, "scripts/check_freeze_readiness.py"],
        [sys.executable, "scripts/validate.py"],
        [sys.executable, "scripts/ingest_sources.py", "check"],
        [sys.executable, "scripts/test_comparisons.py"],
        [sys.executable, "scripts/test_acceptance.py"],
        [sys.executable, "scripts/test_ingestion.py"],
        [sys.executable, "scripts/test_release_candidate.py"],
        ["node", "scripts/test_ask.js"],
        ["node", "scripts/test_thursday_independent.cjs", "."],
        ["node", "scripts/test_receipts.js"],
        ["node", "scripts/test_interface.cjs"],
        *[["node", "--check", name] for name in sorted(inventory(root)) if name.startswith("dist/") and name.endswith(".js")],
        ["git", "diff", "--check"],
    ]
    results = []
    for command in commands:
        done = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=120)
        output = done.stdout + done.stderr
        print(f"{'PASS' if done.returncode == 0 else 'FAIL'} {' '.join(command[1:] if command[0] == sys.executable else command)}", flush=True)
        if done.returncode:
            raise ValueError(output[-6000:])
        summary = output[-1000:]
        if "scripts/test_thursday_independent.cjs" in command:
            replay = json.loads(done.stdout)
            if replay["total"] != 72 or replay["failures"] != 0:
                raise ValueError("archived independent harness replay mismatch")
            summary = "72 archived independent probes replayed by builder; zero failures; not a new independent review"
        results.append({"command": ["python3" if part == sys.executable else part for part in command],
                        "exit_code": done.returncode, "output_sha256": sha(output.encode()),
                        "output_tail_or_summary": summary})
    node = subprocess.check_output(["node", "--version"], text=True).strip()
    return {"id": "review:friday-candidate-validation", "date": "2026-10-02",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "reviewer_type": "builder-regression-validation", "model_and_effort": "not asserted by this artifact",
            "result": "pass-builder-validation-with-recorded-limits",
            "environment": {"python": platform.python_version(), "node": node,
                            "pymupdf": fitz.VersionBind, "jsdom": jsdom},
            "checks": results,
            "test_counts": {"integrity_assertions": 79, "comparison_tests": 25,
                            "acceptance_tests": 28, "ingestion_tests": 7,
                            "release_manifest_tests": 5, "ask_checks": 91,
                            "archived_independent_probe_replay": 72, "dom_views": 9},
            "findings": [{"id": "F2-1", "severity": "reproducibility-gap", "status": "repaired",
                          "description": "DOM checks depended on transient unrecorded jsdom. package.json and package-lock.json now pin jsdom 27.4.0."}],
            "limitations": ["Mechanical source fidelity and hashes do not certify all-document semantic review or current URL byte equivalence.",
                            "No new rendered browser, zoom, full-accessibility or independent release review.",
                            "Policy question remains September 28, 2026; no refreshed applicability/cohort determination.",
                            "Clean-room boundary is documented, not mechanically proven."],
            "freeze_authorized": False, "immutable_tag_authorized": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rerun all checks and generate candidate evidence")
    args = parser.parse_args()
    if args.write:
        record = run_checks(ROOT)
        manifest = make_manifest(ROOT, record)
        for name, value in ((RECORD, record), (MANIFEST, manifest), (EXPORT, manifest)):
            (ROOT / name).write_bytes(encoded(value))
    manifest = verify(ROOT)
    print(f"Candidate manifest verified: {len(manifest['artifacts_sha256'])} hashed artifacts; separate release audit pending; freeze/tag unauthorized.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(f"candidate validation failed: {error}")
