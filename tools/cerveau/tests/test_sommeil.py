from __future__ import annotations

import unittest
from types import SimpleNamespace

from cerveau.sommeil import Sommeil, experience_m8


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


if __name__ == "__main__":
    unittest.main()
