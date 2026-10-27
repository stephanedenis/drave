from __future__ import annotations
import unittest
from cerveau.memoire_travail import MemoireTravail
from cerveau.episodique import Episodique
from cerveau.sequences import partie


class TestModules(unittest.TestCase):
    def test_span(self):
        s = partie("echecs", 0, 5)
        m = MemoireTravail(5)
        self.assertGreaterEqual(m.span([s])["span"], 1)

    def test_episodique(self):
        e = Episodique()
        a = {"jeu": "echecs", "action": "deplacer", "de": 62, "vers": 45}
        b = {"jeu": "echecs", "action": "deplacer", "de": 52, "vers": 36}
        e.stocker("Nf3", a); e.stocker("e4", b)
        self.assertTrue(e.rappel(a)["exact"])
        self.assertTrue(e.separation(a, b)["distincts"])


if __name__ == "__main__":
    unittest.main()
