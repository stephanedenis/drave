"""test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.

Ce que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de
POS valide) :

1. la cascade remplace bien les POS par ceux du tagger (et garde les syntagmes de l'heuristique,
   avec leurs rôles et leurs cibles) ;
2. le JSON reste valide : le schéma **déclaré** (v2) le lit, et le contrat **v1** reste lisible ;
3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;
4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
5. les quatre cas d'erreur, chacun avec un transport factice :
   - **clé absente** → code **4**, message clair, `stdout` vide (`TestCle.test_sans_cle_code_4`) ;
   - **clé invalide** (HTTP 401/403) → code **4**, message clair, `stdout` vide, pas de repli ;
   - **réseau coupé** → **repli heuristique**, code **0**, `refus` non vide et message sur `stderr` ;
   - **refus du modèle** (texte non JSON, JSON incomplet) → **repli heuristique**, code **0**,
     `refus` non vide ;
6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`,
   puis `DEEPSEEK_API_KEY` ;
7. le mode **`--tagger auto`** (prototype, `TestTaggerAuto`) : les quatre cas — clé présente,
   clé invalide, clé absente, clé + réseau coupé — rendent **0** (ou **3** pour un refus de
   texte), `stderr` dit lequel a servi, et **sans clé** la sortie est identique au défaut.

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
from tools.llm.deepseek import DeepSeek, ErreurDeepSeek  # noqa: E402

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


def _env_sans_cle(home: pathlib.Path, **extra: str) -> dict[str, str]:
    """Un environnement sans aucune des sources de la clé, avec un `HOME` vide."""
    env = {cle: valeur for cle, valeur in os.environ.items()
           if cle not in {"DEEPSEEK_API_KEY", "DSH_API_KEY", "DEEPSEEK_KEY_FILE",
                          "DSH_KEY_FILE", "HOME"}
           and not cle.startswith("DEEPSEEK") and not cle.startswith("DSH_")}
    env["HOME"] = str(home)
    env.update(extra)
    return env


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
                         {(0, 2): "VERB", (3, 7): "DET", (8, 12): "ADV", (12, 13): "PONCT"})
        # l'heuristique, elle, dit DET/NOUN/VERB : la substitution est réelle. Le tagger ne
        # reçoit que les mots et les nombres ; le PONCT est restitué depuis l'heuristique.
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
        # **un seul** appel POS ; la seconde analyse est servie par le cache du tagger
        self.assertEqual(compteur["appels"], 1)
        self.assertEqual(premier.json(), second.json())
        self.assertEqual(cascade.n.appels, 1)

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
        self.assertEqual(_pos_map(donnees), {(0, 2): "VERB", (3, 7): "DET", (8, 12): "ADV", (12, 13): "PONCT"})
        self.assertEqual(donnees["source"], "cascade")
        self.assertIn("TAGGER API", erreur)
        self.assertEqual(self.client.demandes, 1)

    def test_analyser_tagger_lisible(self) -> None:
        code, sortie, erreur = self._lancer("analyser", TEXTE, "--tagger")
        self.assertEqual(code, 0, erreur)
        self.assertIn("analyse cascade POS (tagger API DeepSeek, réseau)", sortie)
        self.assertIn("TAGGER API", sortie)
        self.assertIn("Le/VERB chat/DET dort/ADV", sortie)
        self.assertEqual(self.client.demandes, 1)

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
        self.assertEqual(donnees["tagger"]["cout"]["appels"], 2)  # 2 phrases × 1 tagger
        self.assertEqual(donnees["tagger"]["cout"]["requetes"], 2)
        self.assertEqual(donnees["tagger"]["cout"]["tokens"], 34)
        self.assertEqual(donnees["tagger"]["refus"], 0)
        self.assertAlmostEqual(donnees["tagger"]["delta_pos"],
                               donnees["tagger"]["pos"]["exactitude"]
                               - donnees["heuristique"]["pos"]["exactitude"], places=4)
        self.assertIn("TAGGER API", erreur)


class TestErreursTagger(unittest.TestCase):
    """Les cas d'erreur de l'option, **sans réseau** : un client dont le transport échoue.

    Ce que chaque cas verrouille :

    - **clé invalide** : 401/403 n'est pas un refus de phrase ; le CLI sort **4**, `stdout`
      reste vide, le message nomme les trois sources de la clé ;
    - **réseau coupé** : le client réessaie (`essais=3`), puis la cascade **replie** sur
      l'heuristique ; code **0**, `refus` dans le JSON, message sur `stderr` ;
    - **refus du modèle** : la sortie n'est pas le contrat POS ; même repli, code **0**.

    La clé absente est couverte par `TestCle.test_sans_cle_code_4` (HOME vide, code 4).
    """

    def setUp(self) -> None:
        self._ancien_client = drave._client_tagger

    def tearDown(self) -> None:
        drave._client_tagger = self._ancien_client

    def _client(self, cache: str, transport, *, essais: int = 3) -> DeepSeek:
        return DeepSeek(cle="cle-de-test-sentinelle", transport=transport,
                        cache_dir=cache, sleep=lambda _: None, essais=essais)

    def _lancer(self, client, *arguments: str) -> tuple[int, str, str]:
        drave._client_tagger = lambda: client
        sortie, erreur = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreur):
            code = drave.main(list(arguments))
        return code, sortie.getvalue(), erreur.getvalue()

    def test_cle_invalide_code_4(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            def transport(*_args):
                raise ErreurDeepSeek("HTTP 401 : invalid key", code=401)

            client = self._client(tmp, transport)
            for arguments in (("analyser", TEXTE, "--tagger", "--json"),
                              ("evaluer", "--tagger", "--json")):
                code, sortie, erreur = self._lancer(client, *arguments)
                self.assertEqual(code, 4, f"{arguments} → {code} : {erreur}")
                self.assertEqual(sortie, "", "une clé refusée ne publie pas de repli")
                self.assertIn("clé DeepSeek refusée", erreur)
                self.assertIn("HTTP 401", erreur)
                self.assertIn("DEEPSEEK_KEY_FILE", erreur)
                self.assertIn("heuristique hors ligne", erreur)
                self.assertNotIn("cle-de-test-sentinelle", erreur)
                self.assertNotIn("TAGGER API", erreur)

    def test_reseau_coupe_repli_heuristique(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tentatives: list[int] = []

            def transport(*_args):
                tentatives.append(1)
                raise ErreurDeepSeek("réseau : [Errno -2] Name or service not known",
                                     reessayable=True)

            code, sortie, erreur = self._lancer(
                self._client(tmp, transport), "analyser", TEXTE, "--tagger", "--json")
            self.assertEqual(code, 0, erreur)
            self.assertEqual(len(tentatives), 3, "le client doit réessayer avant de replier")
            donnees = json.loads(sortie)
            self.assertIn("réseau", donnees["refus"])
            self.assertEqual(donnees["source"], "cascade")
            self.assertEqual(_pos_map(donnees),
                             _pos_map(bl.Heuristique().analyser(TEXTE).json()))
            self.assertEqual({e["source"] for e in donnees["etiquettes"]
                              if e["niveau"] == "pos"}, {"heuristique"})
            self.assertIn("refus partiel", erreur)
            self.assertIn("réseau", erreur)
            self.assertIn("TAGGER API", erreur)

    def test_refus_du_modele_repli_heuristique(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            def transport(*_args):
                return {"choices": [{"message": {"content": "Je ne peux pas répondre."}}],
                        "model": "deepseek-chat", "usage": {}}

            code, sortie, erreur = self._lancer(
                self._client(tmp, transport), "analyser", TEXTE, "--tagger", "--json")
            self.assertEqual(code, 0, erreur)
            donnees = json.loads(sortie)
            self.assertIn("pas de JSON", donnees["refus"])
            self.assertIn("Je ne peux pas répondre", donnees["refus"])
            self.assertEqual(donnees["source"], "cascade")
            self.assertEqual(_pos_map(donnees),
                             _pos_map(bl.Heuristique().analyser(TEXTE).json()))
            self.assertEqual({e["source"] for e in donnees["etiquettes"]
                              if e["niveau"] == "pos"}, {"heuristique"})
            self.assertIn("refus partiel", erreur)
            self.assertIn("pas de JSON", erreur)

    def test_modele_json_incomplet_repli_heuristique(self) -> None:
        """Un JSON qui n'a pas une classe par token est un refus de contrat, pas une exception."""
        with tempfile.TemporaryDirectory() as tmp:
            def transport(*_args):
                return {"choices": [{"message": {"content": '{"pos": ["DET"]}'}}],
                        "model": "deepseek-chat", "usage": {}}

            code, sortie, erreur = self._lancer(
                self._client(tmp, transport), "analyser", TEXTE, "--tagger", "--json")
            self.assertEqual(code, 0, erreur)
            donnees = json.loads(sortie)
            self.assertIn("longueur POS", donnees["refus"])
            self.assertEqual(_pos_map(donnees),
                             _pos_map(bl.Heuristique().analyser(TEXTE).json()))
            self.assertIn("refus partiel", erreur)


