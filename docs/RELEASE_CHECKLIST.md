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


## Technical validation

From the GitHub directory, install `requirements.txt` and run `tools/validate_release.py` with both release roots. Read `release_validation.json` for the latest technical findings. The checker verifies row IDs, schema, image hashes/decoding, preview paths, metadata stripping, paired GitHub/HF row consistency and HF config mappings. 


