# T3W6 Monday Modular Regression Record

## Status

**Superseded diagnostic benchmark.**

The 23 August 2026 artefact established the modular routing architecture, but classroom feedback on 24 August identified instructional-language, warm-up independence, group-labelling and panel-containment failures. It must not be used as an approved classroom-quality floor without applying the corrections in this record.

Reference artefact:

- file name: `T3W6_Monday_Daily_Lesson_Pack_Modular_Regression.pptx`
- slide count: **72**
- SHA-256: `46477f17937b55db6dc31a8c70558df0af0b56dd647d21fb84a72ef1d73dccce`

The PPTX is retained as a source of regression cases, not as a layout to reproduce.

## Known failures that must not recur

### Literacy warm-up

- Question slides did not have a preceding reminder slide.
- Some questions depended on unstated or earlier context, including a linking-phrase question without the preceding idea.
- `classification opening` was not student-facing language.
- Corrected punctuation was not visually isolated on answer slides.
- Generic answer explanations such as `the answer matches the meaning and grammar in the prompt` did not teach the relevant rule.

### Guided Reading

- The deck displayed `Very low group`.
- Guided Reading text, prompts and transition tasks were generated despite the later timetable-only decision.

### Writing

- Text escaped shaded or coloured panels on multiple writing slides.
- Some technical-vocabulary explanations were too vague to show what precision was added.

## Current acceptance characteristics

### Morning Work

- Slide 1 is immediately usable Morning Work rather than a cover or setup slide.
- Every response can be completed in a book while the slide remains projected.
- No instruction asks students to circle, highlight or underline projected-only content.
- A model described as precise contains details specific to its topic.

### Literacy warm-up

- The default sequence contains 10 `Reminder -> Question -> Answer` triads.
- Each question contains all information required to answer it.
- The reminder teaches the method with a different example and does not reveal the next answer.
- Student language is familiar, direct and immediately actionable.
- Answer slides make inserted punctuation or changed wording green, bold and enlarged, with a textual cue.
- Answer explanations state the relevant rule or meaning.

### Shared Reading

- Each question slide displays one short paragraph and one question about that paragraph.
- Every question slide is immediately followed by its matched answer slide.
- The complete model answer is visually dominant and does not introduce a new paragraph or question.
- Question slides do not reveal the answer or teaching-only evidence cues.
- Text remains suitable for whole-class projection.

### Guided Reading

- Guided Reading appears only in the timetable.
- No Guided Reading instructional slide, passage, prompt, teacher guide or transition task is generated.
- Any displayed group comes from an authoritative schedule and is exactly `Alpha`, `Beta`, `Gamma`, `Delta` or `Epsilon`.
- No ability descriptor or inferred group appears.

### Writing

- The lesson explicitly teaches and applies the scheduled Information Report feature.
- Student-facing language uses familiar actions and defines necessary technical terminology.
- Technical-word substitutions preserve meaning and scope.
- Each precision explanation states the exact information added.
- Comparison tables use no more than two substantial rows per projected slide.

### Visual quality

- Projected readability takes priority over fixed layouts.
- Important content uses available slide space.
- Colour is restrained and instructional.
- Inserted corrections remain understandable without colour alone.
- Every coloured, shaded or bordered panel contains its text with deliberate padding.
- Internal margins below `0.15 in` on substantive filled text panels block release.

## Regression pass criteria

A future representative Daily Lesson Pack passes when:

1. all component-specific QA checks pass;
2. none of the known failures above recurs;
3. the pack satisfies the current acceptance characteristics;
4. the pack is inspected slide-by-slide at full projected size;
5. a fix in one component does not degrade an unrelated component;
6. any deliberate departure is supported by a later explicit teacher instruction.

## Required use

Use these regression cases after changes to:

- `SKILL.md` orchestrator routing;
- any `skills/dlp-*/SKILL.md` component;
- warm-up architecture or calibration;
- Guided Reading scope or group labels;
- student-facing instructional language;
- technical-vocabulary modelling;
- projected typography, semantic colour or panel containment;
- release QA.
