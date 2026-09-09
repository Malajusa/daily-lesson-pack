"""Shared deterministic manifests for the complete and component distributions."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess


def source_revision(root: Path) -> str | None:
    """Identify only an exact, clean checkout; an exported/dirty tree stays unbound."""
    root = Path(root).resolve()
    try:
        def git(*args: str) -> str:
            return subprocess.run(['git', '-C', str(root), *args], check=True,
                                  capture_output=True, text=True, timeout=10).stdout.strip()
        if Path(git('rev-parse', '--show-toplevel')).resolve() != root:
            return None
        if git('status', '--porcelain', '--untracked-files=normal'):
            return None
        revision = git('rev-parse', 'HEAD')
        return revision if re.fullmatch('[a-f0-9]{40}', revision) else None
    except (OSError, subprocess.SubprocessError):
        return None


def manifest(version: str, files: dict[str, bytes], *, source_commit: str | None = None) -> bytes:
    if source_commit is not None and not re.fullmatch('[a-f0-9]{40}', source_commit):
        raise ValueError('A package source commit must be a full Git SHA')
    entries = [dict(path=name, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
               for name, data in sorted(files.items())]
    return (json.dumps(dict(version=version, source_commit=source_commit, files=entries),
                       indent=2) + '\n').encode('utf-8')
