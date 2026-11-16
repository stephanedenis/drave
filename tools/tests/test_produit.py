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
            (5, 5),
            (sans_commande.returncode, langue_inconnue.returncode),
            detail(sans_commande) + detail(langue_inconnue),
        )

    def test_duree_dans_le_json(self) -> None:
        """T5 — `--duree` ajoute le temps de l'analyse, et lui seul."""
        sans = drave("analyser", "Le chat dort.", "--json")
        avec = drave("analyser", "Le chat dort.", "--json", "--duree")
        self.assertEqual(avec.returncode, 0, detail(avec))
        d_sans = json.loads(sans.stdout)
        d_avec = json.loads(avec.stdout)
        self.assertNotIn("duree_s", d_sans["cout"], detail(sans))
        self.assertIn("duree_s", d_avec["cout"], detail(avec))
        self.assertIsInstance(d_avec["cout"]["duree_s"], (int, float))
        self.assertGreaterEqual(d_avec["cout"]["duree_s"], 0.0)
        # la durée est le seul ajout : le texte et les étiquettes ne bougent pas
        self.assertEqual(d_sans["texte"], d_avec["texte"])
        self.assertEqual(d_sans["etiquettes"], d_avec["etiquettes"])

    def test_duree_jsonl(self) -> None:
        """T5 — `--duree` vaut aussi pour chaque ligne de `--jsonl`."""
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write("Le chat dort.\n\nLa voisine parle.\n")
            chemin = f.name
        try:
            sortie = drave("analyser", "--fichier", chemin, "--jsonl", "--duree")
            self.assertEqual(sortie.returncode, 0, detail(sortie))
            lignes = [json.loads(l) for l in sortie.stdout.splitlines() if l.strip()]
            self.assertEqual(len(lignes), 2, detail(sortie))
            for ligne in lignes:
                self.assertIn("duree_s", ligne["cout"], ligne)
        finally:
            pathlib.Path(chemin).unlink(missing_ok=True)

    def test_tableau_des_codes_dans_l_aide_et_la_notice(self) -> None:
        """T5 — le contrat des codes est écrit dans `--aide` et la notice."""
        aide = drave("--aide")
        self.assertEqual(aide.returncode, 0, detail(aide))
        self.assertIn("Codes de sortie", aide.stdout)
        for attendu in ("0 succès", "3 refus", "4 clé/dépendance", "5 usage"):
            self.assertIn(attendu, aide.stdout, detail(aide))
        notice = (RACINE / "docs" / "produit" / "README.md").read_text(encoding="utf-8")
        for code, sens in (("0", "succès"), ("3", "refus"), ("4", "dépendance"),
                           ("5", "usage")):
            ligne = re.search(rf"^\| \*\*{code}\*\* \|.*$", notice, re.MULTILINE)
            self.assertIsNotNone(ligne, f"ligne du code {code} absente de la notice")
            self.assertIn(sens, ligne.group(0), ligne.group(0))

    def test_aide_et_help_des_cinq_sous_commandes(self) -> None:
        """T5/U3 — `--aide` et `--help` répondent sur les cinq sous-commandes, code 0."""
        for commande in ("analyser", "evaluer", "profils", "rejouer", "restituer"):
            for drapeau in ("--aide", "--help"):
                sortie = drave(commande, drapeau)
                self.assertEqual(sortie.returncode, 0,
                                 f"{commande} {drapeau}\n" + detail(sortie))
                self.assertIn("usage:", sortie.stdout,
                              f"{commande} {drapeau}\n" + detail(sortie))
                self.assertIn(commande, sortie.stdout,
                              f"{commande} {drapeau}\n" + detail(sortie))

    def test_fichier_inexistant(self) -> None:
        """T5 — chemin inexistant : dépendance absente (4), message clair, pas de trace."""
        import tempfile
        dossier = tempfile.mkdtemp(prefix="drave-t5-")
        chemin = pathlib.Path(dossier) / "absent.txt"
        try:
            sortie = drave("analyser", "--fichier", str(chemin))
            self.assertEqual(sortie.returncode, 4, detail(sortie))
            self.assertEqual(sortie.stdout, "", detail(sortie))
            self.assertIn("fichier introuvable", sortie.stderr, detail(sortie))
            self.assertIn(str(chemin), sortie.stderr, detail(sortie))
            self.assertNotIn("Traceback", sortie.stderr, detail(sortie))
            self.assertNotIn("Traceback", sortie.stdout, detail(sortie))
        finally:
            pathlib.Path(dossier).rmdir()

    def test_fichier_repertoire(self) -> None:
        """T5 — répertoire : usage invalide (5), message clair, pas de trace."""
        import tempfile
        with tempfile.TemporaryDirectory(prefix="drave-t5-") as dossier:
            sortie = drave("analyser", "--fichier", dossier)
            self.assertEqual(sortie.returncode, 5, detail(sortie))
            self.assertEqual(sortie.stdout, "", detail(sortie))
            self.assertIn("répertoire", sortie.stderr, detail(sortie))
            self.assertIn(dossier, sortie.stderr, detail(sortie))
            self.assertNotIn("Traceback", sortie.stderr, detail(sortie))
            self.assertNotIn("Traceback", sortie.stdout, detail(sortie))


