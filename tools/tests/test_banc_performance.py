"""test_banc_performance.py — les fondations du banc : découpage, ajustements, tagger.

Le banc est un outil de mesure : ses **calculs** doivent être justes avant que ses chiffres
servent de résultat. Ces tests ne mesurent pas la performance de la machine ; ils vérifient
que le préfixe est exact, que le bloc est fait de phrases entières, que les ajustements
retrouvent une pente connue et que l'extrapolation du tagger est cohérente.

    python3 tools/tests/test_banc_performance.py
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CHEMIN = RACINE / "tools" / "banc_performance.py"


def _charger():
    spec = importlib.util.spec_from_file_location("banc_performance_test", CHEMIN)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


banc = _charger()


class TestDecoupage(unittest.TestCase):
    def test_prefixe_exact(self) -> None:
        texte = "Un deux trois quatre cinq six sept huit neuf dix."
        prefixe, n = banc._prefixe_mots(texte, 5)
        self.assertEqual(n, 5)
        self.assertEqual(banc._compter_mots(prefixe), 5)
        self.assertTrue(prefixe.endswith("cinq"))
        # le 6e mot n'est pas dans le préfixe
        self.assertNotIn("six", prefixe)

    def test_prefixe_plus_long_que_le_texte(self) -> None:
        texte = "Un deux trois."
        prefixe, n = banc._prefixe_mots(texte, 100)
        self.assertEqual(n, 3)
        # le préfixe s'arrête au dernier token mot, pas après la ponctuation finale
        self.assertEqual(banc._compter_mots(prefixe), 3)
        self.assertTrue(texte.startswith(prefixe))

    def test_bloc_de_phrases_entieres(self) -> None:
        texte = "Le chat dort.\n\nLe chien mange.\n\nL'oiseau vole."
        bloc, debut, fin = banc._bloc_phrases(texte, cible=6)
        self.assertGreaterEqual(banc._compter_mots(bloc), 3)
        self.assertLessEqual(banc._compter_mots(bloc), 6)
        self.assertTrue(bloc.endswith("."))
        self.assertGreaterEqual(fin, debut)
        self.assertTrue(texte[debut:fin].strip().startswith(bloc.split("\n")[0]))

    def test_phrases_courtes_3_a_12_mots(self) -> None:
        texte = ("Le chat dort.\n\nLe chien mange.\n\nL'oiseau vole.\n\n"
                 "La voisine lit.\n\nLe facteur passe.\n\n"
                 "Un très long texte qui contient beaucoup de mots et qui ne doit pas "
                 "être retenu comme phrase courte.")
        phrases = banc._phrases_courtes(texte, 5)
        self.assertEqual(len(phrases), 5)
        for phrase in phrases:
            self.assertTrue(3 <= banc._compter_mots(phrase) <= 12, phrase)


class TestAjustements(unittest.TestCase):
    def test_lineaire(self) -> None:
        xs = [1.0, 2.0, 3.0, 4.0, 5.0]
        ys = [2.0 + 3.0 * x for x in xs]
        fit = banc._ols(xs, ys)
        self.assertAlmostEqual(fit["a"], 2.0, places=9)
        self.assertAlmostEqual(fit["b"], 3.0, places=9)
        self.assertAlmostEqual(fit["r2"], 1.0, places=9)
        self.assertAlmostEqual(fit["rmse"], 0.0, places=9)

    def test_quadratique(self) -> None:
        xs = [1.0, 2.0, 3.0, 4.0]
        ys = [1.0 + 2.0 * x + 0.5 * x * x for x in xs]
        fit = banc._quadratique(xs, ys)
        self.assertAlmostEqual(fit["a"], 1.0, places=9)
        self.assertAlmostEqual(fit["b"], 2.0, places=9)
        self.assertAlmostEqual(fit["c"], 0.5, places=9)
        self.assertAlmostEqual(fit["r2"], 1.0, places=9)

    def test_loglog_quadratique(self) -> None:
        xs = [1.0, 2.0, 4.0, 8.0, 16.0]
        ys = [x * x for x in xs]
        fit = banc._loglog(xs, ys)
        self.assertAlmostEqual(fit["alpha"], 2.0, places=9)
        self.assertAlmostEqual(fit["r2"], 1.0, places=9)

    def test_loglog_lineaire(self) -> None:
        xs = [1.0, 2.0, 4.0, 8.0, 16.0]
        ys = [3.0 * x for x in xs]
        fit = banc._loglog(xs, ys)
        self.assertAlmostEqual(fit["alpha"], 1.0, places=9)


class TestTagger(unittest.TestCase):
    LIGNE = ("drave: TAGGER API · modèle=deepseek-chat · appels=92 · réseau=92 "
             "· cache=0 · tokens=14677 · latence=109.1 s")

    def test_lecture_de_la_ligne(self) -> None:
        stats = banc._lire_stats_tagger(self.LIGNE + "\n")
        self.assertEqual(stats["appels"], 92)
        self.assertEqual(stats["reseau"], 92)
        self.assertEqual(stats["cache"], 0)
        self.assertEqual(stats["tokens"], 14677)
        self.assertAlmostEqual(stats["latence_s"], 109.1, places=1)

    def test_ligne_absente(self) -> None:
        self.assertEqual(banc._lire_stats_tagger("rien"), {})

    def test_extrapolation(self) -> None:
        tagger = {"cent_courtes": {
            "phrases": 94, "duree_s": 110.0,
            "stats": {"appels": 92, "reseau": 92, "tokens": 14677, "latence_s": 109.1},
        }}
        corpus = {"phrases": 814, "mots": 10000,
                  "phrases_courtes": {"n": 100, "mots": 661}}
        banc._extrapoler_10k(tagger, corpus)
        e = tagger["cent_courtes"]["extrapolation_10k"]
        self.assertFalse(e["mesure"])
        self.assertEqual(e["phrases"], 814)
        self.assertEqual(e["phrases_mesurees"], 94)
        self.assertEqual(e["appels_estimes"], 797)
        self.assertGreater(e["tokens_estimes"], 200000)
        self.assertGreater(e["duree_estimee_s"], 900)
        self.assertAlmostEqual(e["rapport_longueur"], (10000 / 814) / (661 / 94), places=6)


class TestResumes(unittest.TestCase):
    def test_resume(self) -> None:
        r = banc._resume([1.0, 2.0, 3.0, 4.0])
        self.assertEqual(r["n"], 4)
        self.assertEqual(r["mediane"], 2.5)
        self.assertEqual(r["min"], 1.0)
        self.assertEqual(r["max"], 4.0)
        self.assertEqual(r["p95"], 4.0)


if __name__ == "__main__":
    unittest.main()
