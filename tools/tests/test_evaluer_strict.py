"""test_evaluer_strict.py — le mode `evaluer --strict` : quatre modes, plancher 0,70, code 1.

Ce que le fichier verrouille :

1. `evaluer --strict --json` mesure les **quatre modes** (heuristique, neuronal, parallèle,
   cascade) sur le gold vivant **612** et sur le réel **452** ;
2. la cascade locale passe le plancher **0,70** et la commande sort **0** ;
3. le **contrôle négatif** est mesuré dans la même passe : une cascade dont le POS est forcé
   tombe à **0,00** et le rapport porte **code 1** — le plancher mord ;
4. si le verdict est faux, `cmd_evaluer` sort **1** (injection du rapport, aucun réseau) ;
5. `--strict` est exclusif avec `--gold`, `--tagger` et `--par-langue` (code **5**).

Aucun réseau, aucun GPU : `MockNeuronal` est le neuronal **de contrat**, déterministe.
"""
from __future__ import annotations

import contextlib
import io
import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools"))

import drave  # noqa: E402


def drave_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8", timeout=180,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return f"code={resultat.returncode}\nstdout={resultat.stdout}\nstderr={resultat.stderr}"


class TestEvaluerStrict(unittest.TestCase):
    def test_strict_json_quatre_modes_et_plancher(self) -> None:
        resultat = drave_cli("evaluer", "--strict", "--json")
        self.assertEqual(resultat.returncode, 0, detail(resultat))
        rapport = json.loads(resultat.stdout)
        self.assertTrue(rapport["strict"])
        self.assertEqual(rapport["plancher"], 0.70)
        self.assertEqual(rapport["gold"]["vivant"]["phrases"], 612, rapport["gold"])
        self.assertEqual(rapport["gold"]["reel"]["phrases"], 452, rapport["gold"])
        for gold in ("612", "452"):
            self.assertEqual(
                set(rapport["modes"][gold]),
                {"heuristique", "neuronal", "parallele", "cascade"},
                rapport["modes"][gold].keys(),
            )
            self.assertIn("cascade", rapport["delta"][gold])
        verdict = rapport["verdict"]
        self.assertGreaterEqual(verdict["cascade_pos_612"], 0.70, verdict)
        self.assertGreaterEqual(verdict["cascade_pos_452"], 0.70, verdict)
        self.assertTrue(verdict["ok"], verdict)
        negatif = rapport["controle_negatif"]
        self.assertLess(negatif["pos"], 0.70, negatif)
        self.assertFalse(negatif["passe"], negatif)
        self.assertEqual(negatif["code"], 1, negatif)
        self.assertTrue(negatif["ok"], negatif)

    def test_strict_lisible(self) -> None:
        resultat = drave_cli("evaluer", "--strict")
        self.assertEqual(resultat.returncode, 0, detail(resultat))
        for attendu in ("heuristique", "neuronal", "parallèle", "cascade",
                        "PLANCHER 0.70", "CONTRÔLE NÉGATIF", "code 0"):
            self.assertIn(attendu, resultat.stdout, detail(resultat))

    def test_negative_control_code_1(self) -> None:
        """Une cascade sous le plancher doit faire échouer la commande (code 1)."""
        faux = {
            "verdict": {"plancher": 0.70, "cascade_pos_612": 0.60,
                        "cascade_pos_452": 0.80, "passe_612": False,
                        "passe_452": True, "ok": False},
            "controle_negatif": {"nom": "cascade dégradée", "pos": 0.60,
                                 "plancher": 0.70, "passe": False, "code": 1,
                                 "ok": True},
        }
        ancien_verdict = drave._verdict_strict
        ancien_eval = drave._evaluer_strict
        ancien_module = drave._module_evaluation
        drave._module_evaluation = lambda gele=False: object()
        drave._evaluer_strict = lambda evaluateur, plancher=0.70: faux
        try:
            self.assertFalse(drave._verdict_strict(
                {"cascade": {"pos": {"exactitude": 0.60}}},
                {"cascade": {"pos": {"exactitude": 0.80}}},
            )["ok"])
            sortie, erreur = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreur):
                code = drave.main(["evaluer", "--strict", "--json"])
        finally:
            drave._verdict_strict = ancien_verdict
            drave._evaluer_strict = ancien_eval
            drave._module_evaluation = ancien_module
        self.assertEqual(code, 1, erreur.getvalue())
        self.assertFalse(json.loads(sortie.getvalue())["verdict"]["ok"])

    def test_strict_options_exclusives(self) -> None:
        for option in ("--gold", "--tagger", "--par-langue"):
            resultat = drave_cli("evaluer", "--strict", option)
            self.assertEqual(resultat.returncode, 5, f"{option}\n" + detail(resultat))
            self.assertIn("erreur d'usage", resultat.stderr, detail(resultat))

    def test_aide_declare_strict(self) -> None:
        resultat = drave_cli("evaluer", "--aide")
        self.assertEqual(resultat.returncode, 0, detail(resultat))
        self.assertIn("--strict", resultat.stdout, detail(resultat))


if __name__ == "__main__":
    unittest.main()
