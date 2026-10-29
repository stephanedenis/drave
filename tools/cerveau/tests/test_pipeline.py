from __future__ import annotations
import unittest
from cerveau.pipeline import Pipeline
from jeux.regles import echecs as E
from semantique.typed_corpus import items


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

    def test_contexte_rsn(self):
        """Le pipeline porte le contexte RSN, pas son résumé en chaîne."""
        it = next(i for i in items() if i.jeu == "cartes" and i.contexte_rsn is not None)
        p = Pipeline()
        code = p.percevoir_item(it)
        self.assertIsNotNone(code)
        self.assertEqual(code, it.code)
        self.assertEqual(len(p.memoire.episodes), 1)


if __name__ == "__main__":
    unittest.main()
