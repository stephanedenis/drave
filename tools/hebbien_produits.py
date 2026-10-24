#!/usr/bin/env python3
"""hebbien_produits.py — A6.1 : les produits hebbiens ajoutent-ils quelque chose à la trace linéaire ?

L'idée (rapport-capteur-hebbien § 4) : la trace LINÉAIRE H = XᵀX capture les corrélations
entre neurones, mais aucun nœud nouveau — ses colonnes restent dans l'espace des entrées.
La trace des PRODUITS H[o][(i,j)] += y[o]·x_i·x_j capture, elle, un espace de
caractéristiques réellement neuf. On le teste sur une vraie trace :

  on tient à l'écart 1/8 des neurones d'une couche, on prédit leur activation à partir
  des autres (7/8), avec (a) la régression linéaire seule, (b) la linéaire + les produits.

Si les produits n'ajoutent rien, la R² ne bouge pas ; s'ils ajoutent, elle monte.

Usage : hebbien_produits.py --trace /tmp/t6.drvf --couche 6 [--paires 256] [--tenus 112]
"""
import argparse
import sys

import numpy as np

sys.path.insert(0, "tools")
from diff_flux import lire  # le lecteur DRVF (v1/v2)


def principal():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", required=True)
    ap.add_argument("--couche", type=int, default=6)
    ap.add_argument("--tenus", type=int, default=112, help="neurones tenus à l'écart (1/8 de 896)")
    ap.add_argument("--paires", type=int, default=256)
    ap.add_argument("--graine", type=int, default=42)
    a = ap.parse_args()
    version, n_layer, hidden, listes = lire(a.trace)
    lignes = sorted((pos, ech, actifs)
                    for (c, pos), (ech, actifs) in listes.items() if c == a.couche)
    if len(lignes) < 32:
        raise SystemExit(f"pas assez de positions pour la couche {a.couche} ({len(lignes)})")
    X = np.zeros((len(lignes), hidden), np.float32)
    for r, (_, ech, actifs) in enumerate(lignes):
        for i, v in actifs.items():
            X[r, i] = v * ech
    print(f"  {len(lignes)} positions × {hidden} neurones · couche {a.couche} · trace v{version}")

    rng = np.random.default_rng(a.graine)
    tenus = rng.choice(hidden, a.tenus, replace=False)
    masque = np.ones(hidden, bool); masque[tenus] = False
    coupe = int(0.8 * len(X))
    Xtr, Ytr = X[:coupe][:, masque], X[:coupe][:, tenus]
    Xte, Yte = X[coupe:][:, masque], X[coupe:][:, tenus]

    def r2(Y, P):
        return 1.0 - ((Y - P) ** 2).sum(0) / ((Y - Y.mean(0)) ** 2).sum(0)

    def regression(A, B, lam=10.0):
        Ab = np.hstack([A, np.ones((len(A), 1), np.float32)])
        return np.linalg.solve(Ab.T @ Ab + lam * np.eye(Ab.shape[1], dtype=np.float32), Ab.T @ B)

    W = regression(Xtr, Ytr)
    pred = np.hstack([Xte, np.ones((len(Xte), 1), np.float32)]) @ W
    r2_lin = r2(Yte, pred)

    # les produits : x_i · x_j pour `paires` couples tirés parmi les non-tenus
    # Les colonnes de Xtr/Xte sont celles du masque (0..len(masque)-1), pas les
    # indices d'origine : les paires se tirent dans ce même espace.
    paires = [(int(i), int(j)) for i, j in
              rng.integers(0, masque.sum(), size=(a.paires * 2, 2))]
    paires = [(i, j) for i, j in paires if i != j][:a.paires]

    def produits(Xb):
        return np.stack([Xb[:, i] * Xb[:, j] for i, j in paires], 1).astype(np.float32)

    Ztr = np.hstack([Xtr, produits(Xtr)])
    Zte = np.hstack([Xte, produits(Xte)])
    Wp = regression(Ztr, Ytr)
    predp = np.hstack([Zte, np.ones((len(Zte), 1), np.float32)]) @ Wp
    r2_prod = r2(Yte, predp)

    print(f"  R² linéaire seul        : {r2_lin.mean():.4f}")
    print(f"  R² linéaire + {a.paires} produits : {r2_prod.mean():.4f}")
    gain = float(r2_prod.mean() - r2_lin.mean())
    print(f"  gain des produits       : {gain:+.4f}")
    if gain > 0.02:
        print("  → les produits ajoutent un espace neuf : la piste § 4 du rapport est soutenue")
    else:
        print("  → les produits n'ajoutent presque rien : la piste § 4 n'est pas soutenue ici")


if __name__ == "__main__":
    principal()
