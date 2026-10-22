# BiRebus

## Seeing Sounds, Missing Meanings
### A Chinese–English Bilingual Benchmark for Visual Homophone Reasoning

**Peijin Xie · Jiayi Zhao · Xiaoxue Wang · Zhen Xu · Baoxun Wang · Bingquan Liu**

Harbin Institute of Technology, ITNLP Lab · Tencent, Platform and Content Group, QQAI

[🚀 Project website](https://xiepeijinhit-hue.github.io/rebus/) · [📄 Paper](paper.pdf) · [🧩 Data explorer](https://xiepeijinhit-hue.github.io/rebus/#explore) · [Method](docs/METHOD.md) · [Results](docs/RESULTS.md) · [Data audit](docs/DATA_AUDIT.md) · [Release checklist](docs/RELEASE_CHECKLIST.md)

> **Release status: partial diagnostic snapshot.** This repository contains 400 available diagnostic samples, not the approximately 1,600 task instances described in the manuscript. The exact correspondence to the paper's human-reviewed split, data redistribution rights, and experimental reproducibility require author confirmation. See the audit before citing results or redistributing data.

## What is BiRebus?

Visual homophone rebuses encode expressions through objects, attributes, counts, actions and relations whose names evoke similar-sounding words. A solver must connect **what it sees** with **how it names and pronounces the clues**, then compose a valid expression. This differs from literal image captioning.

The paper contributes:

1. **A bilingual, two-format benchmark:** English and Chinese, emoji/symbol sequences and open-ended pictorial scenes.
2. **An agent–human construction workflow:** public-content collection or homophone decomposition, visual planning, image synthesis, iterative verification and human review.
3. **Structured Rebus Reasoning:** visual grounding → phonological imagination → composition and verification, without parameter updates or additional training data.

The paper reports approximately 1,600 task instances, a balanced 400-example diagnostic split, a strongest direct-prompting VLM score of 58%, a human score of 63%, and aggregate improvement from 48% to 56%. **These are manuscript-reported claims, not independently reproduced numbers.** [Results and discrepancies](docs/RESULTS.md) separate them from the available local evidence.

## Available data

| Configuration | Paper shorthand | Answer language | Input | Released rows | Images |
|---|---|---|---|---:|---:|
| `en_emoji` | En-E | English | Emoji/symbol sequence | 100 | 0 |
| `en_image` | En-P | English | Ordered figure 1 + figure 2, optional figure 1 hint | 100 | 200 |
| `zh_emoji` | Zh-E | Chinese | Emoji/characters → idiom | 100 | 0 |
| `zh_image` | Zh-P | Chinese | Single picture → expression | 100 | 100 |
| **Total** | | | | **400** | **300** |

Only a `test` split is packaged. IDs are namespaced (`en_image_1`, `zh_image_000002`); leading zeros are preserved. English emoji and pictorial tasks may share source IDs and answers; do not split them randomly into train/test and assume independence.

- `data/*.json`: sanitized annotations for every released sample. Pictorial inputs do **not** include their source emoji, explanations or model predictions.
- `assets/previews/`: metadata-stripped, maximum-960-pixel WebP **display previews**, not lossless evaluation images.
- `data/release.json`: counts, source checksums, artifact checksums and release status.
- `data/image_manifest.json`: per-image source checksum, released PNG checksum and preview mapping.
- The separately prepared **Hugging Face directory** contains the same 400 rows with full-resolution, metadata-stripped lossless PNG bytes embedded in Parquet. It is the image-bearing evaluation package. Its future repository identifier is intentionally not guessed here.

No user names, answer-session logs, editor identities, credentials, internal endpoints, caches or raw model reasoning traces are included. Reference answers are preserved, not silently corrected. Their correctness and clue quality are not newly human-verified.

## Browse locally

No Node build, cloud account, model API or server dependencies are needed. From this repository:

```bash
python3 -m http.server 3010 --bind 127.0.0.1
```

Open `http://localhost:3010/`, or visit the [🚀 project website](https://xiepeijinhit-hue.github.io/rebus/). The project page includes an emoji wordplay demo, paper and author information, the three-stage method, result charts with separate manuscript/audit views, and copyable citation metadata. The data explorer supports all four subsets, clue/ID search, image-count filters, pagination, image zoom, per-card answer reveal and filtered JSON download.

The page is read-only and collects no responses. Answers are present in downloadable JSON; the reveal button is a convenience, **not secure exam protection**. Do not use preview images for benchmark scores. GitHub Pages serves the repository root from `main`; `.nojekyll` preserves the static assets unchanged, and relative paths support `/rebus/`. Future pushes to `main` update the site automatically. Publishing the page does not resolve the rights or experimental limitations documented in the release checklist.

## Load and score data

JSON annotations require only Python's standard library:

```python
import json
from pathlib import Path
rows = json.loads(Path("data/en_emoji.json").read_text(encoding="utf-8"))
print(rows[0]["uid"], rows[0]["emoji"], rows[0]["answer"])
```

For full-resolution image loading, see the Hugging Face data card. The offline scorer accepts a JSONL file with one `uid`, `prediction`, and `status` (`ok` or an error label) per item:

```bash
python3 tools/score.py --data-dir data --predictions predictions.jsonl --output scores.json
```

It reports reference-normalized strict accuracy over **all expected items** and success-conditioned accuracy separately. Missing, empty and failed outputs receive no end-to-end credit. Duplicate/unknown IDs are rejected. It does not call a model or read credentials.

## Method and evidence

- [METHOD.md](docs/METHOD.md): paper construction workflow, structured prompt templates, historical implementation caveats.
- [RESULTS.md](docs/RESULTS.md): paper tables, fixed-denominator local checks and interpretation limits.
- [DATA_AUDIT.md](docs/DATA_AUDIT.md): the historical selector labeled many empty outputs as errors. **374/400** released rows originated from empty screening responses; this is not evidence of 374 genuine reasoning failures.
- `results/paper_tables.json`: transcription of Tables 1–3, clearly labeled paper-reported.
- `results/local_audit.json`: offline recomputation with coverage, same-ID paired comparisons, source hashes and no raw reasoning text.

The public helpers are not a claim that the full collection/planning/critic agent pipeline is implemented here. Private-endpoint scripts and unsafe editable services from the development workspace are intentionally excluded. No new model calls were made to prepare this release.

## Build / verify a release

Python 3.9+ is supported; Python 3.10+ with a modern OpenSSL build is recommended.

```bash
python3 -m pip install -r requirements.txt
python3 tools/validate_release.py --github-dir . --hf-dir ../huggingface
```

The packager is an offline maintainer tool that needs the original workspace, not a downloader. To reproduce the data artifacts into **fresh** directories:

```bash
python3 tools/build_release.py --source-root /path/to/original-workspace --github-dir /path/to/fresh-github --hf-dir /path/to/fresh-huggingface
```

It packages the frozen `benchmark_100`, strips image metadata, audits historical results and refuses to overwrite an existing release manifest. It does not regenerate site source, docs or a missing paper. Original annotations are never changed.

## Citation and rights

Use [CITATION.cff](CITATION.cff) for the manuscript title and authors. No DOI, conference, publication date or Hugging Face URL has been fabricated. The repository URL printed in the manuscript is `https://github.com/xiepeijinhit-hue/rebus`; its remote publication status has not been checked.

**No blanket data license is asserted.** A development package's MIT declaration is insufficient to license collected images, emoji renderings, generated images or the paper. Review [RIGHTS.md](docs/RIGHTS.md) and [RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md) before public upload. This package is structurally prepared, not a legal clearance certificate.
