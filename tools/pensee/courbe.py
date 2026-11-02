"""courbe.py — la courbe d'apprentissage de la porte : épisodes × graines.

La `PolitiqueApprise` (Q-learning tabulaire) est entraînée sur le labyrinthe à porte, puis
testée par l'A* + la sonde ; on mesure le **but**, les **nœuds**, le **coût** et les **appels**
pour chaque couple (épisodes, graine). Le JSON et la fiche sont écrits dans `reports/`.

    python3 -m tools.pensee.courbe --json reports/pensee-courbe.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import time

import random

from .moteur import AStar
from .operateurs import (DRVM, LABYRINTHE_PORTE, P_BUT, REGISTRE_P, PolitiqueApprise,
                         _etat_p)
from .store import Budget

EPISODES = (50, 100, 200, 400, 800)
GRAINES = (0, 1, 2)


def seule(p: PolitiqueApprise) -> tuple[bool, int]:
    """La politique seule, sans A* : elle suit son argmax Q jusqu'au but."""
    cle, pas = (0, 0, False), 0
    for _ in range(200):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_p(cle[0], cle[1], cle[2])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


def seule_sto(p: PolitiqueApprise, graine: int = 0, p_ouvre: float = 0.8,
              max_pas: int = 200) -> tuple[bool, int, int]:
    """La politique seule sur la porte stochastique : elle réessaie si la porte résiste."""
    rng = random.Random(graine)
    cle, pas, essais = (0, 0, False), 0, 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas, essais
        if cle[0] == 3 and cle[1] == 2 and not cle[2]:
            essais += 1
            pas += 1
            if rng.random() < p_ouvre:
                cle = (3, 3, True)
            continue
        e = _etat_p(cle[0], cle[1], cle[2])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas, essais
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas, essais


def seule_minute(p: PolitiqueApprise, max_pas: int = 200) -> tuple[bool, int]:
    """La politique seule sur la porte minute : elle ouvre et passe dans le même pas."""
    cle, pas = (0, 0, False), 0
    for _ in range(max_pas):
        if cle[:2] == P_BUT:
            return True, pas
        e = _etat_p(cle[0], cle[1], cle[2])
        a = p.propose(e, P_BUT)
        if a is None:
            return False, pas
        if (cle[0], cle[1]) == (3, 2) and a == "bas":
            cle = (3, 3, False)
            pas += 1
            continue
        cle, _ = p._pas(cle, a, True)
        pas += 1
    return False, pas


def executer() -> list[dict]:
    lignes = []
    for ep in EPISODES:
        for g in GRAINES:
            t0 = time.perf_counter()
            p = PolitiqueApprise(episodes=ep, graine=g)
            p.apprendre()
            d = DRVM(REGISTRE_P, p)
            d.penser(LABYRINTHE_PORTE, AStar(), Budget(200))
            b = d.instantane()
            ok_seule, pas_seule = seule(p)
            ok_sto, pas_sto, essais = seule_sto(p, graine=g)
            ok_min, pas_min = seule_minute(p)
            lignes.append({"episodes": ep, "graine": g, "etats_q": len(p.q),
                           "noeuds": b["noeuds"], "sonde": b["par_operateur"].get("sonde", 0),
                           "cout": b["cout"], "appels": b["appels"], "but": b["but"],
                           "seule_but": ok_seule, "seule_pas": pas_seule,
                           "sto_but": ok_sto, "sto_pas": pas_sto, "sto_essais": essais,
                           "min_but": ok_min, "min_pas": pas_min,
                           "duree_s": round(time.perf_counter() - t0, 3)})
    return lignes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="")
    args = ap.parse_args()
    lignes = executer()
    for l in lignes:
        print(f"{l['episodes']:4d} ep g{l['graine']}  Q {l['etats_q']:3d}  "
              f"{l['noeuds']:3d} nœuds  sonde {l['sonde']:2d}  coût {l['cout']:5.1f}  "
              f"but {l['but']}  seule {l['seule_but']}/{l['seule_pas']}  "
              f"sto {l['sto_but']}/{l['sto_pas']} ({l['sto_essais']} essais)  "
              f"min {l['min_but']}/{l['min_pas']}")
    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-01", "ligne": "B13", "episodes": EPISODES,
                                 "graines": GRAINES, "lignes": lignes},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
