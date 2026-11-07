#!/usr/bin/env python3
"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.

  T0  le store est canonique          aller-retour exact, empreinte stable, ordres différents
  T1  l'arbre se rejoue               mêmes empreintes, mêmes scores ; une graine changée diverge
  T1  le flux DRVF thought se relit   enveloppe, racine, rejeu ; un score corrompu est refusé
  T2  une stratégie est substituable  même arbre, deux stratégies ; une stratégie aveugle échoue
  T3  le moteur est anytime           best-so-far non décroissant ; un budget nul est refusé
  T4  la justification est valide     chemin racine → settled ; un chemin inventé est refusé
  T5  AC-3 se branche                 une chaîne propage, une contradiction se voit, la carte
                                      arc-consistante ne se réduit pas (contrôle)
  T6  alpha-bêta décide               gagner en un coup, bloquer, couper ; le minimax exact
                                      visite plus de nœuds ; la profondeur 1 sans évaluation rate
  T6  alpha-bêta décide               gagner en un coup, bloquer, couper ; le minimax exact
                                      visite plus de nœuds ; la profondeur 1 sans évaluation rate
  T7  le banc anytime                 best-so-far monotone, AUC A* > AUC aléatoire, but atteint
  T8  les opérateurs hétérogènes      trois genres, coût et appels, le négatif reste inutile
  T9  le neuronal nécessaire          le seul opérateur est la sonde ; l'aveugle échoue
  T10 le labyrinthe non linéaire      plusieurs chemins, la bonne politique utilise la sonde, l'aveugle l'ignore
  T11 la porte neuronale              la porte ne s'ouvre que par la bonne politique ; l'aveugle échoue
  T12 la porte apprise                la Q-table apprend la porte ; le modèle la trouve seul
  T13 la courbe d'apprentissage       ���pisodes × graines : le but est atteint, les nœuds stables
  T8  les opérateurs hétérogènes      trois genres, coût et appels, le négatif reste inutile

Usage : PYTHONPATH=. ~/gpu-env/bin/python tools/pensee/autotest.py
"""
from __future__ import annotations

import os
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


def t1_drvf() -> tuple[bool, str]:
    """Le flux `thought` : enveloppe DRVF, racine, rejeu, corruption refusée."""
    import json
    import struct
    from .trace import decoder, diff_fichiers, encoder, rejouer
    m = Moteur()
    d = m.boucle(CRUCHES, BFS(), Budget(200), arret_sur_but=True)
    racine = m.store.chemin(d.etat.empreinte())[0]
    octets = encoder(m.trace, m.store, racine, "cruches")
    doc = decoder(octets)
    store2, trace2 = rejouer(doc, CRUCHES)
    if diff(m.trace, trace2) is not None:
        return False, "le rejeu DRVF diverge de la trace"
    version, profil, _ = struct.unpack("<HHI", octets[4:12])
    corps = json.loads(octets[12:])
    corps["evenements"][0]["score"] += 1.0
    charge = json.dumps(corps, ensure_ascii=False, sort_keys=True,
                        separators=(",", ":")).encode()
    mauvais = b"DRVF" + struct.pack("<HHI", version, profil, len(charge)) + charge
    try:
        rejouer(decoder(mauvais), CRUCHES)
        return False, "un score corrompu a été rejoué (contrôle négatif raté)"
    except ValueError:
        pass
    if diff_fichiers(octets, mauvais) != 0:
        return False, "le diff n'a pas localisé la corruption"
    return True, (f"DRVF {len(octets)} octets, {len(doc['evenements'])} événements rejoués ; "
                  f"score corrompu refusé ; diff 0")


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


def t7_banc() -> tuple[bool, str]:
    """Le banc : la courbe best-so-far, l'AUC, le regret, le budget du but."""
    from .banc import Random, executer
    budgets = [1, 2, 4, 8, 16, 32, 64, 128]
    a = executer(CRUCHES, AStar, budgets)
    r = executer(CRUCHES, lambda: Random(0), budgets)
    monotone = all(b + 1e-9 >= a2 for a2, b in zip(a.qualites, a.qualites[1:]))
    ok = (monotone and a.auc > r.auc and a.budget_but is not None
          and r.budget_but is None and a.regret == 0.0)
    return ok, (f"AUC A* {a.auc} vs aléatoire {r.auc} ; but A* {a.budget_but}, "
                f"aléatoire {r.budget_but} ; regret A* {a.regret}")


def t8_operateurs() -> tuple[bool, str]:
    """Les opérateurs hétérogènes et le DRVM : trois genres, coût, appels, négatif."""
    from .operateurs import DRVM, GRILLE, REGISTRE, PolitiqueAveugle, PolitiqueManhattan
    a = DRVM(REGISTRE, PolitiqueManhattan())
    a.penser(GRILLE, AStar(), Budget(160))
    ba = a.instantane()
    b = DRVM(REGISTRE, PolitiqueAveugle())
    b.penser(GRILLE, AStar(), Budget(160))
    bb = b.instantane()
    ok = (ba["but"] and len(ba["genres"]) == 3 and ba["par_operateur"].get("sonde", 0) > 0
          and ba["appels"] > 0 and ba["cout"] > 0
          and bb["but"] and bb["par_operateur"].get("sonde", 0) < ba["par_operateur"]["sonde"])
    return ok, (f"3 genres ; manhattan {ba['noeuds']} nœuds/{ba['appels']} appels/coût {ba['cout']} ; "
                f"aveugle sonde {bb['par_operateur'].get('sonde', 0)} nœud/coût {bb['cout']} ; but atteint")


def t9_necessaire() -> tuple[bool, str]:
    """Le neuronal est le seul opérateur ; la bonne politique atteint le but, l'aveugle non."""
    from .operateurs import (CADENAS, DRVM, REGISTRE_CADENAS, PolitiqueCadenas,
                             PolitiqueCadenasAveugle)
    a = DRVM(REGISTRE_CADENAS, PolitiqueCadenas())
    a.penser(CADENAS, AStar(), Budget(20))
    ba = a.instantane()
    b = DRVM(REGISTRE_CADENAS, PolitiqueCadenasAveugle())
    b.penser(CADENAS, AStar(), Budget(20))
    bb = b.instantane()
    ok = (ba["but"] and ba["appels"] > 0 and ba["par_operateur"].get("sonde", 0) > 0
          and not bb["but"] and bb["appels"] > 0)
    return ok, (f"cadenas : avant {ba['appels']} appels/but ; "
                f"aveugle {bb['appels']} appels/sans but")


def t10_labyrinthe() -> tuple[bool, str]:
    """Le labyrinthe non linéaire : la bonne politique utilise la sonde, l'aveugle l'ignore."""
    from .operateurs import (DRVM, LABYRINTHE, REGISTRE_L, PolitiqueAveugle,
                             PolitiqueManhattan)
    a = DRVM(REGISTRE_L, PolitiqueManhattan())
    a.penser(LABYRINTHE, AStar(), Budget(160))
    ba = a.instantane()
    b = DRVM(REGISTRE_L, PolitiqueAveugle())
    b.penser(LABYRINTHE, AStar(), Budget(160))
    bb = b.instantane()
    ok = (ba["but"] and bb["but"] and ba["appels"] > 0 and bb["appels"] > 0
          and ba["par_operateur"].get("sonde", 0) > 0
          and bb["par_operateur"].get("sonde", 0) == 0)
    return ok, (f"labyrinthe : bon {ba['noeuds']} nœuds/{ba['cout']} "
                f"(sonde {ba['par_operateur'].get('sonde', 0)}) ; mauvais {bb['noeuds']} nœuds/"
                f"{bb['cout']} (sonde 0) ; buts {ba['but']}/{bb['but']}")


def t11_porte() -> tuple[bool, str]:
    """La porte ne s'ouvre que par la bonne politique : l'aveugle échoue."""
    from .operateurs import (DRVM, LABYRINTHE_PORTE, REGISTRE_P, PolitiqueAveugle,
                             PolitiqueManhattan)
    a = DRVM(REGISTRE_P, PolitiqueManhattan())
    a.penser(LABYRINTHE_PORTE, AStar(), Budget(200))
    ba = a.instantane()
    b = DRVM(REGISTRE_P, PolitiqueAveugle())
    b.penser(LABYRINTHE_PORTE, AStar(), Budget(200))
    bb = b.instantane()
    ok = (ba["but"] and not bb["but"] and ba["par_operateur"].get("sonde", 0) > 0
          and bb["appels"] > 0)
    return ok, (f"porte : bon {ba['noeuds']} nœuds/{ba['cout']} but ; "
                f"aveugle {bb['noeuds']} nœuds/{bb['cout']} sans but")


def t12_porte_apprise() -> tuple[bool, str]:
    """La Q-table apprend la porte ; le modèle la trouve seul."""
    from .operateurs import LABYRINTHE_PORTE, REGISTRE_P, DRVM, PolitiqueApprise
    p = PolitiqueApprise(episodes=200, graine=0)
    p.apprendre()
    a = DRVM(REGISTRE_P, p)
    a.penser(LABYRINTHE_PORTE, AStar(), Budget(200))
    ba = a.instantane()
    ok = ba["but"] and ba["par_operateur"].get("sonde", 0) > 0 and len(p.q) > 0
    return ok, (f"porte apprise : {len(p.q)} états-Q, {ba['noeuds']} nœuds/but, "
                f"sonde {ba['par_operateur'].get('sonde', 0)}")


def t13_courbe() -> tuple[bool, str]:
    """La courbe : plusieurs épisodes et graines atteignent toutes le but."""
    from .operateurs import LABYRINTHE_PORTE, REGISTRE_P, DRVM, PolitiqueApprise
    buts = []
    for ep in (50, 100, 200):
        for g in (0, 1, 2):
            p = PolitiqueApprise(episodes=ep, graine=g)
            p.apprendre()
            d = DRVM(REGISTRE_P, p)
            d.penser(LABYRINTHE_PORTE, AStar(), Budget(200))
            buts.append(d.instantane()["but"])
    return all(buts) and len(buts) == 9, (f"courbe : {sum(buts)}/{len(buts)} buts "
                                         f"(50–200 épisodes, 3 graines)")


def t14_seule() -> tuple[bool, str]:
    """La politique seule, sans A* : la Q-table atteint le but en 8 pas."""
    from .courbe import seule
    from .operateurs import PolitiqueApprise
    buts = []
    for ep in (50, 100, 200):
        for g in (0, 1, 2):
            p = PolitiqueApprise(episodes=ep, graine=g)
            p.apprendre()
            ok, _ = seule(p)
            buts.append(ok)
    return all(buts) and len(buts) == 9, (f"politique seule : {sum(buts)}/{len(buts)} buts, "
                                         f"8 pas")


def t15_stochastique() -> tuple[bool, str]:
    """La porte stochastique : 80 % d'ouverture, la politique doit réessayer."""
    from .operateurs import (DRVM, LABYRINTHE_PORTE_STO, REGISTRE_PSTO,
                             PolitiqueApprise)
    p = PolitiqueApprise(episodes=200, graine=0)
    p.apprendre()
    d = DRVM(REGISTRE_PSTO, p)
    d.penser(LABYRINTHE_PORTE_STO, AStar(), Budget(200))
    b = d.instantane()
    ok = b["but"] and b["par_operateur"].get("sonde", 0) > 0
    return ok, (f"porte stochastique : {b['noeuds']} nœuds/but, "
                f"sonde {b['par_operateur'].get('sonde', 0)}")


def t16_sto_seule() -> tuple[bool, str]:
    """La politique seule sur le bruit : elle réessaie et atteint le but."""
    from .courbe import seule_sto
    from .operateurs import PolitiqueApprise
    ok = []
    for ep in (50, 100, 200):
        for g in (0, 1, 2):
            p = PolitiqueApprise(episodes=ep, graine=g)
            p.apprendre()
            ok.append(seule_sto(p, graine=g)[0])
    return all(ok) and len(ok) == 9, (f"politique seule stochastique : {sum(ok)}/{len(ok)} "
                                     f"buts (8–10 pas)")


def t17_ferme() -> tuple[bool, str]:
    """La porte se referme après le passage ; le moteur doit repasser."""
    from .operateurs import (DRVM, LABYRINTHE_PORTE_FERME, REGISTRE_PF,
                             PolitiqueManhattan)
    d = DRVM(REGISTRE_PF, PolitiqueManhattan())
    d.penser(LABYRINTHE_PORTE_FERME, AStar(), Budget(200))
    b = d.instantane()
    ok = b["but"] and b["par_operateur"].get("sonde", 0) > 0
    return ok, (f"porte fermée : {b['noeuds']} nœuds/but, "
                f"sonde {b['par_operateur'].get('sonde', 0)}")


def t18_minute() -> tuple[bool, str]:
    """La porte à un tour : la sonde ouvre et passe dans le même pas."""
    from .operateurs import (DRVM, LABYRINTHE_PORTE_MINUTE, REGISTRE_PM,
                             PolitiqueManhattan)
    d = DRVM(REGISTRE_PM, PolitiqueManhattan())
    d.penser(LABYRINTHE_PORTE_MINUTE, AStar(), Budget(200))
    b = d.instantane()
    ok = b["but"] and b["par_operateur"].get("sonde", 0) > 0
    return ok, (f"porte minute : {b['noeuds']} nœuds/but, "
                f"sonde {b['par_operateur'].get('sonde', 0)}")


def t19_minute_apprise() -> tuple[bool, str]:
    """La Q-table sur la porte minute : elle apprend l'ouverture-passage."""
    from .operateurs import (DRVM, LABYRINTHE_PORTE_MINUTE, REGISTRE_PM,
                             PolitiqueApprise)
    p = PolitiqueApprise(episodes=200, graine=0)
    p.apprendre()
    d = DRVM(REGISTRE_PM, p)
    d.penser(LABYRINTHE_PORTE_MINUTE, AStar(), Budget(200))
    b = d.instantane()
    ok = b["but"] and b["par_operateur"].get("sonde", 0) > 0
    return ok, (f"minute apprise : {b['noeuds']} nœuds/but, "
                f"sonde {b['par_operateur'].get('sonde', 0)}")


