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


def main() -> int:
    portes = [("T0 store canonique", t0_store()), ("T1 rejeu", t1_rejeu()),
              ("T1 graine", t1_graine()), ("T1 DRVF thought", t1_drvf()),
              ("T2 stratégies", t2_strategies()),
              ("T3 anytime", t3_anytime()), ("T4 justification", t4_justification()),
              ("T5 AC-3", t5_ac3()), ("T6 alpha-bêta", t6_alphabeta()),
              ("T7 banc anytime", t7_banc()),
              ("T8 opérateurs hétérogènes", t8_operateurs()),
              ("T9 neuronal nécessaire", t9_necessaire()),
              ("T10 labyrinthe non linéaire", t10_labyrinthe()),
              ("T11 porte neuronale", t11_porte()),
              ("T12 porte apprise", t12_porte_apprise()),
              ("T13 courbe d'apprentissage", t13_courbe()),
              ("T14 politique seule", t14_seule()),
              ("T15 porte stochastique", t15_stochastique()),
              ("T16 politique seule sur le bruit", t16_sto_seule()),
              ("T17 porte qui se referme", t17_ferme()),
              ("T18 porte à un tour", t18_minute()),
              ("T19 Q-table sur la porte minute", t19_minute_apprise()),
              ("T20 politique seule/minute", t20_minute_seule()),
              ("T21 Q-table entraînée/minute", t21_minute_entrainee()),
              ("T22 reward shaping", t22_shaping()),
              ("T23 réseau linéaire", t23_reseau()),
              ("T24 MLP", t24_mlp()),
              ("T25 professeur complet", t25_professeur()),
              ("T26 politique sans None", t26_sans_none()),
              ("T27 mesure corrigée", t27_correction()),
              ("T28 audit des mesures", t28_audit()),
              ("T29 curriculum open", t29_ouverte()),
              ("T30 robustesse sur 5 graines", t30_graines()),
              ("T31 porte mobile", t31_mobile()),
              ("T32 porte mobile sur 5 graines", t32_mobile_graines()),
              ("T33 bruit variable", t33_bruit()),
              ("T34 porte qui bouge", t34_bouge()),
              ("T35 porte qui bouge, 5 graines", t35_bouge_graines()),
              ("T36 période variable", t36_periode()),
              ("T37 période qui change", t37_phase()),
              ("T38 phase sur 5 graines", t38_phase_graines()),
              ("T39 porte aléatoire", t39_aleatoire()),
              ("T40 hasard variable", t40_hasard()),
              ("T41 observation partielle", t41_partielle()),
              ("T42 croyance", t42_croyance()),
              ("T43 curiosité", t43_curieuse()),
              ("T44 action observer", t44_observatrice()),
              ("T45 observation bruitée", t45_bruitee()),
              ("T46 observation votante", t46_votante()),
              ("T47 trois looks", t47_votante3()),
              ("T48 croyance bayésienne", t48_bayes()),
              ("T49 bayésien deux looks", t49_bayes2()),
              ("T50 vraisemblance apprise", t50_bayes_appris()),
              ("T51 fiabilité qui dérive", t51_derive()),
              ("T52 fenêtre adaptative", t52_adaptive()),
              ("T53 dérive continue", t53_glisse()),
              ("T54 rupture", t54_rupture()),
              ("T55 ruptures répétées", t55_alternance()),
              ("T56 alternance aléatoire", t56_chaotique()),
              ("T57 bascule fréquente", t57_frequent()),
              ("T58 bascule très fréquente", t58_rapide()),
              ("T59 bascule limite", t59_limite()),
              ("T60 régime aléatoire", t60_hasard2()),
              ("T61 régime intra-épisode", t61_intra()),
              ("T62 fiabilité asymétrique", t62_asym()),
              ("T63 information rare", t63_rare()),
              ("T64 information très rare", t64_tres_rare())]
    échecs = 0
    for nom, (ok, msg) in portes:
        print(f"  {'✅' if ok else '❌'} {nom:22s} {msg}")
        échecs += 0 if ok else 1
    print(f"  {len(portes) - échecs}/{len(portes)} portes tenues")
    return 1 if échecs else 0


if __name__ == "__main__":
    sys.exit(main())
