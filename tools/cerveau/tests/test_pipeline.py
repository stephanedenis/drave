from __future__ import annotations
import unittest
from cerveau.pipeline import Pipeline
from jeux.regles import echecs as E


class TestPipeline(unittest.TestCase):
    def test_chaine(self):
        p = Pipeline()
        ctx = E.rsn_depuis_position(E.Position.depart())
        code = p.percevoir("Nf3", "echecs", ctx, "notation")
        self.assertEqual(code["de"], 62)
        self.assertEqual(len(p.memoire.episodes), 1)
        p.consolider()
        self.assertTrue(p.prototypes)

    def test_repondre(self):
        p = Pipeline()
        ctx = E.rsn_depuis_position(E.Position.depart())
        code = p.percevoir("Nf3", "echecs", ctx)
        kind, r = p.repondre(code)
        self.assertEqual(kind, "memoire")
        self.assertTrue(r["exact"])


if __name__ == "__main__":
    unittest.main()
