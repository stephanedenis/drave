#!/usr/bin/env python3
"""test_verificateur_cic.py — le banc du vérificateur indépendant du corpus d'or CIC.

Ce que le test fige :
- le corpus portable est byte-identique à l'artefact Panini (sha256) ;
- les 42 verdicts sont rejoués (36 acceptés, 6 rejetés), 42/42 d'accord ;
- les 42 empreintes `sha256(preuve || type)` sont valides ;
- la sérialisation de Bruijn est canonique (décodage puis ré-encodage identique) ;
- altérer un octet d'une preuve acceptée la fait rejeter (36/36), et l'énumération
  exhaustive des 1 020 mutations de `eq(2,2)` n'en accepte aucune ;
- un noyau « accepte tout » et un noyau « rejette tout » échouent (non-trivialité) ;
- un corpus localement corrompu (octet ou verdict) est détecté, pas absorbé.
"""
from __future__ import annotations

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
MANIFESTE = RACINE / "tools" / "tests" / "cic" / "manifeste.json"
SHA = vc.SHA256_CORPUS


def _mesure(chemin: pathlib.Path = CORPUS, controles: bool = False) -> dict:
    return vc.mesurer(chemin, SHA, controles=controles)


class TestCorpusPortable(unittest.TestCase):
    def test_manifeste_et_copie(self):
        m = json.loads(MANIFESTE.read_text(encoding="utf-8"))
        octets = CORPUS.read_bytes()
        self.assertEqual(hashlib.sha256(octets).hexdigest(), m["copie"]["sha256"])
        self.assertEqual(m["copie"]["sha256"], m["source"]["sha256"])
        self.assertTrue(m["copie"]["byte_identique"])
        self.assertEqual(len(octets), m["copie"]["octets"])
        self.assertEqual(m["source"]["sha256"], SHA)

    def test_structure(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        self.assertEqual(len(d["defs"]), 3)
        self.assertEqual(len(d["consts"]), 21)
        self.assertEqual(len(d["entrees"]), 42)
        verdicts = [e["verdict"] for e in d["entrees"]]
        self.assertEqual(verdicts.count("accepte"), 36)
        self.assertEqual(verdicts.count("rejette"), 6)

    def test_serialisation_canonique(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        for nom, hexa in d["defs"].items():
            t = vc.decode_exact(hexa)
            self.assertEqual(vc.serialize(t).hex(), hexa, nom)
        for nom, hexa in d["consts"].items():
            t = vc.decode_exact(hexa)
            self.assertEqual(vc.serialize(t).hex(), hexa, nom)
        for e in d["entrees"]:
            for cle in ("preuve_hex", "type_hex"):
                t = vc.decode_exact(e[cle])
                self.assertEqual(vc.serialize(t).hex(), e[cle], f"{e['nom']}:{cle}")

    def test_empreintes(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        for e in d["entrees"]:
            self.assertEqual(vc.empreinte(e["preuve_hex"], e["type_hex"]),
                             e["empreinte"], e["nom"])


class TestRejeu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = _mesure()

    def test_42_sur_42(self):
        r = self.m["resultat"]
        self.assertEqual(r["verdicts"], 42)
        self.assertEqual(r["accord"], 42)
        self.assertEqual(r["desaccord"], 0)
        self.assertEqual(r["attendus_acceptes"], 36)
        self.assertEqual(r["attendus_rejetes"], 6)
        self.assertEqual(r["taux_accord"], 1.0)

    def test_integrite(self):
        i = self.m["integrite"]
        self.assertTrue(i["sha256_corpus"])
        self.assertTrue(i["serialisation_environnement"])
        self.assertTrue(i["serialisation_entrees"])
        self.assertTrue(i["empreintes"])
        self.assertTrue(i["verdicts"])
        self.assertEqual(self.m["resultat"]["empreintes_valides"], 42)
        self.assertEqual(self.m["resultat"]["serialisations_canoniques"], 42)

    def test_verdict_global(self):
        self.assertEqual(self.m["verdict"], "pass")

    def test_les_six_rejets_sont_rejetes(self):
        rejets = [e for e in self.m["resultat"]["entrees"] if e["attendu"] == "rejette"]
        self.assertEqual(len(rejets), 6)
        for e in rejets:
            self.assertEqual(e["obtenu"], "rejette", e["nom"])
            self.assertTrue(e["accord"], e["nom"])

    def test_les_arithmetiques_sont_acceptees(self):
        for nom in ("add_zero", "add_succ", "add_comm", "add_assoc",
                    "mul_zero", "mul_succ", "mul_comm"):
            e = next(x for x in self.m["resultat"]["entrees"] if x["nom"] == nom)
            self.assertEqual(e["obtenu"], "accepte", nom)


class TestControlesNegatifs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = _mesure(controles=True)

    def test_octet_altere_sur_les_36_preuves(self):
        a = self.m["controles_negatifs"]["octet_altere"]
        self.assertEqual(a["mutations"], 36)
        self.assertEqual(a["acceptes_apres_mutation"], 0)
        self.assertEqual(a["rejetes_apres_mutation"], 36)
        self.assertEqual(a["empreintes_changees"], 36)
        self.assertEqual(a["verdict"], "pass")

    def test_octet_altere_exhaustif(self):
        e = self.m["controles_negatifs"]["octet_altere_exhaustif"]
        self.assertEqual(e["preuve"], "eq(2,2)")
        self.assertEqual(e["octets"], 4)
        self.assertEqual(e["mutations"], 4 * 255)
        self.assertEqual(e["acceptes_apres_mutation"], 0)
        self.assertEqual(e["verdict"], "pass")

    def test_non_trivialite(self):
        n = self.m["controles_negatifs"]["non_trivialite"]
        self.assertEqual(n["accepte_tout"]["accord"], 36)
        self.assertEqual(n["accepte_tout"]["desaccord"], 6)
        self.assertEqual(n["rejette_tout"]["accord"], 6)
        self.assertEqual(n["rejette_tout"]["desaccord"], 36)
        self.assertEqual(n["accepte_tout"]["verdict"], "pass")
        self.assertEqual(n["rejette_tout"]["verdict"], "pass")

    def test_mutation_directe(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        e = next(x for x in d["entrees"] if x["verdict"] == "accepte")
        mut = vc._muter_octet(e["preuve_hex"], -1, 1)
        self.assertNotEqual(mut, e["preuve_hex"])
        self.assertNotEqual(vc.empreinte(mut, e["type_hex"]), e["empreinte"])
        noyau = vc.Kernel(
            {k: vc.decode_exact(h) for k, h in d["defs"].items()},
            {k: vc.decode_exact(h) for k, h in d["consts"].items()},
        )
        try:
            self.assertFalse(noyau.verify(vc.decode_exact(mut),
                                          vc.decode_exact(e["type_hex"])))
        except vc.DecodeError:
            pass  # un flux tronqué est un rejet, pas un plantage du banc


class TestRobustesse(unittest.TestCase):
    def test_octet_en_trop(self):
        with self.assertRaises(vc.DecodeError):
            vc.decode_exact("0a07070600")

    def test_etiquette_inconnue(self):
        with self.assertRaises(vc.DecodeError):
            vc.decode_exact("ff")

    def test_varint_non_canonique(self):
        # 0x80 0x00 encode 0 sur deux octets : non canonique, doit être refusé.
        with self.assertRaises(vc.DecodeError):
            vc.decode_exact("008000")

    def test_substitution_simultanee_ne_capture_pas(self):
        # var 0 -> a, var 1 -> b ; a et b ont des variables libres.
        t = ("pair", ("var", 0), ("var", 1))
        a, b = ("var", 7), ("var", 9)
        self.assertEqual(vc.subst_many(t, [a, b]),
                         ("pair", a, b))

    def test_corpus_altere_est_detecte(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        e = next(x for x in d["entrees"] if x["verdict"] == "accepte")
        e["preuve_hex"] = vc._muter_octet(e["preuve_hex"], -1, 1)
        with tempfile.TemporaryDirectory() as tmp:
            chemin = pathlib.Path(tmp) / "corpus.json"
            chemin.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            m = vc.mesurer(chemin, None, controles=False)
            self.assertEqual(m["verdict"], "fail")
            self.assertLess(m["resultat"]["empreintes_valides"], 42)

    def test_verdict_flippe_est_detecte(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        e = next(x for x in d["entrees"] if x["verdict"] == "accepte")
        e["verdict"] = "rejette"
        with tempfile.TemporaryDirectory() as tmp:
            chemin = pathlib.Path(tmp) / "corpus.json"
            chemin.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            m = vc.mesurer(chemin, None, controles=False)
            self.assertEqual(m["verdict"], "fail")
            self.assertGreaterEqual(m["resultat"]["desaccord"], 1)

    def test_cli_json(self):
        p = subprocess.run([sys.executable, str(RACINE / "tools" / "verificateur_cic.py"),
                            "--json", "--sans-controles"],
                           capture_output=True, text=True, cwd=str(RACINE))
        self.assertEqual(p.returncode, 0, p.stderr[:500])
        m = json.loads(p.stdout)
        self.assertEqual(m["verdict"], "pass")
        self.assertEqual(m["resultat"]["accord"], 42)

    def test_cli_corpus_corrompu_code_1(self):
        d = json.loads(CORPUS.read_text(encoding="utf-8"))
        e = next(x for x in d["entrees"] if x["verdict"] == "accepte")
        e["preuve_hex"] = vc._muter_octet(e["preuve_hex"], -1, 1)
        with tempfile.TemporaryDirectory() as tmp:
            chemin = pathlib.Path(tmp) / "corpus.json"
            chemin.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            p = subprocess.run([sys.executable, str(RACINE / "tools" / "verificateur_cic.py"),
                                "--corpus", str(chemin), "--sha256", "",
                                "--sans-controles"],
                               capture_output=True, text=True, cwd=str(RACINE))
            self.assertEqual(p.returncode, 1, p.stdout[-500:] + p.stderr[-500:])


if __name__ == "__main__":
    unittest.main(verbosity=2)
