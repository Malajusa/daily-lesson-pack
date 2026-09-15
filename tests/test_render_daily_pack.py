import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "render_daily_pack.py"


class RenderDailyPackCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = Path(self.tmp.name)
        instance = {"id": "i1", "owner": "dlp-morning-work", "duration_minutes": 10, "purpose": "retrieval"}
        def field(value):
            return {"resolved": True, "value": value, "source": "fixture"}
        self.context = {
            "schema_version": 2, "generation_run_id": "run-1",
            "active_year_profile": field("year-4-5"),
            "pack_profile": field("default-daily-pack-architecture"),
            "date": field("2026-09-15"), "term_week": field("T3W9"), "day": field("Tuesday"),
            "timetable": field("08:30 Morning Work"), "mathematics_focus": field("volume and capacity"),
            "english_focus": field("narrative"), "lesson_status": field("previous scheduled lesson covered"),
            "timetable_instances": [instance],
        }
        self.content = {
            "schema_version": 3, "instances": [instance],
            "tasks": [
                {"id": "m", "instance_id": "i1", "operation": "calculate", "fields": {"prompt": "345 + 278", "answer": "623"}, "demands": [{"id": "d1", "action": "calculate", "answer_quote": "623"}], "render_group": "maths"},
                {"id": "l", "instance_id": "i1", "operation": "edit", "fields": {"prompt": "Correct: we was late", "answer": "We were late."}, "demands": [{"id": "d2", "action": "edit", "answer_quote": "We were late."}], "render_group": "literacy"},
            ],
            "documents": {},
        }
        self.components = {
            "schema_version": 2, "generation_run_id": "run-1", "active_year_profile": "year-4-5",
            "instances": [{"instance_id": "i1", "owner": "dlp-morning-work", "status": "PASS", "active_year_profile": "year-4-5", "estimated_minutes": 9, "checks": [{"id": "COMPONENT.CONTENT", "result": "PASS", "evidence": "fixture"}]}],
        }
        for name, payload in (("context", self.context), ("content", self.content), ("components", self.components)):
            (self.p / f"{name}.json").write_text(json.dumps(payload), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def invoke_cli(self):
        return subprocess.run([
            sys.executable, str(CLI),
            "--context", str(self.p / "context.json"),
            "--content", str(self.p / "content.json"),
            "--component-record", str(self.p / "components.json"),
            "--out", str(self.p / "pack.pptx"),
            "--render-manifest", str(self.p / "render.json"),
        ], cwd=ROOT, text=True, capture_output=True)

    def test_cli_binds_deck_and_source_hashes(self):
        result = self.invoke_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        import hashlib
        digest = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
        manifest = json.loads((self.p / "render.json").read_text())
        self.assertEqual(manifest["deck_sha256"], digest(self.p / "pack.pptx"))
        self.assertEqual(manifest["content_sha256"], digest(self.p / "content.json"))
        self.assertEqual(manifest["renderer"], "daily-lesson-pack")

    def test_cli_fails_closed_on_unknown_render_field(self):
        self.content["tasks"][0]["fields"]["mystery"] = "???"
        (self.p / "content.json").write_text(json.dumps(self.content))
        result = self.invoke_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mystery", result.stdout + result.stderr)
        self.assertFalse((self.p / "pack.pptx").exists())


if __name__ == "__main__":
    unittest.main()
