#!/usr/bin/env python3
"""pas_de_pensee_recurrent.py — ÉTAGE 2 : un opérateur appris PAR RÉCURRENCE tient-il plus de pas ?

POURQUOI ✓✓. Le linéaire F tient deux pas puis s'effondre (mesure 82) ; la taille ne repousse pas la falaise
(mesure 83) ; la contraction par mélange dégrade (mesure 87) ; le MLP naïf sur-apprend (mesure 88) ✗✗. Le
chapitre 5 et le docstring du contrat disent la suite : un opérateur **appris par récurrence** — les **mêmes poids**
appliqués K fois, entraînés de bout en bout sur les cibles multi-pas ✓✓. On teste `F(x) = x + MLP(x)` partagé,
entraîné sur les transitions ET sur les cibles F¹, F², F³ depuis la phrase 0 ✓✓.

CE QU'ON MESURE ✓✓ : le retrieval de la bonne position (parmi les 4 phrases de la série, hasard 25 %) aux pas 1,
2 et 3, contre le linéaire (mesure 82) et l'identité ✓✓. *Si la récurrence tient 3 pas, la falaise est repoussée
par l'apprentissage, pas par la contraction.*
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np
import torch
import torch.nn as nn


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=-1, keepdims=True))


def cos(a, b):
    return float(np.mean(np.sum(norm(a) * norm(b), -1)))


def tnorm(x):
    return x / x.norm(dim=-1, keepdim=True).clamp_min(1e-9)


class Bloc(nn.Module):
    def __init__(self, d: int, cache: int = 256):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(d, cache), nn.GELU(), nn.Linear(cache, d))

    def forward(self, x):
        return x + self.f(x)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", default="data/composition-verne-etats.npz")
    ap.add_argument("--sortie", default="reports/pas-de-pensee-recurrent.json")
    ap.add_argument("--pas", type=int, default=3)
    ap.add_argument("--epochs", type=int, default=400)
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
        E = torch.tensor(z[f"L{L}"].astype(np.float32))
        d = E.shape[1]
        torch.manual_seed(1234)
        modele = Bloc(d)
        opt = torch.optim.AdamW(modele.parameters(), lr=1e-3, weight_decay=1e-4)
        # entraînement : transitions + multi-pas depuis la phrase 0
        X, Y1, Y2, Y3 = [], [], [], []
        for k in train_s:
            for j in range(3):
                X.append(E[series[k][j]]); Y1.append(E[series[k][j + 1]])
            Y2.append(E[series[k][2]]); Y3.append(E[series[k][3]])
        X = torch.stack(X); Y1 = torch.stack(Y1)
        # les cibles multi-pas : on réutilise Y1 pour le pas 1, et les états 2/3 des séries
        s0 = torch.stack([E[series[k][0]] for k in train_s])
        t2 = torch.stack([E[series[k][2]] for k in train_s])
        t3 = torch.stack([E[series[k][3]] for k in train_s])
        s1 = torch.stack([E[series[k][1]] for k in train_s])
        for ep in range(a.epochs):
            opt.zero_grad()
            # multi-pas partagé : F¹ = état 1, F² = état 2, F³ = état 3
            h = s0
            perte = 0.0
            for cible in (s1, t2, t3):
                h = modele(h)
                perte = perte + (1 - torch.sum(tnorm(h) * tnorm(cible), -1)).mean()
            # un pas sur les transitions
            p1 = modele(X)
            perte = perte + 0.5 * (1 - torch.sum(tnorm(p1) * tnorm(Y1), -1)).mean()
            perte.backward(); opt.step()
        modele.eval()
        with torch.no_grad():
            # un pas
            p1 = modele(torch.stack([E[series[k][j]] for k in test_s for j in range(3)]))
            y1 = torch.stack([E[series[k][j + 1]] for k in test_s for j in range(3)])
            ret1 = float((torch.argmax(norm(p1) @ norm(y1).T, 1) == torch.arange(len(y1))).float().mean())
            # itération depuis la phrase 0
            h = torch.stack([E[series[k][0]] for k in test_s])
            rets = []
            for pas in range(1, a.pas + 1):
                h = modele(h)
                justes = 0
                for idx, k in enumerate(test_s):
                    cand = torch.stack([E[series[k][j]] for j in range(4)])
                    sims = norm(h[idx:idx + 1]) @ norm(cand).T
                    justes += int(torch.argmax(sims) == min(pas, 3))
                rets.append(justes / len(test_s))
        res.append({"couche": int(L), "retrieval_un_pas": round(ret1, 4),
                    "retrieval_iteration": [round(x, 4) for x in rets]})
        print(f"  couche {L:2d} · un pas ret {ret1:.3f} · itération {rets}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"n_train": len(train_s), "n_test": len(test_s),
                                                  "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
