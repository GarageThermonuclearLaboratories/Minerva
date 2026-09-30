# Wildcats / Minerva foundation specification

Specification version: **0.1.0** · Policy snapshot: **2026-09-28**  
Baseline inspected: research release `wildcats-0.0.3-primary-pdfs`, local commit `ea2e9e0`.  
Status: project requirements and architecture; implementation coverage is recorded below. This specification version is not the ontology v0.1 freeze.

## 1. Purpose and responsibilities

Wildcats models what a student following the canonical New York State K–12 general-education pathway is expected to know and be able to do. Its research question is: **What learning does the documented pathway require, how does that learning relate, and what evidence supports each assertion?**

Minerva is the humane interface to that model. It lets a person explore grades, subjects, expectations, connections, and fictional learners, then inspect the evidence behind an answer. Reading JSON must never be a prerequisite for understanding a claim.

| Component | Responsibility | Authority boundary |
| --- | --- | --- |
| Wildcats research corpus and graph | Preserve sources, represent expectations, document transformations, test relationships, retain uncertainty | A project interpretation is not a new state requirement. |
| Minerva interface | Present the graph through Atlas, Curriculum, Journey, Crossroads, Follow the Wildcats, Workbench, Findings, Lab Log, and eventually Ask Minerva | Presentation cannot strengthen a claim, hide its uncertainty, or create curriculum facts. |
| GitHub research record | Version sources, data, code, decisions, reviews, and release evidence | A commit proves what was recorded, not that its contents are true. |
| Site publication | Expose a named research snapshot and its receipts | A successful deployment proves publication, not scientific validation. |

Here, “must” states a required project rule. It does not assert that code already enforces that rule. The implementation matrix in section 12 identifies the difference.

## 2. Canonical scope and authority

The canonical pathway is a declared reference model: ordinary, nonaccelerated, nonspecialized NYS public-school general education from kindergarten through Grade 12. It is not a statistical average of students or a claim that every district teaches identical lessons.

The corpus inventory covers the twelve queued content areas: Arts; Career Development and Occupational Studies; Computer Science and Digital Fluency; English Language Arts; Family and Consumer Sciences; Health; Mathematics; Physical Education; Science; Social Studies; Technology; and World Languages. A queued area is not evidence of a universal course requirement. Prekindergarten material may supply context without expanding the K–12 completion denominator.

Learning standards, local curriculum choices, courses, credits, assessments, and diploma requirements are distinct entities. A standard does not specify a textbook, daily lesson, course schedule, assessment score, or diploma entitlement unless separate evidence establishes that relationship. Source grade bands must be preserved; the model must not invent single-grade placement from a band.

Apply authority according to the question:

1. Use applicable primary state standards and authoritative state policy instruments for statewide claims. Preserve the issuing authority and document type. Supporting NYSED guidance helps interpretation but cannot silently override a governing instrument.
2. Use Johnson City Central School District material only where a necessary local implementation question remains unresolved by state sources. Mark its jurisdiction and local scope.
3. If a reference pathway still requires a choice, record a canonical assumption with rationale, alternatives, affected claims, and review status. An assumption must never appear as a NYSED mandate.

If state sources conflict, preserve both and mark the affected claim contested while resolving document authority, version, date, and cohort. A district source or model preference cannot resolve a statewide conflict by fiat.

Accelerated/gifted pathways, disability-specific accommodations and alternate pathways, behavioral interventions, CTE/New Visions programs, and other specialized variants are deferred. The core may later support separately scoped variants; their absence says nothing about individual students' entitlement or ability.

## 3. EXPECTED learning and the fictional learners

**EXPECTED** means the model associates a learning expectation with a specified pathway, grade or band, and policy context. It is a normative state, not a measurement of a learner.

**Observed mastery** would require evidence of a particular person's performance, a specified task or assessment, criteria, time, and interpretation. No such data exists in the current model. `EXPOSED`, `EXPERIENCED`, and `DEMONSTRATED` remain future concepts; enrollment, instruction, exposure, grades, and graduation must not be treated as interchangeable with mastery.

Matthew and Eva are fictional navigation avatars. Matthew is represented as a white boy and Eva as a Black girl; those identities do not change standards, expectations, ability, opportunity, or predicted outcomes. They are not models of Willis's children. At the same grade, pathway, and policy context, both must project the same expected graph.

