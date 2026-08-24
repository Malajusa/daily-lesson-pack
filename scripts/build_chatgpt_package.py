#!/usr/bin/env python3
"""Build the complete ChatGPT Daily Lesson Pack installation ZIP.

The repository remains the source of truth. The generated package contains the
orchestrator, all component contracts, registration metadata, shared standards,
the regression benchmark, runtime QA scripts and a verifiable package manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


SHARED_REFERENCES = (
    "references/slide-deck-quality-standards.md",
    "references/semantic-colour-standard.md",
    "references/panel-containment-standard.md",
)

ROOT_RUNTIME_FILES = (
    "SKILL.md",
    "VERSION",
    "agents/openai.yaml",
    "skills/registry.json",
    *SHARED_REFERENCES,
    "examples/benchmarks/t3w6-monday-modular-regression.md",
    "scripts/audit_slide_typography.py",
    "scripts/audit_panel_containment.py",
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


def package_json(component: dict[str, str], version: str) -> bytes:
    payload = {
        "name": component["name"],
        "entrypoint": "SKILL.md",
        "source": component["entrypoint"],
        "owner": component["owner"],
        "shared_references": list(SHARED_REFERENCES),
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
        files[f"{component_root}/SKILL.md"] = skill_text
        files[f"{component_root}/PACKAGE.json"] = package_json(component, version)
        files[f"{component_root}/agents/openai.yaml"] = read_required(
            repo, f"{component_root}/agents/openai.yaml"
        )

        for reference in SHARED_REFERENCES:
            files[f"{component_root}/{reference}"] = read_required(repo, reference)

        if name == "dlp-pack-qa":
            benchmark = "examples/benchmarks/t3w6-monday-modular-regression.md"
            files[f"{component_root}/{benchmark}"] = read_required(repo, benchmark)
            for script in (
                "scripts/audit_slide_typography.py",
                "scripts/audit_panel_containment.py",
            ):
                files[f"{component_root}/{script}"] = read_required(repo, script)

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
