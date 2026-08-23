#!/usr/bin/env python3
"""Package Daily Lesson Pack component skills as individually installable ZIPs.

Usage:
    python scripts/package_component_skills.py
    python scripts/package_component_skills.py --out dist/component-skills

The script reads skills/registry.json, validates each component entrypoint,
and writes one self-contained ZIP per component plus a combined bundle ZIP.
Shared presentation/QA references are copied into each package so a separately
registered skill does not depend on the parent repository's relative paths.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


SHARED_REFERENCES = (
    "references/slide-deck-quality-standards.md",
    "references/semantic-colour-standard.md",
    "references/panel-containment-standard.md",
)

QA_ONLY_FILES = (
    "examples/benchmarks/t3w6-monday-modular-regression.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="dist/component-skills", help="Output directory")
    return parser.parse_args()


def add_repo_file(zf: zipfile.ZipFile, repo: Path, package_root: str, relative_path: str) -> None:
    source = repo / relative_path
    if not source.exists():
        raise FileNotFoundError(f"Missing package dependency: {source}")
    zf.write(source, f"{package_root}/{relative_path}")


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parents[1]
    registry_path = repo / "skills" / "registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    out_dir = (repo / args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    package_paths: list[Path] = []

    for component in registry["components"]:
        name = component["name"]
        entrypoint = repo / component["entrypoint"]
        if not entrypoint.exists():
            raise FileNotFoundError(f"Missing component entrypoint: {entrypoint}")

        text = entrypoint.read_text(encoding="utf-8")
        if f"name: {name}" not in text:
            raise ValueError(f"Skill name mismatch in {entrypoint}: expected {name}")

        zip_path = out_dir / f"{name}.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"{name}/SKILL.md", text)
            zf.writestr(
                f"{name}/PACKAGE.json",
                json.dumps(
                    {
                        "name": name,
                        "entrypoint": "SKILL.md",
                        "source": component["entrypoint"],
                        "owner": component["owner"],
                        "shared_references": list(SHARED_REFERENCES),
                    },
                    indent=2,
                )
                + "\n",
            )

            for relative_path in SHARED_REFERENCES:
                add_repo_file(zf, repo, name, relative_path)

            if name == "dlp-pack-qa":
                for relative_path in QA_ONLY_FILES:
                    add_repo_file(zf, repo, name, relative_path)

        package_paths.append(zip_path)

    bundle_path = out_dir / "daily-lesson-pack-component-skills.zip"
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.write(registry_path, "registry.json")
        for package in package_paths:
            bundle.write(package, package.name)

    print(f"Packaged {len(package_paths)} component skills")
    for path in package_paths:
        print(path)
    print(bundle_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
