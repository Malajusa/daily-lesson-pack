# Literacy modes and accessible whole-text reading

## Defaults and selection

Keep supported practice as the default: ten Reminder -> Question -> Answer items,
unless the resolved count is explicitly changed. Select question_first_check only
for item IDs explicitly identified by the teacher or supplied plan. Keep
paragraph_local reading as the default; select whole_text only from the current
teacher request or plan. Record the selection source in teacher notes. Do not
silently change either default or any year-level profile.

## Question-first checks

Present a complete question before any item-specific help, take the first attempt,
then give matched feedback with the full answer and concise explanation. If help
is needed, preserve the first attempt, show a reminder/model, take a separately
recorded retry, then give feedback. Never overwrite the first result with a retry.
Each question/retry requires one action and one brief response. Essential task
sentences, words, options and context remain visible. A known target term may be
used without its answer-bearing definition; if that definition needs teaching,
label the attempt supported. Self-contained means readable, not supplied with the
rule being checked. Support remains available; avoid prolonged unsupported struggle.

Question-first is a format, not an independence label. Audit the WHOLE preceding
sequence: reminders, earlier questions, models, answers/feedback, posters and
teacher/peer talk, plus known intervening rehearsal. Earlier feedback on the same
rule cues a later question even when unrelated slides intervene. Record target
rule, cue sources, initial response, support, retry response and actual interval
for delayed checks separately. Use cue status supported, recently_cued,
no_identified_recent_target_cue, or unknown. Missing exposure history means unknown;
it never establishes independence. Known cues remain known even when wider history
is incomplete. Re-audit labels after actual delivery changes. No same-sequence item
proves delayed retention; no single delayed success establishes mastery.

## Whole-text comprehension

Read the complete coherent source before synthesis. Keep every relevant part
readable and accessible during modelling, questions and feedback through readable
source panels or an identical complete handout available to every pupil/pair.
Earlier projection alone is insufficient. Split projection rather than shrink text.
A packet audit verifies supplied source material, not that pupils received it.

Include an exact teacher think-aloud showing a decision: notice, revisit, connect,
infer/check or repair understanding. Distinguish explicit text from reasonable
inference and background knowledge. Model a strategy, not only a polished answer.
Then include guided application and a reduced-support attempt, one clear question
per slide with matched feedback immediately after. Source and model stages are
teaching stages outside the question/answer pairs; number question pairs only.
Reused evidence extracts on feedback may repeat previously read source, never add
new story facts. Keep answers prominent and text/question panels distinct.

Teacher notes identify relevant passages and clue-to-inference links. Accept
alternative answers supported by text. Remove teaching-only evidence highlighting,
leading prompts and sentence starters for reduced-support attempts while retaining
source access. Same-text work after modelling is application, not independent
transfer. Transfer needs a suitable new text/task without answer-bearing guidance.
Record actual help; do not label guided/modelled responses independent.

## Structural evidence for the existing PPTX audit

Legacy/default decks retain their existing headers and need no new notes record.
For ANY mixed-mode literacy sequence, put one single-line `DLP_LITERACY: {JSON}`
record in speaker notes on EVERY numbered literacy slide. Use existing numbered
headers with REMINDER, QUESTION or ANSWER; optional help uses SUPPORT then RETRY.
Keep SUPPORT and RETRY explicit in the rendered header (use an explicit eyebrow
when a renderer would otherwise rename them REMINDER or QUESTION). Each record names target_rule, mode (supported_practice or question_first_check),
selection_source for checks, history_known (boolean), prior_cues (list of strings)
and cue_status on QUESTION/RETRY. Missing or malformed records fail closed.
The audit computes same-rule cueing from all earlier numbered items, including
earlier question-first questions, reminders and answers. Tag additional visible
or spoken cues in prior_cues; semantic review must check their completeness and
target-rule equivalence. Text labels alone cannot prove an exposure audit.

Optional help is a conditional delivery branch, not a requirement for every pupil.
Keep the initial attempt and retry as distinct teacher-note records. Any supplied
initial_response and retry_response must be separate fields, never one overwritten
result. Report actual slide/build count; do not enforce thirty slides in mixed mode.

In whole-text mode, put `DLP_READING: {JSON}` in speaker notes on the SOURCE
declaration, every MODEL stage and every numbered QUESTION/ANSWER stage. Unnumbered
source continuation slides may omit the record when they only repeat exact source
content already bound to the complete handout. A SOURCE stage contains source_id and source_text, plus handout_path (relative
to deck), handout_sha256. Supply a readable PDF handout with identical source text.
MODEL stages contain think_aloud and source_id. QUESTION/ANSWER stages contain
mode=whole_text, source_id, stage=guided or reduced_support, and evidence_quotes
(exact source extracts). Questions also contain selection_source. Model stages
are unnumbered; QUESTION/ANSWER headers retain their normal pair numbering.
The structural audit verifies source identity and supplied PDF text/hash, model
presence and stage order. An independent semantic reviewer still checks genuine
cross-text demand, inference accuracy, actual access, cue removal and useful models.

## Acceptance and limits

Exercise all-supported and paragraph-local defaults; mixed checks with/without
help; earlier same-rule feedback across intervening content; unknown history;
missing/mismatched source and handout; unsupported inference and false transfer
labels. Run existing typography, containment, package and release checks as
applicable. A synthetic test, rendered example or instruction update is not
classroom-effectiveness evidence and does not release a complete teaching pack.

The bundled `examples/benchmarks/literacy-reading-modes.json` contains synthetic
worked content and specs. When regenerating its PDF handout, recompute and bind
the handout hash in the SOURCE notes before auditing the newly built deck.
