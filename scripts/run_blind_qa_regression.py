#!/usr/bin/env python3
"""Run a known-failure Daily Lesson Pack QA fixture without exposing its oracle.

The live reviewer process operates in a temporary repository copy that excludes
case-specific answer material. The parent process scores the completed review
against the machine-readable oracle only after the reviewer exits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

REGRESSION_TEST = Path("tests/test_t3w8_mass_narrative_qa_fixture.py")

REVIEW_INSTRUCTIONS = """# Independent DLP Pack QA regression review

Use `skills/dlp-pack-qa/SKILL.md` as the governing QA contract and follow the
repository references it requires. Independently review `input/deck.pptx`
against `input/request-context.md`.

Do not repair the deck. Do not look outside this workspace for case-specific
answers. The known-answer review and oracle are intentionally absent.

Write one UTF-8 JSON object to the path in `DLP_QA_OUTPUT` with this shape:

{
  "verdict": "PASS or FAIL",
  "findings": [
    {
      "component": "owning component or orchestrator",
      "severity": "release_blocking, major, minor, or advisory",
      "slides": [1, 2],
      "summary": "concise defect statement",
      "details": "evidence and required correction"
    }
  ],
  "strengths": ["optional evidence-based strengths"]
}

Use PowerPoint slide numbers in `slides`. For a finding about delivery/runtime
metadata rather than a specific slide, use an empty list. Return every defect
you judge material under the current QA contract; do not aim for a predetermined
number of findings.
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path, root: Path) -> Path:
    return path.resolve().relative_to(root.resolve())


def build_blind_workspace(
    repo_root: Path, case_dir: Path, deck: Path, workspace: Path
) -> Path:
    """Copy the repo while excluding case-specific answer material."""

    repo_root = repo_root.resolve()
    case_rel = _relative(case_dir, repo_root)
    deck_rel = _relative(deck, repo_root)
    regression_test_rel = REGRESSION_TEST

    if workspace.exists():
        shutil.rmtree(workspace)

    root_ignored = {".git", "dist", ".venv", "venv", ".pytest_cache", "__pycache__"}

    def ignore(directory: str, names: list[str]) -> set[str]:
        current = Path(directory).resolve()
        current_rel = current.relative_to(repo_root)
        ignored: set[str] = set()
        for name in names:
            child_rel = current_rel / name
            if current_rel == Path(".") and name in root_ignored:
                ignored.add(name)
                continue
            if child_rel == case_rel or child_rel == deck_rel or child_rel == regression_test_rel:
                ignored.add(name)
                continue
            if name == "__pycache__":
                ignored.add(name)
        return ignored

    shutil.copytree(repo_root, workspace, ignore=ignore)

    input_dir = workspace / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(deck, input_dir / "deck.pptx")
    shutil.copy2(case_dir / "blind-request-context.md", input_dir / "request-context.md")
    (input_dir / "review-instructions.md").write_text(REVIEW_INSTRUCTIONS, encoding="utf-8")
    return workspace


def _normalise(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value)).casefold()
    return " ".join(text.split())


def _finding_text(finding: dict[str, Any]) -> str:
    values = [
        finding.get("component", ""),
        finding.get("severity", ""),
        finding.get("summary", ""),
        finding.get("details", ""),
    ]
    return _normalise(" ".join(str(value) for value in values))


def _finding_slides(finding: dict[str, Any]) -> set[int]:
    slides: set[int] = set()
    for value in finding.get("slides", []) or []:
        try:
            slides.add(int(value))
        except (TypeError, ValueError):
            continue
    return slides


def _matches(expected: dict[str, Any], finding: dict[str, Any]) -> bool:
    match = expected.get("match", {})
    terms = [_normalise(term) for term in match.get("text_any", []) if str(term).strip()]
    text = _finding_text(finding)
    if terms and not any(term in text for term in terms):
        return False

    expected_slides = {int(value) for value in match.get("slides_any", [])}
    if expected_slides:
        actual_slides = _finding_slides(finding)
        if not actual_slides.intersection(expected_slides):
            return False
    return True


