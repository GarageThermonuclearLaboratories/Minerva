# Primary PDF intake · 2026-09-28

The user supplied two PDFs after direct retrieval failed. Original bytes are retained under `sources/originals`; SHA-256 digests, PDF metadata, byte lengths and page counts are in `data/sources.json`. Live-URL byte equality is unverified.

The complete standards document has 171 pages. Its cover reads “2017” and “Updated June 2019.” Embedded modification metadata is dated March 18, 2024; this is not assigned as a policy or publication date. Exact legal effective dates remain null.

Printed page 90 (PDF page 90) contains NY-7.RP.2 and all four subparts. The heading and a–d were checked visually against page text. The crosswalk has 13 pages; its pages 1–2 corroborate the wording but carry an NYSED Grade 7 Draft footer. The full standards document replaces the draft-marked crosswalk as primary support for this graph slice. Stable source IDs were retained.

The graph now contains 11 nodes and 14 edges: four new source substandards with parent and grade links. The two existing parsed expectations still decompose only the parent heading. They do not purport to exhaust the subparts. Notes and examples remain accessible on the source page; no semantic decomposition of them is claimed.

Six directed Coherence arrows involving this family are recorded as source observations in `data/source-review.json`. They have not been relabeled as prerequisites. Relationship semantics and target expectations need review before graph ingestion. This is an observed source feature, not an ontology-derived finding.

All 184 PDF pages have text extracts, but only the stated pages were visually reviewed. Text extraction is not semantic parsing or human review. PyMuPDF version and method are preserved with the extracts. Both fictional students now carry the same parent and four subpart IDs as EXPECTED.

No Garage internal ontology was used. No findings or canonical assumptions were added. Historical HTTP 502 failures remain in the record, now resolved through user upload.
