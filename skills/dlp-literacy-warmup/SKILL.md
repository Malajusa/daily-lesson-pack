---
name: dlp-literacy-warmup
description: Generate self-contained reminder, question and answer sequences for the Daily Lesson Pack Literacy warm-up.
---

# DLP Literacy Warm-up

## Ownership

Own the Literacy warm-up only. Keep it separate from Morning Work, Shared Reading, Guided Reading, spelling instruction and the main writing lesson.

## Mandatory year-level context

Before generation, read `references/year-level-context-contract.md` and the active year-level profile supplied by the orchestrator.

The active profile controls language load, expected prior knowledge, misconception plausibility, terminology support and appropriate response demand. Do not use Year 4/5-specific calibration for a Year 6 run, or vice versa, unless an explicit shared rule is identified as universal.

## Length and sequence

Create exactly **10 `Reminder -> Question -> Answer` sequences** (30 slides) unless the user explicitly changes the count.

For every sequence:

1. The reminder slide briefly teaches or retrieves the rule needed for the task.
2. The question slide immediately follows the reminder.
3. The answer slide immediately follows and matches only that question.

The reminder should usually take about 15-30 seconds. The question should usually take about 20-45 seconds and produce visible student thinking, speaking or writing.

## Response load

Require exactly **one student action and one response** on each question slide unless the user explicitly requests reasoning in the warm-up or the active year-level profile explicitly defines another warm-up response contract.

- Do not ask students to answer and then explain, justify, give a reason, name supporting evidence or complete another action.
- For a choice question, ask students only to select or write the option. Put any concise rationale on the following answer slide.
- Keep the response brief enough for rapid retrieval. Move sustained reasoning or discussion to the main lesson.
- Do not treat an instruction such as `Write A or B and explain why` as one task. It contains two student actions and must be simplified.

## Self-contained questions

Every question must be achievable without remembering another warm-up slide.

- Put every sentence, word, fact, option or context needed to answer on the question slide itself.
- Do not use an omitted previous sentence, an earlier example or a fact shown only on the reminder slide as required question data.
- A cohesion question must include both ideas being linked, not only a sentence beginning with a blank connective.
- A pronoun question must display the complete sentence containing the noun and pronoun.
- The reminder may explain the method, but the question must remain independently readable.
- Use a different example on the reminder so it supports the method without revealing the question's answer.

## Reminder slides

Use direct, student-facing language. State the useful rule, not a broad teacher definition.

For example, when teaching a simple list without an Oxford comma, a reminder could say:

`Remember: Commas separate items in a list.`

Place the concise applicable `Remember:` rule inside the yellow reminder panel. Put a separate short example beneath it when a model helps. Prefer showing the relevant punctuation clearly in the example over adding a long sentence that explains each insertion position.

When the reminder teaches punctuation, format the target punctuation in its example in green, bold text at least 125% of the surrounding text size. Keep the punctuation in its normal sentence position.

## Task-operation fidelity

Name the exact operation students must perform. Match the question title, instruction and expected answer.

- Say `Combine the two sentences using the conjunction “because”`, not `Write a sentence`.
- Say `Add the missing commas and write the complete sentence` when students must add commas.
- Say `Replace “went” with a more precise verb` when students must replace a word.
- Do not use `write`, `fix` or `improve` alone when the intended transformation is more specific.

The answer must perform exactly the named operation without silently adding another demand.

## Rule and answer consistency

Keep the reminder, model, question and answer within one consistent rule or convention.

- Do not state a rule that contradicts the displayed example or corrected answer.
- For list commas, do not say `place a comma after each item except the last` when the model omits the optional comma before `and` or `or`.
- If deliberately teaching an Oxford comma or another accepted convention, name that choice and use it consistently in the model, question and answer.
- Check that the answer performs exactly the operation requested and that its explanation describes the punctuation or language actually shown.

## Content

Use high-leverage literacy retrieval and language work such as:

- vocabulary and morphology for meaning;
- punctuation;
- sentence construction and improvement;
- parts of speech where useful;
- cohesion and reference;
- fact, opinion and evidence;
- text-feature recognition;
- current writing-genre language and structure where supported by the user's overview.

Do not turn morphology into a Sound Waves-style spelling drill. Exclude spelling lists, phonics, grapheme/sound drills, dictated words and Sound Waves replacement content unless a future active profile explicitly owns a different early-years literacy contract.

## Multiple-choice quality

Use multiple choice only when every distractor is credible enough to test the target distinction.

- Keep options grammatically parallel and reasonably similar in length, detail and tone.
- Base distractors on a plausible misconception or incomplete understanding for the **active year-level profile**.
- Do not pair the correct answer with a joke, vague throwaway, subjective claim or option that can be rejected without applying the reminder.
- If a credible distractor cannot be written, replace the item with a direct production, correction, matching or selection task.
- Ask only for the selected option. Explain the distinction on the answer slide rather than requiring students to justify their selection.

