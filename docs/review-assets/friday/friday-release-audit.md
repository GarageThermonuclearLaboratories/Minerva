# Friday package 3 · separate release audit

**Verdict: pass-with-recorded-limits for the exact published version 20 candidate.** No blocking defect was found. This partial foundation baseline is defensible for a narrowly scoped v0.1 freeze decision. It is not a completed canonical NYS K–12 ontology. The required immutable tag has not been created, so a completed tagged freeze must not be claimed.

## Identity and independence

Reviewer: `/root/thursday_reviewer`, reused for Friday with its prior Thursday review context. Friday review began from a bounded brief and the exact current artifacts, without the Friday builder conversation. This is separate AI code, release-integrity and semantic-boundary review, not human or blind-source review. Session instructions identify the model family as GPT-6; the exact model variant and reasoning-effort setting are not exposed and are not asserted.

The product checkout was read-only. No source edits, publication, Git pushes, Garage ontology access, source imports or sub-agents were used. The reviewer used an isolated archive for installs, mutation probes and replay. Native Site and GitHub calls were read-only provenance checks. No browser QA was performed.

## Exact candidate

| Binding | Reviewed value |
|---|---|
| Published Site version | 20 |
| Published Site source | `a79f62871a225a8c1ff12507c9c009d5bcecc5a8` |
| Postpublication checkout inspected | `6fad7d334cddc6e84bb139cb9733dced171f0de5` |
| GitHub research commit | `049d7c657f0e0535b8403c6fcac65183ef9442f9` |
| GitHub research tree | `10882bc9cdf570a77d51137a4378aa67d0d7fc6d` |
| Candidate manifest SHA-256 | `e0aebcd457dd384f5d742d48d28869a427457666a6825e203d1d4ce509c22851` |
| Builder record SHA-256 | `861a5d3fae2f257585c3a6fd7e74851dee53232ffd269d47639aa9dea20f1d30` |
| Native archive digest, independently read from Sites | `728510a271959f05884b3570441ed359bc40b00f0070dcd43ada99795d4040ca` |
| Native deployment | `appgdep_6abfaf36381881919888fdbe106fba56`, succeeded |

The fresh GitHub commit/tree read matches every tracked Site candidate blob except the declared `dist/release.json` research pointer: null in the research commit to avoid self-reference, and the exact research commit in the Site source. Release semantics otherwise agree. The postpublication checkout adds only the receipt and two Lab Log lines to the published source.

A fresh native read confirms the saved version, source commit, archive metadata and successful deployment. The submitted local gzip contains 28 delivery files byte-identical to the Site source plus one packaging hosting file with matching configuration semantics. Its decompressed tar bytes/hash differ from the native archive metadata. Service repacking is a plausible explanation, not established evidence. Native stored bytes could not be downloaded; this review **does not claim raw local/native archive byte equivalence**. The native content hash is a verified service-reported value, while delivery-member equality was independently tested locally.

`audit-fingerprints.json` records specific code/document/dependency hashes, the preserved educational snapshot and receipt hash. `github-candidate-tree.json` and `native-readback.json` preserve read-only provenance evidence.

## Findings

**Blocking findings: none.**

**F3-1 — low, verifier robustness follow-up.** `scripts/validate_release_candidate.py:verify` requires a nonempty all-zero command list, not the exact required command inventory or counts. An isolated probe replaced the record with one anonymous successful check and reissued both manifests through `make_manifest`; `verify` accepted that coordinated new evidence. This is not a failure of the observed immutable candidate: its externally identified manifest/record hashes match, its record contains all 17 expected commands, and the reviewer independently replayed all 17 successfully. `run_checks` itself executes a fixed command list. The finding limits generic verifier guarantees; it does not invalidate the actual evidence reviewed here. The closeout verifier should require the exact ordered command inventory and counts as well as the frozen record hash, without editing the historical v20 artifacts.

The verifier deliberately excludes the research pointer and publication receipts. Independent probes confirm these can change without invalidating its artifact check. That is a declared boundary, not hidden coverage: publication bindings must be verified separately, as they were in this review. Future status/envelope validation must retain that explicit distinction.

## Verification performed

