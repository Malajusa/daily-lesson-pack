#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

from dlp_build_runtime import validate_component_record, validate_resolved_context
from pack_evidence import validate_content
from slide_render_model import RenderModelError, compile_render_model
from slide_renderer import render_presentation


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--content", type=Path, required=True)
    parser.add_argument("--component-record", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--render-manifest", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    temporary_deck: Path | None = None
    try:
        context = read_json(args.context)
        content = read_json(args.content)
        components = read_json(args.component_record)

        errors: list[str] = []
        errors.extend(validate_resolved_context(context))
        errors.extend(validate_component_record(context, components))
        errors.extend(validate_content(content))
        if content.get("instances") != context.get("timetable_instances"):
            errors.append("content instances must exactly match resolved timetable_instances")
        if errors:
            raise ValueError("\n".join(errors))

        pack = compile_render_model(context, content, components)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.render_manifest.parent.mkdir(parents=True, exist_ok=True)

        handle, temporary_name = tempfile.mkstemp(prefix=args.out.stem + "-", suffix=".pptx", dir=args.out.parent)
        os.close(handle)
        temporary_deck = Path(temporary_name)
        render_manifest = render_presentation(pack, temporary_deck)
        os.replace(temporary_deck, args.out)
        temporary_deck = None

        payload = render_manifest.to_dict()
        payload.update(
            {
                "deck_sha256": sha256(args.out),
                "context_sha256": sha256(args.context),
                "content_sha256": sha256(args.content),
                "component_record_sha256": sha256(args.component_record),
            }
        )
        temporary_manifest = args.render_manifest.with_suffix(args.render_manifest.suffix + ".tmp")
        temporary_manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary_manifest, args.render_manifest)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "deck": str(args.out),
                    "render_manifest": str(args.render_manifest),
                    "deck_sha256": payload["deck_sha256"],
                },
                indent=2,
            )
        )
        return 0
    except (OSError, ValueError, json.JSONDecodeError, RenderModelError) as exc:
        if temporary_deck is not None:
            temporary_deck.unlink(missing_ok=True)
        args.out.unlink(missing_ok=True)
        args.render_manifest.unlink(missing_ok=True)
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
