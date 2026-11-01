"""banc.py — le banc anytime : AUC, regret et budget du but, par problème et stratégie.

Pour chaque budget croissant, on relance le moteur **à froid** et on lit la meilleure qualité
**visitée** (le score des états du store). La courbe best-so-far donne :

  - l'**AUC** : la moyenne des meilleures qualités aux budgets (1 = parfait) ;
  - le **regret** : 1 − la meilleure qualité au budget maximal ;
  - le **budget du but** : le premier budget où la qualité atteint 1.

Le contrôle négatif est une stratégie **aléatoire** : même budget, AUC basse.

    python3 -m tools.pensee.banc --json reports/pensee-banc.json
"""
from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass, field

from .cruches import CRUCHES
from .moteur import AStar, BFS, Greedy, MCTSLite, Moteur, Proposition, Strategie
from .store import Budget
from .taquin import TAQUIN


class Random(Strategie):
    nom = "random"

    def __init__(self, graine: int = 0):
        self.rng = random.Random(graine)

    def choisir(self, store, probleme):
        return self.rng.choice(list(store.ouverts))

    def proposer(self, etat, probleme):
        ops = [n for n in sorted(probleme.operateurs) if probleme.operateurs[n](etat, {})]
        if not ops:
            return []
        return [Proposition(etat.empreinte(), self.rng.choice(ops), {})]


@dataclass
class Resultat:
    probleme: str
    strategie: str
    budgets: list[int]
    qualites: list[float]
    auc: float
    regret: float
    budget_but: int | None
    noeuds: int
    duree_s: float
    meilleure: float

    def vers_dict(self) -> dict:
        return {"probleme": self.probleme, "strategie": self.strategie,
                "budgets": self.budgets, "qualites": self.qualites,
                "auc": self.auc, "regret": self.regret,
                "budget_but": self.budget_but, "noeuds": self.noeuds,
                "duree_s": round(self.duree_s, 4), "meilleure": self.meilleure}


def executer(probleme, fabrique, budgets, nom: str = "") -> Resultat:
    qualites: list[float] = []
    noeuds = 0
    duree = 0.0
    for b in budgets:
        t0 = time.perf_counter()
        m = Moteur()
        d = m.boucle(probleme, fabrique(), Budget(b), arret_sur_but=True)
        duree += time.perf_counter() - t0
        noeuds += d.budget_consomme
        meilleure = max((probleme.score(e) for e in m.store.etats.values()), default=0.0)
        qualites.append(round(float(meilleure), 4))
    auc = round(sum(qualites) / len(qualites), 4) if qualites else 0.0
    meilleure = max(qualites, default=0.0)
    regret = round(1.0 - meilleure, 4)
    budget_but = next((b for b, q in zip(budgets, qualites) if q >= 1.0 - 1e-9), None)
    return Resultat(probleme.nom, nom or fabrique().__class__.__name__, budgets, qualites,
                    auc, regret, budget_but, noeuds, duree, meilleure)


BUDGETS = {"cruches": [1, 2, 4, 8, 16, 32, 64, 128],
           "taquin": [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]}

STRATEGIES = {
    "bfs": lambda: BFS(),
    "greedy": lambda: Greedy(),
    "astar": lambda: AStar(),
    "mcts": lambda: MCTSLite(graine=0),
    "random": lambda: Random(graine=0),
}


def banc(problemes: dict | None = None, strategies: dict | None = None) -> list[Resultat]:
    problemes = problemes or {"cruches": CRUCHES, "taquin": TAQUIN}
    strategies = strategies or STRATEGIES
    sortie = []
    for nom, probleme in problemes.items():
        for s_nom, fabrique in strategies.items():
            sortie.append(executer(probleme, fabrique, BUDGETS.get(nom, [1, 2, 4, 8]), s_nom))
    return sortie


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="")
    args = ap.parse_args()
    resultats = banc()
    for r in resultats:
        print(f"{r.probleme:8s} {r.strategie:7s} AUC {r.auc:.3f}  regret {r.regret:.3f}  "
              f"but {r.budget_but}  nœuds {r.noeuds}  {r.duree_s:.2f}s  {r.qualites}")
    if args.json:
        payload = {"date": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "budgets": BUDGETS,
                   "resultats": [r.vers_dict() for r in resultats]}
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
            f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
