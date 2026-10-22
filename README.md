<h1 align="center">🧩 BiRebus</h1>

<h2 align="center">
  <a href="https://xiepeijinhit-hue.github.io/rebus/">🚀 Visit the BiRebus Project Website</a>
</h2>
<p align="center">
  <a href="https://xiepeijinhit-hue.github.io/rebus/"><strong>https://xiepeijinhit-hue.github.io/rebus/</strong></a><br>
  <em>Explore the project · Try the puzzles · Browse the data</em>
</p>

<h3 align="center">Seeing Sounds, Missing Meanings</h3>
<p align="center">
  A Chinese–English Bilingual Benchmark for Visual Homophone Reasoning
</p>

<p align="center">
  <a href="https://xiepeijinhit-hue.github.io/rebus/"><img src="https://img.shields.io/badge/Project-Website-7160D6?style=for-the-badge&amp;logo=githubpages&amp;logoColor=white" alt="Project website"></a>
  <a href="paper.pdf"><img src="https://img.shields.io/badge/Paper-PDF-394150?style=for-the-badge&amp;logo=readthedocs&amp;logoColor=white" alt="Read the paper PDF"></a>
  <a href="https://xiepeijinhit-hue.github.io/rebus/#explore"><img src="https://img.shields.io/badge/Data-Explorer-168A72?style=for-the-badge&amp;logo=databricks&amp;logoColor=white" alt="Interactive data explorer"></a>
</p>
<p align="center">
  <a href="#paper-and-data"><img src="https://img.shields.io/badge/Hugging%20Face-Coming%20soon-FFD21E?style=flat-square&amp;logo=huggingface&amp;logoColor=black" alt="Hugging Face dataset — public link coming soon"></a>
  <a href="#paper-and-data"><img src="https://img.shields.io/badge/arXiv-Coming%20soon-B31B1B?style=flat-square&amp;logo=arxiv&amp;logoColor=white" alt="arXiv — identifier not yet confirmed"></a>
  <img src="https://img.shields.io/badge/Samples-400-7160D6?style=flat-square" alt="400 released samples">
  <img src="https://img.shields.io/badge/Subsets-4-168A72?style=flat-square" alt="4 subsets">
  <img src="https://img.shields.io/badge/Languages-EN%20%2F%20ZH-4D7BBC?style=flat-square" alt="English and Chinese">
</p>
<p align="center">
  <a href="#paper-figures">🎨 Paper figures</a> · <a href="#examples">🎮 Examples</a> · <a href="docs/METHOD.md">🧠 Method</a> · <a href="docs/RESULTS.md">📊 Results</a> · <a href="docs/DATA_AUDIT.md">🔎 Data audit</a> · <a href="docs/RELEASE_CHECKLIST.md">📋 Release notes</a>
</p>

<p align="center">
  <a href="https://xiepeijinhit-hue.github.io/rebus/assets/readme/paper-fig1-examples.png"><img src="https://xiepeijinhit-hue.github.io/rebus/assets/readme/paper-fig1-examples.png" width="920" alt="Paper Figure 1: representative English and Chinese emoji and pictorial rebuses"></a>
</p>
<p align="center"><sub>🌏 <strong>Figure 1 · A glimpse of BiRebus.</strong> Symbols, scenes and sound-based wordplay across English and Chinese.<br>Cropped from <a href="paper.pdf#page=1">the manuscript, page 1</a> · Click the image to enlarge.</sub></p>

> 📦 **Partial diagnostic snapshot:** 400 available samples across four subsets, not the approximately 1,600 task instances described in the manuscript. 

## 💡 What is BiRebus?

Visual homophone rebuses encode expressions through objects, attributes, counts, actions and relations whose names evoke similar-sounding words. A solver must connect **what it sees** with **how it names and pronounces the clues**, then compose a valid expression. This differs from literal image captioning.

| | Key idea |
|---|---|
| 🌏 **Bilingual & multimodal** | English and Chinese, emoji/symbol sequences and open-ended pictorial scenes. |
| 🤝 **Agent–human construction** | Public-content collection or homophone decomposition, visual planning, image synthesis, iterative verification and human review. |
| 🧠 **Structured reasoning** | Visual grounding → phonological imagination → composition and verification, without parameter updates or additional training data. |

