from __future__ import annotations
import unittest
from cerveau.bus import Bus
from cerveau.hub import Hub
from jeux.regles import echecs as E


class TestBus(unittest.TestCase):
    def test_publier_rejouer(self):
        b = Bus(); vus = []
        b.abonner("sens", lambda e: vus.append(e.valeur))
        b.publier("sens", {"jeu": "echecs"}, "test")
        self.assertEqual(vus, [{"jeu": "echecs"}])
        self.assertEqual(len(list(b.rejouer("sens"))), 1)
        self.assertEqual(b.compter("sens"), 1)

    def test_hub(self):
        h = Hub()
        ctx = E.rsn_depuis_position(E.Position.depart())
        code = h.percevoir("Nf3", "echecs", ctx)
        self.assertEqual(code["jeu"], "echecs")
        self.assertEqual(code["de"], 62)
        self.assertEqual(code["vers"], 45)
        surface = h.rendre(code, ctx)
        self.assertIn(surface, ("Nf3", "nf3", "g1f3", "g1-f3"))


if __name__ == "__main__":
    unittest.main()
