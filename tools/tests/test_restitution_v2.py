#!/usr/bin/env python3
"""test_restitution_v2.py — la restitution v2 (D2) : les rôles agent / prédicat / lieu.

Ce que le test fige :
- `drave restituer TEXTE --roles` rend un cadre principal lisible et un JSON v2 ;
- `relire_roles(rendre_roles(a))` redonne le cadre principal (codec) ;
- le contrôle négatif retire/permute un rôle et le lecteur le voit ;
- sur les **46 textes** de la v0, le cadre principal est exact **19/46** et **16/46**
  non vides ; les rôles exacts sont **91/138**, avec **32 faux positifs** et **38 faux
  négatifs** — la fidélité n'est donc pas acquise ;
- l'or externe (gold S, 61 phrases) donne **139/144** : le lecteur n'est pas cassé quand
  l'or est propre ; l'écart mesure la difficulté du banc v0, pas un bug de format.
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

CLI = RACINE / "tools" / "drave.py"
BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
GOLD = RACINE / "tools" / "tests" / "linguistique" / "gold_restitution_v2.json"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8", timeout=120,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return f"code={resultat.returncode}\nstdout={resultat.stdout}\nstderr={resultat.stderr}"


class TestCommandeRoles(unittest.TestCase):
    def test_restituer_roles(self):
        sortie = drave("restituer", "Le chat dort.", "--roles")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertIn("restitution v2", sortie.stdout)
        self.assertIn("agent         : Le chat", sortie.stdout)
        self.assertIn("prédicat      : dort", sortie.stdout)
        self.assertIn("lieu          : —", sortie.stdout)
        self.assertIn("restitution du rendu : exacte", sortie.stdout)

    def test_restituer_roles_json(self):
        sortie = drave("restituer", "Le chat dort.", "--roles", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["schema"], "drave.restitution.v2")
        self.assertEqual(donnees["version"], 1)
        self.assertEqual(donnees["roles"]["principal"]["agent"], "Le chat")
        self.assertEqual(donnees["roles"]["principal"]["predicat"], "dort")
        self.assertEqual(donnees["roles"]["principal"]["lieu"], "")
        self.assertTrue(donnees["rendu"]["exact"])
        self.assertTrue(donnees["controle_negatif_rendu"]["detecte"])
        self.assertIsNone(donnees["comparaison"])  # pas d'or pour un texte seul

    def test_roles_et_canonique_exclusifs(self):
        sortie = drave("restituer", "Le chat dort.", "--roles", "--canonique")
        self.assertEqual(sortie.returncode, 5, detail(sortie))
        self.assertIn("exclusifs", sortie.stderr)

    def test_gold_sans_banc_refuse(self):
        sortie = drave("restituer", "Le chat dort.", "--roles",
                       "--gold", str(GOLD))
        self.assertEqual(sortie.returncode, 5, detail(sortie))
        self.assertIn("--banc", sortie.stderr)

    def test_banc_roles_json(self):
        sortie = drave("restituer", "--banc", str(BANC), "--roles", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["schema"], "drave.restitution.v2.banc")
        self.assertEqual(donnees["synthese"]["annotations"], 46)
        self.assertEqual(donnees["synthese"]["or_textes"], 46)
        self.assertEqual(donnees["synthese"]["cadre"]["exacts_non_vides"], 16)
        self.assertEqual(donnees["synthese"]["roles"]["f1"], 0.5270)
        self.assertEqual(donnees["synthese"]["controles"]["rendu"]["exacts"], 46)


class TestRenduRoles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = bl.Heuristique()

    def test_rendu_simple(self):
        a = self.h.analyser("Le chat dort.", "fr")
        rendu = v2.rendre_roles(a)
        self.assertEqual(rendu["principal"]["agent"], "Le chat")
        self.assertEqual(rendu["principal"]["predicat"], "dort")
        self.assertEqual(rendu["principal"]["lieu"], "")
        self.assertEqual(rendu["compteurs"]["segments_role"], 2)
        self.assertEqual(v2.relire_roles(rendu["lisible"]), {
            "agent": "Le chat", "predicat": "dort", "lieu": ""})
        self.assertIn("GN/agent", rendu["lisible"])

    def test_rendu_ne_lit_pas_le_texte(self):
        a = self.h.analyser("Le chat dort.", "fr")
        avant = v2.rendre_roles(a)["lisible"]
        a.texte = "PAS LA SOURCE"
        apres = v2.rendre_roles(a)["lisible"]
        self.assertEqual(avant, apres)

    def test_controle_negatif_rendu(self):
        a = self.h.analyser("Le chat dort.", "fr")
        rendu = v2.rendre_roles(a)
        controle = v2.controler_negatif_rendu(rendu)
        self.assertTrue(controle["eligible"])
        self.assertTrue(controle["sans_predicat"]["change"])
        self.assertTrue(controle["permute"]["change"])
        self.assertTrue(controle["detecte"])
        self.assertEqual(controle["sans_predicat"]["relu"]["predicat"], "")
        self.assertEqual(controle["permute"]["relu"]["agent"], "dort")

    def test_controle_non_eligible(self):
        a = self.h.analyser("1234567890", "fr")
        rendu = v2.rendre_roles(a)
        controle = v2.controler_negatif_rendu(rendu)
        self.assertFalse(controle["eligible"])
        self.assertFalse(controle["detecte"])

    def test_melange_roles(self):
        cadre = {"agent": "A", "predicat": "P", "lieu": "L"}
        self.assertEqual(v2.melanger_roles(cadre),
                         {"agent": "P", "predicat": "L", "lieu": "A"})


class TestOrEtBanc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.banc = json.loads(BANC.read_text(encoding="utf-8"))
        cls.gold = json.loads(GOLD.read_text(encoding="utf-8"))
        cls.items = restitution.items_banc(cls.banc)
        cls.rapport = v2.mesurer_banc_v2(cls.items, cls.gold)

    def test_or_46_textes(self):
        textes = self.gold["textes"]
        self.assertEqual(len(textes), 46)
        ids = {t["id"] for t in textes}
        refus = {"f14", "f15", "f16", "f17"}
        self.assertEqual(ids | refus, {it["id"] for it in self.items})
        par_id = {it["id"]: it["texte"] for it in self.items}
        for texte in textes:
            self.assertEqual(texte["texte"], par_id[texte["id"]])
            self.assertTrue(texte["variantes"])
            for variante in texte["variantes"]:
                self.assertEqual(set(variante), set(v2.ROLES))

    def test_synthese_v2(self):
        s = self.rapport["synthese"]
        self.assertEqual(s["n"], 50)
        self.assertEqual(s["annotations"], 46)
        self.assertEqual(s["refus"], 4)
        self.assertEqual(s["or_textes"], 46)
        cadre = s["cadre"]
        self.assertEqual(cadre["exacts"], 19)
        self.assertEqual(cadre["taux"], 0.4130)
        self.assertEqual(cadre["exacts_non_vides"], 16)
        self.assertEqual(cadre["exacts_vides"], 3)
        self.assertEqual(cadre["partiels"], 42)
        self.assertEqual(cadre["exacts_stricts"], 16)
        roles = s["roles"]
        self.assertEqual(roles["exacts"], 91)
        self.assertEqual(roles["total"], 138)
        self.assertEqual(roles["justes"], 39)
        self.assertEqual(roles["attendus"], 77)
        self.assertEqual(roles["predits"], 71)
        self.assertEqual(roles["faux_positifs"], 32)
        self.assertEqual(roles["faux_negatifs"], 38)

    def test_roles_par_role(self):
        roles = self.rapport["synthese"]["roles"]["par_role"]
        self.assertEqual(roles["agent"]["justes"], 18)
        self.assertEqual(roles["agent"]["attendus"], 32)
        self.assertEqual(roles["predicat"]["justes"], 19)
        self.assertEqual(roles["predicat"]["attendus"], 39)
        self.assertEqual(roles["lieu"]["justes"], 2)
        self.assertEqual(roles["lieu"]["attendus"], 6)
        self.assertEqual(roles["agent"]["f1"], 0.6)
        self.assertEqual(roles["predicat"]["f1"], 0.4872)
        self.assertEqual(roles["lieu"]["f1"], 0.4)

    def test_controles_v2(self):
        c = self.rapport["synthese"]["controles"]
        self.assertEqual(c["vide"]["cadres_exacts"], 7)
        self.assertEqual(c["constant_par_type"]["cadres_exacts"], 6)
        self.assertEqual(c["roles_melanges"]["cadres_exacts"], 3)
        self.assertEqual(c["rendu"]["exacts"], 46)
        self.assertEqual(c["negatif_rendu"]["eligibles"], 39)
        self.assertEqual(c["negatif_rendu"]["detectes"], 39)
        self.assertEqual(c["spans_dans_source"]["justes"], 198)
        self.assertEqual(c["spans_dans_source"]["total"], 198)

    def test_cas_connus(self):
        par_id = {r["id"]: r for r in self.rapport["resultats"]}
        self.assertEqual(par_id["f01"]["comparaison"]["exacts"], 3)
        self.assertEqual(par_id["f02"]["comparaison"]["exacts"], 3)
        self.assertEqual(par_id["f46"]["comparaison"]["exacts"], 3)
        # f27 (« Élodie sourit. ») n'a aucun syntagme : le cadre est vide, donc faux.
        self.assertEqual(par_id["f27"]["comparaison"]["exacts"], 1)
        self.assertEqual(par_id["f03"]["comparaison"]["exacts"], 1)
        self.assertEqual(par_id["f20"]["comparaison"]["exacts"], 0)


class TestGoldExterne(unittest.TestCase):
    def test_gold_analyseur(self):
        r = v2.mesurer_gold_analyseur()
        self.assertEqual(r["phrases"], 61)
        self.assertEqual(r["roles_justes"], 139)
        self.assertEqual(r["roles_total"], 144)
        self.assertEqual(r["taux"], 0.9653)
        self.assertEqual(r["baseline_role_constant"]["justes"], 104)
        self.assertEqual(r["baseline_role_constant"]["taux"], 0.7222)


class TestMesureSansOr(unittest.TestCase):
    def test_sans_or(self):
        h = bl.Heuristique()
        source = "Le chat dort."
        a = h.analyser(source, "fr")
        m = v2.mesurer_annotation_v2(a, source)
        self.assertIsNone(m["comparaison"])
        self.assertTrue(m["rendu"]["exact"])
        self.assertIsNotNone(m["controle_negatif_rendu"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
