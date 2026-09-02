#!/usr/bin/env python3
"""Audit year-profile resolution and cross-component isolation for a DLP run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SUPPORTED_PROFILES = {"year-4-5", "year-6"}
RUNTIME_FIELDS = {
    "timetable",
    "mathematics_focus",
    "english_focus",
    "printing_quantity",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-record", type=Path, required=True)
    parser.add_argument("--component-record", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def load_object(path: Path, label: str, failures: list[str]) -> dict:
    if not path.is_file():
        failures.append(f"Missing {label}: {path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"Invalid {label}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"{label} must be a JSON object")
        return {}
    return value


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    context = load_object(args.context_record, "context record", failures)
    components = load_object(args.component_record, "component record", failures)

    active = context.get("active_year_profile")
    profile = ""
    profile_status = ""
    if not isinstance(active, dict):
        failures.append("Context record is missing active_year_profile")
    else:
        profile = str(active.get("value", "")).strip()
        source = str(active.get("source", "")).strip()
        resolved = active.get("resolved") is True
        profile_status = str(active.get("status", "")).strip().lower()
        if not resolved:
            failures.append("active_year_profile is unresolved")
        if profile not in SUPPORTED_PROFILES:
            failures.append(f"Unsupported active_year_profile: {profile or 'MISSING'}")
        if not source:
            failures.append("active_year_profile does not identify its profile source")

    for field in RUNTIME_FIELDS:
        entry = context.get(field)
        if not isinstance(entry, dict):
            continue
        source = str(entry.get("source", "")).lower()
        if "year-level profile" in source or "year level profile" in source:
            failures.append(
                f"Runtime field {field} incorrectly cites a year-level profile as its source"
            )

    scheduled = components.get("scheduled_components", [])
    records = components.get("components", [])
    if not isinstance(scheduled, list):
        failures.append("component record scheduled_components must be a list")
        scheduled = []
    if not isinstance(records, list):
        failures.append("component record components must be a list")
        records = []

    by_name: dict[str, dict] = {}
    for record in records:
        if not isinstance(record, dict):
            continue
        name = str(record.get("name", "")).strip()
        if name:
            by_name[name] = record

    for name in [str(item) for item in scheduled]:
        record = by_name.get(name)
        if record is None:
            continue
        component_profile = str(record.get("active_year_profile", "")).strip()
        if not component_profile:
            failures.append(f"Component {name} does not record active_year_profile")
        elif profile and component_profile != profile:
            failures.append(
                f"Component {name} profile mismatch: {component_profile} != {profile}"
            )

    release_mode = "candidate" if profile_status in {"candidate", "calibration", "scaffold"} else "normal"
    if profile == "year-6" and not profile_status:
        # The bundled Year 6 profile is currently a calibration scaffold. Requiring
        # an explicit status prevents a caller from silently treating it as mature.
        failures.append("Year 6 context must record profile status while calibration is incomplete")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "active_year_profile": profile or None,
        "profile_status": profile_status or None,
        "release_mode": release_mode,
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