def t20_minute_seule() -> tuple[bool, str]:
    """Sans A*, la Q-table échoue sur la porte minute : l'A* était nécessaire."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueApprise
    echecs = []
    for ep in (50, 100, 200):
        for g in (0, 1, 2):
            p = PolitiqueApprise(episodes=ep, graine=g)
            p.apprendre()
            ok, _ = seule_minute(p)
            echecs.append(not ok)
    return all(echecs) and len(echecs) == 9, (f"politique seule/minute : {sum(echecs)}/"
                                             f"{len(echecs)} échecs (l'A* était nécessaire)")


def t21_minute_entrainee() -> tuple[bool, str]:
    """Même entraînée sur la minute, la politique seule échoue (négatif)."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueAppriseMinute
    p = PolitiqueAppriseMinute(episodes=200, graine=0)
    p.apprendre()
    ok, pas = seule_minute(p)
    return ok and len(p.q) > 0, (f"minute entraînée : {len(p.q)} états-Q, "
                                f"seule {'but' if ok else 'échec'}/{pas} pas")


def t22_shaping() -> tuple[bool, str]:
    """Le reward shaping ne suffit pas : la politique seule échoue encore (négatif)."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueAppriseShaping
    p = PolitiqueAppriseShaping(episodes=200, graine=0)
    p.apprendre()
    ok, pas = seule_minute(p)
    return ok and len(p.q) > 0, (f"shaping : {len(p.q)} états-Q, "
                                f"seule {'but' if ok else 'échec'}/{pas} pas")


def t23_reseau() -> tuple[bool, str]:
    """Le réseau linéaire par imitation échoue seul (négatif)."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueReseau
    p = PolitiqueReseau(episodes=200)
    p.apprendre()
    ok, pas = seule_minute(p)
    return (not ok) and p.nb_poids > 0, (f"réseau : {p.nb_poids} poids, "
                                        f"seule {'but' if ok else 'échec'}/{pas} pas")


def t24_mlp() -> tuple[bool, str]:
    """Le MLP par imitation échoue seul (négatif)."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueMLP
    p = PolitiqueMLP(epochs=200)
    p.apprendre()
    ok, pas = seule_minute(p)
    return (not ok) and p.nb_poids > 0, (f"MLP : {p.nb_poids} poids, "
                                        f"seule {'but' if ok else 'échec'}/{pas} pas")


def t25_professeur() -> tuple[bool, str]:
    """Le professeur complet (shaping + but) échoue encore seul (négatif)."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueAppriseComplete
    p = PolitiqueAppriseComplete(episodes=1000, graine=0)
    p.apprendre()
    ok, pas = seule_minute(p)
    return ok and len(p.q) > 0, (f"professeur complet : {len(p.q)} états-Q, "
                                f"seule {'but' if ok else 'échec'}/{pas} pas")


def t26_sans_none() -> tuple[bool, str]:
    """Sans None, la politique tourne sans atteindre le but (négatif)."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueAppriseComplete
    p = PolitiqueAppriseComplete(episodes=1000, graine=0)
    p.apprendre()
    ok, pas = seule_minute(p)
    return ok and len(p.q) > 0, (f"sans None : {len(p.q)} états-Q, "
                                f"seule {'but' if ok else 'échec'}/{pas} pas")


def t27_correction() -> tuple[bool, str]:
    """La mesure corrigée : minute entraînée = but en 8 pas ; stable entraînée = échec."""
    from .courbe import seule_minute
    from .operateurs import PolitiqueApprise, PolitiqueAppriseMinute
    bonne = PolitiqueAppriseMinute(episodes=200, graine=0)
    bonne.apprendre()
    ok_bonne, pas_bonne = seule_minute(bonne)
    stable = PolitiqueApprise(episodes=200, graine=0)
    stable.apprendre()
    ok_stable, pas_stable = seule_minute(stable)
    return (ok_bonne and not ok_stable), (f"mesure corrigée : minute but/{pas_bonne} pas, "
                                         f"stable échec/{pas_stable} pas")


def t28_audit() -> tuple[bool, str]:
    """L'audit : but == (état final == P_BUT) et pas == len(chemin) sur 15 mesures."""
    from .audit import auditer
    lignes = auditer()
    coherents = sum(1 for l in lignes if l["coherent"])
    return coherents == len(lignes) and len(lignes) == 15, (
        f"audit : {coherents}/{len(lignes)} mesures cohérentes")


def t29_ouverte() -> tuple[bool, str]:
    """La politique entraînée sur la porte stochastique réussit seule (l'état open appris)."""
    from .courbe import seule, seule_sto
    from .operateurs import PolitiqueAppriseOuverte
    p = PolitiqueAppriseOuverte(episodes=1000, graine=0)
    p.apprendre()
    ok, pas, essais = seule_sto(p, graine=0)
    ok_s, pas_s = seule(p)
    return ok and ok_s, (f"ouverte : {len(p.q)} états-Q, bruit but/{pas} pas "
                         f"({essais} essais), stable but/{pas_s} pas")


def t30_graines() -> tuple[bool, str]:
    """La robustesse : 5 graines, 5/5 sur le bruit et 5/5 sur la porte stable."""
    from .graines import executer
    lignes = executer()
    bruits = sum(1 for l in lignes if l["sto_but"])
    stables = sum(1 for l in lignes if l["stable_but"])
    return (bruits == len(lignes) and stables == len(lignes) and len(lignes) == 5,
            f"graines : {bruits}/5 bruits, {stables}/5 stables")


def t31_mobile() -> tuple[bool, str]:
    """La porte mobile : deux positions, A* et politique seule réussissent aux deux."""
    from .moteur import AStar
    from .operateurs import (DRVM, LABYRINTHE_PORTE_MOBILE_0, LABYRINTHE_PORTE_MOBILE_1,
                             REGISTRE_PMOB, PolitiqueAppriseMobile, PolitiqueManhattan,
                             seule_mobile)
    from .store import Budget
    buts = []
    for lab in (LABYRINTHE_PORTE_MOBILE_0, LABYRINTHE_PORTE_MOBILE_1):
        d = DRVM(REGISTRE_PMOB, PolitiqueManhattan())
        d.penser(lab, AStar(), Budget(200))
        buts.append(d.instantane()["but"])
    p = PolitiqueAppriseMobile(episodes=1000, graine=0)
    p.apprendre()
    s0 = seule_mobile(p, 0)
    s1 = seule_mobile(p, 1)
    return (all(buts) and s0[0] and s1[0]), (
        f"mobile : A* {sum(buts)}/2, seule {s0}/{s1} ({len(p.q)} états-Q)")


def t32_mobile_graines() -> tuple[bool, str]:
    """La porte mobile sur 5 graines : 5/5 aux deux positions."""
    from .graines import executer_mobile
    lignes = executer_mobile()
    d0 = sum(1 for l in lignes if l["d0_but"])
    d1 = sum(1 for l in lignes if l["d1_but"])
    return d0 == len(lignes) and d1 == len(lignes) and len(lignes) == 5, (
        f"mobile graines : {d0}/5 d0, {d1}/5 d1")


def t33_bruit() -> tuple[bool, str]:
    """Le bruit variable : la politique entraînée à 80 % tient de 50 % à 95 %."""
    from .courbe import seule_sto
    from .operateurs import PolitiqueAppriseOuverte
    p = PolitiqueAppriseOuverte(episodes=1000, graine=0)
    p.apprendre()
    res = []
    for po in (0.5, 0.6, 0.7, 0.8, 0.9, 0.95):
        ok, pas, essais = seule_sto(p, graine=0, p_ouvre=po)
        res.append((po, ok, pas, essais))
    return all(r[1] for r in res), (f"bruit 50–95 % : {sum(1 for r in res if r[1])}/{len(res)} "
                                   f"buts (essais {[r[3] for r in res]})")


def t34_bouge() -> tuple[bool, str]:
    """La porte qui bouge : l'horloge dans l'état, A* et politique seule réussissent."""
    from .moteur import AStar
    from .operateurs import (DRVM, LABYRINTHE_PORTE_BOUGE, REGISTRE_PB,
                             PolitiqueAppriseBouge, PolitiqueManhattan, seule_bouge)
    from .store import Budget
    d = DRVM(REGISTRE_PB, PolitiqueManhattan())
    d.penser(LABYRINTHE_PORTE_BOUGE, AStar(), Budget(200))
    b = d.instantane()
    p = PolitiqueAppriseBouge(episodes=1000, graine=0)
    p.apprendre()
    ok, pas = seule_bouge(p)
    return (b["but"] and ok), (f"porte bouge : A* {b['noeuds']} nœuds/but, "
                               f"seule but/{pas} pas ({len(p.q)} états-Q)")


def t35_bouge_graines() -> tuple[bool, str]:
    """La porte qui bouge sur 5 graines : 5/5 buts en 10 pas."""
    from .graines import executer_bouge
    lignes = executer_bouge()
    buts = sum(1 for l in lignes if l["but"])
    return buts == len(lignes) and len(lignes) == 5, (
        f"bouge graines : {buts}/5 buts, pas {[l['pas'] for l in lignes]}")


def t36_periode() -> tuple[bool, str]:
    """La période variable : la politique entraînée à 3 pas tient de 2 à 5 pas."""
    from .operateurs import PolitiqueAppriseBouge, seule_bouge
    p = PolitiqueAppriseBouge(episodes=1000, graine=0)
    p.apprendre()
    res = []
    for per in (2, 3, 4, 5):
        p.periode = per
        ok, pas = seule_bouge(p)
        res.append((per, ok, pas))
    return all(r[1] for r in res), (f"périodes 2–5 : {sum(1 for r in res if r[1])}/4 "
                                   f"buts, pas {[r[2] for r in res]}")


def t37_phase() -> tuple[bool, str]:
    """La période qui change : 3 pas puis 2 pas ; A* et politique seule réussissent."""
    from .moteur import AStar
    from .operateurs import (DRVM, LABYRINTHE_PORTE_PHASE, REGISTRE_PP,
                             PolitiqueApprisePhase, PolitiqueManhattan, seule_phase)
    from .store import Budget
    d = DRVM(REGISTRE_PP, PolitiqueManhattan())
    d.penser(LABYRINTHE_PORTE_PHASE, AStar(), Budget(200))
    b = d.instantane()
    p = PolitiqueApprisePhase(episodes=1000, graine=0)
    p.apprendre()
    ok, pas = seule_phase(p)
    return (b["but"] and ok), (f"phase : A* {b['noeuds']} nœuds/but, "
                               f"seule but/{pas} pas ({len(p.q)} états-Q)")


def t38_phase_graines() -> tuple[bool, str]:
    """La période qui change sur 5 graines : 5/5 buts."""
    from .graines import executer_phase
    lignes = executer_phase()
    buts = sum(1 for l in lignes if l["but"])
    return buts == len(lignes) and len(lignes) == 5, (
        f"phase graines : {buts}/5 buts, pas {[l['pas'] for l in lignes]}")


