#!/usr/bin/env python3
"""pensee.py — l'étage 2 : décider sur la RSN, jamais sur la surface.

Ce module est la **logique de la pensée** des jeux. Il reçoit une RSN d'état
(produite par l'étage 1), la convertit en état interne, cherche, et rend une RSN
d'action. Il ne lit **aucune** chaîne de surface : c'est le contrat qui rend
mesurable l'invariance (« la même position écrite de cinq façons donne le même
coup »).

Cinq logiques, une par jeu :
- **morpion** : minimax exact (le jeu est résolu, la valeur de la position vide
  est 0) ;
- **échecs** : négamax alpha-bêta, approfondissement itératif, table de
  transposition, ordre des coups (prises, promotions), budget de temps ;
- **dames** : négamax alpha-bêta, prises d'abord, budget de temps ;
- **go** : MCTS (UCT), playouts aléatoires, budget de playouts — le go est le
  jeu où la recherche exhaustive est hors de portée ;
- **cartes** : politique (fournir, ne pas surjouer le partenaire, gagner au plus
  bas), parce que l'information est imparfaite.

Toutes les décisions sont **déterministes** à graine et budget fixés : la
mesure peut donc être rejouée.
"""
from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field

from .rsn import RSN
from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G
from .regles import morpion as M

MATE = 100000.0


@dataclass(frozen=True)
class Budget:
    profondeur: int = 4
    temps_s: float = 5.0
    playouts: int = 400
    graine: int = 0


