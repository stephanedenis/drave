#!/usr/bin/env python3
"""masque.py — la perte ne porte que sur les réponses du professeur.

POURQUOI. Le premier entraînement distillait le texte **entier** (system + user +
professeur) : le modèle apprend surtout la distribution des réponses, et le
contrôle mélangé fait aussi bien. Ici, le prompt est **lu** mais sa perte est
**masquée** : seul le byte de réponse compte. C'est la différence entre « imiter
le style » et « répondre à la question ».

Le format est celui de `distillation.py` :

    ### system
    ...
    ### user
    ...
    ### professeur
    ...

La fonction `exemples` rend `(prompt, reponse)` en octets ; `fenetre` découpe un
exemple en une fenêtre de `seq` octets et rend `(entrées, masque)` où le masque
vaut 1 sur les cibles de réponse, 0 sur le prompt et le remplissage. La cible est
décalée d'un octet : le dernier octet du prompt prédit le premier de la réponse,
ce qui est précisément le conditionnement que l'on veut apprendre.
"""
from __future__ import annotations

import random


def exemples(texte: str) -> list[tuple[bytes, bytes]]:
    """Les couples (prompt, réponse) d'un corpus `distillation.py`."""
    out: list[tuple[bytes, bytes]] = []
    for bloc in texte.split("### system\n"):
        if "### professeur\n" not in bloc:
            continue
        prompt, reponse = bloc.split("### professeur\n", 1)
        prompt = "### system\n" + prompt
        reponse = reponse.strip("\n")
        if reponse:
            out.append((prompt.encode("utf-8"), reponse.encode("utf-8")))
    return out


def _fenetre(prompt: bytes, reponse: bytes, seq: int, debut: int) -> tuple[list[int], list[int]]:
    full = list(prompt + reponse)
    masque = [0] * len(prompt) + [1] * len(reponse)
    x = full[debut:debut + seq]
    cible = full[debut + 1:debut + seq + 1]
    m = masque[debut + 1:debut + seq + 1]
    if len(x) < seq:
        x += [0] * (seq - len(x))
    if len(cible) < seq:
        cible += [0] * (seq - len(cible))
    if len(m) < seq:
        m += [0] * (seq - len(m))
    return x, m


def fenetre(prompt: bytes, reponse: bytes, seq: int,
            rng: random.Random | None = None) -> tuple[list[int], list[int]]:
    """Une fenêtre d'entraînement avec au moins une cible de réponse."""
    full = len(prompt) + len(reponse)
    if full <= seq:
        return _fenetre(prompt, reponse, seq, 0)
    dernier = full - seq - 1
    if rng is None:
        return _fenetre(prompt, reponse, seq, dernier)
    for _ in range(20):
        x, m = _fenetre(prompt, reponse, seq, rng.randrange(0, dernier + 1))
        if any(m):
            return x, m
    return _fenetre(prompt, reponse, seq, dernier)


def fenetres_validation(prompt: bytes, reponse: bytes,
                        seq: int) -> list[tuple[list[int], list[int]]]:
    """Les fenêtres couvrant l'exemple ; les réponses sont toutes vues."""
    full = len(prompt) + len(reponse)
    if full <= seq:
        return [_fenetre(prompt, reponse, seq, 0)]
    out = []
    debut = 0
    while debut < full:
        out.append(_fenetre(prompt, reponse, seq, min(debut, full - seq - 1)))
        debut += seq
    return out


def poids_masque(masque: list[int]) -> int:
    return sum(1 for x in masque if x)
