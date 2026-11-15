#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**restitution v0** (annotation → surface, avec la fidélité du miroir) et la **v2** (rôles
agent/prédicat/lieu lisibles). La restitution est un **codec de surface** : elle reconstruit
depuis le niveau `graphème`, pas un décodeur neuronal.
En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
l'API DeepSeek : la clé est lue dans `DEEPSEEK_KEY_FILE`, `~/.config/drave/deepseek.key` puis
`DEEPSEEK_API_KEY` ; le cache du client évite de refaire un appel ; la clé n'est jamais affichée.
`analyser --tagger auto` choisit : API si une clé existe, heuristique sinon, **sans jamais
changer le code de sortie** (0 dans les deux cas, 3 pour un refus) ; `stderr` dit lequel a servi,
et la ligne `TAGGER API` porte le coût de l'appel quand il a eu lieu. Le mode `auto` est un
**prototype** : il ne change pas le défaut, qui reste l'heuristique hors ligne.
**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
Ce que la commande n'expose pas : le neuronal local (`llama-cli` ou endpoint), la traduction et la
génération : ils demandent des poids, un service ou un GPU.

Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
(absente ou refusée) · 1 erreur.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import sys
import textwrap

# Le dépôt d'abord — `sys.path.insert(0, '.')` quand on lance depuis sa racine, et les chemins
# déduits du fichier pour que la commande marche aussi depuis un autre répertoire. Aucun paquet
# externe n'est importé : le point d'entrée est autonome.
sys.path.insert(0, ".")
RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(RACINE))

import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)
import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
import restitution_v2  # noqa: E402  (la restitution v2 : les rôles)
import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)

NOM = "drave"
VERSION = "0.1.0"
LARGEUR = 100

# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
MODELE_TAGGER = "deepseek-chat"
SEUIL_TAGGER = 0.6
# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
# pas les syntagmes du neuronal (`PRIORITE_NIVEAU` le ferait) parce qu'ils n'ont ni rôle ni
# cible : l'attachement mesuré du produit serait perdu. Le gain mesuré porte sur le POS.
PRIORITE_TAGGER = dict(bl.PRIORITE_NIVEAU)
PRIORITE_TAGGER["syntagme"] = "heuristique"


# --------------------------------------------------------------------------- sorties JSON


def _sur(s: str) -> str:
    """Une chaîne toujours **écrivable** : un surrogate isolé devient U+FFFD (jamais d'exception)."""
    return s.encode("utf-8", "replace").decode("utf-8", "replace")


def _dumps(objet) -> str:
    """JSON stable (pas d'horodatage, pas de durée) et lisible."""
    return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"


def _canonique(a: bl.Annotation) -> str:
    """La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles."""
    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


# --------------------------------------------------------------------------- le tagger (option)


class CleTaggerAbsente(RuntimeError):
    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""


class CleTaggerRefusee(RuntimeError):
    """L'API refuse la clé (HTTP 401/403) : ce n'est pas un refus de phrase, c'est un arrêt.

    Une clé absente et une clé refusée sont la même dépendance manquante du point de vue du
    produit : le code 4, un message qui nomme les trois sources de la clé, et rien sur `stdout`.
    """

    def __init__(self, code: int) -> None:
        self.code = int(code)
        super().__init__(
            f"clé DeepSeek refusée (HTTP {self.code}) : vérifiez DEEPSEEK_KEY_FILE, "
            f"~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. "
            f"Sans --tagger, le défaut reste l'heuristique hors ligne."
        )


def _lire_cle(chemin: pathlib.Path) -> str:
    try:
        return chemin.read_text(encoding="utf-8").splitlines()[0].strip()
    except (OSError, IndexError):
        return ""


def _cle_tagger() -> str:
    """La clé, dans l'ordre du chantier — jamais rendue, jamais journalisée, jamais affichée."""
    for variable in ("DEEPSEEK_KEY_FILE", "DSH_KEY_FILE"):
        chemin = os.environ.get(variable)
        if chemin:
            cle = _lire_cle(pathlib.Path(chemin).expanduser())
            if cle:
                return cle
    cle = _lire_cle(pathlib.Path.home() / ".config" / "drave" / "deepseek.key")
    if cle:
        return cle
    for variable in ("DEEPSEEK_API_KEY", "DSH_API_KEY"):
        valeur = (os.environ.get(variable) or "").strip()
        if valeur:
            return valeur
    raise CleTaggerAbsente(
        "clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans "
        "~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. "
        "Sans --tagger, le défaut reste l'heuristique hors ligne."
    )


def _client_tagger():
    """Le client de l'API. L'import est **local** : le défaut ne charge pas le module réseau."""
    from tools.llm.deepseek import DeepSeek
    return DeepSeek(cle=_cle_tagger())


def _cle_tagger_presente() -> bool:
    """Vrai si une clé est trouvée — sans importer le module réseau et sans l'afficher."""
    try:
        _cle_tagger()
    except CleTaggerAbsente:
        return False
    return True


def _sans_secret(message: str) -> str:
    """Retire la clé d'un message de diagnostic si elle y apparaissait par accident."""
    try:
        cle = _cle_tagger()
    except CleTaggerAbsente:
        return message
    if cle and cle in message:
        return message.replace(cle, "<clé>")
    return message


