# Wednesday package 1: first science slice

September 30, 2026 · release wildcats-0.0.7-wednesday-science · builder review.

## Scope and result

Added two selected performance expectations from MS. Forces and Interactions: MS-PS2-2 (planning and conducting an investigation of forces, mass and changes in motion) and MS-PS2-4 (constructing and presenting evidence-based arguments about gravitational interactions). Each retains its verbatim source wording, one compound parsed expectation, full clarification statement, full assessment boundary, original PDF and rendered source-page Receipt.

This is two of five performance expectations on page 33, not completion of the Forces and Interactions topic or a complete three-dimensional science model. Science and engineering practices, disciplinary core ideas, crosscutting concepts and other source connections remain inspectable on the full page but have not been separately decomposed into ontology claims. No prerequisite, cross-disciplinary equivalence or finding was added.

The graph now contains 26 nodes, 31 relationships and 9 parsed expectations. The acquired corpus remains 42 PDFs and 1,237 pages. No further uploads were needed.

## Source and interpretation

Primary evidence: `src:nysed:science-full`, uploaded New York State P-12 Science Learning Standards, PDF/printed page 33. Original SHA-256: `673499b3a712830b56117d4cfd69cf53bc23bd7f37a123f1a030924f07527670`. Page 33 was visually inspected and compared with its extracted text. Page 34 was visually inspected to preserve the adjacent connections context; its September 2018 update note applies to connection boxes, not a proven whole-document publication or effective date.

The source's MS heading, repeated grades 6–8 practice descriptions and grade-band context support middle-school band placement. A `GradeBand` node and `ASSIGNED_TO_GRADE_BAND` relation preserve this scope. These standards are never exported into the Grade 7 standard list. They appear separately as shared band context while viewing grades 6, 7 or 8. Displaying them there does not assign them to all three grades or establish a deadline. Both fictional students use the same projection.

The existing `Standard` class holds the source's performance expectations; `Expectation` denotes our parsed representation. The heading “Students who demonstrate understanding can” describes the source's performance expectations, not evidence that either avatar has demonstrated them. Coordinated actions remain compound: planning plus conducting an investigation, and constructing plus presenting an argument.

The clarification for MS-PS2-2 retains balanced/unbalanced forces, simple machines, qualitative comparisons, frame of reference and units. Its assessment boundary preserves one-dimensional motion, an inertial reference frame, one variable at a time and the exclusion of trigonometry. MS-PS2-4 retains attraction, masses and distance; its evidence examples remain examples, and Newton's Law of Gravitation and Kepler's Laws remain excluded from the assessment boundary.

## Implementation and verification

Atlas and Curriculum expose the science standards and parsed expectations. Receipts link the correct source page and archived bytes. The science Receipt's student action focuses the corresponding object in shared band context. Journey distinguishes exact-grade anchors from science band context. Workbench and the Lab Log disclose bounded science coverage and builder-only review.

Corrected the Tuesday review's conditional coverage-text defect: the individual-grade summary now lists eligible source families from the rendered projection. Rejecting math leaves an ELA-only summary, without continuing to claim both subjects.

Completed checks:

- Main validator: all source hashes, 42 extraction bundles, data/export agreement, exact quotations and annotations against their own pages, source image hashes, provenance, relationship endpoints and equal student projections.
- 28 acceptance tests, including false exact-grade science placement, lost band membership, deleted assessment boundary, lost qualifier and rejected band assignment.
- 7 ingestion regression tests.
- Receipt/projection tests: all nine parsed expectations; grade and band eligibility, all 13 grades for both students, five stages and graduation abstention; rejected math summary regression.
- DOM tests: eight views, all 26 Receipts, science-specific evidence URL and student focus, graph expansion, band context, matrix controls and load ordering.
- Rendered cloud Chromium: desktop science Receipt and band-context navigation at 1363 × 936; a 320 × 740 iframe mobile viewport with no page-wide overflow (305 px client and scroll widths), Receipt wrapping, science focus and Grade 6 band context.
- JavaScript syntax and Git whitespace checks.

[Desktop science evidence](review-assets/wednesday-science-desktop.jpg). Mobile checks use a real rendered iframe viewport, not a physical phone or touch emulation. Prior native-zoom and full accessibility limitations remain. These are bounded builder checks, not independent review or human semantic review.

## Next packages

Package 2 compares the bounded science, mathematics and ELA material without presupposing equivalence. Page 34's references to other literacy and math standards are source leads, not links to our existing NY-7.RP.2 and 7R1 nodes. Package 3 supplies a separate AI audit, repairs and final Wednesday review. This first publication does not close all of Wednesday.

Exact edition/cohort applicability remains unresolved. No local district assumption, mastery assertion or broader completion claim was added. The first package is complete when this candidate and its evidence are durably saved and successfully published; the publication record is added after deployment.

## Publication confirmed

Public Site version 11 succeeded on September 30, 2026. Research commit `6b64e00d3fe710ebb256770cdd475c9cfded88c1`; Site source `c8ec5ff7a808e609a736985cec09f92c31ec523a`. See `data/publications/wednesday-0.0.7.json` for the exact native publication record. Package 1 is complete. This post-publication confirmation does not imply completion of packages 2 or 3.
