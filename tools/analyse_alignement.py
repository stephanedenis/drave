#!/usr/bin/env python3
"""analyse_alignement.py — le pont linéaire en ridge DUAL (rapide), dans les deux sens.

POURQUOI ✓✓. L'analyse primale de `pensee_multilingue.py` résout un système (D+1)×(D+1) pour chaque λ et chaque
couche : sur le 7 B (D = 3 584), c'est trop lent ✗✗. Le ridge **dual** donne **la même prédiction** pour n < D en
résolvant un système **n×n** (n = 100) ✓✓ — quelques secondes ✓✓.

CE QU'IL MESURE ✓✓ :
  · retrieval brut (sans pont) ✓ ;
  · pont dual X → Y (λ choisi par validation interne), cosinus et retrieval après pont ✓✓ ;
  · contrôle négatif : pont appris sur des paires **mélangées** ✓✓ ;
  · les deux sens : X → anglais (lire) et anglais → X (écrire) ✓✓ — *le miroir entrée/sortie* ✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def retr(A, B):
    return float(np.mean(np.argmax(norm(A) @ norm(B).T, 1) == np.arange(len(A))))


def dual_fit(X, Y, lam):
    """Ridge dual centré : W n'est jamais formé ; α = (K + λI)⁻¹ Y, K = X Xᵀ."""
    mx, my = X.mean(0), Y.mean(0)
    Xc, Yc = X - mx, Y - my
    K = Xc @ Xc.T
    alpha = np.linalg.solve(K + lam * np.eye(len(K), dtype=np.float32), Yc)
    return mx, my, Xc, alpha


def dual_pred(X, modele):
    mx, my, Xtr, alpha = modele
    return (X - mx) @ Xtr.T @ alpha + my


def analyse(npz: str, sortie: str) -> None:
    d = np.load(npz, allow_pickle=False)
    couches = [int(c) for c in d["couches"]]
    langues = [str(x) for x in d["langues"]]
    rng = np.random.default_rng(1234)
    n = d[f"eng_{couches[0]}"].shape[0]
    idx = rng.permutation(n)
    tr, va, te = idx[:70], idx[70:100], idx[100:]
    lam_grid = (0.1, 1.0, 10.0, 100.0, 1000.0)
    res = []
    for lg in langues:
        if lg == "eng":
            continue
        for sens, (src, dst) in {"lire": (lg, "eng"), "ecrire": ("eng", lg)}.items():
            best = None
            for L in couches:
                X = d[f"{src}_{L}"].astype(np.float32)
                Y = d[f"{dst}_{L}"].astype(np.float32)
                brut = retr(X[te], Y[te])
                lam = max(lam_grid, key=lambda l: retr(dual_pred(X[va], dual_fit(X[tr], Y[tr], l)), Y[va]))
                modele = dual_fit(X[tr], Y[tr], lam)
                pred = dual_pred(X[te], modele)
                cos = float(np.mean(np.sum(norm(pred) * norm(Y[te]), 1)))
                r = retr(pred, Y[te])
                mel = rng.permutation(len(tr))
                neg = retr(dual_pred(X[te], dual_fit(X[tr], Y[tr][mel], lam)), Y[te])
                ligne = {"langue": lg, "sens": sens, "couche": int(L), "lambda": lam,
                         "retrieval_brut": round(brut, 4), "cosinus_pont": round(cos, 4),
                         "retrieval_pont": round(r, 4), "retrieval_negatif": round(neg, 4)}
                if best is None or r > best["retrieval_pont"]:
                    best = ligne
            res.append(best)
    pathlib.Path(sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(sortie).write_text(json.dumps({"n": n, "couches": couches, "langues": langues,
                                                "resultats": res}, ensure_ascii=False, indent=1))
    for x in sorted(res, key=lambda r: (r["sens"], -r["retrieval_pont"])):
        print(f"  {x['sens']:7s} {x['langue']:4s} couche {x['couche']:2d} · brut {x['retrieval_brut']:.3f} · "
              f"cos {x['cosinus_pont']:.3f} · pont {x['retrieval_pont']:.3f} · neg {x['retrieval_negatif']:.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True)
    ap.add_argument("--sortie", required=True)
    a = ap.parse_args()
    analyse(a.etats, a.sortie)
