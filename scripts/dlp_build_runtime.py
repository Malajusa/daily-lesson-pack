#!/usr/bin/env python3
"""Fail-closed staging and release helpers for Daily Lesson Pack artefacts.

This module does not author lesson content. It validates repository-owned runtime
records, stages a candidate artefact set, and delegates classroom-ready release
to audit_release_bundle.py.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent

def load_content_components() -> set[str]:
    # Registry validation is fail-closed; never fall back to a stale hardcoded list.
    from agent_registry import AgentRegistry
    registry = AgentRegistry.load(ROOT.parent / "skills" / "registry.v2.json")
    return {agent.id for agent in registry.generators()}


CONTENT_COMPONENTS = load_content_components()

REQUIRED_CONTEXT_FIELDS = (
    "active_year_profile",
    "pack_profile",
    "date",
    "term_week",
    "day",
    "timetable",
    "mathematics_focus",
    "english_focus",
    "lesson_status",
)

REQUIRED_RELEASE_EVIDENCE = (
    "contract",
    "year_profile",
    "typography",
    "containment",
    "visual",
    "semantic_review",
    "warning_ledger",
    "visual_review",
    "semantic_trace",
    "visual_trace",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def validate_request(request: dict) -> list[str]:
    errors: list[str] = []
    if request.get("schema_version") != 1:
        errors.append("request schema_version must be 1")
    if not str(request.get("requested_date", "")).strip():
        errors.append("request requested_date is required")
    requested_output = str(request.get("requested_output", "")).strip().lower()
    if requested_output not in {"powerpoint", "pptx", "deck"}:
        errors.append("request requested_output must identify the teaching deck")
    return errors


def validate_resolved_context(context: dict) -> list[str]:
    errors: list[str] = []
    if context.get("schema_version") != 2:
        errors.append("context schema_version must be 2")

    for name in REQUIRED_CONTEXT_FIELDS:
        entry = context.get(name)
        if not isinstance(entry, dict):
            errors.append(f"context field {name} is missing")
            continue
        if entry.get("resolved") is not True or entry.get("value") in (None, "", [], {}):
            errors.append(f"context field {name} is unresolved")
        if not str(entry.get("source", "")).strip():
            errors.append(f"context field {name} has no source provenance")

    instances = context.get("timetable_instances")
    if not isinstance(instances, list) or not instances:
        errors.append("context timetable_instances must contain scheduled instances")
        return errors

    seen: set[str] = set()
    for index, instance in enumerate(instances):
        if not isinstance(instance, dict):
            errors.append(f"timetable instance {index} must be an object")
            continue
        instance_id = str(instance.get("id", "")).strip()
        owner = str(instance.get("owner", "")).strip()
        if not instance_id:
            errors.append(f"timetable instance {index} has no id")
        elif instance_id in seen:
            errors.append(f"timetable instance id {instance_id} is duplicated")
        seen.add(instance_id)
        if owner not in CONTENT_COMPONENTS:
            errors.append(f"timetable instance {instance_id or index} has unknown owner {owner!r}")
        duration = instance.get("duration_minutes")
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"timetable instance {instance_id or index} has invalid duration_minutes")

    unresolved = context.get("unresolved_fields", [])
    if unresolved not in (None, []) and bool(unresolved):
        errors.append("context contains unresolved_fields and cannot be released")
    return errors


def _component_entries(component_record: dict) -> list[dict]:
    # `components` is the canonical schema-v2 key. `instances` is accepted here
    # only so the staging validator can report a useful candidate error for
    # early/runtime fixtures; final repository audits still enforce canonical v2.
    entries = component_record.get("components")
    if entries is None:
        entries = component_record.get("instances")
    return entries if isinstance(entries, list) else []


def validate_component_record(context: dict, component_record: dict) -> list[str]:
    errors: list[str] = []
    if component_record.get("schema_version") != 2:
        errors.append("component record schema_version must be 2")
    if not str(component_record.get("generation_run_id", "")).strip():
        errors.append("component record generation_run_id is required")

    context_run_id = str(context.get("generation_run_id", "")).strip()
    if context_run_id and component_record.get("generation_run_id") != context_run_id:
        errors.append("component record generation_run_id does not match resolved context")

    profile_entry = context.get("active_year_profile", {})
    active_profile = str(profile_entry.get("value", "")).strip() if isinstance(profile_entry, dict) else ""
    entries = _component_entries(component_record)
    scheduled = context.get("timetable_instances") if isinstance(context.get("timetable_instances"), list) else []

    by_id: dict[str, list[dict]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("component entries must be objects")
            continue
        by_id.setdefault(str(entry.get("instance_id", "")).strip(), []).append(entry)

    for instance in scheduled:
        if not isinstance(instance, dict):
            continue
        instance_id = str(instance.get("id", "")).strip()
        owner = str(instance.get("owner", "")).strip()
        matches = by_id.get(instance_id, [])
        if len(matches) != 1:
            errors.append(f"scheduled instance {instance_id} requires exactly one component result")
            continue
        component = matches[0]
        if str(component.get("owner", "")).strip() != owner:
            errors.append(f"scheduled instance {instance_id} owner does not match component owner")
        if component.get("status") != "PASS":
            errors.append(f"scheduled instance {instance_id} must record PASS before assembly")
        component_profile = str(component.get("active_year_profile", active_profile)).strip()
        if active_profile and component_profile != active_profile:
            errors.append(f"scheduled instance {instance_id} uses a different year profile from the context")
        estimate = component.get("estimated_minutes")
        duration = instance.get("duration_minutes")
        if isinstance(estimate, (int, float)) and isinstance(duration, (int, float)) and estimate > duration:
            errors.append(f"scheduled instance {instance_id} exceeds its timetable duration")

    scheduled_ids = {str(item.get("id", "")).strip() for item in scheduled if isinstance(item, dict)}
    extra_ids = {key for key in by_id if key and key not in scheduled_ids}
    if extra_ids:
        errors.append("component record contains unscheduled instance results: " + ", ".join(sorted(extra_ids)))
    return errors


def _load_and_validate_inputs(
    *,
    request_path: Path,
    context_path: Path,
    content_path: Path,
    component_record_path: Path,
    deck_path: Path,
    manifest_path: Path,
) -> tuple[dict, dict, dict, dict, dict]:
    paths = {
        "request": Path(request_path),
        "context": Path(context_path),
        "content": Path(content_path),
        "component record": Path(component_record_path),
        "deck": Path(deck_path),
        "manifest": Path(manifest_path),
    }
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        raise ValueError("missing build inputs: " + ", ".join(missing))

    request = read_json(paths["request"])
    context = read_json(paths["context"])
    content = read_json(paths["content"])
    components = read_json(paths["component record"])
    manifest = read_json(paths["manifest"])

    errors = validate_request(request)
    errors.extend(validate_resolved_context(context))
    errors.extend(validate_component_record(context, components))
    if content.get("schema_version") != 3:
        errors.append("content schema_version must be 3")
    if content.get("instances") != context.get("timetable_instances"):
        errors.append("content instances must exactly match resolved timetable_instances")
    if manifest.get("schema_version") != 3:
        errors.append("manifest schema_version must be 3")
    if errors:
        raise ValueError("\n".join(errors))
    return request, context, content, components, manifest


def stage_candidate(
    run_root: Path,
    *,
    request_path: Path,
    context_path: Path,
    content_path: Path,
    component_record_path: Path,
    deck_path: Path,
    manifest_path: Path,
) -> dict:
    """Validate and stage a candidate. Never creates or mutates released/."""
    _load_and_validate_inputs(
        request_path=request_path,
        context_path=context_path,
        content_path=content_path,
        component_record_path=component_record_path,
        deck_path=deck_path,
        manifest_path=manifest_path,
    )
    run_root = Path(run_root)
    candidate = run_root / "candidate"
    if candidate.exists():
        shutil.rmtree(candidate)
    candidate.mkdir(parents=True, exist_ok=True)

    copies = {
        "request.json": Path(request_path),
        "context.json": Path(context_path),
        "content.json": Path(content_path),
        "component-record.json": Path(component_record_path),
        "pack.pptx": Path(deck_path),
        "manifest.json": Path(manifest_path),
    }
    for destination, source in copies.items():
        shutil.copy2(source, candidate / destination)

    status = {
        "status": "CANDIDATE",
        "candidate": str(candidate),
        "artifact_sha256": sha256(candidate / "pack.pptx"),
        "manifest_sha256": sha256(candidate / "manifest.json"),
        "release_ready": False,
        "reason": "Independent semantic/visual review and final repository release audit are still required.",
    }
    (candidate / "candidate-status.json").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    return status


def promote_release(
    candidate_dir: Path,
    released_dir: Path,
    evidence: dict[str, Path],
    *,
    runner: Callable[..., object] = subprocess.run,
) -> dict:
    """Run the repository release authority and promote only its same-hash PASS."""
    candidate = Path(candidate_dir)
    released = Path(released_dir)
    required_candidate = (
        candidate / "pack.pptx",
        candidate / "manifest.json",
        candidate / "content.json",
        candidate / "context.json",
        candidate / "component-record.json",
    )
    if not all(path.is_file() for path in required_candidate):
        return {"status": "CANDIDATE", "reason": "Candidate artefact set is incomplete."}

    missing_evidence = [key for key in REQUIRED_RELEASE_EVIDENCE if key not in evidence or not Path(evidence[key]).is_file()]
    if missing_evidence:
        return {
            "status": "CANDIDATE",
            "reason": "Release evidence is incomplete: " + ", ".join(missing_evidence),
        }

    release_report = candidate / "release-audit.json"
    release_report.unlink(missing_ok=True)
    command = [
        sys.executable,
        str(ROOT / "audit_release_bundle.py"),
        "--deck", str(candidate / "pack.pptx"),
        "--contract", str(evidence["contract"]),
        "--year-profile", str(evidence["year_profile"]),
        "--typography", str(evidence["typography"]),
        "--containment", str(evidence["containment"]),
        "--visual", str(evidence["visual"]),
        "--semantic-review", str(evidence["semantic_review"]),
        "--out", str(release_report),
        "--manifest", str(candidate / "manifest.json"),
        "--content", str(candidate / "content.json"),
        "--context-record", str(candidate / "context.json"),
        "--component-record", str(candidate / "component-record.json"),
        "--warning-ledger", str(evidence["warning_ledger"]),
        "--visual-review", str(evidence["visual_review"]),
        "--semantic-trace", str(evidence["semantic_trace"]),
        "--visual-trace", str(evidence["visual_trace"]),
    ]
    result = runner(command, capture_output=True, text=True)
    if getattr(result, "returncode", 1) != 0 or not release_report.is_file():
        return {
            "status": "CANDIDATE",
            "reason": "Repository release audit did not pass.",
            "stderr": str(getattr(result, "stderr", ""))[-500:],
        }

    try:
        report = read_json(release_report)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"status": "CANDIDATE", "reason": f"Release report is invalid: {exc}"}

    deck_hash = sha256(candidate / "pack.pptx")
    manifest_hash = sha256(candidate / "manifest.json")
    if report.get("status") != "PASS":
        return {"status": "CANDIDATE", "reason": "Final release report status is not PASS."}
    if str(report.get("artifact_sha256", "")).lower() != deck_hash:
        return {"status": "CANDIDATE", "reason": "Release report is not bound to the current deck hash."}
    if str(report.get("manifest_sha256", "")).lower() != manifest_hash:
        return {"status": "CANDIDATE", "reason": "Release report is not bound to the current manifest hash."}

    if released.exists():
        shutil.rmtree(released)
    released.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidate / "pack.pptx", released / "pack.pptx")
    shutil.copy2(release_report, released / "release.json")
    return {
        "status": "RELEASED",
        "released": str(released),
        "artifact_sha256": deck_hash,
        "manifest_sha256": manifest_hash,
    }
