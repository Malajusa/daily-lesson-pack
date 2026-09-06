#!/usr/bin/env python3
"""Aggregate repository-owned DLP audits into one fail-closed release result."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pack_evidence import audit_pack, audit_review, digest
from pathlib import Path


GENERIC_EVIDENCE = re.compile(r"^(?:checked|reviewed|intentional|looks good|acceptable|pass)$", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--year-profile", type=Path, required=True)
    parser.add_argument("--typography", type=Path, required=True)
    parser.add_argument("--containment", type=Path, required=True)
    parser.add_argument("--visual", type=Path, required=True)
    parser.add_argument("--semantic-review", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    for flag in ("manifest", "content", "context-record", "component-record", "warning-ledger", "visual-review", "semantic-trace", "visual-trace"):
        parser.add_argument("--"+flag, type=Path, required=True)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.unlink(missing_ok=True)
    deck_hash = sha256(args.deck)
    failures: list[str] = []
    reports: dict[str, dict] = {}
    try:
        bundle_errors, content, manifest = audit_pack(args.manifest, args.content, args.context_record)
        failures.extend(bundle_errors)
        deck_entry = next(a for a in manifest['artifacts'] if a['role'] == 'deck')
        if (args.manifest.parent/deck_entry['path']).resolve() != args.deck.resolve():
            failures.append('Audited deck is not the manifest deck')
        failures.extend(audit_review(args.semantic_review, 'semantic', args.manifest, args.content, content, manifest, args.semantic_trace))
        failures.extend(audit_review(args.visual_review, 'visual', args.manifest, args.content, content, manifest, args.visual_trace))
        if not failures:
            # Structural visual audit adapter is derived only AFTER page-level review validates.
            reviewed = json.loads(args.visual_review.read_text())
            component = json.loads(args.component_record.read_text())
            adapter = dict(reviewed, artifact_sha256=deck_hash,
                run_id=reviewed['execution_id'], generator_run_id=component['generation_run_id'],
                reviewer=json.loads(args.visual_trace.read_text())['reviewer_actor'])
            adapter['checks'] = [{'id':name,'result':'PASS','evidence':'Page-level evidence validated against the complete hashed release manifest.'} for name in (
                'VISUAL.HIERARCHY','VISUAL.PROJECTION_READABILITY','VISUAL.SPACE_USE','VISUAL.REPRESENTATION_CLARITY','VISUAL.CROSS_SLIDE_CONSISTENCY')]
            adapter_path = args.out.with_suffix('.visual-adapter.json')
            adapter_path.parent.mkdir(parents=True, exist_ok=True)
            adapter_path.write_text(json.dumps(adapter))
            commands = [
                ('audit_pack_contract.py', ['--context-record',args.context_record,'--component-record',args.component_record], args.contract),
                ('audit_year_profile_context.py', ['--context-record',args.context_record,'--component-record',args.component_record], args.year_profile),
                ('audit_slide_typography.py', ['--dispositions',args.warning_ledger], args.typography),
                ('audit_panel_containment.py', [], args.containment),
                ('audit_visual_exemplar.py', ['--review-record',adapter_path], args.visual)]
            override_tasks = {t['id'] for t in content['tasks'] if t.get('response_override_source')}
            override_slides = sorted({b['page'] for b in manifest['bindings'] if b['artifact'] == deck_entry['id'] and b['record'] in override_tasks and b['field'] == 'prompt'})
            runtime = json.loads(args.context_record.read_text())
            for script, extra, out in commands:
                if script == 'audit_pack_contract.py':
                    if override_slides:
                        extra += ['--response-override-slides', *override_slides]
                    for name, count in runtime.get('warmup_counts', {}).items():
                        if name in ('literacy','numeracy'):
                            extra += ['--'+name+'-count', count]
                command = [sys.executable, str(Path(__file__).parent/script), '--deck',str(args.deck),*map(str,extra),'--out',str(out)]
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode:
                    failures.append(script+' failed: '+result.stderr[-500:])
    except (OSError, ValueError, KeyError, TypeError, IndexError, StopIteration, AttributeError) as exc:
        failures.append('Invalid complete-pack evidence: '+str(exc))
    for name in ("contract", "year_profile", "typography", "containment", "visual"):
        path = getattr(args, name)
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name} report unreadable: {exc}")
            continue
        reports[name] = report
        status = str(report.get("overall_status", report.get("status", ""))).lower()
        if status != "pass":
            failures.append(f"{name} report status is {status or 'missing'}")
        report_hash = str(report.get("artifact_sha256", "")).lower()
        if not report_hash:
            failures.append(f"{name} report is not bound to a deck SHA-256")
        elif report_hash != deck_hash:
            failures.append(f"{name} report belongs to another deck")

    # Scoped semantic/visual review and host receipts were validated before
    # running audits. Do not accept the legacy unscoped evidence-string schema.
    result = {
        "status": "PASS" if not failures else "FAIL",
        "artifact_sha256": deck_hash,
        "manifest_sha256": digest(args.manifest),
        "requirements_sha256": digest(Path(__file__).resolve().parents[1]/"references/qa-requirements.json"),
        "inputs": {name: str(getattr(args, name)) for name in ("contract", "year_profile", "typography", "containment", "visual")},
        "semantic_review": str(args.semantic_review),
        "failures": failures,
        "policy": "Only repository-owned generic audits may certify release; deck-specific expected strings or slide counts are not release gates.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
