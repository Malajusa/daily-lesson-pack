import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from slide_render_model import RenderModelError, SlideRole, Visibility, compile_render_model


def fixture(owner="dlp-shared-reading", fields=None, operation="respond"):
    fields = fields or {
        "paragraph": "The storm rolled across the harbour.",
        "prompt": "What changed in the setting?",
        "answer": "The storm changed the harbour conditions.",
        "teacher_note": "Ask two students to justify before revealing.",
    }
    context = {
        "schema_version": 2,
        "generation_run_id": "run-1",
        "date": {"resolved": True, "value": "2026-09-15", "source": "request"},
        "timetable_instances": [{"id": "instance-1", "owner": owner, "duration_minutes": 30, "purpose": "fixture"}],
    }
    content = {
        "schema_version": 3,
        "instances": context["timetable_instances"],
        "tasks": [{
            "id": "task-1", "instance_id": "instance-1", "operation": operation, "fields": fields,
            "demands": [{"id": "d1", "action": "respond", "answer_quote": fields.get("answer", "x")}],
        }],
    }
    components = {
        "schema_version": 2,
        "generation_run_id": "run-1",
        "components": [{
            "instance_id": "instance-1", "owner": owner, "active_year_profile": "year-4-5",
            "status": "PASS", "estimated_minutes": 20,
        }],
    }
    return context, content, components


class SlideRenderModelTests(unittest.TestCase):
    def test_shared_reading_excludes_teacher_note(self):
        pack = compile_render_model(*fixture())
        self.assertEqual([slide.role for slide in pack.slides], [SlideRole.READING, SlideRole.ANSWER])
        self.assertTrue(all(block.visibility is Visibility.STUDENT for slide in pack.slides for block in slide.blocks))
        self.assertNotIn("Ask two students", " ".join(block.text for slide in pack.slides for block in slide.blocks))

    def test_unknown_field_fails_closed(self):
        args = fixture(owner="dlp-maths-lesson", fields={"prompt": "Do it.", "answer": "Done.", "mystery": "???"})
        with self.assertRaisesRegex(RenderModelError, "mystery"):
            compile_render_model(*args)

    def test_success_criteria_split_to_rows(self):
        args = fixture(owner="dlp-writing-lesson", fields={
            "prompt": "Check your work.", "answer": "Complete.",
            "success_criteria": "Clear opening\nPrecise verbs\nVaried sentences\nCorrect punctuation\nParagraphs\nStrong ending",
        })
        pack = compile_render_model(*args)
        criteria = [slide for slide in pack.slides if slide.role is SlideRole.SUCCESS_CRITERIA]
        self.assertEqual(len(criteria), 1)
        self.assertEqual(len(criteria[0].blocks), 6)

    def test_morning_work_groups_maths_and_literacy(self):
        context = {
            "schema_version": 2, "generation_run_id": "run-1",
            "date": {"resolved": True, "value": "2026-09-15", "source": "request"},
            "timetable_instances": [{"id": "instance-1", "owner": "dlp-morning-work", "duration_minutes": 15, "purpose": "morning"}],
        }
        content = {
            "schema_version": 3, "instances": context["timetable_instances"],
            "tasks": [
                {"id": "m", "instance_id": "instance-1", "operation": "calculate", "fields": {"prompt": "345 + 278", "answer": "623"}, "demands": [{"id": "d1", "action": "calculate", "answer_quote": "623"}], "render_group": "maths"},
                {"id": "l", "instance_id": "instance-1", "operation": "edit", "fields": {"prompt": "Correct: we was late", "answer": "We were late."}, "demands": [{"id": "d2", "action": "edit", "answer_quote": "We were late."}], "render_group": "literacy"},
            ],
        }
        components = {"schema_version": 2, "generation_run_id": "run-1", "components": [{"instance_id": "instance-1", "owner": "dlp-morning-work", "active_year_profile": "year-4-5", "status": "PASS", "estimated_minutes": 10}]}
        pack = compile_render_model(context, content, components)
        self.assertEqual(pack.slides[0].role, SlideRole.MORNING_WORK)
        self.assertEqual({block.group for block in pack.slides[0].blocks}, {"maths", "literacy"})

    def test_explicit_render_fields_classify_nonstandard_content(self):
        context, content, components = fixture(
            owner="dlp-maths-lesson",
            fields={"prompt": "Follow the worked steps.", "answer": "24 cm³", "worked_steps": "3 × 4 × 2 = 24 cm³"},
            operation="model",
        )
        content["tasks"][0]["render_fields"] = {"worked_steps": {"visibility": "student", "kind": "worked_step", "role": "worked_example"}}
        self.assertTrue(any(slide.role is SlideRole.WORKED_EXAMPLE for slide in compile_render_model(context, content, components).slides))


if __name__ == "__main__":
    unittest.main()
