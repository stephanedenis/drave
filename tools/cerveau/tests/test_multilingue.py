from __future__ import annotations
import unittest
from cerveau.multilingue import charger_surfaces


class TestMultilingue(unittest.TestCase):
    def test_chargement(self):
        surfaces, meta = charger_surfaces()
        self.assertEqual(len(surfaces), 528)
        self.assertEqual(meta["items"], 528)
        self.assertGreaterEqual(meta["langues_corpus"], 60)
        self.assertEqual(meta["sources"]["B5"]["paires"] + meta["sources"]["B7"]["paires"], 30)

    def test_langues_absentes_declarees(self):
        _, meta = charger_surfaces()
        for langue in ("ky", "lo", "mt", "si", "yo"):
            self.assertIn(langue, meta["langues_absentes_du_corpus"])


if __name__ == "__main__":
    unittest.main()
