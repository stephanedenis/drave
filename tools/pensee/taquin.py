"""taquin.py — le taquin 3×3 : un problème anytime, avec une heuristique exacte en distance.

Le but est `(1,2,3,4,5,6,7,8,0)` (0 = case vide). Les opérateurs sont quatre noms sans
paramètres (`haut`, `bas`, `gauche`, `droite`), pour que la stratégie aléatoire et MCTS-lite
puissent les tirer sans connaître le problème. Le score est `1/(1+Manhattan)` : 1 au but,
et une qualité croissante à mesure qu'on s'approche.
"""
from __future__ import annotations

import random

from .coeur import Candidat, Etat
from .moteur import Probleme

BUT = (1, 2, 3, 4, 5, 6, 7, 8, 0)
VOISINS = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4, 6), 4: (1, 3, 5, 7),
           5: (2, 4, 8), 6: (3, 7), 7: (4, 6, 8), 8: (5, 7)}


def etat_taquin(plateau: tuple[int, ...], parent: str | None = None,
                profondeur: int = 0) -> Etat:
    candidats = tuple(Candidat(f"c{i}", {"case": i, "tuile": plateau[i]}) for i in range(9))
    return Etat("".join(map(str, plateau)), parent, profondeur, candidats)


def plateau_de(e: Etat) -> tuple[int, ...]:
    cases = {c.corps["case"]: c.corps["tuile"] for c in e.candidats if "case" in c.corps}
    return tuple(cases[i] for i in range(9))


def distance(plateau: tuple[int, ...]) -> int:
    total = 0
    for i, tuile in enumerate(plateau):
        if tuile == 0:
            continue
        j = BUT.index(tuile)
        total += abs(i // 3 - j // 3) + abs(i % 3 - j % 3)
    return total


def _deplacer(e: Etat, direction: str) -> list[Etat]:
    p = list(plateau_de(e))
    i = p.index(0)
    j = {"haut": i - 3 if i >= 3 else -1,
         "bas": i + 3 if i <= 5 else -1,
         "gauche": i - 1 if i % 3 else -1,
         "droite": i + 1 if i % 3 != 2 else -1}[direction]
    if j < 0:
        return []
    p[i], p[j] = p[j], p[i]
    return [etat_taquin(tuple(p), e.empreinte(), e.profondeur + 1)]


def haut(e, _p=None):
    return _deplacer(e, "haut")


def bas(e, _p=None):
    return _deplacer(e, "bas")


def gauche(e, _p=None):
    return _deplacer(e, "gauche")


def droite(e, _p=None):
    return _deplacer(e, "droite")


def but(e: Etat) -> bool:
    return plateau_de(e) == BUT


def score(e: Etat) -> float:
    return 1.0 / (1.0 + distance(plateau_de(e)))


def heuristique(e: Etat) -> float:
    return -float(distance(plateau_de(e)))


def melange(n: int = 20, graine: int = 0) -> tuple[int, ...]:
    """Un départ **solvable** : une marche aléatoire depuis le but, sans retour immédiat."""
    rng = random.Random(graine)
    p = list(BUT)
    precedent = None
    for _ in range(n):
        i = p.index(0)
        directions = []
        for direction, j in (("haut", i - 3 if i >= 3 else -1),
                             ("bas", i + 3 if i <= 5 else -1),
                             ("gauche", i - 1 if i % 3 else -1),
                             ("droite", i + 1 if i % 3 != 2 else -1)):
            if j >= 0 and j != precedent:
                directions.append((direction, j))
        if not directions:
            break
        _, j = rng.choice(directions)
        precedent = i
        p[i], p[j] = p[j], p[i]
    return tuple(p)


DÉPART = melange(8, 0)

TAQUIN = Probleme(
    nom="taquin",
    initial=lambda: etat_taquin(DÉPART),
    operateurs={"haut": haut, "bas": bas, "gauche": gauche, "droite": droite},
    but=but,
    heuristique=heuristique,
    score=score,
)
