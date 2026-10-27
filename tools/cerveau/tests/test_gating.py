from __future__ import annotations

import unittest

from cerveau.gating import CONDITIONS, TACHES, Porte


class TestTacheConflit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.porte = Porte()
        cls.essais = cls.porte.tache_conflit()

    def test_taille_et_equilibre(self):
        self.assertEqual(len(self.essais), 88)
        for condition in CONDITIONS:
            n = sum(1 for e in self.essais if e.condition == condition)
            self.assertEqual(n, 22)
        # les blocs de 4 essais partagent la même langue cible
        for i in range(0, len(self.essais), 4):
            bloc = self.essais[i:i + 4]
            self.assertEqual(len({e.cible_langue for e in bloc}), 1)

    def test_conditions(self):
        for e in self.essais:
            if e.condition == "go":
                self.assertEqual(e.langue_vraie, e.cible_langue)
                self.assertEqual(e.code_vrai, e.cible_code)
            elif e.condition == "traduction":
                self.assertEqual(e.code_vrai, e.cible_code)
                self.assertNotEqual(e.langue_vraie, e.cible_langue)
            elif e.condition == "langue":
                self.assertEqual(e.langue_vraie, e.cible_langue)
                self.assertNotEqual(e.code_vrai, e.cible_code)
            else:  # ni
                self.assertNotEqual(e.langue_vraie, e.cible_langue)
                self.assertNotEqual(e.code_vrai, e.cible_code)

    def test_langue_deterministe(self):
        # le canal MULTI global dépend de PYTHONHASHSEED ; la porte, non.
        for texte in ("go D4", "tic-tac-toe A1", "pion e2 e4", "knight g1 f3"):
            self.assertEqual(Porte().langue(texte), self.porte.langue(texte))
        self.assertEqual(self.porte.langue("pion e2 e4"), "fr")
        self.assertEqual(self.porte.langue("knight g1 f3"), "en")

    def test_surfaces_ambigues(self):
        canaux = self.porte._canal_diagnostic(self.essais)
        self.assertEqual(canaux["surfaces_ambigues"], ["go D4", "tic-tac-toe A1"])
        self.assertEqual(canaux["lecture_exact"], 1.0)
        self.assertEqual(canaux["lecture_n"], 20)  # 22 couples, 20 textes distincts

    def test_executer(self):
        r = self.porte.executer()
        self.assertEqual(r["n"], 88)
        self.assertAlmostEqual(r["exact"], 83 / 88, places=6)
        self.assertEqual(r["faux_positifs"], 0)
        self.assertEqual(r["faux_negatifs"], 5)
        self.assertAlmostEqual(r["exactitude_equilibree"], (17 / 22 + 1.0) / 2, places=6)
        self.assertAlmostEqual(r["taux_base_tout_non"], 0.75)
        # aucune mémoire : coût de commutation apparié nul...
        self.assertAlmostEqual(r["cout_commutation"], 0.0)
        # ...mais l'instrument le détecte quand on simule une persévération
        self.assertGreater(r["controle_perseveration"], 0.3)

    def test_politiques_simples_au_taux_de_base(self):
        r = self.porte.executer()
        for nom in ("langue", "sens", "tout_non"):
            self.assertAlmostEqual(r["politiques"][nom]["exact"], 0.75, places=6)
        self.assertGreater(r["politiques"]["langue"]["faux_positifs"], 0)
        self.assertGreater(r["politiques"]["sens"]["faux_positifs"], 0)

    def test_compatibilite_typed_corpus(self):
        from semantique.typed_corpus import items
        its = [i for i in items() if i.langue in ("fr", "en")]
        r = self.porte.executer(its, ("fr", "en"))
        self.assertEqual(r["n"], 88)
        self.assertAlmostEqual(r["exact"], 83 / 88, places=6)


