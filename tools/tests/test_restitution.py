#!/usr/bin/env python3
"""test_restitution.py — la restitution v0 (J1.4) : annotation → surface, et le miroir.

Ce que le test fige :
- la commande `drave restituer TEXTE` sort 0 et affiche la fidélité de surface ;
- la surface est reconstruite **sans lire** `Annotation.texte` ;
- les sauts de ligne sont annotés (`graphème` de type `contrôle`) et reviennent ;
- le miroir strict est le minimum de surface/mots/POS (la ponctuation séparée le fait
  tomber), et le contrôle négatif (mélange, troncature) le détecte ;
- sur les **50 textes libres**, 46 annotations et **46/46 surfaces exactes** ; sans le
  correctif `C`, `f50` perd ses sauts de ligne (45/46) — le trou que le miroir a trouvé.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
import tools.restitution as restitution  # noqa: E402

CLI = RACINE / "tools" / "drave.py"
BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8", timeout=120,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return f"code={resultat.returncode}\nstdout={resultat.stdout}\nstderr={resultat.stderr}"


class TestCommande(unittest.TestCase):
    def test_restituer_texte(self):
        sortie = drave("restituer", "Le chat dort.")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertIn("surface", sortie.stdout)
        self.assertIn("exacte 1.0000", sortie.stdout)
        self.assertIn("surface     : 'Le chat dort.'", sortie.stdout)
        self.assertIn("miroir", sortie.stdout)
        self.assertIn("contrôle négatif", sortie.stdout)

    def test_restituer_json(self):
        sortie = drave("restituer", "Le chat dort.", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["schema"], "drave.restitution")
        self.assertEqual(donnees["surface"]["rendu"], "Le chat dort.")
        self.assertTrue(donnees["surface"]["exact"])
        self.assertEqual(donnees["surface"]["fidelite"], 1.0)
        self.assertEqual(donnees["miroir"]["fidelite"], 0.0)  # le point est un token séparé
        self.assertTrue(donnees["controle_negatif"]["detecte"])

    def test_restituer_multiligne(self):
        texte = "# Notes\nLe chat dort.\nLa voisine parle.\n"
        sortie = drave("restituer", "--fichier", _fichier_temp(texte), "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["surface"]["rendu"], texte)
        self.assertTrue(donnees["surface"]["exact"])

    def test_restituer_refus(self):
        for texte in ("", "..."):
            sortie = drave("restituer", texte)
            self.assertEqual(sortie.returncode, 3, detail(sortie))
            self.assertIn("refus d'analyse", sortie.stderr)
        self.assertEqual(drave("restituer").returncode, 2)

    def test_restituer_banc(self):
        banc = {"banc_50": {"resultats": [
            {"id": "t1", "texte": "Le chat dort."},
            {"id": "t2", "texte": "The cat sleeps."},
            {"id": "t3", "texte": "..."},
        ]}}
        chemin = _fichier_temp(json.dumps(banc, ensure_ascii=False), suffixe=".json")
        sortie = drave("restituer", "--banc", chemin, "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["synthese"]["n"], 3)
        self.assertEqual(donnees["synthese"]["annotations"], 2)
        self.assertEqual(donnees["synthese"]["refus"], 1)
        self.assertEqual(donnees["synthese"]["surface"]["exacts"], 2)
        self.assertEqual(donnees["synthese"]["controle_negatif"]["melange_exacts"], 0)


class TestReconstruction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = bl.Heuristique()

    def test_ne_lit_pas_le_texte(self):
        source = "Le chat de la voisine qui dort sur le toit se réveille."
        annotation = self.h.analyser(source, "fr")
        annotation.texte = "PAS LA SOURCE"
        self.assertEqual(restitution.reconstruire(annotation), source)

    def test_surface_sans_controle(self):
        source = "# Notes\nLe chat dort.\n"
        annotation = self.h.analyser(source, "fr")
        self.assertTrue(any(e.niveau == "graphème" and e.type == "contrôle"
                            for e in annotation.etiquettes))
        self.assertEqual(restitution.reconstruire(annotation), source)
        # avant le correctif `C`, le saut de ligne n'était pas annoté
        self.assertNotEqual(restitution.reconstruire_sans_controle(annotation), source)

    def test_niveaux_pauvres(self):
        source = "Le chat dort."
        annotation = self.h.analyser(source, "fr")
        self.assertEqual(restitution.reconstruire(annotation, "graphème"), source)
        self.assertEqual(restitution.reconstruire(annotation, "mot"), "Le chat dort .")
        self.assertEqual(restitution.reconstruire(annotation, "pos"), "Le chat dort .")
        with self.assertRaises(ValueError):
            restitution.reconstruire(annotation, "syntagme")

    def test_distance(self):
        self.assertEqual(restitution.distance_levenshtein("chat", "chat"), 0)
        self.assertEqual(restitution.distance_levenshtein("chat", "chats"), 1)
        self.assertEqual(restitution.distance_levenshtein("chat", "chien"), 3)
        self.assertEqual(restitution.fidelite_caractere("abc", "abc"), 1.0)
        self.assertEqual(restitution.fidelite_caractere("", ""), 1.0)

    def test_controle_negatif(self):
        annotation = self.h.analyser("1234567890", "fr")
        controle = restitution.controler_negatif(annotation, "1234567890")
        # un seul graphème : le mélange est un retournement, pas un no-op
        self.assertFalse(controle["melange"]["exact"])
        self.assertFalse(controle["tronque"]["exact"])
        self.assertTrue(controle["detecte"])


class TestCinquanteTextes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        donnees = json.loads(BANC.read_text(encoding="utf-8"))
        cls.items = restitution.items_banc(donnees)
        cls.h = bl.Heuristique()

    def test_50_textes_46_annotations(self):
        annotations = 0
        exacts = 0
        sans_controle = 0
        for item in self.items:
            annotation = self.h.analyser(item["texte"])
            if annotation.refus:
                continue
            annotations += 1
            exacts += restitution.reconstruire(annotation) == item["texte"]
            sans_controle += restitution.reconstruire_sans_controle(annotation) == item["texte"]
        self.assertEqual(annotations, 46)
        self.assertEqual(exacts, 46)
        self.assertEqual(sans_controle, 45)  # `f50` perd ses sauts de ligne avant le correctif


def _fichier_temp(contenu: str, suffixe: str = ".txt") -> str:
    with tempfile.NamedTemporaryFile("w", suffix=suffixe, delete=False,
                                     encoding="utf-8") as fichier:
        fichier.write(contenu)
        return fichier.name


if __name__ == "__main__":
    unittest.main(verbosity=2)
