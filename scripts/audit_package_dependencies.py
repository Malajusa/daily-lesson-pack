#!/usr/bin/env python3
"""Validate a built Daily Lesson Pack skill tree before installation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import subprocess
from pathlib import Path

from year_profile_registry import PROFILE_REGISTRY_FILES, YearProfileRegistry
from agent_protocol import ProtocolError


REFERENCE_RE = re.compile(
    r"`((?:\.\./)*(?:assets|examples|references|scripts|skills)/"
    r"[A-Za-z0-9_.<>/-]+)`"
)
ICON_RE = re.compile(
    r"^\s*icon_(?:small|large):\s*[\"']?([^\"'\s#]+)", re.MULTILINE
)
FRONTMATTER_NAME_RE = re.compile(r"^name:\s*([^\n]+)$", re.MULTILINE)
MANDATORY_RUNTIME_FILES = (
    *PROFILE_REGISTRY_FILES,
    "scripts/build_daily_pack.py",
    "scripts/dlp_build_runtime.py",
    "requirements.txt",
    "skills/registry.v2.json",
    "agents/maths-critic.md",
    "scripts/agent_orchestrator.py",
    "scripts/agent_protocol.py",
    "scripts/agent_registry.py",
    "scripts/agent_state.py",
    "scripts/agent_adapter.py",
    "scripts/agent_pipeline.py",
    "scripts/build_execution_plan.py",
    "scripts/validate_agent_artifacts.py",
    "schemas/agent-request.schema.json",
    "schemas/agent-result.schema.json",
    "schemas/component-result.schema.json",
    "schemas/defect.schema.json",
    "schemas/execution-plan.schema.json",
    "schemas/registry-v2.schema.json",
    "schemas/review-request.schema.json",
    "schemas/review-result.schema.json",
    "schemas/run-context.schema.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument(
        "--component",
        action="store_true",
        help="Validate a standalone component package without a root manifest or registry",
    )
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def relative_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "PACKAGE-MANIFEST.json"
    }


def validate_manifest(root: Path, failures: list[str]) -> None:
    manifest_path = root / "PACKAGE-MANIFEST.json"
    if not manifest_path.is_file():
        failures.append("Missing PACKAGE-MANIFEST.json")
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version_path = root / "VERSION"
    if not version_path.is_file():
        failures.append("Missing VERSION")
        return
    version = version_path.read_text(encoding="utf-8").strip()
    if manifest.get("version") != version:
        failures.append(
            f"Manifest version {manifest.get('version')!r} does not match VERSION {version!r}"
        )

    entries = manifest.get("files")
    if not isinstance(entries, list):
        failures.append("Manifest files must be a list")
        return

    declared = {entry.get("path") for entry in entries}
    actual = relative_files(root)
    for path in sorted(actual - declared):
        failures.append(f"Undeclared file: {path}")
    for path in sorted(declared - actual):
        failures.append(f"Declared file missing: {path}")

    for entry in entries:
        relative = entry.get("path")
        if not isinstance(relative, str) or relative not in actual:
            continue
        path = root / relative
        data = path.read_bytes()
        if entry.get("bytes") != len(data):
            failures.append(f"Manifest size mismatch: {relative}")
        if entry.get("sha256") != hashlib.sha256(data).hexdigest():
            failures.append(f"Manifest hash mismatch: {relative}")


def validate_markdown_references(root: Path, failures: list[str]) -> None:
    skill_files = [root / "SKILL.md", *sorted((root / "skills").glob("*/SKILL.md"))]
    for skill_file in skill_files:
        if not skill_file.is_file():
            failures.append(f"Missing skill entrypoint: {skill_file.relative_to(root)}")
            continue
        text = skill_file.read_text(encoding="utf-8")
        for token in REFERENCE_RE.findall(text):
            if "<" in token or ">" in token:
                continue
            target = (skill_file.parent / token).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                failures.append(
                    f"Reference escapes package root: {skill_file.relative_to(root)} -> {token}"
                )
                continue
            expects_directory = token.endswith("/")
            exists_as_expected = target.is_dir() if expects_directory else target.is_file()
            if not exists_as_expected:
                failures.append(
                    f"Missing referenced {'directory' if expects_directory else 'file'}: "
                    f"{skill_file.relative_to(root)} -> {token}"
                )


def validate_metadata_icons(root: Path, failures: list[str]) -> None:
    metadata_files = [
        root / "agents" / "openai.yaml",
        *sorted((root / "skills").glob("*/agents/openai.yaml")),
    ]
    for metadata_file in metadata_files:
        if not metadata_file.is_file():
            failures.append(f"Missing agent metadata: {metadata_file.relative_to(root)}")
            continue
        text = metadata_file.read_text(encoding="utf-8")
        skill_root = metadata_file.parent.parent
        for token in ICON_RE.findall(text):
            if not (skill_root / token).is_file():
                failures.append(
                    f"Missing UI icon: {metadata_file.relative_to(root)} -> {token}"
                )


def validate_registry(root: Path, failures: list[str]) -> None:
    registry_path = root / "skills" / "registry.json"
    if not registry_path.is_file():
        failures.append("Missing skills/registry.json")
        return
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    components = registry.get("components")
    if not isinstance(components, list) or len(components) != 8:
        failures.append("Component registry must contain exactly eight components")
        return

    names: set[str] = set()
    for component in components:
        name = component.get("name")
        if not isinstance(name, str) or name in names:
            failures.append(f"Invalid or duplicate component name: {name!r}")
            continue
        names.add(name)
        skill_file = root / "skills" / name / "SKILL.md"
        if not skill_file.is_file():
            failures.append(f"Missing registered component: {name}")
            continue
        match = FRONTMATTER_NAME_RE.search(skill_file.read_text(encoding="utf-8"))
        if not match or match.group(1).strip().strip("\"'") != name:
            failures.append(f"Component frontmatter name mismatch: {name}")


def validate_provenance(root: Path, failures: list[str]) -> None:
    path = root / "RELEASE-PROVENANCE.json"
    if not path.is_file():
        failures.append("Missing RELEASE-PROVENANCE.json")
        return
    provenance = json.loads(path.read_text(encoding="utf-8"))
    version_path = root / "VERSION"
    if not version_path.is_file():
        failures.append("Missing VERSION")
        return
    version = version_path.read_text(encoding="utf-8").strip()
    if provenance.get("version") != version:
        failures.append("Release provenance version does not match VERSION")
    base_commit = provenance.get("base_commit")
    if not isinstance(base_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", base_commit):
        failures.append("Release provenance requires a full 40-character Git commit")
    sources = provenance.get("reconciled_sources")
    if not isinstance(sources, list) or len(sources) < 2:
        failures.append("Release provenance must identify both reconciled source lines")


def validate_runtime(root: Path, failures: list[str]) -> None:
    for relative in MANDATORY_RUNTIME_FILES:
        if not (root / relative).is_file():
            failures.append(f"Missing mandatory runtime: {relative}")

    runtime_path = root / "scripts" / "dlp_build_runtime.py"
    if not runtime_path.is_file():
        return

    # Import in a clean interpreter rooted at the extracted package. Importing
    # in this process can accidentally reuse modules from the source checkout.
    code = """import sys