Changing the selected avatar changes the narrative point of view. Changing grade or policy context may change the applicable expectation set. An empty grade view means “not yet modeled,” not “nothing is expected.” The Atlas remains the primary ontology; avatars are ways to explore it.

## 4. Claim status, evidence availability, and review

The seven existing claim labels answer different questions and must not be treated as a confidence ladder.

| Label | Meaning | Required support |
| --- | --- | --- |
| `SOURCE` | Wording or structure explicitly present in a cited source | Exact location and faithful representation; not proof of current applicability |
| `PARSED` | A decomposition or interpretation of source wording | Parent record, retained wording, and explanation of the decomposition |
| `NORMALIZED` | A reviewed representation using consistent terminology or identifiers | Input records, mapping rule, rationale, and preserved distinctions |
| `INFERRED` | A relationship or conclusion not explicitly stated by the source | Premises, method, scope, limitations, and review |
| `PROVISIONAL` | A candidate awaiting sufficient evidence or review | Candidate rationale and the unresolved requirement |
| `CONTESTED` | A claim with unresolved conflicting evidence or interpretations | Competing positions and evidence; no silent preferred answer |
| `REJECTED` | A considered claim or hypothesis excluded after review | Rejection reason, evidence, and retained history |

`SOURCE` through `INFERRED` describe derivation. `PROVISIONAL`, `CONTESTED`, and `REJECTED` describe disposition. The current single `status` field mixes these dimensions. Until separate fields are implemented, changing disposition must preserve prior derivation and rationale in the review record and version history. Rejection is not deletion; normalization is not automatic promotion to certainty.

Acquisition and review are separate dimensions. `search-excerpt-only` and `full-document-acquired` describe available evidence, not authority. Extracted text is a processing product. Agent visual review of selected pages is not full-document semantic review, human review, or independent audit.

A snippet may support a narrowly qualified observation in the evidence register, but it cannot establish complete standard wording, exhaustive coverage, or verified policy applicability. Unknown or disputed claims may be stored and displayed with their status; storing them does not admit them into an unqualified canonical answer.

## 5. Provenance contract

Every published claim must be traceable to source evidence or an explicit project assumption. Merely attaching a source URL to an inferred claim is insufficient.

| Record | Minimum receipt |
| --- | --- |
| Source edition | Stable source/edition identity, authority, title, document role, URL, retrieval/acquisition date and method, version label, acquisition and review state, temporal applicability or explicit unknown |
| Acquired file | Archive path, SHA-256, byte count, page count where applicable; relationship to the cited URL and any unverified byte equivalence |
| Source assertion | Stable claim ID, wording or structural assertion, source edition, exact section/page location, review state, scope |
| Parsed/normalized assertion | Source assertion IDs, transformation rationale or rule, retained original meaning and qualifiers, reviewer/run record |
| Inference/hypothesis | Premise IDs, reproducible method where computational, assumptions, conclusion, limitations, disposition and review evidence |
| Canonical assumption | Decision ID, unresolved question, chosen convention, alternatives, jurisdiction, rationale, affected records, reviewer |
| Review/release | Artifact or commit reviewed, checks performed, reviewer/run identity, findings, repairs and remaining issues; actual model/effort only if known |

PDF page numbers are one-based physical pages. Printed page labels must be recorded separately when they differ. For web documents, preserve a retrievable capture or excerpt with heading/section and retrieval date sufficient to locate the assertion; a mutable URL alone is not a durable receipt.

A hash identifies bytes. It does not prove authorship, completeness, legal authority, or equality with the file currently served at an official URL. The two existing PDFs were user uploads associated with supplied NYSED URLs; that acquisition history must remain visible.

Standards must retain official identifiers and verbatim text separately from project labels. Existing `wc:standard:ny-7-rp-2` identifies the project standard concept; `src:nysed:math-full` identifies the current source record. Neither identifier alone distinguishes all future editions. Before ingesting a changed edition, add edition identity and versioned assertions rather than overwriting the historical meaning. Never reuse retired IDs for unrelated entities; record replacements and migrations.

## 6. Policy time, cohorts, and snapshot semantics

The baseline query date is **September 28, 2026**. This date fixes the policy question; it does not certify that every source has been shown to apply on that date.

