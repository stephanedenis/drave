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

    def test_porte_mobile(self):
        from tools.pensee.operateurs import _etat_pmob

        p = PolitiqueLLM("faux", jeu="porte_mobile", transport=lambda *_: "bas")
        etat = _etat_pmob(1, 2, False, 1)
        self.assertEqual(p.propose(etat, P_BUT), "bas")
        invite = p._invite(etat, P_BUT)
        self.assertIn("porte mobile", invite.lower())
        self.assertIn("(1,3)", invite)
        self.assertNotIn("(1,3),", invite)

    def test_porte_bouge(self):
        from tools.pensee.operateurs import _etat_pb

        p = PolitiqueLLM("faux", jeu="porte_bouge", transport=lambda *_: "bas")
        etat = _etat_pb(0, 0, False, 3)
        self.assertEqual(p.propose(etat, P_BUT), "bas")
        invite = p._invite(etat, P_BUT)
        self.assertIn("porte bouge", invite.lower())
        self.assertIn("(1,3)", invite)
        self.assertIn("phase", invite)

    def test_porte_sto(self):
        p = PolitiqueLLM("faux", jeu="porte_sto", transport=lambda *_: "bas")
        self.assertEqual(p.propose(LABYRINTHE_PORTE.initial(), P_BUT), "bas")
        invite = p._invite(LABYRINTHE_PORTE.initial(), P_BUT)
        self.assertIn("80 %", invite)
        self.assertIn("réessaie", invite)

    def test_porte_fenetre(self):
        from tools.pensee.operateurs import _etat_pw

        p = PolitiqueLLM("faux", jeu="porte_fenetre", transport=lambda *_: "bas")
        etat = _etat_pw(0, 0, 1)
        self.assertEqual(p.propose(etat, P_BUT), "bas")
        invite = p._invite(etat, P_BUT)
        self.assertIn("t % 3", invite)
        self.assertIn("attends", invite)

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
