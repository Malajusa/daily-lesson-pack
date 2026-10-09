# Strategic animations for projected teaching

## Purpose and evidence boundary

Use animation to organise the learning sequence, direct attention to a meaningful
change and allow a teacher-controlled pause. Do not animate every slide.
Choose a static slide when students need to inspect, compare or work independently
with all the required information available.

Mayer and Moreno (2003), *Nine Ways to Reduce Cognitive Load in Multimedia
Learning*, discuss segmentation, signalling, removal of extraneous material and
placing corresponding words and graphics together. Their segmented multimedia
examples used learner control; applying those principles to teacher-controlled
whole-class slides is a design inference, not evidence that this plugin reduces
measured cognitive load. See [the paper](https://doi.org/10.1207/S15326985EP3801_6)
and [the full text](https://carpentries.github.io/instructor-training/files/papers/mayer-reduce-cognitive-load-2003.pdf).

Leahy and Sweller (2011), *Cognitive load theory, modality of presentation and
the transient information effect*, investigate how information length and
transience affect processing. Use persistent working and pauses as safeguards;
do not claim that adding motion automatically improves learning.
[Primary publication](https://doi.org/10.1002/acp.1787).

The effect choices below are workflow defaults. Research does not establish a
universal best transition, animation duration or number of clicks.

## Plan before authoring

For each worked model, joint construction or staged explanation, record a concise
teacher-facing reveal plan. A deliberate static decision is valid when it better
serves the task. Keep this plan in authoring records or speaker notes, not in the
student interface. Include:

- slide identity and instructional purpose;
- information visible on entry and information withheld;
- each click's meaningful step, target objects and final native shape IDs;
- effect, objects retained/removed and what changes or remains invariant;
- the question or prediction before the click and the hold point afterwards;
- final state, answer visibility and export/print requirements.

Keep the original problem, relevant givens, diagram scale and needed prior working
visible. Reserve space for subsequent steps so existing content stays in place.
Keep labels close to the objects they explain. Reveal one coherent reasoning step
per click, grouping its equation, changed objects and necessary labels together.
Do not reveal counters individually or equations character by character merely
to increase the number of clicks. Add a separate click only when it creates a
useful decision, prediction or explanation opportunity.

## Native PowerPoint implementation

For `.pptx` worked models whose reveal plan calls for staging, use native
within-slide on-click **Appear** as the default. Keep one worked example on one
slide when the completed model remains readable. Default slide navigation to
instant/manual; slide transitions are a separate feature.

- Use **Disappear** only when removal communicates the mathematical or textual
  change. Retain the prior equation or a labelled before-state when comparison is
  necessary. Removing a representation must not remove the only evidence needed
  to understand the explanation.
- Use a restrained emphasis cue when students must notice a changed quantity or
  feature; retain an accessible label or other cue besides colour.
- Use a short motion path or transformation only when the movement itself teaches
  an exact relationship, such as regrouping or translation. Preserve quantities,
  units, scale and whole size. Provide a stable end-state and a teacher hold point.
- Avoid decorative fly-ins, bounce, spin, sound effects, loops and automatic
  progression. Do not use animation to conceal excessive final-state density.
- Match pacing to observed responses. The click enables a pause; it does not
  enforce think time or establish understanding.

An animation is an object effect stored in slide timing; a transition changes
slides. A series of near-identical slides with Fade is not a native Appear
sequence. Do not inflate the deck with duplicates to simulate animation.
Do not require the sshow plugin. Use the available PowerPoint-authoring capability
and preserve native timing through export, assembly and later edits.
[Microsoft format guidance](https://learn.microsoft.com/en-us/office/open-xml/presentation/working-with-animation).

If the authoring tool cannot encode/preserve native effects, report that concrete
limitation. Supply a clearly labelled unanimated candidate and reveal plan if
useful. Do not silently substitute transitions, claim animations were added, or
introduce duplicate build slides without explicit user direction.
Split a model when its completed content genuinely needs more space or a new
instructional purpose; record that reason rather than treating all extra slides
as a failure.

## Preserve component question/answer rules

Keep mandatory separate question and matched answer slides, counts, roles and
immediate adjacency. This standard does not replace warm-up, Shared Reading or
assessment architecture with answers hidden on the question slide.
Put any staged feedback on the matched answer slide. Keep independent practice,
exit tasks and problem launches free of unsolicited strategy cues. Do not hide
task-critical information behind clicks during independent work.

For writing, reveal a model's annotation or one deliberate revision, while
preserving the before-text when comparison is the learning goal. Do not animate
each word or let a reveal conceal a changed or omitted proposition.

## Representative model: compensation for addition

For `59 + 29`, show the original problem and exactly 29 units on entry. Model
the second addend rather than suggesting these counters represent the whole sum.

| State | Reveal | Retain / remove | Teacher hold point |
|---|---|---|---|
| Entry | Original problem; 29 labelled units | Keep givens visible | How could we make the addition easier? |
| Click 1 | `29 → 30: add 1`; one labelled extra unit | Keep original 29 units | What have we changed? |
| Click 2 | `59 + 30 = 89` | Keep the extra unit and change line | Is 89 too high or too low? By how much? |
| Click 3 | `89 − 1 = 88`; explanation and original sum's answer | Remove only the extra unit; retain working | Why do we subtract 1? |

Three clicks suit this example; do not impose that count on every concept.
For rounding down, show the omitted amount and then add it back. For chunking,
reveal each useful chunk and accumulated sum. For fraction equivalence, retain
the same whole and shaded amount while revealing equal repartitioning and its
matching equation. Check every intermediate mathematical state, not only the
finished answer.

## Validate the final delivered file

1. Check that each planned effect targets an existing native object, shape IDs
   and timing IDs are valid, grouping/order matches the plan, and staging uses
   on-click object effects rather than transitions. Verify the final assembled
   `.pptx`, not only a pre-export model.
2. Inspect entry, every meaningful click and the final state at full size. Check
   quantities, answer timing, persistent working, readable labels, stable position
   and containment. A static renderer may display all animated objects at once;
   its image cannot certify entry visibility or playback.
3. When PowerPoint or the intended host is available, play each animated model
   from slide entry through all clicks. Check correct reveal/removal, hold points,
   no automatic advance, final state, and restart/back navigation as supported.
4. Record structural checks, simulated state inspection and actual host playback
   separately, bound to the final deck hash. A simulated state is not playback
   evidence. If playback is unavailable, state that it is unverified; do not mark
   the playback check PASS or describe the animated pack as classroom-ready.
5. Preserve canonical task and answer content in print/PDF outputs. Static export
   may flatten all effects: inspect student question pages for hidden-answer
   leakage and teacher/answer pages for missing or mutually overlapping states.
   Use explicit static views from the same content source where necessary.

Route defects to the owning component, rebuild, and rerun applicable QA. Adding
timing after a previous PASS changes the deck hash and invalidates that evidence.
