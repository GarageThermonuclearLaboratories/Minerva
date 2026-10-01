# Thursday package 3 — separate AI re-review

**Verdict: pass-with-recorded-limits.** No blocking finding remains in the repaired candidate identified by `repaired-manifest.json`. This is a bounded code and semantic review, not a claim of complete natural-language safety.

The reviewed result is frozen Site base `88c050582145c1522711de2575da2acb2d0c8b37` plus four repaired files: `dist/ask-engine.js`, `dist/ask-ui.js`, `scripts/test_ask.js` and `scripts/test_interface.cjs`. The reviewer copied the candidate into its own archive and checked that every reviewed file still matched the product working tree when issuing the manifest. A later commit may identify this result, but the manifest hashes define the review boundary.

Reviewer `/root/thursday_reviewer` received a bounded brief without inheriting the builder conversation. This was independent AI code/semantic review, not human review or a blind-source audit. Root performed all product repairs. Reviewer activity was read-only against the product; executable probes and source archives were confined to reviewer scratch.

## Findings and repairs

The initial frozen checkpoint had six blocking finding groups, fully described with locations and reproductions in `initial-review.md`. The 57 original builder checks passed while 17 of the first 55 independent probes failed. Re-review deliberately expanded wording variants; an intermediate candidate passed the first 55 but still failed additional whole-question variations. Those failures were reported and repaired before this verdict.

| Finding | Final disposition | Verified repair |
|---|---|---|
| T1: grade/range selection | Resolved | Residual grade words and unsupported ranges abstain. Explicit grade plus band selections abstain instead of selecting one side. |
| T2: exact assignment vs band | Resolved | Exact/assigned/assignment wording with an explicit grade excludes band records. Avatar assignment without explicit placement abstains. All `only` queries abstain because modifier attachment is unsupported. |
| T3: disposition filters | Resolved | PROVISIONAL/REJECTED comparison selectors bind to the authored disposition. Unsupported expectation-status filters abstain. Comparison `or` selections abstain instead of becoming intersections. |
| T4: ignored standard or second operation | Resolved | Standard-specific comparisons abstain. Standard lookup refuses extra selections and conjunctions; tested mixed operations abstain. |
| T5: negation, completion and ability | Resolved | `no` and other exclusions abstain; completion and unsupported ability/mastery questions abstain. Method questions abstain. Explicit expected ability remains an expectation query with no-mastery limits. |
| T6: computer science / science | Resolved | Phrase masking preserves a separately requested Science subject. |

Ask comparison axes now name both subjects beside their corresponding prose. This addresses the initial nonblocking clarity note; the DOM suite still passes.

## Verification

Independently executed against the frozen repaired archive:

- **72 independent probes passed, zero failures, exit code 0.** The suite includes the original supported/refused examples, all reported blocker reproductions and subsequent variants, exact wording/annotations for all eight modeled standards, 21 subject/grade combinations for Matthew/Eva parity, and provenance/qualifier preservation across all nine expectations.
- **91 builder Ask checks passed.** DOM interactions, Receipt/projection checks, 25 comparison tests, 28 acceptance tests and 7 ingestion tests passed.
- Full validator and repaired JavaScript syntax checks passed. The one split PDF was reassembled from checked-in, hash-verified parts inside the review archive before validation.
- W1/W2 safeguards passed code inspection and executable mutation tests. The original Git baseline blob's file hash and declared semantic projection were independently checked against the contract. Method/scope/model/subject drift is rejected before invalid generator output replaces existing files.
- All five Wednesday-audited educational files retain their exact SHA-256 hashes. Public exports match. Counts remain 26 nodes, 31 edges, nine overlapping parsed expectations, one provisional analogy, two rejected equivalences outside the graph, zero promotions and zero findings. Mathematics/ELA exact Grade 7 placement and science grades 6–8 band placement are unchanged. All 42 archived PDFs retain their manifest hashes, totaling 1,237 pages; 47 source records remain.

Evidence files: `repaired-final-probe-results.json`, `independent-probes.cjs`, `repaired-manifest.json`. The manifest covers reviewed code, docs, tests, data, and archived-source hashes. Its SHA-256 is `626ead739963bb18ecf69805ef1d5b009497d85ee8e2ef3d3a5d65b6b3e9b433`.

## Recorded limits and subsequent edits

**Fresh rendered desktop/mobile QA was unavailable and remains open.** The required control-browser skill was unavailable; no alternate browser route was used. DOM execution establishes interaction behavior, not visual layout. No physical-device, native-zoom, complete accessibility, human semantic-review, exhaustive curriculum-coverage, or edition/cohort-applicability pass is claimed.

The engine is a bounded deterministic query layer. These checks establish behavior for reviewed patterns and representative variations; they do not prove every possible natural-language composition is interpreted correctly. Unsupported modifiers and combinations should continue to fail closed, and any broader language or data scope needs a new review. Baseline integrity is a reviewed local contract, not authentication against coordinated malicious edits.

The manifest includes the **pre-publication, pre-status-update** forms of Thursday documentation and UI status text. At this point those still correctly describe the earlier pending-review state. Root's later review-status documentation, release receipt, Lab Log or publication edits are outside this frozen verdict unless separately reviewed. They must distinguish this code verdict from the unchanged Wednesday data audit and from unavailable rendered QA. Publication itself does not extend the verdict or close the Friday freeze.
