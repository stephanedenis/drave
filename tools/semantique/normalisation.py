#!/usr/bin/env python3
"""normalisation.py — la surface vers des concepts, avant le parseur natif.

Le lexique multilingue connaît les noms de jeux, les pièces, les rangs et les
enseignes dans 66 langues. On remplace ces formes par un **concept canonique**
(`[jeu.morpion]`, `[echecs.piece.N]`, `[cartes.rang.13]`) ; les coordonnées et les
nombres restent. Deux surfaces qui disent la même chose dans deux langues
deviennent alors **presque identiques** — c'est ce qui doit rendre le natif
cohérent entre langues.
"""
from __future__ import annotations

from jeux.lexique import normalise_forme
from jeux.lexique_multilingue import MULTI

DOMAINES = ("jeu.nom", "echecs.piece", "cartes.rang", "cartes.couleur",
            "go.passe", "commun.couleur")


def normaliser(texte: str) -> str:
    t = normalise_forme(texte)
    if not t:
        return t
    tokens = t.split()
    trouves = []
    for domaine in DOMAINES:
        trouves.extend(MULTI.cherche(domaine, texte))
    jeux = {m.concept for m in trouves if m.domaine == "jeu.nom"}
    # Une enseigne de carte tranche l'ambiguïté « roi » (pièce d'échecs vs rang).
    cartes = any(m.domaine == "cartes.couleur" for m in trouves) or "jeu.cartes" in jeux
    echecs = "jeu.echecs" in jeux or (not cartes and any(m.domaine == "echecs.piece" for m in trouves))
    if cartes:
        autorises = {"jeu.nom", "cartes.rang", "cartes.couleur"}
    elif echecs:
        autorises = {"jeu.nom", "echecs.piece"}
    else:
        autorises = set(DOMAINES)
    marques: dict[int, tuple[int, str]] = {}
    for m in trouves:
        if m.domaine not in autorises:
            continue
        n = len(m.forme.split())
        if n < 1 or m.position + n > len(tokens):
            continue
        actuel = marques.get(m.position)
        if actuel is None or n > actuel[0]:
            marques[m.position] = (n, m.concept)
    out = []
    i = 0
    while i < len(tokens):
        if i in marques:
            n, concept = marques[i]
            out.append(f"[{concept}]")
            i += n
        else:
            out.append(tokens[i])
            i += 1
    return " ".join(out)
