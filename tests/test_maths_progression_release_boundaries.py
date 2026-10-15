"""Main-lesson boundaries must reach every scheduled instance."""
import sys
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pack_evidence import expected_checks
from build_chatgpt_package import build_file_map

MATHS_BOUNDARIES = {
    "MATHS.OPENING.DIAGNOSTIC",
    "MATHS.TASK.PROGRESSION",
    "MATHS.ADVANCE.ROUTE",
    "MATHS.TASK.SUFFICIENCY",
}


class MathsProgressionBoundaryTests(unittest.TestCase):
    def test_both_maths_blocks_require_every_progression_check(self):
        content = {
            "instances": [
                {"id": "maths-1", "owner": "dlp-maths-lesson"},
                {"id": "maths-2", "owner": "dlp-maths-lesson"},
                {"id": "reading", "owner": "dlp-shared-reading"}],
            "tasks": []}
        checks = expected_checks(content, {"artifacts": []}, "semantic")
        for boundary in MATHS_BOUNDARIES:
            with self.subTest(boundary=boundary):
                self.assertIn((boundary, "maths-1"), checks)
                self.assertIn((boundary, "maths-2"), checks)
                self.assertNotIn((boundary, "reading"), checks)

    def test_unscheduled_maths_has_no_progression_requirements(self):
        content = {"instances": [{"id": "reading", "owner": "dlp-shared-reading"}],
                   "tasks": []}
        checks = expected_checks(content, {"artifacts": []}, "semantic")
        self.assertFalse({key for key, subject in checks} & MATHS_BOUNDARIES)

    def test_complete_package_keeps_owner_and_reviewer_dependencies(self):
        _, files = build_file_map(ROOT)
        benchmark = "examples/benchmarks/maths-demand-progression-regression.md"
        for owner in ("dlp-maths-lesson", "dlp-numeracy-warmup", "dlp-pack-qa"):
            self.assertIn("skills/" + owner + "/" + benchmark, files)
        self.assertIn("skills/dlp-maths-lesson/references/release-boundaries.json", files)
        for owner in ("dlp-maths-lesson", "dlp-numeracy-warmup"):
            self.assertIn("skills/dlp-pack-qa/skills/" + owner +
                          "/references/release-boundaries.json", files)

    def test_standalone_qa_enforces_maths_and_numeracy_without_siblings(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = subprocess.run(
                [sys.executable, str(ROOT / "scripts/package_component_skills.py"),
                 "--out", tmp], capture_output=True, text=True, timeout=30)
            self.assertEqual(run.returncode, 0, run.stderr)
            benchmark = "examples/benchmarks/maths-demand-progression-regression.md"
            for owner in ("dlp-maths-lesson", "dlp-numeracy-warmup", "dlp-pack-qa"):
                with zipfile.ZipFile(Path(tmp) / (owner + ".zip")) as archive:
                    self.assertIn(owner + "/" + benchmark, archive.namelist())
                    if owner == "dlp-pack-qa":
                        archive.extractall(Path(tmp) / "isolated")
            isolated = Path(tmp) / "isolated/dlp-pack-qa"
            for owner in ("dlp-maths-lesson", "dlp-numeracy-warmup"):
                self.assertTrue((isolated / "skills" / owner /
                                 "references/release-boundaries.json").is_file())
            script = (
                "import sys,json;sys.path.insert(0,sys.argv[1]);"
                "from pack_evidence import expected_checks;"
                "content={'instances':[{'id':'maths','owner':'dlp-maths-lesson'},"
                "{'id':'warmup','owner':'dlp-numeracy-warmup'}],'tasks':[]};"
                "print(json.dumps(sorted(expected_checks(content,{'artifacts':[]},'semantic'))))"
            )
            result = subprocess.run(
                [sys.executable, "-I", "-B", "-c", script, str(isolated / "scripts")],
                cwd=tmp, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            checks = {tuple(item) for item in json.loads(result.stdout)}
            for boundary in MATHS_BOUNDARIES:
                self.assertIn((boundary, "maths"), checks)
            for boundary in ("NW.CALIBRATION", "NW.DEMAND.PROGRESSION",
                             "NW.TIER.INDEPENDENCE"):
                self.assertIn((boundary, "warmup"), checks)


if __name__ == "__main__":
    unittest.main()