class TestMatriceW3(unittest.TestCase):
    """La matrice de W3 : le défaut hors ligne, le coût pour 1 000 phrases, zéro socket.

    Les autres lignes de la matrice ont déjà leur test : **avec clé**
    (`TestCliAvecTransportFactice.test_analyser_tagger_json`), **clé invalide**
    (`TestErreursTagger.test_cle_invalide_code_4`), **réseau coupé** et **repli**
    (`TestErreursTagger.test_reseau_coupe_repli_heuristique`,
    `test_refus_du_modele_repli_heuristique`, `test_modele_json_incomplet_repli_heuristique`).
    Ce bloc ajoute les deux lignes qui décident du défaut : sans clé, code **0** ; et le coût
    extrapolé à **1 000** phrases.
    """

    def _env_sans_cle(self, home: pathlib.Path) -> dict[str, str]:
        env = {cle: valeur for cle, valeur in os.environ.items()
               if cle not in {"DEEPSEEK_API_KEY", "DSH_API_KEY", "DEEPSEEK_KEY_FILE",
                              "DSH_KEY_FILE", "HOME"}
               and not cle.startswith("DEEPSEEK") and not cle.startswith("DSH_")}
        env["HOME"] = str(home)
        return env

    def test_defaut_sans_cle_code_0(self) -> None:
        """Sans clé, le défaut rend l'heuristique, code 0, et n'appelle jamais le tagger."""
        with tempfile.TemporaryDirectory() as tmp:
            env = self._env_sans_cle(pathlib.Path(tmp))
            analyse = drave_cli("analyser", TEXTE, "--json", env=env)
            self.assertEqual(analyse.returncode, 0, analyse.stderr)
            donnees = json.loads(analyse.stdout)
            self.assertEqual(donnees["source"], "heuristique")
            self.assertFalse(donnees["refus"])
            self.assertFalse([t for t in donnees["trace"]
                              if "neuronal" in str(t.get("etape"))])
            evaluation = drave_cli("evaluer", "--json", env=env)
            self.assertEqual(evaluation.returncode, 0, evaluation.stderr)
            self.assertEqual(evaluation.stderr, "")
            self.assertNotIn("tagger", json.loads(evaluation.stdout))

    def test_defaut_n_ouvre_aucune_socket(self) -> None:
        """Le défaut ne charge pas le client réseau et ne construit aucune socket."""
        code = (
            "import contextlib, io, socket, sys\n"
            "class Interdit(socket.socket):\n"
            "    def __init__(self, *a, **k):\n"
            "        raise RuntimeError('socket ouverte')\n"
            "socket.socket = Interdit\n"
            "sys.path.insert(0, 'tools')\n"
            "import drave\n"
            "with contextlib.redirect_stdout(io.StringIO()):\n"
            "    c = drave.main(['analyser', 'Le chat dort.', '--json'])\n"
            "print('CODE', c)\n"
            "print('DEEPSEEK', 'tools.llm.deepseek' in sys.modules)\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            env = self._env_sans_cle(pathlib.Path(tmp))
            resultat = subprocess.run(
                [sys.executable, "-c", code], cwd=str(RACINE), capture_output=True,
                text=True, encoding="utf-8", timeout=60, env=env)
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        self.assertIn("CODE 0", resultat.stdout)
        self.assertIn("DEEPSEEK False", resultat.stdout)

    def test_cout_pour_1000_phrases(self) -> None:
        """`evaluer --tagger` publie le coût linéaire pour 1 000 phrases."""
        client = _FauxClient()
        ancien_client = drave._client_tagger
        evaluateur = drave._module_evaluation()
        chargeur = evaluateur.charger
        # deux phrases **identiques** : le cache mémoire ne fait qu'un appel, mais le lot
        # mesuré fait bien **deux** phrases. L'extrapolation doit suivre les phrases, pas les
        # appels — c'est la différence 449 appels / 452 phrases de W2.
        premier = dict(chargeur()[0])
        second = dict(premier, id=str(premier.get("id", "")) + "-bis")
        evaluateur.charger = lambda: [premier, second]
        ancien_module = drave._module_evaluation
        drave._client_tagger = lambda: client
        drave._module_evaluation = lambda: evaluateur
        try:
            sortie, erreur = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreur):
                code = drave.main(["evaluer", "--tagger", "--json"])
        finally:
            drave._client_tagger = ancien_client
            drave._module_evaluation = ancien_module
            evaluateur.charger = chargeur
        self.assertEqual(code, 0, erreur.getvalue())
        donnees = json.loads(sortie.getvalue())
        self.assertEqual(donnees["tagger"]["cout"]["appels"], 1)
        self.assertEqual(donnees["tagger"]["cout"]["tokens"], 17)
        cout = donnees["tagger"]["cout_pour_1000_phrases"]
        self.assertEqual(cout["phrases"], 1000)
        self.assertEqual(cout["phrases_mesurees"], 2)
        self.assertEqual(cout["appels"], 500)     # 1 appel pour 2 phrases, × 500
        self.assertEqual(cout["requetes"], 500)
        self.assertEqual(cout["tokens"], 8500)    # 17 tokens pour 2 phrases, × 500
        self.assertEqual(cout["latence_s"], 0.0)


