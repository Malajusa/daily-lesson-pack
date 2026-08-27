# T3W6 Tuesday Component-Standard Regression Record

## Status

**Approved minimum standard for Morning Work, Literacy warm-up and Shared Reading, with explicit content exclusions.**

The revised 25 August 2026 deck establishes the minimum visual architecture, projected readability, sequence structure and answer treatment for these three components. This approval does not make every sentence or task design in the artefact an exemplar. Apply the exclusions below whenever using it as a benchmark.

Reference artefact:

- file name: `2026-08-25_T3W6_Tuesday_Daily-Teaching-Slides.pptx`
- build: `tuesday_w6_rebuilt`
- slide count: **50**
- SHA-256: `d62d25693d14c529958f02bb4bf7ff46bd00e39ac879fdd1684712876328b573`

The PPTX remains an external regression artefact and is not bundled with the skill.

## Approved minimum characteristics

### Morning Work

- Slide 1 is the Morning Work rather than a cover or setup slide.
- Tasks are independent revision that students can complete in their books without pre-teaching.
- Numeracy revises the four operations and vocabulary connected to the current numeracy focus.
- Multiplication uses a two-digit-by-two-digit calculation rather than a single times-table fact.
- Literacy revises familiar grammar and punctuation rather than demanding a paragraph about unfamiliar content.

### Literacy warm-up

- The component contains exactly 10 `Reminder -> Question -> Answer` triads.
- Amber reminders, blue questions and green answers establish a consistent instructional rhythm.
- Every question is self-contained and is followed immediately by its answer.
- Main content is projected in Trebuchet MS at a readable scale; generic whiteboard footers are absent.
- Answers are visually dominant, and changes remain identifiable without relying on colour alone.

### Shared Reading

- Five short paragraph-and-question slides alternate with five immediate answer slides.
- Each question slide contains one readable paragraph and one clearly separated question.
- Each answer is supported by the preceding paragraph and is visually dominant.
- The component retains the established large-text, low-clutter layout.

## Explicit Literacy exclusions

The following parts of the reference artefact are regression cases, not models to reproduce:

- Slide 12 uses `Join the ideas with because` and then asks for a sentence that explains the reason. Replace it with an explicit instruction such as `Combine these two sentences into one sentence using because.`
- Slides 18, 24 and 27 require a choice plus a reason, explanation or second action. A warm-up question must require exactly one student response.
- The multiple-choice distractors on Slides 18, 24 and 27 are too easy to reject without applying the target rule. Use grammatically parallel, similarly detailed options based on plausible misconceptions, or replace the item with a direct-response task.
- Slides 29-31 use a propeller example that invites debate about whether `rotate` is more precise than `turn`. Replace the entire sequence with an unambiguous semantic contrast. Do not treat technicality or formality as precision.

## Earlier corrected failures that must remain corrected

- Do not restore generic whiteboard-response footers.
- Keep the list-comma reminder, model, question and answer within one stated convention.
- Keep all text inside its instructional panel with deliberate internal margins.
- Support every Shared Reading title, question, inference and answer with the displayed paragraph.
- Preserve meaning when modelling controlled vocabulary changes; label added facts as elaboration.

## Deterministic regression expectations

Running `scripts/audit_pack_contract.py` on the reference deck with its complete component-acceptance record must report:

- **1** `literacy_combine_instruction_unclear` failure on Slide 12;
- **3** `literacy_multiple_response_prompt` failures on Slides 18, 24 and 27;
- **1** `literacy_contestable_precision_claim` failure on Slide 29;
- no failure of the correctly ordered 10 Literacy triads or five Shared Reading pairs.

The audit cannot determine distractor plausibility or settle every semantic distinction reliably. Independent human review must reject the multiple-choice and precision exclusions above even if deterministic checks pass.

## Regression pass criteria

A future pack passes when:

1. it retains or improves on the approved component characteristics;
2. none of the explicit exclusions or earlier corrected failures recurs;
3. every Literacy question requires one student action and one response;
4. every choice task has credible, parallel distractors and requests only the selected option;
5. every claimed precision distinction is accurate, meaning-preserving and explainable in one short prepared sentence; and
6. the complete deck passes deterministic, semantic and full-size rendered review.

## Required use

Use this record after changes to:

- Morning Work revision design;
- Literacy warm-up architecture, instruction wording, response load, distractors or semantic precision;
- Shared Reading paragraph/question/answer structure;
- student-facing language, projected typography, semantic colour or panel containment; or
- pack release QA.
