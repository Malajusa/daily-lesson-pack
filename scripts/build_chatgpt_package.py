#!/usr/bin/env python3
"""Build the complete ChatGPT Daily Lesson Pack installation ZIP.

The repository remains the source of truth. The generated package contains the
orchestrator, all component contracts, registration metadata, shared standards,
regression benchmarks, runtime QA scripts and a verifiable package manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


COMMON_REFERENCES = (
    "references/slide-deck-quality-standards.md",
    "references/semantic-colour-standard.md",
    "references/panel-containment-standard.md",
)

MATH_REFERENCE = "references/universal-maths-instruction-canon.md"
SHARED_CONTEXT_REFERENCE = "references/shared-class-context-contract.md"
VISUAL_EXEMPLAR_REFERENCE = "references/visual-exemplar-standard.md"
VISUAL_EXEMPLAR_ASSET = (
    "assets/visual-exemplars/t3w6-tuesday-edited-visual-exemplar.pptx"
)
UNIVERSAL_MATHS_BENCHMARK = "examples/benchmarks/universal-maths-canon-regression.md"
MEMORY_INDEPENDENT_BENCHMARK = (
    "examples/benchmarks/memory-independent-wednesday-regression.md"
)
REGRESSION_BENCHMARKS = (
    "examples/benchmarks/t3w6-monday-modular-regression.md",
    "examples/benchmarks/t3w6-tuesday-release-regression.md",
    "examples/benchmarks/t3w6-thursday-literacy-regression.md",
    UNIVERSAL_MATHS_BENCHMARK,
    MEMORY_INDEPENDENT_BENCHMARK,
)

ROOT_RUNTIME_FILES = (
    "SKILL.md",
    "VERSION",
    "RELEASE-PROVENANCE.json",
    "agents/openai.yaml",
    "assets/icon.svg",
    VISUAL_EXEMPLAR_ASSET,
    "skills/registry.json",
    *COMMON_REFERENCES,
    MATH_REFERENCE,
    SHARED_CONTEXT_REFERENCE,
    VISUAL_EXEMPLAR_REFERENCE,
    *REGRESSION_BENCHMARKS,
    "examples/context-record-wednesday.json",
    "scripts/audit_package_dependencies.py",
    "scripts/audit_pack_contract.py",
    "scripts/audit_slide_typography.py",
    "scripts/audit_panel_containment.py",
    "scripts/audit_visual_exemplar.py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (defaults to the script's repository)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("dist/chatgpt/daily-lesson-pack.zip"),
        help="Destination ZIP path",
    )
    return parser.parse_args()


def read_required(repo: Path, relative_path: str) -> bytes:
    source = repo / relative_path
    if not source.is_file():
        raise FileNotFoundError(f"Missing package dependency: {source}")
    return source.read_bytes()


def package_json(
    component: dict[str, str], version: str, references: tuple[str, ...]
) -> bytes:
    payload = {
        "name": component["name"],
        "entrypoint": "SKILL.md",
        "source": component["entrypoint"],
        "owner": component["owner"],
        "shared_references": list(references),
        "daily_lesson_pack_version": version,
    }
    return (json.dumps(payload, indent=2) + "\n").encode("utf-8")


def build_file_map(repo: Path) -> tuple[str, dict[str, bytes]]:
    version = read_required(repo, "VERSION").decode("utf-8").strip()
    registry = json.loads(read_required(repo, "skills/registry.json"))

    files = {path: read_required(repo, path) for path in ROOT_RUNTIME_FILES}

    for component in registry["components"]:
        name = component["name"]
        entrypoint = component["entrypoint"]
        skill_text = read_required(repo, entrypoint)
        if f"name: {name}".encode("utf-8") not in skill_text:
            raise ValueError(f"Skill name mismatch in {entrypoint}: expected {name}")

        component_root = f"skills/{name}"
        component_references = COMMON_REFERENCES
        if name in {"dlp-maths-lesson", "dlp-pack-qa"}:
            component_references = (*COMMON_REFERENCES, MATH_REFERENCE)
        if name == "dlp-pack-qa":
            component_references = (
                *component_references,
                SHARED_CONTEXT_REFERENCE,
                VISUAL_EXEMPLAR_REFERENCE,
            )

        files[f"{component_root}/SKILL.md"] = skill_text
        files[f"{component_root}/PACKAGE.json"] = package_json(
            component, version, component_references
        )
        files[f"{component_root}/agents/openai.yaml"] = read_required(
            repo, f"{component_root}/agents/openai.yaml"
        )

        for reference in component_references:
            files[f"{component_root}/{reference}"] = read_required(repo, reference)

        if name in {"dlp-maths-lesson", "dlp-pack-qa"}:
            files[f"{component_root}/{UNIVERSAL_MATHS_BENCHMARK}"] = read_required(
                repo, UNIVERSAL_MATHS_BENCHMARK
            )

        if name == "dlp-pack-qa":
            for benchmark in REGRESSION_BENCHMARKS:
                files[f"{component_root}/{benchmark}"] = read_required(repo, benchmark)
            for script in (
                "scripts/audit_pack_contract.py",
                "scripts/audit_slide_typography.py",
                "scripts/audit_panel_containment.py",
                "scripts/audit_visual_exemplar.py",
            ):
                files[f"{component_root}/{script}"] = read_required(repo, script)
            files[f"{component_root}/{VISUAL_EXEMPLAR_ASSET}"] = read_required(
                repo, VISUAL_EXEMPLAR_ASSET
            )
            files[f"{component_root}/examples/context-record-wednesday.json"] = read_required(
                repo, "examples/context-record-wednesday.json"
            )

    return version, files


def manifest(version: str, files: dict[str, bytes]) -> bytes:
    entries = []
    for path in sorted(files):
        data = files[path]
        entries.append(
            {
                "path": path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    return (json.dumps({"version": version, "files": entries}, indent=2) + "\n").encode(
        "utf-8"
    )


def write_deterministic(archive: zipfile.ZipFile, path: str, data: bytes) -> None:
    info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, data)


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    destination = args.out
    if not destination.is_absolute():
        destination = repo / destination
    destination.parent.mkdir(parents=True, exist_ok=True)

    version, files = build_file_map(repo)
    files["PACKAGE-MANIFEST.json"] = manifest(version, files)

    package_root = "daily-lesson-pack"
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            write_deterministic(archive, f"{package_root}/{path}", files[path])

    print(f"Built Daily Lesson Pack {version}")
    print(f"Files: {len(files)}")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
