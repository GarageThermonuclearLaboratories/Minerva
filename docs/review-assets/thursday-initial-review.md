# Thursday package 3 — initial independent AI review

Verdict: **blockers** for frozen Site source `88c050582145c1522711de2575da2acb2d0c8b37`.

Reviewer `/root/thursday_reviewer` received a bounded review brief without the builder conversation. This is a separate AI code/semantic review, not human review or a blind-source audit. No product edits, Sites actions, browser automation, publication, or Git pushes were performed by this reviewer. Probe/report files and an immutable source archive are under the reviewer scratch directory.

## Blocking findings

| ID | Severity | Frozen location | Reproduction and observed behavior | Minimal repair |
|---|---|---|---|---|
| T1 | High | `dist/ask-engine.js:47–65, 102–108` | “What expectations are mapped in seventh or eighth grade?” chooses Grade 8; “What expectations are mapped in grade six through eight?” chooses Grade 6. Only adjacent grade tokens are consumed; residual spelled-out values remain allowlisted. | Recognize exactly one complete grade selection, or the explicit supported band; reject unconsumed grade words, ranges and conjunctions. |
| T2 | High | `dist/ask-engine.js:58–65, 102–108` | “What exact Grade 7 science expectations are mapped?” and “What science expectations are individually assigned to Grade 7?” return two shared-band records. “... assigned to Grade 7 only?” also returns them. The summary warns about band placement but the requested constraint was ignored. | Apply a true exact-assignment filter or refuse these qualifiers; never substitute band membership for an exact assignment. |
| T3 | High | `dist/ask-engine.js:58–65, 74–82` | “What rejected comparisons connect English and science?” returns a PROVISIONAL analogy. “What provisional comparisons connect math and science?” returns a REJECTED proposal. “Which provisional expectations are mapped?” returns nine PARSED expectations. | Bind supported comparison disposition selection; refuse unsupported expectation-status qualifiers. |
| T4 | High | `dist/ask-engine.js:56–61, 74–82` | “What connects 7R1 and science?” returns both ELA/science and unrelated mathematics/science records. “Compare NY-7.RP.2c and science” likewise ignores its standard selector. | Refuse standard-specific comparisons until implemented, or constrain both evidence sides to the requested identifiers. |
| T5 | High | `dist/ask-engine.js:29, 58–59` | “What expectations have no Grade 7 assignment?” returns all nine Grade-7-selected records; “What expectations has Matthew completed?” returns all nine expectations, with the same result for Eva. Allowed words `no` and `completed` bypass exclusion/mastery gates. | Refuse complete negation/completion intents before answering; test natural formulations, not only one blacklisted spelling. |
| T6 | Medium | `dist/ask-engine.js:41–43` | “What computer science and science expectations are mapped?” returns unmapped although Science has two band records. Global removal of Science discards a separate explicit selection. | Mask the computer-science phrase before detecting standalone science, or refuse mixed selections. |

The shared cause is that an allowlisted vocabulary is treated as a parsed question even when individual allowed words have unconsumed semantics. A bounded whole-question grammar is preferable to an ever-growing list of keyword exceptions. The frozen builder suite passes all 57 checks despite these findings.

## Independent evidence

`independent-probes.cjs` runs 55 probes; `frozen-probe-results.json` records 17 failing examples across the six finding groups. Other probes pass: all eight modeled standard identifiers return exact source wording/annotations; all five advertised examples remain available; 21 subject/grade combinations have identical Matthew/Eva answer items, summaries and limits; all nine returned expectations preserve their source quotation, page, source identity, qualifiers and annotations. Unsupported years/topics/prerequisites abstain.

Frozen-source suites: 57 Ask checks, DOM interaction suite, Receipt/projection suite, 25 comparison tests, 28 acceptance tests and 7 ingestion tests passed. The validator initially could not find the split source's reassembled PDF in the fresh Git archive. `restore_sources.py` recreated that PDF only inside the reviewer copy from checked-in hash-verified parts; the full validator then passed. This was an archive preparation issue, not a product defect.

W1/W2 review: baseline commit `6b64e00d3fe710ebb256770cdd475c9cfded88c1` was read from its Git object. Its original ontology byte hash and complete declared semantic projection match the baseline contract. Method/scope changes, model drift and misbound subjects fail; invalid generation preserves prior outputs. The baseline remains a reviewed local integrity contract, not authenticated against malicious coordinated edits. No new W1/W2 blocker found.

The five Wednesday-audited educational files match every recorded SHA-256 digest exactly. Public data exports match. The graph has 26 nodes, 31 edges, nine parsed expectations, zero comparison promotions and zero findings. Mathematics retains parent/subpart overlap; science has only its grades 6–8 band. One provisional analogy and two rejected equivalences remain outside the graph. All 42 archived PDFs match manifest hashes, total 1,237 pages; 47 source records remain. `frozen-manifest.json` records reviewed code/docs/tests/data and source archive hashes.

## UI and confidence limits

Static inspection and DOM execution cover Ask form/examples, source and parse Receipts, preserved annotations, focus/escape, navigation persistence, comparison handoff, filters, both data/script arrival orders and HTML escaping. No new blocking UI-code defect found. Optional clarity improvement: Ask comparison axis rows show left/right prose without subject labels; the full Crossroads card has labels. Labeling both sides would make reversed-order questions easier to interpret.

**No fresh rendered desktop/mobile, physical-device, native-zoom or full-accessibility pass is claimed.** The required control-browser skill is unavailable; no alternative path was used. Source applicability, human semantic approval and comprehensive curriculum coverage remain outside this review. A later re-review must bind repaired files to a new hash manifest. This verdict does not cover subsequent audit-status UI edits or publication status.
