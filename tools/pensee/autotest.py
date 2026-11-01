#!/usr/bin/env python3
"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.

  T0  le store est canonique          aller-retour exact, empreinte stable, ordres différents
  T1  l'arbre se rejoue               mêmes empreintes, mêmes scores ; une graine changée diverge
  T2  une stratégie est substituable  même arbre, deux stratégies ; une stratégie aveugle échoue
  T3  le moteur est anytime           best-so-far non décroissant ; un budget nul est refusé
  T4  la justification est valide     chemin racine → settled ; un chemin inventé est refusé
  T5  AC-3 se branche                 une chaîne propage, une contradiction se voit, la carte
                                      arc-consistante ne se réduit pas (contrôle)
  T6  alpha-bêta décide               gagner en un coup, bloquer, couper ; le minimax exact
                                      visite plus de nœuds ; la profondeur 1 sans évaluation rate

Usage : PYTHONPATH=. ~/gpu-env/bin/python tools/pensee/autotest.py
"""
from __future__ import annotations

import sys
from dataclasses import replace

from .coeur import Candidat, Etat
from .cruches import CRUCHES
from .csp import (AC3, CARTE_AUSTRALIE, CSP_CONTRADICTION, CSP_PROPAGATION,
                  domaines_de, probleme_csp, resoudre, verifier_arc_consistance)
from .jeux import MORPION, AlphaBeta, case_jouee, etat_morpion, gagnant, plateau_de
from .moteur import AStar, BFS, Moteur, Strategie
from .store import Budget, justification_valide, replay, diff


class Aveugle(Strategie):
    nom = "aveugle"

    def choisir(self, store, probleme):
        return min(store.ouverts, key=lambda f: store.ouverts[f])

    def proposer(self, etat, probleme):
        return []


def t0_store() -> tuple[bool, str]:
    a = Etat("s1", None, 0, (Candidat("c1", {"x": 1}), Candidat("c2", {"x": 2})))
    b = Etat("s2", None, 0, (Candidat("c2", {"x": 2}), Candidat("c1", {"x": 1})))
    m = Moteur()
    f1 = m.store.put(a)
    f2 = m.store.put(b)
    if f1 != f2:
        return False, "deux ordres d'insertion donnent deux empreintes"
    if m.store.get(f1) is None:
        return False, "get ne rend pas l'état"
    if m.store.put(a) != f1:
        return False, "put n'est pas idempotent"
    different = Etat("s3", None, 0, (Candidat("c1", {"x": 9}),))
    if m.store.put(different) == f1:
        return False, "deux états différents ont la même empreinte (contrôle négatif raté)"
    return True, "aller-retour exact, empreinte stable sous permutation"


def t1_rejeu() -> tuple[bool, str]:
    m = Moteur()
    d = m.boucle(CRUCHES, BFS(), Budget(200), arret_sur_but=True)
    replay(m.store, m.trace, CRUCHES)
    m2 = Moteur()
    d2 = m2.boucle(CRUCHES, BFS(), Budget(200), arret_sur_but=True)
    if diff(m.trace, m2.trace) is not None:
        return False, "deux exécutions identiques divergent"
    return True, f"rejeu identique sur {len(m.trace.evenements)} événements ; deux exécutions égales"


def t1_graine() -> tuple[bool, str]:
    from .moteur import MCTSLite
    m = Moteur()
    m.boucle(CRUCHES, MCTSLite(graine=1), Budget(120))
    n = Moteur()
    n.boucle(CRUCHES, MCTSLite(graine=2), Budget(120))
    if diff(m.trace, n.trace) is None:
        return False, "deux graines donnent la même trace (contrôle négatif raté)"
    return True, "deux graines divergent au premier pas différent"


def t2_strategies() -> tuple[bool, str]:
    m = Moteur()
    d = m.boucle(CRUCHES, BFS(), Budget(200), arret_sur_but=True)
    n = Moteur()
    d2 = n.boucle(CRUCHES, AStar(), Budget(200), arret_sur_but=True)
    if not (CRUCHES.but(d.etat) and CRUCHES.but(d2.etat)):
        return False, "une des deux stratégies n'atteint pas le but"
    if m.trace.settled and n.trace.settled and m.trace.settled[0] != n.trace.settled[0]:
        return False, "les deux stratégies ne trouvent pas le même état settled"
    aveugle = Moteur()
    aveugle.boucle(CRUCHES, Aveugle(), Budget(50))
    if aveugle.trace.settled:
        return False, "une stratégie qui ne propose rien a trouvé un but (contrôle raté)"
    return True, "BFS et A* atteignent le même but ; la stratégie aveugle échoue"


def t3_anytime() -> tuple[bool, str]:
    scores = []
    for budget in (20, 40, 80, 160, 320):
        m = Moteur()
        d = m.boucle(CRUCHES, BFS(), Budget(budget), arret_sur_but=True)
        scores.append(CRUCHES.score(d.etat))
    if any(b + 1e-9 < a for a, b in zip(scores, scores[1:])):
        return False, f"best-so-far décroît : {scores}"
    try:
        Budget(0)
        return False, "un budget nul a été accepté (contrôle négatif raté)"
    except ValueError:
        pass
    return True, f"best-so-far non décroissant sur 5 budgets : {[round(s, 2) for s in scores]}"


def t4_justification() -> tuple[bool, str]:
    m = Moteur()
    d = m.boucle(CRUCHES, BFS(), Budget(200), arret_sur_but=True)
    if not justification_valide(m.store, d.justification):
        return False, "la justification rendue n'est pas un chemin racine → but"
    inventé = d.justification + ["0" * 64]
    if justification_valide(m.store, inventé):
        return False, "un chemin inventé a été accepté (contrôle négatif raté)"
    return True, f"justification valide sur {len(d.justification)} nœuds ; chemin inventé refusé"


def t5_ac3() -> tuple[bool, str]:
    """La chaîne propage, la contradiction se voit, la carte est déjà arc-consistante."""
    m = Moteur()
    d = m.boucle(probleme_csp(CSP_PROPAGATION), AC3(CSP_PROPAGATION), Budget(100),
                 arret_sur_but=True)
    dom = domaines_de(d.etat)
    chaine = (dom == {"A": ("r",), "B": ("g",), "C": ("r",)}
              and verifier_arc_consistance(CSP_PROPAGATION, dom)
              and resoudre(CSP_PROPAGATION, dom) is not None
              and d.etat.statut == "settled")
    m2 = Moteur()
    d2 = m2.boucle(probleme_csp(CARTE_AUSTRALIE), AC3(CARTE_AUSTRALIE), Budget(300))
    dom2 = domaines_de(d2.etat)
    carte = (verifier_arc_consistance(CARTE_AUSTRALIE, dom2)
             and resoudre(CARTE_AUSTRALIE, dom2) is not None
             and all(len(v) == 3 for v in dom2.values()))
    m3 = Moteur()
    d3 = m3.boucle(probleme_csp(CSP_CONTRADICTION), AC3(CSP_CONTRADICTION), Budget(100))
    dom3 = domaines_de(d3.etat)
    contradiction = any(not v for v in dom3.values()) and resoudre(CSP_CONTRADICTION, dom3) is None
    ok = chaine and carte and contradiction
    return ok, (f"chaîne {dom} ; carte 3-colorable non réduite ; "
                f"contradiction domaine vide = {contradiction}")


def t6_alphabeta() -> tuple[bool, str]:
    """Gagner en un coup, bloquer, et couper : le minimax exact visite plus de nœuds."""
    gagnante = ("X", "X", ".", "O", "O", ".", ".", ".", ".")
    e = etat_morpion(gagnante, "X")
    d = AlphaBeta(profondeur=9).decider(replace(MORPION, initial=lambda: e))
    win = case_jouee(e, d.etat)
    gagne = gagnant(plateau_de(d.etat)) == "X"
    blocage = ("X", ".", ".", "O", "O", ".", "X", ".", ".")
    e2 = etat_morpion(blocage, "X")
    p2 = replace(MORPION, initial=lambda: e2)
    d2 = AlphaBeta(profondeur=9).decider(p2)
    d1 = AlphaBeta(profondeur=1, evaluer=lambda _e: 0.0).decider(p2)
    bloque = case_jouee(e2, d2.etat) == 5
    rate = case_jouee(e2, d1.etat) == 1
    ab = AlphaBeta(profondeur=5, pruning=True)
    da = ab.decider(MORPION, Budget(200_000))
    mm = AlphaBeta(profondeur=5, pruning=False)
    dm = mm.decider(MORPION, Budget(200_000))
    coupe = ab.noeuds < mm.noeuds and ab.coupes > 0
    ok = gagne and win == 2 and bloque and rate and coupe
    return ok, (f"gain en {win} ; blocage en 5 ; profondeur 1 rate (1) ; "
                f"alpha-bêta {ab.noeuds} nœuds/{ab.coupes} coupes vs minimax {mm.noeuds}")


def main() -> int:
    portes = [("T0 store canonique", t0_store()), ("T1 rejeu", t1_rejeu()),
              ("T1 graine", t1_graine()), ("T2 stratégies", t2_strategies()),
              ("T3 anytime", t3_anytime()), ("T4 justification", t4_justification()),
              ("T5 AC-3", t5_ac3()), ("T6 alpha-bêta", t6_alphabeta())]
    échecs = 0
    for nom, (ok, msg) in portes:
        print(f"  {'✅' if ok else '❌'} {nom:22s} {msg}")
        échecs += 0 if ok else 1
    print(f"  {len(portes) - échecs}/{len(portes)} portes tenues")
    return 1 if échecs else 0


if __name__ == "__main__":
    sys.exit(main())
