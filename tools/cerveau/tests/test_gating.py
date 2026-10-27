from __future__ import annotations

import unittest

from cerveau.gating import CONDITIONS, Porte


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


if __name__ == "__main__":
    unittest.main()
