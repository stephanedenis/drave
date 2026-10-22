#!/usr/bin/env python3
"""plan_code.py — ÉTAGE 2 : la trajectoire d'une série est-elle compressible en un **code de plan** ?

POURQUOI ✓✓. Les mesures 113-116 ont montré que ni l'état d'une phrase ni le contexte **figé** ne portent la suite
✗✗. Avant de bâtir un objectif de plan dans le modèle, il faut répondre à une question plus simple : la trajectoire
d'une série (8 états) vit-elle dans un **espace de faible dimension** partagé entre séries ? Si oui, un **code de
plan** existe et il reste à l'apprendre ; si non, chaque série est idiosyncratique et le plan doit être entraîné
dans le modèle ✓✓.

CE QU'ON MESURE ✓✓ : un auto-encodeur GRU (8 états → code de 32 → décodeur positionnel) entraîné sur 214 séries et
évalué sur 93 séries **tenues à part** ; on rapporte le cosinus de reconstruction par position, contre la
**moyenne** (baseline) et le **contrôle** (code mélangé entre séries) ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · reconstruction **haute** (> 0,9) sur les séries tenues à part → la trajectoire est un **objet de faible dimension**
    partagé : le plan est représentable, il reste à le prédire ✓✓ ;
  · reconstruction **basse** → les états figés ne contiennent pas de plan compressible ; il faut l'entraîner dans le
    modèle ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np
import torch
import torch.nn as nn

def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))

class Code(nn.Module):
    def __init__(self, d, cache, code, T):
        super().__init__()
        self.gru = nn.GRU(d, cache, batch_first=True)
        self.encode = nn.Linear(cache, code)
        self.pos = nn.Embedding(T, code)
        self.decode = nn.Sequential(nn.Linear(2 * code, cache), nn.GELU(), nn.Linear(cache, d))

    def decoder(self, z, T):
        zt = z[:, None, :].expand(-1, T, -1)
        p = self.pos(torch.arange(T, device=z.device))[None, :, :].expand(len(z), -1, -1)
        return self.decode(torch.cat([zt, p], -1))

    def forward(self, x):
        h, _ = self.gru(x)
        z = self.encode(h[:, -1, :])
        return self.decoder(z, x.shape[1]), z

def entrainer(X, cache, code, epochs, lr, graine, lot=64):
    torch.manual_seed(graine)
    Xt = torch.from_numpy(X)
    n, T, d = Xt.shape
    m = Code(d, cache, code, T)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=1e-4)
    generateur = torch.Generator().manual_seed(graine)
    perte = torch.tensor(0.0)
    for _ in range(epochs):
        ordre = torch.randperm(n, generator=generateur)
        for deb in range(0, n, lot):
            idx = ordre[deb:deb + lot]
            pred, z = m(Xt[idx])
            perte = (1 - torch.sum(torch.nn.functional.normalize(pred, dim=-1) *
                                   torch.nn.functional.normalize(Xt[idx], dim=-1), -1)).mean()
            opt.zero_grad(); perte.backward(); opt.step()
    return m, float(perte.detach())

def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--par-serie", type=int, default=8)
    ap.add_argument("--couches", default="12,18,24")
    ap.add_argument("--cache", type=int, default=256)
    ap.add_argument("--code", type=int, default=32)
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--graines", type=int, default=2)
    a = ap.parse_args()
    z = np.load(a.etats, allow_pickle=False)
    codes = [int(c) for c in a.couches.split(",")]
    E0 = z[f"L{codes[0]}"]
    n_phrases = E0.shape[0] // 2
    T = a.par_serie
    n_series = n_phrases // T
    rng = np.random.default_rng(1234)
    cles = np.arange(n_series); rng.shuffle(cles)
    n_tr = int(0.7 * n_series)
    tr, te = cles[:n_tr], cles[n_tr:]
    res = []
    for L in codes:
        X = z[f"L{L}"].astype(np.float32)[0::2].reshape(n_series, T, -1)
        mean = X[tr].mean((0, 1), keepdims=True)
        Xn = X / np.maximum(1e-9, np.linalg.norm(X, axis=-1, keepdims=True))
        moy = Xn[tr].mean((0, 1), keepdims=True)
        moy_plat = np.broadcast_to(moy, (len(te), T, X.shape[2])).reshape(-1, X.shape[2])
        cos_moy = float(np.mean(np.sum(norm(X[te].reshape(-1, X.shape[2])) * norm(moy_plat), -1)))
        recons, melanges, zs = [], [], []
        for g in range(a.graines):
            m, perte = entrainer(Xn[tr], a.cache, a.code, a.epochs, 1e-3, graine=1000 + g)
            with torch.no_grad():
                pred, zz = m(torch.from_numpy(Xn[te]))
                cible = torch.from_numpy(Xn[te])
                cos = float(np.mean(torch.sum(torch.nn.functional.normalize(pred, dim=-1) *
                                              torch.nn.functional.normalize(cible, dim=-1), -1).numpy()))
                perm = torch.randperm(len(zz), generator=torch.Generator().manual_seed(2000 + g))
                pred_m = m.decoder(zz[perm], T)
                cos_m = float(np.mean(torch.sum(torch.nn.functional.normalize(pred_m, dim=-1) *
                                                torch.nn.functional.normalize(cible, dim=-1), -1).numpy()))
            recons.append(cos); melanges.append(cos_m); zs.append(zz.numpy())
        zcat = np.concatenate(zs, 0)
        res.append({"couche": int(L), "reconstruction": [round(x, 4) for x in recons],
                    "reconstruction_moyenne": round(float(np.mean(recons)), 4),
                    "reconstruction_melangee": [round(x, 4) for x in melanges],
                    "cos_moyenne_baseline": round(cos_moy, 4),
                    "code_std": round(float(zcat.std(0).mean()), 4)})
        print(f"  L{L:<2} reconstruction test {res[-1]['reconstruction']} · mélangé {res[-1]['reconstruction_melangee']} · "
              f"baseline moyenne {res[-1]['cos_moyenne_baseline']} · écart-type du code {res[-1]['code_std']}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({
        "etats": a.etats, "n_series": n_series, "n_series_train": len(tr), "n_series_test": len(te),
        "par_serie": T, "code": a.code, "graines": a.graines, "epochs": a.epochs, "resultats": res},
        ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0

if __name__ == "__main__":
    raise SystemExit(principal())
