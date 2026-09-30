# Wednesday package 2: bounded cross-subject comparisons

Release: wildcats-0.0.8-wednesday-comparisons. Policy snapshot: 2026-09-28. Builder review dated 2026-09-30; separate Wednesday AI audit remains package 3.

## Scope and result

Three purposively selected comparisons, one per subject pair, use the package-1 research baseline `6b64e00d3fe710ebb256770cdd475c9cfded88c1`. This is not an exhaustive crosswalk or a learned capability hierarchy.

ELA 7R1 and science MS-PS2-4 retain a provisional evidence-support analogy. Textual interpretation and empirical gravitational argument differ in object, evidence and required product. Neither interchangeability nor transfer is established.

NY-7.RP.2c and MS-PS2-2 do not justify the proposed equivalence between representing a proportional relationship with an equation and planning/conducting a force-and-motion investigation. The rejection does not rule out mathematical applications in science.

NY-7.RP.2d and 7R1 do not justify equivalence between explaining a graph point and interpreting text with textual evidence. A broad meaning-in-context analogy remains possible, but does not establish a common educational requirement.

Each record compares action, object, evidence, required product, placement and boundary. Exact paired quotations, source-page locators, source hashes and fingerprints of both parent standards and parsed expectations are preserved. Mathematics uses PDF page 90, ELA page 82, science page 33. The science connection box on page 34 names 6-8.WHST.1 for MS-PS2-4, and MP.2, NY-6.EE.2, NY-7.EE.3 and NY-7.EE.4 for MS-PS2-2; it does not name the proposed ELA or proportional-equation counterparts. Absence is not proof that no relationship is possible.

## Data and interface

`data/comparison-drafts.json` is the authored analysis; `scripts/build_comparisons.py` binds it to source/model snapshots in `data/comparisons.json` and `dist/comparisons.json`. These are analysis records, not ontology edges, accepted findings or student requirements. Status remains one PROVISIONAL and two REJECTED records, all builder-reviewed and awaiting independent review.

Crossroads now presents the three expandable comparisons, source and parsed Receipts, differences, dispositions and limitations. Findings links to the comparison register while retaining zero accepted findings. The educational graph remains 26 nodes, 31 edges and 9 parsed expectations; student projections remain unchanged. Stale top-level scope metadata was corrected to include package 1's science slice.

## Verification and limits

The main validator, 12 comparison tests, 28 acceptance tests, Receipt checks and interface DOM tests passed. Negative cases cover altered quotations/hashes, stale fingerprints, lost boundaries, promoted review status, missing axes, wrong pairs, unsupported dispositions, missing rationale and graph leakage. These checks enforce integrity; they do not prove the analysis's semantic correctness.

Cloud Chromium rendered the comparison view at a 1348-pixel content width and in a 320-pixel responsive iframe (305-pixel content width with scrollbar). Both showed no horizontal overflow. Expanded content and narrow-screen wrapping were visually inspected. DOM tests exercised all three comparisons' Receipt opening, Escape focus restoration and Findings navigation. This is targeted QA, not a physical-device, native-zoom or full accessibility certification. Screenshot: `docs/review-assets/wednesday-comparisons-desktop.jpg`.

Source applicability remains unresolved. Grades 6–8 science is not assigned specifically to Grade 7. No mastery, developmental sequence, transfer, shared mechanism or Garage ontology import is asserted. Package 3 must independently audit both Wednesday packages before Wednesday is closed.

Published successfully as public Site version 12. Research commit: `6c93368df56db11958f4e3f77b20cf02db0e8600`. Site source: `765711539d5007f22b717d2fa1c46238e8036c59`. Exact native result: `data/publications/wednesday-0.0.8.json`. This paragraph and receipt were recorded after publication and are not in the deployed commit. Independent Wednesday audit remains pending.
