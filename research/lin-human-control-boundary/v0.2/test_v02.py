import unittest
from boundary import State
from boundary_v02 import BoundaryV02

class V02Tests(unittest.TestCase):
    def test_authorized(self):
        b=BoundaryV02(); p=b.propose('move'); self.assertTrue(b.approve(p)); self.assertTrue(b.execute(p))
    def test_reject(self):
        b=BoundaryV02(); p=b.propose('move'); b.reject(p); self.assertFalse(b.execute(p))
    def test_revoke(self):
        b=BoundaryV02(); p=b.propose('move'); b.approve(p); b.revoke(p); self.assertFalse(b.execute(p))
    def test_fault_types_block(self):
        for fault in ('CHANNEL_LOSS','STALE_APPROVAL','ACTUATOR_MISMATCH','AUDIT_FAILURE'):
            with self.subTest(fault=fault):
                b=BoundaryV02(); p=b.propose('move'); b.approve(p); b.inject_fault(fault)
                self.assertEqual(b.state,State.FROZEN); self.assertFalse(b.execute(p)); self.assertFalse(b.executed)
    def test_invalid_transition(self):
        b=BoundaryV02(); self.assertFalse(b.transition('RESTORE',human_authorized=True)); self.assertFalse(b.transition('BYPASS'))
    def test_recovery_requires_all_checks(self):
        b=BoundaryV02(); b.inject_fault('CHANNEL_LOSS')
        self.assertFalse(b.transition('DECOMPRESS'))
        self.assertTrue(b.transition('DECOMPRESS',human_authorized=True))
        self.assertFalse(b.transition('CONFIRM',self_declaration=True,boundary_reassertion=False,stable_window=True))
        self.assertTrue(b.transition('CONFIRM',self_declaration=True,boundary_reassertion=True,stable_window=True))
        self.assertFalse(b.transition('RESTORE'))
        self.assertTrue(b.transition('RESTORE',human_authorized=True))
        self.assertEqual(b.state,State.READY)
        self.assertFalse(b.faults)
    def test_old_approval_not_reused(self):
        b=BoundaryV02(); p=b.propose('move'); b.approve(p); b.inject_fault('STALE_APPROVAL')
        b.transition('DECOMPRESS',human_authorized=True)
        b.transition('CONFIRM',self_declaration=True,boundary_reassertion=True,stable_window=True)
        b.transition('RESTORE',human_authorized=True)
        self.assertFalse(b.execute(p))
    def test_single_use(self):
        b=BoundaryV02(); p=b.propose('move'); b.approve(p); self.assertTrue(b.execute(p)); self.assertFalse(b.execute(p))

if __name__=='__main__': unittest.main(verbosity=2)
