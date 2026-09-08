from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = "examples/benchmarks/t3w8-tuesday-bypass-known-failure.md"


class BypassRegressionContractTests(unittest.TestCase):
    def test_t3w8_bypass_benchmark_exists_and_covers_failure_classes(self) -> None:
        path = ROOT / BENCHMARK
        self.assertTrue(path.is_file(), BENCHMARK)
        text = path.read_text(encoding="utf-8").lower()
        for phrase in (
            "morning work",
            "cumulative arithmetic retrieval",
            "36 pt",
            "why",
            "distractor",
            "pronoun",
            "shared reading",
            "runtime",
            "timetable",
            "release evidence",
        ):
            self.assertIn(phrase, text)

    def test_benchmark_is_routed_to_orchestrator_and_qa(self) -> None:
        for relative in ("SKILL.md", "skills/dlp-pack-qa/SKILL.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("t3w8-tuesday-bypass-known-failure.md", text, relative)

    def test_benchmark_is_packaged_for_complete_and_qa_packages(self) -> None:
        for relative in ("scripts/build_chatgpt_package.py", "scripts/package_component_skills.py"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("t3w8-tuesday-bypass-known-failure.md", text, relative)

    def test_routing_regression_preserves_runtime_for_python_script_request(self) -> None:
        text = (ROOT / "tests/modular-routing-regressions.md").read_text(encoding="utf-8").lower()
        self.assertIn("python script", text)
        self.assertIn("repository runtime", text)
        self.assertIn("candidate", text)


if __name__ == "__main__":
    unittest.main()
