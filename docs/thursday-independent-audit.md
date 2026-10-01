# Thursday checkpoint: separate AI review and repairs

Decision: **PASS WITH RECORDED LIMITS** for the repaired, bounded question layer and comparison safeguards. Review date October 1, 2026. Separate reviewer `/root/thursday_reviewer`, GPT-6 Astra at High reasoning, received a bounded brief without the builder conversation. This is separate AI code/semantic review, not human approval or a blind-source audit.

The review and repairs are complete. Fresh rendered desktop/mobile QA remains open because the required control-browser capability is unavailable. The Sites managed-preview rule prohibits an alternate browser path. Plugin discovery found general external browser integrations, but none supplies that required skill and internal preview path. No visual pass, screenshot, physical-device or complete accessibility result is claimed. Full Thursday closure and Friday's freeze remain open.

## Exact review boundary

Frozen Site base `88c050582145c1522711de2575da2acb2d0c8b37`, plus repaired `dist/ask-engine.js`, `dist/ask-ui.js`, `scripts/test_ask.js` and `scripts/test_interface.cjs`. The reviewer copied the candidate into a separate archive and independently reran checks there. Exact hashes in `data/reviews/thursday-repaired-manifest.json` define the verdict, rather than a later mutable working tree. Manifest SHA-256: `626ead739963bb18ecf69805ef1d5b009497d85ee8e2ef3d3a5d65b6b3e9b433`.

Initial review, manifest and failing probes are preserved in `docs/review-assets/thursday-initial-review.md`, `data/reviews/thursday-initial-manifest.json` and `data/reviews/thursday-initial-probes.json`. Final reviewer report and passing evidence are `docs/review-assets/thursday-final-review.md`, `data/reviews/thursday-repaired-probes.json` and the repaired manifest. The machine decision is `data/reviews/thursday-independent.json`. Historical package-1/package-2 and Wednesday review records remain unchanged.

## Findings and final behavior

Six issue groups were found despite all 57 original builder query checks passing. Seventeen of the first 55 independent probes failed. Broader re-review found additional wording variants; those were repaired before the final verdict.

T1: incomplete grade parsing could choose one side of a spelled-out range. Unconsumed grade words, unsupported ranges and explicit grade-plus-band combinations now refuse.

T2: exact-assignment questions could return science band records. Explicit exact/assigned/assignment selection with one grade now excludes bands. An avatar name alone is not a source assignment. All “only” questions refuse because the engine does not infer modifier attachment; users can ask for an exact grade, subject or band directly.

T3: comparison dispositions could be ignored. PROVISIONAL/REJECTED filters now bind to the authored record. Unsupported expectation-status selectors and comparison alternatives joined with “or” refuse rather than changing the requested selection.

T4: a standard identifier or second operation could be ignored. Standard-specific comparisons, additional source selections and tested mixed operations now refuse. They do not silently broaden into subject-wide answers.

T5: allowed words such as “no,” “completed” and “able” could turn exclusion, mastery or method requests into expectation lists. Those unsupported intents now refuse. Explicit expected ability remains an expectation query with no-mastery limits; it does not become an assessment result.

T6: computer-science phrase detection removed separately requested Science. Masking the phrase now preserves a standalone Science selection. Ask comparison axis rows also label both subjects beside their own prose.

The repaired query method is `bounded-record-query-v2`. This remains a conservative deterministic query layer, not comprehensive natural-language understanding or generative chat. The verdict covers tested patterns and representative variations, not every possible sentence. Broader language or data scope requires renewed review.

## Verification and preserved evidence

Final independent execution passed 72 probes with zero failures, 91 builder Ask checks, the DOM interaction suite, Receipt/projection checks, 25 comparison tests, 28 acceptance tests, 7 ingestion tests, full validation and JavaScript syntax checks. The reviewer verified W1/W2 baseline/method/scope/subject safeguards and the original baseline Git object. Invalid generation preserves prior outputs. The baseline remains a reviewed local integrity contract, not authentication against coordinated malicious edits.

Independent probes cover all eight modeled standard identifiers, exact source wording and annotations, 21 subject/grade selections for Matthew/Eva parity, all five examples, all reported defects and later variants, and qualifier/provenance preservation for all nine expectations. Reproduce with `node scripts/test_thursday_independent.cjs .` from the repository; it prints evidence JSON and exits nonzero on failure. `node scripts/test_ask.js` is the builder query suite. DOM checks require jsdom and do not verify rendered layout.

All five Wednesday-audited educational hashes remain exact. The public exports match. The graph is unchanged: 26 nodes, 31 edges, nine overlapping parsed expectations, one provisional analogy and two rejected equivalence proposals outside the graph, zero promotions and zero findings. Science remains shared grades 6–8 context; math and ELA retain exact Grade 7 placement. All 42 PDFs retain their hashes, with 1,237 extracted pages and 47 source records. The 40 reattached PDFs already match the archive, so no duplicate intake or semantic expansion was performed.

## Status follow-up and publication

The builder's subsequent review-status text, release metadata, Lab Log, documentation and DOM assertions are outside the frozen independent verdict. Their own targeted query, DOM, syntax and whitespace checks passed; exact builder-status hashes are recorded separately in the machine record. Current notices distinguish Thursday's code verdict, Wednesday's unchanged data audit and unavailable rendered QA. Review never establishes new mastery, equivalence, prerequisites, source applicability or corpus completion.

Successful publication identifiers are recorded afterward in `data/publications/thursday-reviewed.json`. That later receipt is not part of the deployed source bundle and does not extend the independent verdict. Publication of the reviewed code does not close the pending visual check or Friday's freeze.

Reviewed code published successfully as public Site version 17 at 2026-10-01T22:38:16.812460+00:00 (October 1, 2026 at 6:38:16 PM America/New_York). Research `a4945c8809047aea6dd9aad54a9152bbed962eda`, Site source `85ab266efd82f9bf486480e6afdcfbc39aca475c`. Native deployment succeeded with no failure message. The staged research tree matched GitHub before the Site research-commit pin. The status follow-up's first DOM run caught package 2 displayed above package 3 in the Lab Log; insertion order was repaired and the rerun passed. The code-review and publication portions are complete; fresh rendered desktop/mobile checks still prevent full Thursday closure. This paragraph and receipt were added after deployment.
