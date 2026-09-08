#!/usr/bin/env python3
"""Supported Daily Lesson Pack staging/release entry point.

This command does not generate pedagogical content. Component skills and
canonical content records must already exist. It validates/stages the candidate
and optionally requests release through the repository-owned final audit.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dlp_build_runtime import REQUIRED_RELEASE_EVIDENCE, promote_release, stage_candidate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--content", type=Path, required=True)
    parser.add_argument("--component-record", type=Path, required=True)
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="Run root containing candidate/ and released/")
    parser.add_argument(
        "--release-evidence-dir",
        type=Path,
        help=(
            "Optional directory containing contract.json, year_profile.json, typography.json, "
            "containment.json, visual.json, semantic_review.json, warning_ledger.json, "
            "visual_review.json, semantic_trace.json and visual_trace.json"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        staged = stage_candidate(
            args.out,
            request_path=args.request,
            context_path=args.context,
            content_path=args.content,
            component_record_path=args.component_record,
            deck_path=args.deck,
            manifest_path=args.manifest,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
        return 1

    if args.release_evidence_dir is None:
        print(json.dumps(staged, indent=2))
        return 0

    evidence = {
        key: args.release_evidence_dir / f"{key}.json"
        for key in REQUIRED_RELEASE_EVIDENCE
    }
    result = promote_release(args.out / "candidate", args.out / "released", evidence)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"CANDIDATE", "RELEASED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
