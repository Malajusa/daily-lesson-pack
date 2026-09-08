from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from pack_evidence import validate_content  # noqa: E402


class SemanticRelationshipTests(unittest.TestCase):
    def content(self, owner: str = "dlp-numeracy-warmup") -> dict:
        return {
            "schema_version": 3,
            "instances": [
                {
                    "id": "instance-1",
                    "owner": owner,
                    "start": "08:40",
                    "duration_minutes": 10,
                    "purpose": "retrieval",
                }
            ],
            "tasks": [
                {
                    "id": "task-1",
                    "instance_id": "instance-1",
                    "operation": "calculate",
                    "fields": {"prompt": "Calculate 7 + 5.", "answer": "12"},
                    "demands": [
                        {"id": "answer", "action": "calculate", "answer_quote": "12"}
                    ],
                }
            ],
            "documents": {},
        }

    def test_why_fields_require_a_relationship_and_concept(self) -> None:
        content = self.content()
        task = content["tasks"][0]
        task["fields"].update(
            {
                "why_prompt": "How can a known fact help?",
                "why_answer": "Use 7 + 3 = 10, then add 2.",
            }
        )
        errors = validate_content(content)
        self.assertTrue(any("why relationship" in error.lower() for error in errors), errors)

    def test_complete_why_relationship_passes(self) -> None:
        content = self.content()
        task = content["tasks"][0]
        task["fields"].update(
            {
                "why_prompt": "How can a known fact help?",
                "why_answer": "Use 7 + 3 = 10, then add 2.",
            }
        )
        task["relationships"] = {
            "why": {
                "prompt_field": "why_prompt",
                "answer_field": "why_answer",
                "concept": "addition_strategy",
            }
        }
        self.assertEqual(validate_content(content), [])

    def test_shared_reading_requires_paragraph_question_answer_relationship(self) -> None:
        content = self.content("dlp-shared-reading")
        task = content["tasks"][0]
        task["operation"] = "infer"
        task["fields"].update(
            {
                "paragraph": "Ava froze when a whisper came from the dark tunnel.",
            }
        )
        errors = validate_content(content)
        self.assertTrue(any("reading relationship" in error.lower() for error in errors), errors)

    def test_shared_reading_relationship_passes_when_fields_exist(self) -> None:
        content = self.content("dlp-shared-reading")
        task = content["tasks"][0]
        task["operation"] = "infer"
        task["fields"].update(
            {"paragraph": "Ava froze when a whisper came from the dark tunnel."}
        )
        task["relationships"] = {
            "reading": {
                "paragraph_field": "paragraph",
                "question_field": "prompt",
                "answer_field": "answer",
            }
        }
        self.assertEqual(validate_content(content), [])

    def test_relationship_cannot_reference_missing_field(self) -> None:
        content = self.content()
        task = content["tasks"][0]
        task["fields"].update(
            {
                "why_prompt": "How can a known fact help?",
                "why_answer": "Use 7 + 3 = 10, then add 2.",
            }
        )
        task["relationships"] = {
            "why": {
                "prompt_field": "missing_prompt",
                "answer_field": "why_answer",
                "concept": "addition_strategy",
            }
        }
        errors = validate_content(content)
        self.assertTrue(any("missing field" in error.lower() for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
