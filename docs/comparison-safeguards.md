# Comparison safeguards · September 30, 2026

Checkpoint: `comparison-safeguards-2026-09-30`; interface revision `0.0.8-safeguards`. Ontology release remains `wildcats-0.0.8-wednesday-comparisons`.

This is the next bounded preparation package for Thursday's Ask Minerva work. It closes W1 and W2 from Wednesday's independent audit before comparison generation is reused. It does not close Thursday, add an answer engine, or claim a new independent review.

## Repairs and evidence

W1: `data/comparison-baseline.json` binds the input research commit, an explicit semantic projection of the educational model, method and scope. The builder fetched the original [science baseline](https://github.com/GarageThermonuclearLaboratories/Minerva/blob/6b64e00d3fe710ebb256770cdd475c9cfded88c1/data/ontology.json) on September 30 and verified the current policy snapshot, every node, edge, student, hypothesis and finding against it. The lock records both the original file hash and the projection fingerprint. Release labels and scope prose differ between releases and are not included in that projection. The original commit identity is no longer hardcoded by the generator.

Generation now requires `--baseline`, validates the current model against that contract and validates the complete candidate before either output is written. An unrelated model change therefore cannot quietly acquire new fingerprints under the old baseline identity. Validation rejects false input commits, method/scope mismatches, and coordinated draft/export method or scope changes against the contract. A future baseline must be independently retrieved and explicitly reviewed; editing the lock is not itself evidence of validity. This is a bounded local integrity contract, not cryptographic authentication or an automatic semantic reviewer.

W2: each ordered subject label is bound through its paired expectation and parent standard to a known source ID and the matching Subject node. The three bindings are deliberately limited to the existing mathematics, ELA and science records; new subjects require explicit review. A changed draft subject label fails generation before any output is replaced. Reversed subjects and mislabeled pairs also fail.

## Provenance and scope audit

The main validator rechecked quotations against the archived NYSED documents and pages: mathematics page 90, ELA page 82 and science pages 33–34. Existing page-based provenance and file digests remain intact. No new source acquisition or policy-currentness claim was made. The original uploaded-document acquisition caveats remain.

The unchanged science band remains grades 6–8. September 28, 2026 remains the policy query snapshot, not an assertion of verified applicability. The analogy remains provisional; both equivalence proposals remain rejected. No inferred relation or comparison enters student expectations. Counts remain 26 nodes, 31 edges, 9 parsed expectations and zero findings; 42 archived PDFs and 1,237 extracted pages are not semantic coverage. The exact five-file Wednesday independent audit hashes still match. No Garage-internal ontology was imported.

## Verification and failures

Builder regression review passed 25 comparison tests (13 new), 28 acceptance tests, 7 ingestion tests, the main validator, Receipt/student-projection checks, interface DOM checks, JavaScript syntax and whitespace checks. A valid rebuild reproduces both comparison files byte-for-byte. Invalid-baseline and coordinated-subject-error generation tests verify that existing outputs remain untouched.

Initial DOM checks failed its historical Lab Log count (expected eight, now nine after adding this entry). After correcting the test edit to target the existing time-element selector, the count and new-entry content assertion were updated, and the suite was rerun. This was an outdated test expectation, not a hidden application failure. No new rendered browser, physical-device or accessibility audit is claimed; the UI change is a status and Lab Log text update using existing components.

Reproduce from the repository root:

1. `python3 scripts/restore_sources.py`
2. `python3 scripts/build_comparisons.py --baseline data/comparison-baseline.json`
3. `python3 scripts/validate.py`
4. `python3 scripts/test_comparisons.py`
5. `python3 scripts/test_acceptance.py`
6. `python3 scripts/test_ingestion.py`
7. `node scripts/test_receipts.js`
8. With jsdom available: `node scripts/test_interface.cjs`

## Next steps and publication

Next is a bounded Ask Minerva layer: answers from modeled records, source Receipts, visible claim status and explicit abstention for unmodeled coverage, mastery, unresolved applicability and unsupported equivalence. Thursday's wider journeys/review and Friday's reproducible v0.1 freeze remain open. Human review, exact policy applicability, complete corpus coverage and full accessibility remain unresolved.

The dedicated GitHub repository is available. GitHub research and Site source histories remain separate. Actual saved version, deployment ID, source SHA and outcome are recorded in `data/publications/comparison-safeguards.json` and the Lab Log after deployment; that post-publication receipt is not represented as content of the already deployed bundle.
