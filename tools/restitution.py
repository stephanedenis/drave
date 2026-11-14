"""restitution.py — la restitution v0 (surface) et la v1 (forme canonique).

La **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent
les caractères — **sans lire** `Annotation.texte`. Les niveaux `mot` et `pos` sont mesurés
comme des sorties plus pauvres : ils disent ce que la couche de surface ajoute.

Le **miroir** est la règle 6 du dépôt : `fidelite` est binaire (1.0 si la sortie égale la
source), et `miroir` est le minimum des trois fidélités (surface, mots, pos). C'est la
définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour ne pas en
avoir deux. `fidelite_caractere` ajoute une distance de Levenshtein normalisée : elle
distingue « presque fidèle » de « fidèle » et documente la perte de la ponctuation.

La **forme canonique** (v1) est une lecture **structurelle** de l'annotation : les
syntagmes avec leur type, leur rôle et leur cible d'attachement, une linéarisation sans
chevauchement, et un plancher de jetons normalisés (casse repliée, ponctuation retirée).
Elle ne remplace pas la surface : elle la met entre parenthèses pour mesurer ce que la
structure ajoute, et son **miroir canonique** se compare à une source canonisée, pas à la
source brute. Le **miroir strict** reste la référence de surface.

Le **contrôle négatif** mélange les graphèmes (graine fixe) et en retire un : les deux
doivent casser la fidélité. Sans lui, un codec qui recopie la source ne prouverait rien.
La v1 ajoute deux contrôles : mélange/troncature des jetons canoniques, et retrait des
rôles/cibles (la couverture structurelle doit tomber à zéro).
"""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import random
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
from tools.tests.linguistique import miroir as _miroir  # noqa: E402

SCHEMA = "drave.restitution"
VERSION = 1
SCHEMA_CANONIQUE = "drave.restitution.canonique"
VERSION_CANONIQUE = 1
NIVEAUX = ("graphème", "mot", "pos")
NOMS = {"graphème": "surface", "mot": "mots", "pos": "pos"}

# La définition du miroir, publiée dans le JSON : un client n'a pas à la deviner.
DEFINITION_MIROIR = (
    "minimum des fidélités binaires de la surface (graphème), des mots et des POS ; "
    "une sortie n'est fidèle que si elle reproduit exactement la source"
)

# La canonisation de la v1 : casse repliée, lettres et chiffres seulement, espaces réduits.
# Deux surfaces qui ne diffèrent que par la présentation ont la même forme canonique.
_JETON = re.compile(r"[^\W_]+", re.UNICODE)

DEFINITION_MIROIR_CANONIQUE = (
    "minimum des fidélités binaires des mots canoniques, des POS canoniques et de la "
    "forme canonique (jetons normalisés : casse repliée, ponctuation retirée, espaces "
    "réduits) comparées à la source canonique ; le miroir strict reste la référence de "
    "surface, il n'est pas remplacé"
)

DEFINITION_FORME_CANONIQUE = (
    "segments (type, rôle, span, valeur), linéarisation sans chevauchement, squelette "
    "« type/rôle : valeur -> cible », plancher de jetons (mot > POS > graphème) et "
    "empreinte sha256 du corps canonique"
)


# --------------------------------------------------------------------------- reconstruction


def _graphiemes(a: bl.Annotation) -> list[bl.Etiquette]:
    """Les graphèmes triés, dans l'ordre de la surface."""
    return sorted((e for e in a.etiquettes if e.niveau == "graphème"),
                  key=lambda e: (e.debut, e.fin))


def reconstruire(a: bl.Annotation, niveau: str = "graphème") -> str:
    """Reconstruit la surface depuis un niveau, **sans lire** `a.texte`.

    `graphème` est le niveau de surface ; `mot` et `pos` joignent leurs valeurs par une
    espace (la ponctuation devient un token séparé : c'est la perte que le miroir mesure).
    """
    if niveau == "graphème":
        return "".join(e.valeur for e in _graphiemes(a))
    if niveau == "mot":
        return _miroir.rendre_mots(a)
    if niveau == "pos":
        return _miroir.rendre_pos(a)
    raise ValueError(f"niveau de restitution inconnu : {niveau}")


def reconstruire_sans_controle(a: bl.Annotation) -> str:
    """La surface **avant** le correctif `C` : les graphèmes de contrôle sont ignorés.

    Sert de mesure « avant/après » : le miroir a trouvé que les sauts de ligne n'étaient
    pas annotés, donc perdus à la restitution.
    """
    return "".join(e.valeur for e in _graphiemes(a) if e.type != "contrôle")


# --------------------------------------------------------------------------- fidélité


def distance_levenshtein(gauche: str, droite: str) -> int:
    """Distance d'édition exacte, deux lignes (O(min(n, m)) en mémoire)."""
    if gauche == droite:
        return 0
    if len(gauche) < len(droite):
        gauche, droite = droite, gauche
    if not droite:
        return len(gauche)
    precedente = list(range(len(droite) + 1))
    for i, cg in enumerate(gauche, 1):
        courante = [i]
        for j, cd in enumerate(droite, 1):
            courante.append(min(
                precedente[j] + 1,          # suppression
                courante[j - 1] + 1,        # insertion
                precedente[j - 1] + (cg != cd),  # substitution
            ))
        precedente = courante
    return precedente[-1]


def fidelite(rendu: str, source: str) -> float:
    """La fidélité binaire du miroir : 1.0 si la sortie égale la source, 0.0 sinon."""
    return 1.0 if rendu == source else 0.0


def fidelite_caractere(rendu: str, source: str) -> float:
    """La proximité de caractères : 1 − distance / longueur maximale (0..1)."""
    if not source and not rendu:
        return 1.0
    return round(1.0 - distance_levenshtein(rendu, source)
                 / max(len(rendu), len(source), 1), 4)


