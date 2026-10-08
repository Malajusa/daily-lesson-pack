"""Clean packages must retain the visual cases referenced by their QA owners."""
import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
CASES = (
    "examples/projected-readability-regression.md",
    "examples/semantic-colour-regression.md",
    "examples/panel-containment-regression.md",
)


class VisualRegressionPackagingTests(unittest.TestCase):
    def test_complete_package_resolves_cases_and_rejects_each_missing_case(self):
        builder = importlib.import_module("build_chatgpt_package")
        audit = importlib.import_module("audit_package_dependencies")
        _, files = builder.build_file_map(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative, data in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            failures = []
            audit.validate_markdown_references(root, failures)
            self.assertEqual(failures, [])
            for owner in (root, root / "skills/dlp-pack-qa"):
                for case in CASES:
                    with self.subTest(owner=owner.relative_to(root), case=case):
                        path = owner / case
                        self.assertEqual(path.read_bytes(), (ROOT / case).read_bytes())
                        saved = path.read_bytes()
                        path.unlink()
                        failures = []
                        audit.validate_markdown_references(root, failures)
                        self.assertTrue(any(case in failure for failure in failures), failures)
                        path.write_bytes(saved)

    def test_standalone_qa_zip_preserves_cases_and_resolves_its_references(self):
        audit = importlib.import_module("audit_package_dependencies")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = subprocess.run(
                [sys.executable, str(ROOT / "scripts/package_component_skills.py"),
                 "--out", str(root / "packages")],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            with zipfile.ZipFile(root / "packages/dlp-pack-qa.zip") as archive:
                archive.extractall(root / "installed")
            skill = root / "installed/dlp-pack-qa"
            for case in CASES:
                self.assertEqual((skill / case).read_bytes(), (ROOT / case).read_bytes())
            failures = []
            audit.validate_markdown_references(skill, failures)
            self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
