"""Regression tests for the A -> B -> C planning hierarchy."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

TERM_ROOT = ROOT / "planning" / "2026" / "term-4"
CONTRACT = ROOT / "references" / "term-week-day-planning-contract.md"

WEEK_HEADINGS = (
    "## Weekly purpose",
    "## English — Writing",
    "## English — Reading",
    "## Mathematics",
    "## HASS",
    "## Health",
    "## Digital Technologies",
    "## Assessment and evidence",
    "## Preparation and resources",
    "## End-of-week checkpoint",
)


class PlanningHierarchyTests(unittest.TestCase):
    def test_level_a_and_all_ten_level_b_files_exist(self):
        self.assertTrue((TERM_ROOT / "term-overview.md").is_file())
        for week in range(1, 11):
            with self.subTest(week=week):
                self.assertTrue(
                    (TERM_ROOT / "weeks" / f"week-{week:02d}.md").is_file()
                )

    def test_week_files_keep_b_level_structure_and_are_timetable_agnostic(self):
        for week in range(1, 11):
            path = TERM_ROOT / "weeks" / f"week-{week:02d}.md"
            text = path.read_text(encoding="utf-8")
            with self.subTest(week=week):
                for heading in WEEK_HEADINGS:
                    self.assertIn(heading, text)
                self.assertNotIn("## Monday", text)
                self.assertNotIn("## Tuesday", text)
                self.assertNotIn("## Wednesday", text)
                self.assertNotIn("## Thursday", text)
                self.assertNotIn("## Friday", text)

    def test_contract_defines_source_precedence_and_exception_only_status(self):
        text = CONTRACT.read_text(encoding="utf-8").lower()
        for phrase in (
            "level a",
            "level b",
            "level c",
            "lesson-status exception",
            "weekly teaching overview",
            "term overview",
            "actual timetable",
            "missing status is not evidence",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertLess(
            text.index("lesson-status exception"),
            text.index("weekly teaching overview"),
        )
        self.assertLess(
            text.index("weekly teaching overview"),
            text.index("term overview"),
        )

    def test_status_ledger_is_exception_only_and_contains_no_student_records(self):
        payload = json.loads(
            (TERM_ROOT / "status" / "lesson-status.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["policy"], "exception-only")
        self.assertEqual(payload["plan_id"], "2026-t4-year-4-5-room-11")
        self.assertEqual(payload["exceptions"], [])
        serialised = json.dumps(payload).lower()
        for prohibited in ("student", "diagnosis", "assessment_record"):
            self.assertNotIn(prohibited, serialised)

    def test_complete_package_contains_planning_contract_and_selected_plan(self):
        module = importlib.import_module("build_chatgpt_package")
        _, files = module.build_file_map(ROOT)
        required = {
            "references/term-week-day-planning-contract.md",
            "planning/2026/term-4/term-overview.md",
            "planning/2026/term-4/status/lesson-status.json",
            *{
                f"planning/2026/term-4/weeks/week-{week:02d}.md"
                for week in range(1, 11)
            },
        }
        self.assertTrue(required.issubset(files), sorted(required - set(files)))


if __name__ == "__main__":
    unittest.main()
