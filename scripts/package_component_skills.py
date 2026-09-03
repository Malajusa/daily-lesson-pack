#!/usr/bin/env python3
"""Build self-contained Daily Lesson Pack component-skill ZIPs."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


COMMON_REFERENCES = (
    "references/slide-deck-quality-standards.md",
    "references/semantic-colour-standard.md",
    "references/panel-containment-standard.md",
    "references/default-pack-profile.json",
    "references/component-instance-contract.md",
)

YEAR_LEVEL_CONTEXT_REFERENCE = "references/year-level-context-contract.md"
YEAR_LEVEL_PROFILE_REFERENCES = (
    "references/year-level-profiles/year-4-5.md",
    "references/year-level-profiles/year-6.md",
)
MATH_REFERENCE = "references/universal-maths-instruction-canon.md"
FRACTION_REFERENCE = "references/fraction-equivalence-standard.md"
SHARED_CONTEXT_REFERENCE = "references/shared-class-context-contract.md"
VISUAL_EXEMPLAR_REFERENCE = "references/visual-exemplar-standard.md"
VISUAL_EXEMPLAR_ASSET = (
    "assets/visual-exemplars/t3w6-tuesday-edited-visual-exemplar.pptx"
)
UNIVERSAL_MATHS_BENCHMARK = "examples/benchmarks/universal-maths-canon-regression.md"
MEMORY_INDEPENDENT_BENCHMARK = (
    "examples/benchmarks/memory-independent-wednesday-regression.md"
)
YEAR_PROFILE_ISOLATION_BENCHMARK = (
    "examples/benchmarks/year-profile-isolation-regression.md"
)
YEAR_PROFILE_AUDIT = "scripts/audit_year_profile_context.py"

QA_ONLY_FILES = (
    "examples/benchmarks/t3w6-monday-modular-regression.md",
    "examples/benchmarks/t3w6-tuesday-release-regression.md",
    "examples/benchmarks/t3w6-thursday-literacy-regression.md",
    UNIVERSAL_MATHS_BENCHMARK,
    MEMORY_INDEPENDENT_BENCHMARK,
    YEAR_PROFILE_ISOLATION_BENCHMARK,
    "examples/benchmarks/t3w7-thursday-known-failure.md",
    "scripts/audit_pack_contract.py",
    YEAR_PROFILE_AUDIT,
    "scripts/audit_slide_typography.py",
    "scripts/audit_panel_containment.py",
    "scripts/audit_visual_exemplar.py",
    "scripts/audit_release_bundle.py",
    "examples/context-record-wednesday.json",
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

        component_references = (
            *COMMON_REFERENCES,
            YEAR_LEVEL_CONTEXT_REFERENCE,
            *YEAR_LEVEL_PROFILE_REFERENCES,
        )
        if name in {"dlp-maths-lesson", "dlp-pack-qa"}:
            component_references = (*component_references, MATH_REFERENCE, FRACTION_REFERENCE)
        if name == "dlp-pack-qa":
            component_references = (
                *component_references,
                SHARED_CONTEXT_REFERENCE,
                VISUAL_EXEMPLAR_REFERENCE,
            )

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
                        "shared_references": list(component_references),
                        "daily_lesson_pack_version": version,
                    },
                    indent=2,
                )
                + "\n"
            ).encode("utf-8"),
        }

        for relative_path in component_references:
            package_files[relative_path] = read_required(repo, relative_path)

        if name in {"dlp-maths-lesson", "dlp-pack-qa"}:
            package_files[UNIVERSAL_MATHS_BENCHMARK] = read_required(
                repo, UNIVERSAL_MATHS_BENCHMARK
            )
            package_files[YEAR_PROFILE_ISOLATION_BENCHMARK] = read_required(
                repo, YEAR_PROFILE_ISOLATION_BENCHMARK
            )

        if name == "dlp-pack-qa":
            for relative_path in QA_ONLY_FILES:
                package_files[relative_path] = read_required(repo, relative_path)
            package_files[VISUAL_EXEMPLAR_ASSET] = read_required(
                repo, VISUAL_EXEMPLAR_ASSET
            )

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