Keep these dates distinct: adoption, publication, document revision, implementation, assessment alignment, legal effectiveness, supersession, retrieval, and project review. Preserve available precision: a month remains a month, a season remains a season, and an unknown value remains unknown. File metadata is not policy evidence. Never convert “September 2022” into an asserted effective day of September 1.

An applicability decision must identify the policy query date, relevant grade/course/pathway and jurisdiction, any source-defined cohort criterion, and supporting evidence. Record whether the result is applicable, inapplicable, or unresolved. These are required semantics; a cohort resolver is not yet implemented.

Cohort rules must use the source's actual basis, such as entry year, assessment year, or another explicitly defined population. Do not infer an entry cohort from age or graduation year without a documented rule or visible assumption. Where a missing cohort would change an answer, return the alternatives or request that detail.

The initial K–12 journey is a reference pathway under the selected policy snapshot, not a reconstruction of thirteen historical school years for a real child. A historical cohort journey would require year-by-year policy resolution. Advancing the avatar slider does not perform that resolution.

Future announcements remain in a separate policy layer until their applicability is established. Future-policy analysis is deferred by Monday's scope freeze. Sources discovered later may help answer the September 28 question, but their later retrieval dates must be preserved; never backdate the evidence trail.

## 7. Valid ontology claims and relation semantics

A claim is eligible for a canonical answer only when its identity, meaning, evidence, scope, temporal applicability, and review state support the strength of that answer. Technical validity and evidential validity are separate gates: valid JSON and connected nodes do not make a claim true.

Before accepting a claim, check:

1. It states one identifiable assertion and preserves material source qualifiers, examples, alternatives, and grade-band scope.
2. Its source is suitable for that assertion and its exact support is inspectable.
3. Its derivation is labeled; any inference has explicit premises and a justified method.
4. Its relation has a defined direction and endpoint types, and all references resolve.
5. Its temporal/jurisdictional scope is established or presented as unresolved.
6. Conflicts, assumptions, limitations, and review state are visible; rejected claims are excluded from accepted results.

Existing relation meanings are:

M5 migration: the candidate replaces the five `EXPECTED_BY` edges with `ASSIGNED_TO_GRADE` (Standard → Grade), meaning source grade placement only. It does not imply an attainment deadline. The table retains the inspected 0.0.3 predicate for historical context; see [the migration record](semantic-trace-ny-7-rp-2.md).

| Relation | Direction and meaning | Does not imply |
| --- | --- | --- |
| `PART_OF` | Standard/subpart → documented parent standard or domain | Prerequisite, teaching order, or mastery inheritance |
| `ASSIGNED_TO_GRADE` | Standard → grade placement in its source edition; replaces the initial EXPECTED_BY predicate | Observed mastery, an attainment deadline, or independently verified cohort applicability |
| `DERIVED_FROM` | Parsed expectation → source standard whose wording was decomposed | That the source author endorsed the project's decomposition |
| `USES_CONCEPT` | Expectation → concept identified through parsing | Concept equivalence across every subject or context |

`EXPECTED_BY` is a project predicate. Existing Grade 7 edges encode source grade placement; any end-of-grade interpretation must be justified or explicitly qualified during semantic review. A `SOURCE` label on those edges does not resolve every temporal interpretation of the predicate.

New relation types need definitions, allowed endpoint types, direction, evidence requirements, and any valid inference rules before use. Do not assume symmetry, transitivity, equivalence, or prerequisite closure. A claim about two source-supported nodes still needs evidence for their relationship.

**Worked example:** `wc:standard:ny-7-rp-2` preserves “Recognize and represent proportional relationships between quantities.” from the archived full mathematics document, PDF/printed page 90. The project separates “recognize” and “represent” into two `PARSED` expectations. That decomposition neither exhausts subparts a–d nor proves that either avatar can perform them. The receipt can establish what this edition says while separately reporting that exact snapshot applicability remains unresolved.

The six arrows labeled “Coherence” on the same source page are recorded observations. Their existence is evidence of source connections; translating them into `PREREQUISITE` edges requires additional semantic justification.

## 8. Required abstentions

The system must decline to assert the following unsupported conclusions and explain what evidence is missing:

- A learner has mastered something because a standard, grade assignment, course, or diploma mentions it.
- Matthew and Eva require different expectations because of race, gender, or their narrative identity.
- Earlier grade placement, adjacent pages, arrows, or shared vocabulary establish a prerequisite, equivalence, or causal relationship.
- Every student follows a particular textbook, course sequence, local practice, or specialized pathway.
- A draft crosswalk supersedes the primary standards or a newer file timestamp establishes a new policy.
- A policy applies to every cohort, or an announcement is already effective, without applicability evidence.
- An absent graph record proves there is no standard, no requirement, or no expected learning.
- Acquired pages, extracted text, node counts, or successful validation establish semantic completeness.
- A plausible language-model explanation is source evidence, or a familiar Garage framework supplies a missing educational primitive.
- An unreviewed hypothesis is a research finding, a self-review is an independent audit, or a planned action has occurred.

Abstention should remain useful: show the supported portion, identify the gap, and link the unresolved question or review task. A disputed relationship may be explored as a labeled hypothesis without entering the accepted graph.

## 9. Clean-room construction

Until the ontology v0.1 freeze, derive educational classes, relationships, mappings, and findings from NYSED sources and ordinary ontology engineering. Do not import Garage-internal ontology classes, hierarchies, primitives, mappings, or expected findings as design inputs. Merely changing their names does not satisfy this boundary.

Project operating requirements may govern provenance, storage, and review; they cannot predetermine educational discoveries. If internal ontology material is encountered, do not use it to shape the model. Record any actual influence and quarantine or rederive affected claims from permitted evidence. Access to an internal file is not authority to use its contents.

After a tagged v0.1 freeze, comparison may occur in a separately versioned crosswalk. Preserve the frozen baseline and label crosswalk matches as comparison results, not original independent discoveries.

## 10. Architecture and workflow

The intended path is: archived evidence → page/section extraction → reviewed source assertions → parsed expectations → normalized concepts and justified relationships → validated release → Minerva receipts.

Each transformation preserves its inputs and adds traceability. Extraction generates a review queue; it does not approve claims. Semantic reviewers check tables, arrows, notes, examples, and qualifiers against source pages rather than trusting text reading order. Findings must identify the graph release, query or method, supporting claims, limitations, and review outcome. Preserve rejected hypotheses and failed acquisitions in the research record.

Minerva must display the original evidence, project interpretation, status, applicability uncertainty, and release identity together. Coverage must distinguish identified documents, acquired documents, extraction, semantic parsing, normalization, relationships, validation, and human review. Percentages require a stated denominator; an unknown corpus size cannot yield a credible completion percentage.

The current implementation uses versioned JSON and a static JavaScript interface. No OWL/RDF serialization, automated reasoner, natural-language query engine, or end-to-end semantic compiler is implied by calling the project an ontology.

## 11. Versioning, review, publication, and freeze

Version the specification, data model/schema, ontology release, source editions, and deployed Site separately. Record their compatibility in release notes. A schema or meaning change requires a documented migration: what changed, why, affected IDs, and how previous releases remain interpretable. Correct errors through new commits/releases while preserving prior records and correction reasons.

Before publication, validate data/export agreement, source integrity, references, relation semantics, applicability language, and review claims. The independent daily audit must identify the actual artifact reviewed and its reviewer/run. Record remaining findings and resolve release-blocking errors. Self-review is useful but must retain that label. A model name or higher reasoning setting alone does not prove independent review.

GitHub is the canonical research/engineering record. The Site currently has a separate source history. Release receipts must connect the research commit, Site source commit, release label, deployed version, deployment outcome, and timestamp. A post-deployment receipt may be appended afterward and must say so; do not imply it was in the already-published bundle. The top-level `git_revision` is currently null; `dist/release.json` supplies the research pointer.

The planned Friday v0.1 freeze requires a declared scope/coverage statement, archived source manifest, reproducible build/validation instructions, reviewed claims, unresolved/contested/rejected registers, completed audit with blocking findings repaired, and a release manifest linking exact commits and artifacts. Create an immutable tag only when those requirements are met. The calendar does not turn an incomplete checkpoint into a freeze. Deficiencies and scope changes require explicit reporting; they must not be hidden by retagging an existing release.

Monday's checklist establishes a narrower foundation checkpoint. Completing this specification closes its documentation gate only. It does not complete corpus ingestion, semantic review, audit, publication, or the v0.1 freeze.

## 12. Implementation coverage and known gaps

Subsequent M6 update: [the K–12 journey scaffold](k12-journey.md) provides five navigable stages and shared avatar projection. Grade coverage gaps and transition-policy review remain explicit. These navigation groupings do not expand the semantic corpus.