class _TaggerAuto:
    """Le mode `auto` du tagger : API si une clé existe, heuristique sinon.

    Ce qu'il garantit :

    - **aucun code 4** : une clé refusée (401/403) ou un réseau coupé n'arrête pas le run ;
      l'analyse est rendue par l'heuristique, code 0, avec la cause dans `refus` ;
    - **aucun appel réseau sans clé** : la cascade n'est même pas construite ;
    - **la même analyse que le défaut** quand aucune clé n'existe : l'annotation sort de
      `Heuristique.analyser`, sans `refus` ajouté et sans source modifiée ;
    - un **message** (`message()`) qui dit lequel a servi, sans jamais nommer la clé.

    Le mode est un **prototype** : il ne change pas le défaut, qui reste l'heuristique.
    """

    nom = "auto"

    def __init__(self, heuristique: bl.Heuristique, cascade=None, stats: dict | None = None):
        self.h = heuristique
        self.cascade = cascade
        self.stats = stats
        self.cle_presente = cascade is not None
        self.api_servie = 0
        self.replis = 0
        self.cause = ""
        # une fois la panne constatée, on ne rappelle plus l'API pour les phrases suivantes
        self.panne = False

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> bl.Annotation:
        if self.cascade is not None and not self.panne:
            try:
                annotation = self.cascade.analyser(texte, langue, contexte)
            except CleTaggerRefusee as exc:
                self.panne = True
                self.cause = f"clé refusée (HTTP {exc.code})"
                return self._heuristique(texte, langue, contexte)
            if not annotation.refus:
                self.api_servie += 1
                return annotation
            if not annotation.refus.startswith("neuronal"):
                # refus du texte (vide, non texte) : ce n'est pas une panne du tagger
                return annotation
            self.panne = True
            self.cause = annotation.refus
        return self._heuristique(texte, langue, contexte)

    def _heuristique(self, texte: str, langue: str | None,
                     contexte: str | None) -> bl.Annotation:
        annotation = self.h.analyser(texte, langue, contexte)
        if annotation.refus:
            # le texte lui-même est refusé : le code 3 reste celui de l'analyse
            return annotation
        self.replis += 1
        if self.cause:
            annotation.refus = _sans_secret(
                f"tagger auto : {self.cause} ; heuristique")
        return annotation

    def message(self) -> str:
        """Le message `stderr` : lequel a servi, et pourquoi, sans la clé."""
        if self.cascade is None:
            if self.cle_presente:
                return "heuristique (clé présente ; refus du texte, aucun appel)"
            return "heuristique (clé absente)"
        if self.cause:
            if self.api_servie:
                return (f"API (clé présente) puis heuristique sur {self.replis} phrase(s) "
                        f"(repli : {_sans_secret(self.cause)})")
            return f"heuristique (repli : {_sans_secret(self.cause)})"
        if self.api_servie:
            appels = (self.stats or {}).get("appels", 0)
            if appels:
                return "API (clé présente)"
            return "API disponible (clé présente) ; non appelée (heuristique suffisante)"
        return "heuristique"

    def titre(self) -> str:
        """Le titre de la sortie lisible : il dit la voie qui a réellement servi."""
        if self.cascade is None:
            return f"{NOM} {VERSION} — analyse heuristique (CPU, hors ligne)"
        if self.cause:
            return (f"{NOM} {VERSION} — analyse heuristique "
                    f"(tagger auto : repli après échec de l'API)")
        if (self.stats or {}).get("appels", 0):
            return f"{NOM} {VERSION} — analyse cascade POS (tagger auto : API DeepSeek, réseau)"
        return f"{NOM} {VERSION} — analyse heuristique (tagger auto : API disponible, non appelée)"


def _transport_tagger(client, stats: dict):
    """Le transport attendu par les taggers : invite → contenu, avec le coût mesuré."""

    def transport(invite: str, _grammaire: str, max_jetons: int) -> str:
        stats["appels"] += 1
        try:
            reponse = client.demande(invite, temperature=0.0,
                                     max_tokens=max(64, int(max_jetons or 256)))
        except Exception as exc:  # noqa: BLE001 — le code HTTP décide du destin de l'option
            # 401/403 : la clé est refusée, aucune phrase ne peut être taguée. On retient le
            # code pour que `_CascadeTagger` arrête le run au lieu de publier un repli muet.
            code = getattr(exc, "code", None)
            if code in (401, 403):
                stats["cle_refusee"] = int(code)
            raise
        if getattr(reponse, "cache", False):
            stats["cache"] += 1
        else:
            usage = reponse.usage if isinstance(reponse.usage, dict) else {}
            stats["requetes"] += 1
            stats["tokens"] += int(usage.get("total_tokens", 0) or 0)
            stats["latence_s"] += float(getattr(reponse, "latence_s", 0.0) or 0.0)
        modele = getattr(reponse, "modele", None)
        if modele:
            stats["modeles"][modele] = stats["modeles"].get(modele, 0) + 1
        return reponse.contenu

    return transport


class _CascadeTagger:
    """La cascade du tagger, avec le **refus** du neuronal reporté sur l'annotation fusionnée.

    `bl.Cascade`/`_fusion` ne recopie pas `refus` : sans ce relais, un tagger qui échoue
    rendrait une annotation muette (POS absents, `refus` vide). Le composite est rappelé après
    la fusion ; ses taggers ont un cache, donc **aucun appel réseau supplémentaire**.
    """

    nom = "cascade"

    def __init__(self, cascade, compose, stats: dict | None = None):
        self.cascade = cascade
        self.compose = compose
        self.stats = stats if stats is not None else {}
        self.h = cascade.h
        self.n = cascade.n

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> bl.Annotation:
        annotation = self.cascade.analyser(texte, langue, contexte)
        # 401/403 : le tagger a échoué pour une raison qui ne dépend pas de la phrase. On ne
        # publie pas un repli heuristique déguisé en cascade : le CLI sort 4, stdout vide.
        code = self.stats.get("cle_refusee")
        if code:
            raise CleTaggerRefusee(int(code))
        if not annotation.refus:
            annotation.refus = self.compose.analyser(texte, langue, contexte).refus
        # le tagger ne reçoit que mots et nombres : la **ponctuation** est restituée depuis
        # l'heuristique (sinon `PONCT` disparaît du POS de l'option).
        deja = {(e.debut, e.fin) for e in annotation.etiquettes if e.niveau == "pos"}
        for e in self.h.analyser(texte, langue, contexte).etiquettes:
            if e.niveau == "pos" and (e.debut, e.fin) not in deja:
                annotation.etiquettes.append(e)
                annotation.etiquettes.sort(key=lambda x: (x.debut, x.fin, x.niveau))
        return annotation


def _cascade_tagger(transport, partition: str = "alternative", stats: dict | None = None):
    """Le câblage mesuré : tagger POS + syntagmes → compose → cascade à 0,6.

    `transport` est injectable : les tests le remplacent par une fonction qui rend un JSON de
    POS valide, sans réseau. La fusion ne force que le **POS** au neuronal ; les syntagmes,
    rôles et attachements restent à l'heuristique (le neuronal n'en rend pas). `stats` porte le
    drapeau `cle_refusee` (401/403) qui arrête le run au lieu de le replier.
    """
    # **un seul** tagger : le POS. Le tagger de syntagmes du composite était appelé et sa
    # sortie **n'était pas utilisée** par la fusion (le niveau syntagme reste à l'heuristique) :
    # le retirer divise le coût par deux (2 appels → 1 par phrase).
    pos = bl.NeuronalLLMPOS(MODELE_TAGGER, transport=transport)
    cascade = bl.Cascade(bl.Heuristique(partition=partition), pos, seuil=SEUIL_TAGGER,
                         priorite_syntagme="confiance", priorite_par_niveau=PRIORITE_TAGGER)
    return _CascadeTagger(cascade, pos, stats=stats)


def _construire_tagger(partition: str = "alternative"):
    """Rend (cascade, stats) ; lève `CleTaggerAbsente` si la clé manque (et ne l'affiche pas)."""
    stats = {"appels": 0, "requetes": 0, "cache": 0, "tokens": 0, "latence_s": 0.0,
             "modeles": {}, "cle_refusee": 0}
    client = _client_tagger()
    return _cascade_tagger(_transport_tagger(client, stats), partition=partition,
                           stats=stats), stats


def _cout_tagger(stats: dict) -> dict:
    """Le coût d'une exécution, tel qu'il va dans un rapport (`evaluer --json`)."""
    return {"modele": MODELE_TAGGER, "appels": stats["appels"],
            "requetes": stats["requetes"], "cache": stats["cache"],
            "tokens": stats["tokens"], "latence_s": round(stats["latence_s"], 3),
            "modeles_renvoyes": dict(stats["modeles"])}


