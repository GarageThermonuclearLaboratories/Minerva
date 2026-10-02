# Friday freeze readiness

Status: **candidate integrity passed; freeze blocked**. This package locks the exact published and separately reviewed candidate, verifies the formal foundation prerequisites, and preserves the remaining project gate. It does not create v0.1 or an immutable tag.

## Locked candidate

- Ontology release: `wildcats-0.0.8-wednesday-comparisons`
- Reviewed research commit: `a4945c8809047aea6dd9aad54a9152bbed962eda`
- Public Site candidate: version 17; source `85ab266efd82f9bf486480e6afdcfbc39aca475c`
- Deployment: `appgdep_6abee0d284fc819193bd0e884319e695`, succeeded October 1, 2026
- Educational snapshot: the five data files exactly match the SHA-256 values in Thursday's separate review

The candidate remains 26 nodes, 31 edges, nine parsed expectations and zero findings. Mathematics and ELA are exact Grade 7 assignments; the two science expectations are shared grades 6–8 band context, not individual Grade 7 assignments. Matthew and Eva receive identical projections.

## Audit result

The mechanical readiness audit passed provenance, temporal precision, comparison disposition, coverage-language, avatar-parity and ontology-drift checks. It rehashed all 42 archived NYSED PDFs in the 47-record source manifest, totaling 1,237 pages, and compared the source data with every public export. Unknown effective dates remain `null`. The graph contains no prerequisite or equivalence edge. Crossroads still contains one `PROVISIONAL` analogy and two `REJECTED` equivalence proposals, with no promotion to a graph edge, hypothesis or finding.

The earlier separate Thursday verdict remains the independent review authority for the bounded question layer and safeguards. This readiness package is builder mechanical review of the unchanged educational snapshot plus status documentation; it does not widen that verdict or substitute for human semantic review.

## Material correction

`dist/release.json` still said `prepared-for-publication` after public Site version 17 had succeeded. That temporal defect is corrected to `published-unfrozen-candidate`. The release now separately records `freeze_status: blocked-rendered-qa`, the exact locked research commit, and the locked Site version.

## Freeze decision

The seven formal prerequisites named in the foundation specification are demonstrable for the locked bounded candidate: declared scope, archived manifest, reproducible validation, reviewed claims, unresolved/rejected registers, repaired blocking findings, and an exact publication receipt. One project release gate remains open: fresh rendered desktop/mobile QA under the required Sites preview workflow.

The runtime does not provide the required control-browser capability, and the managed-preview instructions prohibit substituting a different browser path. No fresh screenshot, rendered layout, native zoom or complete accessibility result is claimed. Consequently:

- v0.1 freeze is not authorized;
- an immutable tag is not authorized;
- Thursday is complete for code review and publication, but not for the outstanding visual follow-up;
- exact edition/cohort applicability, statewide corpus completion, human review and comprehensive accessibility remain outside the candidate's claims.

## Reproduce

After cloning, reassemble the split archived PDF and run the full suites:

```sh
python3 scripts/restore_sources.py
python3 scripts/check_freeze_readiness.py
python3 scripts/validate.py
python3 scripts/test_comparisons.py
python3 scripts/test_acceptance.py
python3 scripts/test_ingestion.py
node scripts/test_ask.js
node scripts/test_thursday_independent.cjs .
node scripts/test_receipts.js
node scripts/test_interface.cjs
```

The DOM suite requires jsdom in the invoking environment and is not rendered-browser verification. The machine-readable decision is in `data/reviews/friday-freeze-readiness.json`.

All 65 readiness assertions, 91 Ask checks, 72 independent-probe replays, 25 comparison tests, 28 acceptance tests, seven ingestion tests, the main validator, Receipt/projection checks, the nine-view DOM suite and JavaScript syntax/whitespace checks passed. The first aggregate command named the archived probe harness incorrectly; rerunning the repository's actual harness with its required root argument passed. The first DOM rerun then exposed a stale “newest log entry” assumption; the assertion was narrowed to the full log plus the readiness entry and passed on rerun. Neither correction changed educational data.

## Next

Run the required fresh rendered desktop/mobile QA. If it passes, rerun the complete validator set, create a release manifest binding the final GitHub commit, Site source, saved version and deployment, and only then decide whether to create the immutable v0.1 tag.

## Publication

The readiness checkpoint published successfully as public Site version 18 at `2026-10-02T00:02:40.640959+00:00` (October 1, 2026 in New York). Research commit `5c7df5641ec6a77deef56ef9a0a9c7bc8de5adca`; Site source `acac5d5efe27327a91e72e075c47f0ada8d5e579`; deployment `appgdep_6abef49b4c148191bf0b5a7eccd64bcb`. The public audience was preserved. Exact native record: `data/publications/friday-freeze-readiness.json`.

Publication confirms availability, not a new review verdict and not the missing rendered QA. The receipt is a post-deployment record and is not represented as content of the already deployed version 18 bundle.
