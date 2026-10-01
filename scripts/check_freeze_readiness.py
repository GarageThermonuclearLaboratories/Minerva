#!/usr/bin/env python3
"""Verify the exact reviewed candidate and report the remaining freeze gate."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text())


def digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


checks: list[str] = []


def require(condition: bool, label: str) -> None:
    if not condition:
        raise SystemExit(f"freeze-readiness check failed: {label}")
    checks.append(label)


ontology = load("data/ontology.json")
comparisons = load("data/comparisons.json")
sources = load("data/sources.json")
journey = load("data/journey.json")
review = load("data/reviews/thursday-independent.json")
review_manifest = load("data/reviews/thursday-repaired-manifest.json")
publication = load("data/publications/thursday-reviewed.json")
release = load("dist/release.json")

educational_files = [
    "data/ontology.json",
    "data/comparisons.json",
    "data/comparison-drafts.json",
    "data/sources.json",
    "data/journey.json",
]
educational_hashes = {path: digest(path) for path in educational_files}

require(ontology["policy_snapshot"] == "2026-09-28", "policy snapshot remains 2026-09-28")
require(ontology["release"] == "wildcats-0.0.8-wednesday-comparisons", "ontology release is unchanged")
require(educational_hashes == review["educational_snapshot"], "educational snapshot matches Thursday's reviewed hashes")
require(educational_hashes == review_manifest["educational_snapshot"], "review manifest identifies the same educational snapshot")
require(ontology == load("dist/data.json"), "ontology and public export agree")
require(comparisons == load("dist/comparisons.json"), "comparisons and public export agree")
require(sources == load("dist/sources.json"), "sources and public export agree")
require(journey == load("dist/journey.json"), "journey and public export agree")

node_types = Counter(node["type"] for node in ontology["nodes"])
require((len(ontology["nodes"]), len(ontology["edges"]), node_types["Expectation"], len(ontology["findings"])) == (26, 31, 9, 0), "bounded graph counts are 26/31/9/0")
require(ontology["students"][0]["grade7_standard_ids"] == ontology["students"][1]["grade7_standard_ids"] and ontology["students"][0]["middle_school_band_standard_ids"] == ontology["students"][1]["middle_school_band_standard_ids"], "Matthew and Eva projections are identical")

relations = {edge["relation"] for edge in ontology["edges"]}
require(relations <= {"PART_OF", "ASSIGNED_TO_GRADE", "DERIVED_FROM", "USES_CONCEPT", "ASSIGNED_TO_GRADE_BAND"}, "no prerequisite, equivalence, or attainment relation entered the graph")
grade_relations = Counter(edge["relation"] for edge in ontology["edges"] if "GRADE" in edge["relation"])
require(grade_relations == Counter({"ASSIGNED_TO_GRADE": 6, "ASSIGNED_TO_GRADE_BAND": 2}), "six exact-grade and two band assignments remain distinct")

statuses = Counter(record["status"] for record in comparisons["records"])
require(statuses == Counter({"REJECTED": 2, "PROVISIONAL": 1}), "comparisons remain one provisional analogy and two rejected equivalences")
require(not ontology["hypotheses"] and not ontology["findings"], "no comparison was promoted to a hypothesis or finding")
require(len(ontology["unresolved"]) == 5, "five unresolved questions remain visible")

acquired = [source for source in sources["sources"] if source.get("archive_path")]
require((len(sources["sources"]), len(acquired), sum(source.get("page_count", 0) for source in acquired)) == (47, 42, 1237), "source manifest records 47 sources, 42 PDFs, and 1,237 pages")
require(all(source.get("effective_date") is None for source in sources["sources"]), "unknown effective dates remain null")
for source in acquired:
    path = source["archive_path"]
    require((ROOT / path).is_file() and digest(path) == source["sha256"], f"archived source hash matches: {path}")

require(review["result"] == "pass-with-recorded-limits" and not review["blocking_findings"], "Thursday separate review passed with no blocking findings")
require(digest("data/reviews/thursday-repaired-manifest.json") == review["repaired_manifest_sha256"], "Thursday repaired manifest hash matches")
require(publication["site_version"]["version_number"] == 17 and publication["deployment"]["status"] == "succeeded", "locked candidate is published Site version 17")
require(publication["research_commit"] == "a4945c8809047aea6dd9aad54a9152bbed962eda", "locked candidate research commit is exact")
require(release["publication_status"] == "published-unfrozen-candidate", "release status says published and unfrozen")
require(release["freeze_status"] == "blocked-rendered-qa", "release preserves the rendered-QA freeze block")

result = {
    "result": "candidate-integrity-pass-freeze-blocked",
    "checks_passed": len(checks),
    "educational_snapshot_sha256": educational_hashes,
    "coverage": {
        "nodes": len(ontology["nodes"]),
        "edges": len(ontology["edges"]),
        "parsed_expectations": node_types["Expectation"],
        "findings": len(ontology["findings"]),
        "source_records": len(sources["sources"]),
        "archived_pdfs": len(acquired),
        "archived_pages": sum(source.get("page_count", 0) for source in acquired),
    },
    "formal_foundation_prerequisites": "demonstrated for the locked bounded candidate",
    "blocking_gates": ["fresh rendered desktop/mobile QA under the required Sites preview workflow"],
    "freeze_authorized": False,
    "immutable_tag_authorized": False,
}
print(json.dumps(result, indent=2, sort_keys=True))
