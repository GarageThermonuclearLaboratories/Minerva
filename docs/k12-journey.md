# Canonical K–12 journey scaffold · Monday M6

The Follow the Wildcats view now has five navigable stages backed by [journey.json](../data/journey.json). Matthew and Eva reference the same pathway ID, `wc:pathway:canonical-nys-general-education`, and the same EXPECTED learning graph.

| Stage | Grade choices | Current coverage |
| --- | --- | --- |
| K–2 | Kindergarten, 1, 2 | Not yet mapped |
| 3–5 | 3, 4, 5 | Not yet mapped |
| 6–8 | 6, 7, 8 | One mathematics family at Grade 7; other grades and content remain unmapped |
| 9–12 | 9, 10, 11, 12 | Not yet mapped; no invented course sequence |
| Graduation / transition | Separate view, not a grade | Policy review pending; no diploma decision or destination prediction |

These stage bands are a project navigation convention. They are not asserted to be universal NYSED subject bands, district building configurations, or developmental stages. Subject-specific grade bands and World Languages proficiency checkpoints must retain their own source semantics.

## How projection works

For a selected grade, the interface finds source Standard nodes connected to that grade by `ASSIGNED_TO_GRADE`. It shows their parsed expectations with source receipts. This query is identical for both avatars and does not depend on race, gender, or a personal profile. Grade 7 currently displays one parent standard, four subparts, and six parsed expectations; those are different levels of representation, not eleven independent standards.

The stage buttons select a stage and its initial grade; the grade selector moves within that stage. The 6–8 stage initially selects Grade 7 so the existing trace is immediately inspectable. Switching avatars preserves the selected stage and grade. Kindergarten is named explicitly rather than displayed as Grade 0.

No grade slider movement implies promotion, cumulative mastery, retention of previous learning, or a historical cohort timeline. The entire scaffold uses the September 28, 2026 policy question, with exact edition applicability unresolved. It is a reference pathway, not a reconstruction of thirteen actual school years.

An empty stage explicitly means the project has not modeled its expectations. It cannot support a claim that NYS expects nothing at that grade. Graduation is treated separately because learning expectations, credits, assessments, credential eligibility, and destinations are distinct questions. Its official-source links are labeled research leads with full review pending; they do not yield a credential decision.

## Verification and limits

- Data validation checks the shared pathway ID and EXPECTED state, all thirteen grades exactly once, valid stage defaults, known transition source references, and identical source/public journey JSON.
- Rendering checks exercise all thirteen grades for both avatars and compare their exact displayed node references. Grade 7 has the same eleven inspectable source/expectation records for both; other grades have none.
- All five stage selections render, including transition without standard-node or diploma claims. Existing six receipt tests and repository validation pass.
- Native buttons with pressed-state labels and a labeled native grade selector support keyboard operation. No browser visual or accessibility audit is claimed; those controls have been checked programmatically.

The scaffold adds navigation data, not educational ontology nodes. The graph remains 15 nodes / 22 relationships. The public Site is still the earlier checkpoint; this implementation is prepared locally for M7 review and M8 publication.
