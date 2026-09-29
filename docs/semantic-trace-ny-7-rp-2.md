# Bounded semantic trace: NY-7.RP.2

Monday gate M5 · candidate `wildcats-0.0.4-monday-candidate` · policy snapshot 2026-09-28.

## Evidence and review scope

The authoritative text for this trace is the uploaded full standards PDF, physical/printed page 90, whose archived SHA-256 is `1bc23fd7e8793c22ba2d398be43411f570b043e4a4da930662c22b81cd5def95`. Its cover identifies an update in June 2019. Selected page visual inspection and text comparison support the transcription; exact applicability to the policy snapshot remains unresolved. The Grade 7 crosswalk corroborates wording but is marked Draft and is supporting evidence only.

This is agent semantic review of the bounded family. The subsequent [M7 independent agent audit](monday-audit.md) passed the trace after repairs; human review remains pending. Other standards on the page are not included in the trace. The M5 machine review record preserves its original review-time status; `data/reviews/monday-m7.json` records the later decision.

## Source → interpretation → receipt

| Source record | Parsed expectation | Meaning retained |
| --- | --- | --- |
| NY-7.RP.2 heading | `wc:expectation:recognize-proportional` and `wc:expectation:represent-proportional` | Two heading actions; their decomposition does not exhaust the subparts. |
| NY-7.RP.2a | `wc:expectation:decide-proportional` | Decide whether two quantities are in a proportional relationship. Source strategies are non-exhaustive. |
| NY-7.RP.2b | `wc:expectation:identify-unit-rate` | Identify the constant of proportionality/unit rate in tables, graphs, equations, diagrams, and verbal descriptions. All five representations remain explicit. |
| NY-7.RP.2c | `wc:expectation:represent-proportional-equation` | Represent the relationship using an equation. The cost example illustrates the action; it is not an additional required real-world context. |
| NY-7.RP.2d | `wc:expectation:explain-proportional-point` | Explain a point in terms of the situation, with special attention to (0, 0) and (1, r), where r is the unit rate. |

Every parsed expectation has a `DERIVED_FROM` edge to its exact source heading/subpart and a `USES_CONCEPT` edge to the proportional-relationship concept. Parsing rationale is stored with each expectation. These are parsed relationships, not inferred prerequisites or equivalences. Six expectation nodes do not mean six independent standards: two decompose the heading and four represent its subparts.

Original standard wording remains separate from action/object/qualifier fields. Clicking a parsed expectation in the prepared interface shows its own source subpart, rather than falling back to the parent heading. Clicking a source standard exposes its parsed expectations and associated notes.

## Source annotations preserved

- Subpart (a): the source permits strategies including equivalent-ratio testing in a table and/or checking whether a graph is a straight line through the origin. The list is explicitly non-exhaustive; both strategies are not mandated on every task.
- Subpart (c): the source example uses total cost t, count n, and constant price p to give t = pn. The example's variable names and shopping context are not universal requirements.
- Shared footer: NY-7.RP.2 and 3 present opportunities for modeling (MP.4). The source's apartment-building example is retained as a labeled summary. It describes a modeling assumption, not an empirical assertion that population is always proportional to story count. Footnote 14's citation target has not been reviewed.

The six source Coherence arrows remain observations in `data/source-review.json`. Their targets and semantic force are not reviewed enough to create prerequisite edges. No MP.4 graph edge or cross-disciplinary finding is asserted.

## Grade relation migration

Five existing edges change predicate from `EXPECTED_BY` to `ASSIGNED_TO_GRADE`, retaining their edge IDs and endpoints. The page directly establishes Grade 7 placement. It does not by itself establish an exact attainment deadline or resolve cohort applicability. This change narrows the claim to what the source placement supports.

Affected IDs: `wc:edge:002`, `wc:edge:grade-2a`, `wc:edge:grade-2b`, `wc:edge:grade-2c`, `wc:edge:grade-2d`. Consumers of the previous predicate must migrate to `ASSIGNED_TO_GRADE` for grade placement; no automatic deadline inference is permitted. Earlier releases remain in Git history.

The avatar view now says Grade 7 rather than asserting an end-of-grade attainment deadline. Matthew and Eva retain the same five source-standard IDs and EXPECTED state. No observed mastery is added.

## Validation and publication boundary

The graph now contains 15 nodes and 22 edges, including six parsed expectation nodes. The validator checks each subpart has a parsed expectation with a matching derivation edge, checks source annotation text against page 90, and rejects lingering `EXPECTED_BY` or prerequisite edges in this bounded release. Existing hash/reference/export checks pass.

`node scripts/test_receipts.js` exercises all six expectation receipts and seven view render functions using the actual data. It verifies exact source linkage and retained representation/strategy details. This is a programmatic rendering check, not a browser visual or accessibility audit.

M5 is complete as a prepared bounded trace and receipt implementation. The public Site remains at the earlier release until M8. Independent review is M7. The candidate receipt explicitly says publication is pending rather than claiming the previous public commit contains the new model.
