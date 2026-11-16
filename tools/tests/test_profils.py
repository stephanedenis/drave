#!/usr/bin/env python3
"""test_profils.py — `drave profils`, la détection de langue UDHR exposée.

Ce que le test fige :

- la commande `profils --texte` (et le TEXTE positionnel) rend la **langue probable**,
  le **script** et la **confiance** ; le JSON porte `schema`, `langue`, `langue_probable`,
  `script`, `confiance`, `sous_seuil`, `source`, `candidats` et `profils.langues == 398` ;
- un texte **ambigu** (bilingue équilibré) est `und` sous le seuil 0,12 ; un **mot isolé**
  aussi ; un texte vide est un **refus** (code 3) ;
- un texte **long** de l'échantillon UDHR est classé par les profils (script inclus) ;
- `--profils` sur `analyser` sert le même détecteur ;
- l'artefact de profils est une **dépendance** : sans lui, code 4, `stdout` vide, pas de trace ;
- la mesure des **20 langues** de l'échantillon UDHR (article 15) est **20/20**, et le
  contrôle **profils permutés** est proche du hasard (0/20).

Le test passe par `python3 tools/tests/test_profils.py` et par `pytest` : il lance le CLI
comme un utilisateur et, pour l'échantillon, lit le corpus local (sauté s'il est absent).
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"
UDHR = RACINE / "data" / "udhr" / "articles.jsonl"


def drave(*arguments: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8",
        timeout=120, env=env,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return (f"code={resultat.returncode}\nstdout={resultat.stdout}\n"
            f"stderr={resultat.stderr}")


def sans_profils() -> dict:
    env = dict(os.environ)
    env["DRAVE_PROFILS"] = str(pathlib.Path(tempfile.gettempdir()) / "drave-profils-absent.json")
    return env


class TestProfilsCLI(unittest.TestCase):
    def test_profils_francais_json(self) -> None:
        sortie = drave("profils", "--texte", "Le chat dort.", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["schema"], "drave.profils")
        self.assertEqual(d["version"], 1)
        self.assertEqual(d["langue"], "fra")
        self.assertEqual(d["langue_probable"], "fra")
        self.assertEqual(d["script"], "Latn")
        self.assertGreater(d["confiance"], 0.0)
        self.assertLessEqual(d["confiance"], 1.0)
        self.assertFalse(d["sous_seuil"])
        self.assertIn(d["source"], {"lexique", "profils"})
        self.assertEqual(d["profils"]["langues"], 398)
        self.assertTrue(d["candidats"])
        self.assertEqual(d["refus"], "")

    def test_sortie_lisible_compacte(self) -> None:
        sortie = drave("profils", "--texte", "Le chat dort.")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertIn("langue=fra", sortie.stdout, detail(sortie))
        self.assertIn("script=Latn", sortie.stdout, detail(sortie))
        self.assertIn("confiance=0.3333", sortie.stdout, detail(sortie))

    def test_texte_positionnel_et_option_equivalents(self) -> None:
        positionnel = drave("profils", "Le chat dort.", "--json")
        option = drave("profils", "--texte", "Le chat dort.", "--json")
        self.assertEqual(positionnel.returncode, 0, detail(positionnel))
        self.assertEqual(option.returncode, 0, detail(option))
        self.assertEqual(positionnel.stdout, option.stdout)

    def test_anglais(self) -> None:
        sortie = drave("profils", "--texte", "The cat sleeps on the roof.", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["langue"], "eng", d)
        self.assertEqual(d["script"], "Latn", d)

    def test_cyrillique(self) -> None:
        sortie = drave("profils", "--texte", "Привет мир", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["langue"], "rus", d)
        self.assertEqual(d["script"], "Cyrl", d)

    def test_ambigu_est_und(self) -> None:
        texte = ("All human beings are born free and equal in dignity and rights. "
                 "Tous les êtres humains naissent libres et égaux en dignité et en droits.")
        sortie = drave("profils", "--texte", texte, "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["langue"], "und", d)
        self.assertTrue(d["sous_seuil"], d)
        self.assertLess(d["confiance"], d["seuil"], d)
        self.assertIn(d["langue_probable"], {"eng", "fra"}, d)

    def test_mot_isole_est_und(self) -> None:
        sortie = drave("profils", "--texte", "chat", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["langue"], "und", d)
        self.assertTrue(d["sous_seuil"], d)

    def test_mot_outil_isole_est_und(self) -> None:
        """Un seul mot-outil (« le », « the ») ne fait pas une langue."""
        for texte in ("le", "the"):
            sortie = drave("profils", "--texte", texte, "--json")
            self.assertEqual(sortie.returncode, 0, detail(sortie))
            d = json.loads(sortie.stdout)
            self.assertEqual(d["langue"], "und", (texte, d))

    def test_vide_est_un_refus(self) -> None:
        sortie = drave("profils", "--texte", "", "--json")
        self.assertEqual(sortie.returncode, 3, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["refus"], "vide", d)
        self.assertEqual(d["langue"], "und", d)
        self.assertEqual(d["etiquettes"] if "etiquettes" in d else [], [])

    def test_fichier(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write("Le chat de la voisine qui dort sur le toit se réveille.\n")
            chemin = f.name
        try:
            sortie = drave("profils", "--fichier", chemin, "--json")
            self.assertEqual(sortie.returncode, 0, detail(sortie))
            d = json.loads(sortie.stdout)
            self.assertEqual(d["langue"], "fra", d)
            self.assertIn("voisine", d["texte"], d)
        finally:
            pathlib.Path(chemin).unlink(missing_ok=True)

    def test_deterministe(self) -> None:
        a = drave("profils", "--texte", "Le chat de la voisine qui dort.", "--json")
        b = drave("profils", "--texte", "Le chat de la voisine qui dort.", "--json")
        self.assertEqual(a.returncode, 0, detail(a))
        self.assertEqual(a.stdout, b.stdout)

    def test_profils_absents_code_4(self) -> None:
        sortie = drave("profils", "--texte", "Le chat dort.", env=sans_profils())
        self.assertEqual(sortie.returncode, 4, detail(sortie))
        self.assertEqual(sortie.stdout, "", detail(sortie))
        self.assertIn("profils de langue absents", sortie.stderr, detail(sortie))
        self.assertNotIn("Traceback", sortie.stderr, detail(sortie))

    def test_seuil_invalide_code_5(self) -> None:
        sortie = drave("profils", "--texte", "Le chat dort.", "--seuil", "2")
        self.assertEqual(sortie.returncode, 5, detail(sortie))

    def test_texte_et_positionnel_exclusifs(self) -> None:
        sortie = drave("profils", "Le chat dort.", "--texte", "The cat sleeps.")
        self.assertEqual(sortie.returncode, 5, detail(sortie))

    def test_seuil_zero_garde_le_probable(self) -> None:
        texte = ("All human beings are born free and equal in dignity and rights. "
                 "Tous les êtres humains naissent libres et égaux en dignité et en droits.")
        sortie = drave("profils", "--texte", texte, "--json", "--seuil", "0")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertFalse(d["sous_seuil"], d)
        self.assertEqual(d["langue"], d["langue_probable"], d)


class TestAnalyserProfils(unittest.TestCase):
    def test_analyser_profils(self) -> None:
        sortie = drave("analyser", "Le chat dort.", "--profils", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertEqual(d["langue"], "fra", d)
        self.assertEqual(d["script"], "Latn", d)
        self.assertTrue(d["etiquettes"], d)

    def test_analyser_profils_absents_code_4(self) -> None:
        sortie = drave("analyser", "Le chat dort.", "--profils", env=sans_profils())
        self.assertEqual(sortie.returncode, 4, detail(sortie))
        self.assertEqual(sortie.stdout, "", detail(sortie))


class TestEchantillonUDHR(unittest.TestCase):
    """La mesure demandée : 20 langues, article 15 tenu à l'écart, profils permutés."""

    ECHANTILLON = [
        ("udhr_eng.xml", "eng"), ("udhr_hin.xml", "hin"), ("udhr_bel.xml", "bel"),
        ("udhr_ell_monotonic.xml", "ell"), ("udhr_kin.xml", "kin"), ("udhr_ewe.xml", "ewe"),
        ("udhr_ibo.xml", "ibo"), ("udhr_fuf_adlm.xml", "fuf"), ("udhr_ind.xml", "ind"),
        ("udhr_tgl.xml", "tgl"), ("udhr_mly_arab.xml", "zlm"), ("udhr_jav.xml", "jav"),
        ("udhr_mya.xml", "mya"), ("udhr_cmn_hant.xml", "cmn"), ("udhr_cnh.xml", "cnh"),
        ("udhr_ctd.xml", "ctd"), ("udhr_arb.xml", "arb"), ("udhr_amh.xml", "amh"),
        ("udhr_heb.xml", "heb"), ("udhr_hau_NE.xml", "hau"),
    ]

    @classmethod
    def setUpClass(cls) -> None:
        if not UDHR.is_file():
            raise unittest.SkipTest(f"corpus UDHR absent : {UDHR}")
        sys.path.insert(0, str(RACINE / "tools"))
        import profils_udhr as pu  # noqa: E402
        import bloc_linguistique as bl  # noqa: E402
        cls.pu = pu
        cls.bl = bl
        cls.profils = pu.charger_profils()
        cls.langues = pu.langues_de(cls.profils)
        cls.rows = {}
        for ligne in UDHR.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            d = json.loads(ligne)
            if d.get("fichier") in {f for f, _ in cls.ECHANTILLON} and int(d.get("art", 0)) == 15:
                cls.rows[d["fichier"]] = d

    def test_20_langues_article_15(self) -> None:
        justes = 0
        scripts = 0
        for fichier, iso3 in self.ECHANTILLON:
            d = self.rows.get(fichier)
            self.assertIsNotNone(d, fichier)
            det = self.pu.detecter(d["texte"], self.profils)
            justes += int(det["langue_probable"] == iso3)
            scripts += int(det["script"] == d["script"]
                           or (det["script"] == "Hani" and d["script"] in {"Hans", "Hant"}))
        self.assertEqual(justes, 20, f"{justes}/20 langues")
        self.assertEqual(scripts, 20, f"{scripts}/20 scripts")

    def test_profils_permutés_proches_du_hasard(self) -> None:
        noms = sorted(self.langues)
        permutes = {noms[i]: self.langues[noms[(i + 1) % len(noms)]].copy()
                    for i in range(len(noms))}
        justes = 0
        for fichier, iso3 in self.ECHANTILLON:
            d = self.rows.get(fichier)
            justes += int(self.bl.detecter_langue(d["texte"], permutes)[0] == iso3)
        self.assertLessEqual(justes, 2, f"{justes}/20 avec des profils permutés")

    def test_artefact_398_et_source(self) -> None:
        self.assertEqual(len(self.langues), 398)
        self.assertEqual(self.profils.get("schema"), "drave.profils-udhr")
        import hashlib
        sha = hashlib.sha256(UDHR.read_bytes()).hexdigest()
        self.assertEqual(self.profils.get("source_sha256"), sha)


if __name__ == "__main__":
    unittest.main(verbosity=2)