class TestTacheSwitch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.porte = Porte()
        cls.essais = cls.porte.tache_switch()
        cls.resultat = cls.porte.executer_switch()

    def test_taille_et_equilibre(self):
        self.assertEqual(len(self.essais), 792)
        self.assertEqual(sum(1 for e in self.essais if e.tache == "sens"), 440)
        self.assertEqual(sum(1 for e in self.essais if e.tache == "langue"), 352)
        self.assertEqual(sum(1 for e in self.essais if e.condition == "congruent"), 396)
        self.assertEqual(sum(1 for e in self.essais if e.condition == "incongruent"), 396)
        self.assertEqual(sum(1 for e in self.essais if e.transition == "commutation"), 352)
        self.assertEqual(sum(1 for e in self.essais if e.transition == "repetition"), 352)
        self.assertEqual(sum(1 for e in self.essais if e.transition == "initiale"), 88)
        # 4 commutations et 4 répétitions par groupe, à sondes appariées
        for debut in range(0, len(self.essais), 36):
            groupe = self.essais[debut:debut + 36]
            self.assertEqual(len(groupe), 36)
            for b in range(0, 36, 4):
                bloc = groupe[b:b + 4]
                self.assertEqual(len({e.tache for e in bloc}), 1)
                if b:
                    prec = groupe[b - 4].tache
                    attendu = "commutation" if bloc[0].tache != prec else "repetition"
                    self.assertEqual(bloc[0].transition, attendu)
                else:
                    self.assertEqual(bloc[0].transition, "initiale")

    def test_conditions_et_consignes(self):
        for e in self.essais:
            self.assertIn(e.tache, TACHES)
            self.assertEqual(e.reponse_sens, e.code_vrai == e.cible_code)
            self.assertEqual(e.reponse_langue, e.langue_vraie == e.cible_langue)
            self.assertEqual(e.condition,
                             "congruent" if e.reponse_sens == e.reponse_langue
                             else "incongruent")
            self.assertEqual(e.attendu,
                             e.reponse_sens if e.tache == "sens" else e.reponse_langue)

    def test_porte_dure_sans_cout_executif(self):
        r = self.resultat
        self.assertEqual(r["n"], 792)
        self.assertAlmostEqual(r["exact"], 752 / 792, places=6)
        self.assertAlmostEqual(r["taux_base_tout_non"], 0.5)
        # la consigne sélectionne le canal : ni conflit ni commutation
        self.assertAlmostEqual(r["effet_conflit"], 0.0)
        self.assertAlmostEqual(r["effet_commutation"], 0.0)
        self.assertAlmostEqual(r["effet_commutation_congruent"], 0.0)
        self.assertAlmostEqual(r["effet_commutation_incongruent"], 0.0)
        self.assertAlmostEqual(r["par_tache"]["sens"]["exact"], 1.0)
        self.assertLess(r["par_tache"]["langue"]["exact"], 1.0)

    def test_controle_positif_de_perseveration(self):
        c = self.resultat["controles"]["perseveration_tache"]
        self.assertLess(c["effet_commutation"], -0.4)
        self.assertAlmostEqual(c["effet_commutation_congruent"], 0.0)
        self.assertLess(c["effet_commutation_incongruent"], -0.8)
        self.assertLess(c["interaction_conflit_commutation"], -0.8)

    def test_politiques_temoins(self):
        p = self.resultat["politiques"]
        self.assertAlmostEqual(p["tout_non"]["exact"], 0.5)
        self.assertAlmostEqual(p["tache_inversee"]["exact"], 0.5)
        # la consigne vaut mieux que le meilleur canal seul ou un indice au hasard
        self.assertGreater(self.resultat["exact"], p["sens"]["exact"])
        self.assertGreater(self.resultat["exact"], p["langue"]["exact"])
        self.assertGreater(self.resultat["exact"], p["indice_aleatoire"]["exact"])
        self.assertAlmostEqual(p["sens"]["effet_commutation"], 0.0)

    def test_compatibilite_typed_corpus(self):
        from semantique.typed_corpus import items
        its = [i for i in items() if i.langue in ("fr", "en")]
        r = self.porte.executer_switch(its, ("fr", "en"))
        self.assertEqual(r["n"], 792)
        self.assertAlmostEqual(r["exact"], self.resultat["exact"], places=6)


if __name__ == "__main__":
    unittest.main()