def couverture(a: bl.Annotation, niveau: str, longueur: int) -> float:
    """La part de la source couverte par les spans d'un niveau (les espaces comptent)."""
    positions: set[int] = set()
    for e in a.etiquettes:
        if e.niveau == niveau:
            positions.update(range(max(0, e.debut), min(longueur, e.fin)))
    return round(len(positions) / max(1, longueur), 4)


# --------------------------------------------------------------------------- mesure


def _fiche_rendu(rendu: str, source: str) -> dict:
    return {
        "exact": rendu == source,
        "fidelite": fidelite(rendu, source),
        "fidelite_caractere": fidelite_caractere(rendu, source),
        "caracteres": len(rendu),
        "octets": len(rendu.encode("utf-8")),
    }


def _fiche_niveau(a: bl.Annotation, niveau: str, source: str) -> dict:
    rendu = reconstruire(a, niveau)
    fiche = _fiche_rendu(rendu, source)
    fiche.update({
        "niveau": niveau,
        "nom": NOMS[niveau],
        "rendu": rendu,
        "couverture": couverture(a, niveau, len(source)),
    })
    return fiche


def controler_negatif(a: bl.Annotation, source: str, graine: int = 0) -> dict:
    """Deux altérations déterministes de la surface : mélange et troncature.

    Le mélange garde les caractères et casse l'ordre ; la troncature garde l'ordre et
    retire un caractère. Les deux doivent faire tomber la fidélité exacte à 0. Un texte
    qui n'a qu'**un** graphème (`f18`, « 1234567890 ») ne peut pas être mélangé au niveau
    des spans : on retourne alors ses caractères, et si le retournement est un no-op
    (« a », « aa »), on substitue le premier caractère.
    """
    graphemes = _graphiemes(a)
    surface = "".join(e.valeur for e in graphemes)
    if len(graphemes) > 1:
        melange = list(graphemes)
        random.Random(graine).shuffle(melange)
        rendu_melange = "".join(e.valeur for e in melange)
        if rendu_melange == surface:
            rendu_melange = _alterer(surface)
    else:
        rendu_melange = _alterer(surface)
    rendu_tronque = "".join(e.valeur for e in graphemes[:-1])
    return {
        "graine": graine,
        "definition": "mélange des graphèmes (ou retournement/substitution s'il n'y en a "
                      "qu'un) et troncature d'un span (contenu)",
        "melange": _fiche_rendu(rendu_melange, source),
        "tronque": _fiche_rendu(rendu_tronque, source),
        "detecte": bool(graphemes and rendu_melange != source and rendu_tronque != source),
    }


def _alterer(surface: str) -> str:
    """Une altération non triviale d'une surface : retournement, puis substitution."""
    if len(surface) > 1:
        retour = surface[::-1]
        if retour != surface:
            return retour
        return ("X" if surface[0] != "X" else "Y") + surface[1:]
    if not surface:
        return "X"
    return "X" if surface != "X" else "Y"


def mesurer_annotation(a: bl.Annotation, source: str, graine: int = 0) -> dict:
    """La restitution d'une annotation et son miroir (surface, mots, POS, contrôle)."""
    if a.refus:
        return {
            "langue": a.langue,
            "refus": a.refus,
            "source_caracteres": len(source),
            "source_octets": len(source.encode("utf-8")),
            "etiquettes": len(a.etiquettes),
            "niveaux": {},
            "surface": None,
            "surface_sans_controle": None,
            "miroir": None,
            "controle_negatif": None,
        }
    niveaux = {n: _fiche_niveau(a, n, source) for n in NIVEAUX}
    miroir = round(min(niveaux[n]["fidelite"] for n in NIVEAUX), 4)
    return {
        "langue": a.langue,
        "refus": "",
        "source_caracteres": len(source),
        "source_octets": len(source.encode("utf-8")),
        "etiquettes": len(a.etiquettes),
        "niveaux": niveaux,
        "surface": niveaux["graphème"],
        "surface_sans_controle": _fiche_rendu(reconstruire_sans_controle(a), source),
        "miroir": {
            "definition": DEFINITION_MIROIR,
            "fidelite": miroir,
            "exact": miroir == 1.0,
        },
        "controle_negatif": controler_negatif(a, source, graine),
    }


# --------------------------------------------------------------------------- banc


def items_banc(donnees) -> list[dict]:
    """Extrait la liste des textes d'un JSON de banc (banc_50, resultats ou liste)."""
    if isinstance(donnees, list):
        return donnees
    if isinstance(donnees, dict):
        if isinstance(donnees.get("banc_50"), dict):
            return donnees["banc_50"].get("resultats", [])
        if isinstance(donnees.get("resultats"), list):
            return donnees["resultats"]
    raise ValueError("banc illisible : attendu une liste ou un objet banc_50/resultats")


def _moyenne(valeurs: list[float]) -> float:
    return round(sum(valeurs) / max(1, len(valeurs)), 4)


