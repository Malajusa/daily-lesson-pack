# T3W6 Thursday Literacy Regression Record

## Status

**Classroom-feedback regression benchmark.**

The 27 August 2026 Literacy warm-up exposed failures that were not prevented by the earlier generation and QA contracts. Use these cases whenever Literacy wording, reminder architecture, correction emphasis or technical terminology changes.

Corrected reference artefact:

- file name: `2026-08-27_T3W6_Thursday_Daily-Teaching-Slides.pptx`
- slide count: **79**
- SHA-256: `2defcc639b095cc71fc7644a39644e3d730fcbfa546a6abdf5cbfd6984c35b3a`

The PPTX remains an external regression artefact and is not bundled with the skill.

## Known failures that must not recur

- A sentence-combination task instructed students only to `write a sentence` instead of stating the required operation.
- Reminder rules were not consistently presented as concise applicable statements inside the yellow reminder panel.
- Punctuation placement was described in prose when the example should have shown the punctuation more clearly.
- Source formatting requested enlarged coloured punctuation, but an exported render flattened the run styling.
- Literal words discussed as language, including `because`, appeared without inverted commas.
- The grammatical term `conjunction` was replaced by the vague label `linking word`.
- A one-word replacement answer silently removed additional words from the source sentence.
- A multiple-choice answer introduced wording that was not present in the selected option.
- A defined technical word appeared without inverted commas on an answer slide.
- Automated checks passed while rendered text sat too close to panel borders.

## Required acceptance characteristics

- The question title and instruction state `Combine the two sentences using the conjunction “because”` or an equally exact operation.
- The reminder yellow panel states an applicable rule such as `Remember: Commas separate items in a list.`
- The reminder example displays the target punctuation in green, bold text at least 125% of the surrounding size.
- An answer that adds punctuation shows the complete corrected sentence and makes each inserted mark green, bold and at least 125% of the surrounding size.
- A textual cue identifies the correction without relying on colour alone.
- A word or phrase named as language uses typographic inverted commas.
- Accurate curriculum terms such as `conjunction`, `pronoun`, `clause`, `preposition`, `prefix` and `suffix` are retained and explained rather than replaced by vague labels.
- Each question requires one direct response; the answer slide, not the student prompt, provides the concise explanation.
- An answer performs only the operation requested. A replacement task preserves every unrequested word, and a selected option is reproduced exactly unless an additional edit is explicitly required.
- The exported full-size render visibly preserves every required emphasis.
- Full-size render review confirms comfortable internal panel padding even when deterministic containment checks pass.

## Deterministic regression expectations

`scripts/audit_pack_contract.py` must fail a Literacy warm-up that:

- uses `linking word` as a label;
- uses an obvious unquoted metalinguistic pattern such as `use because`;
- contains a two-sentence `because` task with `write a sentence` but no `combine` or `join` instruction;
- lacks a `Remember:` statement on a reminder slide;
- claims punctuation was added but contains no green, bold, enlarged punctuation run.

Deterministic checks do not replace full-size rendered inspection or semantic comparison of the requested action and answer.