def _cout_pour_phrases(cout: dict, mesurees: int, cible: int) -> dict:
    """Le coût d'un lot de `cible` phrases, au prorata du lot **mesuré**.

    Le tagger fait **un appel par phrase** : le coût est linéaire en nombre de phrases. On ne
    modélise pas la longueur des phrases (le prompt la porte), donc ce chiffre vaut pour un lot
    de même longueur moyenne que le lot mesuré. `mesurees` est le nombre de phrases réellement
    passées au tagger ; il ne doit pas être confondu avec le nombre d'appels (le cache mémoire
    peut en servir plusieurs).
    """
    mesurees = max(1, int(mesurees))
    cible = max(0, int(cible))
    ratio = cible / mesurees
    return {
        "phrases": cible,
        "phrases_mesurees": mesurees,
        "modele": cout.get("modele", MODELE_TAGGER),
        "appels": int(round(cout.get("appels", 0) * ratio)),
        "requetes": int(round(cout.get("requetes", 0) * ratio)),
        "cache": int(round(cout.get("cache", 0) * ratio)),
        "tokens": int(round(cout.get("tokens", 0) * ratio)),
        "latence_s": round(cout.get("latence_s", 0.0) * ratio, 3),
    }


def _ligne_tagger(stats: dict) -> str:
    """Une ligne de coût pour l'affichage et la stderr ; pas de clé, pas d'horodatage."""
    return (f"modèle={MODELE_TAGGER} · appels={stats['appels']} "
            f"· réseau={stats['requetes']} · cache={stats['cache']} "
            f"· tokens={stats['tokens']} · latence={stats['latence_s']:.1f} s")


# --------------------------------------------------------------------------- rendu lisible


def _valeur_affichee(valeur: str, largeur: int) -> str:
    """Une valeur de syntagme sur une ligne (les blancs sont normalisés pour l'affichage)."""
    v = " ".join(str(valeur).split())
    if len(v) <= largeur:
        return v
    return v[: max(1, largeur - 1)].rstrip() + "…"


def _envelopper(prefixe: str, contenu: str, largeur: int = LARGEUR) -> list[str]:
    """Coupe une ligne trop longue en gardant l'alignement sous le préfixe."""
    lignes = textwrap.wrap(contenu, width=max(20, largeur - len(prefixe)),
                           break_long_words=False, break_on_hyphens=False) or [""]
    return [prefixe + lignes[0]] + [" " * len(prefixe) + ligne for ligne in lignes[1:]]


class _Formateur(argparse.RawDescriptionHelpFormatter):
    """Une aide de largeur fixe : la sortie ne dépend pas de la taille du terminal."""

    def __init__(self, prog: str, **kwargs):
        kwargs.setdefault("width", LARGEUR)
        super().__init__(prog, **kwargs)


def formater_annotation(a: bl.Annotation, tagger: bool = False,
                        stats: dict | None = None, titre: str | None = None) -> str:
    """La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique, couverture.

    Avec `--tagger`, l'en-tête le dit, le coût de l'API est affiché et un refus du tagger est
    nommé — le JSON d'annotation, lui, garde exactement le même contrat. `titre` permet au mode
    `auto` de nommer la voie qui a réellement servi (API, heuristique, ou repli).
    """
    if titre is None:
        titre = (f"{NOM} {VERSION} — analyse cascade POS (tagger API DeepSeek, réseau)"
                 if tagger else f"{NOM} {VERSION} — analyse heuristique (CPU, hors ligne)")
    lignes = [titre]
    lignes.append(
        f"langue={a.langue} script={a.script} source={a.source} · {len(a.etiquettes)} étiquettes "
        f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"
    )

    pos = [e for e in a.etiquettes if e.niveau == "pos"]
    if pos:
        lignes.extend(_envelopper("POS  ", " ".join(f"{e.valeur}/{e.type}" for e in pos)))
    else:
        lignes.append("POS  —")

    syntagmes = [e for e in a.etiquettes if e.niveau == "syntagme"]
    if syntagmes:
        valeurs = [_valeur_affichee(e.valeur, 46) for e in syntagmes]
        roles = [str(e.meta.get("role") or "—") for e in syntagmes]
        cibles = [str((e.meta.get("attachement") or {}).get("cible") or "—") for e in syntagmes]
        spans = [f"[{e.debut}:{e.fin}]" for e in syntagmes]
        lt = max(3, max(len(e.type) for e in syntagmes))
        lsp = max(len(s) for s in spans)
        lv = max(len(v) for v in valeurs)
        lr = max(len(r) for r in roles)
        lignes.append("SYNTAGMES")
        for e, valeur, role, cible, span in zip(syntagmes, valeurs, roles, cibles, spans):
            lignes.append(
                f"  {e.type:<{lt}}  {span:<{lsp}}  {valeur:<{lv}}  "
                f"rôle={role:<{lr}}  → {cible}"
            )
    else:
        lignes.append("SYNTAGMES —")

    phrases = [e for e in a.etiquettes if e.niveau == "phrase" and e.type == "type"]
    if phrases:
        lignes.append("PRAGMATIQUE")
        par_span: dict[tuple[int, int], list[bl.Etiquette]] = {}
        for e in a.etiquettes:
            if e.niveau == "pragmatique":
                par_span.setdefault((e.debut, e.fin), []).append(e)
        for p in phrases:
            ici = par_span.get((p.debut, p.fin), [])
            acte = next((e.valeur for e in ici if e.type == "acte"), "—")
            negation = "oui" if any(e.type == "négation" for e in ici) else "non"
            modalite = "oui" if any(e.type == "modalité" for e in ici) else "non"
            double_sens = "oui" if any(e.type == "double_sens" for e in ici) else "non"
            lignes.append(
                f"  phrase [{p.debut}:{p.fin}] {p.valeur} · acte={acte} "
                f"· négation={negation} · modalité={modalite} · double sens={double_sens}"
            )
    else:
        lignes.append("PRAGMATIQUE —")

    couverture = a.couverture()
    if couverture:
        ordre = [n for n in bl.NIVEAUX if n in couverture]
        ordre += sorted(n for n in couverture if n not in bl.NIVEAUX)
        lignes.extend(_envelopper(
            "COUVERTURE  ",
            "(confiance max par niveau)  "
            + " · ".join(f"{n}={couverture[n]:.2f}" for n in ordre),
        ))
    if tagger and a.refus:
        lignes.extend(_envelopper("REFUS TAGGER  ", a.refus))
    if stats is not None:
        lignes.extend(_envelopper("TAGGER API  ", _ligne_tagger(stats)))
    return "\n".join(lignes)


# --------------------------------------------------------------------------- commandes


