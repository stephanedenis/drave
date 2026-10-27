#!/usr/bin/env python3
"""universaux.py — la base fixe des universaux sémantiques des jeux.

Le protocole libre apprenait un vecteur `z` : il retrouvait l'article, mais ne
disait pas **ce qu'il contenait**. Ici, la sortie n'est plus un vecteur libre :
c'est un **code typé**, un tuple de champs fixes, chacun avec un vocabulaire fixe.
Deux conséquences, et c'est le but :

- l'embedding est **typé** : `jeu=carte`, `action=prendre`, `de=12`, `vers=28` ;
- il est **déterministe** : le même code se lit par `argmax`, sans seuil appris.

La base couvre les **coups** des cinq jeux (B5/B6) et les surfaces multilingues
(B7). Les champs sont des **universaux du jeu** (agent/action/source/cible/
matériel), pas des tokens : un `de` est une case, pas un mot.
"""
from __future__ import annotations

import hashlib
import json

JEUX = ("morpion", "echecs", "dames", "go", "cartes")
ACTIONS = ("deplacer", "prendre", "promouvoir", "jouer_case", "jouer_carte", "poser", "passer", "autre")
PROMOTIONS = (None, "q", "r", "b", "n")
ROQUES = (None, "K", "Q")
TAILLES = (None, 5, 9, 13, 19)
SYMBOLES = (None, "X", "O")
PASSES = (None, True, False)

# L'ordre est le contrat : il ne change jamais sans une nouvelle version.
CHAMPS: tuple[tuple[str, tuple], ...] = (
    ("jeu", JEUX),
    ("action", ACTIONS),
    ("de", (None,) + tuple(range(64))),
    ("vers", (None,) + tuple(range(64))),
    ("promotion", PROMOTIONS),
    ("roque", ROQUES),
    ("case", (None,) + tuple(range(9))),
    ("symbole", SYMBOLES),
    ("carte", (None,) + tuple(range(52))),
    ("taille", TAILLES),
    ("point", (None,) + tuple(range(81))),
    ("passe", PASSES),
    ("chemin_0", (None,) + tuple(range(64))),
    ("chemin_1", (None,) + tuple(range(64))),
    ("chemin_2", (None,) + tuple(range(64))),
)
INDEX = {nom: {val: i for i, val in enumerate(vals)} for nom, vals in CHAMPS}
DIM = sum(len(vals) for _, vals in CHAMPS)
VERSION = 1


def action(corps: dict) -> str:
    if corps.get("chemin"):
        return "prendre"
    if "carte" in corps:
        return "jouer_carte"
    if corps.get("passe"):
        return "passer"
    if "case" in corps:
        return "jouer_case"
    if corps.get("promotion") is not None:
        return "promouvoir"
    if "de" in corps and "vers" in corps:
        return "deplacer"
    if "point" in corps:
        return "poser"
    return "autre"


def code_rsn(rsn) -> dict:
    corps = dict(rsn.corps)
    code = {
        "jeu": rsn.jeu,
        "action": action(corps),
        "de": corps.get("de"),
        "vers": corps.get("vers"),
        "promotion": corps.get("promotion"),
        "roque": corps.get("roque"),
        "case": corps.get("case"),
        "symbole": corps.get("symbole"),
        "carte": corps.get("carte"),
        "taille": corps.get("taille"),
        "point": corps.get("point"),
        "passe": corps.get("passe"),
    }
    chemin = list(corps.get("chemin") or [])
    for i in range(3):
        code[f"chemin_{i}"] = chemin[i] if i < len(chemin) else None
    return code


def code_item(item) -> dict:
    return code_rsn(item.attendu)


def index_code(code: dict) -> dict[str, int]:
    return {nom: INDEX[nom][code.get(nom)] for nom, _ in CHAMPS}


def vecteur(code: dict) -> list[int]:
    """Le code typé, un vecteur one-hot concaténé de dimension fixe DIM."""
    out = [0] * DIM
    base = 0
    for nom, vals in CHAMPS:
        out[base + INDEX[nom][code.get(nom)]] = 1
        base += len(vals)
    return out


def depuis_index(idx: dict[str, int]) -> dict:
    return {nom: CHAMPS[i][1][idx[nom]] for i, (nom, _) in enumerate(CHAMPS)}


def rsn_depuis_code(code: dict, nature: str = "coup"):
    from jeux.rsn import RSN
    corps = {}
    if code.get("chemin_0") is not None:
        corps["chemin"] = [v for v in (code.get("chemin_0"), code.get("chemin_1"), code.get("chemin_2")) if v is not None]
    elif code.get("carte") is not None:
        corps["carte"] = code["carte"]
    elif code.get("case") is not None:
        corps["case"] = code["case"]
        if code.get("symbole") is not None:
            corps["symbole"] = code["symbole"]
    elif code.get("passe"):
        corps["taille"] = code.get("taille")
        corps["passe"] = True
    elif code.get("de") is not None and code.get("vers") is not None:
        corps["de"] = code["de"]
        corps["vers"] = code["vers"]
        corps["promotion"] = code.get("promotion")
        corps["roque"] = code.get("roque")
    elif code.get("point") is not None:
        corps["taille"] = code.get("taille")
        corps["point"] = code["point"]
    return RSN(str(code.get("jeu", "morpion")), nature, corps)


def empreinte_code(code: dict) -> str:
    """L'empreinte du code typé : stable, indépendante de la langue."""
    return hashlib.sha256(json.dumps(code, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode()).hexdigest()
