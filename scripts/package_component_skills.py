#!/usr/bin/env python3
"""Build self-contained Daily Lesson Pack component-skill ZIPs."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


SHARED_REFERENCES = (
    "references/slide-deck-quality-standards.md",
    "references/semantic-colour-standard.md",
    "references/panel-containment-standard.md",
    "references/universal-maths-instruction-canon.md",
)

QA_ONLY_FILES = (
    "examples/benchmarks/t3w6-monday-modular-regression.md",
    "examples/benchmarks/universal-maths-canon-regression.md",
    "scripts/audit_slide_typography.py",
    "scripts/audit_panel_containment.py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="dist/component-skills", help="Output directory")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (defaults to the script's repository)",
    )
    return parser.parse_args()


def write_bytes(archive: zipfile.ZipFile, path: str, data: bytes) -> None:
    info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, data)


def read_required(repo: Path, relative_path: str) -> bytes:
    source = repo / relative_path
    if not source.is_file():
        raise FileNotFoundError(f"Missing package dependency: {source}")
    return source.read_bytes()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    registry_path = repo / "skills" / "registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    version = (repo / "VERSION").read_text(encoding="utf-8").strip()

    out_dir = (repo / args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    package_paths: list[Path] = []

    for component in registry["components"]:
        name = component["name"]
        entrypoint = component["entrypoint"]
        skill_text = read_required(repo, entrypoint)
        if f"name: {name}".encode("utf-8") not in skill_text:
            raise ValueError(f"Skill name mismatch in {entrypoint}: expected {name}")

        package_files: dict[str, bytes] = {
            "SKILL.md": skill_text,
            "agents/openai.yaml": read_required(repo, f"skills/{name}/agents/openai.yaml"),
            "PACKAGE.json": (
                json.dumps(
                    {
                        "name": name,
                        "entrypoint": "SKILL.md",
                        "source": entrypoint,
                        "owner": component["owner"],
                        "shared_references": list(SHARED_REFERENCES),
                        "daily_lesson_pack_version": version,
                    },
                    indent=2,
                )
                + "\n"
            ).encode("utf-8"),
        }

        for relative_path in SHARED_REFERENCES:
            package_files[relative_path] = read_required(repo, relative_path)

        if name == "dlp-pack-qa":
            for relative_path in QA_ONLY_FILES:
                package_files[relative_path] = read_required(repo, relative_path)

        zip_path = out_dir / f"{name}.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for relative_path in sorted(package_files):
                write_bytes(archive, f"{name}/{relative_path}", package_files[relative_path])
        package_paths.append(zip_path)

    bundle_path = out_dir / "daily-lesson-pack-component-skills.zip"
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        write_bytes(bundle, "registry.json", registry_path.read_bytes())
        for package in sorted(package_paths):
            write_bytes(bundle, package.name, package.read_bytes())

    print(f"Packaged {len(package_paths)} component skills for {version}")
    for path in package_paths:
        print(path)
    print(bundle_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