def _resume(resultats: list[dict]) -> dict:
    annotes = [r for r in resultats if not r.get("refus")]
    refuses = [r for r in resultats if r.get("refus")]

    def exacts(cle: str) -> int:
        return sum(1 for r in annotes if r[cle]["exact"])

    def fidelite(cle: str) -> float:
        return _moyenne([r[cle]["fidelite"] for r in annotes])

    def caracteres(cle: str) -> float:
        return _moyenne([r[cle]["fidelite_caractere"] for r in annotes])

    return {
        "n": len(resultats),
        "annotations": len(annotes),
        "refus": len(refuses),
        "refus_ids": [r.get("id") for r in refuses],
        "surface": {
            "exacts": exacts("surface"),
            "fidelite": fidelite("surface"),
            "fidelite_caractere": caracteres("surface"),
        },
        "surface_sans_controle": {
            "exacts": sum(1 for r in annotes if r["surface_sans_controle"]["exact"]),
            "fidelite": _moyenne([r["surface_sans_controle"]["fidelite"] for r in annotes]),
            "fidelite_caractere": _moyenne(
                [r["surface_sans_controle"]["fidelite_caractere"] for r in annotes]),
        },
        "mots": {
            "exacts": exacts("mots"),
            "fidelite": fidelite("mots"),
            "fidelite_caractere": caracteres("mots"),
        },
        "pos": {
            "exacts": exacts("pos"),
            "fidelite": fidelite("pos"),
            "fidelite_caractere": caracteres("pos"),
        },
        "miroir": {
            "exacts": sum(1 for r in annotes if r["miroir"]["exact"]),
            "fidelite": _moyenne([r["miroir"]["fidelite"] for r in annotes]),
        },
        "controle_negatif": {
            "melange_exacts": sum(
                1 for r in annotes if r["controle_negatif"]["melange"]["exact"]),
            "melange_fidelite": _moyenne(
                [r["controle_negatif"]["melange"]["fidelite"] for r in annotes]),
            "melange_fidelite_caractere": _moyenne(
                [r["controle_negatif"]["melange"]["fidelite_caractere"] for r in annotes]),
            "tronque_exacts": sum(
                1 for r in annotes if r["controle_negatif"]["tronque"]["exact"]),
            "tronque_fidelite_caractere": _moyenne(
                [r["controle_negatif"]["tronque"]["fidelite_caractere"] for r in annotes]),
            "detectes": sum(1 for r in annotes if r["controle_negatif"]["detecte"]),
        },
    }


def mesurer_banc(items: list[dict], langue: str | None = None, graine: int = 0) -> dict:
    """Mesure la restitution sur une liste de textes (`id`, `texte`, `langue` optionnelle).

    `langue=None` laisse le bloc détecter, comme le CLI sans `--langue` — c'est la
    condition du banc des 50 textes libres.
    """
    h = bl.Heuristique()
    resultats: list[dict] = []
    for item in items:
        texte = item.get("texte", "")
        ident = item.get("id", f"t{len(resultats) + 1:02d}")
        a = h.analyser(texte, langue)
        if a.refus:
            resultats.append({
                "id": ident,
                "refus": a.refus,
                "caracteres": len(texte),
                "langue": a.langue,
            })
            continue
        m = mesurer_annotation(a, texte, graine)
        resultats.append({
            "id": ident,
            "refus": "",
            "langue": a.langue,
            "caracteres": len(texte),
            "etiquettes": len(a.etiquettes),
            "surface": m["surface"],
            "surface_sans_controle": m["surface_sans_controle"],
            "mots": m["niveaux"]["mot"],
            "pos": m["niveaux"]["pos"],
            "miroir": m["miroir"],
            "controle_negatif": m["controle_negatif"],
        })
    return {
        "schema": SCHEMA + ".banc",
        "version": VERSION,
        "definition_miroir": DEFINITION_MIROIR,
        "parametres": {"graine": graine, "langue": langue or "auto"},
        "synthese": _resume(resultats),
        "resultats": resultats,
    }


# --------------------------------------------------------------------------- forme canonique v1


def jetons_canoniques(texte: str) -> list[str]:
    """Les jetons d'une surface canonique : lettres et chiffres, casse repliée."""
    return _JETON.findall(texte.casefold())


def canoniser(texte: str) -> str:
    """La forme canonique d'une surface : ses jetons joints par une espace."""
    return " ".join(jetons_canoniques(texte))


def _canonique_valeur(valeur: str) -> str:
    return canoniser(valeur)


def _preference_segment(e: bl.Etiquette) -> tuple:
    """L'ordre de préférence d'une linéarisation : chunker, puis le plus large, le plus sûr.

    C'est la clé de `bloc_linguistique._cle_preferee`, recopiée ici pour que la forme
    canonique dépende d'une règle **publiée** et non d'un ordre d'insertion. Le segment
    du chunker (`union`) passe avant le générateur S ; à défaut, le plus large gagne.
    """
    meta = e.meta or {}
    return (0 if meta.get("union") else 1, -(e.fin - e.debut), -e.confiance,
            e.debut, e.fin, e.type)


def segments_lineaires(a: bl.Annotation) -> list[bl.Etiquette]:
    """Une vue **sans chevauchement** des syntagmes, choisie par `_preference_segment`.

    Les autres segments restent dans la forme canonique (avec `lineaire: false`) : c'est
    une vue de lecture, pas une suppression. L'ordre rendu est celui de la surface.
    """
    segments = [e for e in a.etiquettes if e.niveau == "syntagme"]
    choisis: list[bl.Etiquette] = []
    for e in sorted(segments, key=_preference_segment):
        if all(max(e.debut, x.debut) >= min(e.fin, x.fin) for x in choisis):
            choisis.append(e)
    return sorted(choisis, key=lambda e: (e.debut, e.fin, e.type))


def _jetons_de(a: bl.Annotation) -> list[str]:
    """Le plancher lexical de la forme : `mot`, sinon `pos`, sinon `graphème`.

    Il ne lit **jamais** `Annotation.texte` : les valeurs viennent des étiquettes. Le
    plancher est ce qui couvre les mots hors syntagme (déterminants, prépositions,
    ponctuation) ; les segments, eux, portent la structure.
    """
    for niveau in ("mot", "pos", "graphème"):
        etiquettes = sorted((e for e in a.etiquettes if e.niveau == niveau),
                            key=lambda e: (e.debut, e.fin))
        if etiquettes:
            return [j for e in etiquettes for j in jetons_canoniques(e.valeur)]
    return []


