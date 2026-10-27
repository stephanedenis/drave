from __future__ import annotations
import unittest
from semantique.universaux import (CHAMPS, DIM, code_rsn, depuis_index, index_code,
                                   rsn_depuis_code, vecteur)
from jeux.rsn import RSN


class TestUniversaux(unittest.TestCase):
    def test_code_typé(self):
        r = RSN("echecs", "coup", {"de": 62, "vers": 45, "promotion": None, "roque": None})
        c = code_rsn(r)
        self.assertEqual(c["jeu"], "echecs")
        self.assertEqual(c["action"], "deplacer")
        self.assertEqual(c["de"], 62)
        self.assertEqual(sum(vecteur(c)), len(CHAMPS))  # un one-hot par champ
        self.assertEqual(len(vecteur(c)), DIM)

    def test_index_roundtrip(self):
        r = RSN("cartes", "coup", {"carte": 47})
        c = code_rsn(r)
        idx = index_code(c)
        self.assertEqual(depuis_index(idx), c)

    def test_rsn_roundtrip(self):
        for corps in ({"de": 62, "vers": 45, "promotion": None, "roque": None},
                      {"carte": 47}, {"case": 4, "symbole": "X"},
                      {"chemin": [1, 2, 3]}, {"taille": 9, "passe": True}):
            r = RSN("echecs" if "de" in corps else "cartes" if "carte" in corps else "dames" if "chemin" in corps else "go", "coup", corps)
            c = code_rsn(r)
            r2 = rsn_depuis_code(c)
            self.assertEqual(r2.corps, r.corps)


if __name__ == "__main__":
    unittest.main()
