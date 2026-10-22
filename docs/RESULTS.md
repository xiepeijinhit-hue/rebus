# Results: manuscript claims and local evidence

**Do not merge the following tables.** Section A transcribes the supplied paper. Section B is a new offline audit of stored extracted predictions for this local snapshot, not a new model run. Differences in denominators, request budgets, parsing and coverage prevent treating these as identical experiments.

## A. Paper-reported results

Source: `paper.pdf`, pp. 3–4, Tables 1–3. Values below are rounded integers **as printed**, not recalculated from rounded columns. Model labels follow the paper and do not independently verify provider/version identity.

| Model | English Emoji | English Pictorial | Chinese Idiom | Chinese Pictorial | Overall |
|---|---:|---:|---:|---:|---:|
| Human (Direct) | 67 | 52 | 85 | 48 | 63 |
| GPT-6-Astra (Direct) | 43 | 46 | 74 | 68 | 58 |
| Gemini-3.8-F (Direct) | 32 | 42 | 57 | 59 | 48 |
| GPT-5.6-Sol (Direct) | 30 | 34 | 67 | 49 | 45 |
| DeepSeek-V4-V (Direct) | 27 | 27 | 69 | 49 | 43 |

| Strategy, aggregate reported in Table 2 | English Emoji | English Pictorial | Chinese Idiom | Chinese Pictorial | Overall |
|---|---:|---:|---:|---:|---:|
| Direct | 33 | 37 | 67 | 56 | 48 |
| VG + PI | 41 | 48 | 74 | 63 | 56 |
| Reported gain (pp) | +8 | +11 | +7 | +7 | +8 |

Table 3 reports Direct / VG / VG+PI overall scores of 58 / 65 / 70 for GPT-6-Astra and 45 / 55 / 61 for GPT-5.6-Sol. The paper also reports a stage-wise error analysis and a concept-assisted experiment. Full human responses and individual earliest-failure annotations were not located. We neither invent them nor infer them from local quiz logs.

`results/paper_tables.json` contains the transcription, including the per-model structured scores.

## B. Local audit: fixed expected-item denominator

Each model has 100 expected questions per subset and 400 overall. Only `status=ok` **and nonempty** predictions are valid responses. Strict matches are recomputed from the stored `prediction` field using the historical normalizer. A failed, empty or missing response receives no end-to-end credit. This is a pipeline score under historical conditions, not a statement that the model semantically answered every failure incorrectly.

| Local model label | Direct correct / 400 | VG+PI correct / 400 | Direct % | VG+PI % | Delta (pp) | Valid responses, before / after |
|---|---:|---:|---:|---:|---:|---:|
| `gpt-6-astra` | 230 | 246 | 57.50 | 61.50 | +4.00 | 399 / 351 |
| `gemini-3.8-flash` | 189 | 185 | 47.25 | 46.25 | -1.00 | 399 / 399 |
| `gpt-5.6-sol` | 178 | 209 | 44.50 | 52.25 | +7.75 | 397 / 342 |
| `deepseek-v4-flash-vision-official` | 170 | 183 | 42.50 | 45.75 | +3.25 | 397 / 383 |

With four models and equal 100-item subsets, the per-subset means are:

| Subset | Direct % (fixed denominator) | VG+PI % (fixed denominator) | Delta (pp) |
|---|---:|---:|---:|
| English Emoji | 32.75 | 35.50 | +2.75 |
| English Pictorial | 37.25 | 44.75 | +7.50 |
| Chinese Idiom | 66.00 | 66.25 | +0.25 |
| Chinese Pictorial | 55.75 | 59.25 | +3.50 |
| Overall across 1,600 model–question pairs | 47.9375 | 51.4375 | +3.50 |

For comparison only, pooling **successful nonempty responses** gives 767/1592 = 48.18% before and 823/1475 = 55.80% after. These denominators differ. The historical “average of model-level rates” is another aggregation again. None of these should be silently substituted for the fixed-100 protocol stated in the manuscript.

## C. Same-ID paired diagnostic

`results/local_audit.json` includes 16 Direct/VG+PI pairs (four models × four subsets), using only IDs where both conditions produced a successful, nonempty output. It records:

- `common_valid` and the explicit shared source IDs;
- before/after correct counts and percentages;
- wrong→right and right→wrong counts;
- source-file SHA-256 checksums.

Example: GPT-6-Astra on English Emoji has 80 shared valid IDs. Direct is 41/80 = 51.25%, VG+PI is 46/80 = 57.50%, a paired change of **+6.25 pp**, not the unpaired 43.0→57.5 = +14.5 pp. Paired filtering itself selects a success subset; it does not establish a causal effect.

## Interpretation limits

1. **Split provenance:** 374/400 screening predictions were empty. The local set is not certified as 400 genuine screening-model mistakes or as the paper's reviewed split.
2. **Configuration changes:** budgets, temperatures, retries and output extraction changed across historical runs; complete request metadata are unavailable.
3. **Example contamination:** historical prompts included benchmark answers. The clean method template in this repository removes those examples but has not been evaluated.
4. **Oracle labels:** Unicode names and generation descriptions are not independently validated gold visual concepts. Do not use them to prove a perceptual upper bound.
5. **Human comparison:** manuscript-only; no reproducible human baseline is released.
6. **Generalization:** this is a selected diagnostic snapshot. No claim of significance, random-sample performance, model superiority across populations, or pure VG/PI causal attribution is warranted.

The audit makes these issues inspectable; it does not amend the paper or replace a controlled rerun with fixed settings, disjoint examples, complete coverage and independently verified references.
