"""Tests de la couche multilingue : le même sens dans plusieurs écritures."""
from __future__ import annotations

import unittest

from jeux.codecs import detecte_jeu, lit
from jeux.lexique_multilingue import MULTI
from jeux.regles import cartes as C
from jeux.regles import echecs as E


class TestLangues(unittest.TestCase):
    def test_couverture(self):
        c = MULTI.couverture()
        self.assertGreaterEqual(c["langues"], 70)
        self.assertGreaterEqual(c["concepts"], 30)
        self.assertGreaterEqual(c["couples"], 1400)
        self.assertGreaterEqual(c["n_langues_fortes"], 30)

    def test_piece_dans_quatre_ecritures(self):
        depart = E.rsn_depuis_position(E.Position.depart())
        for texte in ("конь g1 f3", "घोड़ा g1 f3", "馬 g1 f3", "حصان g1 f3"):
            lec = lit(texte, jeu="echecs", niveau=4, contexte=depart)
            self.assertTrue(lec.ok, (texte, lec.erreurs))
            self.assertEqual(lec.rsn.corps["de"], 62, texte)
            self.assertEqual(lec.rsn.corps["vers"], 45, texte)

    def test_carte_dans_trois_ecritures(self):
        for texte, carte in (("туз черви", C.carte_id(14, 2)),
                             ("ملك كوبة", C.carte_id(13, 2)),
                             ("10 черви", C.carte_id(10, 2))):
            lec = lit(texte, jeu="cartes", niveau=4)
            self.assertTrue(lec.ok, (texte, lec.erreurs))
            self.assertEqual(lec.rsn.corps["carte"], carte, texte)

    def test_detection_des_jeux(self):
        for texte, jeu in (("шахматы", "echecs"), ("国际象棋", "echecs"),
                           ("井字棋", "morpion"), ("игра го", "go"),
                           ("dames anglaises", "dames")):
            trouve = detecte_jeu(texte)
            self.assertIsNotNone(trouve, texte)
            self.assertEqual(trouve[0], jeu, texte)

    def test_invariance_empreinte(self):
        depart = E.rsn_depuis_position(E.Position.depart())
        a = lit("конь g1 f3", jeu="echecs", niveau=4, contexte=depart)
        b = lit("馬 g1 f3", jeu="echecs", niveau=4, contexte=depart)
        self.assertTrue(a.ok and b.ok)
        self.assertEqual(a.rsn.empreinte(), b.rsn.empreinte())


if __name__ == "__main__":
    unittest.main()
