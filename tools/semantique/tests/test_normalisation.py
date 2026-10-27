from __future__ import annotations
import unittest
from semantique.normalisation import normaliser


class TestNormalisation(unittest.TestCase):
    def test_morpion(self):
        n = normaliser("tres en ratlla A1")
        self.assertIn("[jeu.morpion]", n)
        self.assertIn("a1", n)

    def test_echecs(self):
        n = normaliser("cavalier g1 f3")
        self.assertIn("[echecs.piece.N]", n)
        self.assertIn("g1 f3", n)

    def test_cartes(self):
        n = normaliser("roi de pique")
        self.assertIn("[cartes.rang.13]", n)
        self.assertIn("[cartes.couleur.S]", n)

    def test_deux_langues_meme_forme(self):
        a = normaliser("cavalier g1 f3")
        b = normaliser("knight g1 f3")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
