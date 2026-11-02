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
    return abs(p2 - 0.8214) < 0.001 and abs(p1 - 0.7897) < 0.001, (
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
    return abs(r["pos"]["exactitude"] - 0.6471) < 0.001, (
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
    return abs(r["pos"]["exactitude"] - 0.6829) < 0.001, (
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
    return abs(r["pos"]["exactitude"] - 0.7013) < 0.001, (
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
    return abs(r["pos"]["exactitude"] - 0.6984) < 0.001, (
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
    """Le gold complet : 522 phrases, POS 0,7586."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    phrases = charger()
    h = bl.Heuristique()
    r = evaluer_bloc("h", h, phrases)
    return (len(phrases) == 552
            and abs(r["pos"]["exactitude"] - 0.7574) < 0.001), (
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
              ("T64 information très rare", t64_tres_rare()),
              ("T65 information ultra-rare", t65_tres_tres_rare()),
              ("T66 un seul look", t66_un_look()),
              ("T67 look tardif", t67_look_tardif()),
              ("T68 mémoire courte", t68_oubli()),
              ("T69 mémoire très courte", t69_oubli_fort()),
              ("T70 oubli total", t70_oubli_total()),
              ("T71 seuil d'oubli", t71_seuil()),
              ("T72 seuil fin", t72_seuil_fin()),
              ("T73 seuil sur 5 graines", t73_seuil_graines()),
              ("T74 bord du seuil", t74_bord()),
              ("T75 seuil bas", t75_bas()),
              ("T76 courbe complète", t76_courbe()),
              ("T77 vérité qui change", t77_verite()),
              ("T78 routes concurrentes", t78_concurrentes()),
              ("T79 phase dans l'état", t79_phase_etat()),
              ("T80 phase devinée", t80_phase_devinee()),
              ("T81 vote de 5 signaux", t81_vote()),
              ("T82 pénalité -1", t82_cycle()),
              ("T83 courbe élargie", t83_courbe20()),
              ("T84 bord fin", t84_bord_fin()),
              ("T85 gold 200", t85_gold200()),
              ("T86 sous-ensembles", t86_gold_subsets()),
              ("T87 phrases complexes", t87_complexes()),
              ("T88 20 complexes", t88_complexes20()),
              ("T89 50 complexes", t89_complexes50()),
              ("T90 100 complexes", t90_complexes100()),
              ("T91 discours", t91_discours()),
              ("T92 anaphore", t92_anaphore()),
              ("T93 pièges anaphore", t93_anaphore_pieges()),
              ("T94 anaphore corrigée", t94_anaphore_corrigee()),
              ("T95 pronoms objets", t95_objets()),
              ("T96 chaînes longues", t96_chaines()),
              ("T97 résolution par rôle", t97_roles()),
              ("T98 hybride", t98_hybride()),
              ("T99 sémantique", t99_semantique()),
              ("T100 plafond du gold", t100_plafond()),
              ("T101 accord kappa", t101_kappa()),
              ("T102 méta-règle", t102_meta()),
              ("T103 vote pondéré", t103_pondere()),
              ("T104 validation croisée", t104_cv()),
              ("T105 CV 20 graines", t105_cv_graines()),
              ("T106 bilan anaphore", t106_bilan_anaphore()),
              ("T107 gold complet", t107_gold_complet()),
              ("T108 coréférence 68", t108_anaphore_68())]
    échecs = 0
    for nom, (ok, msg) in portes:
        print(f"  {'✅' if ok else '❌'} {nom:22s} {msg}")
        échecs += 0 if ok else 1
    print(f"  {len(portes) - échecs}/{len(portes)} portes tenues")
    return 1 if échecs else 0


if __name__ == "__main__":
    sys.exit(main())
