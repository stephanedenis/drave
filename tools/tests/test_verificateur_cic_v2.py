#!/usr/bin/env python3
"""test_verificateur_cic_v2.py — le banc des ajouts B3 au corpus d'or CIC.

Ce que ce fichier fige, en plus des 21 tests de J12.2 :
- la seconde implémentation de SHA-256 (FIPS 180-4) : vecteurs connus, longueurs
  de rembourrage, sha256 du corpus, 42 couples preuve||type, 24 termes ;
- la vérification du **type de de Bruijn** : 42/42 types clos et bien formés
  (`[] ⊢ type : sort n`), 42/42 preuves closes, et le rejet d'un type ouvert ou
  mal typé ;
- les 36 preuves altérées sont rejetées, et l'empreinte change sous les deux
  implémentations de SHA-256 ;
- un type altéré est invalide ou fait rejeter la preuve (42/42) ;
- un corpus dont un type est corrompu est refusé.
"""
from __future__ import annotations

import functools
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "tools"))

import verificateur_cic as vc  # noqa: E402

CORPUS = RACINE / "tools" / "tests" / "cic" / "corpus_dor_cic_v1.json"
SHA = vc.SHA256_CORPUS


@functools.lru_cache(maxsize=1)
def _mesure_complete() -> dict:
    return vc.mesurer(CORPUS, SHA, controles=True)


