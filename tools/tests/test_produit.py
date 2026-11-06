"""test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.

Huit assertions, deux phrases (fr/en), le déterminisme et les codes de sortie. Le test passe
aussi bien par `python3 tools/tests/test_produit.py` que par `pytest` : il n'importe rien du
dépôt directement, il lance la commande comme un utilisateur.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Lance la commande depuis la racine du dépôt, en UTF-8, sans réseau."""
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return (f"code={resultat.returncode}\n"
            f"stdout={resultat.stdout}\n"
            f"stderr={resultat.stderr}")


class TestProduit(unittest.TestCase):
    """Le contrat produit : version/aide, analyse, JSON, rejeu, usage."""

    def test_version_et_aide(self) -> None:
        version = drave("--version")
        aide = drave("--aide")
        self.assertTrue(
            version.returncode == 0
            and re.fullmatch(r"drave \d+\.\d+\.\d+\n", version.stdout)
            and aide.returncode == 0
            and all(mot in aide.stdout for mot in ("analyser", "evaluer", "rejouer", "--aide")),
            detail(version) + detail(aide),
        )

    def test_analyser_francais(self) -> None:
        resultat = drave("analyser", "Le chat dort.")
        self.assertTrue(
            resultat.returncode == 0 and "langue=fr" in resultat.stdout,
            detail(resultat),
        )
        self.assertTrue(
            all(mot in resultat.stdout
                for mot in ("chat/NOUN", "GN", "rôle=agent", "→ dort", "acte=assertion")),
            detail(resultat),
        )

    def test_analyser_anglais(self) -> None:
        resultat = drave("analyser", "The cat sleeps on the roof.", "--langue", "en")
        self.assertTrue(
            resultat.returncode == 0
            and all(mot in resultat.stdout
                    for mot in ("langue=en", "sleeps/VERB", "GN", "GP", "rôle=lieu")),
            detail(resultat),
        )

    def test_json_valide_et_deterministe(self) -> None:
        premier = drave("analyser", "Le chat dort.", "--json")
        second = drave("analyser", "Le chat dort.", "--json")
        donnees = json.loads(premier.stdout)  # un JSON invalide fait échouer le test ici
        etiquettes = {(e["niveau"], e["type"]) for e in donnees["etiquettes"]}
        self.assertTrue(
            premier.returncode == 0
            and donnees["langue"] == "fr"
            and ("pos", "NOUN") in etiquettes
            and ("syntagme", "GN") in etiquettes
            and bool(donnees["unites_semantiques"])
            and "duree_s" not in donnees["cout"],
            detail(premier),
        )
        self.assertEqual(premier.stdout, second.stdout,
                         "deux appels à --json doivent rendre exactement la même sortie")

    def test_rejouer_deterministe(self) -> None:
        resultat = drave("rejouer", "Le chat de la voisine qui dort sur le toit se réveille.")
        self.assertTrue(
            resultat.returncode == 0
            and "rejeu identique : oui" in resultat.stdout
            and "sha256" in resultat.stdout,
            detail(resultat),
        )

    def test_codes_usage(self) -> None:
        sans_commande = drave()
        langue_inconnue = drave("analyser", "Le chat dort.", "--langue", "de")
        self.assertEqual(
            (2, 2),
            (sans_commande.returncode, langue_inconnue.returncode),
            detail(sans_commande) + detail(langue_inconnue),
        )


class TestRobustesse(unittest.TestCase):
    """Les entrées hostiles ne font pas planter le produit (audit de fiabilité P0)."""

    def test_surrogate_isole(self):
        sys.path.insert(0, str(RACINE))
        import tools.bloc_linguistique as bl
        a = bl.Heuristique().analyser("Le chat \ud800 dort.", "fr")
        self.assertEqual(a.refus, "")
        self.assertGreater(len(a.etiquettes), 3)

    def test_entrees_non_textuelles(self):
        sys.path.insert(0, str(RACINE))
        import tools.bloc_linguistique as bl
        h = bl.Heuristique()
        for valeur in (b"octets", 42, ["liste"], None):
            a = h.analyser(valeur, "fr")
            self.assertEqual(a.refus, "non_texte", type(valeur).__name__)
            self.assertEqual(a.etiquettes, [])


if __name__ == "__main__":
    unittest.main()
