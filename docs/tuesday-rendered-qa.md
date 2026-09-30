# Tuesday desktop/mobile QA

Reviewed September 30, 2026. **PASS for desktop/mobile responsive QA; broader accessibility verification remains partial.** No release-blocking layout or interaction defects found in the exercised paths. No product code or ontology changes were needed.

## Reviewed state and method

Site source c23aca87d9651843cd88e3e6c35903e103b23d6e, matching the v0.0.6 research checkpoint and public Site version 10. The unchanged dist application was rendered through a managed Vite preview in cloud Chromium. Added development-only Vite configuration and a reusable responsive harness; neither changes production application assets.

The browser API did not expose viewport resizing. Mobile and tablet checks therefore used same-origin iframe viewports, not physical devices or touch emulation. The harness used the original application without CSS overrides. Screenshots were inspected after render settled.

| Check | Result |
| --- | --- |
| Desktop 1363 × 936 | All eight views opened; document scroll width equals client width, 1348 px. |
| Mobile 320 × 740 | All eight views opened; document scroll width equals client width, 305 px. |
| Mobile 390 × 844 | Atlas, expanded graph and navigation rendered correctly. |
| Tablet 768 × 860 | Atlas sidebar, cards and text reflowed; no document overflow (753 px). |
| Receipt | ELA Receipt opened by Enter; close control received focus; Escape closed and restored object focus. Desktop expansion worked. Mobile source text and links wrapped inside the panel. |
| Student lens | ELA Receipt navigated to and highlighted the ELA object in Grade 7. Matthew and Eva exposed identical 13 object cards. |
| Graph | Expansion produced 15 nodes; keyboard activation opened a Receipt and Escape restored graph-button focus. Horizontal scrolling stayed within graph region. |
| Workbench | Content-area expansion reported aria-expanded=true; wide matrix remained inside its own scrolling region. |
| Enlarged layout | 674 × 420 iframe rendered at CSS zoom:2; Atlas and Receipt remained readable without internal horizontal overflow. This is a simulation, not native browser zoom. |

## Limits and carry-forward items

Native browser zoom could not be verified: the keyboard shortcut did not change viewport width or device pixel ratio. Physical iOS/Android, Safari/Firefox, touch gestures, screen-reader behavior, and a comprehensive contrast/WCAG audit were not tested. The full earlier desktop/mobile/200%-zoom/accessibility gate must not be recorded as unconditionally closed; its desktop/mobile portion is now complete.

The independent review's nonblocking conditional coverage-text inconsistency remains open: if one subject's claims become ineligible, the student summary still names both subjects. Both are eligible in the reviewed checkpoint. Historical Receipt review wording still describes the original checkpoint; the subsequent separate AI audit is documented separately. Neither issue was silently reclassified as fixed.

The separate AI audit is already complete. Human semantic review, exact edition applicability, and broader corpus coverage remain research limitations, not newly assigned PDF-download work.

## Evidence and reproduction

- [Desktop screenshot](review-assets/tuesday-desktop.jpg)
- [Mobile screenshot](review-assets/tuesday-mobile.jpg)
- Development setup: npm ci; managed sites-preview start from this repository. Copy scripts/qa-harness.html to dist/qa-harness.html temporarily to inspect fixed-width iframe layouts. Remove that temporary copy before packaging. Do not publish the harness.

This report is builder UI QA, separate from the earlier independent AI audit. Production assets were unchanged, so no new deployment was needed.
