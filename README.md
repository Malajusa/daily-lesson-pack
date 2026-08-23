# Daily Lesson Pack

Version-controlled development repository for the **Daily Lesson Pack** skill.

## Purpose

The Daily Lesson Pack is being refactored from one large skill into a small orchestrator plus independently owned teaching components. The aim is to prevent a change to one component from silently changing another.

## Modular architecture

```text
.
├── SKILL.md                              # Daily Lesson Pack orchestrator
├── skills/
│   ├── dlp-morning-work/SKILL.md
│   ├── dlp-literacy-warmup/SKILL.md
│   ├── dlp-shared-reading/SKILL.md
│   ├── dlp-guided-reading/SKILL.md
│   ├── dlp-writing-lesson/SKILL.md
│   ├── dlp-numeracy-warmup/SKILL.md
│   ├── dlp-maths-lesson/SKILL.md
│   └── dlp-pack-qa/SKILL.md
├── references/                           # Shared visual/QA standards
├── scripts/                              # Automated QA screening
├── docs/
│   ├── DEVELOPMENT.md
│   └── MODULAR-REFACTOR-AUDIT.md
├── examples/                             # Regression examples
└── .github/
```

The root skill owns context, routing, assembly and release decisions. Each child skill owns its own pedagogy and presentation contract. `dlp-pack-qa` independently reviews the assembled pack and returns defects to the owning component.

A complete Term/Week Mathematics pack remains the responsibility of the standalone **Weekly Maths Pack** skill rather than being duplicated inside Daily Lesson Pack.

## Skill routing and installation

When the host supports direct cross-skill routing, install/register the component skills separately under the names in their frontmatter and let the root orchestrator invoke them.

When direct routing is unavailable, the root skill uses the bundled contracts under `skills/<skill-name>/SKILL.md` as a deterministic fallback. This preserves modular ownership without forcing the parent `SKILL.md` to absorb every rule again.

Do not assume that placing several `SKILL.md` files in one repository automatically registers each one as a separately invokable skill. Registration/packaging depends on the host environment and should be verified before production use.

## Development principles

- Treat the newest deliberate classroom feedback as authoritative.
- Keep each rule with the component that owns the behaviour.
- Keep only true cross-component invariants in the orchestrator.
- Do not silently restore older rules where later changes were intentional.
- Do not invent missing historical reference content.
- Make meaningful changes through small, reviewable commits or pull requests.
- Run component regression checks and then full-pack QA after every revision.
- A fix to one component must not trigger an unrelated rewrite of other components.
- Preserve classroom-facing clarity, curriculum alignment and the established visual-quality floor.

## Suggested workflow

1. Develop or revise the owning component skill only.
2. Run its component regression checks.
3. Assemble a representative Daily Lesson Pack.
4. Run `dlp-pack-qa` over the entire assembled pack.
5. Review the diff for unintended rule loss or contradiction.
6. Merge only after the modular branch passes representative classroom regressions.
7. Synchronise/register the accepted component skills in the production host.

## Current refactor

The modular architecture is under review in the `refactor/modular-daily-lesson-pack` branch. See `docs/MODULAR-REFACTOR-AUDIT.md` for the ownership map, repository-integrity findings and migration strategy.
