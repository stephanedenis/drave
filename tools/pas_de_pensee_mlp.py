#!/usr/bin/env python3
"""pas_de_pensee_mlp.py — ÉTAGE 2 : un opérateur NON LINÉAIRE tient-il plus de pas que le linéaire ?

POURQUOI ✓✓. La mesure 82 a montré qu'un opérateur **linéaire** fait deux pas puis s'effondre, la mesure 84 que la
contraction par mélange **dégrade** ✗✗. *Un opérateur **non linéaire** (un petit MLP résiduel) apprend-il mieux la
dynamique ?* ✓✓ C'est le test le plus simple de l'hypothèse « le problème est la **forme** de l'opérateur » ✓✓.

LE DISPOSITIF ✓✓ : les états Verne (200 phrases, 50 séries, 3 B), les mêmes transitions que la mesure 82 (35 séries
d'entraînement, 15 de test) ✓. L'opérateur : `F(x) = x + MLP(x)` (résiduel, pour apprendre le **changement**) ✓✓ ;
MLP 2048 → 256 → 2048, ReLU, dropout 0,1, weight decay ✓. On compare au linéaire (mesure 82) et à l'identité ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def retrieval(pred, cand):
    return float(np.mean(np.argmax(norm(pred) @ norm(cand).T, 1) == np.arange(len(pred))))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", default="data/composition-verne-etats.npz")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--sortie", default="reports/pas-de-pensee-mlp.json")
    ap.add_argument("--epoques", type=int, default=400)
    a = ap.parse_args()
    import torch
    import torch.nn as nn
    z = np.load(a.etats, allow_pickle=False)
    noms = [str(s) for s in z["noms"]]
    if len(noms) != len(z[f"L{a.couche}"]) or any(len(s.split("|")) != 2 for s in noms):
        raise SystemExit("carte des lignes cassée (noms ≠ lignes) : mesure 113 — utiliser tools/pas_de_pensee_corrige.py")
    series = {}
    for i, s in enumerate(noms):
        k, j = s.split("|")
        series.setdefault(int(k), {})[int(j)] = i
    cles = sorted(series)
    rng = np.random.default_rng(1234); rng.shuffle(cles)
    n_tr = int(0.7 * len(cles)); train_s, test_s = cles[:n_tr], cles[n_tr:]
    E = z[f"L{a.couche}"].astype(np.float32)
    Xtr = np.array([E[series[k][j]] for k in train_s for j in range(3)])
    Ytr = np.array([E[series[k][j + 1]] for k in train_s for j in range(3)])
    # normaliser les états (le MLP travaille sur des vecteurs de norme 1)
    Xtr_n = norm(Xtr); Ytr_n = norm(Ytr)
    X = torch.tensor(Xtr_n); Y = torch.tensor(Ytr_n)
    class Residuel(nn.Module):
        def __init__(self, d):
            super().__init__()
            self.net = nn.Sequential(nn.Linear(d, 256), nn.ReLU(), nn.Dropout(0.1), nn.Linear(256, d))
        def forward(self, x):
            return x + self.net(x)
    model = Residuel(E.shape[1])
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
    perte = nn.MSELoss()
    for ep in range(a.epoques):
        model.train(); opt.zero_grad()
        p = model(X); l = perte(p, Y); l.backward(); opt.step()
        if ep % 100 == 0:
            print(f"  époque {ep} · perte {l.item():.4f}")
    model.eval()
    S0 = np.array([E[series[k][0]] for k in test_s])
    with torch.no_grad():
        cur = torch.tensor(norm(S0))
        res = []
        for pas in range(1, 4):
            cur = model(cur)
            cn = cur.numpy()
            justes = 0
            for idx, k in enumerate(test_s):
                cand = np.stack([E[series[k][j]] for j in range(4)])
                justes += int(np.argmax(norm(cn[idx:idx + 1]) @ norm(cand).T) == min(pas, 3))
            res.append(justes / len(test_s))
            print(f"  pas {pas} · retrieval {res[-1]:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"couche": a.couche, "epoques": a.epoques,
                                                  "retrieval_pas": [round(x, 4) for x in res]},
                                                 ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
