"""Regressions captured from the Daily Lesson Pack 3.10.0-rc.4 baseline.

These behaviours were verified RED against the pinned baseline before the
minimal implementation was added. Keep them as permanent regression guards.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from agent_fixtures import context_fixture  # noqa: E402
from agent_protocol import ProtocolError, validate_json  # noqa: E402
from dlp_build_runtime import validate_resolved_context  # noqa: E402


class BaselineRegressionGapTests(unittest.TestCase):
    def test_request_routing_has_first_class_component_only_path(self) -> None:
        """A one-component request must not be specified as a full-pack request."""
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        routing = text.split("## Request routing", 1)[1].split("## Context architecture", 1)[0]
        lower = routing.lower()

        self.assertIn("component-only", lower)
        self.assertIn("request_scope", lower)
        self.assertIn("required_artifacts", lower)
        self.assertIn("stop-after components", lower)

    def test_component_only_context_can_request_deck_without_briefing(self) -> None:
        """A standalone projected component must not require a full-pack briefing."""
        with tempfile.TemporaryDirectory() as directory:
            _, context = context_fixture(
                directory,
                owners=("dlp-morning-work",),
            )
            context["request_scope"] = "component-only"
            context["required_artifacts"] = ["deck"]

            # Required behaviour: this is a valid frozen component-only context.
            try:
                validate_json(context, ROOT / "schemas" / "run-context.schema.json")
            except ProtocolError as exc:
                self.fail(f"component-only deck context should be valid: {exc}")

    def test_daily_pack_context_still_requires_briefing(self) -> None:
        """Relaxing component-only output must not weaken the full-pack contract."""
        with tempfile.TemporaryDirectory() as directory:
            _, context = context_fixture(
                directory,
                owners=("dlp-morning-work",),
            )
            context["request_scope"] = "daily-pack"
            context["required_artifacts"] = ["deck"]

            with self.assertRaises(ProtocolError):
                validate_json(context, ROOT / "schemas" / "run-context.schema.json")

    def test_direct_runtime_requires_hashed_source_provenance(self) -> None:
        """Direct finalisation must require explicit hashed provenance records."""
        with tempfile.TemporaryDirectory() as directory:
            _, context = context_fixture(
                directory,
                owners=("dlp-morning-work",),
            )
            context.pop("source_provenance")

            errors = validate_resolved_context(context)

        self.assertTrue(
            any("source_provenance" in error or "hashed source" in error for error in errors),
            errors,
        )

    def test_direct_runtime_rejects_unbound_field_source(self) -> None:
        """A non-empty source label is insufficient unless it binds to provenance."""
        with tempfile.TemporaryDirectory() as directory:
            _, context = context_fixture(
                directory,
                owners=("dlp-morning-work",),
            )
            context["mathematics_focus"]["source"] = "unbound-current-focus"

            errors = validate_resolved_context(context)

        self.assertTrue(
            any(
                "mathematics_focus" in error
                and ("source_provenance" in error or "hashed source" in error)
                for error in errors
            ),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
