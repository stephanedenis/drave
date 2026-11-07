"""restitution.py — la restitution v0 : annotation → surface, et le miroir.

La **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent
les caractères — **sans lire** `Annotation.texte`. Les niveaux `mot` et `pos` sont mesurés
comme des sorties plus pauvres : ils disent ce que la couche de surface ajoute.

Le **miroir** est la règle 6 du dépôt : `fidelite` est binaire (1.0 si la sortie égale la
source), et `miroir` est le minimum des trois fidélités (surface, mots, pos). C'est la
définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour ne pas en
avoir deux. `fidelite_caractere` ajoute une distance de Levenshtein normalisée : elle
distingue « presque fidèle » de « fidèle » et documente la perte de la ponctuation.

Le **contrôle négatif** mélange les graphèmes (graine fixe) et en retire un : les deux
doivent casser la fidélité. Sans lui, un codec qui recopie la source ne prouverait rien.
"""
from __future__ import annotations

import pathlib
import random
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
from tools.tests.linguistique import miroir as _miroir  # noqa: E402

SCHEMA = "drave.restitution"
VERSION = 1
NIVEAUX = ("graphème", "mot", "pos")
NOMS = {"graphème": "surface", "mot": "mots", "pos": "pos"}

# La définition du miroir, publiée dans le JSON : un client n'a pas à la deviner.
DEFINITION_MIROIR = (
    "minimum des fidélités binaires de la surface (graphème), des mots et des POS ; "
    "une sortie n'est fidèle que si elle reproduit exactement la source"
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
