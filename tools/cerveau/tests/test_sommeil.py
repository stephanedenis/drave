from __future__ import annotations

import unittest
from types import SimpleNamespace

from cerveau.sommeil import (Sommeil, _cle, experience_contexte,
                             experience_m8)


def _it(code, texte="x", paire="p", jeu="echecs"):
    return SimpleNamespace(code=code, texte=texte, paire=paire, jeu=jeu)


CODE_A = {"jeu": "echecs", "action": "deplacer", "de": 62, "vers": 45}
CODE_B = {"jeu": "echecs", "action": "deplacer", "de": 52, "vers": 36}
CODE_C = {"jeu": "dames", "action": "prendre", "chemin_0": 8, "chemin_1": 13}


class TestSommeil(unittest.TestCase):
    def test_consolider_et_evaluer(self):
        train = [_it(CODE_A, "Nf3"), _it(CODE_A, "g1f3"), _it(CODE_B, "e3")]
        s = Sommeil()
        protos = s.consolider(train)
        self.assertEqual(len(protos), 1)
        self.assertEqual(protos[("echecs", "deplacer")]["de"], 62)
        r = s.evaluer([_it(CODE_A), _it(CODE_B)], protos)
        self.assertEqual(r["n"], 2)
        self.assertGreater(r["champs"], 0.5)
        self.assertTrue(0.0 <= r["exact"] <= 1.0)

    def test_baselines(self):
        train = [_it(CODE_A, "a"), _it(CODE_A, "b"), _it(CODE_B, "c")]
        test = [_it(CODE_A, "d")]
        b = Sommeil().baselines(train, test)
        self.assertIn("global", b)
        self.assertIn("par_jeu", b)
        self.assertIn("par_groupe", b)
        self.assertIn("groupes_melanges", b)
        self.assertGreaterEqual(b["par_groupe"]["champs"], b["global"]["champs"])

    def test_hybride(self):
        train = [_it(CODE_A, "a"), _it(CODE_B, "b")]
        test = [_it(CODE_A, "c"), _it(CODE_C, "d")]
        s = Sommeil()
        protos = s.consolider(train)
        r = s.evaluer_hybride(test, protos, s.index_episodes(train))
        self.assertEqual(r["couverture"], 0.5)
        self.assertEqual(r["exact"], 0.5)
        self.assertEqual(r["exact_sur_couverts"], 1.0)

    def test_dedup(self):
        its = [_it(CODE_A, "a"), _it(CODE_A, "b"), _it(CODE_B, "c")]
        self.assertEqual(len(Sommeil.dedupliquer(its, "code")), 2)

    def test_experience_reelle(self):
        r = experience_m8()
        v = r["verdict"]
        self.assertTrue(v["champs_96_48_reproduit"])
        self.assertTrue(v["exact_annonce_0_est_faux"])
        self.assertGreater(v["exact_queue"], 0.6)
        self.assertTrue(all(x == 0.0 for x in v["exact_codes_nouveaux"]))
        self.assertEqual(r["queue"]["hybride"]["exact"], 1.0)
        self.assertGreater(v["champs_non_nuls"], 0.8)

    # ---- A7 : clés étendues, backoff, hybride honnête, code tenu à l'écart
    def test_cles_etendues(self):
        self.assertEqual(_cle(CODE_A, "type_seul"),
                         (("action", "de", "jeu", "vers"),))
        self.assertEqual(_cle(CODE_A, "jeu_type"),
                         ("echecs", ("action", "de", "jeu", "vers")))
        self.assertEqual(_cle(CODE_A, "action_type"),
                         ("deplacer", ("action", "de", "jeu", "vers")))
        self.assertEqual(_cle(CODE_C, "groupe"), ("dames", "prendre"))

    def test_backoff_champ_par_champ(self):
        train = [_it(CODE_A, "a"), _it(CODE_B, "b")]
        test = [_it(CODE_C, "c")]  # jeu absent du train : repli global
        s = Sommeil()
        pp = s.prototypes_multi(train)
        r = s.evaluer_profond(test, pp)
        self.assertEqual(r["exact"], 0.0)
        self.assertEqual(r["n"], 1)
        self.assertEqual(r["niveaux_utilises"].get("global", 0), 15)
        # support minimal : le groupe (2 épisodes) ne suffit plus
        r3 = s.evaluer_profond([_it(CODE_A)], pp, ladder=("type", "global"),
                               min_support=3)
        self.assertEqual(r3["niveaux_utilises"].get("type", 0), 0)

    def test_hybride_surface_honnete(self):
        train = [_it(CODE_A, "a", paire="pa"), _it(CODE_B, "b", paire="pb")]
        test = [_it(CODE_A, "a", paire="pa"), _it(CODE_C, "c", paire="pc")]
        s = Sommeil()
        pp = s.prototypes_multi(train)
        r = s.evaluer_hybride_surface(test, pp, s.index_surfaces(train))
        self.assertEqual(r["couverture"], 0.5)
        self.assertEqual(r["exact_sur_couverts"], 1.0)
        self.assertEqual(r["exact"], 0.5)
        # l'index par code cible est l'oracle tautologique, pas une surface
        oracle = s.evaluer_hybride(test, pp["groupe"][0],
                                   s.index_episodes(train))
        self.assertEqual(oracle["exact"], 0.5)

    def test_experience_contexte_negative(self):
        r = experience_contexte()
        v = r["verdict"]
        # exact nul par construction sur un code tenu à l'écart
        self.assertEqual(v["exact_loo"], 0.0)
        self.assertTrue(all(x == 0.0 for x in v["exact_codes_tenus"]))
        self.assertGreater(v["champs_loo"]["jeu"], v["champs_loo"]["global"])
        self.assertAlmostEqual(v["gain_groupe_sur_jeu_champs"], 0.0, places=12)
        self.assertFalse(v["conditionner_aide_valeurs"])
        # la queue publiée est intra-code : 106/106 codes vus dans le train
        q = v["queue_publiee"]
        self.assertEqual(q["codes_test_vus_dans_train"], q["n_test"])
        self.assertAlmostEqual(q["champs"], 0.9647798742138365, places=9)
        # et son exact dépasse le plafond contextuel du corpus
        self.assertLess(r["plafond_contextuel"]["groupe"]["masse_modale"],
                        q["exact"])
        # l'hybride par surface ne couvre aucun code tenu à l'écart
        self.assertEqual(v["hybride_surface_couverture"], 0.0)
        self.assertEqual(r["loo_codes"]["ladder"]["exact"], 0.0)


if __name__ == "__main__":
    unittest.main()
