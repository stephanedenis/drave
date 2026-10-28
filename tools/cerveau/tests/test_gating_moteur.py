from __future__ import annotations
import unittest
from cerveau.gating_moteur import mesurer


class TestGatingMoteur(unittest.TestCase):
    def test_mesure(self):
        r = mesurer()
        self.assertEqual(r["n"], 8)
        self.assertIn("conflit", r)


if __name__ == "__main__":
    unittest.main()
