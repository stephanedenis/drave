from __future__ import annotations
import unittest
from cerveau.pipeline_semantique import PipelineSemantique
from jeux.regles import echecs as E


class TestPipelineSemantique(unittest.TestCase):
    def test_m1_m5_m6_m8(self):
        p = PipelineSemantique()
        ctx = E.rsn_depuis_position(E.Position.depart())
        code = p.percevoir("Nf3", "echecs", ctx)
        self.assertEqual(code["de"], 62)
        r = p.selectionner()
        self.assertIn("exact", r)
        self.assertEqual(len(p.memoire.episodes), 1)
        p.consolider()
        self.assertTrue(p.sommeil.nom)


if __name__ == "__main__":
    unittest.main()
