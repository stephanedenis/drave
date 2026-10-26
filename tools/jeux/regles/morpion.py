#!/usr/bin/env python3
"""regles.morpion — le morpion 3×3 : règles, terminalité, utilité.

Le morpion est le **témoin** de l'étage 2 : il est petit, résolu, et sa valeur
minimax est connue (0, nulle, depuis la position vide). Il sert donc de
référence exacte à la recherche : si le minimax ne rend pas 0, c'est le moteur
de recherche qui est faux, pas le jeu.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Iterable

from ..rsn import Annotation, RSN

N = 3
LIGNES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
          (0, 3, 6), (1, 4, 7), (2, 5, 8),
          (0, 4, 8), (2, 4, 6))


def etat_initial(trait: str = "X") -> RSN:
    return RSN("morpion", "etat", {"taille": N, "cases": [None] * 9, "trait": trait},
               Annotation(langue="notation", format="canonique", surface=""))


def cases(rsn: RSN) -> list[str | None]:
    return list(rsn.corps["cases"])


def trait(rsn: RSN) -> str:
    return str(rsn.corps.get("trait") or "X")


def gagnant(cases_: Iterable[str | None]) -> str | None:
    c = list(cases_)
    for a, b, d in LIGNES:
        if c[a] is not None and c[a] == c[b] == c[d]:
            return c[a]
    return None


def plein(cases_: Iterable[str | None]) -> bool:
    return all(x is not None for x in cases_)


def resultat(rsn: RSN) -> str | None:
    """« X », « O », « N » (nulle) ou None (en cours)."""
    c = cases(rsn)
    g = gagnant(c)
    if g:
        return g
    if plein(c):
        return "N"
    return None


def terminal(rsn: RSN) -> bool:
    return resultat(rsn) is not None


def coups_legaux(rsn: RSN) -> list[RSN]:
    if terminal(rsn):
        return []
    c = cases(rsn)
    t = trait(rsn)
    return [RSN("morpion", "coup", {"case": i, "symbole": t},
                Annotation(langue="notation", format="canonique", surface=""))
            for i, v in enumerate(c) if v is None]


def coup_valide(rsn: RSN, coup: RSN) -> tuple[bool, str]:
    if coup.jeu != "morpion" or coup.nature != "coup":
        return False, "ce n'est pas un coup de morpion"
    i = coup.corps.get("case")
    if not isinstance(i, int) or not (0 <= i < 9):
        return False, f"case hors du plateau : {i!r}"
    if cases(rsn)[i] is not None:
        return False, f"la case {i} est déjà occupée"
    s = coup.corps.get("symbole")
    if s is not None and s != trait(rsn):
        return False, f"c'est au tour de {trait(rsn)}, pas de {s}"
    return True, ""


def applique(rsn: RSN, coup: RSN) -> RSN:
    ok, pourquoi = coup_valide(rsn, coup)
    if not ok:
        raise ValueError(pourquoi)
    i = int(coup.corps["case"])
    c = cases(rsn)
    c[i] = trait(rsn)
    suivant = "O" if trait(rsn) == "X" else "X"
    return RSN("morpion", "etat", {"taille": N, "cases": c, "trait": suivant},
               annotation=rsn.annotation)


def applique_indice(rsn: RSN, i: int) -> RSN:
    return applique(rsn, RSN("morpion", "coup", {"case": i, "symbole": trait(rsn)}))


def cle(rsn: RSN) -> tuple:
    return tuple(cases(rsn)), trait(rsn)


def utilite(rsn: RSN) -> float:
    """Du point de vue du joueur au trait : +1 gagné, −1 perdu, 0 nulle."""
    r = resultat(rsn)
    if r is None:
        return 0.0
    if r == "N":
        return 0.0
    return 1.0 if r == trait(rsn) else -1.0


def heuristique(rsn: RSN) -> float:
    """Une évaluation simple : les lignes encore ouvertes, pondérées.

    Elle ne sert qu'à comparer des positions non terminales (goût du risk) ; le
    minimax exact du morpion n'en a pas besoin. Elle est utile au contrôle
    négatif « sans recherche » : un joueur gourmand doit perdre plus qu'un
    joueur exact.
    """
    c = cases(rsn)
    t = trait(rsn)
    adv = "O" if t == "X" else "X"
    score = 0.0
    for ligne in LIGNES:
        vals = [c[i] for i in ligne]
        if adv in vals and t in vals:
            continue
        if t in vals and adv not in vals:
            score += 10 ** (vals.count(t) - 1)
        elif adv in vals and t not in vals:
            score -= 10 ** (vals.count(adv) - 1)
    return score


def etats_atteignables() -> list[tuple]:
    """Tous les états atteignables (pour la résolution exhaustive)."""
    vus: set[tuple] = set()
    pile = [(tuple([None] * 9), "X")]
    while pile:
        c, t = pile.pop()
        if (c, t) in vus:
            continue
        vus.add((c, t))
        r = RSN("morpion", "etat", {"taille": N, "cases": list(c), "trait": t})
        if terminal(r):
            continue
        for i, v in enumerate(c):
            if v is None:
                cc = list(c)
                cc[i] = t
                pile.append((tuple(cc), "O" if t == "X" else "X"))
    return sorted(vus, key=repr)


def resous(rsn: RSN) -> tuple[float, int | None]:
    """La valeur minimax exacte et le meilleur coup (mémoïsé)."""

    @lru_cache(maxsize=None)
    def valeur(c: tuple, t: str) -> float:
        r = RSN("morpion", "etat", {"taille": N, "cases": list(c), "trait": t})
        if terminal(r):
            if resultat(r) == "N":
                return 0.0
            return -1.0 if resultat(r) != t else 1.0
        vals = []
        for i, v in enumerate(c):
            if v is None:
                cc = list(c)
                cc[i] = t
                vals.append(-valeur(tuple(cc), "O" if t == "X" else "X"))
        v = max(vals)
        return 0.0 if v == 0 else v

    c = tuple(cases(rsn))
    t = trait(rsn)
    if terminal(rsn):
        return valeur(c, t), None
    meilleur, coup = -2.0, None
    for i, v in enumerate(c):
        if v is None:
            cc = list(c)
            cc[i] = t
            s = -valeur(tuple(cc), "O" if t == "X" else "X")
            if s > meilleur:
                meilleur, coup = s, i
    return meilleur, coup
