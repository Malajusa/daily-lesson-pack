#!/usr/bin/env python3
"""Aggregate repository-owned DLP audits into one fail-closed release result."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


GENERIC_EVIDENCE = re.compile(r"^(?:checked|reviewed|intentional|looks good|acceptable|pass)$", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--year-profile", type=Path, required=True)
    parser.add_argument("--typography", type=Path, required=True)
    parser.add_argument("--containment", type=Path, required=True)
    parser.add_argument("--visual", type=Path, required=True)
    parser.add_argument("--semantic-review", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    deck_hash = sha256(args.deck)
    failures: list[str] = []
    reports: dict[str, dict] = {}
    for name in ("contract", "year_profile", "typography", "containment", "visual"):
        path = getattr(args, name)
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name} report unreadable: {exc}")
            continue
        reports[name] = report
        status = str(report.get("overall_status", report.get("status", ""))).lower()
        if status != "pass":
            failures.append(f"{name} report status is {status or 'missing'}")
        report_hash = str(report.get("artifact_sha256", "")).lower()
        if not report_hash:
            failures.append(f"{name} report is not bound to a deck SHA-256")
        elif report_hash != deck_hash:
            failures.append(f"{name} report belongs to another deck")

    try:
        semantic = json.loads(args.semantic_review.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        semantic = {}
        failures.append(f"semantic review unreadable: {exc}")
    expected_generation_run = (
        reports.get("contract", {})
        .get("summary", {})
        .get("component_acceptance", {})
        .get("generation_run_id")
    )
    if str(semantic.get("artifact_sha256", "")).lower() != deck_hash:
        failures.append("semantic review is not bound to this deck")
    semantic_run = str(semantic.get("run_id", "")).strip()
    semantic_generator_run = str(semantic.get("generator_run_id", "")).strip()
    if not str(semantic.get("reviewer", "")).strip() or not semantic_run or not semantic_generator_run:
        failures.append("semantic review needs a reviewer, run_id and generator_run_id")
    elif semantic_run == semantic_generator_run:
        failures.append("semantic review run must differ from the generation run")
    if expected_generation_run and semantic_generator_run != expected_generation_run:
        failures.append("semantic review identifies the wrong generation run")
    visual_review = reports.get("visual", {}).get("independent_review", {})
    if expected_generation_run and visual_review.get("generator_run_id") != expected_generation_run:
        failures.append("visual review identifies the wrong generation run")
    checks = semantic.get("checks")
    if not isinstance(checks, list) or not checks:
        failures.append("semantic review needs evidence-bearing checks")
    else:
        for check in checks:
            evidence = str(check.get("evidence", "")).strip() if isinstance(check, dict) else ""
            if not isinstance(check, dict) or str(check.get("result", "")).upper() != "PASS" or len(evidence) < 20 or GENERIC_EVIDENCE.fullmatch(evidence):
                failures.append("semantic review contains an unsupported or failed check")
                break

    result = {
        "status": "PASS" if not failures else "FAIL",
        "artifact_sha256": deck_hash,
        "inputs": {name: str(getattr(args, name)) for name in ("contract", "year_profile", "typography", "containment", "visual")},
        "semantic_review": str(args.semantic_review),
        "failures": failures,
        "policy": "Only repository-owned generic audits may certify release; deck-specific expected strings or slide counts are not release gates.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
