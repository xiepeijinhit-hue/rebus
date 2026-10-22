# Publication checklist

## Prepared locally

- [x] Read the supplied five-page BiRebus manuscript and inventory the workspace.
- [x] Preserve the paper; provide citation metadata without an invented venue or DOI.
- [x] Package four available subsets, each with 100 rows; no synthetic filler rows.
- [x] Keep stable namespaced IDs and 300 correctly ordered images.
- [x] Separate downsampled GitHub display previews from HF lossless image payloads.
- [x] Strip image metadata and whitelist public annotation fields.
- [x] Exclude credentials, private endpoints, editable services and participant records.
- [x] Prepare a static relative-path browser and an offline strict scorer.
- [x] Separate paper-reported tables from recomputed local audit data.
- [x] Prepare a four-config Hugging Face data card and embedded-image Parquet files.

## Must be confirmed by the owner before public upload

- [ ] Resolve the discrepancy between the historical empty-response-based selector and the paper's human-reviewed diagnostic split.
- [ ] Verify references, clues, aliases, duplicate source puzzles and image semantics; do not call file validation human review.
- [ ] Reconcile paper percentages, denominators and request configurations with reproducible experiment artifacts.
- [ ] Supply or remove unsupported human-study and stage-error annotation release claims.
- [ ] Confirm paper distribution permission and per-source data/image rights, including image-model terms.
- [ ] Add explicit code/data licenses; none were guessed during packaging.
- [ ] Inspect visible image content for privacy, attribution and rights issues; metadata stripping is not visual redaction.
- [ ] Set the final Hugging Face dataset identifier and cross-link it from the GitHub README after the repository exists.
- [ ] Confirm the repository URL printed in the paper and author list.
- [ ] Review the exact Git staging list. Upload **only** this prepared directory, never the parent workspace containing private credentials and session data.

## Technical validation

From the GitHub directory, install `requirements.txt` and run `tools/validate_release.py` with both release roots. Read `release_validation.json` for the latest technical findings. The checker verifies row IDs, schema, image hashes/decoding, preview paths, metadata stripping, paired GitHub/HF row consistency and HF config mappings. Passing does not certify experimental validity or licensing.

## Repository layout and upload boundary

- GitHub repository root: the contents of `github/`, with `paper.pdf`, README, static site, preview annotations, audit artifacts and tools.
- Hugging Face **dataset repository** root: the contents of `huggingface/`, with its own `README.md`, four `data/<subset>/test-*.parquet` files, release manifests, `.gitattributes`, and loader example.
- HF Parquet assets belong in large-file storage as specified by `.gitattributes`; they must not become ordinary large Git blobs.
- If publishing the browser using GitHub Pages, configure it to serve the repository root. The provided site has no absolute `/assets` URLs or model calls.

No remote repository, branch, commit, tag, upload, deployment or account connection was created as part of this preparation. No personal responses are collected by the demo.
