from __future__ import annotations

from typing import Iterable

APPROVED_STRUCTURAL_TEXT = {
    "eyebrow": {
        "MORNING WORK", "LITERACY WARM-UP", "SHARED READING", "GUIDED READING",
        "WRITING", "MATHEMATICS WARM-UP", "MATHEMATICS",
    },
    "title": {
        "Remember", "Your turn", "Answer", "Model", "Read and think",
        "Worked example", "Success criteria", "Next", "Morning Work",
    },
    "group_label": {"MATHS", "LITERACY", "EXTENSION"},
}


def validate_structural_text(entries: Iterable[dict]) -> list[str]:
    errors: list[str] = []
    seen: set[int] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"structural text entry {index} must be an object")
            continue
        shape_id = entry.get("shape_id")
        kind = entry.get("kind")
        text = entry.get("text")
        name = entry.get("shape_name")
        if not isinstance(shape_id, int) or isinstance(shape_id, bool) or shape_id < 1:
            errors.append(f"structural text entry {index} has invalid shape_id")
            continue
        if shape_id in seen:
            errors.append(f"structural text shape_id {shape_id} is duplicated")
        seen.add(shape_id)
        if kind not in APPROVED_STRUCTURAL_TEXT or text not in APPROVED_STRUCTURAL_TEXT.get(kind, set()):
            errors.append(f"structural text {text!r} is not an approved structural label for {kind!r}")
        if not isinstance(name, str) or not name.startswith(("DLP:meta:", "DLP:group-label:")):
            errors.append(f"structural text entry {shape_id} has invalid renderer shape name")
    return errors


def structural_text_allowlist(render_manifest: dict) -> dict[tuple[int, int], str]:
    if render_manifest.get("schema_version") != 1 or render_manifest.get("renderer") != "daily-lesson-pack":
        raise ValueError("Unsupported render manifest")
    allow: dict[tuple[int, int], str] = {}
    slides = render_manifest.get("slides")
    if not isinstance(slides, list):
        raise ValueError("Render manifest slides must be a list")
    for index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            raise ValueError(f"Render manifest slide {index} must be an object")
        page = slide.get("slide_number")
        if not isinstance(page, int) or isinstance(page, bool) or page < 1:
            raise ValueError(f"Render manifest slide {index} has invalid slide_number")
        entries = slide.get("structural_text", [])
        errors = validate_structural_text(entries)
        if errors:
            raise ValueError("; ".join(errors))
        for entry in entries:
            key = (page, entry["shape_id"])
            if key in allow:
                raise ValueError(f"Duplicate structural text binding {key}")
            allow[key] = entry["text"]
    return allow
