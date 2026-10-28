#!/usr/bin/env python3
"""vdc.py — échantillonnage déterministe par van der Corput (base 2).

On n'utilise plus `randint` ni `shuffle` pour choisir les fenêtres : la suite de
van der Corput parcourt [0, 1) en **discrépance faible**. Deux exécutions avec le
même compteur donnent exactement les mêmes indices, sans dépendre d'un état
global de générateur.
"""
from __future__ import annotations


def vdc(i: int, base: int = 2) -> float:
    """i-ème terme de van der Corput dans [0, 1)."""
    if i < 0:
        raise ValueError("l'indice doit être >= 0")
    n, d, r = i, 1, 0.0
    while n:
        n, reste = divmod(n, base)
        d *= base
        r += reste / d
    return r


def ordre_vdc(n: int) -> list[int]:
    """Permutation déterministe de 0..n-1, par valeur de van der Corput."""
    return sorted(range(n), key=lambda i: (vdc(i), i))


def departs_vdc(compteur: int, n: int, borne: int, seq: int) -> list[int]:
    """`n` débuts de fenêtre dans [0, borne), à partir du compteur global."""
    if borne <= 0:
        return [0] * n
    return [min(borne - 1, int(vdc(compteur + j) * borne)) for j in range(n)]
