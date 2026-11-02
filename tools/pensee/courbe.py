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

from .moteur import AStar
from .operateurs import DRVM, LABYRINTHE_PORTE, REGISTRE_P, PolitiqueApprise
from .store import Budget

EPISODES = (50, 100, 200, 400, 800)
GRAINES = (0, 1, 2)


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
            lignes.append({"episodes": ep, "graine": g, "etats_q": len(p.q),
                           "noeuds": b["noeuds"], "sonde": b["par_operateur"].get("sonde", 0),
                           "cout": b["cout"], "appels": b["appels"], "but": b["but"],
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
              f"but {l['but']}")
    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-01", "ligne": "B13", "episodes": EPISODES,
                                 "graines": GRAINES, "lignes": lignes},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
