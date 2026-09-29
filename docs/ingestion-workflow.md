# Reusable PDF ingestion workflow · Monday M4

This workflow accepts an operator-supplied PDF and source record, preserves the bytes, registers provenance, extracts every page, renders selected evidence pages, and emits a semantic review queue. It does not parse educational meaning or promote any ontology claim.

## Reproduce the existing two-document run

Use Python 3.10 or newer. Install the pinned extraction/render dependency in your project environment:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/ingest_sources.py build
python3 scripts/ingest_sources.py check
python3 scripts/validate.py
python3 scripts/test_ingestion.py
```

Run these commands from the repository root, without Python's optimization flag. The existing validator uses assertions. The new ingestion integrity checks use explicit exceptions and do not depend on assertions.

`build` reads acquired entries in `data/sources.json`. Current configuration renders full-standards pages 1 and 90 and crosswalk pages 1 and 2. All other pages receive text extraction and a pending review task. Selected pages are physical PDF page numbers starting at 1; printed page labels must be recorded during semantic review.

## Register another document

First obtain the PDF through an authorized download or upload. The workflow starts from local bytes; it does not fetch URLs. Use a distinct source edition ID and prepare a JSON record such as:

```json
{
  "id": "src:nysed:example-edition",
  "title": "Replace with the actual document title",
  "authority": "New York State Education Department",
  "url": "https://www.nysed.gov/replace-with-observed-source-url",
  "acquisition_method": "user-upload",
  "acquired_at": "2026-09-28",
  "version": "Exact visible edition label, or not established",
  "role": "primary-standards-document",
  "provenance_note": "State how these bytes were obtained and whether equality with the cited live URL was independently verified."
}
```

These example values are placeholders; supply the actual acquisition date and evidence. A URL is provenance, not an instruction to trust the contents. Never claim an official download when the acquisition was a user upload.

```sh
python3 scripts/ingest_sources.py register --input /absolute/path/document.pdf --record /absolute/path/source-record.json
python3 scripts/ingest_sources.py build
python3 scripts/ingest_sources.py check
```

Registration validates PDF readability, stores SHA-256/byte/page counts and embedded metadata, copies bytes to `sources/originals/<sha256>.pdf`, and adds the source entry. It deliberately leaves policy dates unknown and review pending. Review any supplied date evidence separately. Existing source IDs are rejected rather than overwritten; use `build` for repeat runs and a new edition ID for changed evidence. Existing legacy archive filenames remain supported.

Before building, optionally add the new source ID and page list to `data/ingestion-config.json`; otherwise only page 1 is rendered. The scale must be greater than zero and at most four. Blank extracted text is flagged in the queue; OCR is not implemented. Scanned pages remain pending until an appropriate extraction/review method is added.

## Generated artifacts

`data/ingestion-manifest.json` links each acquired source to a versioned bundle in `sources/processed/<source-sha256>/<recipe-hash>/`:

| Artifact | Purpose |
| --- | --- |
| `metadata.json` | File hash, byte/page counts, and embedded metadata; metadata is not a policy date |
| `pages.json` | Page text and extraction recipe; reading order is not semantic structure |
| `page-N.png` | Selected evidence pages rendered with pinned PyMuPDF |
| `review-queue.json` | One pending task per physical page, with empty-text and rendered-page indicators |

The recipe records pipeline version, dependency version, selected pages, and rendering scale. Different recipes create different bundles. Rebuilding the same recipe must reproduce identical bytes. If an existing generated artifact differs, the build stops and preserves it; inspect the difference and version the processing method rather than overwriting evidence.

The manifest records hashes for every generated artifact. `check` verifies source integrity, artifact hashes, acquired-source coverage, page/queue counts, configuration agreement, and the no-promotion boundary. The main validator calls these checks when an ingestion manifest is present. Historical `sources/extracted/*.pages.json` and the original `extract_sources.py` remain for the 0.0.3 record; the new processed bundles are the current ingestion products. The legacy page-90 wording check remains specific to the initial math slice.

Generated queues are immutable task lists, not completion ledgers. Store review decisions separately under `data/reviews/`, keyed to task IDs, source hashes, page locations, reviewer/run identity, findings, and the ontology commit affected. The ingestion code never reads or rewrites that directory. Existing selected-page review in `data/source-review.json` remains valid history; generated pending tasks do not erase it or claim those pages were never inspected. Reconcile the prior review with full semantic review explicitly.

## Publication and failure handling

The pipeline does not change `data/ontology.json`, student states, release labels, or the deployed Site. Registration changes the source manifest; refresh its public copy before running the full repository validator:

```sh
cp data/sources.json dist/sources.json
python3 scripts/validate.py
```

Review, commit, and publish through the normal release gate. Generated evidence remains inspectable in the repository; the current Site still uses its existing selected images until its publication package is updated.

Run one writer at a time. Manifests use a temporary file and atomic replacement, but the entire workflow is not a multi-file database transaction. If interrupted, an immutable archive/bundle may remain before the receipt is written; rerun the same operation after inspection. Do not delete source bytes or change hashes to make a check pass. An interrupted manifest write may leave a `.tmp` file, which must be inspected before a retry. Changed source bytes, invalid page selections, duplicate IDs, and HTML error bodies are rejected.

## Monday demonstration and verification

- Both original PDFs processed through the same `build` command: 171 + 13 = 184 extracted pages and pending semantic-review tasks.
- Four selected evidence PNGs generated. Full-standards page 90 and crosswalk page 2 were visually inspected after generation; wording, table layout, and the Draft footer are legible. This is rendering QA, not completion of semantic review.
- Five regression tests passed: new source registration and idempotence with preserved review decisions; source corruption rejection; invalid pages and duplicate IDs; output corruption detection without overwrite; and rejection of HTML masquerading as a PDF.
- Full repository validation passed. Ontology remains 11 nodes / 14 relationships; no semantic claims were added by ingestion.

M4 is complete for repeatable local PDF intake and evidence preparation. Automated downloading, OCR, semantic parsing, review-decision tooling, and generalized policy validation remain outside this completed workflow.
