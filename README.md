# Wildcats / Minerva

An evidence-linked computational model of the canonical New York State K–12 educational pathway, with a humane exploration interface. Policy snapshot: **2026-09-28**. This repository begins with a deliberately narrow Grade 7 mathematics slice; it does not claim statewide corpus completion.

## Method

State source → verbatim standard record → parsed expectation → ontology relationship → public receipt. The `SOURCE`, `PARSED`, `NORMALIZED`, `INFERRED`, `PROVISIONAL`, `CONTESTED`, and `REJECTED` labels describe claims, not people. A school expectation is never evidence of a particular student's mastery. Diploma requirements are tracked separately from learning standards.

The v0.1 construction is clean-room: no Garage-internal ontology class, hierarchy, primitive, mapping, or expected finding is used to derive Wildcats. Any post-freeze comparison requires a separate crosswalk.

## Contents

- `data/sources.json`: source manifest and policy applicability
- `data/ontology.json`: stable IDs, assertions, student-state projection, and unresolved questions
- `schema/ontology.schema.json`: machine-checkable shape for the first slice
- `scripts/validate.py`: checks references, provenance, and policy state
- `dist/`: static Minerva interface, built directly from the versioned slice
- `docs/`: decisions, coverage, and lab log

## Source review checkpoint

Release 0.0.2 adds `data/source-review.json` and a twelve-content-area `data/corpus-plan.json`. All seven source records remain search-excerpt-only; full PDF acquisition is blocked by HTTP 502. See `docs/source-review.md`.

## Rebuild / inspect

Run `python3 scripts/validate.py` from this directory. The static site reads `dist/data.json`, which is copied from `data/ontology.json`; run `cp data/ontology.json dist/data.json` after an ontology edit, then validate again. A future pipeline should generate exports and site data rather than relying on this explicit copy step.

GitHub is the canonical engineering record: [GarageThermonuclearLaboratories/Minerva](https://github.com/GarageThermonuclearLaboratories/Minerva). ChatGPT Site source commits and GitHub commits are separate Git histories; each deployment records both identifiers where available.
