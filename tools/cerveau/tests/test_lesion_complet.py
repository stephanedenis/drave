from __future__ import annotations
import unittest
from cerveau.lesion_complet import mesurer


class TestLesionComplet(unittest.TestCase):
    def test_dose(self):
        r = mesurer()
        self.assertEqual(r["M3"]["capacites"]["0"]["span"], 0)
        self.assertEqual(r["M3"]["capacites"]["12"]["span"], 12)
        self.assertEqual(r["sham"]["M3"]["exact"], 1.0)
        self.assertIn("0", r["M5"]["ordres"])


if __name__ == "__main__":
    unittest.main()
