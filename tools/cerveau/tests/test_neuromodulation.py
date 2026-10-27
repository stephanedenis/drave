from __future__ import annotations

import unittest

from cerveau.neuromodulation import (MemoireLimitee, Neuromodulation,
                                     experience_m7, preparer_flux)


class TestNeuromodulation(unittest.TestCase):
    def test_fifo_evince_le_plus_ancien(self):
        m = MemoireLimitee(2, politique="fifo")
        for s in ("a", "b", "c"):
            m.stocker(s, {"surface": s})
        self.assertFalse(m.contient("a"))
        self.assertTrue(m.contient("b"))
        self.assertTrue(m.contient("c"))

    def test_gel_garde_les_premiers(self):
        m = MemoireLimitee(2, politique="gel")
        for s in ("a", "b", "c"):
            m.stocker(s, {"surface": s})
        self.assertTrue(m.contient("a"))
        self.assertTrue(m.contient("b"))
        self.assertFalse(m.contient("c"))

    def test_cle_code_dedouble(self):
        c1 = {"jeu": "echecs", "action": "deplacer", "de": 1, "vers": 2}
        c2 = {"jeu": "echecs", "action": "deplacer", "de": 1, "vers": 2}
        m = MemoireLimitee(4, politique="fifo", cle="code")
        m.stocker("A", c1)
        m.stocker("B", c2)
        self.assertEqual(len(m.episodes), 1)
        self.assertTrue(m.contient_code(c1))
        self.assertFalse(m.contient("A"))

    def test_capacite_zero(self):
        m = MemoireLimitee(0)
        m.stocker("a", {"jeu": "echecs"})
        self.assertEqual(m.episodes, [])

    def test_signaux(self):
        n = Neuromodulation()
        code = {"jeu": "echecs", "action": "deplacer", "de": 1, "vers": 2}
        s1 = n.signal(code, marge=0.5, recompense=1.0)
        s2 = n.signal(code, marge=0.5, recompense=1.0)
        self.assertEqual(s1["nouveaute"], 1.0)
        self.assertEqual(s2["nouveaute"], 0.0)
        self.assertAlmostEqual(s1["incertitude"], 0.5)
        self.assertGreater(s1["poids"], s2["poids"])

    def test_experience(self):
        ep = preparer_flux()
        r = experience_m7(ep, permutations=5, synthetique=False)
        plafond = r["protocole"]["plafonds"]
        self.assertAlmostEqual(plafond["surface_finale"], 16 / 439)
        self.assertAlmostEqual(plafond["code"], 16 / 29)
        self.assertTrue(r["verdict"]["plafond_surface_atteint_par_toutes"])
        self.assertTrue(r["verdict"]["gel_egal_fifo_sur_la_metrique_historique"])
        # la nouveauté par surface ne bat pas FIFO sur les répétés
        d = r["deltas_vs_fifo"]["nouveaute"]
        self.assertLess(d["rep_surface"]["moyenne"], 0)
        # la clé code, elle, améliore le suffixe
        self.assertGreater(r["deltas_vs_fifo"]["fifo_code"]["suf_code"]["moyenne"], 0)
        # contrôle nul : FIFO contre lui-même
        for m, v in r["controles"]["fifo_contre_lui_meme"].items():
            self.assertEqual(v["moyenne"], 0.0)


if __name__ == "__main__":
    unittest.main()
