# Semantic Colour Regression Example

## Purpose

Use this example to check that the Daily Lesson Pack applies colour as an instructional signal rather than decoration. It is a specification for regression testing, not a fixed lesson that overrides the active curriculum sequence.

## Test A — Mathematics warm-up pair

### Intended concept

Adding and subtracting fractions with like denominators.

### Prompt slide structure

Keep the established three-column layout and green `Why` footer.

**All**

Calculate: `2/7 + 3/7`

**Most**

A bottle is `7/10` full. Sam drinks `3/10` of the bottle. What fraction of the bottle remains?

**Some**

Complete: `□/12 + 5/12 = 11/12`

**Why footer**

What stays the same when you add or subtract fractions with the same denominator?

### Semantic-colour mapping

- neutral background and ordinary text;
- one blue instructional accent identifies the denominator in each fraction and the matching denominator in any fraction bar used on the slide;
- do not assign unrelated colours to the three calculations;
- `All`, `Most` and `Some` retain their fixed labels and positions, so colour is not required to know the level;
- the green footer treatment means `Why/reasoning` only.

### Answer slide

**All:** `5/7`

**Most:** `4/10`

**Some:** `6/12 + 5/12 = 11/12`

**Why:** The denominator stays the same because the size of the equal parts has not changed; only the number of those parts changes.

The denominator receives the same blue signal wherever it reappears. The complete answers remain readable and meaningful if the colour is removed.

### Fail examples

- red `All`, amber `Most`, green `Some` traffic-light coding;
- every numerator and denominator given a different colour;
- different denominator colours in question and answer slides;
- saturated card backgrounds that make the three columns compete with the mathematics;
- colour as the only distinction between levels.

## Test B — Shared Reading slide

### Paragraph

**Mangrove roots slow moving water. As waves pass through the tangled roots, the water meets resistance and loses some energy. This means less wave energy reaches the shoreline, which can reduce erosion and damage.**

### Question

What does the **resistance** from mangrove roots do to the waves?

### Semantic-colour mapping

- paragraph and question are separated by spacing/panel structure before colour is applied;
- the word `resistance` uses the same restrained blue signal in the paragraph and question because students must connect the question directly to that part of the text;
- no other vocabulary is automatically highlighted;
- the rest of the paragraph stays neutral and high contrast;
- the answer slide may retain the cue during modelling, then the next independent reading item should remove the cue if students are expected to locate evidence without it.

### Expected answer

The resistance makes the waves lose some energy before they reach the shoreline.

### Fail examples

- colouring several interesting words with unrelated hues;
- using a coloured paragraph background as the only separation between paragraph and question;
- highlighting the whole sentence when only one correspondence matters;
- retaining strong evidence highlights on every independent comprehension item.

## Regression acceptance criteria

Both test slides pass only when:

1. every non-neutral colour has an identifiable instructional role;
2. repeated concepts keep the same colour;
3. the slide remains understandable in greyscale;
4. text and meaningful graphics meet the required contrast thresholds;
5. colour does not replace labels, fixed position, symbols or explicit wording;
6. the visual signal directs attention to the intended relationship rather than to decoration;
7. the cue is reduced when the next task requires independent identification.
