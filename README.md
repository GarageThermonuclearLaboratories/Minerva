# Wildcats / Minerva

An evidence-linked computational model of the canonical New York State K–12 educational pathway, with a humane exploration interface. Policy snapshot: **2026-09-28**. Current checkpoint: two bounded Grade 7 families (mathematics NY-7.RP.2 and ELA 7R1) plus two science performance expectations at the grades 6–8 band, 42 archived PDFs and 1,237 extracted pages. It does not claim statewide corpus completion.

## Method

State source → verbatim standard record → parsed expectation → ontology relationship → public receipt. The `SOURCE`, `PARSED`, `NORMALIZED`, `INFERRED`, `PROVISIONAL`, `CONTESTED`, and `REJECTED` labels describe claims, not people. A school expectation is never evidence of a particular student's mastery. Diploma requirements are tracked separately from learning standards.

The v0.1 construction is clean-room: no Garage-internal ontology class, hierarchy, primitive, mapping, or expected finding is used to derive Wildcats. Any post-freeze comparison requires a separate crosswalk.

## Current checkpoint

[Thursday package 1](docs/thursday-foundation.md) verifies the repaired safeguards and adds subject/disposition filters, claim-status guidance and unresolved-question disclosures. Ask Minerva and the separate Thursday review remain the next packages.

[Wednesday independent audit](docs/wednesday-independent-audit.md) passed the bounded science and comparison packages with recorded limits. The two validation follow-ups were subsequently repaired with builder regression review in [comparison safeguards](docs/comparison-safeguards.md); no graph edge or finding was promoted. [Wednesday comparison package](docs/wednesday-comparisons.md) records package 2. [Wednesday science package](docs/wednesday-science.md) records package 1. [Tuesday continuation](docs/tuesday-completion.md) and its subsequent audit and QA remain historical records. Historical documents below describe their named checkpoints.

## Contents

- [Monday output assessment](docs/monday-output-assessment.md): post-publication reassessment, negative-test findings, and readiness limits
- [Public interface revision](docs/site-revision-0.0.4.md): sixteen-part UX brief, bounded graph, Receipt behavior, and verification limits
- [Monday independent audit](docs/monday-audit.md): M7 pass, reviewed repair commit, verification, and remaining limitations
- [K–12 journey scaffold](docs/k12-journey.md): shared avatar pathway, five stages, grade coverage, and transition boundary
- [NY-7.RP.2 semantic trace](docs/semantic-trace-ny-7-rp-2.md): all four subparts, source annotations, grade-relation migration, and receipt checks
- [Ingestion workflow](docs/ingestion-workflow.md): repeatable PDF registration, extraction, rendering, and semantic review queues
- [Source inventory](docs/source-inventory.md): twelve-area document candidates, evidence states, date gaps, and acquisition queue
- [Foundation specification](docs/foundation-specification.md): scope, architecture, evidence rules, valid claims, and implementation gaps
- [Monday closure checklist](docs/monday-closure-checklist.md): frozen scope, completion gates, and Tuesday–Thursday deferrals
- `data/sources.json`: source manifest and policy applicability
- `data/ontology.json`: stable IDs, assertions, student-state projection, and unresolved questions
- `schema/ontology.schema.json`: machine-checkable shape for the first slice
- `scripts/validate.py`: checks references, provenance, and policy state
- `dist/`: static Minerva interface, built directly from the versioned slice
- `docs/`: decisions, coverage, and lab log

## Primary PDF checkpoint

Release 0.0.3 preserves both uploaded PDFs under `sources/originals`, hashes and acquisition provenance in `data/sources.json`, and page text under `sources/extracted`. Printed/PDF page 90 verifies NY-7.RP.2 and a–d. The crosswalk is draft-marked and supporting only. See `docs/primary-pdf-review.md`. Acquired/extracted does not mean semantically parsed.

## Rebuild / inspect

Run `python3 scripts/restore_sources.py` once after cloning to reassemble the largest PDF from hash-verified parts, then `python3 scripts/validate.py` from this directory. The static site reads `dist/data.json`, which is copied from `data/ontology.json`; run `cp data/ontology.json dist/data.json` after an ontology edit, then validate again. A future pipeline should generate exports and site data rather than relying on this explicit copy step.

For acquired PDFs, install `requirements.txt`, then run `python3 scripts/ingest_sources.py build` and `python3 scripts/ingest_sources.py check`. See the ingestion workflow for new-document registration and review boundaries.

GitHub is the canonical engineering record: [GarageThermonuclearLaboratories/Minerva](https://github.com/GarageThermonuclearLaboratories/Minerva). ChatGPT Site source commits and GitHub commits are separate Git histories; each deployment records both identifiers where available.

To rebuild the frozen comparisons, run `python3 scripts/build_comparisons.py --baseline data/comparison-baseline.json`, then `python3 scripts/test_comparisons.py` and the main validator. A changed educational graph requires a new explicitly verified baseline contract and review; do not relabel the old baseline.
