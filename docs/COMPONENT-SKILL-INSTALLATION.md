# Daily Lesson Pack component skill installation

## Architecture

The repository contains one parent orchestrator and eight component skills.

The parent `daily-lesson-pack` remains the user-facing entrypoint for a normal Daily Lesson Pack. Each component owns one stable area of generation or QA.

Registered components are listed in `skills/registry.json`.

## Preferred registration

Where the host supports separately registered custom/local skills, register each of these folders as an independent skill:

- `skills/dlp-morning-work/`
- `skills/dlp-literacy-warmup/`
- `skills/dlp-shared-reading/`
- `skills/dlp-guided-reading/`
- `skills/dlp-writing-lesson/`
- `skills/dlp-numeracy-warmup/`
- `skills/dlp-maths-lesson/`
- `skills/dlp-pack-qa/`

The folder name and YAML `name:` in each `SKILL.md` must remain identical.

## Reproducible packages

Run:

```bash
python scripts/package_component_skills.py
```

This creates:

```text
dist/component-skills/
├── dlp-morning-work.zip
├── dlp-literacy-warmup.zip
├── dlp-shared-reading.zip
├── dlp-guided-reading.zip
├── dlp-writing-lesson.zip
├── dlp-numeracy-warmup.zip
├── dlp-maths-lesson.zip
├── dlp-pack-qa.zip
└── daily-lesson-pack-component-skills.zip
```

Each individual ZIP contains a self-contained skill folder with `SKILL.md` and `PACKAGE.json`. The combined ZIP contains all eight installable packages plus the registry.

## Fallback mode

Some hosts do not expose skill-to-skill invocation or separate custom-skill registration. In that case, do not collapse the architecture back into a monolith.

The parent orchestrator reads the appropriate bundled component contract from `skills/<skill-name>/SKILL.md` and executes that contract directly. The ownership and QA boundaries therefore remain intact even without direct invocation.

## Update discipline

When changing one component:

1. edit only that component unless a cross-component invariant genuinely changed;
2. run its local checks;
3. run `dlp-pack-qa` across the assembled pack;
4. compare against `examples/benchmarks/t3w6-monday-modular-regression.md` when applicable;
5. rebuild the component packages;
6. update the registered copy of only the changed skill where the host supports separate registration.

This prevents a Shared Reading fix, for example, from silently changing Mathematics warm-up behaviour.