class TestSha256SecondeImplementation(unittest.TestCase):
    def test_vecteurs_fips_et_rembourrage(self):
        a = vc.autotest_sha256_pur()
        self.assertEqual(a["verdict"], "pass")
        self.assertGreaterEqual(a["vecteurs"], 16)
        self.assertEqual(a["ecarts"], [])

    def test_vecteurs_connus(self):
        self.assertEqual(
            vc.sha256_pur(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        self.assertEqual(
            vc.sha256_pur(b""),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def test_sha256_du_corpus(self):
        brut = CORPUS.read_bytes()
        self.assertEqual(vc.sha256_pur(brut), hashlib.sha256(brut).hexdigest())
        self.assertEqual(vc.sha256_pur(brut), SHA)

    def test_42_empreintes_par_la_seconde_implementation(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        for e in d["entrees"]:
            self.assertEqual(vc.empreinte_pure(e["preuve_hex"], e["type_hex"]),
                             e["empreinte"], e["nom"])

    def test_24_termes_de_environnement(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        for cle in ("defs", "consts"):
            for nom, hexa in d[cle].items():
                octets = bytes.fromhex(hexa)
                self.assertEqual(vc.sha256_pur(octets),
                                 hashlib.sha256(octets).hexdigest(), nom)

    def test_un_octet_change_empreinte(self):
        self.assertNotEqual(vc.sha256_pur(b"abc"), vc.sha256_pur(b"abd"))
        self.assertNotEqual(vc.sha256_pur(b"\x00" * 64),
                            vc.sha256_pur(b"\x00" * 63 + b"\x01"))


class TestTypeDeBruijn(unittest.TestCase):
    def test_42_types_biens_formes_et_clos(self):
        m = _mesure_complete()
        t = m["type_de_bruijn"]
        self.assertEqual(t["types_totaux"], 42)
        self.assertEqual(t["types_clos"], 42)
        self.assertEqual(t["types_bien_formes"], 42)
        self.assertEqual(t["preuves_closes"], 42)
        self.assertEqual(t["verdict"], "pass")
        self.assertEqual(t["niveaux_observes"], [0, 1])

    def test_type_ouvert_rejete(self):
        noyau = vc.Kernel({}, {})
        self.assertIsNone(noyau.type_bien_forme(("var", 0)))
        self.assertIsNone(noyau.type_bien_forme(("pi", ("var", 0), ("nat",))))
        self.assertFalse(vc.est_clos(("lam", ("nat",), ("var", 1))))

    def test_type_mal_type_rejete(self):
        noyau = vc.Kernel({}, {})
        self.assertIsNone(noyau.type_bien_forme(("app", ("zero",), ("zero",))))
        self.assertIsNone(noyau.type_bien_forme(("lam", ("nat",), ("var", 0))))

    def test_type_valide_accepte(self):
        noyau = vc.Kernel({}, {})
        self.assertEqual(noyau.type_bien_forme(("sort", 0)), ("sort", 1))
        self.assertEqual(noyau.type_bien_forme(("nat",)), ("sort", 0))
        self.assertEqual(
            noyau.type_bien_forme(("pi", ("nat",), ("nat",))), ("sort", 0))

    def test_indices_hors_portee(self):
        self.assertEqual(vc.indices_hors_portee(("var", 0)), [0])
        self.assertEqual(vc.indices_hors_portee(("lam", ("nat",), ("var", 0))), [])
        self.assertEqual(vc.indices_hors_portee(("lam", ("nat",), ("var", 1))), [1])


class TestPreuvesEtTypesAlteres(unittest.TestCase):
    def test_36_preuves_alterees_rejetees(self):
        a = _mesure_complete()["controles_negatifs"]["octet_altere"]
        self.assertEqual(a["mutations"], 36)
        self.assertEqual(a["acceptes_apres_mutation"], 0)
        self.assertEqual(a["rejetes_apres_mutation"], 36)
        self.assertEqual(a["empreintes_changees"], 36)
        self.assertEqual(a["empreintes_pures_changees"], 36)
        self.assertEqual(a["noms_encore_acceptes"], [])
        self.assertEqual(a["verdict"], "pass")

    def test_42_types_alteres_rejetes(self):
        t = _mesure_complete()["controles_negatifs"]["type_altere"]
        self.assertEqual(t["mutations"], 42)
        self.assertEqual(t["acceptes_apres_mutation"], 0)
        self.assertEqual(t["rejetes_apres_mutation"], 42)
        self.assertGreater(t["types_devenus_invalides"], 0)
        self.assertEqual(t["empreintes_changees"], 42)
        self.assertEqual(t["empreintes_pures_changees"], 42)
        self.assertEqual(t["verdict"], "pass")

    def test_exhaustif_eq_2_2(self):
        e = _mesure_complete()["controles_negatifs"]["octet_altere_exhaustif"]
        self.assertEqual(e["preuve"], "eq(2,2)")
        self.assertEqual(e["octets"], 4)
        self.assertEqual(e["mutations"], 1020)
        self.assertEqual(e["acceptes_apres_mutation"], 0)


class TestMesureEtCLI(unittest.TestCase):
    def test_verdict_global_et_integrite(self):
        m = _mesure_complete()
        self.assertEqual(m["tache"], "B3")
        self.assertEqual(m["verdict"], "pass")
        self.assertEqual(m["resultat"]["accord"], 42)
        for cle in ("empreintes", "empreintes_pures", "type_de_bruijn",
                    "preuves_closes", "sha256_seconde_implementation", "verdicts"):
            self.assertTrue(m["integrite"][cle], cle)
        s = m["sha256_independant"]
        self.assertEqual(s["verdict"], "pass")
        self.assertEqual(s["entrees"]["empreintes_declarees_ok"], 42)
        self.assertEqual(s["entrees"]["concordantes_hashlib"], 42)
        self.assertEqual(s["environnement"]["concordants_hashlib"], 24)

    def test_corpus_avec_type_corrompu_refuse(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        e = next(x for x in d["entrees"] if x["verdict"] == "accepte")
        e["type_hex"] = vc._muter_octet(e["type_hex"], -1, 1)
        with tempfile.TemporaryDirectory() as tmp:
            chemin = pathlib.Path(tmp) / "corpus.json"
            chemin.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            m = vc.mesurer(chemin, None, controles=False)
            self.assertEqual(m["verdict"], "fail")
            self.assertLess(m["resultat"]["types_bien_formes"], 42)
            self.assertLess(m["resultat"]["empreintes_pures_valides"], 42)

    def test_cli_json(self):
        p = subprocess.run([sys.executable, str(RACINE / "tools" / "verificateur_cic.py"),
                            "--json", "--sans-controles"],
                           capture_output=True, text=True, cwd=str(RACINE))
        self.assertEqual(p.returncode, 0, p.stderr[:500])
        m = json.loads(p.stdout)
        self.assertEqual(m["verdict"], "pass")
        self.assertIn("sha256_independant", m)
        self.assertEqual(m["type_de_bruijn"]["types_bien_formes"], 42)


if __name__ == "__main__":
    unittest.main(verbosity=2)
