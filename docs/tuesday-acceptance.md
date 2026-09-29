# Tuesday acceptance checkpoint · v0.0.5

September 29, 2026. Package 1 of Tuesday's agenda; builder review, not independent audit or daily closure.

## Baseline and evidence

Site source `5ab4d743be7bb04d54d9f8ab880f2ba6622cd3f5` and dedicated GitHub `main` at `9c500877335e1fb3b8b5233bb4756b7a77849c6b` contained matching research files. The public baseline was Site version 8. The unchanged primary evidence is the archived NYSED full mathematics standards, PDF/printed page 90, SHA-256 `1bc23fd7e8793c22ba2d398be43411f570b043e4a4da930662c22b81cd5def95`.

The page image was visually reinspected in this run. The regression contract retains all five representations in 2b, contextual graph meaning and both distinguished points with the meaning of r in 2d, non-exhaustive strategies in 2a, the illustrative equation in 2c, and the shared modeling note. No current-policy claim was researched or added. September 28 remains the policy snapshot; edition/cohort applicability and provisional timeline observations remain unresolved.

## Repairs

- `scripts/acceptance.py`, called by the main validator, rejects unknown node types, unsupported predicates or endpoint-type pairs, missing source locators/review metadata, invalid PDF pages, unacquired evidence, invalid derivations, missing rationale, contradictory derivation edges, cyclic standard parents, and stale avatar exports.
- Allowed relationships are deliberately bounded to PART_OF, ASSIGNED_TO_GRADE, DERIVED_FROM, and USES_CONCEPT with explicit endpoint types. Adding another relation requires an intentional contract change and evidence review. Similarity is not equivalence; neither prerequisite nor attainment-deadline claims were introduced.
- Expected-learning projection admits SOURCE/PARSED records only, requiring eligible grade assignments, parent links, parents, and expectation derivation links. REJECTED, CONTESTED, PROVISIONAL, NORMALIZED, and INFERRED records remain inspectable but are not silently promoted into the expected set. This is an edition-based projection, not proof of applicability or mastery. Rejected records may remain in the ontology when their exported expected sets are updated.
- A reviewed, family-specific acceptance fixture protects structured action/object/qualifier fields and annotation wording/interpretation. Receipt tests inspect the parsed field block separately from the original quotation. The fixture was initialized from the existing trace, then reviewed against the source page; it is a regression contract, not an independent semantic oracle.
- Added explicit action/object/qualifier fields to the two existing heading expectations and a parsing rationale to the existing Concept. IDs and graph topology are unchanged.

## Validation and actual failures

Passed: 19 acceptance tests; seven ingestion tests; main validator including hashes and public-copy equality; six Receipt traces and independent parsed-field checks; projection mutation checks; eight DOM views and fifteen Receipts; thirteen grades for both avatars; JavaScript syntax and Git whitespace checks.

Initial DOM regression failed because its old release-label assertion expected v0.0.4. The label and assertion were updated to Tuesday v0.0.5 and the suite passed. The old temporary jsdom location was absent; the retained project QA installation was used successfully. No dependency change was needed. No live source mutation was used for negative tests.

## Limits and next work

Coverage remains one Grade 7 standard family, six parsed expectations, 15 nodes, 22 relationships, zero ontology findings. The repository intake still contains two mathematics PDFs. The separate conversation reports a verified 22-file upload batch; those files are not yet registered in this checkpoint, and this package makes no new acquisition claim. Do not ask the user to download that batch again.

The JSON Schema remains skeletal and is not executed; explicit Python acceptance checks are the enforcement boundary. General semantic completeness, arbitrary inference validation, applicability resolution, and automatic clean-room detection are not implemented. Source quotes and hashes do not prove an interpretation correct. Clean-room review found no Garage-internal classes or mappings introduced.

Current-versus-historical review status reconciliation remains open. The M7 audit is preserved as a Monday baseline audit; it does not approve Tuesday's code or metadata changes. Loading-navigation, concept-to-student highlighting, Receipt overlap, mobile/zoom/accessibility QA, and renderer consolidation remain pending from Monday's assessment. No rendered browser audit is claimed.

Next coherent package: reconcile current review/publication records without rewriting history; then repair the remaining interface defects, register the uploaded source batch, capture durable policy evidence, and expand one bounded family after review. Tuesday as a whole remains open.

Publication outcome and exact Git/Site identifiers are appended to the Lab Log and `data/publications/tuesday-0.0.5.json` after deployment succeeds.
