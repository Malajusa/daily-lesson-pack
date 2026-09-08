import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

class StateTests(unittest.TestCase):
    def test_cannot_pass_without_running_or_skip_dependency(self):
        from agent_state import ExecutionState
        from agent_protocol import ProtocolError
        with tempfile.TemporaryDirectory() as tmp:
            plan={'nodes':[dict(id='one',state='PENDING',depends_on=[]),dict(id='two',state='BLOCKED',depends_on=['one'])]}
            state=ExecutionState(plan,Path(tmp)/'state.json')
            with self.assertRaises(ProtocolError):state.finish('one',True)
            with self.assertRaises(ProtocolError):state.begin('two','inv-two')
            state.begin('one','inv-one');state.finish('one',True)
            state.begin('two','inv-two');state.finish('two',True)
            self.assertTrue(state.passed('two'))
            state.invalidate('one')
            self.assertFalse(state.passed('two'))
            with self.assertRaises(ProtocolError):state.begin('one','inv-one')

    def test_fail_requires_a_new_invocation(self):
        from agent_state import ExecutionState
        from agent_protocol import ProtocolError
        with tempfile.TemporaryDirectory() as tmp:
            state=ExecutionState({'nodes':[dict(id='x',state='PENDING',depends_on=[])]},Path(tmp)/'state.json')
            state.begin('x','first');state.finish('x',False)
            with self.assertRaises(ProtocolError):state.finish('x',True)
            state.begin('x','second');state.finish('x',True)
            self.assertTrue(state.passed('x'))
