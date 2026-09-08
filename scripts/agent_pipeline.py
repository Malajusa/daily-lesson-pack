"""Bridge orchestration to existing canonical staging, evidence and release audits.

The trusted host supplies a ContentSource-based assembler; this module does not
invent a new pedagogical renderer or accept model-authored release decisions.
"""
from __future__ import annotations

import asyncio
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from agent_adapter import run_json_command
from agent_protocol import (ProtocolError, read_json, reference_record, safe_path,
                            sha256_file, write_json_atomic)
from dlp_build_runtime import REQUIRED_RELEASE_EVIDENCE, promote_release, stage_candidate, validate_component_record
from pack_evidence import audit_pack, expected_checks
from validate_agent_artifacts import export_release_review

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Candidate:
    root: Path
    revision: int

    def hashes(self) -> dict:
        return {'artifact_sha256': sha256_file(self.root/'pack.pptx'),
                'manifest_sha256': sha256_file(self.root/'manifest.json'),
                'content_sha256': sha256_file(self.root/'content.json'),
                'requirements_sha256': sha256_file(ROOT/'references/qa-requirements.json')}


def manifest_payloads(root: Path, *, require_renders: bool = True) -> list[tuple[str, str]]:
    """Validate every file path/hash and every final page's render coverage."""
    manifest = read_json(root/'manifest.json')
    if manifest.get('schema_version') != 3:
        raise ProtocolError('Manifest schema must remain 3')
    payloads, artifact_hashes, pages = [], {}, set()
    reserved = {'manifest.json','content.json','context.json','component-record.json','request.json','candidate-status.json'}
    for artifact in manifest.get('artifacts', []):
        if artifact['id'] in artifact_hashes:
            raise ProtocolError('Duplicate artifact ID')
        count = artifact['pages']
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise ProtocolError('Invalid artifact page count')
        if artifact['path'] in reserved:
            raise ProtocolError('Artifact collides with canonical metadata')
        if artifact['role'] == 'deck' and artifact['path'] != 'pack.pptx':
            raise ProtocolError('Canonical deck path must be pack.pptx')
        path = safe_path(root, artifact['path'])
        if not path.is_file() or sha256_file(path) != artifact['sha256']:
            raise ProtocolError('Missing or stale artifact: ' + artifact['path'])
        payloads.append((artifact['path'], artifact['sha256']))
        artifact_hashes[artifact['id']] = artifact['sha256']
        pages.update((artifact['id'], n) for n in range(1, count+1))
    rendered = set()
    for render in manifest.get('renders', []):
        key = (render['artifact'], render['page'])
        if key in rendered or key not in pages:
            raise ProtocolError('Duplicate or unexpected rendered page')
        rendered.add(key)
        if render['artifact_sha256'] != artifact_hashes[render['artifact']]:
            raise ProtocolError('Render belongs to a different artifact')
        path = safe_path(root, render['path'])
        if render['path'] in reserved or not path.is_file() or sha256_file(path) != render['sha256']:
            raise ProtocolError('Missing, unsafe or stale render: ' + render['path'])
        payloads.append((render['path'], render['sha256']))
    paths = [p for p, _ in payloads]
    if len(paths) != len(set(paths)):
        raise ProtocolError('Artifact/render paths must be unique')
    if require_renders and pages != rendered:
        raise ProtocolError('Every delivered artifact page requires a current render')
    return payloads