sys.path.insert(0, sys.argv[1])
import dlp_build_runtime as runtime
from agent_registry import AgentRegistry
from agent_orchestrator import DailyPackOrchestrator
AgentRegistry.load()
for name in ('stage_candidate','promote_release','validate_resolved_context'):
    if not callable(getattr(runtime,name,None)):
        raise ValueError('Missing mandatory runtime callable: '+name)
"""
    try:
        result = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(root / "scripts")],
                                cwd=str(root), capture_output=True, text=True, timeout=60)
        if result.returncode:
            failures.append("Mandatory runtime is not importable: " + result.stderr[-2000:])
    except (OSError, subprocess.TimeoutExpired) as exc:
        failures.append("Mandatory runtime is not importable: " + str(exc))


def main() -> int:
    args = parse_args()
    root = args.skill_root.resolve()
    failures: list[str] = []

    if not root.is_dir():
        failures.append(f"Skill root is not a directory: {root}")
    else:
        try:
            YearProfileRegistry.load(root)
        except ProtocolError as exc:
            failures.append(str(exc))
        if not args.component:
            validate_manifest(root, failures)
        validate_markdown_references(root, failures)
        validate_metadata_icons(root, failures)
        if not args.component:
            validate_registry(root, failures)
            validate_provenance(root, failures)
            validate_runtime(root, failures)

    report = {
        "status": "PASS" if not failures else "FAIL",
        "skill_root": str(root),
        "failure_count": len(failures),
        "failures": failures,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
