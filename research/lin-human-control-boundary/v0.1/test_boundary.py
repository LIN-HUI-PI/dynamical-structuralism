import unittest
from boundary import Boundary, State

class BoundaryTests(unittest.TestCase):
    def test_01_authorized_execution(self):
        b=Boundary(); p=b.propose('move'); self.assertFalse(b.execute(p)); self.assertTrue(b.approve(p)); self.assertTrue(b.execute(p)); self.assertEqual(len(b.executed),1)
    def test_02_rejection(self):
        b=Boundary(); p=b.propose('move'); b.reject(p); self.assertFalse(b.approve(p)); self.assertFalse(b.execute(p)); self.assertFalse(b.executed)
    def test_03_revocation(self):
        b=Boundary(); p=b.propose('move'); b.approve(p); b.revoke(p); self.assertFalse(b.execute(p)); self.assertFalse(b.executed)
    def test_04_unauthorized_attempt(self):
        b=Boundary(); self.assertFalse(b.execute('FAKE')); self.assertFalse(b.executed)
    def test_05_freeze_and_recovery(self):
        b=Boundary(); p=b.propose('move'); b.approve(p); b.freeze(); self.assertEqual(b.state,State.FROZEN); self.assertFalse(b.execute(p)); self.assertIsNone(b.propose('other')); self.assertFalse(b.decompress(False)); self.assertTrue(b.decompress(True)); self.assertFalse(b.confirm(True,False,True)); self.assertTrue(b.confirm(True,True,True)); self.assertFalse(b.restore(False)); self.assertTrue(b.restore(True)); self.assertFalse(b.execute(p)); self.assertFalse(b.executed)
    def test_06_single_use_authorization(self):
        b=Boundary(); p=b.propose('move'); b.approve(p); self.assertTrue(b.execute(p)); self.assertFalse(b.execute(p)); self.assertEqual(len(b.executed),1)

if __name__=='__main__': unittest.main(verbosity=2)
