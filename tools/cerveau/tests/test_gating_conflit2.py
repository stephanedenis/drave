from __future__ import annotations
import unittest
from cerveau.gating_conflit2 import mesurer


class TestGatingConflit2(unittest.TestCase):
    def test_replication(self):
        r = mesurer()
        self.assertIn("conflit", r)
        self.assertIn("commutation", r)


if __name__ == "__main__":
    unittest.main()