The paper reports approximately 1,600 task instances, a balanced 400-example diagnostic split, a strongest direct-prompting VLM score of 58%, a human score of 63%, and aggregate improvement from 48% to 56%. **These are manuscript-reported claims, not independently reproduced numbers.** [📊 Results and discrepancies](docs/RESULTS.md) separate them from the available local evidence.

<a id="paper-figures"></a>

## 🎨 The paper at a glance

### 🤝 From visual clues to a bilingual benchmark

<p align="center">
  <a href="https://xiepeijinhit-hue.github.io/rebus/assets/readme/paper-fig2-pipeline.png"><img src="https://xiepeijinhit-hue.github.io/rebus/assets/readme/paper-fig2-pipeline.png" width="820" alt="Paper Figure 2: public-rebus collection and target-expression synthesis, followed by critic-agent checks and human verification"></a>
</p>
<p align="center"><sub><strong>Figure 2 · Construction pipeline.</strong> Collection and synthesis meet iterative verification and human review.<br>Cropped from <a href="paper.pdf#page=2">the manuscript, page 2</a> · Click to enlarge.</sub></p>

### 🧠 See the clues. Imagine the sounds. Verify the answer.

<p align="center">
  <a href="https://xiepeijinhit-hue.github.io/rebus/assets/readme/paper-fig3-reasoning.png"><img src="https://xiepeijinhit-hue.github.io/rebus/assets/readme/paper-fig3-reasoning.png" width="920" alt="Paper Figure 3: visual grounding and phonological imagination turn eye plus scream into ice cream, followed by clue verification"></a>
</p>
<p align="center"><sub><strong>Figure 3 · Structured Rebus Reasoning.</strong> Visual grounding → phonological imagination → composition and verification.<br>Cropped from <a href="paper.pdf#page=3">the manuscript, page 3</a> · Click to enlarge.</sub></p>

These figures illustrate the supplied manuscript; they are not additional benchmark samples or independent verification of the construction pipeline. See [method notes](docs/METHOD.md) for implementation scope and limitations.

---

<a id="examples"></a>

## 🎮 Try a few examples

### 🖼️ English pictorial: what does figure 2 represent?

**Sample:** `en_image_1` · **Figure 1 hint:** `leg start`

> 图一是 **leg start**，图二是什么？

<table>
  <tr><th align="center">FIG 1 · the given clue</th><th align="center">FIG 2 · guess the expression</th></tr>
  <tr>
    <td align="center"><img src="https://xiepeijinhit-hue.github.io/rebus/assets/readme/en_image_1_1.png" width="300" alt="Figure 1: an arrow points to the top of a leg; hint: leg start"></td>
    <td align="center"><img src="https://xiepeijinhit-hue.github.io/rebus/assets/readme/en_image_1_2.png" width="300" alt="Figure 2: the arrow moves to the foot at the end of the leg"></td>
  </tr>
</table>

<details>
<summary>👀 Reveal the reference answer</summary>

**legend** — the second picture points to the **leg end**; reading the clue together suggests *legend*.

</details>

### 💬 Chinese emoji: 猜一个成语

**Sample:** `zh_emoji_9`

<h3 align="center">✋ 🐷 👜 🐇</h3>

<details>
<summary>👀 查看参考答案</summary>

**守株待兔**。Consider alternative names and near-homophones rather than only the literal objects.

</details>

### 🎨 Chinese pictorial: 这张图表示什么？

**Sample:** `zh_image_000002`

<p align="center"><img src="https://xiepeijinhit-hue.github.io/rebus/assets/readme/zh_image_000002_1.png" width="360" alt="Chinese pictorial rebus, sample zh_image_000002"></p>

<details>
<summary>👀 查看参考答案</summary>

**充电宝**

</details>

These examples use the published snapshot's images and inherited references; they are not newly adjudicated labels. Images shown here are display previews.

<p align="center"><a href="https://xiepeijinhit-hue.github.io/rebus/#explore"><strong>🚀 Explore all 400 puzzles on the project website →</strong></a></p>

<a id="paper-and-data"></a>

## 📄 Paper & 🤗 dataset availability

