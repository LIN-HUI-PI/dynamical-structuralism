"""LIN Human-Control Boundary v0.2: illustrative, in-memory safety harness.
Not a clinical, hardware, or formal verification claim.
"""
from boundary import Boundary, State

class BoundaryV02(Boundary):
    def __init__(self):
        super().__init__()
        self.faults = []

    def inject_fault(self, kind):
        """Fail closed on simulated faults; invalidate outstanding approvals."""
        if kind not in {'CHANNEL_LOSS', 'STALE_APPROVAL', 'ACTUATOR_MISMATCH', 'AUDIT_FAILURE'}:
            raise ValueError('unknown fault')
        self.faults.append(kind)
        self.log('FAULT_INJECTED', kind=kind)
        self.freeze()
        return True

    def execute(self, ident):
        # Refuse execution if a simulated fault has not been cleared by human-led recovery.
        if self.faults:
            self.log('FAULT_EXECUTION_BLOCKED', proposal=ident)
            return False
        return super().execute(ident)

    def restore(self, human_authorized):
        ok = super().restore(human_authorized)
        if ok:
            self.faults.clear()
            self.log('FAULTS_CLEARED_BY_RECOVERY')
        return ok

    def transition(self, event, **kwargs):
        """Explicit, auditable transition interface; unsupported events fail closed."""
        transitions = {
            'FREEZE': lambda: (self.freeze() or True),
            'DECOMPRESS': lambda: self.decompress(kwargs.get('human_authorized', False)),
            'CONFIRM': lambda: self.confirm(kwargs.get('self_declaration', False), kwargs.get('boundary_reassertion', False), kwargs.get('stable_window', False)),
            'RESTORE': lambda: self.restore(kwargs.get('human_authorized', False)),
        }
        if event not in transitions:
            self.log('UNKNOWN_TRANSITION_BLOCKED', requested=event)
            return False
        if event == 'FREEZE' and self.state != State.READY:
            self.log('INVALID_TRANSITION_BLOCKED', requested=event)
            return False
        return transitions[event]()
