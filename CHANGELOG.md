# Changelog

All significant changes to the Daily Lesson Pack skill should be recorded here.

## Unreleased — modular refactor

### Added
- Orchestrator + specialised component-skill architecture.
- Separate skills for Morning Work, Literacy warm-up, Shared Reading, Guided Reading, Writing, Mathematics warm-up, main Mathematics teaching and independent pack QA.
- Bundled-contract fallback when direct cross-skill invocation is unavailable.
- Modular routing regression suite.
- Architecture and migration audit in `docs/MODULAR-REFACTOR-AUDIT.md`.

### Changed
- Root `SKILL.md` now owns context, routing, assembly and release decisions rather than detailed component pedagogy.
- Complete weekly Mathematics requests are delegated to the standalone Weekly Maths Pack skill instead of being duplicated in Daily Lesson Pack.
- Existing-pack audit/revision requests route through the independent QA skill.
- Literacy warm-up default is 10 prompt/answer pairs.
- Mathematics All / Most / Some prompts are explicitly three separate questions/tasks of increasing complexity.
- Shared Reading explicitly uses one short paragraph plus one question per substantive slide.
- Generic whiteboard-use footers are removed from warm-up requirements.

### Reliability
- QA no longer self-certifies generation. Defects are routed to the owning component and the full applicable QA suite reruns after repair.
- The refactor avoids carrying forward dangling filenames from the monolithic skill unless their source content is actually available.

## 2.4.0 — 23 August 2026

### Added
- Mandatory Panel Containment and Responsive Container Standard in `references/panel-containment-standard.md`.
- Automated `scripts/audit_panel_containment.py` geometry screening for shaded/coloured panel overflow and inadequate padding.
- Regression examples for the green `Why` footer, All / Most / Some cards and Shared Reading question panels.

### Changed
- Shaded, coloured and bordered panels must now expand/reflow with their text rather than remain fixed while typography grows.
- Meaningful panel text should normally retain approximately `0.15–0.25 in` internal padding.
- The green `Why` footer may grow taller when reasoning text wraps; its text may not extend above or below the green panel.
- Visual QA now includes a fourth check: containment of text within its intended panel.

### Fixed
- Prevents the recurring failure where enlarged student-facing text crosses or visually escapes coloured panels after a readability pass.

## 2.3.0 — 23 August 2026

### Added
- Mandatory projected-readability and space-utilisation standard in `references/slide-deck-quality-standards.md`.
- Role-based warm-up typography hierarchy instead of a single locked font size.
- `Largest sensible type` rule: short answers, key words and mathematical expressions should grow when space allows.
- Rewrite/reflow-before-shrink repair order for dense slides.
- Shared Reading projected typography guidance for paragraph and question sizing.
- Automated screening script `scripts/audit_slide_typography.py` for undersized warm-up content and likely unused-space problems.
- Regression examples covering Mathematics warm-ups, Literacy warm-ups and Shared Reading.

### Changed
- Warm-up main instructional content remains anchored at 36 pt minimum, while supporting content may use smaller or larger role-appropriate sizes.
- Supporting student-facing text is now explicitly protected from becoming fine print simply to preserve fixed card geometry.
- Visual QA now checks whether important content could be materially enlarged by using currently empty slide space.
- Space is treated as instructional real estate: layouts should reflow or merge regions before text is reduced.

## 2.2.0 — 23 August 2026

### Added
- Mandatory semantic-colour standard for instructional slides.
- Role-based colour planning before slide generation: correspondence, category, current focus, meaningful change and reasoning panels.
- Accessibility release checks for contrast, greyscale robustness and colour-only meaning.
- Colour-scaffold fading from modelling towards independent and uncued performance where appropriate.
- Regression examples for a Mathematics warm-up pair and a Shared Reading slide.

### Changed
- Visual QA now assesses whether colour supports instructional structure rather than merely improving appearance.
- Mathematics worked examples and representations must keep corresponding concepts/quantities in consistent colours when colour coding is used.
- All / Most / Some colour treatment must remain restrained, labelled and position-based; red/amber/green traffic-light coding is prohibited.
- The established green `Why` footer is reserved as a semantic reasoning cue.
- Shared Reading may use matched colour to connect a question with a relevant word/phrase, but unrelated vocabulary remains neutral and the cue must not replace layout separation.

## 2.1.0 — 19 August 2026

### Added
- Term 3 four-day overview routing for Monday, Tuesday, Thursday and Friday.
- Mandatory 20-slide Mathematics warm-up: 10 prompt-and-answer pairs.
- Fixed All / Most / Some three-column warm-up layout with green Why footer.
- Cumulative retrieval requirements based on the Mathematics Rules Worth Memorising spine.
- Stronger Morning Work, student-facing instruction and slide-quality requirements.
- Expanded evidence-backed release checks, visual validation and package QA.

### Changed
- Relief-day guidance now keeps preparation in the briefing or speaker notes.
- Shared Reading and Guided Reading are now explicitly separated from Morning Work and each other.
- Information Report writing progression is tied to the Term 3 overview.
- Mathematics visual validation and answer-slide requirements are more explicit.

## 2.0.0

### Repository setup
- Created the GitHub development repository.
- Added repository workflow and regression-testing scaffolding.

## Change-entry format

For future updates, record changes under one or more of:

- **Added** — new behaviour, rules or capabilities.
- **Changed** — intentional changes to existing behaviour.
- **Fixed** — corrections to faulty or ambiguous behaviour.
- **Removed** — behaviour deliberately retired.

Where useful, include the reason for the change and the regression example used to validate it.
