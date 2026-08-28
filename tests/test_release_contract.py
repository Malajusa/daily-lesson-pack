from __future__ import annotations

import unittest
import json
import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def load_contract_audit():
    path = ROOT / "scripts" / "audit_pack_contract.py"
    spec = importlib.util.spec_from_file_location("audit_pack_contract", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ReleaseContractTests(unittest.TestCase):
    def test_version_is_reconciled_release(self) -> None:
        self.assertEqual(read("VERSION").strip(), "3.5.0")

    def test_release_provenance_records_both_source_lines(self) -> None:
        provenance = json.loads(read("RELEASE-PROVENANCE.json"))
        self.assertEqual(provenance["version"], "3.5.0")
        self.assertEqual(
            provenance["base_commit"],
            "3a84e4ff1665521f627b243ef4e20b4008f1cf67",
        )
        self.assertGreaterEqual(len(provenance["reconciled_sources"]), 3)

    def test_visual_exemplar_contract_is_complete(self) -> None:
        self.assertTrue(
            (ROOT / "assets/visual-exemplars/t3w6-tuesday-edited-visual-exemplar.pptx").is_file()
        )
        self.assertTrue((ROOT / "references/visual-exemplar-standard.md").is_file())
        self.assertTrue((ROOT / "scripts/audit_visual_exemplar.py").is_file())
        self.assertIn("visual-exemplar-standard.md", read("SKILL.md"))

    def test_release_is_memory_independent(self) -> None:
        orchestrator = read("SKILL.md")
        contract = read("references/shared-class-context-contract.md")
        qa = read("skills/dlp-pack-qa/SKILL.md")
        self.assertNotIn("standing teaching preferences", orchestrator)
        self.assertIn("Do not use chat memory", orchestrator)
        self.assertIn("Wednesday co-teacher mode", contract)
        self.assertIn("Context provenance gate", qa)

    def test_example_context_record_passes(self) -> None:
        audit = load_contract_audit()
        issues, summary = audit.audit_context_record(
            str(ROOT / "examples" / "context-record-wednesday.json")
        )
        self.assertEqual(issues, [])
        self.assertEqual(summary["resolved"], summary["required"])

    def test_memory_context_source_is_rejected(self) -> None:
        audit = load_contract_audit()
        data = json.loads(read("examples/context-record-wednesday.json"))
        data["mathematics_focus"]["source"] = "chat memory"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "context.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            issues, _ = audit.audit_context_record(str(path))
        self.assertIn("prohibited_memory_source", {item["code"] for item in issues})

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
            "memory-independent-wednesday-regression.md",
        ):
            self.assertIn(benchmark, qa)
            self.assertTrue((ROOT / "examples" / "benchmarks" / benchmark).is_file())


if __name__ == "__main__":
    unittest.main()
