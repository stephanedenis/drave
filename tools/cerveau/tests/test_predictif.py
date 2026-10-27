from __future__ import annotations

import unittest

from cerveau.predictif import (Predictif, baseline_tour, controle_negatif,
                               permuter, valeur)
from cerveau.sequences import Pas, Sequence, corpus


def _pas(jeu: str, action: str = "deplacer", source=None, cible=None,
         champ_cible: str | None = None) -> Pas:
    code = {"jeu": jeu, "action": action}
    if source is not None:
        code["de" if jeu == "echecs" else "chemin_0"] = source
    if cible is not None:
        if champ_cible is None:
            champ_cible = {"echecs": "vers", "dames": "chemin_1",
                           "go": "point", "morpion": "case"}[jeu]
        code[champ_cible] = cible
    return Pas(jeu, code, "", "", None)


def _sequence(jeu: str, pas) -> Sequence:
    return Sequence(jeu, tuple(pas))


class TestCibles(unittest.TestCase):
    def test_source_et_cible(self):
        self.assertEqual(valeur(_pas("echecs", source=62, cible=45), "source"), 62)
        self.assertEqual(valeur(_pas("echecs", source=62, cible=45), "cible"), 45)
        dames = _pas("dames", source=8, cible=17, champ_cible="chemin_1")
        self.assertEqual(valeur(dames, "source"), 8)
        self.assertEqual(valeur(dames, "cible"), 17)

    def test_cible_dames_dernier_chemin(self):
        code = {"jeu": "dames", "action": "prendre", "chemin_0": 8,
                "chemin_1": 17, "chemin_2": 26}
        pas = Pas("dames", code, "", "", None)
        self.assertEqual(valeur(pas, "cible"), 26)
        code2 = {"jeu": "dames", "action": "prendre", "chemin_0": 8,
                 "chemin_1": 17, "chemin_2": None}
        self.assertEqual(valeur(Pas("dames", code2, "", "", None), "cible"), 17)

    def test_source_absente(self):
        self.assertIsNone(valeur(_pas("go", cible=48), "source"))
        self.assertEqual(valeur(_pas("go", cible=48), "cible"), 48)
        self.assertEqual(valeur(_pas("morpion", cible=4), "cible"), 4)
        self.assertEqual(valeur(_pas("go", action="passer"), "cible"), None)

    def test_cible_inconnue(self):
        with self.assertRaises(ValueError):
            valeur(_pas("echecs", source=1), "autre")


class TestPredictif(unittest.TestCase):
    def test_action_constante_aucun_gain(self):
        # cible constante : le modèle ne peut pas battre la majorité
        seqs = [_sequence("echecs", [_pas("echecs", source=i, cible=i + 1)
                                     for i in range(8)]) for _ in range(4)]
        for ordre in (0, 1, 2):
            m = Predictif("action", ordre)
            m.entrainer(seqs)
            r = m.evaluer(seqs)
            self.assertEqual(r["n"], 4 * 7)
            self.assertAlmostEqual(r["exact"], 1.0)
            self.assertAlmostEqual(r["majoritaire"], 1.0)
            self.assertAlmostEqual(r["gain"], 0.0)

    def test_structure_alternee_gain(self):
        # une source qui alterne 8/24 : l'ordre 1 la prédit, la majorité non
        seqs = [_sequence("dames", [_pas("dames", source=(8 if i % 2 == 0 else 24))
                                    for i in range(12)]) for _ in range(6)]
        m1 = Predictif("source", 1)
        m1.entrainer(seqs)
        r1 = m1.evaluer(seqs)
        self.assertAlmostEqual(r1["exact"], 1.0)
        self.assertAlmostEqual(r1["majoritaire"], 6 / 11)
        self.assertGreater(r1["gain"], 0.4)
        t = baseline_tour(seqs, seqs, "source")
        self.assertAlmostEqual(t["exact"], 1.0)

    def test_ordre_2_ne_change_rien_sur_constante(self):
        seqs = [_sequence("morpion", [_pas("morpion", action="jouer_case",
                                            cible=i % 9) for i in range(9)])
                for _ in range(3)]
        r1 = Predictif("action", 1); r1.entrainer(seqs); a = r1.evaluer(seqs)
        r2 = Predictif("action", 2); r2.entrainer(seqs); b = r2.evaluer(seqs)
        self.assertEqual(a["exact"], b["exact"])
        self.assertEqual(a["n"], b["n"])

    def test_cles_historiques(self):
        m = Predictif("action")
        m.entrainer([_sequence("echecs", [_pas("echecs") for _ in range(5)])])
        r = m.evaluer([_sequence("echecs", [_pas("echecs") for _ in range(5)])])
        for cle in ("exact", "majoritaire", "surprise", "n"):
            self.assertIn(cle, r)

    def test_permutation_conserve_la_marginale(self):
        seqs = [_sequence("echecs", [_pas("echecs", source=i, cible=i + 1)
                                     for i in range(6)]) for _ in range(3)]
        melange = permuter(seqs, "source", graine=1)
        avant = sorted(valeur(p, "source") for s in seqs for p in s.pas)
        apres = sorted(valeur(p, "source") for s in melange for p in s.pas)
        self.assertEqual(avant, apres)

    def test_controle_negatif_tue_le_gain(self):
        seqs = [_sequence("dames", [_pas("dames", source=(8 if i % 2 == 0 else 24))
                                    for i in range(12)]) for _ in range(6)]
        c = controle_negatif(seqs[:4], seqs[4:], "source", 1,
                             permutations=5, graine=0)
        self.assertGreater(c["gain_observe"], 0.4)
        self.assertLess(abs(c["gain_null_moyen"]), 0.15)
        self.assertLessEqual(c["p_value_gain"], 0.2)

    def test_corpus_action_quasi_constante(self):
        diag = Predictif().diagnostic(corpus(0, 4, 6), cibles=("action",))
        for jeu, stats in diag["action"].items():
            self.assertLessEqual(stats["distincts"], 2, jeu)
        self.assertEqual(diag["action"]["echecs"]["entropie"], 0.0)
        self.assertEqual(diag["action"]["dames"]["entropie"], 0.0)


if __name__ == "__main__":
    unittest.main()
