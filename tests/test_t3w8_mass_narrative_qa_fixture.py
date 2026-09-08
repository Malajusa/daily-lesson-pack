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
CASE_REL = "examples/benchmarks/t3w8-tuesday-mass-narrative-known-failure"
CASE_DIR = ROOT / CASE_REL
ASSET_REL = "assets/qa-regressions/t3w8-tuesday-mass-narrative-known-failure.pptx"
ASSET = ROOT / ASSET_REL
ORACLE = CASE_DIR / "expected-findings.json"
REVIEW = CASE_DIR / "review.md"
CONTRACT = CASE_DIR / "README.md"
REQUEST_CONTEXT = CASE_DIR / "blind-request-context.md"
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


def synthetic_review(oracle: dict) -> dict:
    findings = []
    for expected in oracle["required_findings"]:
        match = expected["match"]
        findings.append(
            {
                "component": expected["component"],
                "severity": expected["severity"],
                "slides": match.get("slides_any", [])[:1],
                "summary": match["text_any"][0],
                "details": expected["expectation"],
            }
        )
    return {"verdict": "FAIL", "findings": findings, "strengths": []}


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
        self.assertEqual(data["review"]["sha256"], EXPECTED_REVIEW_SHA256)

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

    def test_case_is_routed_to_orchestrator_qa_and_qa_packages(self) -> None:
        contract_relative = f"{CASE_REL}/README.md"
        for relative in ("SKILL.md", "skills/dlp-pack-qa/SKILL.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(contract_relative, text, relative)
        for relative in ("scripts/build_chatgpt_package.py", "scripts/package_component_skills.py"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(contract_relative, text, relative)

    def test_blind_workspace_excludes_answer_material(self) -> None:
        module = load_harness_module()
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            module.build_blind_workspace(ROOT, CASE_DIR, ASSET, workspace)

            self.assertTrue((workspace / "input/deck.pptx").is_file())
            self.assertEqual(sha256(workspace / "input/deck.pptx"), EXPECTED_DECK_SHA256)
            self.assertTrue((workspace / "input/request-context.md").is_file())
            self.assertTrue((workspace / "input/review-instructions.md").is_file())
            self.assertTrue((workspace / "skills/dlp-pack-qa/SKILL.md").is_file())

            forbidden_names = {"review.md", "expected-findings.json"}
            visible_forbidden = [
                path
                for path in workspace.rglob("*")
                if path.is_file() and path.name in forbidden_names
            ]
            self.assertEqual(visible_forbidden, [])
            self.assertFalse((workspace / CASE_REL).exists())
            self.assertFalse((workspace / ASSET_REL).exists())

    def test_oracle_scorer_accepts_complete_blind_findings(self) -> None:
        module = load_harness_module()
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        score = module.score_review(synthetic_review(oracle), oracle)
        self.assertTrue(score["passed"], score)
        self.assertEqual(score["missing_required"], [])
        self.assertEqual(score["false_positive_guards_triggered"], [])

    def test_oracle_scorer_rejects_missing_required_finding(self) -> None:
        module = load_harness_module()
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        review = synthetic_review(oracle)
        review["findings"].pop()
        score = module.score_review(review, oracle)
        self.assertFalse(score["passed"])
        self.assertEqual(len(score["missing_required"]), 1)

    def test_oracle_scorer_rejects_known_false_positive(self) -> None:
        module = load_harness_module()
        oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        review = synthetic_review(oracle)
        guard = oracle["must_not_flag"][0]
        review["findings"].append(
            {
                "component": "dlp-numeracy-warmup",
                "severity": "major",
                "slides": [],
                "summary": guard["match"]["text_any"][0],
                "details": "Synthetic false positive for scorer verification.",
            }
        )
        score = module.score_review(review, oracle)
        self.assertFalse(score["passed"])
        self.assertEqual(score["false_positive_guards_triggered"], [guard["id"]])

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