def score_review(review: dict[str, Any], oracle: dict[str, Any]) -> dict[str, Any]:
    """Deterministically compare a completed blind review with the oracle."""

    findings = review.get("findings", [])
    if not isinstance(findings, list):
        raise ValueError("Review field 'findings' must be a list")

    missing_required: list[str] = []
    for expected in oracle.get("required_findings", []):
        if not any(_matches(expected, finding) for finding in findings if isinstance(finding, dict)):
            missing_required.append(expected["id"])

    guards_triggered: list[str] = []
    for guard in oracle.get("must_not_flag", []):
        if any(_matches(guard, finding) for finding in findings if isinstance(finding, dict)):
            guards_triggered.append(guard["id"])

    expected_verdict = _normalise(oracle.get("expected_release", ""))
    actual_verdict = _normalise(review.get("verdict", ""))
    verdict_matches = actual_verdict == expected_verdict

    return {
        "passed": verdict_matches and not missing_required and not guards_triggered,
        "expected_verdict": oracle.get("expected_release"),
        "actual_verdict": review.get("verdict"),
        "missing_required": missing_required,
        "false_positive_guards_triggered": guards_triggered,
        "finding_count": len(findings),
    }


def run_reviewer(runner: str, workspace: Path, output_path: Path, timeout: int) -> None:
    command = shlex.split(runner)
    if not command:
        raise ValueError("Runner command is empty")

    env = os.environ.copy()
    env.update(
        {
            "DLP_QA_WORKSPACE": str(workspace),
            "DLP_QA_DECK": str(workspace / "input/deck.pptx"),
            "DLP_QA_SKILL": str(workspace / "skills/dlp-pack-qa/SKILL.md"),
            "DLP_QA_REQUEST_CONTEXT": str(workspace / "input/request-context.md"),
            "DLP_QA_REVIEW_INSTRUCTIONS": str(workspace / "input/review-instructions.md"),
            "DLP_QA_OUTPUT": str(output_path),
        }
    )
    completed = subprocess.run(
        command,
        cwd=workspace,
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Independent QA runner failed\n"
            f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
        )
    if not output_path.is_file():
        raise RuntimeError(
            "Independent QA runner completed without writing DLP_QA_OUTPUT\n"
            f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--runner", required=True, help="Independent reviewer command")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--score-out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    case_dir = args.case_dir.resolve()
    deck = args.deck.resolve()

    if not deck.is_file():
        raise FileNotFoundError(deck)
    if not (case_dir / "expected-findings.json").is_file():
        raise FileNotFoundError(case_dir / "expected-findings.json")

    with tempfile.TemporaryDirectory(prefix="dlp-qa-blind-") as tmp:
        workspace = Path(tmp) / "workspace"
        build_blind_workspace(repo_root, case_dir, deck, workspace)
        review_output = Path(tmp) / "review-output.json"

        # The reviewer runs before the parent process opens the oracle.
        run_reviewer(args.runner, workspace, review_output, args.timeout)
        review = json.loads(review_output.read_text(encoding="utf-8"))

        oracle = json.loads((case_dir / "expected-findings.json").read_text(encoding="utf-8"))
        expected_hash = oracle["artifact"]["sha256"]
        actual_hash = sha256(deck)
        if actual_hash != expected_hash:
            raise ValueError(
                f"Fixture deck hash mismatch: expected {expected_hash}, got {actual_hash}"
            )

        score = score_review(review, oracle)
        score["case_id"] = oracle["case_id"]
        score["deck_sha256"] = actual_hash

    output = json.dumps(score, indent=2) + "\n"
    print(output, end="")
    if args.score_out:
        args.score_out.parent.mkdir(parents=True, exist_ok=True)
        args.score_out.write_text(output, encoding="utf-8")
    return 0 if score["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