class RepositoryPipeline:
    def __init__(self, assembly_command: list[str] | None, *, timeout: float = 300):
        self.assembly_command = assembly_command
        self.timeout = timeout

    async def assemble(self, *, run_root: Path, request_path: Path, context_path: Path,
                       content_path: Path, component_record_path: Path, revision: int) -> Candidate:
        if not self.assembly_command:
            raise ProtocolError('No trusted ContentSource-based assembly command configured')
        revision_root = run_root/'assembly'/f'revision-{revision}'
        work = revision_root/'work'
        work.mkdir(parents=True, exist_ok=False)
        inputs = {'request.json':request_path, 'context.json':context_path,
                  'content.json':content_path, 'component-record.json':component_record_path}
        before = {path:sha256_file(path) for path in inputs.values()}
        for name, path in inputs.items():
            shutil.copy2(path, work/name)
        response = await run_json_command(self.assembly_command, {
            'task_type':'ASSEMBLE_CANONICAL_PACK', 'output_directory':str(work.resolve()),
            'context_path':str((work/'context.json').resolve()),
            'content_path':str((work/'content.json').resolve()),
            'component_record_path':str((work/'component-record.json').resolve()),
            'contract':str(ROOT/'references/qa-workflow-v3.md'),
            'content_source':str(ROOT/'scripts/content_source.py'),
            'may_rewrite_content':False, 'may_release':False,
        }, cwd=work, timeout=self.timeout)
        if response.get('status') != 'PASS':
            raise ProtocolError('Assembler did not complete the canonical artifact set')
        for name, path in inputs.items():
            if sha256_file(path) != before[path] or sha256_file(work/name) != before[path]:
                raise ProtocolError('Assembler changed authoritative inputs')
        manifest = read_json(work/'manifest.json')
        if (manifest.get('content_sha256') != before[content_path] or
                manifest.get('context_sha256') != before[context_path]):
            raise ProtocolError('Assembler returned stale canonical-content bindings')
        payloads = manifest_payloads(work)
        record = read_json(component_record_path)
        record['artifact_sha256'] = sha256_file(work/'pack.pptx')
        bound_record = revision_root/'bound-component-record.json'
        write_json_atomic(bound_record, record, immutable=True)
        # Existing runtime is the staging authority, never an alternative renderer.
        stage_candidate(revision_root, request_path=request_path, context_path=context_path,
                        content_path=content_path, component_record_path=bound_record,
                        deck_path=work/'pack.pptx', manifest_path=work/'manifest.json')
        candidate = Candidate(revision_root/'candidate', revision)
        for relative, digest in payloads:
            target = safe_path(candidate.root, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(safe_path(work, relative), target)
            if sha256_file(target) != digest:
                raise ProtocolError('Artifact changed while staging: ' + relative)
        ledger = work/'warning_ledger.json'
        if ledger.is_file():
            shutil.copy2(ledger, candidate.root/'warning_ledger.json')
        errors, _, _ = audit_pack(candidate.root/'manifest.json', candidate.root/'content.json', candidate.root/'context.json')
        if errors:
            raise ProtocolError('\n'.join(errors))
        return candidate

    def snapshot(self, candidate: Candidate) -> dict[Path, str]:
        payloads = manifest_payloads(candidate.root)
        names = ['request.json','context.json','content.json','component-record.json','manifest.json']
        snapshot = {candidate.root/name:sha256_file(candidate.root/name) for name in names}
        snapshot.update({safe_path(candidate.root, name):digest for name, digest in payloads})
        if (candidate.root/'warning_ledger.json').exists():
            snapshot[candidate.root/'warning_ledger.json'] = sha256_file(candidate.root/'warning_ledger.json')
        return snapshot

    def review_inputs(self, candidate: Candidate) -> list[dict]:
        paths = self.snapshot(candidate)
        # Pack reviewers must not receive generator PASS assertions.
        excluded = {'component-record.json', 'request.json'}
        entries = []
        for path, digest in paths.items():
            if path.name in excluded:
                continue
            entry = {'path':str(path.resolve()), 'sha256':digest}
            if path.suffix.lower() in ('.json', '.md', '.txt'):
                entry['text'] = path.read_text(encoding='utf-8')
            entries.append(entry)
        return entries

    def expected(self, candidate: Candidate, method: str) -> list[dict]:
        content, manifest = read_json(candidate.root/'content.json'), read_json(candidate.root/'manifest.json')
        return [{'check_id':key, 'target':subject} for key,subject in sorted(expected_checks(content,manifest,method))]

    async def provenance(self, candidate: Candidate, request: dict) -> dict:
        errors = []
        try:
            manifest_payloads(candidate.root)
            errors, content, _ = audit_pack(candidate.root/'manifest.json', candidate.root/'content.json', candidate.root/'context.json')
            errors.extend(validate_component_record(read_json(candidate.root/'context.json'),
                                                     read_json(candidate.root/'component-record.json')))
            if read_json(candidate.root/'component-record.json').get('artifact_sha256') != request['bindings']['artifact_sha256']:
                errors.append('Component record does not bind the current deck')
        except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
            errors.append(str(exc))
        evidence = {'observation':'\n'.join(errors) if errors else 'Canonical content, all declared files and final renders match the frozen manifest.',
                    'citations':['manifest.json','content.json','context.json','component-record.json']}
        defects = []
        if errors:
            defects.append(dict(defect_id='def-'+uuid.uuid4().hex,
                generation_run_id=request['generation_run_id'],review_run_id=request['review_run_id'],
                check_id='RUNTIME.PROVENANCE',severity='release_blocking',owner='pack-assembler',scope='pack',
                description='Canonical assembly/provenance validation failed.',evidence=evidence,
                required_correction='Resolve the recorded assembly/provenance faults without altering frozen context.'))
        return dict(protocol_version=1, result_type='REVIEW', reviewer='provenance-reviewer',
                    **{k:request[k] for k in ('generation_run_id','invocation_id','agent_id','context_sha256','review_run_id')},
                    **request['bindings'], status='FAIL' if errors else 'PASS', defects=defects,
                    checks=[dict(check_id='RUNTIME.PROVENANCE',target='pack',status='FAIL' if errors else 'PASS',evidence=evidence)])

    async def release(self, candidate: Candidate, reviews: dict, *, generation_actors: set[str], run_root: Path) -> dict:
        before = self.snapshot(candidate)
        directory = run_root/'evidence'/f'revision-{candidate.revision}'
        for method, agent in (('semantic','semantic-reviewer'), ('visual','visual-reviewer')):
            result, execution = reviews[agent]
            export_release_review(result, execution, method=method, generation_actors=generation_actors,
                                  evidence_dir=directory)
        ledger = candidate.root/'warning_ledger.json'
        if ledger.is_file():
            shutil.copy2(ledger, directory/'warning_ledger.json')
        else:
            # An empty disposition ledger waives nothing. Actual typography warnings
            # still fail the existing final audit; never invent a disposition.
            write_json_atomic(directory/'warning_ledger.json',
                              {'artifact_sha256':candidate.hashes()['artifact_sha256'], 'dispositions':[]}, immutable=True)
        # These are output slots, explicitly NOT evidence of PASS. The existing
        # release audit reruns and overwrites all five repository-owned audits.
        for name in ('contract','year_profile','typography','containment','visual'):
            write_json_atomic(directory/f'{name}.json', {'status':'UNREVIEWED'}, immutable=True)
        evidence = {key:directory/f'{key}.json' for key in REQUIRED_RELEASE_EVIDENCE}
        result = await asyncio.to_thread(promote_release, candidate.root, run_root/'released', evidence)
        if any(not p.is_file() or sha256_file(p) != digest for p,digest in before.items()):
            shutil.rmtree(run_root/'released', ignore_errors=True)
            raise ProtocolError('Candidate changed during final release audit')
        if result['status'] == 'RELEASED':
            manifest = read_json(candidate.root/'manifest.json')
            for artifact in manifest['artifacts']:
                target = safe_path(run_root/'released', artifact['path'])
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(safe_path(candidate.root, artifact['path']), target)
        return result
