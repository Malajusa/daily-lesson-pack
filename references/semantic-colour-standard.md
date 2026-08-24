# Semantic Colour Standard for Instructional Slides

## Purpose

Use colour to make instructional structure easier to see. Colour is not decoration by default; it is a signalling system. Every non-neutral colour should help students locate, connect, distinguish or track information that matters to the learning task.

This standard is derived from the research review supplied for the Daily Lesson Pack on 23 August 2026. The evidence base supports restrained cueing, consistent correspondence coding and adequate contrast. It does not support claims that a particular hue inherently improves learning.

## Core rule

Use colour relationally and semantically:

- the same colour means the same thing within a lesson sequence;
- the same concept, quantity, category or representation keeps the same colour wherever it reappears;
- a changed colour must signal a meaningful change;
- ordinary information remains visually neutral;
- vivid colour is reserved for information that deserves attention;
- no essential meaning depends on colour alone;
- colour scaffolds are reduced when students should perform independently without them.

If a non-neutral colour cannot answer the question `What does this colour tell the learner?`, remove it or mute it.

## Palette architecture

Use a restrained role-based palette rather than a rainbow palette.

Recommended default roles:

| Role | Example | Use |
|---|---|---|
| Background | `#FFFFFF` | default slide surface |
| Body/title text | `#111827` | ordinary information |
| Primary instructional signal | `#005A9C` | one important correspondence, quantity, concept or current target |
| Blue semantic panel | `#EAF2F8` with `#103A5E` text | concept-linked explanation or definition |
| Attention panel | `#FFF3BF` with `#3B2F00` text | current operation, temporary focus or important reminder |
| Why/reasoning panel | `#EAF7EE` with `#184D2B` text | established mathematics `Why` footer |

These HEX values are examples, not learning-optimal hues. Their value is predictable role assignment and strong contrast. Do not introduce a new hue unless a genuinely different category needs distinguishing.

## Colour hierarchy

1. **Neutral first.** Most backgrounds, ordinary text, inactive steps and supporting information remain neutral.
2. **One primary signal.** Use one main accent to show the relationship or element students should notice first.
3. **Additional category colours only when needed.** Add another colour only when two or more genuinely different categories must remain distinguishable at the same time.
4. **Saturation carries priority.** More vivid treatment is reserved for the current instructional focus; inactive/context elements should be visually quieter.
5. **Colour never replaces labels.** Labels, position, borders, shapes, symbols, markers or patterns must preserve the meaning if hue is removed.

## Mathematics

Colour is especially valuable when it reduces visual search between equivalent or corresponding representations.

Use semantic correspondence coding for:

- the same value in a worked example and its diagram;
- a fraction and the matching portion of a fraction bar or number line;
- a quantity in a word problem and the same quantity in an equation;
- a geometric feature and its matching label;
- matching data series across a chart, legend and explanation;
- a current operation or step when students need to track a process.

Rules:

- Keep the same mathematical object the same colour while its identity is unchanged.
- Do not give each step in a worked example a different arbitrary colour.
- Do not colour every numeral, operator or diagram part.
- Use colour to show a relationship, not to make the mathematics look more colourful.
- When independent recognition is the goal, fade the colour scaffold through `Model` → `We do` → `Independent practice` or assessment.

### Mathematics warm-up

`All`, `Most` and `Some` remain three separate calibrated questions or responses, not degrees of completion of one question.

For the three-column warm-up layout:

- keep `All`, `Most` and `Some` in fixed positions;
- keep the text labels visible at all times;
- if category colour is used, use restrained, consistent accents or tints rather than saturated full-card fills;
- do not use a red/amber/green traffic-light mapping;
- do not imply that `All` is failure or `Some` is the only successful response;
- `Most` remains the secure target;
- the established `Why` footer keeps one fixed green semantic treatment and that green treatment is not reused for unrelated decoration.

## Shared Reading and Literacy

Use colour only when it helps students connect the displayed text with the question or analysis.

Appropriate uses include:

