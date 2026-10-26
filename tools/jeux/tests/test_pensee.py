import random
import unittest

from jeux.mesure import _invariance_negative, _invariance_pensee, _mates_echecs
from jeux.pensee import Budget, decide, decide_cartes, decide_dames, decide_echecs
from jeux.regles import cartes as C
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M


class TestMorpionPensee(unittest.TestCase):
    def test_valeur_et_decision(self):
        d = decide(M.etat_initial())
        self.assertIsNotNone(d.coup)
        self.assertEqual(d.score, 0.0)
        self.assertTrue(d.coup.corps["case"] in range(9))

    def test_exact_ne_perd_pas(self):
        rng = random.Random(11)
        for _ in range(30):
            etat = M.etat_initial()
            while not M.terminal(etat):
                if M.trait(etat) == "X":
                    d = decide(etat)
                    c = d.coup.corps["case"]
                else:
                    c = rng.choice([x.corps["case"] for x in M.coups_legaux(etat)])
                etat = M.applique_indice(etat, c)
            self.assertNotEqual(M.resultat(etat), "O")


class TestEchecsPensee(unittest.TestCase):
    def test_mats_en_un(self):
        r = _mates_echecs()
        self.assertEqual(r["trouves"], r["total"], r)
        self.assertLessEqual(r["statiques"], r["total"])

    def test_decision_legale(self):
        etat = E.rsn_depuis_position(E.Position.depart())
        d = decide_echecs(etat, Budget(profondeur=2, temps_s=3))
        pos = E.position_depuis_rsn(etat)
        c = E.coup_depuis_action(d.coup, pos)
        self.assertIn(c, pos.coups_legaux())
        self.assertGreater(d.noeuds, 0)


class TestDamesPensee(unittest.TestCase):
    def test_decision_legale(self):
        pos = D.Position.depart()
        etat = D.rsn_depuis_position(pos)
        d = decide_dames(etat, Budget(profondeur=3, temps_s=3))
        c = D.coup_depuis_action(d.coup, pos)
        self.assertIn(c, pos.coups_legaux())

    def test_recherche_gagne_contre_sans_recherche(self):
        from jeux.pensee import coup_dames_sans_recherche
        gagnees = 0
        for graine in range(3):
            pos = D.Position.depart()
            for _ in range(60):
                if pos.terminal():
                    break
                if pos.trait == D.NOIR:
                    d = decide_dames(D.rsn_depuis_position(pos),
                                     Budget(profondeur=3, temps_s=2))
                    c = D.coup_depuis_action(d.coup, pos)
                else:
                    c = D.coup_depuis_action(
                        coup_dames_sans_recherche(D.rsn_depuis_position(pos)), pos)
                pos = pos.applique(c)
            def mat(coul):
                return sum(175 if p in (D.NOIR_DAME, D.BLANC_DAME) else 100
                           for p in pos.cases if p != D.VIDE and D._couleur(p) == coul)
            gagnees += 1 if mat(D.NOIR) > mat(D.BLANC) else 0
        self.assertGreaterEqual(gagnees, 2)


class TestGoPensee(unittest.TestCase):
    def test_mcts_legal(self):
        pos = G.Position.depart(5, 0)
        d = decide(pos.vers_rsn(), Budget(playouts=20, temps_s=10, graine=1))
        self.assertIsNotNone(d.coup)
        if d.coup.corps.get("passe"):
            self.assertTrue(pos.terminal() or not pos.coups_legaux())
        else:
            self.assertTrue(pos.coup_legal(int(d.coup.corps["point"])))


class TestCartesPensee(unittest.TestCase):
    def test_politique_legale_et_gagnante(self):
        gagnees = 0
        for graine in range(100):
            pos = C.Position.depart(graine)
            rng = random.Random(graine + 12345)
            while not pos.terminal():
                if pos.tour % 2 == 0:
                    c = pos.politique()
                    self.assertTrue(pos.coup_legal(c))
                else:
                    c = rng.choice(pos.coups_legaux())
                pos = pos.joue(c)
            gagnees += 1 if pos.plis[0] > pos.plis[1] else 0
        self.assertGreater(gagnees, 60)


class TestInvariancePensee(unittest.TestCase):
    def test_cinq_jeux_invariants(self):
        r = _invariance_pensee(__import__("jeux.corpus", fromlist=["construire_corpus"]).construire_corpus(),
                               rapide=True)
        self.assertEqual(r["identiques"], r["total"])

    def test_controle_negatif(self):
        r = _invariance_negative()
        self.assertEqual(r["differents"], r["total"])


if __name__ == "__main__":
    unittest.main()
