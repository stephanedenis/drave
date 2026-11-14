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

    def test_restituer_canonique(self):
        sortie = drave("restituer", "Le chat dort.", "--canonique")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertIn("forme canonique", sortie.stdout)
        self.assertIn("GN/agent: le chat -> dort", sortie.stdout)
        self.assertIn("miroir strict", sortie.stdout)
        self.assertIn("canonique: 1.0000", sortie.stdout)

    def test_restituer_canonique_json(self):
        sortie = drave("restituer", "Le chat dort.", "--canonique", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["schema"], "drave.restitution.canonique")
        self.assertEqual(donnees["forme"]["surface_canonique"], "le chat dort")
        self.assertEqual(len(donnees["forme"]["segments"]), 2)
        self.assertTrue(donnees["canonique"]["exact"])
        self.assertFalse(donnees["strict"]["exact"])
        self.assertFalse(donnees["strict_sur_canonique"]["exact"])
        self.assertTrue(donnees["controle_negatif_canonique"]["detecte"])

    def test_restituer_banc_canonique(self):
        banc = {"banc_50": {"resultats": [
            {"id": "t1", "texte": "Le chat dort."},
            {"id": "t2", "texte": "...", "langue": "fr"},
        ]}}
        chemin = _fichier_temp(json.dumps(banc, ensure_ascii=False), suffixe=".json")
        sortie = drave("restituer", "--banc", chemin, "--canonique", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        donnees = json.loads(sortie.stdout)
        self.assertEqual(donnees["schema"], "drave.restitution.canonique.banc")
        self.assertEqual(donnees["synthese"]["annotations"], 1)
        self.assertEqual(donnees["synthese"]["canonique"]["exacts"], 1)
        self.assertEqual(donnees["synthese"]["strict"]["exacts"], 0)


class TestFormeCanonique(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = bl.Heuristique()

    def test_forme_simple(self):
        a = self.h.analyser("Le chat dort.", "fr")
        forme = restitution.forme_canonique(a)
        self.assertIsNotNone(forme)
        self.assertEqual(forme["surface_canonique"], "le chat dort")
        self.assertEqual(forme["jetons"], ["le", "chat", "dort"])
        self.assertEqual(len(forme["segments"]), 2)
        self.assertEqual([s["type"] for s in forme["segments"]], ["GN", "GV"])
        self.assertEqual([s["role"] for s in forme["segments"]], ["agent", "predicat"])
        self.assertEqual([s["cible"] for s in forme["segments"]], ["dort", "chat"])
        self.assertEqual([s["cible_segment"] for s in forme["segments"]], [1, 0])
        self.assertEqual(forme["squelette"],
                         ["GN/agent: le chat -> dort", "GV/predicat: dort -> chat"])
        self.assertEqual(len(forme["cle"]), 64)

    def test_ne_lit_pas_le_texte(self):
        a = self.h.analyser("Le chat dort.", "fr")
        avant = restitution.forme_canonique(a)["cle"]
        a.texte = "PAS LA SOURCE"
        apres = restitution.forme_canonique(a)["cle"]
        self.assertEqual(avant, apres)

    def test_miroir_canonique_et_strict(self):
        source = "Le chat dort."
        a = self.h.analyser(source, "fr")
        mesure = restitution.mesurer_annotation_v1(a, source)
        self.assertEqual(mesure["canonique"]["fidelite"], 1.0)
        self.assertTrue(mesure["canonique"]["exact"])
        self.assertEqual(mesure["strict"]["fidelite"], 0.0)
        self.assertEqual(mesure["strict_sur_canonique"]["fidelite"], 0.0)
        self.assertEqual(mesure["structure"]["cibles_resolues"], 2)
        self.assertTrue(mesure["stabilite"]["squelette_identique"])

    def test_controles_negatifs(self):
        source = "Le chat dort."
        a = self.h.analyser(source, "fr")
        canonique = restitution.controler_negatif_canonique(a, source)
        self.assertFalse(canonique["melange"]["exact"])
        self.assertFalse(canonique["tronque"]["exact"])
        self.assertTrue(canonique["detecte"])
        structure = restitution.controler_negatif_structure(a)
        self.assertEqual(structure["roles_retires"], 2)
        self.assertEqual(structure["cibles_retirees"], 2)
        self.assertTrue(structure["cle_changee"])
        self.assertTrue(structure["detecte"])

    def test_distance_canonique(self):
        self.assertEqual(restitution.canoniser("Le Chat, dort !"), "le chat dort")
        self.assertEqual(restitution.jetons_canoniques("l'eau"), ["l", "eau"])
        self.assertEqual(restitution.canoniser(""), "")


class TestCinquanteTextesV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        donnees = json.loads(BANC.read_text(encoding="utf-8"))
        cls.items = restitution.items_banc(donnees)
        cls.rapport = restitution.mesurer_banc_v1(cls.items)

    def test_synthese_v1(self):
        s = self.rapport["synthese"]
        self.assertEqual(s["annotations"], 46)
        self.assertEqual(s["refus"], 4)
        self.assertEqual(s["strict"]["exacts"], 5)
        self.assertEqual(s["strict"]["fidelite"], 0.1087)
        self.assertEqual(s["canonique"]["exacts"], 46)
        self.assertEqual(s["canonique"]["fidelite"], 1.0)
        self.assertEqual(s["strict_sur_canonique"]["exacts"], 1)
        self.assertEqual(s["strict_sur_canonique"]["fidelite"], 0.0217)

    def test_structure_v1(self):
        s = self.rapport["synthese"]["structure"]
        self.assertEqual(s["segments"], 395)
        self.assertEqual(s["segments_avec_role"], 395)
        self.assertEqual(s["attachements"], 315)
        self.assertEqual(s["cibles_resolues"], 315)
        self.assertEqual(s["cibles_dans_un_segment"], 313)
        self.assertEqual(s["taux_roles"], 1.0)
        self.assertEqual(s["taux_cibles_resolues"], 1.0)
        self.assertEqual(s["taux_cibles_dans_un_segment"], 0.9937)
        self.assertEqual(s["couverture_jetons"], 0.6584)
        self.assertEqual(s["couverture_caracteres"], 0.7519)

    def test_stabilite_et_controles_v1(self):
        s = self.rapport["synthese"]
        self.assertEqual(s["stabilite"]["squelette_identique"], 18)
        self.assertEqual(s["stabilite"]["fidelite"], 0.3913)
        self.assertEqual(s["stabilite"]["jetons_identiques"], 46)
        self.assertEqual(s["controle_negatif_canonique"]["melange_exacts"], 0)
        self.assertEqual(s["controle_negatif_canonique"]["tronque_exacts"], 0)
        self.assertEqual(s["controle_negatif_canonique"]["detectes"], 46)
        self.assertEqual(s["controle_negatif_structure"]["eligibles"], 43)
        self.assertEqual(s["controle_negatif_structure"]["cle_changee"], 43)
        self.assertEqual(s["controle_negatif_structure"]["roles_retires"], 395)
        self.assertEqual(s["controle_negatif_structure"]["cibles_retirees"], 315)


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
