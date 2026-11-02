"""Tests de la politique DRVM/native — le contrat sans modèle, puis le refus."""
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))
from tools.pensee.operateurs import (BUT_C, CADENAS, LABYRINTHE, LABYRINTHE_PORTE,  # noqa: E402
                                     L_BUT, P_BUT, PolitiqueLLM)


class TestPolitiqueLLM(unittest.TestCase):
    def test_cadenas(self):
        p = PolitiqueLLM("faux", jeu="cadenas", transport=lambda *_: "avant")
        self.assertEqual(p.propose(CADENAS.initial(), BUT_C), "avant")
        self.assertGreater(p.latence, 0.0)

    def test_cadenas_variantes(self):
        etat = CADENAS.initial()
        minimal = PolitiqueLLM("faux", jeu="cadenas", variante="minimal")
        regle = PolitiqueLLM("faux", jeu="cadenas", variante="regle")
        self.assertNotIn("augmente", minimal._invite(etat, BUT_C))
        self.assertIn("augmente", regle._invite(etat, BUT_C))

    def test_porte(self):
        p = PolitiqueLLM("faux", jeu="porte", transport=lambda *_: "bas")
        self.assertEqual(p.propose(LABYRINTHE_PORTE.initial(), P_BUT), "bas")
        invite = p._invite(LABYRINTHE_PORTE.initial(), P_BUT)
        self.assertIn("porte", invite.lower())
        self.assertIn("(3,2)", invite)

    def test_labyrinthe(self):
        p = PolitiqueLLM("faux", transport=lambda *_: "droite")
        self.assertEqual(p.propose(LABYRINTHE.initial(), L_BUT), "droite")

    def test_refus(self):
        p = PolitiqueLLM("faux", transport=lambda *_: "n'importe quoi")
        self.assertIsNone(p.propose(LABYRINTHE.initial(), L_BUT))
        self.assertEqual(p.erreurs, 1)

    def test_serveur_absent(self):
        def transport(*_):
            raise OSError("serveur absent")

        p = PolitiqueLLM("faux", transport=transport)
        self.assertIsNone(p.propose(LABYRINTHE.initial(), L_BUT))
        self.assertEqual(p.erreurs, 1)


if __name__ == "__main__":
    unittest.main()
