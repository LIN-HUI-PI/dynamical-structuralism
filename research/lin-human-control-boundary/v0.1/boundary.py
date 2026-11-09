"""LIN Human-Control Boundary MVP v0.1 — illustrative governance test harness.
Not an implementation or validation of the full LIN specification.
"""
from dataclasses import dataclass, field
from enum import Enum
import json

class State(str, Enum):
    READY = 'READY'
    FROZEN = 'FROZEN'
    DECOMPRESS = 'DECOMPRESS'
    CONFIRM = 'CONFIRM'

@dataclass
class Boundary:
    state: State = State.READY
    pending: dict = field(default_factory=dict)
    approved: set = field(default_factory=set)
    executed: list = field(default_factory=list)
    audit: list = field(default_factory=list)
    counter: int = 0

    def log(self, event, **details):
        self.audit.append({'event': event, 'state': self.state.value, **details})

    def propose(self, action):
        self.counter += 1
        ident = f'P{self.counter:03}'
        if self.state != State.READY:
            self.log('PROPOSAL_BLOCKED', proposal=ident)
            return None
        self.pending[ident] = action
        self.log('PROPOSED', proposal=ident, action=action)
        return ident

    def approve(self, ident):
        if self.state != State.READY or ident not in self.pending:
            self.log('APPROVAL_DENIED', proposal=ident)
            return False
        self.approved.add(ident)
        self.log('APPROVED', proposal=ident)
        return True

    def reject(self, ident):
        existed = ident in self.pending
        self.pending.pop(ident, None)
        self.approved.discard(ident)
        self.log('REJECTED', proposal=ident)
        return existed

    def revoke(self, ident):
        existed = ident in self.pending
        self.pending.pop(ident, None)
        self.approved.discard(ident)
        self.log('REVOKED', proposal=ident)
        return existed

    def execute(self, ident):
        if self.state != State.READY or ident not in self.pending or ident not in self.approved:
            self.log('EXECUTION_BLOCKED', proposal=ident)
            return False
        action = self.pending.pop(ident)
        self.approved.remove(ident)
        self.executed.append({'proposal': ident, 'action': action})
        self.log('EXECUTED', proposal=ident)
        return True

    def freeze(self):
        self.state = State.FROZEN
        self.pending.clear()
        self.approved.clear()
        self.log('FREEZE')

    def decompress(self, human_authorized):
        if self.state != State.FROZEN or not human_authorized:
            self.log('DECOMPRESS_BLOCKED')
            return False
        self.state = State.DECOMPRESS
        self.log('DECOMPRESS')
        return True

    def confirm(self, self_declaration, boundary_reassertion, stable_window):
        if self.state != State.DECOMPRESS or not all((self_declaration, boundary_reassertion, stable_window)):
            self.log('CONFIRM_BLOCKED')
            return False
        self.state = State.CONFIRM
        self.log('CONFIRM')
        return True

    def restore(self, human_authorized):
        if self.state != State.CONFIRM or not human_authorized:
            self.log('RESTORE_BLOCKED')
            return False
        self.state = State.READY
        self.log('RESTORED')
        return True

if __name__ == '__main__':
    b = Boundary()
    p = b.propose('demo_move')
    b.approve(p)
    b.execute(p)
    print(json.dumps({'executed': b.executed, 'audit': b.audit}, indent=2, ensure_ascii=False))