- **14 independent manifest probes passed their stated expectations.** Added/missing delivery assets, mutated archived source bytes, dependency pins, ontology bytes, release semantics, omitted manifest entries, altered public exports and missing/failed/changed evidence were rejected. The three declared or observed trust-boundary cases were recorded explicitly rather than falsely presented as rejection guarantees.
- **20 new independent runtime/claim probes passed.** These cover future-year/cohort and legal/mastery abstention, prohibited avatar differences, exclusion requests, exact-grade science versus band context at grades 6/7/8, explicit band assignment, reversed comparison order and rejection status, full MS-PS2-4 source annotations, damaged locators/pages, avatar parity and non-mutation.
- **All 17 recorded validation commands replayed successfully** in the isolated candidate, including 79 readiness assertions, main and ingestion checks, 25 comparison tests, 28 acceptance tests, seven ingestion tests, five original manifest tests, 91 Ask checks, the archived 72-probe Thursday harness, Receipt/projection checks, nine-view DOM checks, five JavaScript syntax checks and ordinary `git diff --check`. Replaying Thursday's harness here is identified as replay, separate from the 34 new Friday probes and this audit judgment.
- `npm ci --offline` installed 61 packages from the available cache using the exact lockfile. jsdom is 27.4.0, Node is 24.19.0, Python is 3.12.14, and the available pinned PyMuPDF is 1.26.6. A clean separate Python environment or fresh remote package download was not claimed. Vite remained pinned at 8.3.1; the new dependency change adds jsdom for reproducible DOM checks.
- The split source was restored inside the review archive from its checked-in parts; all 315 manifest artifacts verified. An extra check that treated the entire historical repository as newly staged flagged existing Markdown hard-break spaces and whitespace preserved inside an old reviewed patch. This was outside the candidate's recorded differential whitespace check and is not a new functional defect; historical evidence was not edited.

## Educational and status boundaries

All five Wednesday/Thursday educational snapshot hashes remain exact. The source/export agreement and archived source checks pass. Counts remain 26 nodes, 31 edges, nine parsed expectations, 47 source records, 42 PDFs and 1,237 extracted pages. The mathematics parent/subpart interpretations overlap; nine expectations are not nine independent or exhaustive requirements.

Semantic coverage remains Grade 7 NY-7.RP.2 and 7R1 plus MS-PS2-2/MS-PS2-4 in the grades 6–8 band. Science is not assigned to each constituent grade. Thirteen navigable grades and twelve inventory areas do not establish statewide semantic completeness. The one provisional analogy and two rejected equivalence proposals remain outside graph edges, hypotheses and findings. Findings/hypotheses are empty; five unresolved questions remain visible.

Matthew and Eva remain fictional identical canonical projections, without mastery data or demographic tailoring. The policy query remains September 28, 2026. Unknown effective dates, edition/cohort applicability, archived-upload provenance and unverified current official-URL byte equivalence remain explicit. No new prerequisite, equivalence, policy-currentness or assessment conclusion is licensed by this audit.

The clean-room boundary is documented and consistent with inspected artifacts. No Garage ontology was consulted during this audit. Neither hashes nor this bounded inspection prove absence of every possible conceptual influence.

User-reported desktop/mobile acceptance is attributed specifically to version 18, with no invented per-check outcomes or screenshots. The seven recorded functional asset hashes match that candidate. `interface.js` changes between v18 and v20 are status/Log copy, independently inspected here; they are not retroactively included in the user's test. The more recent status documents correctly distinguish builder validation, archived-probe replay, prior independent review and the then-pending Friday audit. No fresh rendered, native-zoom, full-accessibility or human semantic pass is claimed.

## Freeze recommendation and closeout

Approve this exact, commit-identifiable **partial foundation candidate** for the bounded freeze decision with these limits. It provides a reproducible source-to-record-to-Receipt foundation, not a complete K–12 model or generalized natural-language/inference system. Human semantic review, applicability resolution, broader coverage, descriptive-schema enforcement gaps and comprehensive accessibility remain open.

A completed tagged v0.1 freeze still requires the immutable tag operation. An unavailable tag tool does not make the tag exist or waive the specification. Root may publish a truthful status of audited/approved candidate with tag completion pending, but must not call the tagged freeze complete or begin post-tag Garage crosswalk work prematurely.

Preserve the v20 candidate manifest and builder record byte-for-byte. For later status, audit and envelope files, use a separate closeout envelope that binds the historical candidate manifest/record, exact candidate Git/native receipt and explicit changed-file hashes. Verify the historical candidate from its Git reference in isolation; do not compare a growing current tree to the old inventory and then overwrite the old evidence to make it pass. The audit attestation should hash the already-frozen envelope and be excluded from that envelope's own input set. Root's later status/verifier/envelope changes require scoped re-review; this verdict does not automatically approve them.
