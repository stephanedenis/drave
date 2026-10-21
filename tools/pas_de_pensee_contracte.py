#!/usr/bin/env python3
"""pas_de_pensee_contracte.py — ÉTAGE 2 : une dynamique CONTRACTANTE tient-elle plus de pas ?

POURQUOI ✓✓. La mesure 82 a montré qu'un opérateur linéaire F fait **deux pas** de pensée puis s'effondre, et la
mesure 83 que la taille ne repousse pas la falaise ✗✗. Le chapitre 5 attribue la falaise à l'absence de
**contraction** : l'état prédit sort de la variété des états réels ✓✓. On teste ici la correction la plus simple :
**mélanger** le pas appris avec l'état courant, `x' = (1−α)·x + α·F(x)`, pour α ∈ {0,25, 0,5, 0,75, 1} ✓✓ — et
une **projection de norme** (garder la norme de l'état courant) ✓✓.

CE QU'ON MESURE ✓✓ : le retrieval de la bonne position (parmi les 4 phrases de la série, hasard 25 %) aux pas 1,
2 et 3, pour chaque α et chaque couche ✓✓. *Si une contraction tient 3 pas, la falaise n'est pas une fatalité ;
sinon, il faut un opérateur **appris** par récurrence, pas un linéaire mélangé* ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def cos(a, b):
    return float(np.mean(np.sum(norm(a) * norm(b), 1)))


def retr(pred, cand):
    return float(np.mean(np.argmax(norm(pred) @ norm(cand).T, 1) == np.arange(len(pred))))


def fit(X, Y, lam):
    Xb = np.hstack([X, np.ones((len(X), 1), np.float32)])
    return np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)


def apply(X, W):
    return np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", default="data/composition-verne-etats.npz")
    ap.add_argument("--sortie", default="reports/pas-de-pensee-contracte.json")
    a = ap.parse_args()
    z = np.load(a.etats, allow_pickle=False)
    couches = [int(c) for c in z["couches"]]
    noms = [str(s) for s in z["noms"]]
    series = {}
    for i, s in enumerate(noms):
        k, j = s.split("|")
        series.setdefault(int(k), {})[int(j)] = i
    cles = sorted(series)
    rng = np.random.default_rng(1234); rng.shuffle(cles)
    n_tr = int(0.7 * len(cles))
    train_s, test_s = cles[:n_tr], cles[n_tr:]
    res = []
    for L in couches:
        E = z[f"L{L}"].astype(np.float32)
        Xtr, Ytr = [], []
        for k in train_s:
            for j in range(3):
                Xtr.append(E[series[k][j]]); Ytr.append(E[series[k][j + 1]])
        Xtr, Ytr = np.array(Xtr), np.array(Ytr)
        nv = max(10, len(Xtr) // 5)
        lam = max((0.1, 1.0, 10.0, 100.0, 1000.0),
                  key=lambda l: cos(apply(Xtr[-nv:], fit(Xtr[:-nv], Ytr[:-nv], l)), Ytr[-nv:]))
        W = fit(Xtr, Ytr, lam)
        S0 = np.array([E[series[k][0]] for k in test_s])
        for alpha in (0.25, 0.5, 0.75, 1.0):
            for projeter in (False, True):
                cur = S0.copy(); pas_reussis = []
                for pas in range(1, 4):
                    pred = apply(cur, W)
                    if projeter:
                        # garder la norme de l'état courant (projection sur la sphère) ✓
                        ncur = np.linalg.norm(cur, axis=1, keepdims=True)
                        pred = pred / np.maximum(1e-9, np.linalg.norm(pred, axis=1, keepdims=True)) * ncur
                    cur = (1 - alpha) * cur + alpha * pred
                    justes = 0
                    for idx, k in enumerate(test_s):
                        cand = np.stack([E[series[k][j]] for j in range(4)])
                        sims = norm(cur[idx:idx + 1]) @ norm(cand).T
                        justes += int(np.argmax(sims) == min(pas, 3))
                    pas_reussis.append(justes / len(test_s))
                res.append({"couche": int(L), "alpha": alpha, "projeter": projeter,
                            "retrieval_pas": [round(x, 4) for x in pas_reussis]})
        print(f"  couche {L:2d} : fait")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"n_series_test": len(test_s), "resultats": res},
                                                 ensure_ascii=False, indent=1))
    # meilleur réglage : celui qui tient le plus de pas au-dessus de 0,25
    def tenue(r):
        return sum(1 for x in r["retrieval_pas"] if x > 0.25)
    meilleur = max(res, key=lambda r: (tenue(r), sum(r["retrieval_pas"])))
    print(f"  meilleur : couche {meilleur['couche']} · α {meilleur['alpha']} · projection {meilleur['projeter']} · "
          f"pas {meilleur['retrieval_pas']}")
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
