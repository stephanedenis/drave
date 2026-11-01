"""jeux.py — alpha-bêta : le décideur deux joueurs, sur les mêmes états et opérateurs.

Le moteur anytime est **mono-agent** : il choisit un nœud, propose des transitions, garde le
meilleur. Alpha-bêta est un **décideur deux joueurs** : il descend l'arbre, remonte une valeur,
et coupe une branche dès que la borne le permet. Il partage les types (`Etat`, `Probleme`,
`Decision`), les opérateurs et le store — pas la boucle, parce que la valeur remonte au lieu de
se propager vers l'avant.

    from tools.pensee.jeux import MORPION, AlphaBeta, plateau_de
    d = AlphaBeta(profondeur=9).decider(MORPION)
    print(plateau_de(d.etat))
"""
from __future__ import annotations

import math
from typing import Callable

from .coeur import Candidat, Decision, Etat
from .moteur import Probleme
from .store import Budget, Store, Trace

LIGNES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
          (0, 3, 6), (1, 4, 7), (2, 5, 8),
          (0, 4, 8), (2, 4, 6))


# --------------------------------------------------------------------------- morpion


def etat_morpion(plateau: tuple[str, ...], joueur: str, parent: str | None = None,
                 profondeur: int = 0) -> Etat:
    candidats = tuple([Candidat(f"c{i}", {"case": i, "marque": plateau[i]}) for i in range(9)]
                      + [Candidat("tour", {"joueur": joueur})])
    return Etat("".join(plateau) + "|" + joueur, parent, profondeur, candidats)


def plateau_de(e: Etat) -> tuple[str, ...]:
    cases = {c.corps["case"]: c.corps["marque"] for c in e.candidats if "case" in c.corps}
    return tuple(cases[i] for i in range(9))


def joueur_de(e: Etat) -> str:
    return next(c.corps["joueur"] for c in e.candidats if "joueur" in c.corps)


def gagnant(plateau: tuple[str, ...]) -> str | None:
    for a, b, c in LIGNES:
        if plateau[a] != "." and plateau[a] == plateau[b] == plateau[c]:
            return plateau[a]
    return None


def terminal(e: Etat) -> bool:
    p = plateau_de(e)
    return gagnant(p) is not None or "." not in p


def score(e: Etat) -> float:
    g = gagnant(plateau_de(e))
    return 1.0 if g == "X" else (-1.0 if g == "O" else 0.0)


def heuristique(e: Etat) -> float:
    p = plateau_de(e)
    valeurs = {"X": 0, "O": 0}
    for a, b, c in LIGNES:
        marques = {p[a], p[b], p[c]}
        if "X" in marques and "O" not in marques:
            valeurs["X"] += 1
        elif "O" in marques and "X" not in marques:
            valeurs["O"] += 1
    return float(valeurs["X"] - valeurs["O"])


def jouer(e: Etat, params: dict) -> list[Etat]:
    if terminal(e):
        return []
    case = int(params["case"])
    p = list(plateau_de(e))
    if p[case] != ".":
        return []
    joueur = joueur_de(e)
    p[case] = joueur
    suivant = "O" if joueur == "X" else "X"
    return [etat_morpion(tuple(p), suivant, e.empreinte(), e.profondeur + 1)]


MORPION = Probleme(
    nom="morpion",
    initial=lambda: etat_morpion((".",) * 9, "X"),
    operateurs={"jouer": jouer},
    but=terminal,
    heuristique=heuristique,
    score=score,
)


def case_jouee(avant: Etat, apres: Etat) -> int | None:
    a, b = plateau_de(avant), plateau_de(apres)
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return None


# --------------------------------------------------------------------------- alpha-bêta


class AlphaBeta:
    """Le décideur : une profondeur, une évaluation, une table (le store) et une trace.

    `pruning=False` donne le **minimax** exact, pour le contrôle : même valeur, plus de nœuds.
    """

    def __init__(self, profondeur: int = 9, pruning: bool = True,
                 evaluer: Callable[[Etat], float] | None = None):
        self.profondeur = profondeur
        self.pruning = pruning
        self.evaluer = evaluer
        self.noeuds = 0
        self.coupes = 0

    def _valeur(self, e: Etat, probleme: Probleme) -> float:
        if self.evaluer is not None:
            return float(self.evaluer(e))
        return probleme.score(e) if probleme.but(e) else probleme.heuristique(e)

    def decider(self, probleme: Probleme, budget: Budget | None = None) -> Decision:
        budget = budget or Budget(400_000)
        store, trace = Store(), Trace()
        self.noeuds = self.coupes = 0
        racine_etat = probleme.initial()
        racine = store.put(racine_etat)

        def val(e: Etat, alpha: float, beta: float, profondeur: int, maximisant: bool,
                parent_fp: str) -> tuple[float, Etat | None]:
            if not budget.reste():
                return self._valeur(e, probleme), None
            budget.compter(1)
            self.noeuds += 1
            if probleme.but(e) or profondeur == 0:
                return self._valeur(e, probleme), None
            meilleur: Etat | None = None
            if maximisant:
                valeur = -math.inf
                for case in range(9):
                    enfants = probleme.operateurs["jouer"](e, {"case": case})
                    if not enfants:
                        continue
                    enfant = enfants[0]
                    fp = store.put(enfant)
                    v, _ = val(enfant, alpha, beta, profondeur - 1, False, fp)
                    store.edge(parent_fp, fp, "jouer", {"case": case}, v)
                    trace.pas(parent_fp, fp, "jouer", {"case": case}, v, 1,
                              "alpha-beta" if self.pruning else "minimax")
                    if v > valeur:
                        valeur, meilleur = v, enfant
                    alpha = max(alpha, valeur)
                    if self.pruning and alpha >= beta:
                        self.coupes += 1
                        break
                return valeur, meilleur
            valeur = math.inf
            for case in range(9):
                enfants = probleme.operateurs["jouer"](e, {"case": case})
                if not enfants:
                    continue
                enfant = enfants[0]
                fp = store.put(enfant)
                v, _ = val(enfant, alpha, beta, profondeur - 1, True, fp)
                store.edge(parent_fp, fp, "jouer", {"case": case}, v)
                trace.pas(parent_fp, fp, "jouer", {"case": case}, v, 1,
                          "alpha-beta" if self.pruning else "minimax")
                if v < valeur:
                    valeur, meilleur = v, enfant
                beta = min(beta, valeur)
                if self.pruning and alpha >= beta:
                    self.coupes += 1
                    break
            return valeur, meilleur

        _, meilleur = val(racine_etat, -math.inf, math.inf, self.profondeur, True, racine)
        if meilleur is None:
            meilleur = racine_etat
        chemin = store.chemin(meilleur.empreinte()) if meilleur.empreinte() in store.etats else [racine]
        return Decision(meilleur, chemin, budget.consomme,
                        "alpha-beta" if self.pruning else "minimax")
