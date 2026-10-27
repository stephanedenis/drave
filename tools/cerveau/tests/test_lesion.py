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
            self.assertEqual(v, 0.0)

    def test_m1_contexte(self):
        d = self.r["modules"]["M1"]["deficit"]["exact"]
        self.assertGreater(d, 0.25)
        self.assertLess(d, 0.35)

    def test_m2_double_dissociation(self):
        m2 = self.r["modules"]["M2"]
        self.assertTrue(m2["deficit"]["double_dissociation"])
        self.assertGreater(m2["deficit"]["action"], 0.3)
        self.assertGreater(m2["deficit"]["de_non_nul"], 0.3)

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
        self.assertGreater(m8["deficit"]["champs"], 0.15)
        self.assertEqual(m8["deficit"]["exact_codes_nouveaux"], 0.0)
        self.assertEqual(m8["intacte"]["hybride_exact_queue"], 1.0)

    def test_json(self):
        texte = json.dumps(self.r, ensure_ascii=False, default=str)
        self.assertIn("M8", texte)


if __name__ == "__main__":
    unittest.main()
