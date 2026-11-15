#!/usr/bin/env python3
"""test_restitution_v3.py — la restitution v3 (W5) : les rôles des GP.

Ce que le test fige :
- `role_gp` sépare `lieu / temps / destinataire / possession / complement` avec le
  contexte (`à` + lieu/temps/destinataire, `de` + GN/GV, `avec` + moyen, `par` +
  passif/moyen, `en` + temps/lieu/moyen/manière, anglais) : 24/24 cas ;
- la préparation dédoublonne les GP de même début sans avaler le verbe ;
- le gold v2 (46) passe de **19/46** cadres exacts (F1 0,5270) à **20/46** (F1 0,5406),
  avec `lieu` 3/6 (P 0,75, R 0,50, F1 0,60) ; le codec 46/46 n'est pas la fidélité ;
- le gold S (61/144) donne **144/144** (cinq rôles 18/18) ; le découpage montre +4 rôles
  et +1 appariement — les deux leviers ne sont pas confondus ;
- le contrôle négatif permute les rôles : les cinq tombent à **0/18**, la permutation de
  tous les rôles tombe à **0,4028** global, le rôle constant `lieu` à **0,0208** ;
- `--roles` (v2) reste inchangé ; `--roles-v3` est le mode v3.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
import tools.restitution as restitution  # noqa: E402
import tools.restitution_v2 as v2  # noqa: E402
import tools.restitution_v3 as v3  # noqa: E402
from tools import roles_gp  # noqa: E402

CLI = RACINE / "tools" / "drave.py"
BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
GOLD = RACINE / "tools" / "tests" / "linguistique" / "gold_restitution_v2.json"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8", timeout=180,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return f"code={resultat.returncode}\nstdout={resultat.stdout}\nstderr={resultat.stderr}"


class TestSeparation(unittest.TestCase):
    def test_cas_de_separation(self):
        r = v3.mesurer_separation()
        self.assertEqual(r["justes"], 24)
        self.assertEqual(r["total"], 24)
        for cas in r["cas"]:
            self.assertTrue(cas["ok"], cas)

    def test_role_gp_contexte(self):
        self.assertEqual(roles_gp.role_gp("à", "la maison"), "lieu")
        self.assertEqual(roles_gp.role_gp("à", "14 h"), "temps")
        self.assertEqual(roles_gp.role_gp("à", "demain"), "temps")
        self.assertEqual(roles_gp.role_gp("à", "Marie"), "destinataire")
        self.assertEqual(roles_gp.role_gp("de", "la voisine", "GN"), "possession")
        self.assertEqual(roles_gp.role_gp("de", "son projet", "GV"), "theme")
        self.assertEqual(roles_gp.role_gp("avec", "le télescope"), "moyen")
        self.assertEqual(roles_gp.role_gp("vers", "9 h"), "temps")
        self.assertEqual(roles_gp.role_gp("vers", "la gare"), "lieu")
        self.assertEqual(roles_gp.role_gp(
            "par", "Marie", "GV", "La lettre a été écrite"), "agent")
        self.assertEqual(roles_gp.role_gp("par", "la porte", "GV", "Il entre"), "moyen")
        self.assertEqual(roles_gp.role_gp("over", "the lazy dog", langue="en"), "lieu")
        self.assertEqual(roles_gp.role_gp("to", "Mary", langue="en"), "destinataire")
        self.assertEqual(roles_gp.role_gp("to", "the station", langue="en"), "lieu")

    def test_role_gp_sans_contexte_reste_v2(self):
        # compatibilité : l'ancien mapping préposition seule ne change pas
        self.assertEqual(bl._role_gp("par"), "agent")
        self.assertEqual(bl._role_gp("avec"), "moyen")
        self.assertEqual(bl._role_gp("à"), "destinataire")
        self.assertEqual(bl._role_gp("de"), "theme")
        self.assertEqual(bl._role_gp("dans"), "lieu")

    def test_preposition_connue(self):
        self.assertTrue(roles_gp.est_preposition("vers"))
        self.assertTrue(roles_gp.est_preposition("d'"))
        self.assertFalse(roles_gp.est_preposition("hier"))
        self.assertFalse(roles_gp.est_preposition("demain"))


class TestPreparation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = bl.Heuristique()

    def _gp(self, texte):
        a = self.h.analyser(texte)
        v3.preparer_annotation(a, texte)
        return [(e.valeur, e.meta.get("role")) for e in a.etiquettes
                if e.niveau == "syntagme" and e.type == "GP"]

    def test_a_heure_un_seul_gp_temps(self):
        self.assertEqual(self._gp("Le train part à 14 h."), [("à 14 h", "temps")])

    def test_vers_heure_dedouble(self):
        self.assertEqual(self._gp("Il part vers 9 h."), [("vers 9 h", "temps")])

    def test_de_la_voisine_ne_mange_pas_le_verbe(self):
        self.assertEqual(self._gp("Le chat de la voisine dort sur le toit."),
                         [("de la voisine", "possession"), ("sur le toit", "lieu")])

    def test_a_marie_et_de_son_projet(self):
        self.assertEqual(self._gp("Il parle à Marie de son projet."),
                         [("à Marie", "destinataire"), ("de son projet", "theme")])

    def test_avec_moyen(self):
        self.assertEqual(self._gp("J'ai vu l'homme avec le télescope."),
                         [("avec le télescope", "moyen")])


class TestBancV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.banc = json.loads(BANC.read_text(encoding="utf-8"))
        cls.gold = json.loads(GOLD.read_text(encoding="utf-8"))
        cls.items = restitution.items_banc(cls.banc)
        cls.rapport = v3.mesurer_banc_v3(cls.items, cls.gold)

    def test_synthese(self):
        s = self.rapport["synthese"]
        self.assertEqual(s["n"], 50)
        self.assertEqual(s["annotations"], 46)
        self.assertEqual(s["refus"], 4)
        self.assertEqual(s["or_textes"], 46)
        c = s["cadre"]
        self.assertEqual(c["exacts"], 20)
        self.assertEqual(c["exacts_non_vides"], 17)
        self.assertEqual(c["exacts_vides"], 3)
        self.assertEqual(c["partiels"], 43)
        self.assertEqual(c["exacts_stricts"], 17)
        r = s["roles"]
        self.assertEqual(r["exacts"], 93)
        self.assertEqual(r["total"], 138)
        self.assertEqual(r["justes"], 40)
        self.assertEqual(r["attendus"], 77)
        self.assertEqual(r["predits"], 71)
        self.assertEqual(r["faux_positifs"], 31)
        self.assertEqual(r["faux_negatifs"], 37)
        self.assertAlmostEqual(r["precision"], 0.5634, places=4)
        self.assertAlmostEqual(r["rappel"], 0.5195, places=4)
        self.assertAlmostEqual(r["f1"], 0.5406, places=4)

    def test_par_role(self):
        r = self.rapport["synthese"]["roles"]["par_role"]
        self.assertEqual((r["agent"]["justes"], r["agent"]["attendus"]), (18, 32))
        self.assertAlmostEqual(r["agent"]["f1"], 0.6, places=4)
        self.assertEqual((r["predicat"]["justes"], r["predicat"]["attendus"]), (19, 39))
        self.assertAlmostEqual(r["predicat"]["f1"], 0.4872, places=4)
        self.assertEqual((r["lieu"]["justes"], r["lieu"]["attendus"]), (3, 6))
        self.assertEqual(r["lieu"]["predits"], 4)
        self.assertAlmostEqual(r["lieu"]["precision"], 0.75, places=4)
        self.assertAlmostEqual(r["lieu"]["rappel"], 0.5, places=4)
        self.assertAlmostEqual(r["lieu"]["f1"], 0.6, places=4)

    def test_couverture_et_codec(self):
        s = self.rapport["synthese"]
        self.assertEqual(s["couverture"]["segments_role"], 194)
        self.assertEqual(s["couverture"]["cinq_roles"], 34)
        self.assertEqual(s["couverture"]["gp_roles"]["temps"], 13)
        self.assertEqual(s["couverture"]["gp_roles"]["possession"], 5)
        self.assertEqual(s["controles"]["spans_dans_source"]["justes"], 194)
        self.assertEqual(s["controles"]["spans_dans_source"]["total"], 194)
        self.assertEqual(s["controles"]["rendu"]["exacts"], 46)
        self.assertEqual(s["controles"]["negatif_rendu"]["eligibles"], 39)
        self.assertEqual(s["controles"]["negatif_rendu"]["detectes"], 39)

    def test_controles(self):
        c = self.rapport["synthese"]["controles"]
        self.assertEqual(c["vide"]["cadres_exacts"], 7)
        self.assertEqual(c["vide"]["justes"], 0)
        self.assertEqual(c["constant_par_type"]["cadres_exacts"], 6)
        self.assertEqual(c["constant_par_type"]["justes"], 39)
        self.assertEqual(c["roles_melanges"]["cadres_exacts"], 3)
        self.assertEqual(c["roles_melanges"]["justes"], 0)


class TestBancV3Negatif(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        banc = json.loads(BANC.read_text(encoding="utf-8"))
        gold = json.loads(GOLD.read_text(encoding="utf-8"))
        cls.items = restitution.items_banc(banc)
        cls.c = v3.controler_banc_v3(cls.items, gold)

    def test_permutation_des_cinq(self):
        p = self.c["permutation_gp"]["synthese"]
        self.assertEqual(p["cadre"]["exacts"], 17)
        self.assertEqual(p["cadre"]["exacts_non_vides"], 14)
        self.assertEqual(p["roles"]["justes"], 37)
        self.assertEqual(p["roles"]["par_role"]["lieu"]["justes"], 0)
        self.assertEqual(p["roles"]["par_role"]["lieu"]["f1"], 0.0)
        self.assertAlmostEqual(p["roles"]["f1"], 0.5139, places=4)

    def test_melange_des_trois(self):
        m = self.c["melange"]
        self.assertEqual(m["cadres_exacts"], 3)
        self.assertEqual(m["justes"], 0)

    def test_mapping(self):
        self.assertEqual(self.c["permutation_gp"]["mapping"], {
            "lieu": "temps", "temps": "destinataire", "destinataire": "possession",
            "possession": "complement", "complement": "lieu"})


class TestGoldS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = v3.mesurer_gold_analyseur_v3()
        cls.v2_roles = v3.mesurer_gold_analyseur_v3(appariement="v2", preparer=False)
        cls.v2_roles_v3_app = v3.mesurer_gold_analyseur_v3(appariement="v3", preparer=False)
        cls.v3_roles_v2_app = v3.mesurer_gold_analyseur_v3(appariement="v2", preparer=True)

    def test_global_et_cinq(self):
        self.assertEqual(self.g["phrases"], 61)
        self.assertEqual(self.g["roles"], 144)
        self.assertEqual(self.g["base"]["justes"], 144)
        self.assertEqual(self.g["base"]["total"], 144)
        self.assertAlmostEqual(self.g["base"]["taux"], 1.0, places=4)
        c = self.g["base"]["cinq_roles"]
        self.assertEqual(c["justes"], 18)
        self.assertEqual(c["attendus"], 18)
        self.assertAlmostEqual(c["precision"], 1.0, places=4)
        self.assertAlmostEqual(c["rappel"], 1.0, places=4)
        self.assertAlmostEqual(c["f1"], 1.0, places=4)

    def test_par_role(self):
        r = self.g["base"]["par_role"]
        for role in ("lieu", "temps", "destinataire", "possession", "theme",
                     "agent", "predicat", "patient", "qualite"):
            self.assertEqual(r[role]["justes"], r[role]["attendus"], role)
            self.assertAlmostEqual(r[role]["f1"], 1.0, places=4)
        self.assertEqual(r["lieu"]["attendus"], 3)
        self.assertEqual(r["temps"]["attendus"], 9)
        self.assertEqual(r["destinataire"]["attendus"], 5)
        self.assertEqual(r["possession"]["attendus"], 1)
        self.assertNotIn("complement", r)  # 0 attendu, 0 prédit : hors table

    def test_decoupage_roles_et_appariement(self):
        self.assertEqual(self.v2_roles["base"]["justes"], 139)
        self.assertEqual(self.v2_roles["base"]["cinq_roles"]["justes"], 17)
        self.assertEqual(self.v2_roles_v3_app["base"]["justes"], 142)
        self.assertEqual(self.v2_roles_v3_app["base"]["cinq_roles"]["justes"], 18)
        self.assertEqual(self.v3_roles_v2_app["base"]["justes"], 143)
        self.assertEqual(self.v3_roles_v2_app["base"]["cinq_roles"]["justes"], 18)
        # +4 rôles (139→143), +1 appariement (143→144)
        self.assertEqual(self.v3_roles_v2_app["base"]["justes"]
                         - self.v2_roles["base"]["justes"], 4)
        self.assertEqual(self.g["base"]["justes"]
                         - self.v3_roles_v2_app["base"]["justes"], 1)

    def test_baseline_type(self):
        b = self.g["baseline_role_constant"]
        self.assertEqual(b["justes"], 104)
        self.assertEqual(b["total"], 144)
        self.assertAlmostEqual(b["taux"], 0.7222, places=4)

    def test_negatifs(self):
        p = self.g["permutation_cinq"]["mesure"]
        self.assertEqual(p["cinq_roles"]["justes"], 0)
        self.assertAlmostEqual(p["cinq_roles"]["f1"], 0.0, places=4)
        self.assertAlmostEqual(p["taux"], 0.875, places=4)
        q = self.g["permutation_tous"]["mesure"]
        self.assertEqual(q["cinq_roles"]["justes"], 0)
        self.assertAlmostEqual(q["taux"], 0.4028, places=4)
        c = self.g["role_constant_lieu"]
        self.assertEqual(c["cinq_roles"]["justes"], 3)
        self.assertAlmostEqual(c["taux"], 0.0208, places=4)
        self.assertAlmostEqual(c["cinq_roles"]["f1"], 0.037, places=4)


class TestRendu(unittest.TestCase):
    def test_codec(self):
        h = bl.Heuristique()
        a = h.analyser("Le chat dort.", "fr")
        rendu = v3.mesurer_annotation_v3(a, "Le chat dort.")
        self.assertEqual(rendu["roles"]["principal"]["agent"], "Le chat")
        self.assertEqual(rendu["roles"]["principal"]["predicat"], "dort")
        self.assertEqual(rendu["roles"]["principal"]["lieu"], "")
        self.assertTrue(rendu["rendu"]["exact"])
        self.assertTrue(rendu["controle_negatif_rendu"]["detecte"])

    def test_rendu_gp(self):
        h = bl.Heuristique()
        m = v3.mesurer_annotation_v3(
            h.analyser("Le train part à 14 h.", "fr"), "Le train part à 14 h.")
        self.assertEqual(m["roles_gp"], {"temps": 1})
        self.assertIn("restitution v3", v3.formater_mesure_v3(m, "Le train part à 14 h."))


class TestCLI(unittest.TestCase):
    def test_roles_v3(self):
        sortie = drave("restituer", "Le train part à 14 h.", "--roles-v3")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertIn("restitution v3", sortie.stdout)
        self.assertIn("temps: 1", sortie.stdout)

    def test_roles_v3_json(self):
        sortie = drave("restituer", "Le train part à 14 h.", "--roles-v3", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["schema"], "drave.restitution.v3")
        self.assertEqual(d["version"], 1)
        self.assertEqual(d["roles_gp"], {"temps": 1})

    def test_banc_v3_json(self):
        sortie = drave("restituer", "--banc", str(BANC), "--roles-v3", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["schema"], "drave.restitution.v3.banc")
        self.assertEqual(d["synthese"]["cadre"]["exacts"], 20)
        self.assertEqual(d["synthese"]["roles"]["f1"], 0.5406)
        self.assertEqual(d["synthese"]["controles"]["rendu"]["exacts"], 46)

    def test_roles_v2_inchange(self):
        sortie = drave("restituer", "--banc", str(BANC), "--roles", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["schema"], "drave.restitution.v2.banc")
        self.assertEqual(d["synthese"]["cadre"]["exacts"], 19)
        self.assertEqual(d["synthese"]["roles"]["f1"], 0.5270)

    def test_exclusifs(self):
        sortie = drave("restituer", "Le chat dort.", "--roles", "--roles-v3")
        self.assertEqual(sortie.returncode, 2, detail(sortie))
        self.assertIn("exclusifs", sortie.stderr)
        sortie = drave("restituer", "Le chat dort.", "--roles-v3", "--canonique")
        self.assertEqual(sortie.returncode, 2, detail(sortie))
        self.assertIn("exclusifs", sortie.stderr)

    def test_gold_avec_roles_v3(self):
        sortie = drave("restituer", "Le chat dort.", "--roles-v3", "--gold", str(GOLD))
        self.assertEqual(sortie.returncode, 2, detail(sortie))
        self.assertIn("--banc", sortie.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