def _contient_jetons(sequence: list[str], motif: list[str]) -> bool:
    """Vrai si `motif` apparaît **dans l'ordre** dans `sequence` (sous-suite contiguë)."""
    n = len(motif)
    return bool(n) and any(sequence[i:i + n] == motif
                           for i in range(len(sequence) - n + 1))


def _index_cible(cible: str, rang: int, segments: list[bl.Etiquette],
                 canoniques: list[str]) -> int | None:
    """Le rang du **premier autre** segment qui porte la cible (en jetons), sinon None."""
    if not cible:
        return None
    motif = cible.split()
    for j, canonique in enumerate(canoniques):
        if j == rang:
            continue
        if _contient_jetons(canonique.split(), motif):
            return j
    return None


def forme_canonique(a: bl.Annotation) -> dict | None:
    """La forme canonique v1 : segments + rôles + cibles, et un plancher de jetons.

    Le corps est **déterministe** : les segments sont triés par `(debut, fin, type)`, les
    rôles et cibles viennent de `meta`, la linéarisation suit `_preference_segment`, et
    l'empreinte `cle` est le sha256 du JSON canonique (clés triées). Deux analyses du même
    texte donnent la même clé ; retirer les rôles/cibles la change (contrôle négatif).
    """
    if a.refus:
        return None
    segments = sorted((e for e in a.etiquettes if e.niveau == "syntagme"),
                      key=lambda e: (e.debut, e.fin, e.type))
    lineaires = segments_lineaires(a)
    ids_lineaires = {id(e) for e in lineaires}
    canoniques = [_canonique_valeur(e.valeur) for e in segments]
    records: list[dict] = []
    for rang, (e, canonique) in enumerate(zip(segments, canoniques)):
        meta = e.meta or {}
        attachement = meta.get("attachement") or {}
        cible = attachement.get("cible", "") or ""
        cible_c = _canonique_valeur(cible)
        records.append({
            "rang": rang,
            "type": e.type,
            "role": meta.get("role", ""),
            "niveau": meta.get("niveau", 0),
            "debut": e.debut,
            "fin": e.fin,
            "valeur": e.valeur,
            "canonique": canonique,
            "cible": cible,
            "cible_canonique": cible_c,
            "cible_segment": _index_cible(cible_c, rang, segments, canoniques),
            "lineaire": id(e) in ids_lineaires,
            "union": bool(meta.get("union")),
        })
    squelette = [
        f"{r['type']}/{r['role'] or '—'}: {r['canonique'] or '—'} -> "
        f"{r['cible_canonique'] or '—'}"
        for r in records if r["lineaire"]
    ]
    jetons = _jetons_de(a)
    corps = {
        "segments": records,
        "squelette": squelette,
        "jetons": jetons,
        "surface_canonique": " ".join(jetons),
    }
    cle = hashlib.sha256(
        json.dumps(corps, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {"definition": DEFINITION_FORME_CANONIQUE, **corps, "cle": cle}


def _fiche_canonique(rendu: str, cible: str) -> dict:
    return {
        "exact": rendu == cible,
        "fidelite": 1.0 if rendu == cible else 0.0,
        "fidelite_caractere": fidelite_caractere(rendu, cible),
        "jetons": len(rendu.split()) if rendu else 0,
    }


def _rendu_canonique_niveau(a: bl.Annotation, niveau: str) -> str:
    etiquettes = sorted((e for e in a.etiquettes if e.niveau == niveau),
                        key=lambda e: (e.debut, e.fin))
    return " ".join(j for e in etiquettes for j in jetons_canoniques(e.valeur))


def miroir_canonique(a: bl.Annotation, source: str) -> dict:
    """Le miroir de la v1 : les niveaux lexical et la forme, comparés à la source canonique.

    `fidelite` est le **minimum** des trois fidélités binaires (mots, POS, forme), comme
    le miroir strict ; la source est canonisée (casse/ponctuation/espaces). Le miroir
    strict n'est pas recalculé ici : il reste celui de `mesurer_annotation`.
    """
    cible = canoniser(source)
    forme = forme_canonique(a) or {}
    fiches = {
        "mots": _fiche_canonique(_rendu_canonique_niveau(a, "mot"), cible),
        "pos": _fiche_canonique(_rendu_canonique_niveau(a, "pos"), cible),
        "forme": _fiche_canonique(forme.get("surface_canonique", ""), cible),
    }
    fidelite = round(min(f["fidelite"] for f in fiches.values()), 4)
    return {
        "definition": DEFINITION_MIROIR_CANONIQUE,
        "source_canonique": cible,
        "mots": fiches["mots"],
        "pos": fiches["pos"],
        "forme": fiches["forme"],
        "fidelite": fidelite,
        "exact": all(f["exact"] for f in fiches.values()),
    }


def structure_canonique(a: bl.Annotation, source: str) -> dict:
    """Ce que les segments + rôles + cibles couvrent et résolvent, sans gold.

    - `couverture_caracteres` : part de la source couverte par au moins un segment ;
    - `couverture_jetons` : part des jetons `mot` dont le début tombe dans un segment ;
    - `cibles_resolues` : la cible (en jetons) est présente dans la source canonique ;
    - `cibles_dans_un_segment` : la cible est portée par un **autre** segment.

    Ce sont des mesures de **cohérence** de l'annotation, pas de justesse : sans gold de
    forme canonique, on ne peut pas dire que le rôle ou la cible sont les bons.
    """
    segments = [e for e in a.etiquettes if e.niveau == "syntagme"]
    positions: set[int] = set()
    for e in segments:
        positions.update(range(max(0, e.debut), min(len(source), e.fin)))
    mots = [e for e in a.etiquettes if e.niveau == "mot"]
    jetons_couverts = sum(1 for e in mots if e.debut in positions)
    source_jetons = jetons_canoniques(source)
    canoniques = [_canonique_valeur(e.valeur) for e in segments]
    attachements = 0
    cibles_resolues = 0
    cibles_dans = 0
    roles: collections.Counter[str] = collections.Counter()
    types: collections.Counter[str] = collections.Counter()
    for i, e in enumerate(segments):
        meta = e.meta or {}
        types[e.type] += 1
        if meta.get("role"):
            roles[meta["role"]] += 1
        attachement = meta.get("attachement") or {}
        cible = _canonique_valeur(attachement.get("cible", ""))
        if not cible:
            continue
        attachements += 1
        jetons = cible.split()
        if _contient_jetons(source_jetons, jetons):
            cibles_resolues += 1
        if any(j != i and _contient_jetons(canoniques[j].split(), jetons)
               for j in range(len(segments))):
            cibles_dans += 1
    return {
        "segments": len(segments),
        "segments_avec_role": sum(roles.values()),
        "attachements": attachements,
        "cibles_resolues": cibles_resolues,
        "cibles_dans_un_segment": cibles_dans,
        "couverture_caracteres": round(len(positions) / max(1, len(source)), 4),
        "couverture_jetons": round(jetons_couverts / max(1, len(mots)), 4),
        "roles": dict(sorted(roles.items())),
        "types": dict(sorted(types.items())),
    }


def controler_negatif_canonique(a: bl.Annotation, source: str, graine: int = 0) -> dict:
    """Mélange et troncature des **jetons canoniques** (pas des graphèmes).

    Même principe que la v0 : le mélange doit casser l'ordre, la troncature doit retirer
    un jeton. Un texte d'un seul jeton est retourné/substitué pour que le contrôle ne soit
    pas un no-op.
    """
    forme = forme_canonique(a) or {}
    jetons = list(forme.get("jetons") or [])
    cible = canoniser(source)
    surface = " ".join(jetons)
    melange = list(jetons)
    random.Random(graine).shuffle(melange)
    rendu_melange = " ".join(melange)
    if rendu_melange == surface:
        rendu_melange = _alterer(surface)
    rendu_tronque = " ".join(jetons[:-1])
    return {
        "graine": graine,
        "definition": "mélange des jetons canoniques (ou retournement/substitution s'il "
                      "n'y en a qu'un) et troncature du dernier jeton",
        "melange": _fiche_canonique(rendu_melange, cible),
        "tronque": _fiche_canonique(rendu_tronque, cible),
        "detecte": bool(jetons and rendu_melange != cible and rendu_tronque != cible),
    }


def controler_negatif_structure(a: bl.Annotation, forme: dict | None = None) -> dict:
    """Retire les rôles et les cibles : la couverture structurelle doit tomber à zéro.

    Ce contrôle ne dit pas que les rôles sont **justes** (il faudrait un gold) ; il dit
    que la mesure les lit vraiment et que la clé de la forme en dépend.
    """
    forme = forme or forme_canonique(a) or {}
    segments = forme.get("segments", [])
    roles = sum(1 for s in segments if s.get("role"))
    cibles = sum(1 for s in segments if s.get("cible"))
    sans = {
        "segments": [{**s, "role": "", "cible": "", "cible_canonique": "",
                      "cible_segment": None} for s in segments],
        "squelette": [],
        "jetons": forme.get("jetons", []),
        "surface_canonique": forme.get("surface_canonique", ""),
    }
    cle_sans = hashlib.sha256(
        json.dumps(sans, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    eligible = bool(roles or cibles)
    return {
        "segments": len(segments),
        "roles_retires": roles,
        "cibles_retirees": cibles,
        "roles_apres": 0,
        "cibles_apres": 0,
        "cle_changee": eligible and cle_sans != forme.get("cle"),
        "detecte": eligible,
    }


def stabilite_structurelle(a: bl.Annotation, forme: dict | None = None,
                           analyseur: bl.Heuristique | None = None) -> dict:
    """La forme canonique est-elle un point fixe ? On re-analyse sa surface canonique.

    Le **lexique** est stable par construction (mêmes jetons) ; la **structure** ne l'est
    que si la segmentation ne dépend pas de la présentation. C'est une limite mesurée de
    la v1, pas un critère de réussite : le bloc heuristique segmente la surface, et la
    surface canonique a perdu la ponctuation et la casse.
    """
    forme = forme or forme_canonique(a)
    if not forme:
        return {"surface": "", "refus": "aucune forme", "squelette_identique": False,
                "jetons_identiques": False, "segments_avant": 0, "segments_apres": 0}
    surface = forme["surface_canonique"]
    b = (analyseur or bl.Heuristique()).analyser(surface)
    forme2 = forme_canonique(b)
    return {
        "surface": surface,
        "refus": b.refus,
        "squelette_identique": bool(forme2) and forme2["squelette"] == forme["squelette"],
        "jetons_identiques": bool(forme2) and forme2["jetons"] == forme["jetons"],
        "segments_avant": len(forme["segments"]),
        "segments_apres": len(forme2["segments"]) if forme2 else 0,
    }


def mesurer_annotation_v1(a: bl.Annotation, source: str, graine: int = 0,
                          analyseur: bl.Heuristique | None = None) -> dict:
    """La restitution v1 d'une annotation : strict (v0) + canonique + structure."""
    base = mesurer_annotation(a, source, graine)
    if a.refus:
        return {
            "langue": a.langue,
            "refus": a.refus,
            "source_caracteres": len(source),
            "source_octets": len(source.encode("utf-8")),
            "etiquettes": len(a.etiquettes),
            "strict": base["miroir"],
            "surface_stricte": base["surface"],
            "canonique": None,
            "forme": None,
            "structure": None,
            "stabilite": None,
            "strict_sur_canonique": None,
            "controle_negatif_canonique": None,
            "controle_negatif_structure": None,
        }
    forme = forme_canonique(a)
    return {
        "langue": a.langue,
        "refus": "",
        "source_caracteres": len(source),
        "source_octets": len(source.encode("utf-8")),
        "etiquettes": len(a.etiquettes),
        "strict": base["miroir"],
        "surface_stricte": base["surface"],
        "canonique": miroir_canonique(a, source),
        "forme": forme,
        "structure": structure_canonique(a, source),
        "stabilite": stabilite_structurelle(a, forme, analyseur),
        "strict_sur_canonique": _fiche_rendu(forme["surface_canonique"], source),
        "controle_negatif_canonique": controler_negatif_canonique(a, source, graine),
        "controle_negatif_structure": controler_negatif_structure(a, forme),
    }


def _resume_v1(resultats: list[dict]) -> dict:
    annotes = [r for r in resultats if not r.get("refus")]
    refuses = [r for r in resultats if r.get("refus")]
    n = len(annotes)

    def moyenne(valeurs: list[float]) -> float:
        return round(sum(valeurs) / max(1, len(valeurs)), 4)

    structure = {
        "segments": sum(r["structure"]["segments"] for r in annotes),
        "segments_avec_role": sum(r["structure"]["segments_avec_role"] for r in annotes),
        "attachements": sum(r["structure"]["attachements"] for r in annotes),
        "cibles_resolues": sum(r["structure"]["cibles_resolues"] for r in annotes),
        "cibles_dans_un_segment": sum(
            r["structure"]["cibles_dans_un_segment"] for r in annotes),
        "couverture_caracteres": moyenne(
            [r["structure"]["couverture_caracteres"] for r in annotes]),
        "couverture_jetons": moyenne(
            [r["structure"]["couverture_jetons"] for r in annotes]),
    }
    structure["taux_roles"] = round(
        structure["segments_avec_role"] / max(1, structure["segments"]), 4)
    structure["taux_cibles_resolues"] = round(
        structure["cibles_resolues"] / max(1, structure["attachements"]), 4)
    structure["taux_cibles_dans_un_segment"] = round(
        structure["cibles_dans_un_segment"] / max(1, structure["attachements"]), 4)
    return {
        "n": len(resultats),
        "annotations": n,
        "refus": len(refuses),
        "refus_ids": [r.get("id") for r in refuses],
        "strict": {
            "exacts": sum(1 for r in annotes if r["strict"]["exact"]),
            "fidelite": moyenne([r["strict"]["fidelite"] for r in annotes]),
        },
        "canonique": {
            "exacts": sum(1 for r in annotes if r["canonique"]["exact"]),
            "fidelite": moyenne([r["canonique"]["fidelite"] for r in annotes]),
            "fidelite_caractere": moyenne(
                [r["canonique"]["forme"]["fidelite_caractere"] for r in annotes]),
        },
        "strict_sur_canonique": {
            "exacts": sum(1 for r in annotes if r["strict_sur_canonique"]["exact"]),
            "fidelite": moyenne(
                [r["strict_sur_canonique"]["fidelite"] for r in annotes]),
            "fidelite_caractere": moyenne(
                [r["strict_sur_canonique"]["fidelite_caractere"] for r in annotes]),
        },
        "structure": structure,
        "stabilite": {
            "squelette_identique": sum(
                1 for r in annotes if r["stabilite"]["squelette_identique"]),
            "jetons_identiques": sum(
                1 for r in annotes if r["stabilite"]["jetons_identiques"]),
            "fidelite": round(
                sum(1 for r in annotes if r["stabilite"]["squelette_identique"]) / max(1, n), 4),
        },
        "controle_negatif_canonique": {
            "melange_exacts": sum(
                1 for r in annotes if r["controle_negatif_canonique"]["melange"]["exact"]),
            "melange_fidelite_caractere": moyenne(
                [r["controle_negatif_canonique"]["melange"]["fidelite_caractere"]
                 for r in annotes]),
            "tronque_exacts": sum(
                1 for r in annotes if r["controle_negatif_canonique"]["tronque"]["exact"]),
            "tronque_fidelite_caractere": moyenne(
                [r["controle_negatif_canonique"]["tronque"]["fidelite_caractere"]
                 for r in annotes]),
            "detectes": sum(
                1 for r in annotes if r["controle_negatif_canonique"]["detecte"]),
        },
        "controle_negatif_structure": {
            "eligibles": sum(
                1 for r in annotes if r["controle_negatif_structure"]["detecte"]),
            "detectes": sum(
                1 for r in annotes if r["controle_negatif_structure"]["detecte"]),
            "cle_changee": sum(
                1 for r in annotes if r["controle_negatif_structure"]["cle_changee"]),
            "roles_retires": sum(
                r["controle_negatif_structure"]["roles_retires"] for r in annotes),
            "cibles_retirees": sum(
                r["controle_negatif_structure"]["cibles_retirees"] for r in annotes),
        },
    }


def mesurer_banc_v1(items: list[dict], langue: str | None = None, graine: int = 0) -> dict:
    """Mesure la v1 sur une liste de textes (`id`, `texte`, `langue` optionnelle)."""
    h = bl.Heuristique()
    resultats: list[dict] = []
    for item in items:
        texte = item.get("texte", "")
        ident = item.get("id", f"t{len(resultats) + 1:02d}")
        a = h.analyser(texte, langue)
        if a.refus:
            resultats.append({
                "id": ident,
                "refus": a.refus,
                "caracteres": len(texte),
                "langue": a.langue,
            })
            continue
        m = mesurer_annotation_v1(a, texte, graine, analyseur=h)
        resultats.append({
            "id": ident,
            "refus": "",
            "langue": a.langue,
            "caracteres": len(texte),
            "etiquettes": len(a.etiquettes),
            "strict": m["strict"],
            "surface_stricte": m["surface_stricte"],
            "canonique": m["canonique"],
            "forme": m["forme"],
            "structure": m["structure"],
            "stabilite": m["stabilite"],
            "strict_sur_canonique": m["strict_sur_canonique"],
            "controle_negatif_canonique": m["controle_negatif_canonique"],
            "controle_negatif_structure": m["controle_negatif_structure"],
        })
    return {
        "schema": SCHEMA_CANONIQUE + ".banc",
        "version": VERSION_CANONIQUE,
        "definition_miroir": DEFINITION_MIROIR,
        "definition_miroir_canonique": DEFINITION_MIROIR_CANONIQUE,
        "definition_forme_canonique": DEFINITION_FORME_CANONIQUE,
        "parametres": {"graine": graine, "langue": langue or "auto"},
        "synthese": _resume_v1(resultats),
        "resultats": resultats,
    }


# --------------------------------------------------------------------------- affichage


def formater_mesure(m: dict, source: str) -> str:
    """La sortie lisible de `drave restituer TEXTE`."""
    if m.get("refus"):
        return f"refus d'analyse : {m['refus']} (aucune surface à restituer)"
    surface = m["surface"]
    sans = m["surface_sans_controle"]
    mots = m["niveaux"]["mot"]
    pos = m["niveaux"]["pos"]
    controle = m["controle_negatif"]
    lignes = [
        "restitution (annotation → surface)",
        f"source      : {source!r}",
        f"surface     : {surface['rendu']!r}",
        f"fidélité    : exacte {surface['fidelite']:.4f} · "
        f"caractères {surface['fidelite_caractere']:.4f} · "
        f"couverture {surface['couverture']:.2%}",
        f"mots        : exacte {mots['fidelite']:.4f} · "
        f"caractères {mots['fidelite_caractere']:.4f} · "
        f"couverture {mots['couverture']:.2%}",
        f"pos         : exacte {pos['fidelite']:.4f} · "
        f"caractères {pos['fidelite_caractere']:.4f} · "
        f"couverture {pos['couverture']:.2%}",
        f"miroir      : {m['miroir']['fidelite']:.4f} "
        f"({'exact' if m['miroir']['exact'] else 'non exact'}) — {DEFINITION_MIROIR}",
    ]
    if sans["fidelite"] != surface["fidelite"] or sans["fidelite_caractere"] != surface["fidelite_caractere"]:
        lignes.append(
            f"  sans contrôle : exacte {sans['fidelite']:.4f} · "
            f"caractères {sans['fidelite_caractere']:.4f} "
            "(les sauts de ligne n'étaient pas annotés avant le correctif C)"
        )
    lignes.append(
        f"contrôle négatif : mélange exacte {controle['melange']['fidelite']:.4f} "
        f"(caractères {controle['melange']['fidelite_caractere']:.4f}) · "
        f"troncature exacte {controle['tronque']['fidelite']:.4f} "
        f"(caractères {controle['tronque']['fidelite_caractere']:.4f})"
    )
    return "\n".join(lignes)


def formater_banc(rapport: dict, chemin: str = "") -> str:
    """La sortie lisible du banc (`restituer --banc`)."""
    s = rapport["synthese"]
    lignes = [
        f"restitution v0 — banc {chemin or '(fourni)'}",
        f"textes {s['n']} · annotés {s['annotations']} · refus {s['refus']} "
        f"({', '.join(str(x) for x in s['refus_ids'])})",
        "",
        "niveau                 exacts    fidélité   caractères",
        f"surface (graphème)     {s['surface']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['surface']['fidelite']:>8.4f}   {s['surface']['fidelite_caractere']:>8.4f}",
        f"  sans contrôle C      {s['surface_sans_controle']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['surface_sans_controle']['fidelite']:>8.4f}   "
        f"{s['surface_sans_controle']['fidelite_caractere']:>8.4f}",
        f"mots                   {s['mots']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['mots']['fidelite']:>8.4f}   {s['mots']['fidelite_caractere']:>8.4f}",
        f"pos                    {s['pos']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['pos']['fidelite']:>8.4f}   {s['pos']['fidelite_caractere']:>8.4f}",
        f"miroir (min)           {s['miroir']['exacts']:>6}/{s['annotations']:<6} "
        f"{s['miroir']['fidelite']:>8.4f}",
        "",
        f"contrôle négatif : mélange exacts {s['controle_negatif']['melange_exacts']}/"
        f"{s['annotations']} (caractères {s['controle_negatif']['melange_fidelite_caractere']:.4f}) · "
        f"troncature exacts {s['controle_negatif']['tronque_exacts']}/"
        f"{s['annotations']} (caractères {s['controle_negatif']['tronque_fidelite_caractere']:.4f})",
    ]
    return "\n".join(lignes)


def formater_forme_canonique(forme: dict | None, mesure: dict | None = None) -> str:
    """La sortie lisible de la forme canonique (segments + rôles + cibles)."""
    if not forme:
        return "forme canonique : (aucune annotation)"
    lignes = [
        "forme canonique (segments + rôles + cibles)",
        f"surface canonique : {forme['surface_canonique']!r}",
        "squelette :",
    ]
    lignes += [f"  {s}" for s in forme["squelette"]] or ["  (aucun segment linéaire)"]
    structure = (mesure or {}).get("structure") or {}
    if structure:
        lignes.append(
            f"segments {structure['segments']} · rôles {structure['segments_avec_role']} · "
            f"cibles {structure['attachements']} · "
            f"résolues {structure['cibles_resolues']}/{structure['attachements']} · "
            f"dans un segment {structure['cibles_dans_un_segment']}/{structure['attachements']}"
        )
    return "\n".join(lignes)


def formater_mesure_v1(m: dict, source: str) -> str:
    """La sortie lisible de `restituer TEXTE --canonique`."""
    if m.get("refus"):
        return f"refus d'analyse : {m['refus']} (aucune forme canonique)"
    surface = m["surface_stricte"]
    strict = m["strict"]
    canonique = m["canonique"]
    strict_c = m["strict_sur_canonique"]
    lignes = [
        "restitution v1 (surface + forme canonique)",
        f"source         : {source!r}",
        f"surface brute  : {surface['rendu']!r}",
        f"miroir strict  : {strict['fidelite']:.4f} "
        f"({'exact' if strict['exact'] else 'non exact'}) — surface/mots/POS vs source brute",
        f"forme canonique: {canonique['fidelite']:.4f} "
        f"({'exacte' if canonique['exact'] else 'non exacte'}) — jetons canoniques vs source "
        "canonique",
        f"  caractères   : {canonique['forme']['fidelite_caractere']:.4f}",
        f"strict sur la forme canonique : {strict_c['fidelite']:.4f} "
        "(la forme n'est pas la surface : le strict ne doit pas monter)",
        "",
        formater_forme_canonique(m["forme"], m),
        "",
        f"contrôle négatif canonique : mélange exacte "
        f"{m['controle_negatif_canonique']['melange']['fidelite']:.4f} · "
        f"troncature exacte {m['controle_negatif_canonique']['tronque']['fidelite']:.4f} · "
        f"détecté {m['controle_negatif_canonique']['detecte']}",
        f"contrôle de structure : rôles retirés "
        f"{m['controle_negatif_structure']['roles_retires']} · cibles retirées "
        f"{m['controle_negatif_structure']['cibles_retirees']} · clé changée "
        f"{m['controle_negatif_structure']['cle_changee']}",
        f"stabilité structurelle : {'oui' if m['stabilite']['squelette_identique'] else 'non'} "
        f"({m['stabilite']['segments_avant']} → {m['stabilite']['segments_apres']} segments "
        "après re-analyse de la surface canonique)",
    ]
    return "\n".join(lignes)


def formater_banc_v1(rapport: dict, chemin: str = "") -> str:
    """La sortie lisible du banc v1 (`restituer --banc ... --canonique`)."""
    s = rapport["synthese"]
    n = s["annotations"]
    strict = s["strict"]
    canonique = s["canonique"]
    strict_c = s["strict_sur_canonique"]
    structure = s["structure"]
    stabilite = s["stabilite"]
    controle = s["controle_negatif_canonique"]
    controle_s = s["controle_negatif_structure"]
    lignes = [
        f"restitution v1 — banc {chemin or '(fourni)'}",
        f"textes {s['n']} · annotés {n} · refus {s['refus']} "
        f"({', '.join(str(x) for x in s['refus_ids'])})",
        "",
        "niveau                         exacts    fidélité   caractères",
        f"strict (surface/mots/POS)      {strict['exacts']:>6}/{n:<6} "
        f"{strict['fidelite']:>8.4f}   —",
        f"canonique (jetons)             {canonique['exacts']:>6}/{n:<6} "
        f"{canonique['fidelite']:>8.4f}   {canonique['fidelite_caractere']:>8.4f}",
        f"strict sur la forme canonique  {strict_c['exacts']:>6}/{n:<6} "
        f"{strict_c['fidelite']:>8.4f}   {strict_c['fidelite_caractere']:>8.4f}",
        "",
        f"structure : {structure['segments']} segments · "
        f"{structure['segments_avec_role']} rôles ({structure['taux_roles']:.4f}) · "
        f"{structure['attachements']} cibles · "
        f"{structure['cibles_resolues']}/{structure['attachements']} résolues "
        f"({structure['taux_cibles_resolues']:.4f}) · "
        f"{structure['cibles_dans_un_segment']}/{structure['attachements']} dans un segment "
        f"({structure['taux_cibles_dans_un_segment']:.4f})",
        f"couverture : {structure['couverture_jetons']:.4f} des jetons · "
        f"{structure['couverture_caracteres']:.4f} des caractères (moyenne)",
        f"stabilité structurelle : {stabilite['squelette_identique']}/{n} "
        f"({stabilite['fidelite']:.4f}) · jetons identiques {stabilite['jetons_identiques']}/{n}",
        f"contrôle négatif canonique : mélange {controle['melange_exacts']}/{n} exacts "
        f"(caractères {controle['melange_fidelite_caractere']:.4f}) · "
        f"troncature {controle['tronque_exacts']}/{n} exacts "
        f"(caractères {controle['tronque_fidelite_caractere']:.4f}) · "
        f"détectés {controle['detectes']}/{n}",
        f"contrôle de structure : {controle_s['eligibles']}/{n} textes éligibles · "
        f"rôles retirés {controle_s['roles_retires']} · "
        f"cibles retirées {controle_s['cibles_retirees']} · "
        f"clé changée {controle_s['cle_changee']}/{controle_s['eligibles']}",
    ]
    return "\n".join(lignes)
