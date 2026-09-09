#!/usr/bin/env python3
"""Check the exact downloaded bytes before extracting a candidate skill package.

A matching checksum proves identity relative to the caller's trusted expected
checksum, not teaching quality or approval to release. Never execute archive
code until its identity and dependency closure have been independently accepted.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import stat
import unicodedata
import zipfile

from agent_protocol import ProtocolError, parse_json, safe_path

# Operational resource caps, not pedagogical rules. Current packages are much smaller.
MAX_COMPRESSED_BYTES = 64 * 1024 * 1024
MAX_EXPANDED_BYTES = 256 * 1024 * 1024
MAX_FILES = 10000
RESERVED = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$', re.I)


def _safe_member(name: str) -> None:
    safe_path(Path('/archive-check'), name)
    for part in name.split('/'):
        if (part.endswith((' ', '.')) or RESERVED.fullmatch(part) or
                any(ord(char) < 32 or char in '<>"|?*' for char in part)):
            raise ProtocolError('Non-portable archive path: ' + name)


def _verified_bytes(package: Path, *, expected_sha256: str,
                    expected_source_commit: str | None = None) -> tuple[dict, dict[str, bytes]]:
    if not re.fullmatch(r'[a-fA-F0-9]{64}', expected_sha256 or ''):
        raise ProtocolError('A trusted external SHA-256 is required')
    if expected_source_commit is not None and not re.fullmatch(r'[a-f0-9]{40}', expected_source_commit):
        raise ProtocolError('Expected source commit must be a full Git SHA')
    with Path(package).open('rb') as stream:
        raw = stream.read(MAX_COMPRESSED_BYTES + 1)
    if len(raw) > MAX_COMPRESSED_BYTES:
        raise ProtocolError('Compressed package exceeds the operational size limit')
    actual_hash = hashlib.sha256(raw).hexdigest()
    if actual_hash != expected_sha256.lower():
        raise ProtocolError('Downloaded package SHA-256 mismatch')
    files: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            if not entries or len(entries) > MAX_FILES:
                raise ProtocolError('Invalid package file count')
            if sum(entry.file_size for entry in entries) > MAX_EXPANDED_BYTES:
                raise ProtocolError('Expanded package exceeds the operational size limit')
            identities = set()
            roots = set()
            for entry in entries:
                name = entry.filename
                _safe_member(name)
                key = unicodedata.normalize('NFC', name).casefold()
                if key in identities:
                    raise ProtocolError('Duplicate or case-colliding archive member: ' + name)
                identities.add(key)
                mode = (entry.external_attr >> 16) & 0o170000
                if entry.is_dir() or mode not in (0, stat.S_IFREG) or entry.flag_bits & 1:
                    raise ProtocolError('Only unencrypted regular files may be packaged: ' + name)
                if '/' not in name:
                    raise ProtocolError('Package must have one named skill root')
                roots.add(name.split('/')[0])
                files[name] = archive.read(entry)
            if len(roots) != 1:
                raise ProtocolError('Archive contains multiple skill roots')
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as exc:
        raise ProtocolError('Unreadable package: ' + str(exc)) from exc
    root = next(iter(roots))
    manifest_name = root + '/PACKAGE-MANIFEST.json'
    if manifest_name not in files or root + '/SKILL.md' not in files:
        raise ProtocolError('Missing package manifest or skill entrypoint')
    manifest = parse_json(files[manifest_name].decode('utf-8'))
    if not isinstance(manifest.get('version'), str) or not manifest['version'].strip():
        raise ProtocolError('Manifest requires a version')
    entries = manifest.get('files')
    if not isinstance(entries, list) or not entries:
        raise ProtocolError('Manifest requires a complete file inventory')
    declared = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {'path', 'bytes', 'sha256'}:
            raise ProtocolError('Invalid manifest file record')
        relative = entry['path']
        _safe_member(relative)
        name = root + '/' + relative
        if name in declared:
            raise ProtocolError('Duplicate manifest member: ' + relative)
        declared.add(name)
        data = files.get(name)
        if (data is None or type(entry['bytes']) is not int or len(data) != entry['bytes'] or
                hashlib.sha256(data).hexdigest() != entry['sha256']):
            raise ProtocolError('Missing or changed packaged file: ' + relative)
    if declared != set(files) - {manifest_name}:
        raise ProtocolError('Manifest does not describe the exact archive file set')
    version_file = root + '/VERSION'
    if version_file in files:
        version = files[version_file].decode('utf-8').strip()
    else:
        package_metadata = parse_json(files.get(root + '/PACKAGE.json', b'{}').decode('utf-8'))
        version = package_metadata.get('daily_lesson_pack_version')
    if version != manifest['version']:
        raise ProtocolError('Package and manifest versions disagree')
    source = manifest.get('source_commit')
    if expected_source_commit is not None and source != expected_source_commit:
        raise ProtocolError('Package belongs to another or unidentified source revision')
    return ({'status': 'PASS', 'check': 'package-integrity-only',
             'release_authorised': False, 'sha256': actual_hash,
             'source_commit': source, 'version': version, 'root': root,
             'files': len(files)}, files)


def verify_archive(package: Path, *, expected_sha256: str,
                   expected_source_commit: str | None = None) -> dict:
    report, _ = _verified_bytes(package, expected_sha256=expected_sha256,
                                expected_source_commit=expected_source_commit)
    return report


def extract_verified(package: Path, destination: Path, *, expected_sha256: str,
                     expected_source_commit: str | None = None) -> dict:
    report, files = _verified_bytes(package, expected_sha256=expected_sha256,
                                    expected_source_commit=expected_source_commit)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    try:
        for name, data in files.items():
            path = safe_path(destination, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(data)
    except Exception:
        shutil.rmtree(destination)
        raise
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--expected-sha256', required=True)
    parser.add_argument('--expected-source-commit')
    parser.add_argument('--extract', type=Path)
    args = parser.parse_args()
    try:
        options = dict(expected_sha256=args.expected_sha256,
                       expected_source_commit=args.expected_source_commit)
        report = (extract_verified(args.package, args.extract, **options) if args.extract
                  else verify_archive(args.package, **options))
        print(json.dumps(report, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        parser.exit(1, 'Package rejected: ' + str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
