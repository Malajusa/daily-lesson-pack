import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

BOUNDARY_SOURCE = "skills/dlp-numeracy-warmup/references/release-boundaries.json"
BENCHMARK_SOURCE = "examples/benchmarks/numeracy-warmup-release-boundaries-regression.md"
BOUNDARY_IDS = {
    "NW.PROMPT.THREE_TIERS_ONLY",
    "NW.PAIR.ADJACENT",
    "NW.ANSWER.MIRROR",
    "NW.REASONING.ANSWER_ONLY",
}


class NumeracyWarmupReleaseBoundaryTests(unittest.TestCase):
    def test_boundary_contract_is_fail_closed_and_complete(self):
        payload = json.loads((ROOT / BOUNDARY_SOURCE).read_text(encoding="utf-8"))
        self.assertEqual(payload["owner"], "dlp-numeracy-warmup")
        self.assertEqual(payload["release_policy"], "fail_closed")
        self.assertEqual({item["id"] for item in payload["boundaries"]}, BOUNDARY_IDS)
        self.assertIn("missing result", payload["release_rule"].lower())
        self.assertIn("blocks classroom-ready release", payload["release_rule"].lower())

    def test_complete_package_contains_numeracy_boundary_contract_and_benchmark(self):
        module = importlib.import_module("build_chatgpt_package")
        _, files = module.build_file_map(ROOT)
        component_root = "skills/dlp-numeracy-warmup"
        self.assertIn(f"{component_root}/references/release-boundaries.json", files)
        self.assertIn(f"{component_root}/{BENCHMARK_SOURCE}", files)

    def test_component_zip_contains_numeracy_boundary_contract_and_benchmark(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "package_component_skills.py"),
                    "--out",
                    tmp,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            package = Path(tmp) / "dlp-numeracy-warmup.zip"
            with zipfile.ZipFile(package) as archive:
                names = set(archive.namelist())
            prefix = "dlp-numeracy-warmup/"
            self.assertIn(prefix + "references/release-boundaries.json", names)
            self.assertIn(prefix + BENCHMARK_SOURCE, names)


if __name__ == "__main__":
    unittest.main()