class TestContratJSON(unittest.TestCase):
    """T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés."""

    PHRASE = "Le livre que j'ai lu est intéressant."

    def test_candidats_attachement_en_objets(self) -> None:
        sortie = drave("analyser", self.PHRASE, "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        syntagmes = [e for e in d["etiquettes"] if e["niveau"] == "syntagme"]
        attaches = [e for e in syntagmes
                    if (e.get("meta") or {}).get("attachement")]
        self.assertTrue(attaches, "aucun attachement publié")
        for etiquette in attaches:
            attachement = etiquette["meta"]["attachement"]
            self.assertIn("candidats", attachement, etiquette["valeur"])
            self.assertTrue(attachement["candidats"], etiquette["valeur"])
            for candidat in attachement["candidats"]:
                self.assertEqual({"span", "cible", "source"}, set(candidat))
                self.assertEqual({"debut", "fin"}, set(candidat["span"]))
                debut, fin = candidat["span"]["debut"], candidat["span"]["fin"]
                self.assertTrue(0 <= debut < fin <= len(d["texte"]), candidat)
                self.assertEqual(d["texte"][debut:fin], candidat["cible"], candidat)
                self.assertEqual("heuristique", candidat["source"])
        # la sortie lisible garde les chaînes d'affichage (le champ historique)
        self.assertTrue(all(isinstance(c, str) for e in syntagmes for c in e["candidats"]))

    def test_candidat_negatif_absent_du_texte(self) -> None:
        """Un candidat sans span n'est pas publié : l'objet ne peut pas mentir sur sa position."""
        sortie = drave("analyser", "Le chat dort.", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        for etiquette in d["etiquettes"]:
            for candidat in (((etiquette.get("meta") or {}).get("attachement") or {})
                             .get("candidats", [])):
                debut, fin = candidat["span"]["debut"], candidat["span"]["fin"]
                self.assertEqual(d["texte"][debut:fin], candidat["cible"])
                self.assertNotIn("structure la plus proche", candidat["cible"])

    def test_roles_normalises_et_filtre_predicat(self) -> None:
        sys.path.insert(0, str(RACINE))
        from tools.roles_vocabulaire import ROLES
        sortie = drave("analyser", self.PHRASE, "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        roles = [(e.get("meta") or {}).get("role", "")
                 for e in d["etiquettes"] if e["niveau"] == "syntagme"]
        self.assertTrue(all(role in ("",) + ROLES for role in roles), roles)
        # contrôle négatif : l'ancienne forme accentuée n'est plus publiée
        self.assertNotIn("prédicat", roles)
        # le filtre du consommateur trouve les prédicats (et ce sont des GV)
        predicats = [e for e in d["etiquettes"]
                     if e["niveau"] == "syntagme"
                     and (e.get("meta") or {}).get("role") == "predicat"]
        self.assertTrue(predicats)
        self.assertTrue(any(e["type"] == "GV" for e in predicats))
        # et il n'en trouve aucun avec la forme brute
        self.assertFalse([e for e in d["etiquettes"]
                          if (e.get("meta") or {}).get("role") == "prédicat"])

    def test_role_hors_vocabulaire_refuse(self) -> None:
        sys.path.insert(0, str(RACINE))
        from tools.roles_vocabulaire import (ROLES, RoleHorsVocabulaire,
                                             normaliser_role)
        self.assertEqual("predicat", normaliser_role("prédicat"))
        self.assertEqual("predicat", normaliser_role("predicat"))
        self.assertEqual("qualite", normaliser_role("qualité"))
        self.assertEqual("objet", normaliser_role("patient"))
        self.assertEqual("possesseur", normaliser_role("possession"))
        self.assertEqual("destinataire", normaliser_role("but"))
        self.assertEqual("", normaliser_role(""))
        self.assertRaises(RoleHorsVocabulaire, normaliser_role, "role_invente")
        self.assertRaises(ValueError, normaliser_role, "prédicat-objets")
        # la table ne peut pas produire une valeur hors vocabulaire
        from tools.roles_vocabulaire import CORRESPONDANCES
        self.assertTrue(set(CORRESPONDANCES.values()) <= set(ROLES))


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



class TestPartition(unittest.TestCase):
    """La vue des syntagmes est un choix explicite (`--partition`)."""

    def test_filtrer_donne_une_vue_lineaire(self):
        sortie = drave("analyser", "Le chat de la voisine qui dort sur le toit se réveille.",
                      "--partition", "filtrer", "--json")
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        segs = [e for e in json.loads(sortie.stdout)["etiquettes"] if e["niveau"] == "syntagme"]
        self.assertTrue(segs)
        for a, b in zip(segs, segs[1:]):
            self.assertTrue(a["fin"] <= b["debut"], (a, b))

    def test_alternative_etiquette_les_chevauchements(self):
        sortie = drave("analyser", "Le chat de la voisine qui dort sur le toit se réveille.",
                      "--json")
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        segs = [e for e in json.loads(sortie.stdout)["etiquettes"] if e["niveau"] == "syntagme"]
        self.assertTrue(any("alternative" in (e.get("meta") or {}) for e in segs))


class TestContexte(unittest.TestCase):
    """Le contexte est un champ de première classe (mémoire de discours)."""

    def test_contexte_porte_dans_le_json(self):
        sortie = drave("analyser", "Il dort.", "--contexte", "Le chat est sur le toit.", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertEqual(json.loads(sortie.stdout)["contexte"], "Le chat est sur le toit.")


class TestSortieHostile(unittest.TestCase):
    """Un stdout ASCII ne doit pas faire planter l'en-tête (audit A26, hors banc)."""

    def test_stdout_ascii(self):
        import os
        env = dict(os.environ, PYTHONIOENCODING="ascii")
        sortie = subprocess.run(
            [sys.executable, str(RACINE / "tools/drave.py"), "analyser", "Le chat dort."],
            capture_output=True, text=True, env=env, cwd=str(RACINE))
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        self.assertIn("drave", sortie.stdout)

    def test_stdout_ascii_json(self):
        import os
        env = dict(os.environ, PYTHONIOENCODING="ascii")
        sortie = subprocess.run(
            [sys.executable, str(RACINE / "tools/drave.py"), "analyser",
             "Le chat de la voisine qui dort sur le toit se réveille.", "--json"],
            capture_output=True, text=True, env=env, cwd=str(RACINE))
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        self.assertEqual(json.loads(sortie.stdout)["schema"], "drave.annotation")


class TestDeuxVues(unittest.TestCase):
    """`evaluer` publie la vue fidèle **et** la vue linéaire (transparence)."""

    def test_deux_vues(self):
        sortie = drave("evaluer", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertIn("syntagmes_lineaire", d)
        self.assertGreaterEqual(d["syntagmes_lineaire"]["f1"], d["heuristique"]["syntagme"]["f1"])


class TestCorpus(unittest.TestCase):
    """`--fichier` et `--jsonl` : le traitement de corpus."""

    def test_fichier_et_jsonl(self):
        import tempfile, pathlib as _p
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Le chat dort.\n\nLa voisine parle au chat. Il dort encore.\n")
            chemin = f.name
        try:
            sortie = drave("analyser", "--fichier", chemin, "--jsonl")
            self.assertEqual(sortie.returncode, 0, detail(sortie))
            lignes = [json.loads(l) for l in sortie.stdout.splitlines() if l.strip()]
            self.assertEqual(len(lignes), 3)
            self.assertEqual(lignes[0]["schema"], "drave.annotation")
        finally:
            _p.Path(chemin).unlink(missing_ok=True)

    def test_fichier_seul(self):
        import tempfile, pathlib as _p
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Le chat dort.")
            chemin = f.name
        try:
            sortie = drave("analyser", "--fichier", chemin, "--json")
            self.assertEqual(sortie.returncode, 0, detail(sortie))
            self.assertIn("Le chat", json.loads(sortie.stdout)["texte"])
        finally:
            _p.Path(chemin).unlink(missing_ok=True)


class TestParLangue(unittest.TestCase):
    """`evaluer --par-langue` scinde la mesure fr/en sans la changer."""

    def test_par_langue_json(self) -> None:
        global_ = drave("evaluer", "--json")
        sortie = drave("evaluer", "--par-langue", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertEqual(global_.returncode, 0, detail(global_))
        d = json.loads(sortie.stdout)
        self.assertEqual({"fr", "en"}, set(d["par_langue"]))
        self.assertEqual(d["gold"]["phrases"],
                         sum(m["phrases"] for m in d["par_langue"].values()))
        for langue, m in d["par_langue"].items():
            self.assertGreater(m["phrases"], 0, langue)
            self.assertGreater(m["pos"]["tokens"], 0, langue)
            self.assertIn("controle_negatif", m, langue)
            # l'attachement par langue du rapport global et le sous-rapport coïncident
            attendu = d["heuristique"]["attachement"]["par_langue"][langue]
            self.assertEqual(attendu["cibles"], m["attachement"]["cibles"], langue)
            self.assertEqual(attendu["exact"], m["attachement"]["exact"], langue)
        # le drapeau ne change pas la mesure globale (contrôle de non-régression)
        self.assertEqual(json.loads(global_.stdout)["heuristique"], d["heuristique"])

    def test_par_langue_texte(self) -> None:
        sortie = drave("evaluer", "--par-langue")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        self.assertIn("PAR LANGUE", sortie.stdout)
        for langue in ("fr", "en"):
            self.assertIn(f"  {langue}  ", sortie.stdout)
        # le contrôle négatif est recalculé pour chaque langue, pas recopié
        self.assertEqual(3, sortie.stdout.count("CONTRÔLE NÉGATIF"))


class TestBaseReelle(unittest.TestCase):
    """La base honnête : `--reel` mesure les phrases réelles, sans le synthétique."""

    def test_reel_json(self):
        sortie = drave("evaluer", "--reel", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertIn("réel", d["gold"]["nom"])
        self.assertEqual(d["gold"]["phrases"], 452)

    def test_global_publie_la_base_reelle(self):
        sortie = drave("evaluer", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertIsNotNone(d.get("reel"))
        self.assertEqual(d["reel"]["phrases"], 452)
        self.assertLess(d["reel"]["phrases"], d["gold"]["phrases"])


if __name__ == "__main__":
    unittest.main()


class TestGenerer(unittest.TestCase):
    """`drave generer` : le natif en option, avec des refus propres (jamais de trace)."""

    def test_sans_torch_ou_sans_modele_code_4(self):
        # sans torch : 4 (dépendance) ; avec torch mais un checkpoint absent : 4 aussi
        sortie = drave("generer", "--modele", "/tmp/inexistant-xyz.pt", "--prompt", "x", "--n", "1")
        self.assertEqual(sortie.returncode, 4, detail(sortie))
        self.assertIn("absente", sortie.stderr + sortie.stdout)


if __name__ == "__main__":
    unittest.main()
