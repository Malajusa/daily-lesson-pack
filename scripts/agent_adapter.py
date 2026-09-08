"""Trusted host adapter boundary; provider credentials and model calls stay outside.

AgentExecution metadata must be captured by the actual host, not supplied by the
model authoring result JSON. These receipts are auditable, not cryptographic proof.
Local command execution is NOT an operating-system security sandbox.
"""
from __future__ import annotations

import asyncio
import copy
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from agent_protocol import ProtocolError, json_bytes, parse_json


@dataclass(frozen=True)
class AgentExecution:
    result: dict
    actor: str
    execution_id: str
    source: str
    transcript: str

    def validate_receipt(self) -> None:
        if self.source not in ('collaboration', 'external-runner', 'human-review'):
            raise ProtocolError('Unsupported host receipt source')
        if not all(isinstance(x, str) and x.strip() for x in (self.actor, self.execution_id, self.transcript)):
            raise ProtocolError('Actual host actor, execution ID and transcript are required')


class AgentAdapter(Protocol):
    async def invoke(self, *, agent_id: str, request: dict) -> AgentExecution:
        """Execute in fresh host context and return result plus actual host metadata."""
        ...


async def run_json_command(argv: list[str], payload: dict, *, cwd: Path,
                           timeout: float = 300, max_bytes: int = 16 * 1024 * 1024) -> dict:
    if (not isinstance(argv, list) or not argv or
            not all(isinstance(v, str) and v for v in argv)):
        raise ProtocolError('A trusted command must be a non-empty argv list, not a shell string')
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0 < timeout <= 3600:
        raise ProtocolError('Command timeout must be between 0 and 3600 seconds')
    process = await asyncio.create_subprocess_exec(*argv, cwd=str(cwd), stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(json_bytes(payload)), timeout)
    except BaseException:
        if process.returncode is None:
            process.kill()
        await process.wait()
        raise
    if process.returncode:
        raise ProtocolError(f'Host command failed ({process.returncode}): '
                            + stderr.decode('utf-8', errors='replace')[-2000:])
    if len(stdout) > max_bytes:
        raise ProtocolError('Host response exceeds configured size limit')
    try:
        return parse_json(stdout.decode('utf-8'))
    except UnicodeDecodeError as exc:
        raise ProtocolError('Host response must be UTF-8 JSON') from exc


class JsonCommandAdapter:
    """JSON stdin/stdout transport for explicitly configured host commands.

Output: {"result": <schema-validated model result>, "receipt":
{"actor": "actual host actor", "execution_id": "actual execution",
"source": "external-runner"}, "transcript": "raw host transcript"}.
Never populate receipt fields by asking the model to invent them.
"""
    def __init__(self, commands: dict[str, list[str]], *, timeout: float = 300):
        self.commands = copy.deepcopy(commands)
        self.timeout = timeout

    async def invoke(self, *, agent_id: str, request: dict) -> AgentExecution:
        if agent_id not in self.commands:
            raise ProtocolError('No host command configured for ' + agent_id)
        with tempfile.TemporaryDirectory(prefix='dlp-agent-') as directory:
            value = await run_json_command(self.commands[agent_id], request,
                                           cwd=Path(directory), timeout=self.timeout)
        if set(value) != {'result', 'receipt', 'transcript'} or not isinstance(value['receipt'], dict):
            raise ProtocolError('Host must return result, receipt and raw transcript separately')
        receipt = value['receipt']
        if set(receipt) != {'actor', 'execution_id', 'source'}:
            raise ProtocolError('Invalid host execution receipt')
        execution = AgentExecution(value['result'], receipt['actor'], receipt['execution_id'],
                                   receipt['source'], value['transcript'])
        execution.validate_receipt()
        return execution
