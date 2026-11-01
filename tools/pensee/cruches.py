"""cruches.py — le problème jouet : deux cruches de 3 et 5 litres, mesurer 4.

C'est le plus petit problème qui a tout ce que le moteur doit savoir faire : des états
(candidats typés), des opérateurs classiques, un but exact, une heuristique et un score.

  A = 3 L, B = 5 L ; au départ (0, 0) ; le but est d'avoir **4 litres** dans une cruche.

Ce que le moteur ne fait pas : il ne connaît pas les litres. Il voit des **candidats**
(`{"cruche": "a", "litres": 3}`), et l'opérateur est le seul à savoir les lire.
"""
from __future__ import annotations

from .coeur import Candidat, Etat
from .moteur import Probleme

CAPACITES = {"a": 3, "b": 5}


def etat(a: int, b: int, parent: str | None = None, profondeur: int = 0) -> Etat:
    return Etat(id=f"({a},{b})", parent=parent, profondeur=profondeur,
                candidats=(Candidat("a", {"cruche": "a", "litres": a}),
                           Candidat("b", {"cruche": "b", "litres": b})))


def litres(e: Etat) -> dict[str, int]:
    return {c.corps["cruche"]: c.corps["litres"] for c in e.candidats}


def _fils(e: Etat, a: int, b: int) -> list[Etat]:
    return [etat(a, b, e.empreinte(), e.profondeur + 1)]


def remplir_a(e, _p=None):
    a, b = litres(e)["a"], litres(e)["b"]
    return _fils(e, CAPACITES["a"], b) if a != CAPACITES["a"] else []


def remplir_b(e, _p=None):
    a, b = litres(e)["a"], litres(e)["b"]
    return _fils(e, a, CAPACITES["b"]) if b != CAPACITES["b"] else []


def vider_a(e, _p=None):
    a, b = litres(e)["a"], litres(e)["b"]
    return _fils(e, 0, b) if a else []


def vider_b(e, _p=None):
    a, b = litres(e)["a"], litres(e)["b"]
    return _fils(e, a, 0) if b else []


def verser_a_vers_b(e, _p=None):
    a, b = litres(e)["a"], litres(e)["b"]
    if not a or b == CAPACITES["b"]:
        return []
    verse = min(a, CAPACITES["b"] - b)
    return _fils(e, a - verse, b + verse)


def verser_b_vers_a(e, _p=None):
    a, b = litres(e)["a"], litres(e)["b"]
    if not b or a == CAPACITES["a"]:
        return []
    verse = min(b, CAPACITES["a"] - a)
    return _fils(e, a + verse, b - verse)


def _distances_exactes() -> dict[tuple[int, int], int]:
    """Distance au but pour les 24 états — BFS sur le graphe **inversé**.

    Les opérateurs ne sont pas inversibles un pas pour un pas (vider (0,4) donne (0,0), mais
    remplir (0,0) ne redonne pas (0,4)) : il faut donc inverser les arêtes avant le BFS. C'est
    l'heuristique **exacte** du jouet — admissible et consistante.
    """
    from collections import deque
    etats = [(a, b) for a in range(CAPACITES["a"] + 1) for b in range(CAPACITES["b"] + 1)]
    inverse: dict[tuple[int, int], list[tuple[int, int]]] = {e: [] for e in etats}
    for (a, b) in etats:
        source = etat(a, b)
        for op in ("remplir_a", "remplir_b", "vider_a", "vider_b",
                   "verser_a_vers_b", "verser_b_vers_a"):
            for enfant in globals()[op](source, {}):
                l = litres(enfant)
                inverse[(l["a"], l["b"])].append((a, b))
    buts = [(3, 4), (2, 4), (1, 4), (0, 4)]
    dist = {e: 0 for e in buts}
    file = deque(buts)
    while file:
        courant = file.popleft()
        for pred in inverse[courant]:
            if pred not in dist:
                dist[pred] = dist[courant] + 1
                file.append(pred)
    return dist


DISTANCES = _distances_exactes()


def distance(e: Etat) -> int:
    l = litres(e)
    return DISTANCES.get((l["a"], l["b"]), 99)


def but(e: Etat) -> bool:
    return 4 in litres(e).values()


def score(e: Etat) -> float:
    return 1.0 if but(e) else 1.0 / (1.0 + distance(e))


CRUCHES = Probleme(
    nom="cruches",
    initial=lambda: etat(0, 0),
    operateurs={"remplir_a": remplir_a, "remplir_b": remplir_b, "vider_a": vider_a,
                "vider_b": vider_b, "verser_a_vers_b": verser_a_vers_b,
                "verser_b_vers_a": verser_b_vers_a},
    but=but,
    heuristique=lambda e: -float(distance(e)),
    score=score,
)
