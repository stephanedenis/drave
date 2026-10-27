from __future__ import annotations

import json
import unittest

from cerveau import multilingue as ML


class TestMultilingue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = ML.mesurer()

    # -- corpus réel -----------------------------------------------------
    def test_sources_et_perimetre(self):
        meta = self.r["meta"]
        self.assertEqual(meta["items"], 528)
        self.assertEqual(meta["sources"]["B5"]["coups"], 79)
        self.assertEqual(meta["sources"]["B7"]["items_total"], 449)
        self.assertEqual(meta["sources"]["B7"]["coups"], 449)
        self.assertEqual(meta["sources"]["typed_corpus"]["items"], 528)
        self.assertTrue(meta["sources"]["typed_corpus"]["cles_identiques"])
        self.assertEqual(meta["sources"]["typed_corpus"]["codes_identiques"], 528)
        self.assertEqual(meta["langues_lexique"], 71)
        self.assertEqual(meta["langues_corpus"], 66)
        self.assertEqual(meta["langues_absentes_du_corpus"],
                         ["ky", "lo", "mt", "si", "yo"])

    def test_aucune_langue_inventee(self):
        meta = self.r["meta"]
        # On relit la source du lexique : les langues du corpus doivent en
        # venir, et les langues déclarées absentes ne doivent pas y figurer.
        from jeux.lexique_multilingue import MULTI
        corpus = set(self.r["global"]["langues"])
        absentes = set(meta["langues_absentes_du_corpus"])
        self.assertTrue(corpus <= set(MULTI.langues))
        self.assertTrue(absentes <= set(MULTI.langues))
        self.assertFalse(absentes & corpus)
        self.assertEqual(len(corpus), meta["langues_corpus"])

    def test_langues_n1(self):
        self.assertEqual(self.r["meta"]["langues_n1"],
                         ["am", "km", "pa", "so", "zu"])
        for langue in self.r["meta"]["langues_n1"]:
            self.assertEqual(self.r["par_langue"][langue]["n"], 1)

    # -- M1 global -------------------------------------------------------
    def test_m1_global(self):
        g = self.r["global"]
        self.assertEqual(g["n"], 528)
        self.assertEqual(g["exact_contexte"], {"ok": 528, "n": 528, "taux": 1.0})
        self.assertEqual(g["exact_sans_contexte"], {"ok": 374, "n": 528,
                                                    "taux": 0.708333})
        self.assertEqual(g["canonique"], {"ok": 528, "n": 528, "taux": 1.0})

    def test_B7_est_le_corpus_multilingue(self):
        b7 = self.r["par_source"]["B7"]
        self.assertEqual(b7["n"], 449)
        self.assertEqual(b7["exact_contexte"], {"ok": 449, "n": 449, "taux": 1.0})
        self.assertEqual(b7["exact_sans_contexte"], {"ok": 331, "n": 449,
                                                     "taux": 0.737194})
        self.assertEqual(b7["canonique"], {"ok": 449, "n": 449, "taux": 1.0})
        self.assertEqual(b7["invariance_interlangues"]["n"], 11)
        self.assertEqual(b7["invariance_interlangues"]["invariantes_contexte"], 11)
        self.assertEqual(b7["invariance_interlangues"]["invariantes_sans_contexte"], 11)

    def test_par_langue(self):
        langues = self.r["par_langue"]
        self.assertEqual(len(langues), 67)  # 66 langues + notation
        self.assertIn("notation", langues)
        for langue, ligne in langues.items():
            self.assertGreaterEqual(ligne["n"], 1)
            self.assertEqual(ligne["exact_contexte"]["taux"], 1.0)
            self.assertEqual(ligne["canonique"]["taux"], 1.0)
            if langue == "notation":
                self.assertEqual(ligne["invariance_interlangues"]["n"], 0)
            else:
                self.assertGreater(ligne["invariance_interlangues"]["n"], 0)
        self.assertEqual(langues["de"]["n"], 11)
        self.assertEqual(langues["de"]["exact_sans_contexte"],
                         {"ok": 8, "n": 11, "taux": 0.727273})
        self.assertEqual(langues["fr"]["n"], 55)

    def test_par_langue_jeu_croise(self):
        croise = self.r["par_langue_jeu"]
        self.assertEqual(croise["de"]["go"]["n"], 2)
        self.assertEqual(croise["de"]["cartes"]["n"], 5)
        self.assertEqual(croise["de"]["go"]["exact_sans_contexte"]["taux"], 0.0)
        self.assertEqual(croise["de"]["cartes"]["exact_sans_contexte"]["taux"], 1.0)

    def test_par_jeu(self):
        jeux = self.r["par_jeu"]
        self.assertEqual(list(jeux), list(ML.JEUX))
        self.assertEqual(sum(v["n"] for v in jeux.values()), 528)
        self.assertEqual(jeux["go"]["exact_sans_contexte"]["ok"], 0)
        self.assertEqual(jeux["morpion"]["exact_sans_contexte"]["ok"], 5)
        self.assertEqual(jeux["dames"]["exact_sans_contexte"]["ok"], 70)
        self.assertEqual(jeux["cartes"]["exact_sans_contexte"]["ok"], 161)
        self.assertEqual(jeux["echecs"]["exact_sans_contexte"]["ok"], 138)

    # -- invariance ------------------------------------------------------
    def test_invariance_interlangues(self):
        inv = self.r["global"]["invariance_interlangues"]
        self.assertEqual(inv["n"], 15)
        self.assertEqual(inv["invariantes_contexte"], 15)
        self.assertEqual(inv["invariantes_sans_contexte"], 14)
        b5 = self.r["par_source"]["B5"]["invariance_interlangues"]
        b7 = self.r["par_source"]["B7"]["invariance_interlangues"]
        self.assertEqual((b5["n"], b5["invariantes_contexte"],
                          b5["invariantes_sans_contexte"]), (4, 4, 3))
        self.assertEqual((b7["n"], b7["invariantes_contexte"],
                          b7["invariantes_sans_contexte"]), (11, 11, 11))

    def test_invariance_paire_par_paire(self):
        paires = self.r["paires"]
        self.assertFalse(paires["echecs-nf3"]["invariante_interlangues_sans_contexte"])
        self.assertTrue(paires["echecs-nf3"]["invariante_interlangues_contexte"])
        self.assertEqual(paires["echecs-nf3"]["codes_distincts_sans_contexte"], 2)
        self.assertTrue(paires["ml-go-d4"]["invariante_interlangues_sans_contexte"])
        self.assertEqual(paires["ml-go-d4"]["exact_sans_contexte"]["taux"], 0.0)
        self.assertEqual(paires["ml-morpion-a1"]["exact_sans_contexte"]["taux"], 0.0)
        self.assertEqual(paires["ml-echecs-e4"]["n"], 61)
        self.assertEqual(paires["ml-cartes-10h"]["n_langues"], 36)

    def test_invariance_toutes_variantes(self):
        inv = self.r["global"]["invariance_toutes_variantes"]
        self.assertEqual(inv["n"], 26)
        self.assertEqual(inv["invariantes_contexte"], 26)
        self.assertEqual(inv["invariantes_sans_contexte"], 21)

    # -- baseline --------------------------------------------------------
    def test_baseline_surface(self):
        b = self.r["global"]["baseline_surface"]
        self.assertEqual(b["n_applicable"], 514)
        self.assertEqual(b["exact_contexte"], {"ok": 514, "n": 514, "taux": 1.0})
        self.assertEqual(b["exact_sans_contexte"], {"ok": 369, "n": 514,
                                                    "taux": 0.717899})
        self.assertEqual(b["m1_sur_applicables"]["exact_sans_contexte"],
                         {"ok": 368, "n": 514, "taux": 0.715953})
        self.assertAlmostEqual(b["delta_sans_contexte"], 1 / 514, places=5)
        self.assertLess(self.r["par_jeu"]["morpion"]["baseline_surface"]
                        ["delta_sans_contexte"], 0)
        self.assertGreater(self.r["par_jeu"]["echecs"]["baseline_surface"]
                           ["delta_sans_contexte"], 0)
        self.assertEqual(self.r["par_jeu"]["go"]["baseline_surface"]
                         ["exact_sans_contexte"]["taux"], 0.0)

    def test_baseline_exclut_les_paires_uniques_et_sans_paire(self):
        b = self.r["global"]["baseline_surface"]
        self.assertEqual(b["n_items"], 528)
        self.assertEqual(b["n_applicable"], 514)
        self.assertEqual(528 - 514, 14)  # 10 sans paire + 4 paires à 1 variante
        self.assertEqual(self.r["meta"]["items_sans_paire"], 10)

    # -- contrôle permuté ------------------------------------------------
    def test_controle_surface_permutee(self):
        c = self.r["controle_surface_permutee"]
        strict = c["strict"]["global"]
        self.assertEqual(strict["n"], 369)
        self.assertEqual(strict["exact_attendu_contexte"],
                         {"ok": 0, "n": 369, "taux": 0.0})
        self.assertEqual(strict["exact_donateur_contexte"],
                         {"ok": 332, "n": 369, "taux": 0.899729})
        self.assertEqual(strict["exact_donateur_sans_contexte"],
                         {"ok": 313, "n": 369, "taux": 0.848238})
        b7 = c["strict"]["par_source"]["B7"]
        self.assertEqual(b7["exact_donateur_contexte"],
                         {"ok": 298, "n": 300, "taux": 0.993333})
        large = c["large"]["global"]
        self.assertEqual(large["n"], 518)
        self.assertEqual(large["exact_donateur_contexte"],
                         {"ok": 423, "n": 518, "taux": 0.816602})

    def test_permutation_deterministe_et_valide(self):
        records = [
            {"jeu": "x", "langue": "l", "paire": f"p{i}",
             "attendu": {"i": i}}
            for i in range(6)
        ]
        a = ML._permutation(records, lambda r: (r["jeu"], r["langue"]),
                            ML.GRAINE_CONTROLE)
        b = ML._permutation(records, lambda r: (r["jeu"], r["langue"]),
                            ML.GRAINE_CONTROLE)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 6)
        for i, j in a.items():
            self.assertNotEqual(i, j)
            self.assertNotEqual(records[i]["paire"], records[j]["paire"])
            self.assertNotEqual(records[i]["attendu"], records[j]["attendu"])

    def test_permutation_ne_prend_pas_un_meme_sens(self):
        records = [
            {"jeu": "x", "langue": "l", "paire": "p1", "attendu": {"i": 1}},
            {"jeu": "x", "langue": "l", "paire": "p1", "attendu": {"i": 1}},
            {"jeu": "x", "langue": "l", "paire": "p1", "attendu": {"i": 1}},
        ]
        mapping = ML._permutation(records, lambda r: (r["jeu"], r["langue"]), 7)
        self.assertEqual(mapping, {})

    # -- restitution -----------------------------------------------------
    def test_json_serialisable(self):
        texte = json.dumps(self.r, ensure_ascii=False, allow_nan=False)
        self.assertIn("invariance_interlangues", texte)
        self.assertIn("controle_surface_permutee", texte)
        self.assertNotIn("NaN", texte)
        self.assertNotIn("Infinity", texte)

    def test_markdown(self):
        md = ML.rendre_markdown(self.r)
        self.assertIn("# A10 — M1 (hub typé) sur le corpus multilingue", md)
        self.assertIn("## 6. Par langue", md)
        self.assertIn("## 7. Invariance interlangues, paire par paire", md)
        self.assertIn("ky, lo, mt, si, yo", md)
        self.assertIn("B7", md)
        self.assertIn("99,3 %", md)
        self.assertIn("`Cf3`", md)

    def test_autocritique_presente(self):
        phrases = self.r["autocritique"]
        self.assertGreaterEqual(len(phrases), 5)
        self.assertTrue(any("gold standard" in p for p in phrases))
        self.assertTrue(any("Invariance n'est pas exactitude" in p for p in phrases))

    def test_duree_cpu(self):
        self.assertLess(self.r["duree_s"], 60.0)


if __name__ == "__main__":
    unittest.main()
