"""test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.

Ce que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de
POS valide) :

1. la cascade remplace bien les POS par ceux du tagger (et garde les syntagmes de l'heuristique,
   avec leurs rôles et leurs cibles) ;
2. le JSON reste valide : le schéma **déclaré** (v2) le lit, et le contrat **v1** reste lisible ;
3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;
4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
5. sans clé, `--tagger` sort **4** avec un message clair, et jamais la clé ;
6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`,
   puis `DEEPSEEK_API_KEY`.

Aucun test n'ouvre de socket : les transports sont injectés, et le test « sans clé » lance la
commande dans un `HOME` vide. Le fichier passe par `python3 tools/tests/test_tagger_api.py`
comme par `pytest`.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools"))

import bloc_linguistique as bl  # noqa: E402
import drave  # noqa: E402

TEXTE = "Le chat dort."
TOKENS = ["Le", "chat", "dort"]
# Volontairement **faux** : le POS de l'heuristique est DET/NOUN/VERB, donc la substitution se
# voit. BIO valide (3 tokens) pour que le tagger de syntagmes ne refuse pas.
POS_FACTICE = ["VERB", "DET", "ADV"]
BIO_FACTICE = ["B-GN", "I-GN", "B-GV"]


def drave_cli(*arguments: str, env: dict[str, str] | None = None,
              timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE), capture_output=True, text=True, encoding="utf-8",
        timeout=timeout, env=env,
    )


def _tokens_de_invite(invite: str) -> list[str]:
    """Les tokens sont la **dernière** ligne `Tokens : [...]` de l'invite."""
    marque = "Tokens : "
    debut = invite.rindex(marque) + len(marque)
    fin = invite.index("\nRéponse :", debut)
    return json.loads(invite[debut:fin])


