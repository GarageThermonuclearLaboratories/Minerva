# Thursday package 2: Ask Minerva

Prepared October 1, 2026. Checkpoint `thursday-package-2`, interface `0.0.8-thursday-ask`. Educational release remains `wildcats-0.0.8-wednesday-comparisons`.

## Outcome and scope

Ask Minerva is a new view in the existing atlas. Type a question or choose one of five examples. The first implementation is a deterministic browser-side record-query engine (`bounded-record-query-v1`), not generative chat. It needs no external model or API key, sends no questions to a service and retains the question and answer only in page memory. Reloading clears them. Navigation preserves them within that page.

Supported operations are mapped-expectation selection by subject, one grade or the shared middle-school band; the fictional reference students' shared Grade 7 view; exact standard-identifier lookup; current map coverage; and the existing comparison register by subject selection. Identifiers include NY-7.RP.2 and its a–d subparts, 7R1, MS-PS2-2 and MS-PS2-4. The five examples exercise learner expectations, science band context, ELA/science comparison, source wording and an unmapped grade.

Each expectation answer retains its parsed action, object and qualifiers, source quotation and annotations, exact-grade or band placement, SOURCE/PARSED status and source/parse Receipt controls. Source annotations include clarification, assessment boundaries and mathematics notes. Comparison answers retain PROVISIONAL/REJECTED status, the authored decision, differences and next evidence, with source Receipts and a link to the expanded Crossroads card. No comparison becomes an accepted equivalence or graph relationship.

## Refusal and evidence gates

Only eligible SOURCE/PARSED claims with registered-source/page/locator provenance enter expectation answers. The source derivation, eligible assignment and parent-standard chain must remain available. Comparison evidence must still match eligible modeled expectations and their source wording, source identity, page, locator and manifest hash. Runtime gates complement repository validation; they are not a new semantic audit or a general-purpose hostile-data validator.

The parser conservatively recognizes a bounded vocabulary and selection patterns. Unknown words, narrower topic filters, ambiguous grade ranges or exclusions are refused rather than silently broadened. It is not a comprehensive natural-language parser: equivalent questions outside those patterns can be declined. The examples are the dependable starting point. Source identifiers provide the most specific retrieval path.

Mastery, current legal/graduation applicability, prerequisites/progression/transfer, lessons/exercise solving and invented claims are not answered. An unmapped selection explicitly means no eligible records have been modeled here, not that New York has no requirements. Both avatars receive identical canonical expectations. Science records remain shared grades 6–8 context, never extra Grade 7 assignments. Counts preserve the mathematics parent/subpart overlap rather than asserting nine independent requirements.

Answers distinguish current educational data from Wednesday's exact frozen audit. The new answer layer has builder verification only and awaits Thursday's separate package 3 review. Human review, exact edition/cohort applicability, complete coverage and full accessibility remain open.

## Verification and limits

Passed: 57 query-engine checks; expanded nine-view DOM interaction suite; main validator; 25 comparison tests; 28 acceptance tests; 7 ingestion tests; Receipt/projection suite; JavaScript syntax and whitespace checks. Query tests cover all examples, matching avatar results, band placement at grades 6/7/8, coverage gaps, exact quotations and annotations, comparison dispositions, abstention, rejected claims and parent chains, broken derivation/placement/source links, stale evidence, dynamic counts, Receipt identities and non-mutation.

The DOM suite verifies form submission, examples, retained question/answer on navigation, source/parsed Receipts, Escape and focus restoration, comparison handoff, source-only answers, abstention, hostile input escaping, all existing controls and both script/data arrival orders. Its first run failed because the new test expected eleven quotations while the answer correctly retained seventeen, including all source annotations. The assertion was changed to derive the expected count from the model; the rerun passed.

Fresh rendered-browser QA was unavailable: the required control-browser skill is not available in this runtime, and the Sites managed-preview instructions prohibit substituting another browser path. No new desktop/mobile screenshot, visual-layout pass or full accessibility result is claimed. CSS follows the existing responsive system, but this is not proof of rendered layout. Thursday's separate review remains package 3 and should include that follow-up when preview access is available.

All five audited educational files and public exports remain unchanged. The graph still has 26 nodes, 31 edges, 9 parsed expectations, zero promoted comparisons and zero findings. This package adds no policy date, new source, ontology claim or Garage-internal hierarchy.

## Publication

Actual publication identifiers and outcome are recorded after successful deployment in `data/publications/thursday-ask.json`. Such a post-publication record is not part of the deployed source bundle. Package 2 does not close Thursday or the Friday freeze.

Package 2 was published successfully as public Site version 16 at 2026-10-01T18:42:00.912827+00:00 (October 1, 2026 at 2:42:00 PM America/New_York). Research commit `c723e5cce5c1784be06bb4e9189b58d306e44c2e`; research tree `02a08f61998615bee0d77f55fec833ceea6e0625`; Site source `99ba774f9342177378b149e44f4a3e12df96bc52`. The local staged research tree matched GitHub exactly before pinning that research commit in the Site release receipt. The native deployment succeeded without a failure message. Fresh rendered QA and Thursday's separate package 3 review remain open; publication supplies no additional review verdict.