Subsequent M4 update: [the ingestion workflow](ingestion-workflow.md) now implements local source registration, immutable processing bundles, selected rendering, pinned extraction dependency, generated review queues, and integrity checks. The table below retains the inspected 0.0.3 baseline; automated downloading, semantic review decisions and cohort resolution remain open.

This matrix reports the inspected 0.0.3 baseline, not promises about future code.

| Requirement | Existing evidence/implementation | Remaining gap |
| --- | --- | --- |
| Responsibilities and canonical scope | [README](../README.md), [decisions](decisions.md), this specification | Full source inventory and pathway representation remain incomplete. |
| EXPECTED state and avatar equality | [ontology data](../data/ontology.json); [validator](../scripts/validate.py) compares the two Grade 7 ID lists | State value, general pathway equality, and cohort behavior are not comprehensively enforced. |
| Claim status and relation semantics | Nodes/edges carry statuses; validator checks allowed labels and endpoint existence | Separate disposition/derivation, typed relation constraints, inference rules, and acceptance filtering are missing. |
| Provenance and source integrity | [source manifest](../data/sources.json), archived PDFs, page locators, hashes and byte/page counts checked | Mandatory provenance fields, unique source IDs, derivation chains, reviewer identity, and future edition identity are not comprehensively validated. |
| Source fidelity | Validator checks stored standard text against normalized page 90 text; [PDF review](primary-pdf-review.md) records selected visual checks | Examples/qualifiers and complete subpart parsing require semantic review; substring matches alone do not establish completeness. |
| Temporal rules | Snapshot equality checked; partial dates and uncertainty in [source review](../data/source-review.json) | No cohort/applicability resolver. Current all-effective-dates-null assertion is a snapshot safeguard, not a general rule forbidding evidenced dates. |
| Clean room and prohibited inferences | README, decisions, this specification; no inferred findings currently recorded | Governance/manual review, not an automated contamination or reasoning check. |
| Extraction | [extract_sources.py](../scripts/extract_sources.py) regenerates text for acquired manifest entries | Generic acquisition/registration, evidence rendering, dependency pinning, and semantic review queue remain incomplete. |
| Public receipts and humane interface | [app.js](../dist/app.js) exposes source wording, page evidence, statuses and review notes | Receipts are tailored to page 90; broad K–12 journey and advanced Ask Minerva remain unimplemented. |
| Versioning and publication | [release pointer](../dist/release.json), [Lab Log](lab-log.md), separate Git histories | Monday M7 audit exists; Tuesday expansion has builder review only. No v0.1 freeze or comprehensive schema migrations. |
| Validation | Explicit Python assertions and public/source JSON equality | JSON schema is skeletal and is not loaded by the validator; passing the script is not proof of specification compliance. Run without Python optimization, which disables assertions. |

## 13. Reader acceptance check

A reader should now be able to answer:

- What does the project model? A declared normative NYS reference pathway, with scoped evidence and explicit gaps.
- What are Matthew and Eva? Fictional views of the same expected graph, without mastery data.
- What does `SOURCE` prove? That an assertion is represented as explicit source content; acquisition, review, and current applicability still require inspection.
- When may the system infer a relationship? When premises, relation meaning, method, scope, and review justify it and its inferential origin remains visible.
- What happens when evidence is absent or conflicting? Preserve an unresolved or contested record and qualify the answer.
- Is this entire architecture implemented? No; section 12 identifies the current implementation and missing enforcement.
- Is Monday or v0.1 complete because this document exists? No; the [closure checklist](monday-closure-checklist.md) and release gates determine completion.

Prepared through builder review of the repository and established project requirements. No independent or human audit is claimed by this document.


## September 29 implementation amendment · Tuesday package 1

`validate.py` now invokes `acceptance.py` for bounded relation/endpoint, provenance, derivation, parsed-field, and avatar-export checks. Expected-learning projection excludes rejected/unresolved records and requires eligible assignment, parent, and derivation links. The original implementation-gap table above is a historical baseline. General inference validation, separate derivation/disposition fields, and applicability resolution remain open. The JSON Schema is still descriptive and skeletal, not the enforcement mechanism. See [Tuesday acceptance checkpoint](tuesday-acceptance.md) for tested scope and remaining limits.
