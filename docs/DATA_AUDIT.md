# Release audit and data provenance

## Scope

This package preserves the existing `benchmark_100` IDs and references. It is a **400-item local diagnostic snapshot** with all four subsets present. It does not claim to reproduce the complete ~1,600-instance resource or certify equivalence to the manuscript's reviewed split. Nothing was added to make counts look complete.

| Subset | Historical candidate pool | Released rows | Released images | Screening prediction empty |
|---|---:|---:|---:|---:|
| English emoji | 594 | 100 | 0 | 95 |
| English pictorial | 142 | 100 | 200 | 85 |
| Chinese emoji-idiom | 267 | 100 | 0 | 95 |
| Chinese pictorial | 628 | 100 | 100 | 99 |
| **Total task instances** | **1,631** | **400** | **300** | **374** |

Candidate counts are historical pool counts from `benchmark_100/summary.json`, not a claim that 1,631 independent puzzles are packaged. The English tasks share an annotation pool. The original Chinese emoji source configured in development lived outside this workspace; the 100 selected rows are locally available and sufficient for this partial export. Full external sources were not copied.

## Selection issue

The historical selection procedure prioritized a screening model's errors. However, **374 of the 400 selected items have empty screening predictions**. Earlier code recorded empty model outputs as successful API calls and strict mismatches. Empty outputs can reflect truncation, format handling or an API problem; they do not establish an incorrect semantic answer.

Public rows therefore record `selection_status` as `empty_response`, `nonempty_incorrect` or `nonempty_correct`, not the unsupported label “verified hard example.” The remaining 26 are nonempty mismatches under the historical criterion, not newly adjudicated reasoning failures. The package retains these 400 samples rather than silently selecting a new benchmark and pretending historical results still apply.

The paper instead describes quality-reviewed, contrastive diagnostic selection. Independent evidence connecting the local selection process to that described split was not found. Authors should reconcile the two before presenting this snapshot as the final paper split.

## References and identity

- `uid` combines subset and original ID; `source_id` preserves leading zeros.
- `emoji` holds the symbolic task input only; `hint` is the permitted figure 1 hint for English pictorial questions.
- `answer` is inherited verbatim. It may admit aliases, spelling differences or ambiguous interpretations; none were guessed or automatically repaired.
- `reference_review` is `inherited_unverified`. File integrity checking is not human semantic validation.
- Per-sample source-model output, human names, review notes, editor metadata and timestamps are excluded.
- Source files and lossless release image bytes have SHA-256 mappings in the manifests.

## Image processing

All 300 referenced source files were required to exist and pass image decoding checks. Images are auto-oriented from EXIF when present and re-encoded as PNG at their original displayed resolution with metadata stripped. Raw encoded bytes may therefore differ from the source; decoded display pixels are preserved. GitHub WebP previews are downsampled to at most 960×960 and lossy. HF Parquet contains the PNG bytes, not links to the private machine.

This removes file metadata, **not text or personal content visibly embedded in pixels**. Visual rights/privacy review is still required. Emoji rendering in the website is platform-dependent; the underlying Unicode sequences are preserved.

## Evidence and statistical caution

- Manuscript Tables 1–3 are transcribed separately in `results/paper_tables.json`.
- `results/local_audit.json` recomputes strict scores from stored extracted predictions after excluding blank outputs from the valid subset; expected sample counts remain fixed for the all-item score.
- Historical data include changing token budgets, automatic parameter selection, retries and incomplete coverage. Neither passing an 80% completeness threshold nor filtering to successful requests guarantees comparability.
- Same-ID paired comparisons reduce denominator mismatch but do not remove model-run/configuration confounds or survivorship bias.
- The 48→56 manuscript statement and the previous `+8.2` result use historical aggregation choices. Do not infer significance or causal gains from them alone.
- Human accuracy and earliest-failure labels for the manuscript's Figure 4 cannot be independently reconstructed from the included artifacts. Small local quiz-session logs are not a substitute and are deliberately withheld.
- Unicode-name assistance is not a human oracle. Different model sets cannot be compared as though they were the same ablation cohort.

## Exclusions

Not included: raw data ZIPs, original larger pools, images without a selected reference, trash/rejected image folders, private API runners, credentials, internal addresses, API logs, model reasoning traces, user-session data, caches, and unverifiable per-example human labels. The paper PDF itself is preserved unchanged; its authorship and embedded examples are part of the author-supplied document.

## Before public release

Confirm redistribution rights for the paper, collected pictures, artificial images and any third-party renderings; reconcile selection and denominator definitions; review reference answers and prompt-example overlap; record the exact public revision of the split. No license or complete reproducibility claim should be added until these checks are satisfied.
