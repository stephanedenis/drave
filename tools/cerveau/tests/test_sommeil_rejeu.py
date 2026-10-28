from __future__ import annotations
import unittest
from cerveau.sommeil_rejeu import mesurer


class TestSommeilRejeu(unittest.TestCase):
    def test_split(self):
        r = mesurer(graine=1)
        self.assertEqual(r["codes_train"] + r["codes_test"], 29)
        self.assertIn("rejeu_exact", r)
        self.assertIn("hybride_exact", r)


if __name__ == "__main__":
    unittest.main()
