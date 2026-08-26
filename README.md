# Daily Lesson Pack

Version-controlled development repository for the **Daily Lesson Pack** skill.

## Purpose

Daily Lesson Pack 3.2 uses a small orchestrator plus independently owned teaching components. The architecture is designed to prevent a change to one component from silently changing another.

## Modular architecture

```text
.
├── SKILL.md                              # Daily Lesson Pack orchestrator
├── skills/
│   ├── registry.json                    # Canonical component registry
│   ├── dlp-morning-work/SKILL.md
│   ├── dlp-literacy-warmup/SKILL.md
│   ├── dlp-shared-reading/SKILL.md
│   ├── dlp-guided-reading/SKILL.md
│   ├── dlp-writing-lesson/SKILL.md
│   ├── dlp-numeracy-warmup/SKILL.md
│   ├── dlp-maths-lesson/SKILL.md
│   └── dlp-pack-qa/SKILL.md
├── references/                           # Shared visual, QA and Mathematics standards
├── scripts/                              # QA + component packaging
├── docs/
│   ├── DEVELOPMENT.md
│   ├── MODULAR-REFACTOR-AUDIT.md
│   └── COMPONENT-SKILL-INSTALLATION.md
├── examples/
│   └── benchmarks/                       # Regression fixtures and cross-topic checks
└── .github/
```

The root skill owns context, routing, assembly and release decisions. Each child skill owns its own pedagogy and presentation contract. `dlp-pack-qa` independently reviews the assembled pack and returns defects to the owning component.

A complete Term/Week Mathematics pack remains the responsibility of the standalone **Weekly Maths Pack** skill rather than being duplicated inside Daily Lesson Pack.

## Universal Mathematics canon

`references/universal-maths-instruction-canon.md` is the authoritative instructional standard for all Daily Lesson Pack Mathematics content.

It requires:

- lesson-mode and scope classification;
- meaning before procedural shorthand;
- mathematically purposeful and exact representations;
- explicit correspondence between representations, language and notation;
- precise technical vocabulary with student-friendly explanation;
- genuine guided practice and non-revealing question slides;
- model-to-independent-demand alignment;
- plausible misconception analysis;
- accurate distinctions between calculation, reasoning and problem solving;
- complete answer modelling and Mathematics-specific release QA.

The full canon applies to the main Mathematics lesson. Mathematics warm-ups and Morning Work apply its accuracy, terminology, representation and answer-integrity requirements while remaining retrieval tasks.

Use `examples/benchmarks/universal-maths-canon-regression.md` to test Mathematics changes across at least two different concept families.

## Classroom-feedback regression record

`examples/benchmarks/t3w6-monday-modular-regression.md` records the first modular Daily Lesson Pack artefact and the classroom failures identified after use. Treat it as a diagnostic regression source, not as an approved layout or quality floor.

## Skill routing and installation

The canonical list of child skills is `skills/registry.json`.

When the host supports direct cross-skill routing, install/register the component skills separately under the names in their frontmatter and let the root orchestrator invoke them.

Build individually installable packages with:

```bash
python scripts/package_component_skills.py
```

See `docs/COMPONENT-SKILL-INSTALLATION.md` for the package layout and registration workflow.

When direct routing is unavailable, the root skill uses the bundled contracts under `skills/<skill-name>/SKILL.md` as a deterministic fallback. This preserves modular ownership without forcing the parent `SKILL.md` to absorb every rule again.

Do not assume that placing several `SKILL.md` files in one repository automatically registers each one as a separately invokable skill. Registration depends on the host environment and should be verified before production use.

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
- Test Mathematics changes across more than one concept family.

## Update workflow

1. Develop or revise the owning component skill only.
2. Run its component checks.
3. For Mathematics changes, apply the universal Mathematics regression benchmark to at least two concept families.
4. Assemble a representative Daily Lesson Pack.
5. Run `dlp-pack-qa` over the entire assembled pack.
6. Compare against the relevant classroom-feedback benchmarks.
7. Rebuild the affected component package.
8. Review the diff for unintended rule loss or contradiction.
9. Merge only after representative classroom regression passes.
10. Synchronise/register the accepted component skill in the production host where supported.

## Current version

**3.2.0 — universal Mathematics instruction canon with cross-topic regression and independent QA enforcement.**