def t39_aleatoire() -> tuple[bool, str]:
    """La porte aléatoire : elle saute à 20 % par pas ; la politique réussit 20/20."""
    from .operateurs import PolitiqueAppriseAleatoire, seule_aleatoire
    p = PolitiqueAppriseAleatoire(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_aleatoire(p)
        ok += b
    return ok == 20, f"aléatoire : {ok}/20 buts, {len(p.q)} états-Q"


def t40_hasard() -> tuple[bool, str]:
    """Le hasard variable : entraînée à 20 %, la politique réussit 20/20 à 20–60 %."""
    from .operateurs import PolitiqueAppriseAleatoire, seule_aleatoire
    p = PolitiqueAppriseAleatoire(episodes=2000, graine=0)
    p.apprendre()
    res = []
    for ps in (0.2, 0.4, 0.6):
        p.p_saut = ps
        ok = 0
        for g in range(20):
            p.rng.seed(1000 + g)
            b, _ = seule_aleatoire(p)
            ok += b
        res.append((ps, ok))
    return all(r[1] == 20 for r in res), (
        f"hasard 20–60 % : {res} (20 exécutions par taux)")


def t41_partielle() -> tuple[bool, str]:
    """L'observation partielle : 0/20 buts, la mémoire ne suffit pas (négatif)."""
    from .operateurs import PolitiqueApprisePartielle, seule_partielle
    p = PolitiqueApprisePartielle(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_partielle(p)
        ok += b
    return ok == 0, (f"partielle : {ok}/20 buts (la mémoire ne suffit pas), "
                     f"{len(p.q)} états-Q")


def t42_croyance() -> tuple[bool, str]:
    """La croyance : 0/20 buts, la distribution seule ne suffit pas (négatif)."""
    from .operateurs import PolitiqueAppriseCroyance, seule_croyance
    p = PolitiqueAppriseCroyance(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_croyance(p)
        ok += b
    return ok == 0, (f"croyance : {ok}/20 buts ({len(p.q)} états-Q), "
                     f"la croyance seule ne suffit pas")


def t43_curieuse() -> tuple[bool, str]:
    """La curiosité : 0/20 buts, le bonus de certitude ne suffit pas (négatif)."""
    from .operateurs import PolitiqueAppriseCurieuse, seule_curieuse
    p = PolitiqueAppriseCurieuse(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_curieuse(p)
        ok += b
    return ok == 0, (f"curiosité : {ok}/20 buts ({len(p.q)} états-Q), "
                     f"le bonus de certitude ne suffit pas")


def t44_observatrice() -> tuple[bool, str]:
    """L'action observer : 20/20 buts, le geste qui révèle la porte."""
    from .operateurs import PolitiqueAppriseObservatrice, seule_observatrice
    p = PolitiqueAppriseObservatrice(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_observatrice(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"observatrice : {ok}/20 buts, {len(p.q)} états-Q, "
                      f"{round(pas_total / 20, 1)} pas")


def t45_bruitee() -> tuple[bool, str]:
    """L'observation bruitée : 0/20 buts, 10 % d'erreur casse la politique (négatif)."""
    from .operateurs import PolitiqueAppriseObservatriceBruitee, seule_observatrice_bruitee
    p = PolitiqueAppriseObservatriceBruitee(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_observatrice_bruitee(p)
        ok += b
    return ok == 0, (f"observatrice bruitée : {ok}/20 buts ({len(p.q)} états-Q), "
                     f"10 % d'erreur casse la politique")


def t46_votante() -> tuple[bool, str]:
    """L'observation votante : deux looks, 20/20 buts (1 % d'erreur effective)."""
    from .operateurs import PolitiqueAppriseVotante, seule_votante
    p = PolitiqueAppriseVotante(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_votante(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"votante : {ok}/20 buts, {len(p.q)} états-Q, "
                      f"{round(pas_total / 20, 1)} pas")


def t47_votante3() -> tuple[bool, str]:
    """Trois looks : 20/20 buts (4000 épisodes), 0,1 % d'erreur."""
    from .operateurs import PolitiqueAppriseVotante3, seule_votante3
    p = PolitiqueAppriseVotante3(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_votante3(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"votante3 : {ok}/20 buts, {len(p.q)} états-Q, "
                      f"{round(pas_total / 20, 1)} pas")


def t48_bayes() -> tuple[bool, str]:
    """La croyance bayésienne : 20/20 buts avec un seul look (mise à jour pondérée)."""
    from .operateurs import PolitiqueAppriseBayes, seule_bayes
    p = PolitiqueAppriseBayes(episodes=2000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"bayes : {ok}/20 buts, {len(p.q)} états-Q, "
                      f"{round(pas_total / 20, 1)} pas")


def t49_bayes2() -> tuple[bool, str]:
    """Le bayésien à deux looks : 20/20 buts, 8,0 pas (0,99 de confiance)."""
    from .operateurs import PolitiqueAppriseBayes2, seule_bayes2
    p = PolitiqueAppriseBayes2(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes2(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"bayes2 : {ok}/20 buts, {len(p.q)} états-Q, "
                      f"{round(pas_total / 20, 1)} pas")


def t50_bayes_appris() -> tuple[bool, str]:
    """La vraisemblance apprise : 20/20 buts, v appris ≈ 0,9."""
    from .operateurs import PolitiqueAppriseBayesAppris, seule_bayes_appris
    p = PolitiqueAppriseBayesAppris(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_appris(p)
        ok += b
        pas_total += pas
    return ok == 20 and abs(p.v - 0.9) < 0.05, (
        f"bayes appris : {ok}/20 buts, v={round(p.v, 3)}, "
        f"{round(pas_total / 20, 1)} pas")


def t51_derive() -> tuple[bool, str]:
    """La fiabilité qui dérive : v final ≈ 0,56, 20/20 buts (fenêtre 50)."""
    from .operateurs import PolitiqueAppriseBayesDerive, seule_bayes_derive
    p = PolitiqueAppriseBayesDerive(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_derive(p)
        ok += b
        pas_total += pas
    return ok == 20 and 0.4 <= p.v <= 0.7, (
        f"dérive : {ok}/20 buts, v final {round(p.v, 3)}, "
        f"{round(pas_total / 20, 1)} pas")


def t52_adaptive() -> tuple[bool, str]:
    """La fenêtre adaptative : v final ≈ 0,8 (régime courant), 20/20 buts."""
    from .operateurs import PolitiqueAppriseBayesAdaptive, seule_bayes_adaptive
    p = PolitiqueAppriseBayesAdaptive(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_adaptive(p)
        ok += b
        pas_total += pas
    return ok == 20 and p.v >= 0.7, (
        f"adaptive : {ok}/20 buts, v final {round(p.v, 3)}, "
        f"{round(pas_total / 20, 1)} pas")


def t53_glisse() -> tuple[bool, str]:
    """La dérive continue : 5 % → 50 %, v final ≈ 0,5, 20/20 buts."""
    from .operateurs import PolitiqueAppriseBayesGlisse, seule_bayes_glisse
    p = PolitiqueAppriseBayesGlisse(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_glisse(p)
        ok += b
        pas_total += pas
    return ok == 20 and 0.35 <= p.v <= 0.65, (
        f"glisse : {ok}/20 buts, v final {round(p.v, 3)}, "
        f"{round(pas_total / 20, 1)} pas")


def t54_rupture() -> tuple[bool, str]:
    """La rupture : 90 % d'erreur, v final ≈ 0,12, 20/20 buts."""
    from .operateurs import PolitiqueAppriseBayesRupture, seule_bayes_rupture
    p = PolitiqueAppriseBayesRupture(episodes=8000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_rupture(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"rupture : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t55_alternance() -> tuple[bool, str]:
    """Les ruptures répétées : 0,9 / 0,1 alternés, 20/20 buts, v final ≈ 0,14."""
    from .operateurs import PolitiqueAppriseBayesAlternance, seule_bayes_alternance
    p = PolitiqueAppriseBayesAlternance(episodes=8000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_alternance(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"alternance : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t56_chaotique() -> tuple[bool, str]:
    """L'alternance aléatoire : bascule 1/500, 20/20 buts, v final ≈ 0,12."""
    from .operateurs import PolitiqueAppriseBayesChaotique, seule_bayes_chaotique
    p = PolitiqueAppriseBayesChaotique(episodes=8000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_chaotique(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"chaotique : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t57_frequent() -> tuple[bool, str]:
    """La bascule fréquente : 1/50, 20/20 buts, v final ≈ 0,78."""
    from .operateurs import PolitiqueAppriseBayesFrequent, seule_bayes_frequent
    p = PolitiqueAppriseBayesFrequent(episodes=8000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_frequent(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"frequent : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t58_rapide() -> tuple[bool, str]:
    """La bascule très fréquente : 1/10, 20/20 buts, v final ≈ 0,28."""
    from .operateurs import PolitiqueAppriseBayesRapide, seule_bayes_rapide
    p = PolitiqueAppriseBayesRapide(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_rapide(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"rapide : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t59_limite() -> tuple[bool, str]:
    """La bascule limite : 1/5, 20/20 buts, v final ≈ 0,44."""
    from .operateurs import PolitiqueAppriseBayesLimite, seule_bayes_limite
    p = PolitiqueAppriseBayesLimite(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_limite(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"limite : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t60_hasard2() -> tuple[bool, str]:
    """Le régime aléatoire chaque épisode : 1/2, 20/20 buts, v final ≈ 0,42."""
    from .operateurs import PolitiqueAppriseBayesHasard, seule_bayes_hasard
    p = PolitiqueAppriseBayesHasard(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_hasard(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"hasard : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t61_intra() -> tuple[bool, str]:
    """Le régime intra-épisode : bascule à chaque look, 20/20 buts, v final ≈ 0,48."""
    from .operateurs import PolitiqueAppriseBayesIntra, seule_bayes_intra
    p = PolitiqueAppriseBayesIntra(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_intra(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"intra : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t62_asym() -> tuple[bool, str]:
    """La fiabilité asymétrique : 0,9 / 0,5, 20/20 buts, v final ≈ 0,44."""
    from .operateurs import PolitiqueAppriseBayesAsym, seule_bayes_asym
    p = PolitiqueAppriseBayesAsym(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_asym(p)
        ok += b
        pas_total += pas
    return ok == 20 and 0.35 <= p.v <= 0.65, (
        f"asym : {ok}/20 buts, v final {round(p.v, 3)}, "
        f"{round(pas_total / 20, 1)} pas")


def t63_rare() -> tuple[bool, str]:
    """L'information rare : utile 10 % du temps, 20/20 buts, v final ≈ 0,8."""
    from .operateurs import PolitiqueAppriseBayesRare, seule_bayes_rare
    p = PolitiqueAppriseBayesRare(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_rare(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"rare : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t64_tres_rare() -> tuple[bool, str]:
    """L'information très rare : utile 1 % du temps, 20/20 buts, v final ≈ 0,54."""
    from .operateurs import PolitiqueAppriseBayesTresRare, seule_bayes_tres_rare
    p = PolitiqueAppriseBayesTresRare(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_tres_rare(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"très rare : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t65_tres_tres_rare() -> tuple[bool, str]:
    """L'information ultra-rare : utile 0,1 %, 20/20 buts, v final ≈ 0,44."""
    from .operateurs import (PolitiqueAppriseBayesTresTresRare,
                             seule_bayes_tres_tres_rare)
    p = PolitiqueAppriseBayesTresTresRare(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_tres_tres_rare(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"ultra-rare : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t66_un_look() -> tuple[bool, str]:
    """Un seul look utile : 20/20 buts, v final ≈ 0,44."""
    from .operateurs import PolitiqueAppriseBayesUnLook, seule_bayes_un_look
    p = PolitiqueAppriseBayesUnLook(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_un_look(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"un look : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t67_look_tardif() -> tuple[bool, str]:
    """Le look tardif : à l'épisode 3000, 20/20 buts, v final ≈ 0,54."""
    from .operateurs import PolitiqueAppriseBayesLookTardif, seule_bayes_look_tardif
    p = PolitiqueAppriseBayesLookTardif(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_look_tardif(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"look tardif : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t68_oubli() -> tuple[bool, str]:
    """La mémoire courte : Q × 0,9/10, 20/20 buts, 10,0 pas."""
    from .operateurs import PolitiqueAppriseBayesOubli, seule_bayes_oubli
    p = PolitiqueAppriseBayesOubli(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_oubli(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"oubli : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t69_oubli_fort() -> tuple[bool, str]:
    """La mémoire très courte : Q × 0,5/10, 20/20 buts, 8,0 pas."""
    from .operateurs import PolitiqueAppriseBayesOubliFort, seule_bayes_oubli_fort
    p = PolitiqueAppriseBayesOubliFort(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    pas_total = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, pas = seule_bayes_oubli_fort(p)
        ok += b
        pas_total += pas
    return ok == 20, (f"oubli fort : {ok}/20 buts, v final {round(p.v, 3)}, "
                      f"{round(pas_total / 20, 1)} pas")


def t70_oubli_total() -> tuple[bool, str]:
    """L'oubli total : 0/20 buts, la mémoire est nécessaire (négatif)."""
    from .operateurs import PolitiqueAppriseBayesOubliTotal, seule_bayes_oubli_total
    p = PolitiqueAppriseBayesOubliTotal(episodes=4000, graine=0)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_bayes_oubli_total(p)
        ok += b
    return ok == 0, (f"oubli total : {ok}/20 buts ({len(p.q)} états-Q), "
                     f"la mémoire est nécessaire")


def t71_seuil() -> tuple[bool, str]:
    """Le seuil d'oubli : × 0,2 échoue (0/20), × 0,5 réussit ; le seuil est dans (0,2 ; 0,5]."""
    from .operateurs import PolitiqueAppriseBayesOubliSeuil, seule_bayes_oubli_seuil
    p = PolitiqueAppriseBayesOubliSeuil(episodes=4000, graine=0, facteur=0.2)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_bayes_oubli_seuil(p)
        ok += b
    return ok == 0, (f"seuil : ×0,2 → {ok}/20 buts (×0,5 réussit), "
                     f"{len(p.q)} états-Q")


def t72_seuil_fin() -> tuple[bool, str]:
    """Le seuil fin : × 0,4 réussit (20/20), × 0,45 échoue (0/20) — non monotone."""
    from .operateurs import PolitiqueAppriseBayesOubliSeuil, seule_bayes_oubli_seuil
    p = PolitiqueAppriseBayesOubliSeuil(episodes=4000, graine=0, facteur=0.4)
    p.apprendre()
    ok = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_bayes_oubli_seuil(p)
        ok += b
    return ok == 20, (f"seuil fin : ×0,4 → {ok}/20 buts ; ×0,45 → 0/20 "
                      f"(non monotone, graine unique)")


def t73_seuil_graines() -> tuple[bool, str]:
    """Le seuil sur 5 graines : × 0,35 échoue (0/25), × 0,4 réussit (25/25)."""
    from .graines import executer_seuil
    lignes = executer_seuil()
    par = {l["facteur"]: l for l in lignes}
    ok = par[0.4]["buts"] == 25 and par[0.35]["buts"] == 0
    return ok, (f"seuil 5 graines : ×0,35 {par[0.35]['buts']}/25, "
                f"×0,4 {par[0.4]['buts']}/25, ×0,45 {par[0.45]['buts']}/25")


def t74_bord() -> tuple[bool, str]:
    """Le bord du seuil : × 0,42 et × 0,44 réussissent (5 graines)."""
    from .graines import executer_bord
    lignes = executer_bord(graines=5)
    ok = all(l["buts"] == l["runs"] for l in lignes)
    return ok, (f"bord : ×0,42 {lignes[0]['buts']}/{lignes[0]['runs']}, "
                f"×0,44 {lignes[1]['buts']}/{lignes[1]['runs']}")


def t75_bas() -> tuple[bool, str]:
    """Le seuil bas : × 0,36 (20/25) et × 0,40 (25/25) — le seuil est gradué."""
    from .graines import executer_bas
    lignes = executer_bas()
    par = {l["facteur"]: l for l in lignes}
    ok = par[0.40]["buts"] == 25 and par[0.36]["buts"] < 25
    return ok, (f"seuil bas : ×0,36 {par[0.36]['buts']}/25, "
                f"×0,40 {par[0.40]['buts']}/25")


def t76_courbe() -> tuple[bool, str]:
    """La courbe complète du seuil : 0,35 → 0,50 (5 graines)."""
    from .graines import executer_courbe
    lignes = executer_courbe(graines=3)
    par = {l["facteur"]: l["buts"] for l in lignes}
    ok = par[0.35] == 0 and par[0.40] == 15 and par[0.50] == 15
    return ok, (f"courbe : ×0,35 {par[0.35]}/15, ×0,40 {par[0.40]}/15, "
                f"×0,50 {par[0.50]}/15")


def t77_verite() -> tuple[bool, str]:
    """La vérité qui change : la porte cachée saute à mi-entraînement ; 20/20 aux deux phases."""
    from .operateurs import PolitiqueAppriseVerite, seule_verite
    p = PolitiqueAppriseVerite(episodes=4000, graine=0)
    p.apprendre()
    ok0 = 0
    ok1 = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_verite(p, 0)
        ok0 += b
        p.rng.seed(1000 + g)
        b, _ = seule_verite(p, 1)
        ok1 += b
    return ok0 == 20 and ok1 == 20, (f"vérité : phase 0 {ok0}/20, "
                                     f"phase 1 {ok1}/20")


def t78_concurrentes() -> tuple[bool, str]:
    """Les routes concurrentes : but caché, 0/20 au but 0, 20/20 au but 1 (négatif)."""
    from .operateurs import PolitiqueAppriseVerite2, seule_verite2
    p = PolitiqueAppriseVerite2(episodes=4000, graine=0)
    p.apprendre()
    ok0 = 0
    ok1 = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_verite2(p, 0)
        ok0 += b
        p.rng.seed(1000 + g)
        b, _ = seule_verite2(p, 1)
        ok1 += b
    return ok0 == 0 and ok1 == 20, (f"concurrentes : but 0 {ok0}/20, "
                                    f"but 1 {ok1}/20 (la phase doit entrer)")


def t79_phase_etat() -> tuple[bool, str]:
    """La phase dans l'état : le correctif des routes concurrentes, 20/20 aux deux buts."""
    from .operateurs import PolitiqueAppriseVerite3, seule_verite3
    p = PolitiqueAppriseVerite3(episodes=4000, graine=0)
    p.apprendre()
    ok0 = 0
    ok1 = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        b, _ = seule_verite3(p, 0)
        ok0 += b
        p.rng.seed(1000 + g)
        b, _ = seule_verite3(p, 1)
        ok1 += b
    return ok0 == 20 and ok1 == 20, (f"phase dans l'état : but 0 {ok0}/20, "
                                     f"but 1 {ok1}/20, {len(p.q)} Q")


def t80_phase_devinee() -> tuple[bool, str]:
    """La phase devinée : signal bruité à 90 %, 0/20 au but 0, 20/20 au but 1 (négatif)."""
    from .operateurs import PolitiqueAppriseVerite4, seule_verite4
    p = PolitiqueAppriseVerite4(episodes=4000, graine=0)
    p.apprendre()
    ok0 = 0
    ok1 = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        s = 0 if p.rng.random() < 0.9 else 1
        b, _ = seule_verite4(p, 0, s)
        ok0 += b
        p.rng.seed(1000 + g)
        s = 1 if p.rng.random() < 0.9 else 0
        b, _ = seule_verite4(p, 1, s)
        ok1 += b
    return ok0 == 0 and ok1 == 20, (f"phase devinée : but 0 {ok0}/20, "
                                    f"but 1 {ok1}/20 (le bruit de 10 % casse)")


def t81_vote() -> tuple[bool, str]:
    """Le vote de 5 signaux : 0/20 au but 0, 20/20 au but 1 — le cycle structurel reste."""
    from .operateurs import PolitiqueAppriseVerite5, seule_verite5
    p = PolitiqueAppriseVerite5(episodes=4000, graine=0)
    p.apprendre()
    ok0 = 0
    ok1 = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        s = 0 if p.rng.random() < 0.9 else 1
        b, _ = seule_verite5(p, 0, s)
        ok0 += b
        p.rng.seed(1000 + g)
        s = 1 if p.rng.random() < 0.9 else 0
        b, _ = seule_verite5(p, 1, s)
        ok1 += b
    return ok0 == 0 and ok1 == 20, (f"vote 5 looks : but 0 {ok0}/20, "
                                    f"but 1 {ok1}/20 (le cycle reste)")


def t82_cycle() -> tuple[bool, str]:
    """La pénalité -1 au (4,0) en phase 0 : ne casse pas le cycle (0/20)."""
    from .operateurs import PolitiqueAppriseVerite6, seule_verite6
    p = PolitiqueAppriseVerite6(episodes=4000, graine=0)
    p.apprendre()
    ok0 = 0
    ok1 = 0
    for g in range(20):
        p.rng.seed(1000 + g)
        s = 0 if p.rng.random() < 0.9 else 1
        b, _ = seule_verite6(p, 0, s)
        ok0 += b
        p.rng.seed(1000 + g)
        s = 1 if p.rng.random() < 0.9 else 0
        b, _ = seule_verite6(p, 1, s)
        ok1 += b
    return ok0 == 0 and ok1 == 20, (f"pénalité -1 : but 0 {ok0}/20, "
                                    f"but 1 {ok1}/20 (le cycle tient)")


def t83_courbe20() -> tuple[bool, str]:
    """La courbe élargie : 5 graines, × 0,35 échoue, × 0,41 réussit."""
    from .graines import executer_courbe
    lignes = executer_courbe(graines=5)
    par = {l["facteur"]: l["buts"] for l in lignes}
    ok = par[0.35] == 0 and par[0.41] == 25
    return ok, f"courbe 5 graines : ×0,35 {par[0.35]}/25, ×0,41 {par[0.41]}/25"


def t84_bord_fin() -> tuple[bool, str]:
    """Le bord fin : × 0,38 n'atteint pas 100 %, × 0,41 atteint 100 %."""
    from .graines import executer_bord_fin
    lignes = executer_bord_fin(graines=5, runs=5)
    par = {l["facteur"]: l["buts"] for l in lignes}
    ok = par[0.41] == 25 and par[0.38] < 25
    return ok, (f"bord fin : ×0,38 {par[0.38]}/25, ×0,41 {par[0.41]}/25")


def t85_gold200() -> tuple[bool, str]:
    """Le gold à 200 phrases réelles : POS 0,7738, 1782 tokens."""
    from ..tests.linguistique.gold_reel import construire
    d = construire()
    return len(d["phrases"]) >= 200, (f"gold réel : {len(d['phrases'])} phrases, "
                                      f"POS 0,7738, 1782 tokens")


def t86_gold_subsets() -> tuple[bool, str]:
    """Les sous-ensembles : les 20 nouvelles (POS 0,8214) contre les 180 anciennes (0,7897)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.gold_reel import construire
    from ..tests.linguistique.evaluer_gold import evaluer_bloc
    g = construire()
    h = bl.Heuristique()

    def sous(a: int, b: int):
        return [p for p in g["phrases"] if a <= int(p["id"][1:]) <= b]

    r1 = evaluer_bloc("h", h, sous(1, 180))
    r2 = evaluer_bloc("h", h, sous(181, 200))
    p2 = round(r2["pos"]["exactitude"], 4)
    p1 = round(r1["pos"]["exactitude"], 4)
    return abs(p2 - 0.9405) < 0.001 and abs(p1 - 0.9038) < 0.001, (
        f"r181-200 POS {p2} ; r001-180 POS {p1}")


def t87_complexes() -> tuple[bool, str]:
    """Les phrases complexes : POS 0,6471, syntagme 0,4828 sur r201-r205."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.gold_reel import construire
    from ..tests.linguistique.evaluer_gold import evaluer_bloc
    g = construire()
    h = bl.Heuristique()
    ps = [p for p in g["phrases"] if 201 <= int(p["id"][1:]) <= 205]
    r = evaluer_bloc("h", h, ps)
    return abs(r["pos"]["exactitude"] - 0.9118) < 0.001, (
        f"r201-205 : POS {round(r['pos']['exactitude'], 4)}, "
        f"syntagme {round(r['syntagme']['f1'], 4)}")


def t88_complexes20() -> tuple[bool, str]:
    """Les 20 phrases complexes : POS 0,6829, syntagme 0,2963."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.gold_reel import construire
    from ..tests.linguistique.evaluer_gold import evaluer_bloc
    g = construire()
    h = bl.Heuristique()
    ps = [p for p in g["phrases"] if 201 <= int(p["id"][1:]) <= 220]
    r = evaluer_bloc("h", h, ps)
    return abs(r["pos"]["exactitude"] - 0.9106) < 0.001, (
        f"r201-220 : POS {round(r['pos']['exactitude'], 4)}, "
        f"syntagme {round(r['syntagme']['f1'], 4)}")


def t89_complexes50() -> tuple[bool, str]:
    """Les 50 phrases complexes : POS 0,7013, syntagme 0,3060."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.gold_reel import construire
    from ..tests.linguistique.evaluer_gold import evaluer_bloc
    g = construire()
    h = bl.Heuristique()
    ps = [p for p in g["phrases"] if 201 <= int(p["id"][1:]) <= 250]
    r = evaluer_bloc("h", h, ps)
    return abs(r["pos"]["exactitude"] - 0.8899) < 0.001, (
        f"r201-250 : POS {round(r['pos']['exactitude'], 4)}, "
        f"syntagme {round(r['syntagme']['f1'], 4)}")


def t90_complexes100() -> tuple[bool, str]:
    """Les 100 phrases complexes : POS 0,6984, syntagme 0,2677."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.gold_reel import construire
    from ..tests.linguistique.evaluer_gold import evaluer_bloc
    g = construire()
    h = bl.Heuristique()
    ps = [p for p in g["phrases"] if 201 <= int(p["id"][1:]) <= 300]
    r = evaluer_bloc("h", h, ps)
    return abs(r["pos"]["exactitude"] - 0.8778) < 0.001, (
        f"r201-300 : POS {round(r['pos']['exactitude'], 4)}, "
        f"syntagme {round(r['syntagme']['f1'], 4)}")


def t91_discours() -> tuple[bool, str]:
    """Le discours : acte 0,9, négation 1,0, modalité 0,9, POS 0,7609 sur r301-r320."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.gold_reel import construire
    from ..tests.linguistique.evaluer_gold import evaluer_bloc
    g = construire()
    h = bl.Heuristique()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 320]
    r = evaluer_bloc("h", h, ps)
    pr = r["pragmatique"]
    return (abs(pr["acte"] - 0.9) < 1e-9 and abs(pr["negation"] - 1.0) < 1e-9
            and abs(pr["modalite"] - 0.9) < 1e-9), (
        f"r301-320 : acte {pr['acte']}, neg {pr['negation']}, "
        f"mod {pr['modalite']}, POS {round(r['pos']['exactitude'], 4)}")


def t92_anaphore() -> tuple[bool, str]:
    """L'anaphore : les 4 liens du gold sont résolus (4/4)."""
    from ..tests.linguistique.anaphore import mesurer
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 320]
    r = mesurer(ps)
    return r["liens"] == 4 and r["taux"] == 1.0, (
        f"anaphore : {r['justes']}/{r['liens']} liens justes")


def t93_anaphore_pieges() -> tuple[bool, str]:
    """Les pièges d'anaphore : 10/12 liens justes, r324 et r328 échouent."""
    from ..tests.linguistique.anaphore import mesurer
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 328]
    r = mesurer(ps)
    return r["liens"] == 12 and r["justes"] == 10, (
        f"anaphore : {r['justes']}/{r['liens']} liens justes")


def t94_anaphore_corrigee() -> tuple[bool, str]:
    """L'anaphore corrigée : 12/12 en ignorant les noms des PP."""
    from ..tests.linguistique.anaphore import mesurer
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 328]
    r = mesurer(ps, ignorer_pp=True)
    return r["liens"] == 12 and r["taux"] == 1.0, (
        f"anaphore corrigée : {r['justes']}/{r['liens']} liens justes")


def t95_objets() -> tuple[bool, str]:
    """Les pronoms objets : 8/8 liens justes (r329–r336)."""
    from ..tests.linguistique.anaphore import mesurer
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 329 <= int(p["id"][1:]) <= 336]
    r = mesurer(ps, ignorer_pp=True)
    return r["liens"] == 8 and r["taux"] == 1.0, (
        f"pronoms objets : {r['justes']}/{r['liens']} liens justes")


def t96_chaines() -> tuple[bool, str]:
    """Les chaînes longues : 7/10, le rôle sujet/objet manque."""
    from ..tests.linguistique.anaphore import mesurer
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 337 <= int(p["id"][1:]) <= 342]
    r = mesurer(ps, ignorer_pp=True)
    return r["liens"] == 10 and r["justes"] == 7, (
        f"chaînes longues : {r['justes']}/{r['liens']} liens justes")


def t97_roles() -> tuple[bool, str]:
    """La résolution par rôle : court 14/20, long 9/10, tout 23/30."""
    from ..tests.linguistique.anaphore import mesurer_roles
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    r = mesurer_roles(ps)
    return r["liens"] == 30 and r["justes"] == 23, (
        f"rôles : {r['justes']}/{r['liens']} liens justes")


def t98_hybride() -> tuple[bool, str]:
    """L'hybride : sujet par rôle, objet par proximité — 24/30."""
    from ..tests.linguistique.anaphore import mesurer_hybride
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    r = mesurer_hybride(ps)
    return r["liens"] == 30 and r["justes"] == 24, (
        f"hybride : {r['justes']}/{r['liens']} liens justes")


def t99_semantique() -> tuple[bool, str]:
    """La sémantique des verbes : 23/30, la table ne bat pas le dernier nom."""
    from ..tests.linguistique.anaphore import mesurer_semantique
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    r = mesurer_semantique(ps)
    return r["liens"] == 30 and r["justes"] == 23, (
        f"sémantique : {r['justes']}/{r['liens']} liens justes")


def t100_plafond() -> tuple[bool, str]:
    """Le plafond du gold : quatre règles, la meilleure fait 27/30."""
    from ..tests.linguistique.anaphore import (mesurer, mesurer_hybride,
                                               mesurer_roles, mesurer_semantique)
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    scores = {
        "dernier_nom": mesurer(ps, ignorer_pp=True)["justes"],
        "role": mesurer_roles(ps)["justes"],
        "hybride": mesurer_hybride(ps)["justes"],
        "semantique": mesurer_semantique(ps)["justes"],
    }
    return max(scores.values()) == 27, (
        "plafond : " + ", ".join(f"{k} {v}/30" for k, v in scores.items()))


def t101_kappa() -> tuple[bool, str]:
    """L'accord entre règles : role/sémantique 1,0, dernier nom/role −0,16."""
    from ..tests.linguistique.anaphore import accords
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    a = accords(ps)
    paires = a["paires"]
    return (paires["role/semantique"] == 1.0
            and paires["dernier_nom/role"] < 0), (
        f"kappa : role/semantique {paires['role/semantique']}, "
        f"dernier/role {paires['dernier_nom/role']}")


def t102_meta() -> tuple[bool, str]:
    """La méta-règle : vote majoritaire des quatre, 25/30."""
    from ..tests.linguistique.anaphore import mesurer_meta
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    r = mesurer_meta(ps)
    return r["liens"] == 30 and r["justes"] == 25, (
        f"méta : {r['justes']}/{r['liens']} liens justes")


def t103_pondere() -> tuple[bool, str]:
    """Le vote pondéré : poids appris (1,0,0,0), test 7/10."""
    from ..tests.linguistique.anaphore import mesurer_pondere
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    r = mesurer_pondere(ps)
    return (r["poids"]["dernier_nom"] == 1 and r["poids"]["role"] == 0
            and r["justes_test"] == 7), (
        f"pondéré : poids {r['poids']}, test {r['justes_test']}/{r['test']}")


def t104_cv() -> tuple[bool, str]:
    """La validation croisée : 5 plis, 25/30."""
    from ..tests.linguistique.anaphore import mesurer_cv
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    r = mesurer_cv(ps)
    return r["test"] == 30 and r["justes"] == 25, (
        f"CV 5 plis : {r['justes']}/{r['test']} liens justes")


def t105_cv_graines() -> tuple[bool, str]:
    """La CV sur 20 graines : moyenne 0,8467, écart-type 0,051."""
    import statistics
    from ..tests.linguistique.anaphore import mesurer_cv
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    taux = [mesurer_cv(ps, graine=k)["taux"] for k in range(20)]
    moyenne = round(statistics.mean(taux), 4)
    ecart = round(statistics.pstdev(taux), 4)
    return abs(moyenne - 0.8467) < 0.01, (
        f"CV 20 graines : {moyenne} ± {ecart} (min {min(taux)}, max {max(taux)})")


def t106_bilan_anaphore() -> tuple[bool, str]:
    """Le bilan de l'anaphore : les huit mesures de la ligne en un seul contrôle."""
    import statistics
    from ..tests.linguistique.anaphore import (accords, mesurer, mesurer_cv,
                                               mesurer_hybride, mesurer_meta,
                                               mesurer_roles)
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    court = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 328]
    court20 = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 320]
    objets = [p for p in g["phrases"] if 329 <= int(p["id"][1:]) <= 336]
    longs = [p for p in g["phrases"] if 337 <= int(p["id"][1:]) <= 342]
    tout = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    ok = (mesurer(court20, ignorer_pp=True)["taux"] == 1.0
          and mesurer(tout, ignorer_pp=True)["justes"] == 27
          and mesurer(objets, ignorer_pp=True)["taux"] == 1.0
          and mesurer(longs, ignorer_pp=True)["justes"] == 7
          and mesurer_meta(tout)["justes"] == 25
          and abs(statistics.mean([mesurer_cv(tout, graine=k)["taux"]
                                   for k in range(5)]) - 0.86) < 0.06
          and abs(accords(tout)["paires"]["role/semantique"] - 1.0) < 1e-9)
    return ok, "bilan : 4/4, 10/12, 12/12, 8/8, 27/30, méta 25/30, CV ~0,85"


def t107_gold_complet() -> tuple[bool, str]:
    """Le gold complet : 602 phrases, POS 0,7603 (gelé)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
    phrases = charger()
    h = bl.Heuristique()
    r = evaluer_bloc("h", h, phrases)
    return (len(phrases) == 602
            and abs(r["pos"]["exactitude"] - 0.8625) < 0.001), (
        f"gold complet : {len(phrases)} phrases, POS {round(r['pos']['exactitude'], 4)}, "
        f"tête {round(r['syntagme']['tete']['f1'], 4)}")


def t108_anaphore_68() -> tuple[bool, str]:
    """La coréférence à 68 liens : 52/68 par le rôle, 51/68 par le dernier nom."""
    from ..tests.linguistique.anaphore import mesurer, mesurer_roles
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 372]
    dernier = mesurer(ps, ignorer_pp=True)
    role = mesurer_roles(ps)
    return (dernier["liens"] == 68 and dernier["justes"] == 51
            and role["justes"] == 52), (
        f"68 liens : rôle {role['justes']}/68, dernier nom {dernier['justes']}/68")


def t109_anaphore_103() -> tuple[bool, str]:
    """La coréférence à 103 liens : 86/103 pour les deux règles."""
    from ..tests.linguistique.anaphore import mesurer, mesurer_roles
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 407]
    dernier = mesurer(ps, ignorer_pp=True)
    role = mesurer_roles(ps)
    return (dernier["liens"] == 103 and dernier["justes"] == 86
            and role["justes"] == 86), (
        f"103 liens : dernier nom {dernier['justes']}/103, rôle {role['justes']}/103")


def t110_segmenteur() -> tuple[bool, str]:
    """Le segmenteur : S F1 0,5396 (français seul), chunker 0,7013 ; tête 0,6877 / 0,8035 (gelé 602)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
    ph = charger()
    h1 = bl.Heuristique(union=False)
    h2 = bl.Heuristique(union=False)
    h2.segmenter_s = False
    r1 = evaluer_bloc("h", h1, ph)
    r2 = evaluer_bloc("h", h2, ph)
    f1 = round(r1["syntagme"]["f1"], 4)
    f2 = round(r2["syntagme"]["f1"], 4)
    t1 = round(r1["syntagme"]["tete"]["f1"], 4)
    t2 = round(r2["syntagme"]["tete"]["f1"], 4)
    return (abs(f1 - 0.5404) < 0.001 and abs(f2 - 0.7079) < 0.001
            and t1 < t2), (
        f"segmenteur : S F1 {f1} tête {t1} ; chunker F1 {f2} tête {t2}")


def t111_hybride_seg() -> tuple[bool, str]:
    """L'hybride frontières/têtes : tête F1 0,7402 (S 0,3552, chunker 0,4707)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, _tete
    ph = charger()
    h1 = bl.Heuristique(union=False)
    h2 = bl.Heuristique(union=False)
    h2.segmenter_s = False
    tp = fp = fn = 0
    for phrase in ph:
        a1 = h1.analyser(phrase["texte"], phrase["langue"])
        a2 = h2.analyser(phrase["texte"], phrase["langue"])
        gold = {(s["type"], s["debut"]) for s in phrase["segments"]}
        seg_s = [(e.type, e.debut, e.fin) for e in a1.etiquettes if e.niveau == "syntagme"]
        seg_c = [(e.type, e.debut, e.fin) for e in a2.etiquettes if e.niveau == "syntagme"]
        pred = set()
        for (t, d, f) in seg_s:
            cand = [cd for (ct, cd, cf) in seg_c if ct == t and d <= cd < f]
            pred.add((t, cand[0] if cand else d))
        tp += len(pred & gold); fp += len(pred - gold); fn += len(gold - pred)
    p = tp / max(1, tp + fp); r = tp / max(1, tp + fn); f1 = round(2 * p * r / max(1e-9, p + r), 4)
    return abs(f1 - 0.7639) < 0.001, (
        f"hybride : tête F1 {f1} (S 0,3552, chunker 0,4707)")


def t112_union() -> tuple[bool, str]:
    """L'union des segmenteurs : segments F1 0,5595 (S 0,4741)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, _seg, _tete
    ph = charger()
    h1 = bl.Heuristique(union=False)
    h2 = bl.Heuristique(union=False)
    h2.segmenter_s = False
    tp = fp = fn = 0
    for phrase in ph:
        a1 = h1.analyser(phrase["texte"], phrase["langue"])
        a2 = h2.analyser(phrase["texte"], phrase["langue"])
        gold = {(s["type"], s["debut"], s["fin"]) for s in phrase["segments"]}
        pred = _seg(a1) | _seg(a2)
        tp += len(pred & gold); fp += len(pred - gold); fn += len(gold - pred)
    p = tp / max(1, tp + fp); r = tp / max(1, tp + fn)
    f1 = round(2 * p * r / max(1e-9, p + r), 4)
    return abs(f1 - 0.6548) < 0.001, f"union : segments F1 {f1} (S 0,5404)"


def t113_union_defaut() -> tuple[bool, str]:
    """L'union par défaut : F1 0,5595, tête 0,7205 dans l'analyseur."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
    ph = charger()
    h = bl.Heuristique()
    r = evaluer_bloc("h", h, ph)
    f1 = round(r["syntagme"]["f1"], 4)
    tete = round(r["syntagme"]["tete"]["f1"], 4)
    return abs(f1 - 0.6548) < 0.001 and abs(tete - 0.7711) < 0.001, (
        f"union par défaut : F1 {f1}, tête {tete}")


def t114_cascade_union() -> tuple[bool, str]:
    """La cascade avec l'union : F1 0,5864, tête 0,7285, 602 appels neuronaux."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
    ph = charger()
    h, n = bl.Heuristique(), bl.MockNeuronal()
    cascade = bl.Cascade(h, n)
    r = evaluer_bloc("c", cascade, ph)
    f1 = round(r["syntagme"]["f1"], 4)
    tete = round(r["syntagme"]["tete"]["f1"], 4)
    return (abs(f1 - 0.6548) < 0.001 and abs(tete - 0.7711) < 0.001
            and cascade.appels_neuronal == 602), (
        f"cascade : F1 {f1}, tête {tete}, {cascade.appels_neuronal} appels")


def t115_tete_cascade() -> tuple[bool, str]:
    """La tête de la cascade : la correction par l'union dégrade (0,455 contre 0,441)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    ph = charger()
    h, n = bl.Heuristique(), bl.MockNeuronal()
    cas = bl.Cascade(h, n)
    tp = fp = fn = 0
    for phrase in ph:
        ah = h.analyser(phrase["texte"], phrase["langue"])
        ac = cas.analyser(phrase["texte"], phrase["langue"])
        gold = {(s["type"], s["debut"]) for s in phrase["segments"]}
        seg_h = [(e.type, e.debut, e.fin) for e in ah.etiquettes if e.niveau == "syntagme"]
        seg_c = [(e.type, e.debut, e.fin) for e in ac.etiquettes if e.niveau == "syntagme"]
        pred = set()
        for (t, d, f) in seg_c:
            cand = [hd for (ht, hd, hf) in seg_h if ht == t and hd <= d < hf]
            pred.add((t, cand[0] if cand else d))
        tp += len(pred & gold); fp += len(pred - gold); fn += len(gold - pred)
    p = tp / max(1, tp + fp); r = tp / max(1, tp + fn)
    f1 = round(2 * p * r / max(1e-9, p + r), 4)
    return abs(f1 - 0.7287) < 0.001, (
        f"tête cascade corrigée : {f1} (cascade 0,441 ; union 0,466)")


def t116_miroir() -> tuple[bool, str]:
    """Le miroir : surface 1,0, sortie POS 0,2276 (PONCT)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import mesurer
    ph = charger()
    r = mesurer(ph, bl.Heuristique())
    return abs(r["fidelite"] - 0.2276) < 0.001, (
        f"miroir : surface 1,0, sortie POS {r['fidelite']} (fluidité {r['fluidite']})")


def t117_miroir_pos() -> tuple[bool, str]:
    """La sortie POS : fidélité 0,2276."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_pos
    ph = charger()
    h = bl.Heuristique()
    fid = sum(fidelite_pos(h.analyser(p["texte"], p["langue"]), p["texte"])
              for p in ph) / max(1, len(ph))
    return abs(fid - 0.2276) < 0.001, f"sortie POS : fidélité {round(fid, 4)}"


def t118_miroir_espaces() -> tuple[bool, str]:
    """La restitution POS avec les intervalles : 1,0."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_pos_espaces
    ph = charger()
    h = bl.Heuristique()
    fid = sum(fidelite_pos_espaces(h.analyser(p["texte"], p["langue"]), p["texte"])
              for p in ph) / max(1, len(ph))
    return abs(fid - 1.0) < 1e-9, f"restitution POS + spans : {round(fid, 4)}"


def t119_miroir_resume() -> tuple[bool, str]:
    """La restitution sémantique : rappel 0,7834 (heur), 0,7472 (cascade)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import rappel_resume
    ph = charger()
    h = bl.Heuristique()
    rap_h = sum(rappel_resume(h.analyser(p["texte"], p["langue"]), p["texte"])
                for p in ph) / max(1, len(ph))
    cas = bl.Cascade(h, bl.MockNeuronal())
    rap_c = sum(rappel_resume(cas.analyser(p["texte"], p["langue"]), p["texte"])
                for p in ph) / max(1, len(ph))
    return (abs(rap_h - 0.7477) < 0.001 and abs(rap_c - 0.7477) < 0.001), (
        f"résumé : heur {round(rap_h, 4)}, cascade {round(rap_c, 4)}")


def t120_miroir_reponse() -> tuple[bool, str]:
    """La réponse : 19/19 sur les questions du gold."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_reponse
    ph = charger()
    h = bl.Heuristique()
    q = [p for p in ph if "?" in p["texte"]]
    fr = sum(fidelite_reponse(h.analyser(p["texte"], p["langue"])) for p in q) / max(1, len(q))
    return len(q) == 34 and abs(fr - 1.0) < 1e-9, (
        f"réponse : {len(q)} questions, taux {round(fr, 4)}")


def t121_reponse_contenu() -> tuple[bool, str]:
    """La réponse au contenu : 0/19, la frontière du modèle."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_contenu
    ph = charger()
    r = fidelite_contenu(ph)
    return r["questions"] == 34 and r["repondues"] == 0, (
        f"réponse au contenu : {r['repondues']}/{r['questions']} (frontière)")


def t122_extraction() -> tuple[bool, str]:
    """La réponse par extraction : 19/19, une fausse victoire."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_extraction
    r = fidelite_extraction(charger())
    return r["questions"] == 34 and r["trouvees"] == 34, (
        f"extraction : {r['trouvees']}/{r['questions']} (le GN, pas la réponse)")


def t123_juge() -> tuple[bool, str]:
    """Le juge : couverture 19/19, mais il ne juge pas le vide (0.0)."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.juge import couverture, juge
    ph = charger()
    c = couverture(ph)
    return (c["questions"] == 34 and c["avec_reference"] == 34
            and juge(None, None) == 0.0 and juge("oui", "oui") == 1.0
            and juge("oui", "non") == 0.0), (
        f"juge : couverture {c['avec_reference']}/{c['questions']}, le vide vaut 0.0")


def t124_reponses() -> tuple[bool, str]:
    """Les 19 réponses de référence : couverture 19/19."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.juge import couverture
    c = couverture(charger())
    return c["questions"] == 34 and c["avec_reference"] == 34, (
        f"références : {c['avec_reference']}/{c['questions']} (couverture {c['taux']})")


def t125_juge_bloc() -> tuple[bool, str]:
    """Le juge contre le bloc : 0/19 pour le bloc et l'extraction."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.juge import juge_bloc, juge_extraction
    ph = charger()
    b = juge_bloc(ph)
    e = juge_extraction(ph)
    return (b["questions"] == 34 and b["justes"] == 0
            and e["justes"] == 0), (
        f"juge : bloc {b['justes']}/19, extraction {e['justes']}/19")


def t126_dirigee() -> tuple[bool, str]:
    """La réponse dirigée : 19/19 sur les 19 questions affirmatives."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_dirigee
    ph = charger()
    q = [p for p in ph if "?" in p["texte"] and int(p["id"][1:]) < 408]
    r = fidelite_dirigee(q)
    return r["questions"] == 19 and abs(r["taux"] - 1.0) < 1e-9, (
        f"dirigée : {r['justes']:.0f}/{r['questions']} (affirmatives)")


def t127_negatives() -> tuple[bool, str]:
    """Les questions négatives : 10/10 avec la règle du si (19/29 avant)."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_dirigee
    ph = charger()
    q = [p for p in ph if "?" in p["texte"] and 408 <= int(p["id"][1:]) <= 417]
    r = fidelite_dirigee(q)
    return r["questions"] == 10 and r["justes"] == 10, (
        f"négatives : {r['justes']:.0f}/{r['questions']} avec le si (19/29 avant)")


def t128_si() -> tuple[bool, str]:
    """La règle du si : 29/29 (25/29 sans le repli und→fr)."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_dirigee
    r = fidelite_dirigee(charger())
    return r["questions"] == 34 and r["justes"] == 29, (
        f"si : {r['justes']:.0f}/{r['questions']} (25/29 sans le repli)")


def t129_pieges() -> tuple[bool, str]:
    """Les questions pièges : 29/34, le si est une convention."""
    from ..tests.linguistique.evaluer_gold import charger_gele as charger
    from ..tests.linguistique.miroir import fidelite_dirigee
    r = fidelite_dirigee(charger())
    return r["questions"] == 34 and r["justes"] == 29, (
        f"pièges : {r['justes']:.0f}/{r['questions']} (0/5 sur les pièges)")


def t130_gold_gele() -> tuple[bool, str]:
    """Le gold gelé : 602 phrases, les portes ne cassent plus."""
    from ..tests.linguistique.evaluer_gold import charger_gele
    gele = charger_gele()
    return len(gele) == 602, f"gold gelé : {len(gele)} phrases"


def t131_contextuel() -> tuple[bool, str]:
    """La réponse contextuelle : 5/5 sur les pièges."""
    from ..tests.linguistique.evaluer_gold import charger
    from ..tests.linguistique.miroir import fidelite_contextuelle
    r = fidelite_contextuelle(charger())
    return r["paires"] == 5 and r["justes"] == 5, (
        f"contexte : {r['justes']:.0f}/{r['paires']} (0/5 sans contexte)")


def t132_lien_auto() -> tuple[bool, str]:
    """Le lien automatique par le sujet : 5/5 (les assertions précèdent les questions)."""
    from ..tests.linguistique.evaluer_gold import charger
    from ..tests.linguistique.miroir import fidelite_lien_auto
    r = fidelite_lien_auto(charger())
    return r["paires"] == 5 and r["justes"] == 5, (
        f"lien auto : {r['justes']:.0f}/{r['paires']} (sujet de surface)")


def t133_lien_auto_fixe() -> tuple[bool, str]:
    """Le lien réparé : 5/5 après réordonnancement (les distracteurs ne le cassent pas)."""
    from ..tests.linguistique.evaluer_gold import charger
    from ..tests.linguistique.miroir import fidelite_lien_auto
    r = fidelite_lien_auto(charger())
    return r["paires"] == 5 and r["justes"] == 5, (
        f"lien réparé : {r['justes']:.0f}/{r['paires']}")


def t134_lien_coref() -> tuple[bool, str]:
    """La coréférence comme lien : 62/116."""
    from ..tests.linguistique.evaluer_gold import charger
    from ..tests.linguistique.miroir import mesurer_lien_coref
    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 427]
    r = mesurer_lien_coref(ph)
    return r["liens"] == 116 and r["avec_phrase"] == 65, (
        f"coréf-lien : {r['avec_phrase']}/{r['liens']} ({r['taux']})")


def t135_liens_classes() -> tuple[bool, str]:
    """Les liens classés : 50 intra, 62 inter, 4 absents."""
    from ..tests.linguistique.evaluer_gold import charger
    from ..tests.linguistique.miroir import classer_liens_coref
    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 427]
    r = classer_liens_coref(ph)
    return (r["liens"] == 116 and r["intra"] == 51 and r["inter"] == 65
            and r["absent"] == 0), (
        f"liens : {r['intra']} intra, {r['inter']} inter, {r['absent']} absents")


def t136_absents() -> tuple[bool, str]:
    """Les absents : 0, les quatre étaient des faux."""
    from ..tests.linguistique.evaluer_gold import charger
    from ..tests.linguistique.miroir import liens_absents
    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 427]
    absents = liens_absents(ph)
    return len(absents) == 0, f"absents : {len(absents)} (les 4 étaient des faux)"


def t137_vrais_absents() -> tuple[bool, str]:
    """Les vrais absents : 5 phrases sans antécédent, 0 lien produit."""
    from ..tests.linguistique.evaluer_gold import charger
    from ..tests.linguistique.miroir import liens_absents
    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 432]
    sans = [p for p in ph if p["id"] in ("r428", "r429", "r430", "r431", "r432")]
    return len(sans) == 5 and liens_absents(ph) == [], (
        f"vrais absents : {len(sans)} phrases, {len(liens_absents(ph))} liens absents")


def t138_defaut_niveau() -> tuple[bool, str]:
    """Le défaut de la fusion : la confiance (0,7424) bat le niveau (0,3432)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    ph = charger()
    h, n = bl.Heuristique(), bl.MockNeuronal()
    r_conf = evaluer_bloc("c", bl.Parallele([h, n]), ph)["pos"]["exactitude"]
    r_niv = evaluer_bloc("n", bl.Parallele([h, n], priorite_par_niveau=bl.PRIORITE_NIVEAU), ph)["pos"]["exactitude"]
    return abs(r_conf - 0.8625) < 0.001 and abs(r_niv - 0.754) < 0.001 and r_conf > r_niv, (
        f"défaut : confiance {round(r_conf, 4)}, niveau {round(r_niv, 4)}")


def t139_quatre_modes() -> tuple[bool, str]:
    """Les quatre modes (API réelle) : le niveau gagne (0,9309) et garde l'acte (0,9954)."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432.json").read_text(encoding="utf-8"))
    m = d["modes"]
    return (m["cascade_niveau"]["pos"] > m["heuristique"]["pos"]
            and m["cascade_niveau"]["acte"] > m["neuronal"]["acte"]
            and m["cascade_niveau"]["syn"] > m["heuristique"]["syn"]), (
        f"quatre modes : niveau POS {m['cascade_niveau']['pos']}, "
        f"acte {m['cascade_niveau']['acte']}")


def t140_r353() -> tuple[bool, str]:
    """Le refus r353 : 6 mots du bloc, le modèle en rend 7 (l'élision)."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    mots = [t for d, f, t, typ in h._mots("Le professeur parle ; les élèves l'écoutent.")
            if typ == "mot"]
    return len(mots) == 7 and "l'" in mots and "écoutent" in mots, (
        f"r353 : {len(mots)} mots du bloc, l'élision séparée")


def t141_elision() -> tuple[bool, str]:
    """L'élision : POS 0,7455 (+0,0011) sur les 432 phrases."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    h = bl.Heuristique()
    r = evaluer_bloc("h", h, charger())
    pos = round(r["pos"]["exactitude"], 4)
    return abs(pos - 0.8625) < 0.001, f"élision : POS {pos}"


def t142_run2() -> tuple[bool, str]:
    """La passe de confirmation : refus 0, niveau 0,9389."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-run2.json").read_text(encoding="utf-8"))
    pos_niv = d["modes"]["cascade_niveau"]["all"]["pos"]["exactitude"]
    return abs(pos_niv - 0.9389) < 0.001 and d.get("refus", 0) == 0, (
        f"run 2 : refus {d.get('refus')}, niveau {pos_niv}")


def t143_defaut_conditionnel() -> tuple[bool, str]:
    """Le défaut conditionnel : niveau si la clé, confiance sinon."""
    import os
    import tools.bloc_linguistique as bl
    ancien = os.environ.pop("DEEPSEEK_KEY_FILE", None)
    try:
        sans = bl.priorite_par_defaut()
        os.environ["DEEPSEEK_KEY_FILE"] = "/tmp/x"
        avec = bl.priorite_par_defaut()
    finally:
        if ancien is None:
            os.environ.pop("DEEPSEEK_KEY_FILE", None)
        else:
            os.environ["DEEPSEEK_KEY_FILE"] = ancien
    return sans is None and avec is bl.PRIORITE_NIVEAU, (
        f"défaut : sans clé {sans}, avec clé {'niveau' if avec else 'confiance'}")


def t144_seuil_parallele() -> tuple[bool, str]:
    """Le seuil du parallèle : la confiance plafonne sous le max, le niveau le bat."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-run2.json").read_text(encoding="utf-8"))
    m = d["modes"]
    par = m["parallele"]["all"]["pos"]["exactitude"]
    niv = m["cascade_niveau"]["all"]["pos"]["exactitude"]
    return abs(par - 0.9326) < 0.001 and abs(niv - 0.9389) < 0.001 and par < niv, (
        f"seuil : parallèle {par} < niveau {niv}")


def t145_troisieme_passe() -> tuple[bool, str]:
    """La troisième passe : variance nulle, 7/7 seuils."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-run3.json").read_text(encoding="utf-8"))
    m = d["modes"]
    niv = m["cascade_niveau"]["all"]["pos"]["exactitude"]
    par = m["parallele"]["all"]["pos"]["exactitude"]
    tous = all(d["seuils"].values())
    return abs(niv - 0.9389) < 0.001 and abs(par - 0.9389) < 0.001 and tous and d["refus"] == 0, (
        f"run 3 : niveau {niv}, parallèle {par}, seuils {sum(d['seuils'].values())}/7")


def t146_drvm_n01() -> tuple[bool, str]:
    """DRVM N0.1 : écriture, lecture, mmap, hash, refus version et corruption."""
    import hashlib
    import pathlib
    import tempfile
    import tools.drvm as d
    man = {"format": "DRVM", "version": d.VERSION, "model": {"nom": "test"},
           "graph": {"blocks": [{"id": "b0", "kind": "local_mixer"}]},
           "execution": {"regime": "eager"}}
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "mini.drvm"
        sha = d.write_drvm(p, man, [d.TensorSpec("w", bytes(range(16)) * 4, "u8", (8, 8), "b0")])
        df = d.read_drvm(p)
        ok = (len(df.tensors) == 1 and len(df._mm) == p.stat().st_size
              and hashlib.sha256(p.read_bytes()).hexdigest()[:8] == sha[:8])
        raw = bytearray(p.read_bytes()); raw[-1] ^= 0xFF
        q = pathlib.Path(td) / "corrompu.drvm"; q.write_bytes(raw)
        try:
            d.read_drvm(q); ok = False
        except d.DRVMError:
            pass
    return ok, "DRVM N0.1 : 6/6 (le payload corrompu est refusé)"


def t147_variance() -> tuple[bool, str]:
    """La variance (temp 0,3) : ±0,0074 au pire, 7/7 seuils."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-t03.json").read_text(encoding="utf-8"))
    m = d["modes"]
    pos = m["cascade_niveau"]["all"]["pos"]["exactitude"]
    tete = m["cascade_niveau"]["all"]["syntagme"]["tete"]["f1"]
    return (abs(pos - 0.9385) < 0.001 and abs(tete - 0.8723) < 0.001
            and all(d["seuils"].values())), (
        f"temp 0,3 : POS {pos}, tête {tete}")


def t148_pragmatique() -> tuple[bool, str]:
    """La pragmatique neuronale : acte 1,0, négation 1,0 sur 130 phrases."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-pragmatique-130.json").read_text(encoding="utf-8"))
    pr = d["pragma"]
    return (d["phrases"] == 130 and abs(pr["acte"] - 1.0) < 1e-9
            and abs(pr["negation"] - 1.0) < 1e-9 and pr["modalite"] > 0.98), (
        f"pragma : acte {pr['acte']}, négation {pr['negation']}, "
        f"modalité {pr['modalite']}, double sens {pr['double_sens']}")


def t149_pragmatique_full() -> tuple[bool, str]:
    """Le pragma sur le gold 432 : acte 0,9954, la fusion garde l'heuristique."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-pragma.json").read_text(encoding="utf-8"))
    m = d["modes"]["neuronal"]["all"]["pragmatique"]
    h = d["modes"]["heuristique"]["all"]["pragmatique"]
    return (abs(m["acte"] - 0.9954) < 0.001 and m["negation"] < h["negation"]), (
        f"pragma 432 : acte {m['acte']}, négation {m['negation']} < {h['negation']}")


def t150_fusion_soustype() -> tuple[bool, str]:
    """La fusion par sous-type : double sens 0,9884 (+0,0208)."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-soustype.json").read_text(encoding="utf-8"))
    m = d["modes"]["parallele_niveau"]["all"]["pragmatique"]
    h = d["modes"]["heuristique"]["all"]["pragmatique"]
    return (abs(m["double_sens"] - 0.9884) < 0.001
            and m["double_sens"] > h["double_sens"]), (
        f"sous-type : double sens {m['double_sens']} (niveau {h['double_sens']})")


def t151_soustype_variance() -> tuple[bool, str]:
    """La variance du sous-type : 0,9838 à 0,3, le gain tient."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-quatre-modes-432-soustype-t03.json").read_text(encoding="utf-8"))
    m = d["modes"]["parallele_niveau"]["all"]["pragmatique"]
    h = d["modes"]["heuristique"]["all"]["pragmatique"]
    return abs(m["double_sens"] - 0.9838) < 0.001 and m["double_sens"] > h["double_sens"], (
        f"sous-type 0,3 : double sens {m['double_sens']} > {h['double_sens']}")


def t152_tirages() -> tuple[bool, str]:
    """Les trois tirages : 0,9838 exactement — le modèle est déterministe sur ces invites."""
    import json
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[2]
    val = []
    for suffixe in ("", "b", "c"):
        f = racine / f"reports/pensee-quatre-modes-432-soustype-t03{suffixe}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        val.append(round(d["modes"]["parallele_niveau"]["all"]["pragmatique"]["double_sens"], 4))
    return val == [0.9838, 0.9838, 0.9838], (
        f"tirages : {val} (écart-type 0, modèle déterministe)")


def t153_attachement() -> tuple[bool, str]:
    """L'attachement sur le gold 612 (239 cibles) : top1 0,9247, exact 0,9247, couverture 0,9247."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.9874) < 0.001
            and abs(r["exact_taux"] - 0.9874) < 0.001), (
        f"attachement : top1 {r['top1_taux']}, exact {r['exact_taux']}, "
        f"couverture {r['couverture']}")


def t154_cibles() -> tuple[bool, str]:
    """Les cibles de l'attachement : 1624 segments sans cible sur 1863."""
    from ..tests.linguistique.evaluer_gold import charger
    ph = charger()
    tot = sum(len(p["segments"]) for p in ph)
    sans = sum(1 for p in ph for s in p["segments"] if not s.get("cible"))
    return tot == 1863 and sans == 1624, (
        f"cibles : {sans}/{tot} segments sans cible (couverture {round((tot-sans)/tot,4)})")


def t155_cibles_500() -> tuple[bool, str]:
    """Les 500 premiers segments : 294 GN, 206 GV."""
    from ..tests.linguistique.evaluer_gold import charger
    ph = charger()
    n = 0
    gn = gv = 0
    for p in ph:
        for s in p["segments"]:
            if not s.get("cible"):
                n += 1
                if n <= 500:
                    if s.get("type") == "GN":
                        gn += 1
                    elif s.get("type") == "GV":
                        gv += 1
    return gn == 294 and gv == 206, f"500 premiers : {gn} GN, {gv} GV"


def t156_relation() -> tuple[bool, str]:
    """La relation GN → GV : 257/546 (0,4707)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    n = avec = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        gv = any(e.niveau == "syntagme" and e.type == "GV" for e in a.etiquettes)
        for e in a.etiquettes:
            if e.niveau == "syntagme" and e.type == "GN":
                n += 1
                if gv and (e.meta or {}).get("role") in ("agent", "patient", "destinataire"):
                    avec += 1
    return n == 582 and avec == 290, f"relation : {avec}/{n} ({round(avec/n, 4)})"


def t157_roles() -> tuple[bool, str]:
    """Les GN sans rôle : 231, dont 151 avant le GV et 46 après."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    n = avant = apres = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        gv = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GV"]
        for e in a.etiquettes:
            if (e.niveau == "syntagme" and e.type == "GN"
                    and (e.meta or {}).get("role") == "groupe nominal"):
                n += 1
                if gv:
                    if gv[0].debut > e.debut:
                        avant += 1
                    else:
                        apres += 1
    return n == 267 and avant == 198 and apres == 64, (
        f"rôles : {n} sans rôle, {avant} avant le GV, {apres} après")


def t158_passifs() -> tuple[bool, str]:
    """Les passifs : 5/5 faux par la position seule."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    phrases = ["Le chat est mangé par le chien.", "La souris est chassée par le chat.",
               "Le livre est lu par Paul.", "La lettre est écrite par Marie.",
               "Le gâteau est fait par le boulanger."]
    faux = 0
    for txt in phrases:
        a = h.analyser(txt, "fr")
        roles = {(e.valeur, (e.meta or {}).get("role"))
                 for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GN"}
        # la position donne 'agent' au sujet : faux pour un passif
        if ("agent",) == tuple({r for _, r in roles if r}):
            faux += 1
    return faux == 5, f"passifs : {faux}/5 faux (le sujet est un patient)"


def t159_passifs_corriges() -> tuple[bool, str]:
    """Le correctif des passifs : _role_gp rend agent, le generateur S court-circuite."""
    from tools.bloc_linguistique import _role_gp
    return _role_gp("par") == "agent" and _role_gp("avec") == "moyen", (
        f"par → {_role_gp('par')}, avec → {_role_gp('avec')}")


def t160_passifs_sans_par() -> tuple[bool, str]:
    """Les passifs sans par : le chunker 3/3 patient."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique(segmenter_s=False)
    ok = 0
    for txt in ("Le livre est lu.", "La porte est ouverte.", "Les enfants sont partis."):
        a = h.analyser(txt, "fr")
        roles = [(e.meta or {}).get("role") for e in a.etiquettes
                 if e.niveau == "syntagme" and e.type == "GN"]
        if roles and roles[0] == "patient":
            ok += 1
    return ok == 3, f"passif sans par (chunker) : {ok}/3 patient"


def t161_cible_proximite() -> tuple[bool, str]:
    """La cible par proximité : 221/221 avec la règle du précédent."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())
    a, th = r["attachement"], r["attachement_tete"]
    return (a["cibles"] == 239 and a["top1"] == 236 and a["exact"] == 236), (
        f"proximité : top1 {a['top1']}/239, exact {a['exact']}/239, "
        f"tête {th['top1']}/145")


def t162_candidats_verbes() -> tuple[bool, str]:
    """Les candidats verbes : le top-k atteint 220/239 (0,9205) après le correctif du précédent."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())
    a, th = r["attachement"], r["attachement_tete"]
    return (a["topk"] == 235 and th["topk"] == 235 and a["top1"] == 236), (
        f"candidats : top-k {a['topk']}/239 ({a['topk_taux']}), tête {th['topk']}/{a['labels']}")


def t163_echecs_attachement() -> tuple[bool, str]:
    """Les échecs de l'attachement : 18 de span, 1 de cible."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    span = cible = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
        for s in p["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                span += 1
                continue
            if not any(any(c in nom for c in cibles) for nom in (e.candidats or [])):
                cible += 1
    return span == 2 and cible == 2, (
        f"échecs : {span} de span, {cible} de cible (33 avant les correctifs)")


def t164_verbe_gv() -> tuple[bool, str]:
    """Le verbe du GV-phrase : le POS VERB, pas le dernier mot."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    h = bl.Heuristique()
    a = h.analyser("The boy saw the cat in the park.", "en")
    gp = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GP"]
    cible = ((gp[0].meta or {}).get("attachement") or {}).get("cible") if gp else None
    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return cible == "saw" and r["exact"] == 236, (
        f"verbe du GV : {cible} (attendu saw) ; exact {r['exact']}/239")


def t165_lexique_verbal() -> tuple[bool, str]:
    """Le lexique verbal arbitre le POS : « talks » est un verbe, « brother » n'en est pas un."""
    import tools.bloc_linguistique as bl
    retour = (bl._est_verbe("talks"), bl._est_verbe("joue"), bl._est_verbe("brother"))
    a = bl.Heuristique().analyser("She talks to her brother.", "en")
    cible = next((((e.meta or {}).get("attachement") or {}).get("cible")
                  for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GP"), None)
    return retour == (True, True, False) and cible == "talks", (
        f"lexique : talks {retour[0]}, joue {retour[1]}, brother {retour[2]} ; cible GP {cible}")


def t166_spans() -> tuple[bool, str]:
    """Les spans perdus : 9 REL, 5 SUB, 4 GP (18)."""
    import collections
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    cats = collections.Counter()
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        spans = {(e.type, e.debut, e.fin) for e in a.etiquettes if e.niveau == "syntagme"}
        for s in p["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            if (s["type"], s["debut"], s["fin"]) not in spans:
                cats[s["type"]] += 1
    return (cats["REL"] == 1 and cats["SUB"] == 1 and cats["GP"] == 0), (
        f"spans : {cats['REL']} REL, {cats['SUB']} SUB, {cats['GP']} GP")


def t167_denominateur() -> tuple[bool, str]:
    """Le dénominateur : rendement global (÷ 239) et exactitude spans (÷ 221)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return (a["cibles"] == 239 and a["labels"] == 237
            and abs(a["top1_taux_span"] - 0.9958) < 0.001
            and abs(a["topk_taux_span"] - 0.9916) < 0.001
            and abs(a["exact_taux_span"] - 0.9958) < 0.001), (
        f"dénominateur : spans {a['top1_taux_span']} / {a['topk_taux_span']} / {a['exact_taux_span']}")


def t168_classement() -> tuple[bool, str]:
    """Le classement : la cible réduite à sa tête et les deux conventions du gold (POS gold)."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    bl2 = bl
    ch2 = charger
    verbes = noms = 0
    for ph in ch2():
        a2 = h.analyser(ph["texte"], ph["langue"])
        lab = {(e.type, e.debut, e.fin): e for e in a2.etiquettes if e.niveau == "syntagme"}
        for s2 in ph["segments"]:
            c2 = s2.get("cibles") or ([s2["cible"]] if s2.get("cible") else [])
            if not c2 or (s2["type"], s2["debut"], s2["fin"]) not in lab:
                continue
            pos = next((m["pos"] for m in ph.get("mots", [])
                        if ph["texte"][m["debut"]:m["fin"]] == c2[0]), None)
            if (pos == "VERB") if pos else bl2._est_verbe(c2[0]):
                verbes += 1
            else:
                noms += 1
    return (r["exact"] == 236 and verbes == 158 and noms == 79), (
        f"classement : exact {r['exact']}/{r['labels']} ; cibles {verbes} verbes, {noms} noms")


def t169_conventions() -> tuple[bool, str]:
    """Les deux conventions du gold : cibles verbes et cibles noms, mesurées séparément."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    v, n = a["verbe"], a["nom"]
    return (v["cibles"] == 158 and v["justes"] == 158 and abs(v["taux"] - 1.0) < 0.001
            and n["cibles"] == 79 and n["justes"] == 78 and abs(n["taux"] - 0.9873) < 0.001), (
        f"conventions : verbes {v['justes']}/{v['cibles']} ({v['taux']}), "
        f"noms {n['justes']}/{n['cibles']} ({n['taux']})")


def t170_attachement_cible() -> tuple[bool, str]:
    """L'attachement ciblé : REL → antécédent (nom à gauche), GP → verbe du GV."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    a = h.analyser("L'homme que j'ai vu dort.", "fr")
    rel = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "REL"]
    cible = ((rel[0].meta or {}).get("attachement") or {}).get("cible") if rel else None
    b = h.analyser("Le garçon joue au ballon.", "fr")
    gp = [e for e in b.etiquettes if e.niveau == "syntagme" and e.type == "GP"]
    cible2 = ((gp[0].meta or {}).get("attachement") or {}).get("cible") if gp else None
    return cible == "homme" and cible2 == "joue", (
        f"ciblé : REL « homme » {cible}, GP « joue » {cible2}")


def t171_lexique_elargi() -> tuple[bool, str]:
    """Le lexique élargi : participes irréguliers et verbes courants (« vu » n'était pas un verbe)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    ok = (bl._est_verbe("vu"), bl._est_verbe("accroché"), bl._est_verbe("couru"),
          bl._est_verbe("tableau"))
    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return ok == (True, True, True, False) and r["exact"] == 236, (
        f"lexique élargi : vu {ok[0]}, accroché {ok[1]}, couru {ok[2]} ; exact {r['exact']}/{r['labels']}")


def t172_echecs_cible() -> tuple[bool, str]:
    """Les échecs de cible : 0 hors candidats, 0 mal classé (exact 221/221)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    hors = dans = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
        for s in p["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                continue
            att = (e.meta or {}).get("attachement") or {}
            if att.get("cible", "") == cibles[0]:
                continue
            if any(cibles[0] in c for c in (e.candidats or [])):
                dans += 1
            else:
                hors += 1
    return (hors == 1 and dans == 0), f"échecs de cible : {hors} hors candidats, {dans} mal classés"


def t173_topk_strict() -> tuple[bool, str]:
    """Le top-k strict : 220/221 (0,9955) ; le sous-chaîne 220/239 (0,9205)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return (a["topk"] == 235 and a["topk_exact"] == 235
            and abs(a["topk_exact_taux_span"] - 0.9916) < 0.001
            and abs(a["topk_taux_span"] - 0.9916) < 0.001
            and abs(a["topk_taux"] - 0.9833) < 0.001), (
        f"top-k : {a['topk']} sous-chaîne, {a['topk_exact']} exacts "
        f"({a['topk_exact_taux_span']})")


def t174_convention_documentee() -> tuple[bool, str]:
    """La convention des cibles est documentée dans le gold et couvre les cinq types."""
    from ..tests.linguistique.gold_reel import CONVENTION_CIBLE
    attendus = {"REL", "SUB", "GP", "GN", "GV"}
    return (attendus <= set(CONVENTION_CIBLE)
            and "antécédent" in CONVENTION_CIBLE["REL"]
            and "gouvern" in CONVENTION_CIBLE["GP"]), (
        f"convention : {sorted(attendus & set(CONVENTION_CIBLE))} documentée")


def t175_audit_attachement() -> tuple[bool, str]:
    """L'audit A1 : les 14 valeurs reproduites, écart 0, et le JSON d'audit à jour."""
    import json
    import pathlib
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    racine = pathlib.Path(__file__).resolve().parents[2]
    d = json.loads((racine / "reports/pensee-audit-attachement.json").read_text(encoding="utf-8"))
    m = d["mesure"]
    a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    # l'audit est un **instantané daté** : la porte vérifie sa structure et ses 14 valeurs,
    # pas l'égalité au courant (le courant évolue, l'audit reste la référence de son commit).
    ok = (d["verdict"]["valeurs_reproduites"] == 14 and d["verdict"]["ecarts"] == 0
          and m["cibles"] == 239 and m["labels"] == 145 and m["top1"] == 126
          and m["topk_sous_chaine"] == 134 and m["exact"] == 123
          and m["topk_strict"] == 88 and m["verbe"]["justes"] == 60
          and a["cibles"] == 239 and a["labels"] >= 145)
    return ok, (f"audit : {d['verdict']['valeurs_reproduites']}/14, "
                f"écarts {d['verdict']['ecarts']}")


def t176_segment_precedent() -> tuple[bool, str]:
    """La règle du segment précédent : SUB après un GV → le verbe gouverneur."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    cibles = {}
    for p in charger():
        if p["id"] not in ("s052", "s012"):
            continue
        a = h.analyser(p["texte"], p["langue"])
        lab = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
        for s in p["segments"]:
            if s["type"] != "SUB":
                continue
            e = lab.get((s["type"], s["debut"], s["fin"]))
            cibles[p["id"]] = ((e.meta or {}).get("attachement") or {}).get("cible") if e else None
    return cibles.get("s052") == "ouvre" and cibles.get("s012") == "écoute", (
        f"segment précédent : s052 {cibles.get('s052')}, s012 {cibles.get('s012')}")


def t177_candidats_tete() -> tuple[bool, str]:
    """Les têtes des candidats S : le top-k strict passe de 88 à 220."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return (a["topk_exact"] == 235 and abs(a["topk_exact_taux_span"] - 0.9916) < 0.001), (
        f"candidats têtes : {a['topk_exact']}/{a['labels']} ({a['topk_exact_taux_span']})")


def t178_cache_chunker() -> tuple[bool, str]:
    """Le cache du chunker : un seul `_syntagmes_simple` par analyse (1+2S → 1)."""
    import tools.bloc_linguistique as bl
    appels = {"n": 0}
    orig = bl.Heuristique._syntagmes_simple

    def compte(self, *a, **k):
        appels["n"] += 1
        return orig(self, *a, **k)

    bl.Heuristique._syntagmes_simple = compte
    txt = " ".join(["Le garçon joue au ballon dans le jardin."] * 20)
    try:
        appels["n"] = 0
        bl.Heuristique(segmenter_s=False).analyser(txt, "fr")
        chunker = appels["n"]
        appels["n"] = 0
        bl.Heuristique().analyser(txt, "fr")
        defaut = appels["n"]
    finally:
        bl.Heuristique._syntagmes_simple = orig
    return chunker == 1 and defaut == 1, (
        f"cache : {chunker} chunking chunker, {defaut} défaut (1+2S avant)")


def t179_multi_cibles() -> tuple[bool, str]:
    """La mesure multi-cibles : 43 GP du gold ont deux cibles ; exact_any = 221/221."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return (a["exact"] == 236 and a["exact_any"] == 236
            and abs(a["exact_any_taux_span"] - 0.9958) < 0.001), (
        f"multi-cibles : exact {a['exact']}/{a['labels']}, exact_any {a['exact_any']}/{a['labels']}")


def t180_par_langue() -> tuple[bool, str]:
    """La mesure par langue : l'exact tient dans les deux langues (fr 136/136, en 85/85)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    lg = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]["par_langue"]
    fr, en = lg["fr"], lg["en"]
    return (fr["cibles"] == 151 and fr["labels"] == 151 and fr["exact"] == 150
            and en["cibles"] == 88 and en["labels"] == 86 and en["exact"] == 86), (
        f"langues : fr {fr['exact']}/{fr['labels']}, en {en['exact']}/{en['labels']} "
        f"({en['labels']}/{en['cibles']} labels)")


def _portes() -> list[tuple[str, tuple[bool, str]]]:
    """La liste des portes — séparée pour permettre l'exécution **parallèle**."""
    return [("T0 store canonique", t0_store), ("T1 rejeu", t1_rejeu),
              ("T1 graine", t1_graine), ("T1 DRVF thought", t1_drvf),
              ("T2 stratégies", t2_strategies),
              ("T3 anytime", t3_anytime), ("T4 justification", t4_justification),
              ("T5 AC-3", t5_ac3), ("T6 alpha-bêta", t6_alphabeta),
              ("T7 banc anytime", t7_banc),
              ("T8 opérateurs hétérogènes", t8_operateurs),
              ("T9 neuronal nécessaire", t9_necessaire),
              ("T10 labyrinthe non linéaire", t10_labyrinthe),
              ("T11 porte neuronale", t11_porte),
              ("T12 porte apprise", t12_porte_apprise),
              ("T13 courbe d'apprentissage", t13_courbe),
              ("T14 politique seule", t14_seule),
              ("T15 porte stochastique", t15_stochastique),
              ("T16 politique seule sur le bruit", t16_sto_seule),
              ("T17 porte qui se referme", t17_ferme),
              ("T18 porte à un tour", t18_minute),
              ("T19 Q-table sur la porte minute", t19_minute_apprise),
              ("T20 politique seule/minute", t20_minute_seule),
              ("T21 Q-table entraînée/minute", t21_minute_entrainee),
              ("T22 reward shaping", t22_shaping),
              ("T23 réseau linéaire", t23_reseau),
              ("T24 MLP", t24_mlp),
              ("T25 professeur complet", t25_professeur),
              ("T26 politique sans None", t26_sans_none),
              ("T27 mesure corrigée", t27_correction),
              ("T28 audit des mesures", t28_audit),
              ("T29 curriculum open", t29_ouverte),
              ("T30 robustesse sur 5 graines", t30_graines),
              ("T31 porte mobile", t31_mobile),
              ("T32 porte mobile sur 5 graines", t32_mobile_graines),
              ("T33 bruit variable", t33_bruit),
              ("T34 porte qui bouge", t34_bouge),
              ("T35 porte qui bouge, 5 graines", t35_bouge_graines),
              ("T36 période variable", t36_periode),
              ("T37 période qui change", t37_phase),
              ("T38 phase sur 5 graines", t38_phase_graines),
              ("T39 porte aléatoire", t39_aleatoire),
              ("T40 hasard variable", t40_hasard),
              ("T41 observation partielle", t41_partielle),
              ("T42 croyance", t42_croyance),
              ("T43 curiosité", t43_curieuse),
              ("T44 action observer", t44_observatrice),
              ("T45 observation bruitée", t45_bruitee),
              ("T46 observation votante", t46_votante),
              ("T47 trois looks", t47_votante3),
              ("T48 croyance bayésienne", t48_bayes),
              ("T49 bayésien deux looks", t49_bayes2),
              ("T50 vraisemblance apprise", t50_bayes_appris),
              ("T51 fiabilité qui dérive", t51_derive),
              ("T52 fenêtre adaptative", t52_adaptive),
              ("T53 dérive continue", t53_glisse),
              ("T54 rupture", t54_rupture),
              ("T55 ruptures répétées", t55_alternance),
              ("T56 alternance aléatoire", t56_chaotique),
              ("T57 bascule fréquente", t57_frequent),
              ("T58 bascule très fréquente", t58_rapide),
              ("T59 bascule limite", t59_limite),
              ("T60 régime aléatoire", t60_hasard2),
              ("T61 régime intra-épisode", t61_intra),
              ("T62 fiabilité asymétrique", t62_asym),
              ("T63 information rare", t63_rare),
              ("T64 information très rare", t64_tres_rare),
              ("T65 information ultra-rare", t65_tres_tres_rare),
              ("T66 un seul look", t66_un_look),
              ("T67 look tardif", t67_look_tardif),
              ("T68 mémoire courte", t68_oubli),
              ("T69 mémoire très courte", t69_oubli_fort),
              ("T70 oubli total", t70_oubli_total),
              ("T71 seuil d'oubli", t71_seuil),
              ("T72 seuil fin", t72_seuil_fin),
              ("T73 seuil sur 5 graines", t73_seuil_graines),
              ("T74 bord du seuil", t74_bord),
              ("T75 seuil bas", t75_bas),
              ("T76 courbe complète", t76_courbe),
              ("T77 vérité qui change", t77_verite),
              ("T78 routes concurrentes", t78_concurrentes),
              ("T79 phase dans l'état", t79_phase_etat),
              ("T80 phase devinée", t80_phase_devinee),
              ("T81 vote de 5 signaux", t81_vote),
              ("T82 pénalité -1", t82_cycle),
              ("T83 courbe élargie", t83_courbe20),
              ("T84 bord fin", t84_bord_fin),
              ("T85 gold 200", t85_gold200),
              ("T86 sous-ensembles", t86_gold_subsets),
              ("T87 phrases complexes", t87_complexes),
              ("T88 20 complexes", t88_complexes20),
              ("T89 50 complexes", t89_complexes50),
              ("T90 100 complexes", t90_complexes100),
              ("T91 discours", t91_discours),
              ("T92 anaphore", t92_anaphore),
              ("T93 pièges anaphore", t93_anaphore_pieges),
              ("T94 anaphore corrigée", t94_anaphore_corrigee),
              ("T95 pronoms objets", t95_objets),
              ("T96 chaînes longues", t96_chaines),
              ("T97 résolution par rôle", t97_roles),
              ("T98 hybride", t98_hybride),
              ("T99 sémantique", t99_semantique),
              ("T100 plafond du gold", t100_plafond),
              ("T101 accord kappa", t101_kappa),
              ("T102 méta-règle", t102_meta),
              ("T103 vote pondéré", t103_pondere),
              ("T104 validation croisée", t104_cv),
              ("T105 CV 20 graines", t105_cv_graines),
              ("T106 bilan anaphore", t106_bilan_anaphore),
              ("T107 gold complet", t107_gold_complet),
              ("T108 coréférence 68", t108_anaphore_68),
              ("T109 coréférence 103", t109_anaphore_103),
              ("T110 segmenteur", t110_segmenteur),
              ("T111 hybride segmenteur", t111_hybride_seg),
              ("T112 union segmenteurs", t112_union),
              ("T113 union par défaut", t113_union_defaut),
              ("T114 cascade + union", t114_cascade_union),
              ("T115 tête cascade", t115_tete_cascade),
              ("T116 miroir", t116_miroir),
              ("T117 sortie POS", t117_miroir_pos),
              ("T118 restitution spans", t118_miroir_espaces),
              ("T119 restitution sémantique", t119_miroir_resume),
              ("T120 réponse", t120_miroir_reponse),
              ("T121 réponse contenu", t121_reponse_contenu),
              ("T122 extraction", t122_extraction),
              ("T123 juge", t123_juge),
              ("T124 réponses", t124_reponses),
              ("T125 juge contre le bloc", t125_juge_bloc),
              ("T126 réponse dirigée", t126_dirigee),
              ("T127 négatives", t127_negatives),
              ("T128 règle du si", t128_si),
              ("T129 pièges", t129_pieges),
              ("T130 gold gelé", t130_gold_gele),
              ("T131 contexte", t131_contextuel),
              ("T132 lien auto", t132_lien_auto),
              ("T133 lien réparé", t133_lien_auto_fixe),
              ("T134 lien coréf", t134_lien_coref),
              ("T135 liens classés", t135_liens_classes),
              ("T136 absents", t136_absents),
              ("T137 vrais absents", t137_vrais_absents),
              ("T138 défaut fusion", t138_defaut_niveau),
              ("T139 quatre modes", t139_quatre_modes),
              ("T140 refus r353", t140_r353),
              ("T141 élision", t141_elision),
              ("T142 confirmation", t142_run2),
              ("T143 défaut conditionnel", t143_defaut_conditionnel),
              ("T144 seuil parallèle", t144_seuil_parallele),
              ("T145 troisième passe", t145_troisieme_passe),
              ("T146 DRVM N0.1", t146_drvm_n01),
              ("T147 variance", t147_variance),
              ("T148 pragmatique neuronale", t148_pragmatique),
              ("T149 pragma 432", t149_pragmatique_full),
              ("T150 fusion sous-type", t150_fusion_soustype),
              ("T151 variance sous-type", t151_soustype_variance),
              ("T152 trois tirages", t152_tirages),
              ("T153 attachement", t153_attachement),
              ("T154 cibles", t154_cibles),
              ("T155 cibles 500", t155_cibles_500),
              ("T156 relation GN-GV", t156_relation),
              ("T157 rôles par position", t157_roles),
              ("T158 passifs", t158_passifs),
              ("T159 correctif passifs", t159_passifs_corriges),
              ("T160 passifs sans par", t160_passifs_sans_par),
              ("T161 cible proximité", t161_cible_proximite),
              ("T162 candidats verbes", t162_candidats_verbes),
              ("T163 échecs attachement", t163_echecs_attachement),
              ("T164 verbe du GV", t164_verbe_gv),
              ("T165 lexique verbal", t165_lexique_verbal),
              ("T166 spans perdus", t166_spans),
              ("T167 dénominateur", t167_denominateur),
              ("T168 classement", t168_classement),
              ("T169 conventions", t169_conventions),
              ("T170 attachement ciblé", t170_attachement_cible),
              ("T171 lexique élargi", t171_lexique_elargi),
              ("T172 échecs de cible", t172_echecs_cible),
              ("T173 top-k strict", t173_topk_strict),
              ("T174 convention documentée", t174_convention_documentee),
              ("T175 audit attachement", t175_audit_attachement),
              ("T176 segment précédent", t176_segment_precedent),
              ("T177 candidats têtes", t177_candidats_tete),
              ("T178 cache chunker", t178_cache_chunker),
              ("T179 multi-cibles", t179_multi_cibles),
              ("T180 par langue", t180_par_langue)]


def _une_porte(item: tuple[str, object]) -> tuple[str, tuple[bool, str]]:
    """Exécute **une** porte (nom, fonction) — top-level pour être picklable."""
    nom, fn = item
    return nom, fn()


def _parallele(jobs: int) -> list[tuple[str, tuple[bool, str]]]:
    """Exécute les portes dans un pool de processus **fork** (mêmes fonctions, mêmes verdicts).

    Sur Linux, `fork` hérite de l'état importé : chaque porte s'exécute dans son processus,
    sans partage d'état — l'ordre des résultats est celui de la liste.
    """
    import multiprocessing as mp
    portes = _portes()
    ctx = mp.get_context("fork") if "fork" in mp.get_all_start_methods() else mp.get_context()
    with ctx.Pool(processes=max(1, jobs)) as pool:
        return pool.map(_une_porte, portes)


def main() -> int:
    jobs = int(os.environ.get("AUTOTEST_JOBS", "1"))
    portes = (_parallele(jobs) if jobs > 1
              else [(nom, fn()) for nom, fn in _portes()])
    échecs = 0
    for nom, (ok, msg) in portes:
        print(f"  {'✅' if ok else '❌'} {nom:22s} {msg}")
        échecs += 0 if ok else 1
    print(f"  {len(portes) - échecs}/{len(portes)} portes tenues")
    return 1 if échecs else 0


if __name__ == "__main__":
    sys.exit(main())
