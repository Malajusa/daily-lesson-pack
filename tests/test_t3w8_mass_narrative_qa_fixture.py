from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "examples/benchmarks/t3w8-tuesday-mass-narrative-known-failure"
ASSET = ROOT / "assets/qa-regressions/t3w8-tuesday-mass-narrative-known-failure.pptx"
ORACLE = CASE_DIR / "expected-findings.json"
REVIEW = CASE_DIR / "review.md"
CONTRACT = CASE_DIR / "README.md"
HARNESS = ROOT / "scripts/run_blind_qa_regression.py"
EXPECTED_DECK_SHA256 = "f9321b698a7b6c497ea4908e24aa7a90abe57cf83a8171f844395aefecc30ccd"
EXPECTED_REVIEW_SHA256 = "0b82054ac8572b83e204ccb8882025679a53b79a0f364488cee264b06f9a0965"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_harness_module():
    spec = importlib.util.spec_from_file_location("run_blind_qa_regression", HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {HARNESS}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MassNarrativeKnownFailureFixtureTests(unittest.TestCase):
    def test_fixture_preserves_exact_deck_and_full_review(self) -> None:
        self.assertTrue(ASSET.is_file(), ASSET)
        self.assertTrue(REVIEW.is_file(), REVIEW)
        self.assertEqual(sha256(ASSET), EXPECTED_DECK_SHA256)
        self.assertEqual(sha256(REVIEW), EXPECTED_REVIEW_SHA256)

    def test_oracle_names_required_findings_and_false_positive_guards(self) -> None:
        data = json.loads(ORACLE.read_text(encoding="utf-8"))
        self.assertEqual(data["expected_release"], "FAIL")
        self.assertEqual(data["artifact"]["sha256"], EXPECTED_DECK_SHA256)

        finding_ids = {item["id"] for item in data["required_findings"]}
        self.assertTrue(
            {
                "RUNTIME-WRONG-DAY",
                "RUNTIME-UNRESOLVED-TIMETABLE",
                "MATH-INDEPENDENT-REPEATS-MODEL",
                "MATH-INDEPENDENT-PRACTICE-THIN",
                "VISUAL-INSTRUCTION-HIERARCHY",
                "WRITING-COMPLICATION-NOT-OBSTACLE",
                "WRITING-JOINT-SCENARIO-PLAUSIBILITY",
                "WRITING-EXIT-MISALIGNED",
                "DELIVERY-OVERSTATED-COMPLETION",
            }.issubset(finding_ids)
        )

        guard_ids = {item["id"] for item in data["must_not_flag"]}
        self.assertTrue(
            {
                "NUMERACY-FIVE-PAIRS-IS-CORRECT",
                "NO-WIDESPREAD-CLIPPING-CLAIM",
                "LITERACY-WARMUP-GENERALLY-SUCCESSFUL",
                "SHARED-READING-GENERALLY-SUCCESSFUL",
            }.issubset(guard_ids)
        )

    def test_contract_labels_fixture_as_known_failure_not_exemplar(self) -> None:
        text = CONTRACT.read_text(encoding="utf-8").lower()
        for phrase in (
            "known-failure",
            "expected release decision: fail",
            "do not use as a content exemplar",
            "do not use as a visual exemplar",
            "blind",
            "false positive",
        ):
            self.assertIn(phrase, text)

    def test_blind_workspace_excludes_answer_material(self) -> None:
        module = load_harness_module()
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            module.build_blind_workspace(ROOT, CASE_DIR, ASSET, workspace)

            self.assertTrue((workspace / "input/deck.pptx").is_file())
            self.assertEqual(sha256(workspace / "input/deck.pptx"), EXPECTED_DECK_SHA256)
            self.assertTrue((workspace / "skills/dlp-pack-qa/SKILL.md").is_file())

            forbidden_names = {"review.md", "expected-findings.json"}
            visible_forbidden = [
                path
                for path in workspace.rglob("*")
                if path.is_file() and path.name in forbidden_names
            ]
            self.assertEqual(visible_forbidden, [])
            self.assertFalse(
                (workspace / "examples/benchmarks/t3w8-tuesday-mass-narrative-known-failure").exists()
            )
            self.assertFalse(
                (workspace / "assets/qa-regressions/t3w8-tuesday-mass-narrative-known-failure.pptx").exists()
            )

    @unittest.skipUnless(
        os.environ.get("DLP_PACK_QA_RUNNER"),
        "Set DLP_PACK_QA_RUNNER to execute the live blind dlp-pack-qa regression.",
    )
    def test_live_dlp_pack_qa_finds_known_failures_blind(self) -> None:
        command = [
            sys.executable,
            str(HARNESS),
            "--repo-root",
            str(ROOT),
            "--case-dir",
            str(CASE_DIR),
            "--deck",
            str(ASSET),
            "--runner",
            os.environ["DLP_PACK_QA_RUNNER"],
        ]
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        if completed.returncode != 0:
            self.fail(
                "Blind dlp-pack-qa regression failed.\n"
                f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
            )


if __name__ == "__main__":
    unittest.main()
