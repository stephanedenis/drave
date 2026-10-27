from __future__ import annotations

import unittest

from cerveau.neuromodulation import (EpisodeM7, MemoireFrequence,
                                     MemoireLimitee, Neuromodulation,
                                     experience_m7, experience_m7_bis,
                                     preparer_flux)


def _episodes_synthetiques(n: int = 120) -> list[EpisodeM7]:
    out = []
    for i in range(n):
        jeu = ("echecs", "go", "dames")[i % 3]
        surface = f"{jeu} {i % 40}"
        code = {"jeu": jeu,
                "action": ("deplacer", "poser", "prendre")[i % 3],
                "case": i % 40}
        out.append(EpisodeM7(surface, code, jeu, 0.0, 0.0))
    return out


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


class TestMemoireFrequence(unittest.TestCase):
    def test_lfu_evince_le_moins_frequent(self):
        m = MemoireFrequence(2, politique="lfu")
        for s in ("a", "b", "a", "c"):
            m.stocker(s, {"jeu": s})
        self.assertTrue(m.contient("a"))
        self.assertFalse(m.contient("b"))
        self.assertTrue(m.contient("c"))

    def test_lfu_recence_departage(self):
        # a,b,b,a,c : à fréquence 2, le LFU évince a (arrivée plus ancienne),
        # le LFU+récence évince b (dernière écriture plus ancienne).
        for politique, garde, evince in (
                ("lfu", "b", "a"), ("lfu_recence", "a", "b")):
            m = MemoireFrequence(2, politique=politique)
            for s in ("a", "b", "b", "a", "c"):
                m.stocker(s, {"jeu": s})
            self.assertTrue(m.contient(garde))
            self.assertFalse(m.contient(evince))
            self.assertTrue(m.contient("c"))

    def test_contexte_alloue_au_contexte_frequent(self):
        m = MemoireFrequence(2, politique="contexte")
        for s, ctx in (("a", "A"), ("b", "B"), ("c", "A"), ("d", "A")):
            m.stocker(s, {"jeu": s}, contexte=ctx)
        self.assertFalse(m.contient("b"))
        self.assertTrue(m.contient("c"))
        self.assertTrue(m.contient("d"))

    def test_contexte_requis(self):
        m = MemoireFrequence(2, politique="contexte")
        with self.assertRaises(ValueError):
            m.stocker("a", {"jeu": "echecs"})

    def test_beta_zero_egal_lfu_recence(self):
        m0 = MemoireFrequence(4, politique="lfu_recence")
        m1 = MemoireFrequence(4, politique="lfu_contexte", beta=0.0)
        for i in range(40):
            s = f"s{i % 9}"
            m0.stocker(s, {"jeu": s})
            m1.stocker(s, {"jeu": s}, contexte=("jeu", i % 3))
        self.assertEqual(
            [(e["surface"], e["frequence"], e["t_dernier"])
             for e in m0.etat()],
            [(e["surface"], e["frequence"], e["t_dernier"])
             for e in m1.etat()])

    def test_experience_m7_bis(self):
        ep = _episodes_synthetiques()
        r = experience_m7_bis(ep, permutations=3, synthetique=False)
        self.assertEqual(r["protocole"]["n"], 120)
        self.assertEqual(r["protocole"]["prefixe"], 96)
        self.assertTrue(r["verdict"]["toutes_politiques_au_plafond_historique"])
        self.assertTrue(all(r["verdict"]["beta_zero_egal_lfu_recence"].values()))
        self.assertIn("contexte_jeu", r["verdict"]["contexte_bat_lfu"])
        self.assertIn("suf_surface",
                      r["verdict"]["lfu_recence_bat_lfu"]["surface"])
        self.assertIn("ret_nouveaux_suffixe", r["resultats"]["lfu"])
        self.assertIn("evictions", r["controles"])
        # reproductibilité à graine égale
        r2 = experience_m7_bis(ep, permutations=3, synthetique=False)
        self.assertEqual(r["resultats"], r2["resultats"])


if __name__ == "__main__":
    unittest.main()
