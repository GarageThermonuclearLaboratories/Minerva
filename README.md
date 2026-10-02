# Wildcats / Minerva

An evidence-linked computational model of the canonical New York State K–12 educational pathway, with a humane exploration interface. Policy snapshot: **2026-09-28**. Current checkpoint: two bounded Grade 7 families (mathematics NY-7.RP.2 and ELA 7R1) plus two science performance expectations at the grades 6–8 band, 42 archived PDFs and 1,237 extracted pages. It does not claim statewide corpus completion.

## Method

State source → verbatim standard record → parsed expectation → ontology relationship → public receipt. The `SOURCE`, `PARSED`, `NORMALIZED`, `INFERRED`, `PROVISIONAL`, `CONTESTED`, and `REJECTED` labels describe claims, not people. A school expectation is never evidence of a particular student's mastery. Diploma requirements are tracked separately from learning standards.

The v0.1 construction is clean-room: no Garage-internal ontology class, hierarchy, primitive, mapping, or expected finding is used to derive Wildcats. Any post-freeze comparison requires a separate crosswalk.

## Current checkpoint

[The final Foundation v0.1 audit](docs/final-audit-v0.1.1.md) passed after one public-interface repair. The completion-record link now targets the post-freeze GitHub commit that actually contains the record. The frozen educational baseline and `wildcats-foundation-v0.1` tag are unchanged.

[Friday's foundation completion](docs/friday-completion.md) records the verified `wildcats-foundation-v0.1` annotated tag on exact audited commit `5d4dbef18880c2e1aad017f4a72037dfda52d140`. The bounded partial foundation is frozen with the separate audit's recorded limits. This is not completion of the canonical statewide K–12 ontology, policy applicability, human semantic review, full accessibility, or the post-freeze Garage crosswalk.

[Friday's separate release audit](docs/friday-release-audit.md) passed exact version 20 with recorded limits and no blockers before the tag was created. Its reviewed envelope, original candidate manifest and builder record remain untouched.

[Friday package 2's historical version 20 candidate](docs/friday-release-candidate.md) records the full builder validation and exact hash-bound manifest before the separate audit. `dist/release-manifest.json` preserves that candidate artifact manifest.

[Thursday closure](docs/thursday-closure.md) records Willis's combined desktop/mobile acceptance of public Site version 18 on October 2. Thursday is closed for its agreed bounded scope. This is user-reported human acceptance, not an agent browser pass, comprehensive accessibility certification or human semantic review. Later status changes are builder-checked, not retrospectively included in that acceptance.

[Friday freeze readiness](docs/friday-freeze-readiness.md) preserves the earlier blocked checkpoint and its exact reviewed hashes. Educational data remain unchanged.

[Thursday separate review](docs/thursday-independent-audit.md) passed the repaired bounded question layer and safeguards with recorded limits. Six defect groups are resolved; 72 independent probes and 91 Ask checks passed. [Thursday package 2](docs/thursday-ask.md) and [package 1](docs/thursday-foundation.md) preserve the historical builder-reviewed checkpoints.

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

Ask Minerva uses a deterministic, local query engine, not a remote language model. Run `node scripts/test_ask.js` for semantic-boundary checks. The DOM suite is `node scripts/test_interface.cjs` and requires jsdom in the invoking environment. It is not rendered-browser verification.

For Friday's complete candidate check, install pinned dependencies with `npm ci` and `python3 -m pip install -r requirements.txt`, restore split sources, then run `python3 scripts/validate_release_candidate.py --write`. Without `--write`, it verifies the existing candidate manifest and public export without regenerating evidence. This is builder validation, not independent release approval.

Run `python3 scripts/check_freeze_readiness.py` to rehash the locked educational snapshot and all archived PDFs, recheck claim boundaries, and report whether the remaining release gate authorizes a freeze.

The package 2 scripts above describe that historical candidate. The current audit closeout was tested on Python 3.12.14 and Node 24.19.0; broader runtime compatibility is unverified. Run `python3 scripts/verify_release_closeout.py` and `python3 scripts/test_release_closeout.py`. The verifier reconstructs exact version 20 from its research commit (in a GitHub clone) or Site source commit (in a Site checkout), restores split sources in isolation, preserves historical evidence, enforces all 17 recorded command identities/counts and verifies the separately reviewed closeout. Running the old candidate verifier against the growing current tree is expected to fail; do not overwrite the historical manifests to hide that difference.
