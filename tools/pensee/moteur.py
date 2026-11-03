"""moteur.py — la boucle anytime, les stratégies, la décision.

Le moteur est un bloc `state → decision` : il reçoit un problème (état initial, opérateurs, but,
heuristique), une stratégie et un budget ; il rend une **décision** justifiée et une **trace**
rejouable. Il ne lit jamais la surface.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

from .coeur import Candidat, Decision, Etat
from .store import Budget, Store, Trace


@dataclass
class Probleme:
    nom: str
    initial: Callable[[], Etat]
    operateurs: dict[str, Callable[[Etat, dict], list[Etat]]]
    but: Callable[[Etat], bool]
    heuristique: Callable[[Etat], float] = lambda e: 0.0
    score: Callable[[Etat], float] = lambda e: 0.0
    csp: object | None = None


@dataclass(frozen=True)
class Proposition:
    parent: str
    operateur: str
    params: dict
    cout: int = 1


class Strategie:
    """Une stratégie choisit un nœud ouvert et propose des transitions. Elle ne modifie rien."""

    nom = "base"

    def choisir(self, store: Store, probleme: Probleme) -> str:
        raise NotImplementedError

    def proposer(self, etat: Etat, probleme: Probleme) -> list[Proposition]:
        return [Proposition(etat.empreinte(), nom, {}) for nom in probleme.operateurs]


class BFS(Strategie):
    nom = "bfs"

    def choisir(self, store, probleme):
        return min(store.ouverts, key=lambda f: store.ouverts[f])


class Greedy(Strategie):
    nom = "greedy"

    def choisir(self, store, probleme):
        return max(store.ouverts, key=lambda f: (store.noeuds[f].score, -store.ouverts[f]))


class AStar(Strategie):
    nom = "astar"

    def __init__(self, poids_heuristique: float = 1.0):
        self.poids = poids_heuristique

    def choisir(self, store, probleme):
        return max(store.ouverts,
                   key=lambda f: (store.noeuds[f].score + self.poids * probleme.heuristique(store.etats[f]),
                                  -store.ouverts[f]))


class MCTSLite(Strategie):
    nom = "mcts"

    def __init__(self, c: float = 1.4, graine: int = 0):
        self.c = c
        self.rng = __import__("random").Random(graine)

    def choisir(self, store, probleme):
        def ucb(f):
            n = store.noeuds[f]
            visites = max(1, n.visites)
            return n.score + self.c * math.sqrt(math.log(1 + len(store.etats)) / visites)
        return max(store.ouverts, key=lambda f: (ucb(f), -store.ouverts[f]))

    def proposer(self, etat, probleme):
        """Un seul opérateur, mais **applicable** : un opérateur sans enfant n'est pas un coup."""
        applicables = [nom for nom in sorted(probleme.operateurs)
                       if probleme.operateurs[nom](etat, {})]
        if not applicables:
            return []
        return [Proposition(etat.empreinte(), self.rng.choice(applicables), {})]


@dataclass
class Moteur:
    store: Store = field(default_factory=Store)
    trace: Trace = field(default_factory=Trace)

    def boucle(self, probleme: Probleme, strategie: Strategie, budget: Budget,
               arret_sur_but: bool = False) -> Decision:
        racine = self.store.put(probleme.initial())
        self.store.push(racine, probleme.score(self.store.get(racine)))
        meilleur = racine
        meilleur_score = self.store.noeuds[racine].score
        pas = 0
        trouve = False
        while budget.reste() and self.store.ouverts and not trouve:
            noeud = strategie.choisir(self.store, probleme)
            etat = self.store.get(noeud)
            score_noeud = self.store.noeuds[noeud].score
            if score_noeud > meilleur_score:
                meilleur, meilleur_score = noeud, score_noeud
            self.store.ouverts.pop(noeud, None)
            for prop in strategie.proposer(etat, probleme):
                if not budget.reste() or trouve:
                    break
                operateur = probleme.operateurs[prop.operateur]
                enfants = operateur(etat, prop.params)
                for enfant in enfants:
                    fp = self.store.put(enfant)
                    s = probleme.score(enfant)
                    self.store.edge(noeud, fp, prop.operateur, prop.params, s)
                    pas += 1
                    self.trace.pas(noeud, fp, prop.operateur, prop.params, s, 1, strategie.nom)
                    if probleme.but(enfant) or enfant.statut == "settled":
                        enfant.statut = "settled"
                        self.trace.marquer_settled(fp)
                        if s > meilleur_score:
                            meilleur, meilleur_score = fp, s
                        if arret_sur_but:
                            trouve = True
                            break
                    else:
                        self.store.push(fp, s)
                    budget.compter(1)  # un nœud, pas une proposition
                    if not budget.reste() or trouve:
                        break
                if trouve:
                    break
        return Decision(self.store.get(meilleur), self.store.chemin(meilleur),
                        budget.consomme, strategie.nom)
