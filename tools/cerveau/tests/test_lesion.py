from __future__ import annotations

import json
import unittest

from cerveau.lesion import batterie_lesions


class TestLesion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = batterie_lesions(rapide=True)

    def test_structure(self):
        for m in ("M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"):
            self.assertIn(m, self.r["modules"])
            for k in ("lesion", "intacte", "lessee", "deficit", "n", "statut"):
                self.assertIn(k, self.r["modules"][m])

    def test_sham(self):
        for m, v in self.r["controles"]["sham"].items():
            self.assertAlmostEqual(v, 0.0, places=12)

    def test_m1_contexte(self):
        d = self.r["modules"]["M1"]["deficit"]["exact"]
        self.assertGreater(d, 0.25)
        self.assertLess(d, 0.35)

    def test_m2_double_dissociation(self):
        m2 = self.r["modules"]["M2"]
        self.assertTrue(m2["deficit"]["double_dissociation"])
        self.assertGreater(m2["deficit"]["action"], 0.3)
        self.assertGreater(m2["deficit"]["de_non_nul"], 0.3)

    def test_m2_mode_et_preservation(self):
        m2 = self.r["modules"]["M2"]
        self.assertIn(m2["mode"], ("voies", "proxy"))
        self.assertEqual(self.r["protocole"]["m2_mode"], m2["mode"])
        self.assertTrue(m2["statut"])
        p = m2["deficit"]["preservation"]
        self.assertAlmostEqual(p["de_sous_lesion_ventrale"],
                               m2["intacte"]["de"], places=12)
        self.assertAlmostEqual(p["action_sous_lesion_dorsale"],
                               m2["intacte"]["action"], places=12)
        if m2["mode"] == "voies":
            self.assertGreater(m2["intacte"]["de"], 0.8)
            self.assertGreater(m2["deficit"]["de"], 0.5)

    def test_m3_tampon(self):
        m3 = self.r["modules"]["M3"]
        self.assertEqual(m3["intacte"]["span"], 12)
        self.assertEqual(m3["lessee"]["span"], 0)
        self.assertEqual(m3["deficit"]["span"], 1.0)
        self.assertEqual(m3["intacte"]["nback2_controle"], 1.0)

    def test_m4_stockage(self):
        m4 = self.r["modules"]["M4"]
        self.assertEqual(m4["intacte"]["rappel"], 1.0)
        self.assertEqual(m4["lessee"]["rappel"], 0.0)
        self.assertEqual(m4["deficit"]["rappel"], 1.0)
        self.assertGreater(m4["deficit"]["completion"], 0.9)
        for nom, d in m4["deficit"]["par_champ"].items():
            self.assertEqual(d["intacte"], 1.0)
            self.assertAlmostEqual(d["deficit"],
                                   d["intacte"] - d["rappel_lese"], places=12)

    def test_m5_transitions(self):
        m5 = self.r["modules"]["M5"]
        self.assertGreater(m5["deficit"]["controle_positif_deficit"], 0.5)
        self.assertEqual(m5["deficit"]["sans_ordre2"], 0.0)
        self.assertLess(m5["deficit"]["exact"], 0.10)

    def test_m6_porte(self):
        m6 = self.r["modules"]["M6"]
        self.assertGreater(m6["deficit"]["canal_langue"], 0.15)
        self.assertGreater(m6["deficit"]["tout_accepter"], 0.6)

    def test_m7_modulation(self):
        m7 = self.r["modules"]["M7"]
        self.assertLess(m7["deficit"]["signal_sur_cle_code"], 0)
        self.assertGreater(m7["deficit"]["cle_code_sans_signal"], 0)
        self.assertLess(m7["deficit"]["surface_vs_fifo"]["rep_surface"], 0)

    def test_m8_sommeil(self):
        m8 = self.r["modules"]["M8"]
        self.assertEqual(m8["intacte"]["exact"], 0.0)
        self.assertGreater(m8["deficit"]["champs"], 0.10)
        self.assertGreater(m8["deficit"]["champs_non_nuls"], 0.4)
        self.assertTrue(all(x == 0.0
                            for x in m8["deficit"]["exact_codes_nouveaux"]))
        self.assertEqual(m8["intacte"]["hybride_exact_queue"], 1.0)
        self.assertEqual(m8["intacte"]["hybride_couverture_queue"], 1.0)
        self.assertEqual(
            m8["intacte"]["hybride_surface_couverture_codes_tenus"], 0.0)
        self.assertEqual(m8["intacte"]["queue_codes_vus"], 106)
        self.assertLess(m8["deficit"]["plafond_contextuel_groupe"],
                        m8["intacte"]["queue_exact"])

    def test_deficits_intacte_moins_lesee(self):
        couples = {
            "M1": [("exact", "exact", "exact")],
            "M2": [("action", "action", "action"), ("de", "de", "de"),
                   ("de_non_nul", "de_non_nul", "de_non_nul")],
            "M3": [("exact", "exact", "exact")],
            "M4": [("rappel", "rappel", "rappel"),
                   ("completion", "completion", "completion")],
            "M5": [("exact", "exact", "exact")],
            "M6": [("canal_langue", "exact", "canal_langue"),
                   ("tout_accepter", "exact", "tout_accepter")],
            "M8": [("champs", "champs", "champs"), ("exact", "exact", "exact"),
                   ("champs_non_nuls", "champs_non_nuls", "champs_non_nuls"),
                   ("champs_nuls", "champs_nuls", "champs_nuls")],
        }
        for module, paires in couples.items():
            m = self.r["modules"][module]
            for d, i, l in paires:
                self.assertAlmostEqual(m["deficit"][d],
                                       m["intacte"][i] - m["lessee"][l],
                                       places=12)

    def test_json(self):
        texte = json.dumps(self.r, ensure_ascii=False, default=str)
        self.assertIn("M8", texte)


if __name__ == "__main__":
    unittest.main()
