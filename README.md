# Daily Lesson Pack

Version-controlled development repository for the **Daily Lesson Pack** skill.

## Purpose

This repository is the working source for developing, reviewing and testing the Daily Lesson Pack skill used to prepare classroom teaching materials and daily lesson packs.

The current installed local skill remains authoritative until its files are copied into this repository. The local source is:

`C:\Users\mitch\.codex\skills\daily-lesson-pack\SKILL.md`

Do not reconstruct or replace the current skill from older archived versions when synchronising it here.

## Intended repository structure

```text
.
├── SKILL.md                 # Authoritative skill instructions once synchronised
├── README.md                # Repository overview
├── CHANGELOG.md             # Significant skill changes
├── .gitignore
├── docs/
│   └── DEVELOPMENT.md       # Development and update workflow
├── examples/
│   └── README.md            # Regression examples and benchmark outputs
└── .github/
    └── pull_request_template.md
```

## Development principles

- Treat the newest deliberate skill rules as authoritative.
- Do not silently restore rules from older versions where later changes were intentional.
- Make meaningful changes through small, reviewable commits or pull requests.
- Record substantial behaviour changes in `CHANGELOG.md`.
- Test changes against representative Daily Lesson Pack prompts before treating them as stable.
- Preserve classroom-facing clarity, curriculum alignment and the skill's established output requirements.

## Suggested workflow

1. Synchronise the current local `SKILL.md` and any supporting skill files into this repository.
2. Create a branch for each meaningful change.
3. Update the skill and any supporting documentation together.
4. Run representative regression examples.
5. Review the diff for unintended rule loss or contradiction.
6. Merge the change into `main` once the new behaviour is accepted.
7. Synchronise the accepted repository version back to the installed local skill.

## Status

Repository scaffold created. The current local `SKILL.md` has **not yet been copied into this repository**.