def _lire_entree(args: argparse.Namespace) -> str:
    """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
    if getattr(args, "fichier", None):
        return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
    return args.texte or ""


def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
                    stats: dict | None = None, auto: _TaggerAuto | None = None) -> int:
    """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`).

    `h` segmente (le tagger ne change pas les frontières de phrase) ; `bloc` analyse — la
    cascade du tagger quand `--tagger` est posé. Le coût va sur `stderr`, jamais dans le JSONL.
    En mode `auto`, le message qui dit la voie servie va aussi sur `stderr`.
    """
    n = 0
    refus = 0
    for debut, fin, _typ, _ in h._phrases(texte):
        phrase = texte[debut:fin]
        if not phrase.strip():
            continue
        a = bloc.analyser(phrase, args.langue, args.contexte)
        refus += int(bool(a.refus))
        sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
        n += 1
    if n == 0:
        print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
        if auto is not None:
            print(f"{NOM}: tagger auto · {auto.message()}", file=sys.stderr)
        return 3
    if stats is not None:
        print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
        if refus:
            print(f"{NOM}: tagger · {refus}/{n} phrase(s) refusée(s) (JSON partiel)",
                  file=sys.stderr)
    if auto is not None:
        print(f"{NOM}: tagger auto · {auto.message()}", file=sys.stderr)
    return 0


def _mode_tagger(args: argparse.Namespace) -> str | None:
    """`None` (défaut), `"api"` (`--tagger`) ou `"auto"` (`--tagger auto`)."""
    mode = getattr(args, "tagger_mode", None)
    if mode is not None:
        return mode
    if getattr(args, "tagger_auto", False):
        return "auto"
    if getattr(args, "tagger", False):
        return "api"
    return None


def cmd_analyser(args: argparse.Namespace) -> int:
    texte = _lire_entree(args)
    h = bl.Heuristique(partition=args.partition)
    mode = _mode_tagger(args)
    bloc, stats, auto = h, None, None
    a_des_mots = any(typ in ("mot", "nombre") for _, _, _, typ in h._mots(texte))
    if mode == "auto":
        auto = _TaggerAuto(h)
        # sans aucune clé, on ne construit même pas la cascade : aucun import réseau, aucun appel
        auto.cle_presente = _cle_tagger_presente()
        if auto.cle_presente and a_des_mots:
            try:
                cascade, stats_tagger = _construire_tagger(partition=args.partition)
            except CleTaggerAbsente:
                # la clé a disparu entre la vérification et la construction : heuristique
                auto.cle_presente = False
            else:
                auto.cascade, auto.stats = cascade, stats_tagger
                stats = stats_tagger
        # un texte sans mot ni nombre est un refus d'analyse : la cascade n'est pas construite
        bloc = auto
    elif mode == "api":
        # la clé est vérifiée avant toute analyse : sans elle, code 4 (jamais de trace de la clé)
        try:
            cascade, stats_tagger = _construire_tagger(partition=args.partition)
        except CleTaggerAbsente as exc:
            print(f"{NOM}: dépendance absente : {exc}", file=sys.stderr)
            return 4
        if a_des_mots:
            bloc, stats = cascade, stats_tagger
        # sinon, le refus (code 3) reste celui de l'heuristique
    if args.jsonl:
        return _analyser_jsonl(texte, args, h, bloc, stats, auto)
    annotation = bloc.analyser(texte, args.langue, args.contexte)
    if annotation.refus:
        if auto is not None:
            if annotation.refus.startswith("tagger auto :"):
                # un repli du tagger n'est pas un refus du texte : l'analyse est rendue
                print(f"{NOM}: tagger : refus partiel : {annotation.refus}", file=sys.stderr)
            else:
                # refus du texte : code 3, que la clé existe ou non
                if args.json:
                    sys.stdout.write(_dumps(annotation.json()))
                else:
                    print(f"{NOM}: refus d'analyse : {annotation.refus} "
                          "(le texte doit contenir au moins une lettre ou un chiffre)",
                          file=sys.stderr)
                print(f"{NOM}: tagger auto · {auto.message()}", file=sys.stderr)
                return 3
        elif stats is not None:
            # un refus du tagger n'est pas un refus du texte : on le nomme, on ne le déguise pas
            pos = [e for e in annotation.etiquettes if e.niveau == "pos"]
            if not pos:
                print(f"{NOM}: tagger : {annotation.refus}", file=sys.stderr)
                return 1
            print(f"{NOM}: tagger : refus partiel : {annotation.refus}", file=sys.stderr)
        else:
            # un refus est une **réponse** : le JSON la porte, le code 3 la distingue d'une erreur
            if args.json:
                sys.stdout.write(_dumps(annotation.json()))
            else:
                print(f"{NOM}: refus d'analyse : {annotation.refus} "
                      "(le texte doit contenir au moins une lettre ou un chiffre)",
                      file=sys.stderr)
            return 3
    if args.json:
        sys.stdout.write(_dumps(annotation.json()))
        if stats is not None:
            print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
    else:
        titre = auto.titre() if auto is not None else None
        print(_sur(formater_annotation(annotation, tagger=stats is not None, stats=stats,
                                       titre=titre)))
    if auto is not None:
        print(f"{NOM}: tagger auto · {auto.message()}", file=sys.stderr)
    return 0


def _module_evaluation():
    """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
    if not chemin.is_file():
        raise FileNotFoundError(f"mesure du gold introuvable : {chemin}")
    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
    if spec is None or spec.loader is None:
        raise ImportError(f"impossible de charger {chemin}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _cibles_gold(phrases: list[dict]) -> list[str]:
    return [s["cible"] for p in phrases for s in p.get("segments", []) if s.get("cible")]


def _controle_hasard(phrases: list[dict]) -> float:
    """Contrôle négatif : une cible **exacte** tirée au hasard parmi les cibles du gold.

    Graine fixe, donc reproductible : c'est un plancher, pas une mesure de qualité.
    """
    cibles = _cibles_gold(phrases)
    if not cibles:
        return 0.0
    univers = sorted(set(cibles))
    rng = random.Random(0)
    justes = sum(1 for c in cibles if rng.choice(univers) == c)
    return round(justes / len(cibles), 4)


def _pct(valeur: float) -> str:
    return f"{100.0 * float(valeur):.2f} %"


def _points(delta: float) -> str:
    """Un écart de taux en **points** de pourcentage, avec son signe."""
    return f"{100.0 * float(delta):+.2f} pts"


def _formater_evaluation(rapport: dict) -> str:
    gold = rapport["gold"]
    mesure = rapport["heuristique"]
    pos = mesure["pos"]
    syn = mesure["syntagme"]
    tete = syn["tete"]
    att = mesure["attachement"]
    att_tete = mesure["attachement_tete"]
    prag = mesure["pragmatique"]
    controle = rapport["controle_negatif"]
    lignes = [
        f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
        f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
        f"{gold['cibles_attachement']} cibles d'attachement",
        "",
        f"POS         exactitude {_pct(pos['exactitude'])}  "
        f"(fermé {_pct(pos['exactitude_ferme'])}, ouvert {_pct(pos['exactitude_ouvert'])})",
        f"SYNTAGMES   F1 {_pct(syn['f1'])}  "
        f"(P {_pct(syn['precision'])} / R {_pct(syn['rappel'])})",
        f"  tête      F1 {_pct(tete['f1'])}  "
        f"(P {_pct(tete['precision'])} / R {_pct(tete['rappel'])})",
        f"  vue linéaire (partition filtrer) F1 {_pct(rapport['syntagmes_lineaire']['f1'])}  "
        f"· attachement {_pct(rapport['attachement_lineaire']['couverture'])} de couverture",
        (f"BASE RÉELLE (hand + reel, {rapport['reel']['phrases']} phrases)  "
         f"POS {_pct(rapport['reel']['pos'])} · F1 {_pct(rapport['reel']['f1'])} "
         f"· attachement {_pct(rapport['reel']['couverture'])}"
         if rapport.get("reel") else f"BASE RÉELLE — (déjà la base, ou gold gelé)"),
        f"ATTACHEMENT exact {_pct(att['exact_taux'])} · couverture {_pct(att['couverture'])} "
        f"· exact sur span {_pct(att['exact_taux_span'])} · top-k {_pct(att['topk_taux'])}",
        f"  tête      couverture {_pct(att_tete['couverture'])} "
        f"· top-k {_pct(att_tete['topk_taux'])}",
        f"PRAGMATIQUE acte {_pct(prag['acte'])} · négation {_pct(prag['negation'])} "
        f"· modalité {_pct(prag['modalite'])} · double sens {_pct(prag['double_sens'])}",
        f"FRACTION SÉMANTIQUE {_pct(mesure['fraction_semantique'])}",
        f"CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(controle['exact_taux'])} "
        f"(graine {controle['graine']}, {controle['cibles']} cibles)",
    ]
    tagger = rapport.get("tagger")
    if tagger:
        tp, ts, cout = tagger["pos"], tagger["syntagme"], tagger["cout"]
        lignes += [
            "",
            "TAGGER API DEEPSEEK (option --tagger)",
            f"  POS         exactitude {_pct(tp['exactitude'])} "
            f"(fermé {_pct(tp['exactitude_ferme'])}, ouvert {_pct(tp['exactitude_ouvert'])}) "
            f"· Δ {_points(tagger['delta_pos'])} vs heuristique",
            f"  SYNTAGMES   F1 {_pct(ts['f1'])} (tête {_pct(ts['tete']['f1'])}) "
            "— conservés à l'heuristique",
            f"  COÛT        appels {cout['appels']} · réseau {cout['requetes']} "
            f"· cache {cout['cache']} · tokens {cout['tokens']} · modèle {cout['modele']}",
        ]
        renvoyes = cout.get("modeles_renvoyes") or {}
        if renvoyes and set(renvoyes) - {cout["modele"]}:
            lignes.append(f"  modèle renvoyé : {', '.join(sorted(renvoyes))}")
        if tagger.get("refus"):
            detail = ", ".join(tagger.get("refus_detail") or [])
            lignes.append(f"  REFUS       {tagger['refus']} phrase(s)"
                          + (f" : {detail}" if detail else ""))
    par_langue = rapport.get("par_langue") or {}
    if par_langue:
        lignes += ["", "PAR LANGUE"]
        for langue, m in par_langue.items():
            p, s, a, c = m["pos"], m["syntagme"], m["attachement"], m["controle_negatif"]
            pr = m["pragmatique"]
            lignes += [
                f"  {langue}  {m['phrases']} phrases · {p['tokens']} tokens · "
                f"{a['cibles']} cibles d'attachement",
                f"      POS {_pct(p['exactitude'])} (fermé {_pct(p['exactitude_ferme'])}, "
                f"ouvert {_pct(p['exactitude_ouvert'])}) · SYNTAGMES F1 {_pct(s['f1'])} "
                f"(tête {_pct(s['tete']['f1'])})",
                f"      ATTACHEMENT exact {_pct(a['exact_taux'])} · "
                f"couverture {_pct(a['couverture'])} · top-k {_pct(a['topk_taux'])} · "
                f"PRAGMATIQUE acte {_pct(pr['acte'])}",
                f"      CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(c['exact_taux'])} "
                f"(graine {c['graine']}, {c['cibles']} cibles)",
            ]
            t = m.get("tagger")
            if t:
                lignes.append(
                    f"      TAGGER POS {_pct(t['pos']['exactitude'])} "
                    f"· Δ {_points(t['delta_pos'])} "
                    f"· SYNTAGMES F1 {_pct(t['syntagme']['f1'])} "
                    f"(tête {_pct(t['syntagme']['tete']['f1'])})")
    return "\n".join(lignes)


def cmd_evaluer(args: argparse.Namespace) -> int:
    if getattr(args, "tagger_auto", False):
        print(f"{NOM}: erreur d'usage : --tagger auto n'est disponible que pour analyser",
              file=sys.stderr)
        return 2
    evaluateur = _module_evaluation()
    phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
    if getattr(args, "reel", False):
        # la **base honnête** : les phrases réelles (main + corpus), sans le synthétique
        phrases = [p for p in phrases if p.get("source") in ("hand", "reel")]
    cascade = None
    stats = None
    if getattr(args, "tagger", False):
        try:
            cascade, stats = _construire_tagger()
        except CleTaggerAbsente as exc:
            print(f"{NOM}: dépendance absente : {exc}", file=sys.stderr)
            return 4
    mesure = evaluateur.evaluer_bloc("heuristique", bl.Heuristique(), phrases)
    # transparence : la vue **fidèle** (défaut) et la vue **linéaire** (partition filtrer)
    _lineaire = evaluateur.evaluer_bloc("lineaire", bl.Heuristique(partition="filtrer"), phrases)
    # la **base honnête**, publiée à côté du global (les 160 synthétiques sont faciles)
    _reel = None
    if not getattr(args, "reel", False) and not args.gold:
        _phrases_reelles = [p for p in evaluateur.charger() if p.get("source") in ("hand", "reel")]
        if _phrases_reelles and len(_phrases_reelles) < len(phrases):
            _reel = evaluateur.evaluer_bloc("reel", bl.Heuristique(), _phrases_reelles)
    hasard = _controle_hasard(phrases)
    rapport = {
        "version": VERSION,
        "gold": {
            "nom": ("gelé (référence figée)" if args.gold
                    else "réel (hand + reel, sans synthétique)" if getattr(args, "reel", False)
                    else "vivant (hand + reel + synthétique)"),
            "gele": bool(args.gold),
            "phrases": len(phrases),
            "tokens": mesure["pos"]["tokens"],
            "cibles_attachement": mesure["attachement"]["cibles"],
        },
        "heuristique": mesure,
        "reel": ({"phrases": len(_phrases_reelles),
                  "pos": _reel["pos"]["exactitude"],
                  "f1": _reel["syntagme"]["f1"],
                  "attachement": _reel["attachement"]["exact"],
                  "couverture": _reel["attachement"]["couverture"]}
                 if _reel else None),
        "syntagmes_lineaire": _lineaire["syntagme"],
        "attachement_lineaire": {"exact": _lineaire["attachement"]["exact"],
                                 "labels": _lineaire["attachement"]["labels"],
                                 "couverture": _lineaire["attachement"]["couverture"]},
        "controle_negatif": {
            "nom": "cible exacte tirée au hasard dans le gold",
            "graine": 0,
            "cibles": len(_cibles_gold(phrases)),
            "exact_taux": hasard,
        },
    }
    if cascade is not None:
        # `evaluer_bloc` mesure l'annotation de la cascade ; le POS y vient du tagger. Les
        # appels sont ensuite servis par le cache mémoire des taggers (aucun appel en plus).
        mesure_tag = evaluateur.evaluer_bloc("cascade", cascade, phrases)
        refus = [p.get("id", "") for p in phrases
                 if cascade.analyser(p["texte"], p["langue"]).refus]
        rapport["tagger"] = {
            "nom": "cascade POS (tagger API DeepSeek)",
            "modele": MODELE_TAGGER,
            "seuil": SEUIL_TAGGER,
            "priorite": "pos → neuronal ; syntagmes, rôles et pragmatique → heuristique",
            "pos": mesure_tag["pos"],
            "syntagme": mesure_tag["syntagme"],
            "pragmatique": mesure_tag["pragmatique"],
            "fraction_semantique": mesure_tag["fraction_semantique"],
            "delta_pos": round(mesure_tag["pos"]["exactitude"] - mesure["pos"]["exactitude"], 4),
            "refus": len(refus),
            "refus_detail": refus[:10],
            "cout": _cout_tagger(stats),
            # le chiffre de la décision : le coût du même câblage pour 1 000 phrases
            "cout_pour_1000_phrases": _cout_pour_phrases(_cout_tagger(stats), len(phrases), 1000),
        }
    if args.par_langue:
        # le détail fr/en : on rejoue la **même** mesure sur chaque sous-gold. Le contrôle
        # négatif est recalculé par langue (l'univers des cibles change avec la langue).
        par_langue = {}
        for langue in sorted({p.get("langue", "fr") for p in phrases}):
            sous = [p for p in phrases if p.get("langue", "fr") == langue]
            m = evaluateur.evaluer_bloc("heuristique", bl.Heuristique(), sous)
            m["controle_negatif"] = {
                "nom": "cible exacte tirée au hasard dans le gold de la langue",
                "graine": 0,
                "cibles": len(_cibles_gold(sous)),
                "exact_taux": _controle_hasard(sous),
            }
            if cascade is not None:
                mt = evaluateur.evaluer_bloc("cascade", cascade, sous)
                m["tagger"] = {
                    "pos": {k: mt["pos"][k] for k in ("exactitude", "exactitude_ferme",
                                                      "exactitude_ouvert", "tokens")},
                    "syntagme": {"f1": mt["syntagme"]["f1"],
                                 "tete": {"f1": mt["syntagme"]["tete"]["f1"]}},
                    "pragmatique": mt["pragmatique"],
                    "fraction_semantique": mt["fraction_semantique"],
                    "delta_pos": round(mt["pos"]["exactitude"] - m["pos"]["exactitude"], 4),
                }
            par_langue[langue] = m
        rapport["par_langue"] = par_langue
    if args.json:
        sys.stdout.write(_dumps(rapport))
        if stats is not None:
            print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
    else:
        print(_formater_evaluation(rapport))
    return 0


def cmd_rejouer(args: argparse.Namespace) -> int:
    premiere = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    seconde = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    if premiere.refus or seconde.refus:
        refus = premiere.refus or seconde.refus
        print(f"{NOM}: refus d'analyse : {refus} "
              "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 1
    canonique_1 = _canonique(premiere)
    canonique_2 = _canonique(seconde)
    identique = canonique_1 == canonique_2
    empreinte = hashlib.sha256(canonique_1.encode("utf-8")).hexdigest()[:16]
    print(f"rejeu identique : {'oui' if identique else 'non'}")
    print(f"  texte      : {args.texte!r}")
    print(f"  langue     : {premiere.langue}")
    print(f"  étiquettes : {len(premiere.etiquettes)}")
    print(f"  JSON       : {len(canonique_1.encode('utf-8'))} octets "
          f"· sha256 {empreinte}…")
    if not identique:
        print("  divergence : les deux analyses ne rendent pas le même JSON canonique",
              file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- restitution


def cmd_restituer(args: argparse.Namespace) -> int:
    """Reconstruit la surface depuis l'annotation et rend la fidélité du miroir.

    Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
    (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
    ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ;
    `--roles` ajoute la **v2** (agent, prédicat, lieu) et, sur un banc, sa fidélité à
    l'or ; `--roles-v3` ajoute la **v3** (les rôles des GP : lieu, temps, destinataire,
    possession, complément). La sortie de la v0 reste celle par défaut.
    """
    if args.roles_v3 and args.canonique:
        print(f"{NOM}: erreur d'usage : --roles-v3 et --canonique sont exclusifs",
              file=sys.stderr)
        return 2
    if args.roles and args.roles_v3:
        print(f"{NOM}: erreur d'usage : --roles (v2) et --roles-v3 sont exclusifs",
              file=sys.stderr)
        return 2
    if args.roles and args.canonique:
        print(f"{NOM}: erreur d'usage : --roles et --canonique sont exclusifs",
              file=sys.stderr)
        return 2
    if args.gold and not (args.banc and (args.roles or args.roles_v3)):
        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles ou "
              "--banc --roles-v3", file=sys.stderr)
        return 2
    if args.banc:
        if args.texte is not None or args.fichier:
            print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
                  file=sys.stderr)
            return 2
        try:
            donnees = json.loads(pathlib.Path(args.banc).read_text(encoding="utf-8"))
            items = restitution.items_banc(donnees)
        except (OSError, ValueError) as exc:
            print(f"{NOM}: erreur : banc illisible : {exc}", file=sys.stderr)
            return 1
        if args.roles_v3 or args.roles:
            defaut = (restitution_v2.GOLD_DEFAUT if args.roles
                      else restitution_v3.GOLD_DEFAUT)
            chemin_gold = pathlib.Path(args.gold or defaut)
            try:
                gold = json.loads(chemin_gold.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                print(f"{NOM}: erreur : or de rôles illisible : {exc}", file=sys.stderr)
                return 1
            if args.roles_v3:
                rapport = restitution_v3.mesurer_banc_v3(items, gold, args.langue)
            else:
                rapport = restitution_v2.mesurer_banc_v2(items, gold, args.langue)
        elif args.canonique:
            rapport = restitution.mesurer_banc_v1(items, args.langue)
        else:
            rapport = restitution.mesurer_banc(items, args.langue)
        rapport["banc"] = args.banc
        if args.json:
            sys.stdout.write(_dumps(rapport))
        else:
            if args.roles_v3:
                formateur = restitution_v3.formater_banc_v3
            elif args.roles:
                formateur = restitution_v2.formater_banc_v2
            elif args.canonique:
                formateur = restitution.formater_banc_v1
            else:
                formateur = restitution.formater_banc
            print(_sur(formateur(rapport, args.banc)))
        return 0

    texte = _lire_entree(args)
    if args.texte is None and not args.fichier:
        print(f"{NOM}: erreur d'usage : TEXTE ou --fichier requis", file=sys.stderr)
        return 2
    annotation = bl.Heuristique().analyser(texte, args.langue, args.contexte)
    if annotation.refus:
        print(f"{NOM}: refus d'analyse : {annotation.refus} "
              "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 3
    if args.roles_v3:
        mesure_v3 = restitution_v3.mesurer_annotation_v3(annotation, texte)
        if args.json:
            sys.stdout.write(_dumps({
                "schema": restitution_v3.SCHEMA,
                "version": restitution_v3.VERSION,
                **mesure_v3,
            }))
        else:
            print(_sur(restitution_v3.formater_mesure_v3(mesure_v3, texte)))
        return 0
    if args.roles:
        mesure_v2 = restitution_v2.mesurer_annotation_v2(annotation, texte)
        if args.json:
            sys.stdout.write(_dumps({
                "schema": restitution_v2.SCHEMA,
                "version": restitution_v2.VERSION,
                **mesure_v2,
            }))
        else:
            print(_sur(restitution_v2.formater_mesure_v2(mesure_v2, texte)))
        return 0
    if args.canonique:
        mesure_v1 = restitution.mesurer_annotation_v1(annotation, texte)
        if args.json:
            sys.stdout.write(_dumps({
                "schema": restitution.SCHEMA_CANONIQUE,
                "version": restitution.VERSION_CANONIQUE,
                **mesure_v1,
            }))
        else:
            print(_sur(restitution.formater_mesure_v1(mesure_v1, texte)))
        return 0
    mesure = restitution.mesurer_annotation(annotation, texte)
    if args.json:
        sys.stdout.write(_dumps({
            "schema": restitution.SCHEMA,
            "version": restitution.VERSION,
            **mesure,
        }))
    else:
        print(_sur(restitution.formater_mesure(mesure, texte)))
    return 0


# --------------------------------------------------------------------------- CLI


class _Parseur(argparse.ArgumentParser):
    """Un parseur francophone : `-h`, `--help` et `--aide` partout, sans doublon."""

    def __init__(self, *args, **kwargs):
        kwargs["add_help"] = False
        super().__init__(*args, **kwargs)
        self._positionals.title = "arguments"
        self._optionals.title = "options"
        self.add_argument("-h", "--help", "--aide", action="help",
                          help="afficher cette aide et quitter")

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")


def _normaliser_tagger(argv: list[str]) -> list[str]:
    """`--tagger auto` → `--tagger-auto`, sans avaler le TEXTE qui suit.

    Un `--tagger` à valeur optionnelle (`nargs="?"`) mangerait le texte positionnel quand
    l'utilisateur écrit `analyser --tagger "Le chat dort."`. On garde donc `--tagger` comme
    drapeau et on ne transforme que les deux valeurs explicites `auto` et `api`.
    """
    sortie: list[str] = []
    i = 0
    while i < len(argv):
        jeton = argv[i]
        if jeton == "--tagger" and i + 1 < len(argv) and argv[i + 1] in ("auto", "api", "explicite"):
            valeur = argv[i + 1]
            sortie.append("--tagger-auto" if valeur == "auto" else "--tagger")
            i += 2
            continue
        if jeton.startswith("--tagger="):
            valeur = jeton.split("=", 1)[1]
            if valeur == "auto":
                sortie.append("--tagger-auto")
            elif valeur in ("api", "explicite"):
                sortie.append("--tagger")
            else:
                sortie.append(jeton)
        else:
            sortie.append(jeton)
        i += 1
    return sortie


def construire_parseur() -> argparse.ArgumentParser:
    epilogue = (
        "Commandes : analyser, evaluer, rejouer, restituer.\n"
        "Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·\n"
        "4 clé/tagger indisponible (absente ou refusée, seulement avec --tagger explicite) · 1 erreur.\n"
        "Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,\n"
        "--contexte, --banc, --tagger [auto].\n"
        "Limites : heuristique CPU, hors ligne, déterministe par défaut ; --tagger appelle l'API\n"
        "DeepSeek (clé, réseau) pour le POS ; --tagger auto l'appelle seulement si une clé existe,\n"
        "sinon il rend l'heuristique, sans changer le code de sortie ; la restitution est un codec\n"
        "de surface (graphème), pas un décodeur neuronal ; ni traduction ni génération.\n"
        "Exemples :\n"
        "  python3 tools/drave.py analyser \"Le chat dort.\"\n"
        "  python3 tools/drave.py analyser \"Le chat dort.\" --tagger\n"
        "  python3 tools/drave.py analyser \"Le chat dort.\" --tagger auto\n"
        "  python3 tools/drave.py evaluer --gold --json\n"
        "  python3 tools/drave.py restituer \"Le chat dort.\"\n"
        "  python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json\n"
    )
    parseur = _Parseur(
        prog=NOM,
        description="Point d'entrée produit du bloc linguistique (analyse et restitution).",
        epilog=epilogue,
        formatter_class=_Formateur,
    )
    parseur.add_argument("-V", "--version", action="version", version=f"{NOM} {VERSION}",
                         help="afficher la version et quitter")
    sous = parseur.add_subparsers(dest="commande",
                                  metavar="{analyser,evaluer,rejouer,restituer}",
                                  required=True)

    analyser = sous.add_parser(
        "analyser",
        help="étiqueter un texte (POS, syntagmes, pragmatique)",
        description="Analyse un texte avec l'heuristique et rend la lecture compacte ou le JSON. "
                    "Avec --tagger, le POS (et lui seul) vient du tagger de l'API DeepSeek : "
                    "clé requise, réseau, cache du client ; sans l'option, rien ne change. "
                    "Avec --tagger auto, l'API sert si une clé existe, sinon l'heuristique ; "
                    "le code de sortie ne change pas (0 dans les deux cas, 3 pour un refus).",
        epilog="Exemples : python3 tools/drave.py analyser \"Le chat dort.\" --json ; "
               "python3 tools/drave.py analyser \"Le chat dort.\" --tagger ; "
               "python3 tools/drave.py analyser \"Le chat dort.\" --tagger auto",
        formatter_class=_Formateur,
    )
    analyser.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
                          help="texte à analyser (entre guillemets) ou --fichier")
    analyser.add_argument("--partition", choices=("brut", "alternative", "filtrer_union", "filtrer"),
                          default="alternative",
                          help="la vue des syntagmes qui se chevauchent (défaut : alternative)")
    analyser.add_argument("--fichier", default=None, metavar="CHEMIN",
                          help="lire le texte dans un fichier UTF-8 (au lieu de l'argument)")
    analyser.add_argument("--jsonl", action="store_true",
                          help="une ligne JSON par phrase (traitement de corpus)")
    analyser.add_argument("--contexte", default=None,
                          help="le texte qui précède (mémoire de discours : coréférence, connecteurs)")
    analyser.add_argument("--langue", choices=("fr", "en"), default=None,
                          help="indice de langue (fr/en) ; sans lui, le bloc détecte")
    analyser.add_argument("--tagger", action="store_true",
                          help="tagger POS par l'API DeepSeek (clé et réseau ; défaut : heuristique) ; "
                               "`--tagger auto` : API si une clé existe, sinon heuristique, sans "
                               "changer le code de sortie")
    analyser.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
    analyser.add_argument("--json", action="store_true",
                          help="sortie JSON complète (annotation, sans durée)")
    analyser.set_defaults(fonction=cmd_analyser)

    evaluer = sous.add_parser(
        "evaluer",
        help="mesurer l'heuristique sur le gold",
        description="Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) "
                    "sur le gold, avec un contrôle négatif reproductible. Avec --par-langue, "
                    "donne le même détail pour le français et l'anglais. Avec --tagger, mesure "
                    "en plus la cascade POS de l'API DeepSeek et son écart.",
        epilog="Exemples : python3 tools/drave.py evaluer --gold --json ; "
               "python3 tools/drave.py evaluer --par-langue ; "
               "python3 tools/drave.py evaluer --tagger",
        formatter_class=_Formateur,
    )
    evaluer.add_argument("--gold", action="store_true",
                         help="mesurer le gold gelé (référence figée) au lieu du gold vivant")
    evaluer.add_argument("--reel", action="store_true",
                         help="mesurer la base honnête : les phrases réelles (hand + reel), sans synthétique")
    evaluer.add_argument("--par-langue", action="store_true",
                         help="scinder la mesure en français et en anglais")
    evaluer.add_argument("--tagger", action="store_true",
                         help="mesurer en plus la cascade POS de l'API DeepSeek (clé et réseau)")
    evaluer.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
    evaluer.add_argument("--json", action="store_true",
                         help="sortie JSON des mesures complètes")
    evaluer.set_defaults(fonction=cmd_evaluer)

    rejouer = sous.add_parser(
        "rejouer",
        help="analyser deux fois et vérifier le déterminisme",
        description="Analyse le texte deux fois, compare le JSON canonique et rend une empreinte "
                    "sha256. Sortie 1 si les deux analyses divergent.",
        epilog="Exemple : python3 tools/drave.py rejouer \"Le chat dort.\"",
        formatter_class=_Formateur,
    )
    rejouer.add_argument("texte", metavar="TEXTE", help="texte à rejouer (entre guillemets)")
    rejouer.add_argument("--partition", choices=("brut", "alternative", "filtrer_union", "filtrer"),
                         default="alternative")
    rejouer.add_argument("--langue", choices=("fr", "en"), default=None,
                         help="indice de langue (fr/en) ; sans lui, le bloc détecte")
    rejouer.set_defaults(fonction=cmd_rejouer)

    restituer = sous.add_parser(
        "restituer",
        help="reconstruire la surface depuis l'annotation et mesurer le miroir",
        description="Analyse un texte, reconstruit la surface depuis le niveau `graphème` "
                    "(sans lire le champ `texte` de l'annotation) et compare à la source. "
                    "Affiche la fidélité binaire du miroir, la fidélité de caractères et un "
                    "contrôle négatif. Avec --canonique, produit en plus la forme canonique v1 "
                    "(segments + rôles + cibles) et son miroir canonique ; avec --roles, produit "
                    "la forme lisible des rôles (agent, prédicat, lieu) et, sur un banc, leur "
                    "fidélité à un or écrit à la main ; avec --roles-v3, produit les rôles des "
                    "GP (lieu, temps, destinataire, possession, complément).",
        epilog="Exemples : python3 tools/drave.py restituer \"Le chat dort.\" ; "
               "python3 tools/drave.py restituer \"Le chat dort.\" --canonique ; "
               "python3 tools/drave.py restituer \"Le chat dort.\" --roles ; "
               "python3 tools/drave.py restituer \"Le voyage à Paris dure deux heures.\" --roles-v3 ; "
               "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles",
        formatter_class=_Formateur,
    )
    restituer.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
                           help="texte à restituer (entre guillemets) ou --fichier")
    restituer.add_argument("--banc", default=None, metavar="CHEMIN",
                           help="mesurer un banc JSON de textes (ex. les 50 textes libres)")
    restituer.add_argument("--canonique", action="store_true",
                           help="ajouter la forme canonique v1 (segments + rôles + cibles) "
                                "et son miroir canonique")
    restituer.add_argument("--roles", action="store_true",
                           help="ajouter la forme lisible des rôles (agent, prédicat, lieu) ; "
                                "avec --banc, mesurer leur fidélité à l'or")
    restituer.add_argument("--roles-v3", action="store_true",
                           help="ajouter les rôles des GP (lieu, temps, destinataire, "
                                "possession, complément) ; avec --banc, mesurer leur fidélité")
    restituer.add_argument("--gold", default=None, metavar="CHEMIN",
                           help="or de rôles pour --banc --roles ou --banc --roles-v3 "
                                "(défaut : tools/tests/linguistique/gold_restitution_v2.json)")
    restituer.add_argument("--fichier", default=None, metavar="CHEMIN",
                           help="lire le texte dans un fichier UTF-8 (au lieu de l'argument)")
    restituer.add_argument("--langue", choices=("fr", "en"), default=None,
                           help="indice de langue (fr/en) ; sans lui, le bloc détecte")
    restituer.add_argument("--contexte", default=None,
                           help="le texte qui précède (mémoire de discours)")
    restituer.add_argument("--json", action="store_true",
                           help="sortie JSON (restitution, miroir, contrôle négatif ; "
                                "rôles avec --roles)")
    restituer.set_defaults(fonction=cmd_restituer)
    return parseur


def main(argv: list[str] | None = None) -> int:
    # un stdout non-UTF-8 ne doit pas faire planter l'en-tête (« — ») : on tolère les remplacements
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    brut = list(sys.argv[1:] if argv is None else argv)
    args = construire_parseur().parse_args(_normaliser_tagger(brut))
    args.tagger_mode = ("auto" if getattr(args, "tagger_auto", False)
                        else "api" if getattr(args, "tagger", False) else None)
    try:
        return args.fonction(args)
    except BrokenPipeError:
        # `drave analyser ... | head` : le lecteur a fermé la sortie, ce n'est pas une erreur.
        return 0
    except KeyboardInterrupt:
        print(f"{NOM}: interrompu", file=sys.stderr)
        return 1
    except CleTaggerRefusee as exc:
        # même dépendance manquante qu'une clé absente : code 4, message clair, rien sur stdout
        print(f"{NOM}: dépendance absente : {exc}", file=sys.stderr)
        return 4
    except Exception as exc:  # noqa: BLE001 — le point d'entrée rend un code, pas une trace
        print(f"{NOM}: erreur : {type(exc).__name__} : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