| Resource | Status | Access |
|---|---|---|
| 🚀 Project website | Online | [Open the project page](https://xiepeijinhit-hue.github.io/rebus/) |
| 📄 Manuscript | Available in this repository | [Read the PDF](paper.pdf) |
| <img src="https://img.shields.io/badge/arXiv-B31B1B?style=flat-square&amp;logo=arxiv&amp;logoColor=white" alt="arXiv"> | Identifier / public link not yet confirmed | Use the manuscript PDF for now |
| 🤗 Hugging Face | Full-resolution package prepared locally; not yet published | Public dataset link coming soon; [rights and access notes](docs/RIGHTS.md) |
| 🧩 Snapshot annotations & previews | 400 samples · 4 subsets · 300 images | [Browse data files](data/) · [Interactive explorer](https://xiepeijinhit-hue.github.io/rebus/#explore) |

The Hugging Face and arXiv badges are status indicators, not links to unverified repositories or submissions.

## 🗂️ Available data

| Configuration | Paper shorthand | Answer language | Input | Released rows | Images |
|---|---|---|---|---:|---:|
| `en_emoji` | En-E | English | Emoji/symbol sequence | 100 | 0 |
| `en_image` | En-P | English | Ordered figure 1 + figure 2, optional figure 1 hint | 100 | 200 |
| `zh_emoji` | Zh-E | Chinese | Emoji/characters → idiom | 100 | 0 |
| `zh_image` | Zh-P | Chinese | Single picture → expression | 100 | 100 |
| **Total** | | | | **400** | **300** |

Only a `test` split is packaged. IDs are namespaced (`en_image_1`, `zh_image_000002`); leading zeros are preserved. English emoji and pictorial tasks may share source IDs and answers; do not split them randomly into train/test and assume independence.

- `data/*.json`: sanitized annotations for every released sample. Pictorial inputs do **not** include their source emoji, explanations or model predictions.
- `assets/previews/`: metadata-stripped, maximum-960-pixel WebP **display previews** for the project website, not lossless evaluation images.
- `assets/readme/`: PNG copies of the README examples and high-resolution crops of Figures 1–3 from `paper.pdf`. These are display assets, not extra dataset records or higher-quality evaluation inputs.
- `data/release.json`: counts, source checksums, artifact checksums and release status.
- `data/image_manifest.json`: per-image source checksum, released PNG checksum and preview mapping.
- The separately prepared **Hugging Face directory** contains the same 400 rows with full-resolution, metadata-stripped lossless PNG bytes embedded in Parquet. It is the image-bearing evaluation package. Its future repository identifier is intentionally not guessed here.

No user names, answer-session logs, editor identities, credentials, internal endpoints, caches or raw model reasoning traces are included. Reference answers are preserved, not silently corrected. Their correctness and clue quality are not newly human-verified.

## 🚀 Browse locally

No Node build, cloud account, model API or server dependencies are needed. From this repository:

```bash
python3 -m http.server 3010 --bind 127.0.0.1
```

Open `http://localhost:3010/`, or visit the [🚀 project website](https://xiepeijinhit-hue.github.io/rebus/). The project page includes an emoji wordplay demo, the paper overview, the three-stage method, result charts with separate manuscript/audit views, and copyable citation metadata. The data explorer supports all four subsets, clue/ID search, image-count filters, pagination, image zoom, per-card answer reveal and filtered JSON download.

The page is read-only and collects no responses. Answers are present in downloadable JSON; the reveal button is a convenience, **not secure exam protection**. Do not use preview images for benchmark scores. GitHub Pages serves the repository root from `main`; `.nojekyll` preserves the static assets unchanged, and relative paths support `/rebus/`. Future pushes to `main` update the site automatically. Publishing the page does not resolve the rights or experimental limitations documented in the release checklist.

## 📥 Load and score data

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

## 🧠 Method and evidence

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

## 📚 Citation and rights

Use [CITATION.cff](CITATION.cff) for the manuscript's citation metadata. No DOI, conference, publication date, arXiv identifier or Hugging Face dataset URL is asserted without confirmation. The public repository is [xiepeijinhit-hue/rebus](https://github.com/xiepeijinhit-hue/rebus).

**No blanket data license is asserted.** A development package's MIT declaration is insufficient to license collected images, emoji renderings, generated images or the paper. Review [RIGHTS.md](docs/RIGHTS.md) and [RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md) before public upload. This package is structurally prepared, not a legal clearance certificate.
