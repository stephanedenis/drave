"""Tests des principes des maîtres : ils sont encodés, licites et mesurables."""
from __future__ import annotations

import unittest

from jeux.codecs import lit
from jeux.maitres import (LIVRE, PARTIES, cle_livre, eval_dames_maitres,
                          eval_echecs_maitres, politique_cartes_maitres,
                          prior_go)
from jeux.pensee import Budget, decide_echecs
from jeux.regles import cartes as C
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G


class TestMaitres(unittest.TestCase):
    def test_livre(self):
        self.assertGreaterEqual(len(LIVRE), 20)
        start = cle_livre(E.Position.depart())
        self.assertIn("e2e4", LIVRE[start])
        pos = E.Position.depart()
        suivis = 0
        for _ in range(4):
            d = decide_echecs(E.rsn_depuis_position(pos), Budget(livre=True))
            self.assertIsNotNone(d.coup)
            c = E.coup_depuis_action(d.coup)
            self.assertIn(c.uci(), LIVRE.get(cle_livre(pos), []))
            pos.joue(c)
            suivis += 1
        self.assertEqual(suivis, 4)

    def test_premier_coup_de_maitre(self):
        depart = E.rsn_depuis_position(E.Position.depart())
        d = decide_echecs(depart, Budget(profondeur=3, temps_s=3, maitres=True))
        self.assertIsNotNone(d.coup)
        self.assertIn(E.coup_depuis_action(d.coup).uci(),
                      {"e2e4", "d2d4", "g1f3", "c2c4"})

    def test_parties_de_maitres_valides(self):
        for p in PARTIES:
            lec = lit(p["pgn"], jeu="echecs", niveau=4)
            self.assertTrue(lec.ok, (p["nom"], lec.erreurs))
            pos, _ = E.partie_depuis_rsn(lec.rsn)
            self.assertFalse(pos.coups_legaux())
            self.assertTrue(pos.en_echec(pos.trait))

    def test_evaluations_finies(self):
        self.assertIsInstance(eval_echecs_maitres(E.Position.depart()), float)
        self.assertIsInstance(eval_dames_maitres(D.Position.depart()), float)

    def test_prior_go(self):
        # sur 9×9, un point de 3e/4e ligne a un prior plus grand que le centre
        pos = G.Position.depart(9, 0)
        self.assertGreater(prior_go(pos, 2 + 9 * 2), prior_go(pos, 4 + 9 * 4))
        # capture : le coup qui prend une pierre en atari a le prior le plus haut
        plateau = [G.VIDE] * 25
        plateau[0] = G.NOIR
        plateau[1] = G.BLANC
        plateau[6] = G.NOIR
        p = G.Position(5, plateau, G.NOIR)
        self.assertGreater(prior_go(p, 2), prior_go(p, 20))

    def test_politique_cartes(self):
        pos = C.Position.depart(0)
        c = politique_cartes_maitres(pos)
        self.assertIn(c, pos.coups_legaux())


if __name__ == "__main__":
    unittest.main()
