import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class RenderProvenanceTests(unittest.TestCase):
    def test_accepts_only_closed_renderer_structural_labels(self):
        from render_provenance import validate_structural_text
        valid = [
            {"shape_id": 2, "shape_name": "DLP:meta:eyebrow:s1", "text": "MATHEMATICS", "kind": "eyebrow"},
            {"shape_id": 3, "shape_name": "DLP:meta:title:s1", "text": "Your turn", "kind": "title"},
            {"shape_id": 4, "shape_name": "DLP:group-label:maths:s1", "text": "MATHS", "kind": "group_label"},
        ]
        self.assertEqual(validate_structural_text(valid), [])
        bad = valid + [{"shape_id": 5, "shape_name": "DLP:meta:title:s1", "text": "Also write an explanation", "kind": "title"}]
        self.assertTrue(any("not an approved structural label" in error for error in validate_structural_text(bad)))

    def test_builds_exact_page_shape_allowlist(self):
        from render_provenance import structural_text_allowlist
        manifest = {
            "schema_version": 1, "renderer": "daily-lesson-pack",
            "slides": [
                {"slide_number": 1, "structural_text": [{"shape_id": 2, "shape_name": "DLP:meta:eyebrow:s1", "text": "MATHEMATICS", "kind": "eyebrow"}]},
                {"slide_number": 2, "structural_text": [{"shape_id": 7, "shape_name": "DLP:meta:title:s2", "text": "Answer", "kind": "title"}]},
            ],
        }
        allow = structural_text_allowlist(manifest)
        self.assertEqual(allow[(1, 2)], "MATHEMATICS")
        self.assertEqual(allow[(2, 7)], "Answer")


if __name__ == "__main__":
    unittest.main()
