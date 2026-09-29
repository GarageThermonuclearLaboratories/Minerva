# Public interface revision · v0.0.4

September 29, 2026 · Willis's consolidated sixteen-part revision brief.

The revision extends the audited Monday candidate and preserves the dark field, bone typography, cyan instrumentation, serif/sans hierarchy, thin rules, and Explore/Research split. The supplied brief referred to the older v0.0.2 screenshots; the previous public deployment was v0.0.3. No educational node, edge, source wording, student state, or policy date is changed by this interface pass.

## Implemented against the brief

| Request | Result |
| --- | --- |
| Front-door thesis | Explains Wildcats, Minerva, the research ambition, and the present zero-findings boundary. |
| Actual ontology on arrival | Interactive parent and two heading expectations appear in the first mapped region. Four subparts and all six expectations remain inspectable through Curriculum, the graph, and Receipts. |
| Existing interaction grammar | Explore/Research, Source → Structure → Receipt, visible zeroes, and public corrections retained. |
| Expected/mastered notice | Expandable persistent notice, open on Atlas and Follow the Wildcats; compact elsewhere. |
| Unknown territory | Dashed, muted unmapped surfaces; distinct status badges and a legend separating derivation, disposition, review, and coverage. “Known” is explained rather than invented as a truth status. |
| Discrete grade control | Thirteen grade buttons explicitly identify twelve unmapped grades and one partial grade; stage dropdowns also identify coverage. Same projection for both avatars. |
| Taxonomy | Renders actual NYSED grade/subject/domain records. Explicitly states that no normalized Mathematical Reasoning capability family is asserted. Adds no hierarchy. |
| Fictional student lens | Receipts for grade-assigned standards/expectations/concepts open the shared Grade 7 view and focus the relevant object when represented there. Fictional-reference context remains visible. |
| District roles | Methodology explains Garage City's fictional role and Johnson City CSD's conditional local-reference role; current trace uses no local assumption. |
| Signature Receipt | No empty column. Selected objects open a fixed panel with close, expand/reduce, Escape, focus restoration, provenance, source/parse/normalization/relationship distinctions, audit limits, and unresolved issues. |
| Bounded graph | Actual one-step incident neighborhood, deliberate two-step expansion, recenter from a selected object's Receipt, maximum twenty nodes. Exact directed predicates remain in the adjacent text list. No fabricated prerequisites, successor chains, or equivalences. |
| Conservative Findings | Zero findings retained. Documents the required claim/evidence/version/method/review/date contract without creating a pretend finding or disabled action. |
| Workbench matrix | Twelve real content-area records, mathematics first, with six separate progress columns and expandable exact statuses. All human-review statuses remain pending. |
| Living research indicator | Computes the change against published v0.0.3's 11 nodes/14 edges: +4 nodes/+8 links, zero findings. Labeled “Since v0.0.3,” never “Today” or a simulated live feed. Opens the Lab Log. |
| Concrete defects | Footer separation, readable checkpoint label, explicit dated/versioned reverse chronology, nonshrinking mobile navigation with a scroll hint, and collapsed Receipt. |
| Multiple densities | Atlas has spatial structure; Workbench has a compact matrix; the student view has discrete human-scale navigation, all within the existing visual system. |

## Verification and limits

Repository validation, the seven ingestion regression tests, existing receipt checks, and JavaScript syntax checks passed. `scripts/test_interface.cjs` additionally exercised the actual DOM using jsdom 30.1.1: eight views; all fifteen object Receipts; graph-node/edge identity and bounded expansion; contextual student navigation; thirteen grades for both avatars; transition abstention; matrix expansion; Receipt close/reopen/expand/Escape; and both possible script/data arrival orders. These checks verify DOM behavior, not rendered browser layout or visual accessibility.

The managed preview does not support this buildless static site, and the available environment lacks a browser executable. No new real-browser visual QA pass is claimed. Responsive CSS confines wide graphs and matrices to labeled scroll regions; a future rendered-browser pass should check typography, overflow, zoom, and touch interaction.

For the additional DOM check, install the pinned development-only dependency outside the source tree if it is not available, then point Node at it:

```sh
npm install --prefix /tmp/minerva-dom-qa --no-package-lock --ignore-scripts --no-audit --no-fund jsdom@30.1.1
NODE_PATH=/tmp/minerva-dom-qa/node_modules node scripts/test_interface.cjs
```

M7's independent audit covers its recorded baseline and repair diff. This subsequent interface revision is builder-verified; it is not retroactively included in that independent audit. Human semantic review, edition/cohort applicability, generalized enforcement, and broader corpus work remain open. Publication success and exact repository/deployment identifiers are recorded separately after deployment.
