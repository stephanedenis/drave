"""Tests du masque de perte : le prompt est lu, mais ne compte pas."""
from __future__ import annotations

import random
import unittest

from llm.masque import exemples, fenetre, fenetres_validation, poids_masque

TEXTE = """### system
sys
### user
question 1
### professeur
réponse 1
### system
sys
### user
question 2
### professeur
réponse 2
"""


class TestMasque(unittest.TestCase):
    def test_exemples(self):
        ex = exemples(TEXTE)
        self.assertEqual(len(ex), 2)
        self.assertIn(b"question 1", ex[0][0])
        self.assertEqual(ex[0][1], "réponse 1".encode())

    def test_fenetre_masque(self):
        prompt, reponse = exemples(TEXTE)[0]
        x, m = fenetre(prompt, reponse, 64, random.Random(0))
        self.assertEqual(len(x), 64)
        self.assertEqual(len(m), 64)
        self.assertEqual(poids_masque(m), len(reponse))

    def test_fenetre_longue(self):
        prompt, reponse = exemples(TEXTE)[0]
        seq = 8
        x, m = fenetre(prompt, reponse, seq, random.Random(0))
        self.assertEqual(len(x), seq)
        self.assertGreaterEqual(poids_masque(m), 1)

    def test_validation_couvre_les_reponses(self):
        prompt, reponse = exemples(TEXTE)[0]
        total = sum(poids_masque(m) for _, m in fenetres_validation(prompt, reponse, 8))
        self.assertGreaterEqual(total, len(reponse))


if __name__ == "__main__":
    unittest.main()