@dataclass
class Decision:
    jeu: str
    coup: RSN | None
    score: float = 0.0
    profondeur: int = 0
    noeuds: int = 0
    secondes: float = 0.0
    methode: str = ""
    details: dict = field(default_factory=dict)

    def vers_dict(self) -> dict:
        return {
            "jeu": self.jeu,
            "coup": self.coup.corps if self.coup else None,
            "score": round(self.score, 4),
            "profondeur": self.profondeur,
            "noeuds": self.noeuds,
            "secondes": round(self.secondes, 4),
            "methode": self.methode,
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# Morpion : minimax exact
# ---------------------------------------------------------------------------
def decide_morpion(etat: RSN, budget: Budget | None = None) -> Decision:
    budget = budget or Budget()
    t0 = time.monotonic()
    if M.terminal(etat):
        return Decision("morpion", None, M.utilite(etat), 9, 0, time.monotonic() - t0, "terminal")
    score, coup = M.resous(etat)
    score = 0.0 if score == 0 else score
    action = RSN("morpion", "coup", {"case": coup, "symbole": M.trait(etat)})
    return Decision("morpion", action, score, 9, 0,
                    time.monotonic() - t0, "minimax exact (mémoïsé)",
                    {"valeur_theorique": score})


def coup_morpion_sans_recherche(etat: RSN) -> RSN | None:
    """Le contrôle négatif : choisir sur l'heuristique, sans minimax."""
    coups = M.coups_legaux(etat)
    if not coups:
        return None
    meilleur = max(coups, key=lambda c: -M.heuristique(M.applique(etat, c)))
    return meilleur


# ---------------------------------------------------------------------------
# Échecs : négamax alpha-bêta
# ---------------------------------------------------------------------------
class _TempsDepasse(Exception):
    pass


def _valeur_prise(pos: E.Position, c: E.Coup) -> int:
    v = pos.plateau[c.vers]
    if v:
        return 10 * E.VALEURS[E.typ(v)] - E.VALEURS[E.typ(pos.plateau[c.de])]
    return 0


def _ordre_echecs(pos: E.Position, coups: list[E.Coup]) -> list[E.Coup]:
    return sorted(coups, key=lambda c: (_valeur_prise(pos, c)
                                        + (800 if c.promotion else 0)
                                        + (100 if c.drapeau in (E.ROQUE_K, E.ROQUE_Q) else 0)),
                  reverse=True)


def _negamax_echecs(pos: E.Position, profondeur: int, alpha: float, beta: float,
                    ply: int, tt: dict, limite: float, stats: dict) -> float:
    stats["noeuds"] += 1
    if stats["noeuds"] % 2048 == 0 and time.monotonic() > limite:
        raise _TempsDepasse
    if pos.demi >= 100 or pos.insuffisant():
        return 0.0
    cle = (pos.hash, profondeur)
    if cle in tt:
        s, drapeau, _ = tt[cle]
        if drapeau == 0:
            return s
        if drapeau == 1:
            alpha = max(alpha, s)
        else:
            beta = min(beta, s)
        if alpha >= beta:
            return s
    coups = pos.coups_legaux()
    if not coups:
        return -MATE + ply if pos.en_echec(pos.trait) else 0.0
    if profondeur <= 0:
        return pos.heuristique()
    alpha0 = alpha
    meilleur = -math.inf
    meilleur_coup = None
    for c in _ordre_echecs(pos, coups):
        u = pos.joue(c)
        try:
            s = -_negamax_echecs(pos, profondeur - 1, -beta, -alpha, ply + 1,
                                  tt, limite, stats)
        finally:
            pos.annule(u)
        if s > meilleur:
            meilleur, meilleur_coup = s, c
        alpha = max(alpha, s)
        if alpha >= beta:
            break
    drapeau = 0 if alpha0 < meilleur < beta else (1 if meilleur >= beta else 2)
    tt[cle] = (meilleur, drapeau, meilleur_coup)
    return meilleur


def decide_echecs(etat: RSN, budget: Budget | None = None) -> Decision:
    budget = budget or Budget()
    t0 = time.monotonic()
    pos = E.position_depuis_rsn(etat)
    coups = pos.coups_legaux()
    if not coups:
        return Decision("echecs", None, E.Position.utilite(pos), 0, 0,
                        time.monotonic() - t0, "terminal")
    tt: dict = {}
    stats = {"noeuds": 0}
    limite = t0 + budget.temps_s
    meilleur_coup = coups[0]
    meilleur_score = 0.0
    profondeur_faite = 0
    try:
        for d in range(1, budget.profondeur + 1):
            alpha, beta = -math.inf, math.inf
            local = -math.inf
            local_coup = None
            for c in _ordre_echecs(pos, coups):
                u = pos.joue(c)
                try:
                    s = -_negamax_echecs(pos, d - 1, -beta, -alpha, 1, tt, limite, stats)
                finally:
                    pos.annule(u)
                if s > local:
                    local, local_coup = s, c
                alpha = max(alpha, s)
            meilleur_coup, meilleur_score = local_coup, local
            profondeur_faite = d
            if abs(local) > MATE - 1000:
                break
    except _TempsDepasse:
        pass
    return Decision("echecs", E.action_depuis_coup(meilleur_coup), meilleur_score,
                    profondeur_faite, stats["noeuds"], time.monotonic() - t0,
                    "négamax alpha-bêta + table",
                    {"tt": len(tt)})


def coup_echecs_sans_recherche(etat: RSN) -> RSN | None:
    """Contrôle négatif : le meilleur coup statique (matériel), sans recherche."""
    pos = E.position_depuis_rsn(etat)
    coups = pos.coups_legaux()
    if not coups:
        return None
    meilleur = max(coups, key=lambda c: _valeur_prise(pos, c) - pos.heuristique() / 1000)
    return E.action_depuis_coup(meilleur)


# ---------------------------------------------------------------------------
# Dames : négamax alpha-bêta
# ---------------------------------------------------------------------------
def _negamax_dames(pos: D.Position, profondeur: int, alpha: float, beta: float,
                   ply: int, tt: dict, limite: float, stats: dict) -> float:
    stats["noeuds"] += 1
    if stats["noeuds"] % 2048 == 0 and time.monotonic() > limite:
        raise _TempsDepasse
    if pos.demi >= 80:
        return 0.0
    cle = (tuple(pos.cases), pos.trait, profondeur)
    if cle in tt:
        s, drapeau = tt[cle]
        if drapeau == 0:
            return s
        if drapeau == 1:
            alpha = max(alpha, s)
        else:
            beta = min(beta, s)
        if alpha >= beta:
            return s
    coups = pos.coups_legaux()
    if not coups:
        return -MATE + ply
    if profondeur <= 0:
        return pos.heuristique()
    if pos.demi >= 80:
        return 0.0
    alpha0 = alpha
    meilleur = -math.inf
    ordonnes = sorted(coups, key=lambda c: (c.prise, len(c.chemin)), reverse=True)
    for c in ordonnes:
        enfant = pos._applique_direct(c)
        s = -_negamax_dames(enfant, profondeur - 1, -beta, -alpha, ply + 1,
                            tt, limite, stats)
        if s > meilleur:
            meilleur = s
        alpha = max(alpha, s)
        if alpha >= beta:
            break
    drapeau = 0 if alpha0 < meilleur < beta else (1 if meilleur >= beta else 2)
    tt[cle] = (meilleur, drapeau)
    return meilleur


def decide_dames(etat: RSN, budget: Budget | None = None) -> Decision:
    budget = budget or Budget()
    t0 = time.monotonic()
    pos = D.position_depuis_rsn(etat)
    coups = pos.coups_legaux()
    if not coups:
        return Decision("dames", None, pos.utilite(), 0, 0,
                        time.monotonic() - t0, "terminal")
    tt: dict = {}
    stats = {"noeuds": 0}
    limite = t0 + budget.temps_s
    meilleur = coups[0]
    score = 0.0
    profondeur_faite = 0
    try:
        for d in range(1, budget.profondeur + 1):
            alpha, beta = -math.inf, math.inf
            local, local_coup = -math.inf, None
            for c in sorted(coups, key=lambda c: (c.prise, len(c.chemin)), reverse=True):
                enfant = pos._applique_direct(c)
                s = -_negamax_dames(enfant, d - 1, -beta, -alpha, 1, tt, limite, stats)
                if s > local:
                    local, local_coup = s, c
                alpha = max(alpha, s)
            meilleur, score = local_coup, local
            profondeur_faite = d
    except _TempsDepasse:
        pass
    return Decision("dames", D.action_depuis_coup(meilleur), score, profondeur_faite,
                    stats["noeuds"], time.monotonic() - t0,
                    "négamax alpha-bêta", {"tt": len(tt)})


def coup_dames_sans_recherche(etat: RSN) -> RSN | None:
    pos = D.position_depuis_rsn(etat)
    coups = pos.coups_legaux()
    if not coups:
        return None
    meilleur = max(coups, key=lambda c: (c.prise, len(c.chemin), -pos.heuristique() / 1000))
    return D.action_depuis_coup(meilleur)


# ---------------------------------------------------------------------------
# Go : MCTS (UCT)
# ---------------------------------------------------------------------------
class _Noeud:
    __slots__ = ("etat", "parent", "coup", "enfants", "visites", "valeur", "non_essayes")

    def __init__(self, etat: G.Position, parent: "_Noeud | None" = None,
                 coup: int | None = None) -> None:
        self.etat = etat
        self.parent = parent
        self.coup = coup
        self.enfants: dict[int, _Noeud] = {}
        self.visites = 0
        self.valeur = 0.0
        self.non_essayes: list[int] | None = None

    def coups(self) -> list[int]:
        if self.non_essayes is None:
            self.non_essayes = self.etat.coups_legaux()
            if not self.non_essayes:
                self.non_essayes = [-1]  # passe
        return self.non_essayes


def _simulation(pos: G.Position, rng: random.Random, max_plies: int = 160) -> float:
    """Partie aléatoire ; rend la différence de score noir − blanc, normalisée."""
    n = pos.n
    for _ in range(max_plies):
        if pos.terminal():
            break
        coups = pos.coups_legaux()
        if coups and rng.random() < 0.97:
            pos = pos.joue(rng.choice(coups))
        else:
            pos = pos.passe_tour()
    d = pos.difference()
    # normalise dans [-1, 1] : un écart de N² points est déjà énorme
    return max(-1.0, min(1.0, d / (n * n * 10.0)))


def decide_go(etat: RSN, budget: Budget | None = None) -> Decision:
    budget = budget or Budget()
    t0 = time.monotonic()
    pos = G.Position.depuis_rsn(etat)
    if pos.terminal():
        return Decision("go", None, pos.utilite(), 0, 0,
                        time.monotonic() - t0, "terminal")
    rng = random.Random(budget.graine)
    racine = _Noeud(pos)
    limite = t0 + budget.temps_s
    noeuds = 0

    def retro(n: _Noeud, r: float) -> None:
        while n is not None:
            n.visites += 1
            n.valeur += r if n.etat.trait == G.NOIR else -r
            n = n.parent

    # INITIALISATION DE LA RACINE. Sans elle, un budget plus petit que le
    # nombre de coups ne fait qu'essayer chaque coup une fois : aucune
    # exploitation. On donne un playout à chaque coup, puis UCT choisit.
    for c in racine.coups():
        enfant = _Noeud(racine.etat.joue(None if c == -1 else c), racine, c)
        racine.enfants[c] = enfant
        noeuds += 1
        retro(enfant, _simulation(enfant.etat.copie(), rng))

    for _ in range(max(0, budget.playouts - len(racine.enfants))):
        if time.monotonic() > limite:
            break
        # sélection : on descend tant que le nœud est complètement développé
        n = racine
        while not n.etat.terminal() and n.enfants and len(n.enfants) == len(n.coups()):
            n = max(n.enfants.values(),
                    key=lambda c: (-c.valeur / max(1, c.visites)
                                   + 1.4 * math.sqrt(math.log(max(1, n.visites)) / max(1, c.visites))))
        # expansion
        if not n.etat.terminal():
            non = [c for c in n.coups() if c not in n.enfants]
            if non:
                c = rng.choice(non)
                enfant = _Noeud(n.etat.joue(None if c == -1 else c), n, c)
                n.enfants[c] = enfant
                n = enfant
                noeuds += 1
        # simulation + rétropropagation
        retro(n, _simulation(n.etat.copie(), rng))
    if not racine.enfants:
        # aucun coup : passe
        return Decision("go", RSN("go", "coup", {"taille": pos.n, "passe": True}),
                        pos.utilite(), 0, noeuds, time.monotonic() - t0, "MCTS (aucun coup)")
    meilleur = max(racine.enfants.values(), key=lambda c: c.visites)
    if meilleur.coup == -1:
        action = RSN("go", "coup", {"taille": pos.n, "passe": True})
    else:
        action = RSN("go", "coup", {"taille": pos.n, "point": meilleur.coup})
    return Decision("go", action, -meilleur.valeur / max(1, meilleur.visites),
                    budget.playouts, noeuds, time.monotonic() - t0,
                    "MCTS UCT", {"visites_racine": racine.visites})


# ---------------------------------------------------------------------------
# Cartes : politique
# ---------------------------------------------------------------------------
def decide_cartes(etat: RSN, budget: Budget | None = None) -> Decision:
    budget = budget or Budget()
    t0 = time.monotonic()
    pos = C.position_depuis_rsn(etat)
    if pos.terminal():
        return Decision("cartes", None, pos.utilite(), 0, 0,
                        time.monotonic() - t0, "terminal")
    c = pos.politique()
    return Decision("cartes", C.action_depuis_carte(c), pos.utilite(), 1,
                    len(pos.coups_legaux()), time.monotonic() - t0,
                    "politique (fournir, partenaire, plus bas gagnant)")


# ---------------------------------------------------------------------------
# Le point d'entrée : une RSN, un budget, une décision
# ---------------------------------------------------------------------------
def decide(etat: RSN, budget: Budget | None = None) -> Decision:
    budget = budget or Budget()
    if etat.nature != "etat":
        raise ValueError(f"decide attend une RSN d'état, pas une {etat.nature}")
    if etat.jeu == "morpion":
        return decide_morpion(etat, budget)
    if etat.jeu == "echecs":
        return decide_echecs(etat, budget)
    if etat.jeu == "dames":
        return decide_dames(etat, budget)
    if etat.jeu == "go":
        return decide_go(etat, budget)
    if etat.jeu == "cartes":
        return decide_cartes(etat, budget)
    raise ValueError(f"jeu inconnu : {etat.jeu}")
