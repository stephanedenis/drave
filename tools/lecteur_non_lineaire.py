#!/usr/bin/env python3
"""lecteur_non_lineaire.py — VÉRIFIER L'INSTRUMENT AVANT DE CROIRE LES CONCLUSIONS.

LE PROBLÈME, TROUVÉ AU § 23 ✓✗ : le modèle **dim 512** est un **meilleur** modèle de langue (2,7297 contre
2,8183 bits/octet ✓) mais son « contenu » linéaire est **pire** (104,3 % contre 90,2 ✗). Conclusion
provisoire écrite : *la linéarité était une commodité de mesure, pas une propriété de la pensée* ✓✓. Elle se
**teste** ✓ — en remplaçant le lecteur linéaire (ridge ✓) par un **lecteur non linéaire** (un petit MLP ✓)
sur **les mêmes états**, avec **le même découpage** (60 % / 40 % ✓).

Si le 512 redevient lisible avec le MLP ✓✓ → la linéarité était le seul obstacle, et la métrique de la nuit
est **réparable** ✓. S'il reste moins lisible ✗ → la différence est **réelle** (son état est plus distribué,
au sens propre ✓), et la conclusion du § 23 tient ✓✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/lecteur_non_lineaire.py --modeles /tmp/jouet-d256,/tmp/jouet-d512 \\
      --ids /tmp/ids-octets.txt
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch
import torch.nn as nn


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modeles", required=True, help="liste séparée par des virgules")
    ap.add_argument("--ids", required=True)
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--amorces", type=int, default=60)
    ap.add_argument("--cachee", type=int, default=256)
    ap.add_argument("--pas", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=1e-3)
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]

    print()
    print("   modèle  | RIDGE (linéaire) | MLP (non linéaire) | verdict")
    print("   --------|------------------|--------------------|---------")
    for chemin in a.modeles.split(","):
        m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).eval()
        S, T = [], []
        with torch.no_grad():
            for i in range(a.amorces):
                d = 1000 + i * 1200
                b = torch.tensor([ids[d:d + a.longueur]])
                hs = m(b, output_hidden_states=True).hidden_states[-1][0]
                S.append(m.model.norm(hs).numpy().astype(np.float32))
                T.append(m.get_input_embeddings()(torch.tensor([ids[d + 1:d + a.longueur + 1]]))[0]
                         .numpy().astype(np.float32))
        S, T = np.concatenate(S), np.concatenate(T)
        n = int(S.shape[0] * 0.6)
        S_tr, T_tr, S_te, T_te = S[:n], T[:n], S[n:], T[n:]
        dim = S.shape[1]

        # 1. le lecteur LINÉAIRE (le ridge de toute la nuit ✓)
        mh, me = S_tr.mean(0), T_tr.mean(0)
        Hc, Ec = S_tr - mh, T_tr - me
        W = np.linalg.solve(Hc.T @ Hc + 1e-3 * np.eye(dim), Hc.T @ Ec)
        P = (S_te - mh) @ W + me
        lin = 100 * float(np.linalg.norm(P - T_te) / np.linalg.norm(T_te))

        # 2. le lecteur NON LINÉAIRE (même découpage ✓, même cible ✓)
        torch.manual_seed(0)
        mlp = nn.Sequential(nn.Linear(dim, a.cachee), nn.GELU(), nn.Linear(a.cachee, dim)).cuda()
        opt = torch.optim.AdamW(mlp.parameters(), lr=a.lr)
        Xtr = torch.tensor(S_tr).cuda(); Ytr = torch.tensor(T_tr).cuda()
        Xte = torch.tensor(S_te).cuda(); Yte = torch.tensor(T_te).cuda()
        for pas in range(1, a.pas + 1):
            idx = torch.randperm(Xtr.shape[0])[:1024]
            perte = ((mlp(Xtr[idx]) - Ytr[idx]) ** 2).mean()
            opt.zero_grad(); perte.backward(); opt.step()
        with torch.no_grad():
            Q = mlp(Xte).cpu().numpy()
        nl = 100 * float(np.linalg.norm(Q - T_te) / np.linalg.norm(T_te))

        verdict = "linéarité = obstacle ✓" if nl < lin * 0.9 else ("rien ne change ✗" if nl >= lin * 0.95 else "un peu")
        print(f"   {pathlib.Path(chemin).name:8s} | {lin:15.1f} % | {nl:17.1f} % | {verdict}")
        del m

    print()
    print("   lecture : si le MLP fait nettement mieux que le ridge SURTOUT pour le plus gros modèle ✓✓,")
    print("   alors la linéarité était le seul obstacle et la métrique du § 23 est réparable ✓ ; si les deux")
    print("   lecteurs classent les modèles pareil ✗, la conclusion du § 23 tient telle quelle ✓.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