class TestTaggerAuto(unittest.TestCase):
    """Le prototype `--tagger auto` : API si clé, heuristique sinon, **sans code 4**.

    Les quatre cas de la fiche Y1 sont couverts ici, avec un client injecté (aucun socket) :

    - **clé absente** : sortie **identique au défaut**, code **0**, message `heuristique` ;
    - **clé présente** : cascade API, code **0**, POS neuronal, coût dans `TAGGER API` ;
    - **clé invalide** : repli heuristique, code **0** (pas 4), `refus` non vide ;
    - **clé + réseau coupé** : 3 essais, repli heuristique, code **0**, `refus` non vide.

    Le contrôle négatif principal est la paire `--tagger auto` / `--tagger` sur la **même**
    clé invalide : `auto` rend **0**, l'option explicite rend **4**.
    """

    SENTINELLE = "cle-de-test-sentinelle"

    def _lancer(self, client, *arguments: str) -> tuple[int, str, str]:
        ancien_client, ancien_cle = drave._client_tagger, drave._cle_tagger
        drave._client_tagger = lambda: client
        drave._cle_tagger = lambda: self.SENTINELLE
        sortie, erreur = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreur):
                code = drave.main(list(arguments))
        finally:
            drave._client_tagger, drave._cle_tagger = ancien_client, ancien_cle
        return code, sortie.getvalue(), erreur.getvalue()

    def _client_en_panne(self, cache: str, transport) -> DeepSeek:
        return DeepSeek(cle=self.SENTINELLE, transport=transport, cache_dir=cache,
                        sleep=lambda _: None, essais=3)

    def test_auto_sans_cle_identique_au_defaut(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = _env_sans_cle(pathlib.Path(tmp))
            defaut = drave_cli("analyser", TEXTE, "--json", env=env)
            auto = drave_cli("analyser", TEXTE, "--tagger", "auto", "--json", env=env)
        self.assertEqual(defaut.returncode, 0, defaut.stderr)
        self.assertEqual(auto.returncode, 0, auto.stderr)
        # le contrat : sans clé, `auto` **est** le défaut, octet pour octet
        self.assertEqual(auto.stdout, defaut.stdout)
        donnees = json.loads(auto.stdout)
        self.assertEqual(donnees, bl.Heuristique().analyser(TEXTE).json())
        self.assertEqual(donnees["source"], "heuristique")
        self.assertIn("tagger auto", auto.stderr)
        self.assertIn("heuristique", auto.stderr)
        self.assertIn("clé absente", auto.stderr)
        self.assertNotIn("401", auto.stderr)
        self.assertNotIn(self.SENTINELLE, auto.stderr)

    def test_auto_sans_cle_n_importe_pas_le_reseau(self) -> None:
        code = (
            "import contextlib, io, socket, sys\n"
            "class Interdit(socket.socket):\n"
            "    def __init__(self, *a, **k):\n"
            "        raise RuntimeError('socket ouverte')\n"
            "socket.socket = Interdit\n"
            "sys.path.insert(0, 'tools')\n"
            "import drave\n"
            "err = io.StringIO()\n"
            "with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):\n"
            "    c = drave.main(['analyser', 'Le chat dort.', '--tagger', 'auto', '--json'])\n"
            "print('CODE', c)\n"
            "print('DEEPSEEK', 'tools.llm.deepseek' in sys.modules)\n"
            "print('STDERR', err.getvalue().strip())\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            env = _env_sans_cle(pathlib.Path(tmp))
            resultat = subprocess.run(
                [sys.executable, "-c", code], cwd=str(RACINE), capture_output=True,
                text=True, encoding="utf-8", timeout=60, env=env)
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        self.assertIn("CODE 0", resultat.stdout)
        self.assertIn("DEEPSEEK False", resultat.stdout)
        self.assertIn("tagger auto", resultat.stdout)

    def test_auto_cle_presente_api(self) -> None:
        client = _FauxClient()
        code, sortie, erreur = self._lancer(
            client, "analyser", TEXTE, "--tagger", "auto", "--json")
        self.assertEqual(code, 0, erreur)
        donnees = json.loads(sortie)
        self.assertEqual(donnees["source"], "cascade")
        self.assertEqual(_pos_map(donnees),
                         {(0, 2): "VERB", (3, 7): "DET", (8, 12): "ADV", (12, 13): "PONCT"})
        self.assertIn("tagger auto · API", erreur)
        self.assertIn("TAGGER API", erreur)
        self.assertIn("tokens=17", erreur)
        self.assertEqual(client.demandes, 1)
        self.assertNotIn(self.SENTINELLE, erreur + sortie)

    def test_auto_cle_invalide_code_0_pas_4(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            def transport(*_args):
                raise ErreurDeepSeek("HTTP 401 : invalid key", code=401)

            client = self._client_en_panne(tmp, transport)
            code, sortie, erreur = self._lancer(
                client, "analyser", TEXTE, "--tagger", "auto", "--json")
            self.assertEqual(code, 0, erreur)
            donnees = json.loads(sortie)
            self.assertEqual(donnees["source"], "heuristique")
            self.assertIn("tagger auto", donnees["refus"])
            self.assertIn("clé refusée", donnees["refus"])
            self.assertEqual(_pos_map(donnees),
                             _pos_map(bl.Heuristique().analyser(TEXTE).json()))
            self.assertEqual({e["source"] for e in donnees["etiquettes"]
                              if e["niveau"] == "pos"}, {"heuristique"})
            self.assertIn("heuristique (repli", erreur)
            self.assertIn("401", erreur)
            self.assertIn("TAGGER API", erreur)
            self.assertNotIn(self.SENTINELLE, erreur + sortie)
            # contrôle négatif : la **même** clé invalide, en explicite, sort 4 et stdout vide
            code_api, sortie_api, erreur_api = self._lancer(
                client, "analyser", TEXTE, "--tagger", "--json")
            self.assertEqual(code_api, 4, erreur_api)
            self.assertEqual(sortie_api, "")
            self.assertIn("clé DeepSeek refusée", erreur_api)

    def test_auto_reseau_coupe_code_0(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tentatives: list[int] = []

            def transport(*_args):
                tentatives.append(1)
                raise ErreurDeepSeek("réseau : [Errno -2] Name or service not known",
                                     reessayable=True)

            client = self._client_en_panne(tmp, transport)
            code, sortie, erreur = self._lancer(
                client, "analyser", TEXTE, "--tagger", "auto", "--json")
            self.assertEqual(code, 0, erreur)
            self.assertEqual(len(tentatives), 3, "le client doit réessayer avant de replier")
            donnees = json.loads(sortie)
            self.assertEqual(donnees["source"], "heuristique")
            self.assertIn("réseau", donnees["refus"])
            self.assertEqual(_pos_map(donnees),
                             _pos_map(bl.Heuristique().analyser(TEXTE).json()))
            self.assertEqual({e["source"] for e in donnees["etiquettes"]
                              if e["niveau"] == "pos"}, {"heuristique"})
            self.assertIn("heuristique (repli", erreur)
            self.assertIn("réseau", erreur)
            self.assertIn("TAGGER API", erreur)
            self.assertNotIn(self.SENTINELLE, erreur + sortie)

    def test_auto_refus_du_modele_repli(self) -> None:
        """Un modèle qui ne rend pas le contrat POS est un repli, pas un code 4."""
        with tempfile.TemporaryDirectory() as tmp:
            def transport(*_args):
                return {"choices": [{"message": {"content": "Je ne peux pas répondre."}}],
                        "model": "deepseek-chat", "usage": {}}

            client = self._client_en_panne(tmp, transport)
            code, sortie, erreur = self._lancer(
                client, "analyser", TEXTE, "--tagger", "auto", "--json")
            self.assertEqual(code, 0, erreur)
            donnees = json.loads(sortie)
            self.assertEqual(donnees["source"], "heuristique")
            self.assertIn("pas de JSON", donnees["refus"])
            self.assertIn("heuristique (repli", erreur)
            self.assertIn("TAGGER API", erreur)
            self.assertNotIn(self.SENTINELLE, erreur + sortie)

    def test_auto_refus_texte_code_3(self) -> None:
        client = _FauxClient()
        code, sortie, erreur = self._lancer(
            client, "analyser", "... !!! ???", "--tagger", "auto", "--json")
        self.assertEqual(code, 3, erreur)
        self.assertEqual(client.demandes, 0, "un refus de texte ne paie pas d'appel API")
        self.assertEqual(json.loads(sortie)["refus"], "vide")
        self.assertIn("tagger auto", erreur)
        self.assertIn("heuristique", erreur)

    def test_auto_texte_apres_le_drapeau(self) -> None:
        """`--tagger auto TEXTE` ne doit pas avaler le texte comme une valeur de `--tagger`."""
        with tempfile.TemporaryDirectory() as tmp:
            env = _env_sans_cle(pathlib.Path(tmp))
            defaut = drave_cli("analyser", TEXTE, "--json", env=env)
            auto = drave_cli("analyser", "--tagger", "auto", TEXTE, "--json", env=env)
        self.assertEqual(auto.returncode, 0, auto.stderr)
        self.assertEqual(auto.stdout, defaut.stdout)

    def test_auto_evaluer_rejete_en_usage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = _env_sans_cle(pathlib.Path(tmp))
            resultat = drave_cli("evaluer", "--tagger", "auto", env=env)
        self.assertEqual(resultat.returncode, 2, resultat.stderr)
        self.assertIn("n'est disponible que pour analyser", resultat.stderr)


def _pos_map(donnees: dict) -> dict[tuple[int, int], str]:
    return {(e["debut"], e["fin"]): e["type"] for e in donnees["etiquettes"]
            if e["niveau"] == "pos"}


if __name__ == "__main__":
    unittest.main(verbosity=2)
