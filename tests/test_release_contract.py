from __future__ import annotations

import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class ReleaseContractTests(unittest.TestCase):
    def test_version_is_reconciled_release(self) -> None:
        self.assertEqual(read("VERSION").strip(), "3.4.0")

    def test_release_provenance_records_both_source_lines(self) -> None:
        provenance = json.loads(read("RELEASE-PROVENANCE.json"))
        self.assertEqual(provenance["version"], "3.4.0")
        self.assertEqual(
            provenance["base_commit"],
            "59a2516ec7f97d931c72c85f8825792781b6fc3c",
        )
        self.assertEqual(len(provenance["reconciled_sources"]), 2)

    def test_unsupported_visual_exemplar_contract_is_absent(self) -> None:
        checked = [ROOT / "SKILL.md", *sorted((ROOT / "skills").glob("*/SKILL.md"))]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in checked)
        self.assertNotIn("visual-exemplar", combined)
        self.assertNotIn("audit_visual_exemplar.py", combined)

    def test_literacy_contract_preserves_both_release_lines(self) -> None:
        text = read("skills/dlp-literacy-warmup/SKILL.md")
        for expected in (
            "one student action and one response",
            "Task-operation fidelity",
            "conjunction",
            "Multiple-choice quality",
            "Precision and teacher explainability",
            "inverted commas",
        ):
            self.assertIn(expected, text)

    def test_shared_reading_evidence_boundary_is_preserved(self) -> None:
        text = read("skills/dlp-shared-reading/SKILL.md")
        self.assertIn("## Evidence boundary", text)
        self.assertIn("supported by the displayed paragraph", text)

    def test_writing_precision_guard_is_preserved(self) -> None:
        text = read("skills/dlp-writing-lesson/SKILL.md")
        self.assertIn("preserve the sentence's core proposition", text)
        self.assertIn("label and teach it as elaboration", text)

    def test_universal_mathematics_canon_is_preserved(self) -> None:
        maths = read("skills/dlp-maths-lesson/SKILL.md")
        qa = read("skills/dlp-pack-qa/SKILL.md")
        self.assertIn("universal-maths-instruction-canon.md", maths)
        self.assertIn("Meaning before procedure", maths)
        self.assertIn("Apply `references/universal-maths-instruction-canon.md` in full", qa)

    def test_all_regression_records_are_release_inputs(self) -> None:
        qa = read("skills/dlp-pack-qa/SKILL.md")
        for benchmark in (
            "t3w6-monday-modular-regression.md",
            "t3w6-tuesday-release-regression.md",
            "t3w6-thursday-literacy-regression.md",
            "universal-maths-canon-regression.md",
        ):
            self.assertIn(benchmark, qa)
            self.assertTrue((ROOT / "examples" / "benchmarks" / benchmark).is_file())


if __name__ == "__main__":
    unittest.main()
