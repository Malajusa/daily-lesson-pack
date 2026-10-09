# Interactive Mathematics lesson adaptation

Use this contract when the user asks to apply Daily Lesson Pack Mathematics
principles to an existing browser/app lesson bank. Read the Mathematics canon,
the maths component and independent QA contracts. This adaptation does not
invoke the daily timetable/PPTX assembly pipeline or certify a classroom pack.
Retain the application's supported builders, content identities, navigation,
answer handling, accessibility and persistence contracts.

## Plan before authoring

Record each lesson's authored learning goal, observable success criteria,
concept boundary, starting problem, representation purpose and exit task.
Resolve learner pitch from the application's approved skill/profile sources;
do not force a Year 4/5 pack profile onto early-number app lessons.

A goal states what the learner will do with mathematics. A topic title such as
`g and kg` is insufficient. `Convert masses between grams and kilograms` is a
goal. Criteria describe evidence, such as finding the equivalent mass and
explaining that the mass stays constant while the unit and numerical count
change. Completion of screens is not evidence of understanding.

Link the hardest independent demand and exit task to the modelled examples.
Do not generate these fields from the title as a fallback. In a review lesson,
name the intended connections rather than introducing an unrelated new method.

## Author each teaching state

For each meaning/model/guided screen, specify:

- the one teaching point or learner action;
- the exact problem or relationship, visible before its explanation/model;
- the brief sentence and number sentence appropriate to that point;
- the representation and what it makes observable;
- the quantities, units, grouping/partition and relationships shared by the
  words, notation and diagram;
- what is initially visible, what is revealed, what remains and when a response
  is required. A static screen is acceptable where staging adds no value.

Inspect the learner's initial view as well as completed states. Put the
original problem before worked results. Introduce a strategy's purpose before
its steps: taking 8 up to 10 helps use a known ten fact, and splitting 5 into
2 and 3 preserves the original total. The diagram must show that split and
combination, not merely a finished bar for 13.

Use a sentence, notation and a mathematical representation together when they
explain the point. Do not manufacture an equation for a naming/counting goal
where a numeral and exact quantity are the appropriate notation. Independent
and transfer checks can intentionally remove scaffolds; do not require every
assessment screen to contain a diagram that reveals its answer.

An icon, an SVG tag, a caption repeating the answer or a decorative illustration
does not establish mathematical modelling. Use the smallest useful set of
representations. Additional examples need their own question and purpose.

For conversions, preserve the measured quantity and show the relationship
between units. A balance can show equal mass; a calibrated ruler can show the
same length in two units. Fractions and bars are permitted when they illuminate
conversion. Reject a representation that draws attention to a different concept,
not a particular word, shape or family of diagram. Flour bags are one example,
not a mandatory template for all measurement.

## Render and inspect

Inspect every new/revised teaching screen at intended browser widths, including
the narrowest supported width, and every distinct reveal state. Build a complete
lesson/scene inventory so omissions are visible. Record variants driven by table
selection, operation or other content settings. Reuse a representative layout
capture only for identical geometry; retain per-scene semantic coverage.

Review recognisability, hierarchy, useful white space, text density, contrast,
semantic colour and correspondence. Read labels at the actual rendered size.
Test labels against their semantic regions: a bag label belongs inside the
front face, not simply somewhere inside the SVG bounds. Check side padding,
line crossings and collisions. Resize/reflow the drawing or shorten copy where
appropriate. Neither largest possible text nor smallest fitting text is the
objective. Use a consistent visual family without obscuring exact quantities.

## Independent review and evidence

Keep four separate verdicts: mathematical accuracy, instructional clarity,
visual communication and software behaviour. An engineering pass cannot
substitute for another verdict. For semantic review, first infer the learning
goal from the learner-visible content, then compare it with the authored goal.
Inspect actual quantities and relationships, not just titles and captions.

The reviewer must have an actual separate execution and raw evidence. Cite exact
lesson/scene/state IDs, observations and artefact hashes. A screenshot list is
not proof that someone inspected it. Source-only review leaves visual judgement
pending. Unsupported aspects remain unverified; do not manufacture review
receipts or call check counts educational-quality evidence.

`scripts/audit_interactive_lesson_contract.py` checks inventory, authored fields,
source bindings and evidence coverage. It returns structural results separately
from human/model teaching judgements. It cannot prove semantic correspondence,
recognisability or classroom effectiveness from assertions in JSON.

Use `examples/benchmarks/interactive-maths-regression.json` and
`tests/test_interactive_lesson_contract.py` for structural failures. Also use the
blind review cases in `examples/benchmarks/interactive-maths-review.md` for genuine
independent judgement. Test at least two concept families and retain valid
alternatives, including legitimate fractional quantities in conversion lessons.

Repair findings in the owning content/builder, then re-export and re-review the
affected states. Changes invalidate the affected hashes and reviews. Report
bank coverage, unresolved findings and the four verdicts separately. Publish or
merge only within the application's existing authority and user authorisation.
