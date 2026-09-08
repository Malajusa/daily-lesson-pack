"""Persist execution state separately from the immutable dependency plan."""
from __future__ import annotations

import copy
from pathlib import Path
from agent_protocol import ProtocolError, write_json_atomic


class ExecutionState:
    def __init__(self, plan: dict, path: Path):
        self.path = Path(path)
        self.nodes = {n['id']: copy.deepcopy(n) for n in plan['nodes']}
        self.events: list[dict] = []
        self.invocations: set[str] = set()
        self._save()

    def _save(self) -> None:
        write_json_atomic(self.path, {'nodes': list(self.nodes.values()), 'events': self.events})

    def _transition(self, node_id: str, state: str, *, invocation_id: str | None = None) -> None:
        node = self.nodes[node_id]
        self.events.append({'node': node_id, 'from': node['state'], 'to': state,
                            'invocation_id': invocation_id})
        node['state'] = state
        if invocation_id:
            node['invocation_id'] = invocation_id
        self._save()

    def passed(self, node_id: str) -> bool:
        return self.nodes[node_id]['state'] == 'PASS'

    def begin(self, node_id: str, invocation_id: str) -> None:
        node = self.nodes[node_id]
        if node['state'] not in ('PENDING', 'BLOCKED', 'FAIL', 'STALE'):
            raise ProtocolError(f'Cannot start {node_id} from {node["state"]}')
        if not all(self.passed(dep) for dep in node['depends_on']):
            raise ProtocolError('Unsatisfied dependency barrier: ' + node_id)
        if not invocation_id or invocation_id in self.invocations:
            raise ProtocolError('Every execution requires a fresh invocation ID')
        self.invocations.add(invocation_id)
        self._transition(node_id, 'READY', invocation_id=invocation_id)
        self._transition(node_id, 'RUNNING', invocation_id=invocation_id)

    def finish(self, node_id: str, passed: bool) -> None:
        if self.nodes[node_id]['state'] != 'RUNNING':
            raise ProtocolError('Only a running invocation may finish: ' + node_id)
        self._transition(node_id, 'PASS' if passed else 'FAIL',
                         invocation_id=self.nodes[node_id]['invocation_id'])

    def invalidate(self, node_id: str) -> None:
        affected = {node_id}
        while True:
            expanded = affected | {name for name, n in self.nodes.items()
                                   if set(n['depends_on']) & affected}
            if expanded == affected:
                break
            affected = expanded
        if any(self.nodes[name]['state'] == 'RUNNING' for name in affected):
            raise ProtocolError('Cannot invalidate running work; collect reviews first')
        for name in self.nodes:
            if name in affected and self.nodes[name]['state'] in ('PASS', 'FAIL', 'READY'):
                self._transition(name, 'STALE')