def _cycle(valeurs: list[str], n: int) -> list[str]:
    return (valeurs * (n // len(valeurs) + 1))[:n]


def transport_factice(invite: str, _grammaire: str, _max_jetons: int) -> str:
    """Un POS/BIO valide, de la bonne longueur, sans réseau ni modèle."""
    tokens = _tokens_de_invite(invite)
    if '"bio"' in invite:
        return json.dumps({"bio": _cycle(BIO_FACTICE, len(tokens))})
    return json.dumps({"pos": _cycle(POS_FACTICE, len(tokens))})


def _pos(annotation: bl.Annotation) -> dict[tuple[int, int], str]:
    return {(e.debut, e.fin): e.type for e in annotation.etiquettes if e.niveau == "pos"}


class _FauxClient:
    """Le client minimal attendu par `_transport_tagger` : `.demande` → réponse."""

    def __init__(self) -> None:
        self.demandes = 0
        self.tokens = 0

    def demande(self, prompt: str, **_kwargs) -> SimpleNamespace:
        self.demandes += 1
        self.tokens += 17
        return SimpleNamespace(contenu=transport_factice(prompt, "", 0),
                               usage={"total_tokens": 17}, latence_s=0.0,
                               cache=False, modele="deepseek-chat")


class TestCascadeTagger(unittest.TestCase):
    """Le câblage : cascade, POS, JSON, cache — sans clé et sans réseau."""

    def test_cascade_remplace_les_pos(self) -> None:
        cascade = drave._cascade_tagger(transport_factice)
        annotation = cascade.analyser(TEXTE, "fr")
        self.assertEqual(annotation.source, "cascade")
        self.assertEqual(_pos(annotation),
                         {(0, 2): "VERB", (3, 7): "DET", (8, 12): "ADV"})
        # l'heuristique, elle, dit DET/NOUN/VERB : la substitution est réelle. Le tagger ne
        # reçoit que les mots et les nombres : la ponctuation (PONCT) n'est pas rendue.
        heuristique = {span: classe for span, classe in _pos(bl.Heuristique().analyser(TEXTE, "fr")).items()
                       if classe != "PONCT"}
        self.assertEqual(heuristique, {(0, 2): "DET", (3, 7): "NOUN", (8, 12): "VERB"})
        # les syntagmes restent ceux de l'heuristique : rôle et cible conservés
        syntagmes = {(e.type, e.debut, e.fin): e for e in annotation.etiquettes
                     if e.niveau == "syntagme"}
        self.assertIn(("GN", 0, 7), syntagmes)
        self.assertEqual((syntagmes[("GN", 0, 7)].meta.get("attachement") or {}).get("cible"),
                         "dort")
        self.assertEqual(syntagmes[("GN", 0, 7)].meta.get("role"), "agent")
        self.assertIn("neuronal-pos", {t.get("etape") for t in annotation.trace})

    def test_json_valide_schema(self) -> None:
        annotation = drave._cascade_tagger(transport_factice).analyser(TEXTE, "fr")
        donnees = annotation.json()
        self.assertEqual(donnees["schema"], "drave.annotation")
        self.assertIn(donnees["version"], (1, 2))
        try:
            import fastjsonschema
        except ImportError:  # pragma: no cover — le dépôt n'exige pas le paquet
            fastjsonschema = None
        schemas = {v: json.loads((RACINE / "tools" / "schemas" /
                                  f"drave-annotation-v{v}.json").read_text(encoding="utf-8"))
                   for v in (1, 2)}
        if fastjsonschema is not None:
            fastjsonschema.compile(schemas[donnees["version"]])(donnees)
            # rétro-compatibilité : le contrat v1 reste lisible une fois les champs v2 retirés
            v1 = copy.deepcopy(donnees)
            v1["version"] = 1
            for etiquette in v1["etiquettes"]:
                meta = etiquette.get("meta")
                if isinstance(meta, dict):
                    meta.pop("partition", None)
                    meta.pop("alternative", None)
            fastjsonschema.compile(schemas[1])(v1)
        for etiquette in donnees["etiquettes"]:
            for cle in ("niveau", "type", "valeur", "debut", "fin", "source", "confiance"):
                self.assertIn(cle, etiquette)

    def test_cache_par_texte(self) -> None:
        compteur = {"appels": 0}

        def transport(invite: str, grammaire: str, max_jetons: int) -> str:
            compteur["appels"] += 1
            return transport_factice(invite, grammaire, max_jetons)

        cascade = drave._cascade_tagger(transport)
        premier = cascade.analyser(TEXTE, "fr")
        second = cascade.analyser(TEXTE, "fr")
        # 1 appel POS + 1 appel BIO ; la seconde analyse est servie par le cache des taggers
        self.assertEqual(compteur["appels"], 2)
        self.assertEqual(premier.json(), second.json())
        self.assertEqual(cascade.n.pos.appels, 1)
        self.assertEqual(cascade.n.chunks.appels, 1)

    def test_transport_invalide_ne_fait_pas_planter(self) -> None:
        """Un tagger qui rend autre chose qu'un JSON est un refus, pas une exception."""
        cascade = drave._cascade_tagger(lambda *_: "pas du JSON")
        annotation = cascade.analyser(TEXTE, "fr")
        self.assertIn("neuronal", annotation.refus)
        self.assertEqual(annotation.json()["schema"], "drave.annotation")


class TestDefaultInchange(unittest.TestCase):
    """Sans `--tagger`, la sortie est exactement celle de l'heuristique."""

    def test_analyser_json_sans_tagger(self) -> None:
        resultat = drave_cli("analyser", TEXTE, "--json")
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        donnees = json.loads(resultat.stdout)
        self.assertEqual(donnees, bl.Heuristique().analyser(TEXTE).json())
        self.assertEqual(donnees["source"], "heuristique")
        self.assertFalse([t for t in donnees["trace"] if "neuronal" in str(t.get("etape"))])

    def test_evaluer_sans_tagger(self) -> None:
        resultat = drave_cli("evaluer", "--json")
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        donnees = json.loads(resultat.stdout)
        self.assertNotIn("tagger", donnees)
        self.assertGreaterEqual(donnees["gold"]["phrases"], 20)

    def test_aide_expose_tagger(self) -> None:
        resultat = drave_cli("analyser", "--aide")
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        self.assertIn("--tagger", resultat.stdout)


class TestCle(unittest.TestCase):
    """La clé : ordre de résolution, code 4, et aucune trace dans les sorties."""

    def _env_propre(self, home: pathlib.Path, **extra: str) -> dict[str, str]:
        env = {cle: valeur for cle, valeur in os.environ.items()
               if cle not in {"DEEPSEEK_API_KEY", "DSH_API_KEY", "DEEPSEEK_KEY_FILE",
                              "DSH_KEY_FILE", "HOME"}
               and not cle.startswith("DEEPSEEK") and not cle.startswith("DSH_")}
        env["HOME"] = str(home)
        env.update(extra)
        return env

    def test_sans_cle_code_4(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = self._env_propre(pathlib.Path(tmp))
            for commande in (("analyser", TEXTE, "--tagger"),
                             ("evaluer", "--tagger")):
                resultat = drave_cli(*commande, env=env)
                self.assertEqual(resultat.returncode, 4,
                                 f"{commande} → {resultat.returncode} : {resultat.stderr}")
                self.assertIn("clé DeepSeek absente", resultat.stderr)
                self.assertIn("heuristique hors ligne", resultat.stderr)
                self.assertEqual(resultat.stdout, "")

    def test_absence_de_cle_ne_fuit_pas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = self._env_propre(pathlib.Path(tmp))
            resultat = drave_cli("analyser", TEXTE, "--tagger", env=env)
            self.assertNotIn("Bearer", resultat.stderr)
            self.assertNotIn("Authorization", resultat.stderr)

    def test_ordre_de_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            home = tmp / "home"
            (home / ".config" / "drave").mkdir(parents=True)
            (home / ".config" / "drave" / "deepseek.key").write_text("cle-maison\n",
                                                                     encoding="utf-8")
            explicite = tmp / "explicite.key"
            explicite.write_text("cle-fichier\n", encoding="utf-8")
            with mock.patch.dict(os.environ, {
                    "HOME": str(home),
                    "DEEPSEEK_KEY_FILE": str(explicite),
                    "DEEPSEEK_API_KEY": "cle-env"}, clear=True):
                self.assertEqual(drave._cle_tagger(), "cle-fichier")
            with mock.patch.dict(os.environ, {
                    "HOME": str(home), "DEEPSEEK_API_KEY": "cle-env"}, clear=True):
                self.assertEqual(drave._cle_tagger(), "cle-maison")
            vide = tmp / "vide"
            vide.mkdir()
            with mock.patch.dict(os.environ, {
                    "HOME": str(vide), "DEEPSEEK_API_KEY": "cle-env"}, clear=True):
                self.assertEqual(drave._cle_tagger(), "cle-env")

    def test_la_cle_ne_sort_pas_du_client(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fichier = pathlib.Path(tmp) / "cle.key"
            fichier.write_text("cle-secrete-sentinelle\n", encoding="utf-8")
            with mock.patch.dict(os.environ, {"DEEPSEEK_KEY_FILE": str(fichier)}, clear=True):
                client = drave._client_tagger()
            self.assertTrue(client.disponible())
            self.assertNotIn("cle-secrete-sentinelle", repr(client))


class TestCliAvecTransportFactice(unittest.TestCase):
    """La CLI de bout en bout, client injecté : le chemin `--tagger` et son coût."""

    def setUp(self) -> None:
        self.client = _FauxClient()
        self._ancien_client = drave._client_tagger
        drave._client_tagger = lambda: self.client

    def tearDown(self) -> None:
        drave._client_tagger = self._ancien_client

    def _lancer(self, *arguments: str) -> tuple[int, str, str]:
        sortie, erreur = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreur):
            code = drave.main(list(arguments))
        return code, sortie.getvalue(), erreur.getvalue()

    def test_analyser_tagger_json(self) -> None:
        code, sortie, erreur = self._lancer("analyser", TEXTE, "--tagger", "--json")
        self.assertEqual(code, 0, erreur)
        donnees = json.loads(sortie)
        self.assertEqual(_pos_map(donnees), {(0, 2): "VERB", (3, 7): "DET", (8, 12): "ADV"})
        self.assertEqual(donnees["source"], "cascade")
        self.assertIn("TAGGER API", erreur)
        self.assertEqual(self.client.demandes, 2)

    def test_analyser_tagger_lisible(self) -> None:
        code, sortie, erreur = self._lancer("analyser", TEXTE, "--tagger")
        self.assertEqual(code, 0, erreur)
        self.assertIn("analyse cascade POS (tagger API DeepSeek, réseau)", sortie)
        self.assertIn("TAGGER API", sortie)
        self.assertIn("Le/VERB chat/DET dort/ADV", sortie)
        self.assertEqual(self.client.demandes, 2)

    def test_evaluer_tagger(self) -> None:
        evaluateur = drave._module_evaluation()
        chargeur = evaluateur.charger
        evaluateur.charger = lambda: chargeur()[:2]
        ancien_module = drave._module_evaluation
        drave._module_evaluation = lambda: evaluateur
        try:
            code, sortie, erreur = self._lancer("evaluer", "--tagger", "--json")
        finally:
            drave._module_evaluation = ancien_module
        self.assertEqual(code, 0, erreur)
        donnees = json.loads(sortie)
        self.assertIn("tagger", donnees)
        self.assertIn("heuristique", donnees)  # la comparaison est toujours publiée
        self.assertEqual(donnees["tagger"]["cout"]["appels"], 4)  # 2 phrases × 2 taggers
        self.assertEqual(donnees["tagger"]["cout"]["requetes"], 4)
        self.assertEqual(donnees["tagger"]["cout"]["tokens"], 68)
        self.assertEqual(donnees["tagger"]["refus"], 0)
        self.assertAlmostEqual(donnees["tagger"]["delta_pos"],
                               donnees["tagger"]["pos"]["exactitude"]
                               - donnees["heuristique"]["pos"]["exactitude"], places=4)
        self.assertIn("TAGGER API", erreur)


def _pos_map(donnees: dict) -> dict[tuple[int, int], str]:
    return {(e["debut"], e["fin"]): e["type"] for e in donnees["etiquettes"]
            if e["niveau"] == "pos"}


if __name__ == "__main__":
    unittest.main(verbosity=2)
