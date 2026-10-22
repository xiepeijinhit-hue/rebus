# Method: Structured Rebus Reasoning

## Paper overview

**Source:** `paper.pdf`, Sections 1–3, Figures 1–4. BiRebus studies Chinese–English visual homophone reasoning across constrained emoji sequences and open-ended pictorial scenes. Recognizing an object is not sufficient: a solver must select a useful lexical name, activate the intended pronunciation, and compose an expression.

Chinese puzzles can involve character-level homophones, near-homophones and idioms. English puzzles can involve alternate object names, syllable segmentation, blending and phrases. Spatial relations, counts, attributes and actions can matter in either language. Not every puzzle is exclusively phonetic; a solver should not discard literal or spatial clues.

## Construction workflow described by the paper

1. **Collection:** retrieve public rebuses, retain their original language, deduplicate, filter advertisements and answer leakage, and review critical clues.
2. **Planning:** decompose a target expression into depictable homophonic or near-homophonic units; choose symbols or a scene layout.
3. **Synthesis:** construct an emoji sequence or invoke an image model for a cartoon/pixel-art scene. The paper names GPT-Image-2.
4. **Generate–criticize–revise:** check clue visibility, unintended objects/text, sound correspondence and solvability; revise low-quality candidates.
5. **Human review:** correct annotations, regenerate images or reject samples.

The workspace contains annotation, image generation, retry and review utilities. It does not provide a fully reproducible end-to-end implementation of every collection/planning/verification agent described above. Those private-environment utilities are not bundled. The release contains neither full provenance for upstream social-media sources nor a complete human-review trail.

## Three-stage inference instruction

This is a **clean method-level template** based on the supplied manuscript, not the exact historical request log. It deliberately includes no benchmark answer examples.

> **1. Visual grounding:** Identify only essential objects, attributes, counts, actions, text and spatial relations. Avoid unsupported details and narrative descriptions.
>
> **2. Phonological imagination:** Consider alternative names and pronunciations for each clue. Search for homophones and near-homophones in the target language; retain non-phonetic spatial or literal clues when relevant.
>
> **3. Composition and verification:** Compose candidate expressions and select one that accounts for the critical visual clues. Return only the final answer in the requested format.

### English symbolic / pictorial task

Provide either the emoji sequence, or the two ordered images with the optional figure 1 hint. Ask for the expression represented by the symbols or figure 2, in English. Do not insist on a single orthographic word: some references are multiword expressions. Do not supply ground-truth explanations or a reference emoji sequence for pictorial questions.

### 中文任务模板

> 1. 视觉定位：识别关键物体、属性、数量、动作、文字及空间关系，不补充画面外的情节。
> 2. 谐音想象：考虑线索的其他叫法、同音字和近音字，并保留有用的字面意象和空间关系，不强行给所有线索套用谐音。
> 3. 组合与验证：选择能解释全部关键线索的中文词语或成语，只输出最终答案。

For future structured runs, a final `ANSWER: <expression>` marker can simplify parsing. Apply the same parsing rule and sufficient, fixed output budget across comparison conditions. Record the exact prompt, model identifier, temperature, budget, timeout, finish reason, usage and retry policy for each run. Do not reuse historical aggregate percentages as measurements of this cleaned template.

## Ablations and concept assistance

- **Direct:** task + input → answer, without the stage instruction.
- **VG:** explicitly extract relevant clues before predicting the answer.
- **VG + PI:** add alternate lexicalizations, pronunciation search and verification.
- **Concept-assisted diagnostic:** supply independently checked visual concepts. This is not necessarily an upper bound and must be compared on the same models and IDs.

Historical local `oracle` outputs are **not a verified oracle**. English emoji concepts were constructed from Unicode character names, which do not reliably capture multi-codepoint emoji or culturally relevant names. English image descriptions were annotation/generation descriptions, not proven independent perception labels. Images were still sent to the model. Chinese concept assistance was unavailable. Therefore no fresh human-verified concept labels are included in this release.

## Differences from the historical implementation

The local structured prompts contained an English `leg + end → legend` example and a questionable Chinese example ending in `七嘴八舌`; these answers overlap the local diagnostic set. Historical system prompts for VG also mentioned phonological reasoning, so VG versus VG+PI was not a clean removal of all PI instructions. Budgets and output extraction changed across runs. These are confounds, not additional evidence for a causal improvement. No additional training occurred during this release preparation.