## Precision and teacher explainability

Do not label a replacement `more precise` merely because it is more formal, technical or less familiar.

Use a precision comparison only when the original wording is genuinely broad in context, the replacement adds one defensible semantic feature while preserving the core meaning, and the distinction can be explained accurately in one short prepared sentence.

Reject comparisons that create a reasonable synonym debate. In particular, do not present `rotate` as automatically more precise than `turn`; both can accurately describe a propeller's movement. Teach a technical term through a clear definition when appropriate without manufacturing a precision hierarchy.

Supply the defensible explanation on the answer slide or in teacher notes. Do not require the teacher to invent a semantic defence during the lesson.

## Student-facing language

Questions must be immediately understandable to an average student within the active year-level profile.

- Use a concrete classroom action such as `add`, `choose`, `write`, `replace`, `join`, `explain` or `find`.
- Prefer familiar terms such as `topic sentence` over unexplained teacher terminology such as `classification opening`.
- If a technical term is the learning target, explain it on the reminder slide and restate enough meaning on the question slide for the task to stand alone.
- Increase thinking demand without increasing ambiguity or adult-sounding language.

## Technical terminology and inverted commas

Use the accurate grammatical or literacy term, then explain it plainly. Do not replace a known term with a vague substitute.

- Use `conjunction`, not `linking word`, when naming words such as `and`, `but` or `because` by grammatical function.
- Use `subordinating conjunction` when that distinction is the learning focus; otherwise use the level of grammatical precision required by the active profile without replacing an accurate term with a vague substitute.
- Retain accurate terms such as `pronoun`, `clause`, `preposition`, `prefix`, `suffix` and `topic sentence` when they apply.

Put typographic inverted commas around a literal word or phrase when discussing it as language: `Use the conjunction “because”` and `Which noun does “its” refer to?` Do not add inverted commas when the word is simply operating inside an example sentence: `The soil stays damp because the forest is humid.`

## Answer slides

- Put the complete primary answer in bold, visually dominant text.
- Make every changed or inserted element immediately visible.
- For punctuation corrections, show the complete corrected sentence and format inserted punctuation in green, bold text at least 125% of the surrounding text size.
- For word or phrase replacements, show the changed wording in green and bold where that makes the correction easier to locate.
- Add a plain-language cue such as `Added commas:` or `Changed word:` so the correction does not rely on colour alone.
- Explain the relevant rule or meaning specifically. Do not use generic text such as `the answer matches the prompt`.
- Keep this explanation teacher/class-facing; do not turn it into a second student response requirement on the preceding question slide.
- Do not shrink meaningful explanations into fine print.
- Treat the exported render as the evidence of emphasis. Source code that requests green, bold or enlarged punctuation does not pass when the rendered punctuation is flattened or visually indistinguishable.

## Presentation

- Use Trebuchet MS for the established warm-up system.
- Main reminder, question and answer content is normally at least 36 pt and should grow when space allows.
- Use the largest sensible type rather than preserving empty decorative space.
- Keep all text fully within its coloured, shaded or bordered container with deliberate internal padding.
- No generic footer telling students to use whiteboards; that routine is supplied by runtime classroom context when relevant.

## QA

Fail if:

- the active year-level profile is missing, unresolved or inconsistent with the orchestrator;
- a question uses another year profile's assumptions without explicit authorisation;
- the sequence is not `Reminder -> Question -> Answer`;
- a question depends on remembered or unavailable content;
- a reminder reveals the exact answer rather than teaching the method;
- a reminder lacks a concise applicable `Remember:` rule inside its yellow panel;
- a punctuation reminder fails to highlight the target punctuation in its separate example;
- student language is ambiguous, adult-facing or inappropriate for the active profile;
- a question adds an `explain why`, `explain how you know` or `justify` demand to the direct response contrary to the active warm-up contract;
- a question requires more than one student action or response contrary to the active warm-up contract;
- a question title or instruction does not name the exact operation required by the answer;
- a sentence-combination task merely says `write a sentence`;
- an accurate technical term is replaced by a vague label such as `linking word` for `conjunction`;
- a word or phrase discussed as language lacks inverted commas;
- spelling instruction has crept in without an authorised profile contract;
- a multiple-choice distractor is implausible, structurally unmatched or obviously wrong without applying the target rule;
- a claimed precision distinction changes meaning, is reasonably debatable or lacks a prepared defensible explanation;
- an answer does not immediately follow its question;
- a reminder, model, question and answer use conflicting rules or conventions;
- a correction is difficult to locate;
- inserted punctuation is not visibly green, bold and at least 125% of the surrounding size in the exported render;
- an explanation is generic rather than teaching the relevant rule;
- content is undersized or escapes its intended panel.