- the same key word or phrase highlighted in the paragraph and the question when students must locate that correspondence;
- a single textual feature and its matching annotation;
- a repeated cohesive device when the teaching point is the relationship between its occurrences;
- a temporary highlight during explicit modelling that is removed for independent application.

Do not automatically colour vocabulary words merely because they are interesting or unfamiliar. Do not highlight so many words that the paragraph loses a clear visual hierarchy.

### Answer correction highlights

On Literacy warm-up answer slides, green may mark a character, punctuation mark, word or phrase that has been inserted or changed. This is a text-level correction signal, not decorative green and not the Mathematics `Why` panel role.

- Keep unchanged sentence text neutral.
- Make inserted punctuation green, bold and at least 125% of the surrounding sentence size.
- Make a replaced word or phrase green and bold when that helps students locate the change.
- Add a textual cue such as `Added commas:` or `Changed word:` so the correction remains clear in greyscale and for students with colour-vision differences.
- Do not colour the entire corrected sentence green; colour only the instructional change.
- Use the same correction treatment throughout the warm-up.

On Shared Reading slides, the paragraph and the question must remain visually distinct through spacing, panel structure or typography first. Colour may reinforce that separation but must not be the only separator.

## I do / We do / You do fading

Colour can be a scaffold. When students must ultimately identify the structure independently:

- **Model / I do:** use clear semantic correspondence colour where it reduces search or makes the relationship explicit;
- **We do:** reduce the number or intensity of cues while retaining the key relationship;
- **Independent practice / You do:** remove non-essential colour cues and retain only structural or accessibility-safe colour;
- **Assessment or uncued retrieval:** do not preserve teaching-only colour if the intended skill is independent recognition.

Do not fade colour when colour is intrinsically part of the representation being assessed.

## Accessibility and contrast

Treat these as minimum release requirements:

- normal text contrast: at least `4.5:1`;
- large text contrast: at least `3:1`;
- meaningful graphical objects and boundaries: generally at least `3:1` where the criterion applies;
- essential meaning must not be communicated by colour alone.

Because slides are projected at distance under variable classroom lighting, aim comfortably above minimum contrast rather than scraping the threshold.

Use redundant cues:

- `✓ Correct` plus colour, not green alone;
- `✕ Incorrect` plus colour, not red alone;
- chart series distinguished by direct labels and/or marker/line shape as well as hue;
- categories identified by text labels and stable position as well as colour.

## Greyscale and colour-vision QA

Before release, inspect the rendered deck under:

1. normal colour;
2. greyscale;
3. simulated red–green colour-vision deficiency where tooling allows;
4. projected-size/full-slide rendering.

If an essential distinction collapses in greyscale, the slide relies too heavily on colour and must be revised.

## Forbidden patterns

Reject or revise slides that contain:

- arbitrary rainbow headings or icons;
- a different bright colour for every step without semantic meaning;
- changing the colour of the same concept between slides;
- saturated decorative backgrounds that compete with the learning target;
- low-contrast pastel text on pale backgrounds;
- red/green-only correct/incorrect signalling;
- charts, maps or diagrams whose categories disappear when hue is removed;
- so many highlighted elements that the intended signal is no longer obvious;
- decorative colour that attracts more attention than the task, representation or answer.

## Semantic-colour planning pass

Before slide generation, identify only the colour relationships that the lesson genuinely needs. Record them in a short mapping such as:

- `blue = fraction being tracked across equation and number line`;
- `amber panel = current operation only`;
- `green footer = Why/reasoning only`.

Reuse that mapping across the sequence. Do not silently repurpose a colour halfway through the lesson.

## Release questions

For every non-neutral colour in the final render, be able to answer:

1. What does this colour tell the learner?
2. Does the same meaning keep the same colour throughout the sequence?
3. Is the relationship still understandable without colour?
4. Is the contrast sufficient for projected classroom use?
5. Is any colour scaffold stronger than students will have when they must work independently?

A slide fails semantic-colour QA if any essential colour has no instructional role, changes meaning without reason, is inaccessible, or creates dependence that conflicts with the intended independent task.
